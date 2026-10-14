"""Game state regions: the game state is carved into regions (4 is the main simulation state, 1 holds Forge and object globals) and the allocator that hands out memory inside a region never checks the region end. With many players the player tables and pools of the sets in this branch fill region 4 to its end, and what sits behind it is overwritten: the impact pool count wraps and the game thread stops, and pools above 127 (Havok proxies) or 135 (screen effects) crash or stall. This mod grows region 4 by 0x40000 and region 1 by 0x10000 bytes. The saved state size, the backing block, the film checkpoint offsets and the static blocks behind the state all move by the matching amount (123 sites), and the image gets the extra room. Runs after all other mods."""
# saved state size S and values derived from it (region size, pool stride, loops)
STATE = (
    0xc3fe, 0xc42a, 0xc49c, 0x160bb, 0x161a9, 0x16b1e, 0x16e7d, 0x17168, 0x171c7, 0x171cf, 0x171eb,
    0x3559f, 0x88249, 0x88766, 0x88a5a, 0xa53e7, 0x1713db, 0x171698, 0x1716c9, 0x17190f, 0x171939,
    0x171b95, 0x171bed, 0x171bf6, 0x171c48, 0x1721b4,
)
# backing block size (S + 2 x region 4)
BACKING = (
    0xc473, 0x15fb7, 0x1612f,
)
# static blocks behind region 4 (mark queue, pools): rip relative and absolute references
BEHIND = (
    0x44ad, 0x44be, 0x44c5, 0xa3f30, 0xa3f38, 0xa3f3e, 0xa3f52, 0xa3f5b, 0xcfde3, 0xcfdec, 0xcfe0e,
    0xcfe5d, 0xcfe67, 0xcfeb3, 0xcfebc, 0xcfede, 0xcff2d, 0xcff37, 0xcff84, 0xcffe4, 0xcffed, 0xcfffe,
    0xd0007, 0xd0019, 0xd02ff, 0xd030c, 0xd031b, 0xd0322, 0xd04ad, 0xd0a2f, 0xd0a3a, 0xd0ca9, 0xd0cbd,
    0xd0e27, 0xd0e32, 0x118f79, 0x118f8f, 0x118f9a, 0x118fb1, 0x14ead6, 0x14eb0e, 0x2277b2, 0x227873,
    0x227c61, 0x228002, 0x27eca5, 0x27ecb1, 0x27ecb9, 0x27ecc3, 0x27ee84, 0x27f348, 0x27f351, 0x27fcb1,
    0x27fda3, 0x27fe49, 0x28bb18, 0x28bb5d, 0x28bb6c, 0x28bc9f, 0x28bccb, 0x28bd64, 0x298989, 0x298bc1,
    0x298c0d, 0x298c20, 0x298c43, 0x298cab, 0x2998bc, 0x2998c7, 0x2998dd, 0x299a08, 0x29a6d9, 0x29a809,
    0x29a906, 0x29a9cb, 0x29abb3, 0x29e321, 0x29e40c,
)
# S / 4
STATE_QUARTER = (
    0x171676, 0x1718ed, 0x171bca,
)
# S / 2
STATE_HALF = (
    0x171687, 0x1718fe, 0x171bdb,
)
# same blocks referenced from caves in .gsc (info block and table bases)
GSC_BEHIND = (0x9f8, 0x9fc, 0xa71, 0xaa1, 0xad1, 0xb23, 0xb53, 0xb83, 0xbb3)

R4_IMM = 0x161a9  # region 4 size immediate (the region 1 growth does not touch it)
R1_IMM = 0x16155  # region 1 size immediate (mov edx, 0x2c0000 at 0x16154)


def apply(b):
    g = b.r4g
    g1 = b.r1g
    d = g1  # region 1 growth moves everything derived from the saved state like region 3 growth does
    assert g % 0x10000 == 0 and d % 0x10000 == 0
    b.bump(R1_IMM, g1)
    for rva in STATE:
        b.bump(rva, g + (0 if rva == R4_IMM else d))
    for rva in BACKING:
        b.bump(rva, 3 * g + d)
    for rva in STATE_QUARTER:
        b.bump(rva, g // 4 + d // 4)
    for rva in STATE_HALF:
        b.bump(rva, g // 2 + d // 2)
    for rva in BEHIND:
        b.bump(rva, 2 * (g + d))
    for off in GSC_BEHIND:
        b.gsc_bump(off, 2 * (g + d))
