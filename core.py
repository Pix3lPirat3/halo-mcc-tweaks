"""Patch engine: image access, assembly helpers, patch recording, PE layout, verification."""
import hashlib
import re
import struct

import capstone
import keystone

ORIG_SHA = '738dd2d24ea3aea12e1ee9aa4a61094bf116027d42004c35a19e5048608b0894'
IMAGE_BASE = 0x180000000
FILE_ALIGN = 0x200
GSC_VA = 0x5ce7000   # code caves and info blocks (file backed)
GSC_SIZE = 0xe00
GSX_VA = 0x4eda000   # havok heap and placement extras (uninitialised)
GSY_VA = 0x5ce8000   # object tables, save queue, draw pools (uninitialised)
GSY_SIZE = 0x2ca3000

_CS = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
_KS = keystone.Ks(keystone.KS_ARCH_X86, keystone.KS_MODE_64)
_RIP = re.compile(r'\[rip ([+-]) (0x[0-9a-f]+)\]')
_RVA = re.compile(r'\[rva (0x[0-9a-f]+)\]')
# canonical multi byte nops (the assembler cannot emit them)
_NOPS = {2: '66 90', 3: '0f 1f 00', 4: '0f 1f 40 00', 5: '0f 1f 44 00 00', 6: '66 0f 1f 44 00 00',
         7: '0f 1f 80 00 00 00 00', 8: '0f 1f 84 00 00 00 00 00', 9: '66 0f 1f 84 00 00 00 00 00'}
_NOPB = {bytes.fromhex(v.replace(' ', '')): k for k, v in _NOPS.items()}


def hx(s):
    return bytes.fromhex(s.replace(' ', ''))


def sections(img):
    pe = struct.unpack_from('<I', img, 0x3c)[0]
    n = struct.unpack_from('<H', img, pe + 6)[0]
    base = pe + 24 + struct.unpack_from('<H', img, pe + 20)[0]
    out = []
    for i in range(n):
        name, vs, va, rs, rp = struct.unpack_from('<8sIIII', img, base + 40 * i)
        out.append((name.rstrip(b'\0').decode(), va, vs, rp, rs))
    return out


def _insn_text(i):
    raw = bytes(i.bytes)
    if i.mnemonic == 'nop' and raw in _NOPB:
        return 'nop%d' % _NOPB[raw]
    s = (i.mnemonic + ' ' + i.op_str).strip()

    def rep(m):
        d = int(m.group(2), 16)
        return '[rva 0x%x]' % (i.address + i.size + (d if m.group(1) == '+' else -d))
    return _RIP.sub(rep, s)


def dis(buf, rva):
    """text of the instructions in buf, or None when buf does not end on an instruction boundary"""
    out, pos = [], 0
    while pos < len(buf):
        i = next(_CS.disasm(bytes(buf[pos:pos + 16]), rva + pos), None)
        if i is None or pos + i.size > len(buf):
            return None
        out.append(_insn_text(i))
        pos += i.size
    return '; '.join(out)


def _stmts(text):
    out = []
    for line in text.split('\n'):
        line = line.split('#')[0].strip()
        for s in line.split(';'):
            s = s.strip()
            while s:
                m = re.match(r'^(\w+):\s*(.*)$', s)
                if not m:
                    break
                out.append(('label', m.group(1)))
                s = m.group(2)
            m = re.fullmatch(r'nop\*(\d+)', s)
            if m:
                out += [('ins', 'nop')] * int(m.group(1))
            elif s:
                out.append(('ins', s))
    return out


def _alt(b):
    """the other encoding of a register to register instruction (opcode direction bit, swapped modrm and rex fields)"""
    k = 1 if b[0] == 0x66 else 0
    rex = b[k] if 0x40 <= b[k] <= 0x4f else None
    j = k + (rex is not None)
    assert len(b) == j + 2 and b[j + 1] >> 6 == 3, 'no alternate encoding'
    m = b[j + 1]
    out = bytearray(b)
    out[j] ^= 2
    out[j + 1] = 0xc0 | (m & 7) << 3 | (m >> 3) & 7
    if rex is not None:
        out[k] = rex & 0xfa | (rex & 1) << 2 | (rex >> 2) & 1
    return bytes(out)


_STORE = {0x00, 0x01, 0x08, 0x09, 0x10, 0x11, 0x18, 0x19, 0x20, 0x21, 0x28, 0x29, 0x30, 0x31, 0x38, 0x39, 0x88, 0x89}


def _flippable(b):
    k = 1 if b[0] == 0x66 else 0
    j = k + (0x40 <= b[k] <= 0x4f)
    return len(b) == j + 2 and b[j] in _STORE and b[j + 1] >> 6 == 3


def asm(text, addr):
    """assemble text at addr: labels, [rva X] for rip relative operands, nopN for multi byte nops.
    Register to register ALU and mov use the load form opcode (as compilers emit); ~op selects the store form."""
    st = _stmts(text)
    ins_idx = [s for kind, s in st if kind == 'ins']

    def render(disps):
        lines, k = [], 0
        for kind, s in st:
            if kind == 'label':
                lines.append(s + ':')
                continue
            s = s.lstrip('~')
            m = re.fullmatch(r'nop(\d)', s)
            if m:
                s = '.byte ' + ','.join('0x' + x for x in _NOPS[int(m.group(1))].split())
            m = _RVA.search(s)
            if m:
                d = disps.get(k, 0x7fff0)
                s = s.replace(m.group(0), '[rip %s 0x%x]' % ('+' if d >= 0 else '-', abs(d)))
            lines.append(s)
            k += 1
        return chr(10).join(lines)
    enc = bytes(_KS.asm(render({}), addr)[0])
    if any(_RVA.search(s) for s in ins_idx):
        ins = list(_CS.disasm(enc, addr))
        assert len(ins) == len(ins_idx), 'statement count differs from decoded count'
        disps = {}
        for k, (s, i) in enumerate(zip(ins_idx, ins)):
            m = _RVA.search(s)
            if m:
                disps[k] = int(m.group(1), 16) - (i.address + i.size)
        enc = bytes(_KS.asm(render(disps), addr)[0])
    ins = list(_CS.disasm(enc, addr))
    assert len(ins) == len(ins_idx), 'statement count differs from decoded count'
    out = bytearray(enc)
    for s, i in zip(ins_idx, ins):
        if not s.startswith('~') and _flippable(bytes(i.bytes)):
            o = i.address - addr
            out[o:o + i.size] = _alt(bytes(i.bytes))
    enc = bytes(out)
    return enc


