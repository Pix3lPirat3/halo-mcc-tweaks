"""Per tick player update (0x47050): three fixed 16 entry structures. The action flag table has 16 dwords and is written for every player of the datum, the respawn candidate list is 16 entries on the stack and ends at the stack cookie, and the update struct that carries each player's action entry has 16 entries. The first two are cut at 16 so nothing is overwritten, players 16 and up take their action entry from a block in .gsy (a mask and one entry of 0xa8 bytes per player, 16 entries for 32 players, 48 with the players64 group where the mask is a qword) that an outside writer has to fill, with no entry they stay idle."""


def apply(b):
    n = b.nplayers
    blk = b.gsy_grow((0x10 + (n - 16) * 0xa8 + 0xfff) & ~0xfff)
    mask, ent = blk, blk + 0x10
    # flag table write [rbx + index*4] only for index < 16
    cave = b.pcode("""
        movzx eax, word ptr [rsp + 0x48]
        cmp eax, 0x10
        jae skip
        mov dword ptr [rbx + rax*4], edx
        skip:
        jmp 0x47120
    """)
    b.hook(0x47118, 8, cave)
    # respawn candidate list: esi count, r15 write pointer, stop adding at 16
    cave = b.pcode("""
        cmp esi, 0x10
        jae done
        mov dword ptr [r15], ebx
        inc esi
        add r15, 4
        done:
        jmp 0x47287
    """)
    b.hook(0x4727e, 9, cave)
    # action entry of a player: index >= 16 reads the block in .gsy when its mask bit is set
    cave = b.pcode("""
        movzx ecx, word ptr [rsp + 0x48]
        cmp ecx, 0x10
        jae hi16
        mov eax, 1
        shl eax, cl
        test dword ptr [rdi + 8], eax
        je 0x479e7
        imul rbx, rcx, 0xa8
        add rbx, 0x10
        add rbx, rdi
        jmp 0x47639
        hi16:
        cmp ecx, %#x
        jae 0x479e7
        mov edx, ecx
        sub edx, 0x10
        lea rax, [rva %#x]
        %s
        %s
        jae 0x479e7
        imul rbx, rdx, 0xa8
        lea rax, [rva %#x]
        add rbx, rax
        jmp 0x47639
    """ % (n, mask, 'mov eax, dword ptr [rax]' if n <= 32 else 'mov rax, qword ptr [rax]', 'bt eax, edx' if n <= 32 else 'bt rax, rdx', ent))
    b.hook(0x47616, 35, cave)
