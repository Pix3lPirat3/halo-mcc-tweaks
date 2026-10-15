"""Forge per player update (0x735fc, run every tick for each player that has a unit): its sandbox record array has 16 records of 0x12c bytes and the function writes -1 into two fields of the record of its player. For index 16 and up that overwrote the score block and other fields behind the array, from 17 players on. The function now returns at once for such a player, so players 16 and up have no Forge sandbox record. The player argument is a handle (salt in the high word, index in the low word): the guard compares only the index, the low word. Test state: V live on the public players128 build in a proper Forge session: monitor without weapon, HUD, grab and spawn, death screen HUD all work; with a whole handle compare no player was updated and the monitor could not grab."""


def apply(b):
    cave = b.pcode("""
        movzx eax, dx
        cmp eax, 0x10
        jb ok
        xor eax, eax
        ret
        ok:
        mov rax, rsp
        mov qword ptr [rax + 8], rbx
        jmp 0x73603
    """)
    b.hook(0x735fc, 7, cave)
