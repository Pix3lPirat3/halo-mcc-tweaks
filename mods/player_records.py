"""Per player records that exist once per slot for 16 players: the control record array in the world (16 x 0xe0, followed by another array) and the player added registration (announcer, gametype, score and statistics records are 16 wide). Creating or registering a player of index 16 or above would write into the next array. These entry points now return at once for such an index, so those players have no control record and no score or statistics entry."""


def apply(b):
    # control record creation: index in dx
    cave = b.pcode("""
        movzx eax, dx
        cmp eax, 0x10
        jae done
        mov qword ptr [rsp + 0x10], rbx
        jmp 0x3c0add
        done:
        ret
    """)
    b.hook(0x3c0ad8, 5, cave)
    # player added registration: handle in cx
    cave = b.pcode("""
        movzx eax, cx
        cmp eax, 0x10
        jae done
        mov qword ptr [rsp + 8], rbx
        jmp 0x10480d
        done:
        ret
    """)
    b.hook(0x104808, 5, cave)
    # player rejoin registration: returns false for such an index
    cave = b.pcode("""
        movzx r11d, cx
        cmp r11d, 0x10
        jae done
        mov rax, rsp
        mov qword ptr [rax + 8], rbx
        jmp 0x104ae3
        done:
        xor eax, eax
        ret
    """)
    b.hook(0x104adc, 7, cave)
