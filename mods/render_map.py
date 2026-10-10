"""Render object map (u16 per object) relocated to a new 0x2000 byte zero block in .gsy."""


def apply(b):
    blk = b.gsy_grow(0x2000)
    b.code(0x2272b2, f"lea rcx, [rva {blk:#x}]", "lea rcx, [rva 0x2967e58]")  # map base
    b.code(0x2272b9, "mov r8d, 0x2000", "mov r8d, 0x1000")  # clear size for 4096 entries
