"""Script native player lists: the natives that return the players of a game (or of a team) collect unit handles into a 16 entry list on the stack that ends at the stack cookie. With a 32 slot datum the 17th qualifying player overwrites the cookie and the game aborts. The two collectors now stop adding at 16 entries, so scripts see the first 16 players only."""


def apply(b):
    # players native: unit list at [rsp + 0x20], bx is the count
    cave = b.pcode("""
        cmp bx, 0x10
        jae done
        movsx rax, bx
        inc bx
        mov dword ptr [rsp + rax*4 + 0x20], edx
        done:
        jmp 0x1996c9
    """)
    b.hook(0x1996be, 11, cave)
    # players of a team (two callers): unit list at [rsp + 0x30], di is the count
    cave = b.pcode("""
        cmp di, 0x10
        jae done
        movsx rax, di
        inc di
        mov dword ptr [rsp + rax*4 + 0x30], ecx
        done:
        jmp 0x1eb55b
    """)
    b.hook(0x1eb550, 11, cave)
