"""Mark queue 4096 entries, null table guards and the index cap used without stack growth."""


def apply(b):
    c = b.code
    # mark queue struct base (rip relative)
    c(0x44aa, "lea rcx, [rva 0x7ef1008]", "lea rcx, [rva 0x28792c8]")
    c(0x44bc, "and dword ptr [rva 0x7ef5208], 0", "and dword ptr [rva 0x287b3c8], 0")
    c(0x44c3, "and dword ptr [rva 0x7ef920c], 0", "and dword ptr [rva 0x287d3cc], 0")
    c(0xa3f2e, "and dword ptr [rva 0x7ef1000], 0", "and dword ptr [rva 0x28792c0], 0")
    c(0xa3f35, "lea rcx, [rva 0x7ef1008]", "lea rcx, [rva 0x28792c8]")
    c(0xa3f3c, "and dword ptr [rva 0x7ef1004], 0", "and dword ptr [rva 0x28792c4], 0")
    c(0xa3f50, "and dword ptr [rva 0x7ef5208], 0", "and dword ptr [rva 0x287b3c8], 0")
    c(0xa3f59, "and dword ptr [rva 0x7ef920c], 0", "and dword ptr [rva 0x287d3cc], 0")
    c(0xcfde0, "mov r8d, dword ptr [rva 0x7ef1004]", "mov r8d, dword ptr [rva 0x28792c4]")
    c(0xcfdea, "mov edi, dword ptr [rva 0x7ef5208]", "mov edi, dword ptr [rva 0x287b3c8]")
    c(0xcfe0b, "lea rbp, [rva 0x7ef1000]", "lea rbp, [rva 0x28792c0]")
    c(0xcfe5a, "mov r8d, dword ptr [rva 0x7ef1004]", "mov r8d, dword ptr [rva 0x28792c4]")
    c(0xcfe64, "mov dword ptr [rva 0x7ef1004], r8d", "mov dword ptr [rva 0x28792c4], r8d")
    c(0xcfeb0, "mov r8d, dword ptr [rva 0x7ef1004]", "mov r8d, dword ptr [rva 0x28792c4]")
    c(0xcfeba, "mov edi, dword ptr [rva 0x7ef5208]", "mov edi, dword ptr [rva 0x287b3c8]")
    c(0xcfedb, "lea rbp, [rva 0x7ef1000]", "lea rbp, [rva 0x28792c0]")
    c(0xcff2a, "mov r8d, dword ptr [rva 0x7ef1004]", "mov r8d, dword ptr [rva 0x28792c4]")
    c(0xcff34, "mov dword ptr [rva 0x7ef1004], r8d", "mov dword ptr [rva 0x28792c4], r8d")
    c(0xcff81, "lea rsi, [rva 0x7ef1000]", "lea rsi, [rva 0x28792c0]")
    c(0xcffe1, "movsxd rcx, dword ptr [rva 0x7ef5208]", "movsxd rcx, dword ptr [rva 0x287b3c8]")
    c(0xcffeb, "mov dword ptr [rva 0x7ef5208], eax", "mov dword ptr [rva 0x287b3c8], eax")
    c(0xcfffb, "movsxd rcx, dword ptr [rva 0x7ef920c]", "movsxd rcx, dword ptr [rva 0x287d3cc]")
    c(0xd0005, "mov dword ptr [rva 0x7ef920c], eax", "mov dword ptr [rva 0x287d3cc], eax")
    c(0xd0017, "inc dword ptr [rva 0x7ef1000]", "inc dword ptr [rva 0x28792c0]")
    c(0xd02fc, "mov qword ptr [rva 0x7ef1000], r10", "mov qword ptr [rva 0x28792c0], r10")
    c(0xd0309, "lea rcx, [rva 0x7ef1008]", "lea rcx, [rva 0x28792c8]")
    c(0xd0318, "mov dword ptr [rva 0x7ef5208], r10d", "mov dword ptr [rva 0x287b3c8], r10d")
    c(0xd031f, "mov dword ptr [rva 0x7ef920c], r10d", "mov dword ptr [rva 0x287d3cc], r10d")
    c(0xd04aa, "mov dword ptr [rva 0x7ef1004], r10d", "mov dword ptr [rva 0x28792c4], r10d")
    c(0xd0a2d, "mov eax, dword ptr [rva 0x7ef5208]", "mov eax, dword ptr [rva 0x287b3c8]")
    c(0xd0a37, "mov r9d, dword ptr [rva 0x7ef1000]", "mov r9d, dword ptr [rva 0x28792c0]")
    c(0xd0ca6, "movsxd rsi, dword ptr [rva 0x7ef920c]", "movsxd rsi, dword ptr [rva 0x287d3cc]")
    c(0xd0e25, "mov eax, dword ptr [rva 0x7ef5208]", "mov eax, dword ptr [rva 0x287b3c8]")
    c(0xd0e2f, "mov r9d, dword ptr [rva 0x7ef1000]", "mov r9d, dword ptr [rva 0x28792c0]")
    c(0xd0cb9, "mov edx, dword ptr [r15 + rbx*4 + 0x7ef520c]", "mov edx, dword ptr [r15 + rbx*4 + 0x287b3cc]")  # mark list B base (absolute)
    # mark bitset clear size 0x100 -> 0x200
    c(0x44b1, "mov r8d, 0x200", "mov r8d, 0x100")
    c(0xa3f45, "mov r8d, 0x200", "mov r8d, 0x100")
    c(0xd0303, "mov r8d, 0x200", "mov r8d, 0x100")
    # mark list A element offset 0x108 -> 0x208
    c(0xcfe2d, "movzx eax, word ptr [rbp + rax*4 + 0x208]", "movzx eax, word ptr [rbp + rax*4 + 0x108]")
    c(0xcfe4e, "mov edx, dword ptr [rbp + rax*4 + 0x208]", "mov edx, dword ptr [rbp + rax*4 + 0x108]")
    c(0xcfefd, "movzx eax, word ptr [rbp + rax*4 + 0x208]", "movzx eax, word ptr [rbp + rax*4 + 0x108]")
    c(0xcff1e, "mov edx, dword ptr [rbp + rax*4 + 0x208]", "mov edx, dword ptr [rbp + rax*4 + 0x108]")
    c(0xcfff1, "mov dword ptr [rsi + rcx*4 + 0x208], r10d", "mov dword ptr [rsi + rcx*4 + 0x108], r10d")
    c(0xd000b, "mov dword ptr [rsi + rcx*4 + 0x420c], edx", "mov dword ptr [rsi + rcx*4 + 0x210c], edx")  # mark list B element offset 0x210c -> 0x420c
    # skip entries whose table pointer is null
    c(0x298947, "jmp 0x5ce7a90; nop*3", "mov rax, qword ptr [rdx + rbp + 0x40d8]")
    c(0x29a693, "jmp 0x5ce7a60; nop*6", "mov rax, qword ptr [rdx + r13 + 0x40d8]; mov dl, bpl")
    c(0x29a7ce, "jmp 0x5ce7ac0; nop*3", "mov rax, qword ptr [rcx + r10 + 0x40d8]")
    # index cap 0x800 for 2 set functions (dropped by stack_growth)
    c(0x2275cc, "jmp 0x5ce7a00; nop; nop", "mov rax, rsp; mov qword ptr [rax + 8], rbx", tag='index_cap')
    c(0x227c08, "jmp 0x5ce7a30", "mov qword ptr [rsp + 8], rbx", tag='index_cap')

    # caves in .gsc
    b.cave(0xa00, """
            cmp dx, 0x800
            nop
            jae L1
            mov rax, rsp
            mov qword ptr [rax + 8], rbx
            jmp 0x2275d3
        L1: ~xor eax, eax
            ret
    """)
    b.cave(0xa30, """
            cmp cx, 0x800
            nop
            jb L1
            or eax, 0xffffffff
            ret
        L1: mov qword ptr [rsp + 8], rbx
            jmp 0x227c0d
    """)
    # null table guard
    b.cave(0xa60, """
            cmp rdx, 0xa8000
            jae 0x29a6c3
            mov rax, qword ptr [rdx + r13 + 0x55ed8e8]
            test rax, rax
            jne L1
            jmp 0x29a6c3
        L1: mov dl, bpl
            jmp 0x29a69e
    """)
    # null table guard
    b.cave(0xa90, """
            cmp rdx, 0xa8000
            jae 0x298974
            mov rax, qword ptr [rdx + rbp + 0x55ed8e8]
            test rax, rax
            jne L1
            jmp 0x298974
        L1: jmp 0x29894f
    """)
    # null table guard
    b.cave(0xac0, """
            cmp rcx, 0xa8000
            jae 0x29a8f7
            mov rax, qword ptr [rcx + r10 + 0x55ed8e8]
            test rax, rax
            jne L1
            jmp 0x29a8f7
        L1: jmp 0x29a7d6
    """)
