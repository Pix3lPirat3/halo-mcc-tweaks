"""Gametype script (Megalo) player records: the per player records, scores and trait lists are 16 wide, and the random order player list on the stack holds 18 handles. A player index above 15 would read and write the team records behind them. Player references that name such a player now resolve to none, the random order loop skips them, and the trait list reader returns at once, so gametype code only ever sees players 0 to 15."""


def apply(b):
    # player reference resolver 0x1f4724: handle index >= 16 -> none
    cave = b.pcode("""
        mov rbx, qword ptr [rsp + 0x30]
        mov eax, edi
        cmp ax, 0x10
        jb keep
        or eax, -1
        keep:
        jmp 0x1f480b
    """)
    b.hook(0x1f4804, 7, cave)
    # player reference decoder 0x22548c (11 resolver callers): same rule at its single exit
    cave = b.pcode("""
        mov eax, edx
        cmp ax, 0x10
        jb keep
        or eax, -1
        keep:
        add rsp, 0x28
        ret
    """)
    b.hook(0x2255e1, 7, cave)
    # for each player in random order: players of index >= 16 are left out of the 18 entry list
    cave = b.pcode("""
        mov eax, dword ptr [rbp - 0x59]
        cmp ax, 0x10
        jae next
        cmp edi, 0x12
        jge 0xf7002
        lea eax, [rdi + 1]
        movsxd rcx, edi
        jmp 0xf6fea
        next:
        jmp 0xf6ff4
    """)
    b.hook(0xf6fe4, 6, cave)
    # trait list reader 0x1481e0: record array G + 0x2f4 + index * 0xf0 has 16 records, return before touching it
    cave = b.pcode("""
        movzx ecx, dx
        cmp ecx, 0x10
        jb ok
        jmp 0x148261
        ok:
        imul rdi, rcx, 0xf0
        jmp 0x14821c
    """)
    b.hook(0x148212, 10, cave)
