"""Score list (0x191e74, one caller): it writes one score per present player into a buffer on the stack that holds 18 entries and ends right in front of the stack check, with no bound. In a Slayer game with 19 or more present players it overwrote the check and the game closed a few seconds later. The list now stops at 16 entries, so only the first 16 players are listed. Test state: tested offline with scripted players in Slayer at 40 and 128; not tested in a real lobby yet."""


def apply(b):
    cave = b.pcode("""
        cmp dword ptr [rbx], 0x10
        jge skip
        movzx eax, word ptr [rsp + 0x30]
        jmp 0x191f3a
        skip:
        jmp 0x191f4e
    """)
    b.hook(0x191f35, 5, cave)
