"""Gametype script (Megalo) player records for 128 players. The script state holds one 0xf0 byte record per player for 16 players and 40 instructions index it as index times 0xf0. The script state now grows by 0xec80 bytes (its size is set by the respawn mod, which this mod edits) and records 16 to 127 sit behind the old data: each of the 40 instructions gets a small cave that adds a fixed offset when the index is 16 or more. The six loops that step over the records run 128 times and jump the offset at record 16, the random order player list moves from 18 entries to 128 on a stack frame that is 0x240 bytes bigger, the navpoint mask becomes a bit string (one bit per player, 6 sites), 27 Forge sandbox row instructions (rows are 0x12c bytes) and 5 player variable readers that index by dword get the same offset. It replaces the player guards of the megalo and megalo_callbacks mods and the registration guards of player_records, so build.py leaves those out when this mod is in the list. Gametype scripts then see players 16 to 127, with scores, variables and timers, in the offline tests (Slayer, Juggernaut, Swat, Elite Slayer and Escalation with 64 players, Escalation with 128). Not covered: two instructions in functions with no function record (0x149897 in the respawn rule and 0x147f94 in the free for all team getter) still read the old array, so keep respawn_rule in the build. Test state: tested offline with scripted players, but never as exactly this combination (the dword variable sites were tested together with other mods); not tested in a real lobby yet."""
import struct

OLD_G = 0x11e30  # script state size set by the respawn mod
GROW = 0xec80
# (address, destination, source register) of `imul dst, src, 0xf0` that index the player records
RECORDS = (
    (0xf2fe4, 'rdx', 'rcx'), (0xf3a80, 'r8', 'rdx'), (0xf3dec, 'rdx', 'rcx'), (0xf41b6, 'rcx', 'rdx'),
    (0x1477df, 'rbx', 'rcx'), (0x147d90, 'rcx', 'rcx'), (0x147e39, 'rcx', 'rcx'), (0x147ef8, 'rcx', 'rcx'),
    (0x148215, 'rdi', 'rcx'), (0x1488dd, 'rcx', 'rcx'), (0x148be3, 'rax', 'rdx'), (0x148d6e, 'rbx', 'rax'),
    (0x149f45, 'rax', 'rcx'), (0x149f88, 'rax', 'rcx'), (0x149fbc, 'rax', 'rcx'), (0x149ff0, 'rax', 'rcx'),
    (0x14a024, 'rax', 'rcx'), (0x14a115, 'rax', 'rcx'), (0x14a141, 'rcx', 'rax'), (0x14a172, 'rcx', 'rbp'),
    (0x14a1d2, 'rax', 'rbp'), (0x14a1fe, 'rcx', 'rbp'), (0x14a499, 'rcx', 'rax'), (0x14aa1c, 'rcx', 'rax'),
    (0x14c2da, 'r9', 'r8'), (0x1f16e2, 'rbx', 'rcx'), (0x1f1ad5, 'rbx', 'rdx'), (0x1f1fe2, 'rbx', 'rcx'),
    (0x1f2526, 'rbx', 'r8'), (0x1f299e, 'rdi', 'rdx'), (0x1f2b0c, 'rdx', 'r8'), (0x1f2bd4, 'rsi', 'r8'),
    (0x1f2cb9, 'rcx', 'rax'), (0x1f47e1, 'rax', 'rcx'), (0x1f4923, 'rcx', 'rax'), (0x1f4ccc, 'rax', 'rcx'),
    (0x1f4e51, 'rcx', 'rdx'), (0x1f5323, 'rax', 'rcx'), (0x1f7531, 'r9', 'rdx'), (0x3db244, 'rbx', 'r9'),
)
# (address, destination, source register) of `imul dst, src, 0x12c` that index the Forge sandbox rows
SANDBOX = (
    (0x71019, 'rcx', 'r8'), (0x71121, 'rcx', 'rax'), (0x711e9, 'rcx', 'rax'), (0x71678, 'rcx', 'rdi'), (0x71834, 'rsi', 'rdx'),
    (0x71c9f, 'rbx', 'r8'), (0x7245a, 'rsi', 'r9'), (0x72569, 'rcx', 'rax'), (0x72703, 'rcx', 'rax'), (0x728b0, 'rcx', 'rax'),
    (0x72a24, 'r9', 'r8'), (0x72a9d, 'r8', 'rdx'), (0x72ba0, 'rdi', 'rcx'), (0x72e95, 'r14', 'rbx'), (0x73666, 'rdi', 'rcx'),
    (0x74195, 'r8', 'rcx'), (0x742d5, 'rcx', 'rax'), (0x7462a, 'rcx', 'rax'), (0x746ac, 'rcx', 'rax'), (0x747de, 'r10', 'rax'),
    (0x74847, 'rcx', 'rax'), (0x74891, 'r8', 'rdx'), (0x74b28, 'rdx', 'rax'), (0x74b7f, 'rcx', 'rax'), (0x74cd5, 'rdx', 'rcx'),
    (0x74f13, 'rbx', 'rcx'), (0xc54b0, 'rcx', 'rax'),
)
R32 = {'rax': 'eax', 'rcx': 'ecx', 'rdx': 'edx', 'rbx': 'ebx', 'rsi': 'esi', 'rdi': 'edi', 'rbp': 'ebp'}
R32.update({'r%d' % i: 'r%dd' % i for i in range(8, 16)})


