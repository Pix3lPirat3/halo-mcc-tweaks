"""Team audience of incidents (0x1f8b18). For an incident that names no player, the audience is every player of the incident's team, and the loop at 0x1f8b83 appends their indexes to a stack list of 18 entries that ends at the stack check, with no bound. With 19 or more players on one team the 19th index overwrote the check and the game closed. The append now stops at 18 entries, so a team of more than 18 players gets the message for its first 18 players in table order. This is a bound, not a bigger list. Test state: builds with it ran offline with scripted players in Slayer at 33 and 64 without a crash, but a team of 19 was not isolated; not tested in a real lobby yet."""


def apply(b):
    fo = b.rva2fo(0x1f8b9a)
    assert bytes(b.img[fo:fo + 6]).hex() == '8d43014863cb'
    cave = b.pcode("""
        cmp ebx, 18
        jge skip
        lea eax, [rbx + 1]
        movsxd rcx, ebx
        jmp 0x1f8ba0
        skip:
        jmp 0x1f8bad
    """)
    b.hook(0x1f8b9a, 6, cave)
