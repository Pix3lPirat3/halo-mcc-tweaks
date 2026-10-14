"""Havok character proxies: one 80 byte proxy per biped, pool of 16. With 17 or more bipeds every further biped has no physics proxy. The pool is now 64 entries, and the per tick creation driver, which has its own cap of 16 taken from the scenario budget, is raised to the same 64. The pool memory comes from the game state, so a map with a tight game state budget needs room for the extra 3840 bytes. With players128 the pool and the cap are 152 (the players plus 24 for bodies); pools above 127 need the state_regions mod, without it the game thread stalls."""


def apply(b):
    n = b.nplayers
    if n >= 128:  # the counts do not fit the one byte immediate, so the pool and the cap come from small blocks of code; 24 more than players for bodies
        count = n + 24
        cave = b.pcode("""
            mov edx, %#x
            lea r8d, [r9 + 0x50]
            jmp 0x164afa
        """ % count)
        b.hook(0x164af2, 8, cave)
        cave = b.pcode("""
            mov ebx, %#x
            xor eax, eax
            jmp 0x164e85
        """ % count)
        b.hook(0x164e7e, 7, cave)
        return
    c = b.code
    c(0x164af2, "lea edx, [r9 + 0x40]", "lea edx, [r9 + 0x10]")  # pool create count
    c(0x164e7e, "lea ebx, [r15 + 0x40]", "lea ebx, [r15 + 0x10]")  # creation driver cap
    c(0x164e82, "xor eax, eax; nop", "test rax, rax")  # scenario budget record ignored
