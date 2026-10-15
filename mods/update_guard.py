"""Per tick player update: the update message has 16 player entries, but the functions that build and read it use the player index as it is. Players 16 and up only exist with the player mods. The consumer 0x3ab220 and the two writers 0x4212c0 and 0x3bfe94 now skip every player index of 16 or more, so those players have no entry in the update message. Test state: V live: a host with this mod ran with a real client up to 128 players in three runs of over ten minutes without a crash; not tested: combat at 128 players, late join of a client, mixed builds."""


def apply(b):
    cave = b.pcode("""
        cmp ecx, 16
        jae 0x3ab338
        mov eax, dword ptr [rdi + 0xcf48]
        jmp 0x3ab31d
    """)
    b.hook(0x3ab317, 6, cave)
    cave = b.pcode("""
        cmp edx, 16
        jae done
        movsxd r9, edx
        mov al, r8b
        jmp 0x4212c6
        done:
        ret
    """)
    b.hook(0x4212c0, 6, cave)
    cave = b.pcode("""
        movsxd r11, dword ptr [rsi]
        cmp r11d, 16
        jae 0x3bff30
        lea r8, [rbp - 0x29]
        jmp 0x3bfe9b
    """)
    b.hook(0x3bfe94, 7, cave)
