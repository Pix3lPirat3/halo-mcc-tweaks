"""Per-frame object matrix buffer 0x35c00 -> 4 MB, moved from static 0xc51c40 to a new zero block in .gsy."""


def apply(b):
    blk = b.gsy_grow(0x400000)
    c = b.code
    c(0xc804, "mov r8d, 0x400000", "mov r8d, 0x35c00")  # init clear size
    c(0xc80a, f"lea rcx, [rva {blk:#x}]", "lea rcx, [rva 0xc51c40]")  # buffer base
    c(0x250972, "mov ecx, 0x400000", "mov ecx, 0x35c00")  # capacity
    c(0x250997, "shl r10d, 0x16", "shl r10d, 0x12")  # index shift
    # buffer base at the use sites
    c(0x24b037, f"lea rdx, [rva {blk:#x}]", "lea rdx, [rva 0xc51c40]")
    c(0x24b13c, f"lea rcx, [rva {blk:#x}]", "lea rcx, [rva 0xc51c40]")
    c(0x27f1ab, f"lea rcx, [rva {blk:#x}]", "lea rcx, [rva 0xc51c40]")
    c(0x298c24, f"lea r14, [rva {blk:#x}]", "lea r14, [rva 0xc51c40]")
    c(0x2995bf, f"lea rax, [rva {blk:#x}]", "lea rax, [rva 0xc51c40]")
    c(0x29a122, f"lea rax, [rva {blk:#x}]", "lea rax, [rva 0xc51c40]")
    c(0x29a14b, f"lea rax, [rva {blk:#x}]", "lea rax, [rva 0xc51c40]")
    c(0x29a3ac, f"lea rcx, [rva {blk:#x}]", "lea rcx, [rva 0xc51c40]")
    c(0x2a245a, f"lea rax, [rva {blk:#x}]", "lea rax, [rva 0xc51c40]")
    # index masks 0x3ffff -> 0x3fffff
    c(0x24b03e, "and eax, 0x3fffff", "and eax, 0x3ffff")
    c(0x24b143, "and ebx, 0x3fffff", "and ebx, 0x3ffff")
    c(0x27f1b2, "and eax, 0x3fffff", "and eax, 0x3ffff")
    c(0x298c35, "and ecx, 0x3fffff", "and ecx, 0x3ffff")
    c(0x298cd3, "and r9d, 0x3fffff", "and r9d, 0x3ffff")
    c(0x2995c6, "and edx, 0x3fffff", "and edx, 0x3ffff")
    c(0x29a129, "and edx, 0x3fffff", "and edx, 0x3ffff")
    c(0x29a152, "and edx, 0x3fffff", "and edx, 0x3ffff")
    c(0x29a3b3, "and r9d, 0x3fffff", "and r9d, 0x3ffff")
    c(0x2a2461, "and r9d, 0x3fffff", "and r9d, 0x3ffff")
