"""Players datum 16 -> 32: the datum itself, the simulated input region that has one entry per player, and the index bound of the player update. Nothing else in this set works without it. A player index above 15 is still unsafe in many other tables, the other player mods in this set address those one by one."""


def apply(b):
    d = b.data
    d(0x43473, "20", "10")  # players datum allocator: lea edx, [r9 + 0x10] (max count)
    # simulated input region, 16 x 0x240 -> 32 x 0x240 (allocation size, clear size and init count must change together)
    d(0xd9d8c, "00480000", "00240000")
    d(0xd9e1c, "00480000", "00240000")
    d(0xd9e3d, "20000000", "10000000")
    d(0x48ae3, "1f", "0f")  # cmp r14w, 0xf -> 0x1f (player index bound in 0x48a68)
