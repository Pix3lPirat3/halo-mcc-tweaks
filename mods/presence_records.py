"""Per tick presence and score record builder (0x3ebf7c): it writes a float and a 16 byte record per player into a 0x150 byte object, room for 16 players. Index 16 and above wrote past it into the header of the water physics cache, and by player 19 that cache could no longer allocate and the game crashed. The builder now skips such players, and the cache evict scan returns false instead of deleting an invalid entry when it finds nothing."""


def apply(b):
    # builder loop: player index in the word at [rsp + 0x30]
    cave = b.pcode("""
        movzx r14d, word ptr [rsp + 0x30]
        cmp r14d, 0x10
        jb ok
        lea rcx, [rsp + 0x20]
        jmp 0x3ec1e4
        ok:
        jmp 0x3ec08d
    """)
    b.hook(0x3ec087, 6, cave)
    # water cache evict scan 0x93f94: edi == -1 means nothing was found
    cave = b.pcode("""
        cmp edi, -1
        jne ok
        jmp 0x942cc
        ok:
        mov rax, qword ptr [rbx]
        mov edx, edi
        jmp 0x940fc
    """)
    b.hook(0x940f7, 5, cave)
