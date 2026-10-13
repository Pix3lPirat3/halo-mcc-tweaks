"""Gametype script (Megalo) per player callbacks: they run every tick for every player of the datum and look up the player in a record array with 16 records. Two of them (0x149e74 and 0x14a060) now treat an index of 16 or more as an invalid player and leave through their own exit, and the one that stores a byte into the record (0x14c2b8) skips that store. Other readers of the same array (0x14885c, 0x148b1c, 0x14753c, 0x147d68, 0x147ec8, 0x148cf8, 0x14a250, 0x14a7c4) are not guarded, they only read."""


def apply(b):
    for rva, exit_rva in ((0x149eec, 0x14a043), (0x14a0be, 0x14a232)):
        cave = b.pcode("""
            cmp r8d, 0x10
            jge 0x%x
            cmp r8d, dword ptr [rcx + 0x44]
            jge 0x%x
            jmp 0x%x
        """ % (exit_rva, exit_rva, rva + 10))
        b.hook(rva, 10, cave)
    cave = b.pcode("""
        cmp r8d, 0x10
        jae skip
        mov byte ptr [rax + r9 + 0x369], dl
        skip:
        jmp 0x14c2f0
    """)
    b.hook(0x14c2e8, 8, cave)
