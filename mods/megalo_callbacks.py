"""Gametype script (Megalo) per player callbacks: they run every tick for every player of the datum and look up the player in a record array with 16 records. Two of them (0x149e74 and 0x14a060) now treat an index of 16 or more as an invalid player and leave through their own exit, and the one that stores a byte into the record (0x14c2b8) skips that store. Two functions write into the same area for an index of 16 or more and are guarded too: the record initialiser (0x147ec8, it clears a whole 0xf0 byte record) and the player index change (0x147d68, it copies one record onto another), and so are three that read it (the update loop 0x14753c and the two navpoint functions 0x14888e and 0x148b87). The other readers (0x148cf8, 0x14a250, 0x14a7c4) are not guarded, they only read."""


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
    # record writers and readers: index 16 and up leave through the function's own exit
    def guard(rva, n, text, expect):
        fo = b.rva2fo(rva)
        assert b.img[fo:fo + n].hex() == expect, 'unexpected bytes at 0x%x' % rva
        b.hook(rva, n, b.pcode(text))
    guard(0x147ec8, 7, """
        cmp edx, 0x10
        jae 0x147ec4
        sub rsp, 0x28
        mov r8d, edx
        jmp 0x147ecf
    """, '4883ec28448bc2')
    guard(0x147d68, 7, """
        cmp dx, 0x10
        jae 0x147ec4
        cmp r8w, 0x10
        jae 0x147ec4
        sub rsp, 0xf8
        jmp 0x147d6f
    """, '4881ecf8000000')
    guard(0x1477c8, 6, """
        mov esi, dword ptr [rsp + 0x50]
        cmp si, 0x10
        jae 0x1478fe
        mov ecx, esi
        jmp 0x1477ce
    """, '8b7424508bce')
    guard(0x14888e, 9, """
        cmp eax, -1
        je 0x148afa
        cmp ebp, 0x10
        jae 0x148afa
        jmp 0x148897
    """, '83f8ff0f8463020000')
    guard(0x148b87, 10, """
        mov bl, al
        test al, al
        je 0x148ccd
        cmp si, 0x10
        jb ok
        xor ebx, ebx
        jmp 0x148ccd
        ok:
        jmp 0x148b91
    """, '8ad884c00f843c010000')
