"""Per-frame render registration pools 1024 -> 4096 entries."""


def apply(b):
    c = b.code
    # pool array address (rip relative)
    c(0x14ead3, "lea rbx, [rva 0x7efa000]", "lea rbx, [rva 0x291c7cc]")
    c(0x14eb0b, "lea rbx, [rva 0x7f0a000]", "lea rbx, [rva 0x29207f0]")
    c(0x2277af, "lea rax, [rva 0x7efa000]", "lea rax, [rva 0x291c7cc]")
    c(0x227870, "lea rax, [rva 0x7efa000]", "lea rax, [rva 0x291c7cc]")
    c(0x227c5e, "lea rcx, [rva 0x7efa000]", "lea rcx, [rva 0x291c7cc]")
    c(0x227fff, "lea rax, [rva 0x7f0a000]", "lea rax, [rva 0x29207f0]")
    c(0x27ee81, "lea rax, [rva 0x7f0a000]", "lea rax, [rva 0x29207f0]")
    c(0x27fda0, "lea rax, [rva 0x7f0a000]", "lea rax, [rva 0x29207f0]")
    c(0x27fe46, "lea rax, [rva 0x7f0a000]", "lea rax, [rva 0x29207f0]")
    c(0x28bd61, "lea rax, [rva 0x7efa000]", "lea rax, [rva 0x291c7cc]")
    c(0x298986, "lea rax, [rva 0x7efa000]", "lea rax, [rva 0x291c7cc]")
    c(0x298bbe, "lea rax, [rva 0x7efa000]", "lea rax, [rva 0x291c7cc]")
    c(0x299a05, "lea rax, [rva 0x7efa000]", "lea rax, [rva 0x291c7cc]")
    c(0x29a6d6, "lea rax, [rva 0x7efa000]", "lea rax, [rva 0x291c7cc]")
    c(0x29a806, "lea rax, [rva 0x7f0a000]", "lea rax, [rva 0x29207f0]")
    c(0x29a903, "lea rax, [rva 0x7efa000]", "lea rax, [rva 0x291c7cc]")
    c(0x29a9c8, "lea rax, [rva 0x7f0a000]", "lea rax, [rva 0x29207f0]")
    c(0x29abb0, "lea rax, [rva 0x7f0a000]", "lea rax, [rva 0x29207f0]")
    c(0x29e409, "lea rcx, [rva 0x7f0a000]", "lea rcx, [rva 0x29207f0]")
    # pool array address (absolute disp)
    c(0x118f74, "movzx ecx, byte ptr [rdx + r15 + 0x7f0a058]", "movzx ecx, byte ptr [rdx + r15 + 0x2920848]")
    c(0x118f8a, "movzx ecx, byte ptr [rdx + r15 + 0x7f0a08c]", "movzx ecx, byte ptr [rdx + r15 + 0x292087c]")
    c(0x118f96, "mov byte ptr [rdx + r15 + 0x7f0a058], al", "mov byte ptr [rdx + r15 + 0x2920848], al")
    c(0x118fad, "mov byte ptr [rdx + r15 + 0x7f0a08c], al", "mov byte ptr [rdx + r15 + 0x292087c], al")
    c(0x27eca1, "mov byte ptr [r14 + r10 + 0x7efa008], dl", "mov byte ptr [r14 + r10 + 0x291c7d4], dl")
    c(0x27ecac, "mov word ptr [r14 + r10 + 0x7efa006], r9w", "mov word ptr [r14 + r10 + 0x291c7d2], r9w")
    c(0x27ecb5, "mov byte ptr [r14 + r10 + 0x7efa009], 0xff", "mov byte ptr [r14 + r10 + 0x291c7d5], 0xff")
    c(0x27ecbe, "or word ptr [r14 + r10 + 0x7efa000], 3", "or word ptr [r14 + r10 + 0x291c7cc], 3")
    c(0x27f343, "mov word ptr [r14 + r10 + 0x7efa002], r8w", "mov word ptr [r14 + r10 + 0x291c7ce], r8w")
    c(0x27f34c, "mov word ptr [r14 + r10 + 0x7efa004], ax", "mov word ptr [r14 + r10 + 0x291c7d0], ax")
    c(0x27fcae, "lea rdx, [rdx + 0x7f0a000]", "lea rdx, [rdx + 0x29207f0]")
    c(0x28bb15, "lea rcx, [r13 + 0x7efa000]", "lea rcx, [r13 + 0x291c7cc]")
    c(0x28bb59, "cmp byte ptr [rdi + r13 + 0x7f0a08c], 0xa", "cmp byte ptr [rdi + r13 + 0x292087c], 0xa")
    c(0x28bb68, "mov esi, dword ptr [rdi + r13 + 0x7f0a0a0]", "mov esi, dword ptr [rdi + r13 + 0x2920890]")
    c(0x28bc9a, "movzx eax, byte ptr [rdi + r13 + 0x7f0a08c]", "movzx eax, byte ptr [rdi + r13 + 0x292087c]")
    c(0x28bcc6, "movzx eax, byte ptr [rdi + r13 + 0x7f0a08c]", "movzx eax, byte ptr [rdi + r13 + 0x292087c]")
    c(0x298c09, "mov al, byte ptr [rdx + r11 + 0x7f0a054]", "mov al, byte ptr [rdx + r11 + 0x2920844]")
    c(0x298c1c, "mov eax, dword ptr [rdx + r11 + 0x7f0a090]", "mov eax, dword ptr [rdx + r11 + 0x2920880]")
    c(0x298c3e, "movzx eax, byte ptr [rdx + r11 + 0x7f0a05b]", "movzx eax, byte ptr [rdx + r11 + 0x292084b]")
    c(0x298ca8, "lea r11, [r11 + 0x7f0a0a0]", "lea r11, [r11 + 0x2920890]")
    c(0x29e31e, "lea rax, [r9 + 0x7f0a000]", "lea rax, [r9 + 0x29207f0]")
    # pool array disp off the header register
    c(0x2998b8, "test byte ptr [rcx + r12 + 0x55ed8d8], 1", "test byte ptr [rcx + r12 + 0x40c8], 1")
    c(0x2998c3, "cmp byte ptr [rcx + r12 + 0x55ed8d9], r10b", "cmp byte ptr [rcx + r12 + 0x40c9], r10b")
    c(0x2998d9, "mov r14d, dword ptr [rcx + r12 + 0x55ed8f0]", "mov r14d, dword ptr [rcx + r12 + 0x40e0]")
    c(0x14eab5, "mov r14d, 0x1000", "mov r14d, 0x400")  # pool capacity 0x400 -> 0x1000
    c(0x14ec6f, "jmp 0x5ce7af0; nop; nop", "mov dword ptr [rva 0x2966e50], r14d")  # sibling pool max stays 0x400 (cave)
    # lea+shl window: jump to wide disp cave
    c(0x298927, "jmp 0x5ce7b20; nop*3", "lea rcx, [rbp + 0x1c]; shl rax, 4")
    c(0x299808, "jmp 0x5ce7b50; nop*3", "lea r8, [rdx + 0x1c]; shl rax, 4")
    c(0x29a664, "jmp 0x5ce7b80; nop*3", "lea rcx, [r13 + 0x1c]; shl rax, 4")
    c(0x29a798, "jmp 0x5ce7bb0; nop*3", "lea rsi, [r10 + 0x1c]; shl rax, 4")

    # caves in .gsc
    # sibling pool max
    b.cave(0xaf0, """
        mov dword ptr [rva 0x2966e50], 0x400
        jmp 0x14ec76
    """)
    # wide disp lea
    b.cave(0xb20, """
        lea rcx, [rbp + 0x55dd850]
        shl rax, 4
        jmp 0x29892f
    """)
    # wide disp lea
    b.cave(0xb50, """
        lea r8, [rdx + 0x55dd850]
        shl rax, 4
        jmp 0x299810
    """)
    # wide disp lea
    b.cave(0xb80, """
        lea rcx, [r13 + 0x55dd850]
        shl rax, 4
        jmp 0x29a66c
    """)
    # wide disp lea
    b.cave(0xbb0, """
        lea rsi, [r10 + 0x55dd850]
        shl rax, 4
        jmp 0x29a7a0
    """)
