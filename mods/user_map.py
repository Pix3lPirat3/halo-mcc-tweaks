"""Player to local user map: the block that maps a player index to a local user slot (and back) holds 16 entries and a 16 byte mask table of which local users belong to a player. Both are widened to 32 players (block 0xe8 -> 0x178 bytes). With the stock mask table a player past 15 reads another table, is taken for a local user, and view, HUD and first person effects of that player go to the host."""
import core


def apply(b):
    d = b.data
    d(0x43550, "78010000", "e8000000")  # block size 0xe8 -> 0x178
    # setter 0x539cc: the second table moves behind the 32 byte mask table, index shift 0x1d -> 0x21
    d(0x539fb, '410fb7ee' '83c521' '4e8b3cc0' '440fb7c1' '4d69e890040000' '4d8b4f18' '4863fa' '4d036950' '498b9f58010000' '9090909090',
      '41b918000000' '410fb7ee' '4e8b3cc0' '440fb7c1' '4d69e890040000' '4f8b0c39' 'b958010000' '4863fa' '4d036950' '4a8b1c39')
    # accessor 0x53b5c, same shift
    d(0x53b72, '0fb7c9' '83c121' '4c8b04d0' '498b8058010000',
      '41b958010000' '0fb7c9' '4c8b04d0' '4b8b0408')
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
