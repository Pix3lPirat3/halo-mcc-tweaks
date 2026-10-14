"""Navpoint markers above players for more than 16 players. Two fixes. First, the navpoint manager of a local user keeps 20 slots; when all are taken the slot finder returns minus 1 and the code wrote an entry of 0x88 bytes in front of the manager every frame, so two markers flashed and memory in front of the manager was overwritten. It now drops the marker instead. The 20 slot cap itself stays. Second, friendly players farther than 8 units show only while a line of sight bit is set for them, and the routine that sets the bits (0x7bbc0) cycled its target with a mask of 15, so only players 0 to 15 were ever tested. The mask is 127 now and the routine runs 4 times per tick so the cycle stays short; the bit storage for 128 players comes from megalo_records, so that fix is only active with it. Test state: ran offline with scripted players in Slayer at 33 and 64 (the line of sight set then holds players above 16, no crash); not tested in a real lobby yet."""


def apply(b):
    fo = b.rva2fo(0x2cafa2)
    assert bytes(b.img[fo:fo + 10]).hex() == '4863cb4869d188000000'
    cave = b.pcode("""
        test ebx, ebx
        js done
        movsxd rcx, ebx
        imul rdx, rcx, 0x88
        jmp 0x2cafac
        done:
        jmp 0x2cb00f
    """)
    b.hook(0x2cafa2, 10, cave)
    if not b.enabled('megalo_records'):
        return
    fo = b.rva2fo(0x7bc1f)
    assert bytes(b.img[fo:fo + 7]).hex() == '4181e10f000080'
    fo = b.rva2fo(0x7bc2b)
    assert bytes(b.img[fo:fo + 4]).hex() == '4183c9f0'
    b.data(0x7bc22, '7f', '0f')
    b.data(0x7bc2e, '80', 'f0')
    fo = b.rva2fo(0x7c971)
    assert bytes(b.img[fo:fo + 5]).hex() == 'e84af2ffff'
    cave = b.pcode("""
        sub rsp, 0x28
        call 0x7bbc0
        call 0x7bbc0
        call 0x7bbc0
        call 0x7bbc0
        add rsp, 0x28
        ret
    """)
    b.data(0x7c971, __import__('core').asm('call 0x%x' % cave, 0x7c971).hex(), 'e84af2ffff')
