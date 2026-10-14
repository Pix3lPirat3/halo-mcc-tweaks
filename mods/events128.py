"""Player index up to 127 in the optional player fields of events. The shared optional player writer (0x78224) writes 4 bits. Here it writes 7 bits for the five event types whose encoder and decoder both read the wider field (incident, melee clang, orbit camera, damage section response, presence type 8), and those decoder reads are widened to match. The six other callers (Forge command, game variant codec, biped creation and three more) keep 4 bits through a copy of the original writer. An earlier version also widened decoders that had no matching encoder, and it crashed the game in a real lobby when a game variant was cloned (the variant codec shares the writer). This version is fixed for that case but the fix is only tested with an emulator, not in a lobby. It changes the wire format and saved game variants of the earlier version are not stock readable: a stock peer will desync, everyone needs the same DLL. event_index lets 7 bit values through when this mod is in the build. Test state: offline runs with scripted players exist for the earlier version only; not tested in a real lobby yet."""

import struct

DECODERS = (0x3b7cf9, 0x3b7d14, 0x464ec5, 0x458769, 0x466eb5, 0x466ed5, 0x3a459b)
FOUR_BIT_CALLERS = (0x77d58, 0xf6b7a, 0x1f66d8, 0x3b257a, 0x4180bf, 0x469639)
# copy of the original writer with the clamp to 16 (index 16 and up becomes none)
TWIN = """
    mov qword ptr [rsp + 8], rbx
    push rdi
    sub rsp, 0x20
    mov eax, dword ptr [rcx + 0x30]
    xor edx, edx
    cmp r8d, 16
    jb t_ok
    mov r8d, -1
    t_ok:
    cmp r8d, -1
    mov edi, r8d
    mov ebx, 0x40
    mov r11, rcx
    sete dl
    cmp eax, ebx
    jae t_slow1
    inc dword ptr [rcx + 0x24]
    inc eax
    mov dword ptr [rcx + 0x30], eax
    mov rax, qword ptr [rcx + 0x28]
    add rax, rax
    or rax, rdx
    mov qword ptr [rcx + 0x28], rax
    jmp t_cont
    t_slow1:
    mov r8d, 1
    call 0xdcfc4
    t_cont:
    cmp edi, -1
    je t_fin
    mov eax, dword ptr [r11 + 0x30]
    mov r8d, 4
    sub ebx, eax
    mov rdx, rdi
    cmp ebx, r8d
    jl t_slow2
    add dword ptr [r11 + 0x24], r8d
    add eax, r8d
    mov dword ptr [r11 + 0x30], eax
    mov rax, qword ptr [r11 + 0x28]
    shl rax, 4
    or rax, rdx
    mov qword ptr [r11 + 0x28], rax
    jmp t_fin
    t_slow2:
    mov rcx, r11
    call 0xdcfc4
    t_fin:
    mov rbx, qword ptr [rsp + 0x30]
    add rsp, 0x20
    pop rdi
    ret
"""


def apply(b):
    for a in DECODERS:
        fo = b.rva2fo(a)
        assert bytes(b.img[fo - 1:fo + 4]).hex() == 'ba04000000', hex(a)
        b.data(a, '07', '04')
    fo = b.rva2fo(0x78277)
    assert bytes(b.img[fo - 2:fo + 4]).hex() == '41b804000000'
    b.data(0x78277, '07', '04')
    fo = b.rva2fo(0x78297)
    assert bytes(b.img[fo - 3:fo + 1]).hex() == '48c1e004'
    b.data(0x78297, '07', '04')
    twin = b.pcode(TWIN)
    for a in FOUR_BIT_CALLERS:
        fo = b.rva2fo(a)
        assert b.img[fo] == 0xe8 and a + 5 + struct.unpack_from('<i', b.img, fo + 1)[0] == 0x78224, hex(a)
        b.data(a + 1, struct.pack('<i', twin - (a + 5)).hex(), bytes(b.img[fo + 1:fo + 5]).hex())
