"""Glue handle index on the wire: 11 bits stock, 12 bits here, so the glue datum can hold the 4095 entries that many players and their objects need. The writer ORed the unmasked 16 bit index into the field, so an index of 4096 or more (or the none handle) corrupted the salt bits before it; it is clamped now, and the pool keeps 4095 entries so the clamp value is never a live slot. Two host side fixes go with it (the entity id width flag stays set, and only -1 skips a glue pair). Everyone in a game needs the same DLL."""


def apply(b):
    c = b.code
    c(0x3d2d45, "mov r8d, 0xc", "mov r8d, 0xb")  # writer: index width
    c(0x3d2d57, "lea eax, [rcx + 0xc]", "lea eax, [rcx + 0xb]")  # writer: bit position
    c(0x3d2d62, "shl rax, 0xc", "shl rax, 0xb")  # writer: shift
    c(0x3d2da3, "mov edx, 0xc", "mov edx, 0xb")  # reader: index width
    # glue datum array: replaces the size of the objects mod, 0xfff entries (index 0xfff is never allocated)
    site = b.rva2fo(0x3a94a5)
    b.ops = [o for o in b.ops if o['fo'] != site]
    c(0x3a94a5, "mov edx, 0xfff", "mov edx, 0x800")
    # writer: clamp the index to 0xfff before it is written
    cave = b.pcode("""
        movzx edi, dx
        cmp edi, 0xfff
        jbe ok
        mov edi, 0xfff
        ok:
        sar edx, 0x10
        jmp 0x3d2d05
    """)
    b.hook(0x3d2cff, 6, cave)
    c(0x43cb32, "nop7", "mov byte ptr [rva 0xb71108], 0")  # partition overflow no longer clears the entity id width flag
    # host glue allocation result: only -1 skips the pair
    cave = b.pcode("""
        cmp eax, -1
        je 0x3a641d
        mov edx, eax
        mov r15d, eax
        jmp 0x3a63ce
    """)
    b.hook(0x3a63c9, 5, cave)
