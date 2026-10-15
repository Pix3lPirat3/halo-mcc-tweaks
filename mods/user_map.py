"""Player to local user map: the block that maps a player index to a local user slot (and back) holds 16 entries and a 16 byte mask table of which local users belong to a player. Both are widened to 32 players (block 0xe8 -> 0x178 bytes). With the stock mask table a player past 15 reads another table, is taken for a local user, and view, HUD and first person effects of that player go to the host. With the players64 group the block is 0x298 bytes: both index tables get 64 entries, the count, user and mask fields behind them move up by 0x80 (29 instructions carry the new offsets) and the block initialiser is replaced. With players128 the second table sits right behind the first and the block is 0x4d8 bytes (the fields move up by 0x380)."""
import core
import struct

# instructions that address the fields behind the first table: (address, displacement before)
MOVED = [
    (0x53dbb, 0xb8), (0x53df6, 0xb8), (0x53e28, 0xb8), (0x53ef0, 0xb8), (0x53fbf, 0xb8), (0x54010, 0xb8),
    (0x53f20, 0xc8), (0x540b0, 0xc8), (0x540df, 0xc8), (0x5413b, 0xc8), (0x4c69d4, 0xc8),
    (0x53de4, 0xd8), (0x53def, 0xd8), (0x53e2f, 0xd8), (0x53e3a, 0xd8), (0x53e94, 0xd8), (0x53f4d, 0xd8),
    (0x53dfe, 0xb4), (0x53e41, 0xb4), (0x2d5d9, 0xb4), (0x44065, 0xb4), (0xb7ddb, 0xb4), (0xbeb8a, 0xb4), (0xc3117, 0xb4), (0xc8591, 0xb4), (0xc8675, 0xb4),
    (0x2c5f93, 0xb4), (0x35d25b, 0xb4), (0x35d7d6, 0xb4), (0x35d847, 0xb4),
]


