"""Respawn tables: spawner and monitor arrays sized for 1408 entries."""


def apply(b):
    c = b.code
    # globals block size: alloc and memset
    c(0x785eb, "mov r9d, 0x11e30", "mov r9d, 0x8430")
    c(0x786f3, "mov r8d, 0x11e30", "mov r8d, 0x8430")
    c(0x788a9, "mov r8d, 0x11e30", "mov r8d, 0x8430")
    # new/delete size of the sibling heap class
    c(0x37a3aa, "mov edx, 0x11e30", "mov edx, 0x8430")
    c(0x37a3ef, "mov ecx, 0x11e30", "mov ecx, 0x8430")
    c(0x37a4a5, "mov ecx, 0x11e30", "mov ecx, 0x8430")
    # manager base inside the globals block
    c(0x78ba9, "lea rcx, [rdi + 0x8430]", "lea rcx, [rdi + 0x35d4]")
    c(0x7b0ce, "lea rcx, [rdi + 0x8430]", "lea rcx, [rdi + 0x35d4]")
    c(0x7c92f, "add rcx, 0x8430", "add rcx, 0x35d4")
    c(0x7d7fd, "lea rcx, [r9 + 0x8430]", "lea rcx, [r9 + 0x35d4]")
    c(0x17b9ba, "add rcx, 0x8430", "add rcx, 0x35d4")
    c(0x17ba3c, "add r9, 0x8430", "add r9, 0x35d4")
    c(0x17bba2, "add rcx, 0x8430", "add rcx, 0x35d4")
    c(0x17bcac, "lea rcx, [rdi + 0x8430]", "lea rcx, [rdi + 0x35d4]")
    c(0x17bccd, "lea rcx, [rdi + 0x8430]", "lea rcx, [rdi + 0x35d4]")
    c(0x3c3c9a, "add rcx, 0x8430", "add rcx, 0x35d4")
    # monitor array B offset (behind spawner array A)
    c(0x17bf9a, "lea rax, [rcx + 0x5804]", "lea rax, [rcx + 0x2cb4]")
    c(0x17c00f, "lea rbx, [rdi + 0x5800]", "lea rbx, [rdi + 0x2cb0]")
    c(0x17c176, "lea rbx, [rsi + 0x5804]", "lea rbx, [rsi + 0x2cb4]")
    c(0x17c423, "lea rax, [rbp + 0x5800]", "lea rax, [rbp + 0x2cb0]")
    c(0x17c449, "lea rdi, [rbp + 0x5800]", "lea rdi, [rbp + 0x2cb0]")
    c(0x17c83a, "lea r9, [rcx + 0x5800]", "lea r9, [rcx + 0x2cb0]")
    c(0x17c864, "lea rax, [rax + 0x1600]", "lea rax, [rax + 0xb2c]")
    # spawner/monitor count 715 -> 1408
    c(0x7b112, "mov ecx, 0x580", "mov ecx, 0x2cb")
    c(0x17ba5e, "cmp r8, 0x580", "cmp r8, 0x2cb")
    c(0x17bf6c, "mov r8d, 0x580", "mov r8d, 0x2cb")
    c(0x17c00a, "mov esi, 0x580", "mov esi, 0x2cb")
    c(0x17c16e, "cmp ebx, 0x580", "cmp ebx, 0x2cb")
    c(0x17c27d, "cmp ebp, 0x580", "cmp ebp, 0x2cb")
    c(0x17c350, "cmp r9, 0x580", "cmp r9, 0x2cb")
    c(0x17c390, "cmp rax, 0x580", "cmp rax, 0x2cb")
    c(0x17c43b, "cmp rdx, 0x580", "cmp rdx, 0x2cb")
    c(0x17c796, "mov r15d, 0x580", "mov r15d, 0x2cb")
    c(0x17c7ef, "cmp rdx, 0x580", "cmp rdx, 0x2cb")
    c(0x17c853, "cmp r10, 0x580", "cmp r10, 0x2cb")
