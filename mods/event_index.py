"""Player index in the network event stream: the presence event encoder writes the event kind (2 bits) and the player index (4 bits) without a mask, so index 16 turns a presence update into a boot event (in tests it named the first player, and it may remove the local machine from its own session, which is a hypothesis). The optional player index writer has the same unmasked write and loses bit alignment. The encoder now refuses to encode an index of 16 or above, and the optional writer maps such an index to none."""


def apply(b):
    # presence event encoder 0x3a4370: not encoded (al = 0) for index >= 16, callers then post nothing
    cave = b.pcode("""
        cmp dword ptr [rcx + 4], 0x10
        jb ok
        xor eax, eax
        ret
        ok:
        mov qword ptr [rsp + 8], rbx
        jmp 0x3a4375
    """)
    b.hook(0x3a4370, 5, cave)
    # optional player index writer 0x78224: values >= 16 become -1 (no player)
    cave = b.pcode("""
        cmp r8d, 0x10
        jb ok
        mov r8d, -1
        ok:
        cmp r8d, -1
        mov edi, r8d
        jmp 0x7823a
    """)
    b.hook(0x78233, 7, cave)
