"""Havok heap relocation and datum bump block size."""


def apply(b):
    c = b.code
    c(0x1e6fac, "lea r8, [rva 0x4eda000]", "lea r8, [rva 0x4782f10]")  # heap block 1 base moves into .gsx
    # manager ctor: first block size
    c(0x1e6ac9, "mov r8d, 0xe00000", "mov r8d, 0x380000")
    c(0x1e6b16, "mov edx, 0xbe6664", "mov edx, 0x2f9999")
    c(0x1e6fda, "mov qword ptr [rax + 0x28], 0xe00000", "mov qword ptr [rax + 0x28], 0x380000")
    # bump block size +0x100000 (room for 4500 more components)
    c(0xc4cb, "mov r8d, 0x600000", "mov r8d, 0x4b0000")
    c(0x175b9, "cmp eax, 0x600000", "cmp eax, 0x4b0000")
    c(0x99229, "mov edx, 0x1770", "mov edx, 0x5dc")
    c(0x9ae03, "cmp eax, 0x170c", "cmp eax, 0x6a4")
    c(0x9c3ba, "cmp dword ptr [rva 0xb93604], 0x1708", "cmp dword ptr [rva 0xb93604], 0x6a0")
    c(0x9c3ce, "cmp dword ptr [rva 0xb93604], 0x1708", "cmp dword ptr [rva 0xb93604], 0x6a0")
