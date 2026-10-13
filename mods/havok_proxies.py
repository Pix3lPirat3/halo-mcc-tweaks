"""Havok character proxies: one 80 byte proxy per biped, pool of 16. With 17 or more bipeds every further biped has no physics proxy. The pool is now 64 entries, and the per tick creation driver, which has its own cap of 16 taken from the scenario budget, is raised to the same 64. The pool memory comes from the game state, so a map with a tight game state budget needs room for the extra 3840 bytes."""


def apply(b):
    c = b.code
    c(0x164af2, "lea edx, [r9 + 0x40]", "lea edx, [r9 + 0x10]")  # pool create count
    c(0x164e7e, "lea ebx, [r15 + 0x40]", "lea ebx, [r15 + 0x10]")  # creation driver cap
    c(0x164e82, "xor eax, eax; nop", "test rax, rax")  # scenario budget record ignored