def apply(b):
    d = b.data
    n = b.nplayers
    wide = n > 32
    huge = n > 64  # a layout with the second table right behind the first, for any count from 65 up
    if huge:
        sh = 8 * n - 0x80  # shift of the fields behind the first table
        cb, wb = 0x34 + 4 * n, 0x34 + 8 * n
        mb = wb + 0x24
        size = (mb + n + 7) & ~7
        d(0x43550, size.to_bytes(4, 'little').hex(), "e8000000")  # block size 0xe8 -> 0x4d8 for 128
        shift = '%02x' % (n - 16)
    else:
        d(0x43550, "98020000" if wide else "78010000", "e8000000")  # block size 0xe8 -> 0x298 or 0x178
        shift = '49' if wide else '21'  # dword index of the second table in the block (0x1d stock)
    # setter 0x539cc: the second table moves behind the mask table
    d(0x539fb, '410fb7ee' '83c5' + shift + '4e8b3cc0' '440fb7c1' '4d69e890040000' '4d8b4f18' '4863fa' '4d036950' '498b9f58010000' '9090909090',
      '41b918000000' '410fb7ee' '4e8b3cc0' '440fb7c1' '4d69e890040000' '4f8b0c39' 'b958010000' '4863fa' '4d036950' '4a8b1c39')
    # accessor 0x53b5c, same shift
    d(0x53b72, '0fb7c9' '83c1' + shift + '4c8b04d0' '498b8058010000',
      '41b958010000' '0fb7c9' '4c8b04d0' '4b8b0408')
    if wide:
        for addr, disp in MOVED:
            fo = b.rva2fo(addr)
            old = struct.pack('<i', disp)
            k = bytes(b.img[fo:fo + 15]).find(old)
            assert 0 < k < 11, 'displacement 0x%x not found at 0x%x' % (disp, addr)
            d(addr + k, struct.pack('<i', disp + (sh if huge else 0x80)).hex(), old.hex())
        if huge:
            # initialiser 0x53900 (the whole function) replaced: B[n] at +0x34, C[n] behind it, then the count, user and mask fields
            cave = b.pcode("""
                push rbx
                push rdi
                push rsi
                sub rsp, 0x20
                xor edx, edx
                mov ecx, dword ptr [rva 0xc17b18]
                mov rax, qword ptr gs:[rdx + 0x58]
                mov rax, qword ptr [rax + rcx*8]
                mov edi, 0x158
                mov rdi, qword ptr [rdi + rax]
                or rbx, -1
                mov dword ptr [rdi], 0
                mov qword ptr [rdi + 4], rbx
                mov qword ptr [rdi + 0xc], rbx
                mov qword ptr [rdi + 0x14], rbx
                mov qword ptr [rdi + 0x1c], rbx
                mov qword ptr [rdi + 0x24], rbx
                mov qword ptr [rdi + 0x2c], rbx
                lea rcx, [rdi + 0x34]
                mov edx, ebx
                mov r8d, %#x
                call 0x78932a
                lea rcx, [rdi + %#x]
                mov edx, ebx
                mov r8d, %#x
                call 0x78932a
                xor eax, eax
                mov word ptr [rdi + %#x], ax
                mov qword ptr [rdi + %#x], rbx
                mov qword ptr [rdi + %#x], rbx
                mov qword ptr [rdi + %#x], rbx
                mov qword ptr [rdi + %#x], rbx
                lea rcx, [rdi + %#x]
                xor edx, edx
                mov r8d, %#x
                call 0x78932a
                add rsp, 0x20
                pop rsi
                pop rdi
                pop rbx
                ret
            """ % (4 * n, cb, 4 * n, wb, wb + 4, wb + 12, wb + 20, wb + 28, mb, n))
            b.hook(0x53900, 5, cave)
            return
        # initialiser 0x53900 (the whole function) replaced: B and C filled with -1, count, user and mask fields cleared
        cave = b.pcode("""
            push rbx
            push rdi
            push rsi
            sub rsp, 0x20
            xor edx, edx
            mov ecx, dword ptr [rva 0xc17b18]
            mov rax, qword ptr gs:[rdx + 0x58]
            mov rax, qword ptr [rax + rcx*8]
            mov edi, 0x158
            mov rdi, qword ptr [rdi + rax]
            or rbx, -1
            mov dword ptr [rdi], 0
            mov qword ptr [rdi + 4], rbx
            mov qword ptr [rdi + 0xc], rbx
            mov qword ptr [rdi + 0x14], rbx
            mov qword ptr [rdi + 0x1c], rbx
            mov qword ptr [rdi + 0x24], rbx
            mov qword ptr [rdi + 0x2c], rbx
            lea rcx, [rdi + 0x34]
            mov edx, ebx
            mov r8d, 0x100
            call 0x78932a
            xor eax, eax
            mov word ptr [rdi + 0x134], ax
            mov qword ptr [rdi + 0x138], rbx
            mov qword ptr [rdi + 0x140], rbx
            mov qword ptr [rdi + 0x148], rbx
            mov qword ptr [rdi + 0x150], rbx
            lea rcx, [rdi + 0x158]
            xor edx, edx
            mov r8d, 0x40
            call 0x78932a
            lea rcx, [rdi + 0x198]
            mov edx, ebx
            mov r8d, 0x100
            call 0x78932a
            add rsp, 0x20
            pop rsi
            pop rdi
            pop rbx
            ret
        """)
        b.hook(0x53900, 5, cave)
        return
    # init of the tail: zero the 32 mask bytes, fill the second table (32 dwords) with -1
    cave = b.pcode("""
        mov qword ptr [rdi], r14
        mov qword ptr [rdi + 8], r14
        mov qword ptr [rdi + 0x10], r14
        mov qword ptr [rdi + 0x18], r14
        lea rcx, [rdi + 0x20]
        mov edx, ebx
        mov r8d, 0x80
        call 0x78932a
        jmp 0x539b8
    """)
    d(0x539a0, core.asm('jmp 0x%x' % cave, 0x539a0).hex() + '90' * 19,
      '40f6c703' '7509' '4c8937' '4c897708' 'eb09' '33c0' '488907' '48894708')
