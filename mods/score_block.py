"""Score block (returned by 0x80634): the engine keeps the scores of a game in one block with 16 player entries of 8 bytes, then 8 team entries at +0x80, then dirty flags and a 24 entry array (0x354 bytes in all). A player of index 16 or more landed on the team scores and the flags. With 128 players one kill ended a Slayer game at once, because the score limit check read those bytes as a score (end reason 6). With players128 the function now returns a block of its own (0x1000 bytes) with 128 player entries at the start, the instructions that address the team scores, flags and array use displacements moved up by 0x380, the team start index of the snapshot function moves with them, and the clear at the start of a round covers the new size. The block is outside the saved game state, so a revert would not restore it (hypothesis, not tested). Scores of players 16 and up change only when megalo_records is in the build. Test state: tested offline with scripted players (Forge, and Slayer at 128 with kills); not tested in a real lobby yet."""
import struct

# (address of the instruction, displacement before): fields behind the 16 player entries
MOVED = (
    (0x79a98, 0x86), (0x79aa2, 0x82), (0x79aad, 0x80), (0x79ab6, 0x82), (0x79ac5, 0x80), (0x79fa6, 0x80), (0x7a02c, 0x84), (0x7b487, 0x84),
    (0x7d058, 0xc0), (0x7d59b, 0x82), (0x7d5fc, 0x82), (0x7d907, 0xc0), (0x7d913, 0x188), (0x7debb, 0x80),
    (0x80431, 0x80), (0x80439, 0x80), (0x80445, 0x84), (0x8044d, 0x84), (0x80457, 0x84), (0x8045f, 0x84), (0x8046b, 0x82), (0x80473, 0x82),
    (0x146ab2, 0x80), (0x14769a, 0xc0), (0x18a62d, 0x80),
    (0x1922a0, 0x82), (0x1922a9, 0x82), (0x1922b4, 0x80), (0x1922bd, 0x80), (0x1922c8, 0x84), (0x1922d1, 0x84),
    (0x1f112a, 0x80), (0x30d80d, 0x188), (0x30d83f, 0x188), (0x459855, 0xc8),
    # functions that take the block pointer as an argument: 0x18f54c (mark all dirty), 0x18f5a8 (team loop), 0x18f6e8 (snapshot apply), 0x18f974 (team score add)
    (0x18f561, 0xc0), (0x18f576, 0xc8), (0x18f649, 0x86), (0x18f79f, 0xc8), (0x18f81a, 0x148), (0x18f994, 0x80), (0x18f9c8, 0x80), (0x18f9ee, 0x80),
)
SHIFT = 0x380


def apply(b):
    if b.nplayers < 128:
        return
    blk = b.gsy_grow(0x1000)
    cave = b.pcode("""
        lea rcx, [rva %#x]
        jmp 0x80678
    """ % blk)
    b.hook(0x80671, 7, cave)
    for addr, disp in MOVED:
        fo = b.rva2fo(addr)
        raw = bytes(b.img[fo:fo + 15])
        old = struct.pack('<i', disp)
        k = raw.find(old)
        assert 0 < k < 11, 'displacement 0x%x not found at 0x%x' % (disp, addr)
        b.data(addr + k, struct.pack('<i', disp + SHIFT).hex(), old.hex())
    # snapshot apply 0x18f6e8: first team word index 0x40 (byte 0x80) -> 0x200 (byte 0x400)
    b.data(0x18f822, struct.pack('<i', 0x200).hex(), '40000000')
    # clear at round start (0x78a1e to 0x78a56): players and teams 0x440 bytes, the 24 entry array at +0x448, the flags at +0x440 and +0x508
    cave = b.pcode("""
        mov r8d, 0x440
        xor edx, edx
        mov rcx, rdi
        call 0x78932a
        lea rcx, [rdi + 0x448]
        mov r8d, 0xc0
        xor edx, edx
        call 0x78932a
        mov byte ptr [rdi + 0x440], r15b
        mov r14d, 1
        mov byte ptr [rdi + 0x508], r15b
        jmp 0x78a56
    """)
    b.hook(0x78a1e, 56, cave)
