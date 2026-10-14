"""Screen effect pool: one entry per player, 64 at most. With players128 the pool holds 136 entries (the players plus 8). The pool memory comes from the game state, so pools above 135 need the state_regions mod, without it the render thread crashes. For 32 and 64 players nothing changes."""


def apply(b):
    n = b.nplayers
    if n <= 64:
        return
    cave = b.pcode("""
        mov edx, %#x
        lea r8d, [r9 + 0x2c]
        jmp 0x15feba
    """ % (n + 8))
    b.hook(0x15feb2, 8, cave)
