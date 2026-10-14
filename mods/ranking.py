"""Ranking for 128 players (the standings function 0x191860). The stock players section lists and ranks 16 players, and rank_list only cuts it at 16. This replaces the players section by a version that walks the whole players datum (128), sorts it with the game's own sort and compare functions, gives tied players the same code, and writes 16 bit place codes by player index into a 0x1000 byte table in .gsy (one 0x308 byte entry per ruleset). The old 16 entry object still gets the top 16 players, with codes cut at 0x7e, and the single player place lookup (0x19171c) reads the new table. Needs score_block, the compare reads scores by player index. Test state: place codes followed the scores for 128 scripted players in Slayer offline; not tested in a real lobby yet."""


def apply(b):
    if b.nplayers < 128:
        return
    assert b.enabled('score_block'), 'ranking needs score_block'
    blk = b.gsy_grow(0x1000)
    cave = b.pcode("""
        imul r9, r13, 0x308
        lea rsi, [rva %#x]
        add rsi, r9
        mov dword ptr [rsi + 4], 0
        mov eax, 0x18
        mov rcx, qword ptr [rax + rdi]
        mov qword ptr [rbp - 9], rcx
        or eax, 0xffffffff
        mov dword ptr [rbp + 3], eax
        mov dword ptr [rbp - 1], eax
        lea rcx, [rbp - 9]
        call 0x1381c
        mov qword ptr [rbp - 0x11], rax
        test rax, rax
        je q_done1
        q_loop1:
        mov eax, dword ptr [rbp - 1]
        mov ecx, dword ptr [rsi + 4]
        cmp ecx, 128
        jae q_skip1
        mov dword ptr [rsi + rcx*4 + 8], eax
        inc dword ptr [rsi + 4]
        q_skip1:
        lea rcx, [rbp - 9]
        call 0x1381c
        mov qword ptr [rbp - 0x11], rax
        test rax, rax
        jne q_loop1
        q_done1:
        lea rdi, [rsi + 0x208]
        mov ecx, 64
        mov eax, 0xffffffff
        rep stosd
        mov rax, qword ptr [rbp - 0x29]
        mov qword ptr [rbp - 0x21], rax
        mov byte ptr [rbp - 0x19], 0
        lea rcx, [rsi + 8]
        mov edx, dword ptr [rsi + 4]
        lea r8, [rva 0x1924dc]
        lea r9, [rbp - 0x21]
        call 0x689724
        xor r12d, r12d
        q_outer:
        cmp r12d, dword ptr [rsi + 4]
        jge q_groupsdone
        lea r13d, [r12 + 1]
        q_inner:
        cmp r13d, dword ptr [rsi + 4]
        jge q_endgroup
        mov ecx, dword ptr [rsi + r13*4 + 8]
        mov edx, dword ptr [rsi + r13*4 + 4]
        mov r8, qword ptr [rbp - 0x29]
        xor r9d, r9d
        call 0x1923e0
        test eax, eax
        jne q_endgroup
        inc r13d
        jmp q_inner
        q_endgroup:
        mov eax, r13d
        sub eax, r12d
        xor ecx, ecx
        cmp eax, 1
        seta cl
        lea ecx, [rcx + r12*2]
        mov edx, r12d
        q_fill:
        cmp edx, r13d
        jge q_nextgroup
        movzx eax, word ptr [rsi + rdx*4 + 8]
        mov word ptr [rsi + rax*2 + 0x208], cx
        inc edx
        jmp q_fill
        q_nextgroup:
        mov r12d, r13d
        jmp q_outer
        q_groupsdone:
        mov r15, qword ptr [rbp + 7]
        mov eax, dword ptr [rsi + 4]
        cmp eax, 16
        jbe q_nolimit
        mov eax, 16
        q_nolimit:
        xor edx, edx
        q_leg:
        cmp edx, eax
        jge q_legdone
        mov ecx, dword ptr [rsi + rdx*4 + 8]
        mov dword ptr [r15 + rdx*4], ecx
        movzx r9d, cx
        movzx r8d, word ptr [rsi + r9*2 + 0x208]
        cmp r8d, 0x7e
        jbe q_c1
        mov r8d, 0x7e
        q_c1:
        mov byte ptr [r15 + rdx + 0x60], r8b
        inc edx
        jmp q_leg
        q_legdone:
        mov word ptr [r15 + 0x78], ax
        mov rsi, qword ptr [rbp + 0x67]
        mov rdi, qword ptr [rbp - 0x31]
        mov r14, qword ptr [rbp - 0x29]
        mov r13d, dword ptr [rbp + 0x6f]
        mov rbx, r13
        shl rbx, 7
        lea r12, [rva 0x0]
        xor r11d, r11d
        jmp 0x191ab5
    """ % blk)
    b.hook(0x1918f7, 5, cave)
    # place lookup 0x19171c: read the 16 bit code of the new table after the call of 0x191860
    cave = b.pcode("""
        or ecx, 0xffffffff
        movzx r8d, di
        cmp r8d, 128
        jae done
        movsxd rax, dword ptr [rsp + 0x9c]
        imul rax, rax, 0x308
        lea rdx, [rva %#x]
        add rax, rdx
        movzx eax, word ptr [rax + r8*2 + 0x208]
        cmp eax, 0xffff
        je done
        mov ecx, eax
        done:
        jmp 0x1917c1
    """ % blk)
    b.hook(0x191790, 9, cave)
    # keep the ruleset across the call of 0x191860 (r9 is volatile)
    cave = b.pcode("""
        mov edx, r9d
        mov dword ptr [rsp + 0x9c], r9d
        lea rcx, [rsp + 0x20]
        jmp 0x19178b
    """)
    b.hook(0x191783, 8, cave)