class Build:
    def __init__(self, img, mods):
        self.img = bytes(img)
        self.secs = sections(self.img)
        self.mods = list(mods)
        self.ops = []
        self.gsc = bytearray(b'\xcc' * GSC_SIZE)
        self.gsc_used = []
        self.cur = None
        self.gsy_size = GSY_SIZE

    def enabled(self, name):
        return name in self.mods

    def rva2fo(self, rva):
        for _, va, vs, rp, rs in self.secs:
            if va <= rva < va + rs:
                return rva - va + rp
        raise ValueError('rva 0x%x is not file backed' % rva)

    def _add(self, fo, new, was, tag):
        was_b = self.img[fo:fo + len(new)]
        if was is not None and was_b != was:
            raise SystemExit('unexpected original bytes at file offset 0x%x (%s, expected %s)' % (fo, was_b.hex(), was.hex()))
        self.ops.append(dict(fo=fo, new=new, was=was_b, tag=tag, mod=self.cur))

    def code(self, rva, new, was, tag=None):
        """replace instructions at rva; was is the expected original assembly"""
        enc = asm(new, rva)
        fo = self.rva2fo(rva)
        orig = self.img[fo:fo + len(enc)]
        if dis(orig, rva) != was and asm(was, rva) != orig:
            raise SystemExit('unexpected original code at 0x%x: %s (expected %s)' % (rva, dis(orig, rva), was))
        self._add(fo, enc, None, tag)

    def pad(self, rva, new, tag=None):
        """place code into 0xcc padding of the original image"""
        enc = asm(new, rva)
        self._add(self.rva2fo(rva), enc, b'\xcc' * len(enc), tag)

    def data(self, rva, new, was, tag=None):
        self._add(self.rva2fo(rva), hx(new), hx(was), tag)

    def raw(self, fo, new, was, tag=None):
        self._add(fo, hx(new), hx(was), tag)

    def _gsc_put(self, off, b):
        end = off + len(b)
        assert end <= GSC_SIZE, 'gsc overflow'
        for a, e in self.gsc_used:
            assert end <= a or off >= e, 'gsc overlap at 0x%x' % off
        self.gsc_used.append((off, end))
        self.gsc[off:end] = b

    def cave(self, off, text):
        """code in the .gsc section at offset off"""
        self._gsc_put(off, asm(text, GSC_VA + off))

    def blob(self, off, b):
        self._gsc_put(off, bytes(b))

    def gsy_grow(self, n):
        """append n zero bytes to .gsy and return the rva of the new block"""
        va = GSY_VA + self.gsy_size
        self.gsy_size += n
        return va

    def drop(self, tag):
        """remove the patches of another mod that carry this tag"""
        self.ops = [o for o in self.ops if o['tag'] != tag]

    def replace(self, tag, new):
        """change the new bytes of a tagged patch"""
        hit = [o for o in self.ops if o['tag'] == tag]
        assert len(hit) == 1 and len(hit[0]['new']) == len(hx(new))
        hit[0]['new'] = hx(new)

    def finish(self):
        ops = sorted(self.ops, key=lambda o: o['fo'])
        for a, b in zip(ops, ops[1:]):
            if b['fo'] < a['fo'] + len(a['new']):
                raise SystemExit('overlapping patches at 0x%x (%s, %s)' % (b['fo'], a['mod'], b['mod']))
        out = bytearray(self.img)
        for o in ops:
            out[o['fo']:o['fo'] + len(o['new'])] = o['new']
        ptr = (len(out) + FILE_ALIGN - 1) & ~(FILE_ALIGN - 1)
        out += b'\0' * (ptr - len(out))
        out += self.gsc
        self.patches = ops
        return bytes(out)


def verify_pe(img):
    """structural PE check: section order, alignment, SizeOfImage, header room"""
    pe = struct.unpack_from('<I', img, 0x3c)[0]
    n = struct.unpack_from('<H', img, pe + 6)[0]
    osz = struct.unpack_from('<H', img, pe + 20)[0]
    opt = pe + 24
    salign = struct.unpack_from('<I', img, opt + 32)[0]
    soi, soh = struct.unpack_from('<II', img, opt + 56)
    tab = opt + osz
    prev = 0
    for i in range(n):
        o = tab + 40 * i
        vs, va, rs, rp = struct.unpack_from('<IIII', img, o + 8)
        assert va >= prev and va % salign == 0, 'section %d misplaced' % i
        assert rp + rs <= len(img), 'section %d beyond file' % i
        prev = (va + vs + salign - 1) // salign * salign
    assert soi == prev, 'SizeOfImage 0x%x != 0x%x' % (soi, prev)
    assert tab + 40 * n <= soh, 'section table too large'
    return n, soi


def sha(b):
    return hashlib.sha256(b).hexdigest()
