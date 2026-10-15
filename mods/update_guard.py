"""Per tick player update: three functions treat the player index as if there were 16 players. The consumer 0x3ab220 walks the players datum and tests a 32 bit mask (bt with a register operand wraps at 32) before it reads an entry of the update message at rdi + 0xcf4c + index * 0x74. The message has 16 entries, so with a client in the session player 16 and up read past the end of the object, and at player 64 past the top of the thread stack (host crash). The two writers 0x4212c0 and 0x3bfe94 fill the 16 slot per player cache of a peer block with the raw player index. All three now skip every player index of 16 or more, so those players have no entry in the update message. Test state: a host with this mod ran with a real client up to 128 players twice without a crash (ten minutes each); players 16 and up are not shown in the update message to the client."""


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
