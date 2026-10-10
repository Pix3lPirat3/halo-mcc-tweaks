"""Placement records 651 -> 1344: index routing windows, bit vector frame and the per-record extras."""
import struct

from core import GSX_VA


def apply(b):
    c, p, d, r = b.code, b.pad, b.data, b.raw
    # info block: record counts, extras base, record size and count
    b.blob(0x000, struct.pack('<4sHHIIIIII', b'GSXE', 1, 1, 651, 1344, GSX_VA + 0xe00000, 0x4c, 693, 0))
    # empty record template: link words 0xffff, flag word 0x0800
    t = bytearray(0x4c)
    t[2:8] = b"\xff" * 6
    t[0x2c:0x2e] = b"\xff\xff"
    t[0x44:0x46] = b"\xff\xff"
    t[0x46:0x48] = b"\x00\x08"
    t[0x4a] = 0xff
    b.blob(0x940, t)
    # live index cap 651 -> 1344
    c(0x6de7f, "mov r9d, 0x540", "mov r9d, 0x28b")
    c(0x6e112, "cmp r8, 0x540", "cmp r8, 0x28b")
    c(0x6e1cb, "cmp r10d, 0x53f", "cmp r10d, 0x28a")
    c(0x6e5ca, "cmp edx, 0x53f", "cmp edx, 0x28a")
    c(0x6e641, "cmp ebx, 0x540", "cmp ebx, 0x28b")
    c(0x6fe99, "mov r14d, 0x540", "mov r14d, 0x28b")
    c(0x7128f, "mov ecx, 0x53f", "mov ecx, 0x28a")
    c(0x74351, "mov eax, 0x53f", "mov eax, 0x28a")
    c(0x76894, "mov eax, 0x53f", "mov eax, 0x28a")
    c(0x769ea, "mov eax, 0x53f", "mov eax, 0x28a")
    c(0x2ce431, "mov eax, 0x53f", "mov eax, 0x28a")
    c(0x2cf022, "mov eax, 0x53f", "mov eax, 0x28a")
    c(0x2cf92e, "mov eax, 0x53f", "mov eax, 0x28a")
    c(0x4b2d1c, "mov eax, 0x53f", "mov eax, 0x28a")
    c(0x4ed9d5, "mov eax, 0x53f", "mov eax, 0x28a")
    # routing windows: jump to a per-site cave in .gsc
    c(0x6cbb4, "jmp 0x5ce7020; nop*5", "add rsi, 0x4c; cmp edi, 0x28b")
    c(0x6cc1b, "jmp 0x5ce7180; nop; nop", "imul r12, rdi, 0x4c; add rsi, r12")
    c(0x6ccdb, "jmp 0x5ce7040; nop*5", "add r15, 0x4c; cmp ebx, 0x28b")
    c(0x6dc13, "jmp 0x5ce71c0; nop", "imul r14, rcx, 0x4c; mov edx, eax")
    c(0x6de96, "jmp 0x5ce7160; nop", "lea rsi, [rsi + 0x4c]; cmp edx, ebx")
    c(0x6df12, "jmp 0x5ce7200; nop*3", "imul rsi, r15, 0x4c; or r12d, 0xffffffff")
    c(0x6e091, "jmp 0x5ce7060; nop*5", "add rsi, 0x4c; cmp ebx, 0x28b")
    c(0x6e10b, "jmp 0x5ce7080; nop; nop", "add r8, r14; add rdx, 0x4c")
    c(0x6e12d, "jmp 0x5ce7240; nop", "imul rbx, rax, 0x4c; xor edx, edx")
    c(0x6e1d4, "jmp 0x5ce7280; nop*6", "imul rbx, r10, 0x4c; add rbx, 0x14fc")
    c(0x6e281, "jmp 0x5ce72d0; nop; nop", "imul rdx, rax, 0x4c; mov rdi, r8")
    c(0x6e47f, "jmp 0x5ce7310; nop; nop", "imul rcx, rax, 0x4c; add rbx, rcx")
    c(0x6e587, "jmp 0x5ce7350; nop; nop", "movsxd rax, edx; imul rcx, rax, 0x4c")
    c(0x6e5d2, "jmp 0x5ce7390; nop; nop", "movsxd rax, edx; imul rcx, rax, 0x4c")
    c(0x6e649, "jmp 0x5ce73d0; nop*3", "movaps xmm0, xmmword ptr [r8]; imul r9, rbx, 0x4c")
    c(0x6e6de, "jmp 0x5ce7410; nop; nop", "imul rsi, rax, 0x4c; mov rbx, r8")
    c(0x6e884, "jmp 0x5ce7450; nop*3", "imul r8, rdi, 0x4c; movsd xmm0, qword ptr [rcx]")
    c(0x6e953, "jmp 0x5ce7490; nop*6", "imul r12, rbp, 0x4c; lea rdi, [rsi + 0x14fc]")
    c(0x6ead6, "jmp 0x5ce74e0; nop; nop", "mov rdi, r8; imul r14, rax, 0x4c")
    c(0x6ed4b, "jmp 0x5ce7520; nop; nop", "mov r14, rcx; imul rbx, rsi, 0x4c")
    c(0x6ef2c, "jmp 0x5ce70a0; nop*5", "add rbx, 0x4c; cmp edi, 0x28b")
    c(0x6efba, "jmp 0x5ce7560; nop; nop", "imul rsi, rbp, 0x4c; mov rdi, rcx")
    c(0x6f07d, "jmp 0x5ce75a0; nop; nop", "movsxd rax, edx; imul r10, rax, 0x4c")
    c(0x6f29e, "jmp 0x5ce75e0; nop; nop", "add rbx, r14; imul rsi, rax, 0x4c")
    c(0x6f514, "jmp 0x5ce7620; nop; nop", "movsxd rdi, edx; imul rsi, rdi, 0x4c")
    c(0x6febc, "jmp 0x5ce7140; nop*3", "add rsi, 0x4c; sub r14, 1")
    c(0x712b0, "jmp 0x5ce7660; nop; nop", "imul rdx, rcx, 0x4c; add rax, rdx")
    c(0x74227, "jmp 0x5ce70c0; nop*5", "add rdi, 0x4c; cmp ebx, 0x28b")
    c(0x7436d, "jmp 0x5ce76a0; nop; nop", "imul r8, rcx, 0x4c; add r8, rax")
    c(0x753c5, "jmp 0x5ce76e0; nop", "imul r11, rcx, 0x4c; mov ecx, edi")
    c(0x765e2, "jmp 0x5ce70e0; nop*5", "add rbx, 0x4c; cmp esi, 0x28b")
    c(0x768be, "jmp 0x5ce7720; nop; nop", "imul rcx, rax, 0x4c; add rbp, rcx")
    c(0x76a09, "jmp 0x5ce7760; nop; nop", "imul rbx, rcx, 0x4c; add rbx, rax")
    c(0x7743f, "jmp 0x5ce7100; nop*5", "add rdi, 0x4c; cmp ebx, 0x28b")
    c(0x1463a0, "jmp 0x5ce7120; nop*6", "add rbx, 0x4c; cmp rbp, 0x28b")
    c(0x2ce44d, "jmp 0x5ce77a0; nop; nop", "imul rcx, rcx, 0x4c; add rcx, rax")
    c(0x2cf03e, "jmp 0x5ce77e0; nop; nop", "imul rcx, rcx, 0x4c; add rcx, rax")
    c(0x2cf948, "jmp 0x5ce7820; nop; nop", "imul r8, rcx, 0x4c; add r8, rax")
    c(0x46f17b, "jmp 0x5ce78e0; nop*4", "movsx rcx, word ptr [r8 + 0x1c]; imul rdx, rcx, 0x4c")
    c(0x4b2d38, "jmp 0x5ce7860; nop; nop", "imul rcx, rcx, 0x4c; add rcx, rax")
    c(0x4ed9e4, "jmp 0x5ce78a0; nop*3", "movsx rax, r9w; imul r8, rax, 0x4c")
    # frame grows 0xb0 for the 42 dword bit vector
    c(0x6cb6c, "sub rsp, 0x160", "sub rsp, 0xb0")
    c(0x6ccf3, "lea r11, [rsp + 0x160]", "lea r11, [rsp + 0xb0]")
    # bit vector base now [rsp+0x20]
    c(0x6cc3d, "or dword ptr [rsp + rdx*4 + 0x20], eax", "or dword ptr [rbp + rdx*4 - 0x39], eax")
    c(0x6ccc2, "mov eax, dword ptr [rsp + rax*4 + 0x20]", "mov eax, dword ptr [rbp + rax*4 - 0x39]")
    c(0x6cbc2, "jmp 0x2160; nop*3", "lea rcx, [rbp - 0x39]; lea r8d, [rdx + 0x54]")  # bit vector memset: jump to cave
    p(0x2160, "lea rcx, [rsp + 0x20]; mov r8d, 0xa8; jmp 0x6cbca")  # bit vector memset cave
    d(0xaf9214, "19 31 0d 00 23 74 35 00 23 64 34 00 23 34 33 00 23 01 2c 00 18 f0 16 e0 14 d0 12 c0 10 50 00 00 e0 37 79 00 50 01 00 00", "00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")  # private unwind info for 0x6cb50 (.rdata slack)
    d(0x4e57cb0, "14 92 af 00", "b8 eb a9 00")  # unwind data of 0x6cb50 repointed
    r(0x2a0, "3c b2 1d 00", "14 b2 1d 00", tag='rdata_vsize')  # .rdata size covers the private unwind data (stack_growth enlarges it)
    c(0x3a6054, "jmp 0x5ce7920; nop", "push rbx; sub rsp, 0x20")  # dirty mark: ignore index >= 651
    c(0x78ab2, "jmp 0x5ce7990; nop; nop", "cmp dword ptr [rbx + 0x2b4], r12d")  # world init: reset the extra records

    # caves in .gsc
    # step up 0x6cbb4
    b.cave(0x020, """
            add rsi, 0x4c
            cmp edi, 0x28b
            jne L1
            lea rsi, [rva 0x5cda000]
        L1: cmp edi, 0x540
            jmp 0x6cbbe
    """)
    # step up 0x6ccdb
    b.cave(0x040, """
            add r15, 0x4c
            cmp ebx, 0x28b
            jne L1
            lea r15, [rva 0x5cda000]
        L1: cmp ebx, 0x540
            jmp 0x6cce5
    """)
    # step up 0x6e091
    b.cave(0x060, """
            add rsi, 0x4c
            cmp ebx, 0x28b
            jne L1
            lea rsi, [rva 0x5cda000]
        L1: cmp ebx, 0x540
            jmp 0x6e09b
    """)
    # step up 0x6e10b
    b.cave(0x080, """
            add r8, r14
            add rdx, 0x4c
            cmp r8, 0x28b
            jne L1
            lea rdx, [rva 0x5cda000]
        L1: jmp 0x6e112
    """)
    # step up 0x6ef2c
    b.cave(0x0a0, """
            add rbx, 0x4c
            cmp edi, 0x28b
            jne L1
            lea rbx, [rva 0x5cda02c]
        L1: cmp edi, 0x540
            jmp 0x6ef36
    """)
    # step up 0x74227
    b.cave(0x0c0, """
            add rdi, 0x4c
            cmp ebx, 0x28b
            jne L1
            lea rdi, [rva 0x5cda000]
        L1: cmp ebx, 0x540
            jmp 0x74231
    """)
    # step up 0x765e2
    b.cave(0x0e0, """
            add rbx, 0x4c
            cmp esi, 0x28b
            jne L1
            lea rbx, [rva 0x5cda02e]
        L1: cmp esi, 0x540
            jmp 0x765ec
    """)
    # step up 0x7743f
    b.cave(0x100, """
            add rdi, 0x4c
            cmp ebx, 0x28b
            jne L1
            lea rdi, [rva 0x5cda002]
        L1: cmp ebx, 0x540
            jmp 0x77449
    """)
    # step up 0x1463a0
    b.cave(0x120, """
            add rbx, 0x4c
            cmp rbp, 0x28b
            jne L1
            lea rbx, [rva 0x5cda046]
        L1: cmp rbp, 0x540
            jmp 0x1463ab
    """)
    # step down 0x6febc
    b.cave(0x140, """
            add rsi, 0x4c
            cmp r14, 0x2b6
            jne L1
            lea rsi, [rva 0x5cda004]
        L1: sub r14, 1
            jmp 0x6fec4
    """)
    # step down 0x6de96
    b.cave(0x160, """
            lea rsi, [rsi + 0x4c]
            cmp r9, 0x2b6
            jne L1
            lea rsi, [rva 0x5cda002]
        L1: cmp edx, ebx
            jmp 0x6de9c
    """)
    # imul 0x6cc1b
    b.cave(0x180, """
            cmp rdi, 0x28b
            jl L1
            cmp rdi, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul r12, rdi, 0x4c
            ~sub r12, r14
            ~add r12, r10
            pop r10
            add rsi, r12
            jmp 0x6cc22
        L1: imul r12, rdi, 0x4c
            add rsi, r12
            jmp 0x6cc22
    """)
    # imul 0x6dc13
    b.cave(0x1c0, """
            cmp rcx, 0x28b
            jl L1
            cmp rcx, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul r14, rcx, 0x4c
            ~sub r14, rdi
            ~add r14, r10
            pop r10
            mov edx, eax
            jmp 0x6dc19
        L1: imul r14, rcx, 0x4c
            mov edx, eax
            jmp 0x6dc19
    """)
    # imul 0x6df12
    b.cave(0x200, """
            cmp r15, 0x28b
            jl L1
            cmp r15, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul rsi, r15, 0x4c
            ~sub rsi, rdi
            ~add rsi, r10
            pop r10
            or r12d, 0xffffffff
            jmp 0x6df1a
        L1: imul rsi, r15, 0x4c
            or r12d, 0xffffffff
            jmp 0x6df1a
    """)
    # imul 0x6e12d
    b.cave(0x240, """
            cmp rax, 0x28b
            jl L1
            cmp rax, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul rbx, rax, 0x4c
            ~sub rbx, rbp
            ~add rbx, r10
            pop r10
            xor edx, edx
            jmp 0x6e133
        L1: imul rbx, rax, 0x4c
            xor edx, edx
            jmp 0x6e133
    """)
    # imul 0x6e1d4
    b.cave(0x280, """
            cmp r10, 0x28b
            jl L1
            cmp r10, 0x540
            jge L1
            push r11
            lea r11, [rva 0x5ccc9c0]
            imul rbx, r10, 0x4c
            ~sub rbx, rax
            ~add rbx, r11
            pop r11
            add rbx, 0x14fc
            jmp 0x6e1df
        L1: imul rbx, r10, 0x4c
            add rbx, 0x14fc
            jmp 0x6e1df
    """)
    # imul 0x6e281
    b.cave(0x2d0, """
            cmp rax, 0x28b
            jl L1
            cmp rax, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul rdx, rax, 0x4c
            ~sub rdx, rcx
            ~add rdx, r10
            pop r10
            mov rdi, r8
            jmp 0x6e288
        L1: imul rdx, rax, 0x4c
            mov rdi, r8
            jmp 0x6e288
    """)
    # imul 0x6e47f
    b.cave(0x310, """
            cmp rax, 0x28b
            jl L1
            cmp rax, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccdebc]
            imul rcx, rax, 0x4c
            ~sub rcx, rbx
            ~add rcx, r10
            pop r10
            add rbx, rcx
            jmp 0x6e486
        L1: imul rcx, rax, 0x4c
            add rbx, rcx
            jmp 0x6e486
    """)
    # imul 0x6e587
    b.cave(0x350, """
            movsxd rax, edx
            cmp rax, 0x28b
            jl L1
            cmp rax, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul rcx, rax, 0x4c
            ~sub rcx, r8
            ~add rcx, r10
            pop r10
            jmp 0x6e58e
        L1: imul rcx, rax, 0x4c
            jmp 0x6e58e
    """)
    # imul 0x6e5d2
    b.cave(0x390, """
            movsxd rax, edx
            cmp rax, 0x28b
            jl L1
            cmp rax, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul rcx, rax, 0x4c
            ~sub rcx, r8
            ~add rcx, r10
            pop r10
            jmp 0x6e5d9
        L1: imul rcx, rax, 0x4c
            jmp 0x6e5d9
    """)
    # imul 0x6e649
    b.cave(0x3d0, """
            movaps xmm0, xmmword ptr [r8]
            cmp rbx, 0x28b
            jl L1
            cmp rbx, 0x540
            jge L1
            push rax
            lea rax, [rva 0x5ccc9c0]
            imul r9, rbx, 0x4c
            ~sub r9, rcx
            ~add r9, rax
            pop rax
            jmp 0x6e651
        L1: imul r9, rbx, 0x4c
            jmp 0x6e651
    """)
    # imul 0x6e6de
    b.cave(0x410, """
            cmp rax, 0x28b
            jl L1
            cmp rax, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul rsi, rax, 0x4c
            ~sub rsi, rcx
            ~add rsi, r10
            pop r10
            mov rbx, r8
            jmp 0x6e6e5
        L1: imul rsi, rax, 0x4c
            mov rbx, r8
            jmp 0x6e6e5
    """)
    # imul 0x6e884
    b.cave(0x450, """
            cmp rdi, 0x28b
            jl L1
            cmp rdi, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul r8, rdi, 0x4c
            ~sub r8, rbx
            ~add r8, r10
            pop r10
            movsd xmm0, qword ptr [rcx]
            jmp 0x6e88c
        L1: imul r8, rdi, 0x4c
            movsd xmm0, qword ptr [rcx]
            jmp 0x6e88c
    """)
    # imul 0x6e953
    b.cave(0x490, """
            cmp rbp, 0x28b
            jl L1
            cmp rbp, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul r12, rbp, 0x4c
            ~sub r12, rsi
            ~add r12, r10
            pop r10
            lea rdi, [rsi + 0x14fc]
            jmp 0x6e95e
        L1: imul r12, rbp, 0x4c
            lea rdi, [rsi + 0x14fc]
            jmp 0x6e95e
    """)
    # imul 0x6ead6
    b.cave(0x4e0, """
            mov rdi, r8
            cmp rax, 0x28b
            jl L1
            cmp rax, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul r14, rax, 0x4c
            ~sub r14, rbp
            ~add r14, r10
            pop r10
            jmp 0x6eadd
        L1: imul r14, rax, 0x4c
            jmp 0x6eadd
    """)
    # imul 0x6ed4b
    b.cave(0x520, """
            mov r14, rcx
            cmp rsi, 0x28b
            jl L1
            cmp rsi, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul rbx, rsi, 0x4c
            ~sub rbx, rcx
            ~add rbx, r10
            pop r10
            jmp 0x6ed52
        L1: imul rbx, rsi, 0x4c
            jmp 0x6ed52
    """)
    # imul 0x6efba
    b.cave(0x560, """
            cmp rbp, 0x28b
            jl L1
            cmp rbp, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul rsi, rbp, 0x4c
            ~sub rsi, rcx
            ~add rsi, r10
            pop r10
            mov rdi, rcx
            jmp 0x6efc1
        L1: imul rsi, rbp, 0x4c
            mov rdi, rcx
            jmp 0x6efc1
    """)
    # imul 0x6f07d
    b.cave(0x5a0, """
            movsxd rax, edx
            cmp rax, 0x28b
            jl L1
            cmp rax, 0x540
            jge L1
            push r11
            lea r11, [rva 0x5ccc9c0]
            imul r10, rax, 0x4c
            ~sub r10, rcx
            ~add r10, r11
            pop r11
            jmp 0x6f084
        L1: imul r10, rax, 0x4c
            jmp 0x6f084
    """)
    # imul 0x6f29e
    b.cave(0x5e0, """
            add rbx, r14
            cmp rax, 0x28b
            jl L1
            cmp rax, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul rsi, rax, 0x4c
            ~sub rsi, rdi
            ~add rsi, r10
            pop r10
            jmp 0x6f2a5
        L1: imul rsi, rax, 0x4c
            jmp 0x6f2a5
    """)
    # imul 0x6f514
    b.cave(0x620, """
            movsxd rdi, edx
            cmp rdi, 0x28b
            jl L1
            cmp rdi, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul rsi, rdi, 0x4c
            ~sub rsi, rbx
            ~add rsi, r10
            pop r10
            jmp 0x6f51b
        L1: imul rsi, rdi, 0x4c
            jmp 0x6f51b
    """)
    # imul 0x712b0
    b.cave(0x660, """
            cmp rcx, 0x28b
            jl L1
            cmp rcx, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccdebc]
            imul rdx, rcx, 0x4c
            ~sub rdx, rax
            ~add rdx, r10
            pop r10
            add rax, rdx
            jmp 0x712b7
        L1: imul rdx, rcx, 0x4c
            add rax, rdx
            jmp 0x712b7
    """)
    # imul 0x7436d
    b.cave(0x6a0, """
            cmp rcx, 0x28b
            jl L1
            cmp rcx, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccdebc]
            imul r8, rcx, 0x4c
            ~sub r8, rax
            ~add r8, r10
            pop r10
            add r8, rax
            jmp 0x74374
        L1: imul r8, rcx, 0x4c
            add r8, rax
            jmp 0x74374
    """)
    # imul 0x753c5
    b.cave(0x6e0, """
            cmp rcx, 0x28b
            jl L1
            cmp rcx, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul r11, rcx, 0x4c
            ~sub r11, rax
            ~add r11, r10
            pop r10
            mov ecx, edi
            jmp 0x753cb
        L1: imul r11, rcx, 0x4c
            mov ecx, edi
            jmp 0x753cb
    """)
    # imul 0x768be
    b.cave(0x720, """
            cmp rax, 0x28b
            jl L1
            cmp rax, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul rcx, rax, 0x4c
            ~sub rcx, rbp
            ~add rcx, r10
            pop r10
            add rbp, rcx
            jmp 0x768c5
        L1: imul rcx, rax, 0x4c
            add rbp, rcx
            jmp 0x768c5
    """)
    # imul 0x76a09
    b.cave(0x760, """
            cmp rcx, 0x28b
            jl L1
            cmp rcx, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccdebc]
            imul rbx, rcx, 0x4c
            ~sub rbx, rax
            ~add rbx, r10
            pop r10
            add rbx, rax
            jmp 0x76a10
        L1: imul rbx, rcx, 0x4c
            add rbx, rax
            jmp 0x76a10
    """)
    # imul 0x2ce44d
    b.cave(0x7a0, """
            cmp rcx, 0x28b
            jl L1
            cmp rcx, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccdebc]
            imul rcx, rcx, 0x4c
            ~sub rcx, rax
            ~add rcx, r10
            pop r10
            add rcx, rax
            jmp 0x2ce454
        L1: imul rcx, rcx, 0x4c
            add rcx, rax
            jmp 0x2ce454
    """)
    # imul 0x2cf03e
    b.cave(0x7e0, """
            cmp rcx, 0x28b
            jl L1
            cmp rcx, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccdebc]
            imul rcx, rcx, 0x4c
            ~sub rcx, rax
            ~add rcx, r10
            pop r10
            add rcx, rax
            jmp 0x2cf045
        L1: imul rcx, rcx, 0x4c
            add rcx, rax
            jmp 0x2cf045
    """)
    # imul 0x2cf948
    b.cave(0x820, """
            cmp rcx, 0x28b
            jl L1
            cmp rcx, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccdebc]
            imul r8, rcx, 0x4c
            ~sub r8, rax
            ~add r8, r10
            pop r10
            add r8, rax
            jmp 0x2cf94f
        L1: imul r8, rcx, 0x4c
            add r8, rax
            jmp 0x2cf94f
    """)
    # imul 0x4b2d38
    b.cave(0x860, """
            cmp rcx, 0x28b
            jl L1
            cmp rcx, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccdebc]
            imul rcx, rcx, 0x4c
            ~sub rcx, rax
            ~add rcx, r10
            pop r10
            add rcx, rax
            jmp 0x4b2d3f
        L1: imul rcx, rcx, 0x4c
            add rcx, rax
            jmp 0x4b2d3f
    """)
    # imul 0x4ed9e4
    b.cave(0x8a0, """
            movsx rax, r9w
            cmp rax, 0x28b
            jl L1
            cmp rax, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul r8, rax, 0x4c
            ~sub r8, rcx
            ~add r8, r10
            pop r10
            jmp 0x4ed9ec
        L1: imul r8, rax, 0x4c
            jmp 0x4ed9ec
    """)
    # imul 0x46f17b
    b.cave(0x8e0, """
            movsx rcx, word ptr [r8 + 0x1c]
            cmp rcx, 0x28b
            jl L1
            cmp rcx, 0x540
            jge L1
            push r10
            lea r10, [rva 0x5ccc9c0]
            imul rdx, rcx, 0x4c
            ~sub rdx, rax
            ~add rdx, r10
            pop r10
            jmp 0x46f184
        L1: imul rdx, rcx, 0x4c
            jmp 0x46f184
    """)
    # dirty mark guard
    b.cave(0x920, """
            cmp ecx, 0x28b
            jl L1
            ret
        L1: .byte 0x40, 0x53
            sub rsp, 0x20
            jmp 0x3a605a
    """)
    # world init: reset extra records
    b.cave(0x990, """
            push rsi
            push rdi
            push rcx
            push rdx
            lea rdi, [rva 0x5cda000]
            mov edx, 0x2b5
        L1: lea rsi, [rva 0x5ce7940]
            mov ecx, 0x13
            rep movsd dword ptr [rdi], dword ptr [rsi]
            dec edx
            jne L1
            pop rdx
            pop rcx
            pop rdi
            pop rsi
            cmp dword ptr [rbx + 0x2b4], r12d
            jmp 0x78ab9
    """)
