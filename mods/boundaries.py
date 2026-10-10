"""Boundary toggles: kill volumes, soft ceilings and world limits (default set T1 T2 T4a T4b T5)."""

# id: (rva, new, was)
TOGGLES = {
    'T1': (0x153350, "ret; nop; nop", "mov rax, rsp"),  # scenario volume query off (kill volumes)
    'T2': (0x4a100c, "ret; nop; nop", "mov rax, rsp"),  # biped boundary state machine off
    'T2b': (0x4a11f1, "jmp 0x4a12cf; nop", "je 0x4a12cf"),  # skip the placed boundary object loop
    'T3': (0x1f75c0, "~xor eax, eax; ret", "mov rax, rsp"),  # megalo out-of-bounds condition false
    'T4a': (0x1585c, "mov al, 1; ret; nop; nop", "mov qword ptr [rsp + 8], rbx"),  # forge valid area test returns 1
    'T4b': (0x154630, "~xor eax, eax; ret; nop", "push rbp; push r12"),  # forge soft ceiling touch returns 0
    'T4c1': (0x758b4, "nop; nop", "jne 0x758db"),  # alternative to T4b inside 0x75810
    'T4c2': (0x758d9, "jmp 0x75911", "jne 0x75911"),  # alternative to T4a inside 0x75810
    'T5': (0x15557c, "~xor eax, eax; ret; nop; nop", "mov qword ptr [rsp + 0x20], rbx"),  # soft ceiling physics off
    'T6': (0x1dbd70, "ret; nop*4", "mov qword ptr [rsp + 0x10], rbx"),  # observer camera bounds off
    'T6b': (0x15363c, "~xor eax, eax; ret; nop; nop", "mov qword ptr [rsp + 8], rbx"),  # point in kill volume returns 0 (camera only)
    'T7': (0x46ca14, "jmp 0x46ca57", "jne 0x46ca57"),  # world cube range test skipped
}
DEFAULT = ['T1', 'T2', 'T4a', 'T4b', 'T5']


def apply(b):
    ids = b.bounds if b.bounds is not None else DEFAULT
    for t in ids:
        rva, new, was = TOGGLES[t]
        b.code(rva, new, was)
    # bit i of the mask = position in TOGGLES, stored in the GSXF info block
    b.toggle_mask = sum(1 << list(TOGGLES).index(t) for t in ids)
