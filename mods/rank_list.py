"""Player ranking (0x191860): it appends one handle per player of the datum to a 16 entry list in a 0x80 byte static object, with no bound. With 32 players it already ran over the neighbouring lists and count, and from about 50 players it reached the collision pair cache, which then chained forever and hung the game thread. The append now stops at 16 entries, the stock capacity, so ranking only sees the first 16 players."""


def apply(b):
    cave = b.pcode("""
        movsx rcx, word ptr [rbx + r12 + 0x29bbabc]
        cmp ecx, 0x10
        jge skip
        lea eax, [rcx + r13]
        mov word ptr [rbx + r12 + 0x29bbabc], ax
        mov eax, dword ptr [rbp - 1]
        mov dword ptr [r15 + rcx*4], eax
        skip:
        jmp 0x191942
    """)
    b.hook(0x191925, 29, cave)
