"""Respawn rule of a player: the gametype respawn rule byte is read from a record array with 16 records (0xf0 bytes each) by the player index. For index 16 and up the read lands on other memory, so some players never get the answer that lets them respawn and stay dead for minutes. Players with an index of 16 or more now get the answer for no wait rule, so they respawn like everyone else."""


def apply(b):
    cave = b.pcode("""
        xor al, al
        cmp edx, -1
        je 0x1498a9
        cmp dx, 0x10
        jb 0x14987b
        xor al, al
        ret
    """)
    b.hook(0x149874, 5, cave)