def index_cave(b, sites, factor, ext):
    """imul sites: for an index of 16 or more add ext to the product"""
    for a, dst, src in sites:
        fo = b.rva2fo(a)
        old = bytes(b.img[fo:fo + 7])
        assert old[1] == 0x69 and old[3:] == struct.pack('<I', factor), 'unexpected bytes at 0x%x' % a
        assert not [o for o in b.ops if o['fo'] < fo + 7 and fo < o['fo'] + len(o['new'])], 'patch overlap at 0x%x' % a
        cave = b.pcode("""
            cmp %s, 0x10
            jb small
            imul %s, %s, %#x
            add %s, %#x
            jmp 0x%x
            small:
            imul %s, %s, %#x
            jmp 0x%x
        """ % (R32[src], dst, src, factor, dst, ext, a + 7, dst, src, factor, a + 7))
        b.hook(a, 7, cave)


def window(b, rva, n, text, expect):
    """replace the n bytes at rva (checked against expect) by a jump to a cave with text"""
    fo = b.rva2fo(rva)
    assert bytes(b.img[fo:fo + n]).hex() == expect, 'unexpected bytes at 0x%x' % rva
    b.hook(rva, n, b.pcode(text))


def apply(b):
    assert b.enabled('respawn'), 'the script state size is set by the respawn mod'
    ext = OLD_G - 0x2f4 - 16 * 0xf0  # distance from where the formula puts record 16 to where it now sits
    for rva in (0x785ed, 0x786f5, 0x788ab):  # the three size immediates of the respawn mod
        b.bump(rva, GROW)
    index_cave(b, RECORDS, 0xf0, ext)

    # round clear loop (down counter) 16 -> 128 records
    b.data(0x1471e1, '80000000', '10000000')
    window(b, 0x1471ed, 13, """
        add rdi, 0xf0
        sub rsi, 1
        cmp rsi, 0x70
        jne cont
        add rdi, %#x
        cont:
        test rsi, rsi
        jne 0x1471e5
        jmp 0x1471fa
    """ % ext, '4881c7f00000004883ee0175eb')
    # initialise loop of 0x14cb7c
    window(b, 0x14cbb7, 8, """
        lea esi, [r14 + 0x81]
        mov rax, qword ptr [rax + rdx*8]
        jmp 0x14cbbf
    """, '418d7611488b04d0')
    window(b, 0x14cbfb, 13, """
        add rdi, 0xf0
        sub rsi, 1
        cmp rsi, 0x70
        jne cont
        add rdi, %#x
        cont:
        test rsi, rsi
        jne 0x14cbe7
        jmp 0x14cc08
    """ % ext, '4881c7f00000004883ee0175df')
    # per tick timer loops (up counters)
    for rva, ptr, ctr, top, leave, expect in (
            (0x14d381, 'rdi', 'ebx', 0x14d349, 0x14d38d, '4881c7f000000083fb107cbc'),
            (0x14d736, 'rbx', 'edi', 0x14d70e, 0x14d742, '4881c3f000000083ff107ccc'),
            (0x147379, 'r14', 'esi', 0x147352, 0x147385, '4981c6f000000083fe107ccd')):
        window(b, rva, 12, """
            add %s, 0xf0
            cmp %s, 0x10
            jne cont
            add %s, %#x
            cont:
            cmp %s, 0x80
            jl 0x%x
            jmp 0x%x
        """ % (ptr, ctr, ptr, ext, ctr, top, leave), expect)
    window(b, 0x14cf76, 27, """
        add rsi, 0xf0
        cmp r14d, 0x10
        jne cont
        add rsi, %#x
        cont:
        mov dword ptr [rsp + 0x20], r14d
        mov eax, 0xa0
        cmp r14d, 0x80
        jl 0x14cec5
        jmp 0x14cf91
    """ % ext, '4881c6f0000000' '4489742420' 'b8a0000000' '4183fe10' '0f8c34ffffff')

    # random order list of 0xf6de8: the 18 entry list at [rbp - 0x31] ends at the stack check, it moves to [rsp + 0x40] in a frame grown by 0x240 (128 entries)
    def check(rva, hexs):
        fo = b.rva2fo(rva)
        assert bytes(b.img[fo:fo + len(hexs) // 2]).hex() == hexs, 'unexpected bytes at 0x%x' % rva
    check(0xf6dfd, '4881ecb0000000')
    b.data(0xf6e00, 'f0020000', 'b0000000')
    check(0xf70e5, '4881c4b0000000')
    b.data(0xf70e8, 'f0020000', 'b0000000')
    check(0xf70dd, '488b9c2400010000')
    b.data(0xf70e1, '40030000', '00010000')
    for rva, old, new in ((0xf6ff0, '89448dcf', '89448c40'), (0xf7015, '8b4cb5cf', '8b4cb440'), (0xf701c, '8b4495cf', '8b449440'),
                          (0xf7020, '8944b5cf', '8944b440'), (0xf7027, '894c95cf', '894c9440')):
        b.data(rva, new, old)
    window(b, 0xf703b, 9, """
        mov esi, 0x20
        lea rdi, [rsp + 0x40]
        jmp 0xf7044
    """, 'be20000000488d7dcf')

    # navpoint mask (4 users, one dword each, bit = player index) becomes 4 x 16 bytes at the end of the growth
    off = OLD_G + GROW - 0x40
    window(b, 0x148a95, 11, """
        lea rcx, [r13 + r13]
        bt dword ptr [rax + rcx*8 + %#x], ebp
        jmp 0x148aa0
    """ % off, '428b8ca8c4350000' '0fa3e9')
    window(b, 0x148aec, 11, """
        lea rdx, [r13 + r13]
        bt dword ptr [rax + rdx*8 + %#x], ebp
        jmp 0x148af7
    """ % off, '428b94a8c4350000' '0fa3ea')
    window(b, 0x18b25b, 12, """
        lea r8, [rsi + rsi]
        bt dword ptr [rcx + r8*8 + %#x], edi
        jmp 0x18b267
    """ % off, '448b84b1c4350000' '410fa3f8')
    window(b, 0x77f889, 12, """
        lea rax, [r14 + r14]
        bt dword ptr [rsi + rax*8 + %#x], r15d
        jmp 0x77f895
    """ % off, '428b84b6c4350000' '440fa3f8')
    window(b, 0x7bd6e, 26, """
        lea rcx, [rdx + rdx]
        jne l1
        bts dword ptr [r8 + rcx*8 + %#x], eax
        jmp done
        l1:
        btr dword ptr [r8 + rcx*8 + %#x], eax
        done:
        jmp 0x7bd88
    """ % (off, off), '418b8c90c4350000' '7505' '0fabc1' 'eb03' '0fb3c1' '41898c90c4350000')
    window(b, 0x104fb5, 8, """
        lea rcx, [rbx + rbx]
        and dword ptr [rax + rcx*8 + %#x], 0
        and dword ptr [rax + rcx*8 + %#x], 0
        and dword ptr [rax + rcx*8 + %#x], 0
        and dword ptr [rax + rcx*8 + %#x], 0
        jmp 0x104fbd
    """ % (off, off + 4, off + 8, off + 12), '83a498c435000000')

    # Forge sandbox rows (G + 0x1754 + index * 0x12c): rows 16 to 127 sit at G + OLD_G + 0x6900, behind the player records
    index_cave(b, SANDBOX, 0x12c, OLD_G + 0x6900 - 0x1754 - 16 * 0x12c)

    # player variables read by dword index [G + 0x308 + (index * 0x3c + var) * 4]: from 16 * 0x3c on the offset is added (in dwords)
    ext4 = ext // 4
    assert ext % 4 == 0
    for rva, first, reg, tail, back, expect in (
            (0x1464ea, ['mov r9d, 0x20', 'add r8, rax'], 'r8', [], 0x1464f3, '41b920000000' '4c03c0'),
            (0x146bbd, ['add r8, rcx', 'mov r9d, 0x20'], 'r8', [], 0x146bc6, '4c03c1' '41b920000000'),
            (0x1f53be, ['mov r9d, 0x20', 'add r8, rax'], 'r8', [], 0x1f53c7, '41b920000000' '4c03c0'),
            (0x1f55db, ['add r8, rcx'], 'r8', ['mov r10d, 0x20'], 0x1f55e4, '4c03c1' '41ba20000000'),
            (0x1f6be0, ['mov r9d, 0x20', 'add rbx, rax'], 'rbx', [], 0x1f6be9, '41b920000000' '4803d8')):
        lines = first + ['cmp %s, 960' % reg, 'jb cont', 'add %s, %#x' % (reg, ext4), 'cont:'] + tail + ['jmp 0x%x' % back]
        window(b, rva, 9, '\n'.join(lines), expect)
