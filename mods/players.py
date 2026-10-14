"""Players datum 16 -> 32 (64 with the players64 group, 128 with players128): the datum itself, the simulated input region that has one entry per player, and the index bound of the player update. Nothing else in this set works without it. A player index above 15 is still unsafe in many other tables, the other player mods in this set address those one by one."""


def apply(b):
    d = b.data
    n = b.nplayers
    if n < 128:
        d(0x43473, "%02x" % n, "10")  # players datum allocator: lea edx, [r9 + 0x10] (max count)
    else:  # 128 does not fit the one byte immediate: the count moves into a small block of code
        cave = b.pcode("""
            mov edx, %#x
            call 0x12fcc
            jmp 0x43479
        """ % n)
        b.hook(0x43470, 9, cave)
    # simulated input region, 16 x 0x240 -> n x 0x240 (allocation size, clear size and init count must change together)
    size = (n * 0x240).to_bytes(4, 'little').hex()
    d(0xd9d8c, size, "00240000")
    d(0xd9e1c, size, "00240000")
    d(0xd9e3d, "%02x000000" % n, "10000000")
    d(0x48ae3, "%02x" % (n - 1), "0f")  # cmp r14w, 0xf -> n - 1 (player index bound in 0x48a68)
