"""Player statistics: three functions (0xfa5a0, 0xfa6cc, 0xfe75c) and the first stage of the statistics add function (0xfa458) index a static table with 16 entries by the raw player index. For an index of 16 or more they would read and write past that table. They now return at once for such a player (the read functions give none), so players 16 and up have no statistics. The table itself is not widened. Meant for builds where megalo_records lets the registration of players 16 and up run. Test state: tested offline with scripted players together with megalo_records; not tested in a real lobby yet."""


def apply(b):
    cave = b.pcode("""
        lea eax, [rcx + 1]
        cmp eax, 0x11
        jae bad
        lea eax, [rdx + 1]
        cmp eax, 0x11
        jae bad
        push rbx
        sub rsp, 0x20
        jmp 0xfa5a6
        bad:
        mov eax, 0xffffffff
        ret
    """)
    b.hook(0xfa5a0, 6, cave)
    b.data(0xfa6ea, '83f90f772b', '83f9ff742b')  # cmp ecx, -1; je  becomes  cmp ecx, 0xf; ja
    cave = b.pcode("""
        cmp ecx, 0xf
        ja bad
        movsxd rdi, ecx
        xor r10b, r10b
        jmp 0xfe771
        bad:
        xor r10b, r10b
        jmp 0xfe85b
    """)
    b.hook(0xfe76b, 6, cave)
    b.data(0xfa4b7, '83fa0f773d', '83faff743d')  # the same change in the first stage of 0xfa458
