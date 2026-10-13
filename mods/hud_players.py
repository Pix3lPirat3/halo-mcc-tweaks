"""HUD per player array: the HUD keeps a block of 0xc850 bytes (header and 16 elements of 0xc60) indexed by player index with no bound by the HUD script natives, messages and navigation. Element 16 lands on the user HUD state behind it, which corrupts widget lists and crashes the HUD and motion tracker. The array moves to a 0x19000 byte block in .gsy, 32 elements (0x32000 bytes and 64 elements with the players64 group), and all 18 loops over it run to that count. The game state attach callback is hooked as well so the pointer is not reset to the old block. The block is outside the game state, so a save or revert does not rewind it."""

# (address, instruction for 32 players, original instruction); the loop count 0x20 and the array size 0x18c00 are scaled to the player count
LOOPS = [
    (0x1b1646, 'mov eax, 0x20', 'mov eax, 0x10'), (0x1b16ff, 'cmp r8, 0x20', 'cmp r8, 0x10'), (0x1b177a, 'mov eax, 0x20', 'mov eax, 0x10'),
    (0x1b30d9, 'mov eax, 0x20', 'mov eax, 0x10'), (0x1b3151, 'mov eax, 0x20', 'mov eax, 0x10'), (0x1b31dd, 'mov eax, 0x20', 'mov eax, 0x10'),
    (0x1b3269, 'mov eax, 0x20', 'mov eax, 0x10'), (0x1b32f5, 'mov eax, 0x20', 'mov eax, 0x10'), (0x1b33c5, 'mov eax, 0x20', 'mov eax, 0x10'),
    (0x1b3451, 'mov eax, 0x20', 'mov eax, 0x10'), (0x1b3e2b, 'mov r8d, 0x20', 'mov r8d, 0x10'), (0x1b3ec7, 'mov r8d, 0x20', 'mov r8d, 0x10'),
    (0x1b41ed, 'mov r8d, 0x20', 'mov r8d, 0x10'), (0x2c092c, 'cmp esi, 0x20', 'cmp esi, 0x10'), (0x2c194c, 'cmp edi, 0x20', 'cmp edi, 0x10'),
    (0x2c1b54, 'cmp ebp, 0x20', 'cmp ebp, 0x10'), (0x2c3525, 'mov eax, 0x20', 'mov eax, 0x10'), (0x2c3835, 'cmp rcx, 0x18c00', 'cmp rcx, 0xc600'),
]


def apply(b):
    n = b.nplayers
    blk = b.gsy_grow((0x250 + n * 0xc60 + 0xfff) & ~0xfff)  # 0x250 + n * 0xc60 (0x18e50 for 32), rounded up
    # allocation: the pointer stored at TLS + 0x5b0 is the new block (the old allocation stays unused)
    cave = b.pcode("""
        lea rcx, [rva %#x]
        mov qword ptr [rax + rbx], rcx
        jmp 0x2c068e
    """ % blk)
    b.hook(0x2c0685, 9, cave)
    # game state attach callback: store the new block too
    cave = b.pcode("""
        lea rcx, [rva %#x]
        mov qword ptr [r8 + rax], rcx
        ret
    """ % blk)
    b.hook(0x2b8281, 5, cave)
    for rva, new, was in LOOPS:
        b.code(rva, new.replace('0x18c00', '%#x' % (n * 0xc60)).replace('0x20', '%#x' % n), was)
