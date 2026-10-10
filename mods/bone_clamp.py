"""Bone palette upload: clamp the matrix count to the 70 matrix buffer."""


def apply(b):
    c = b.code
    c(0x2851e2, "jmp 0x5ce7c00; nop", "lea ebx, [rdx + rdx*2]; mov rdi, rcx")  # bone palette upload: clamp matrix count to 70 (cave)

    # caves in .gsc
    # clamp matrix count to 70
    b.cave(0xc00, """
            cmp edx, 0x46
            jbe L1
            mov edx, 0x46
        L1: lea ebx, [rdx + rdx*2]
            mov rdi, rcx
            jmp 0x2851e8
    """)
