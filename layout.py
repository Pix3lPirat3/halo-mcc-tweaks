"""PE layout: three added sections (.gsx, .gsc, .gsy) and the GSXF feature block."""
import struct

from core import FILE_ALIGN, GSC_SIZE, GSC_VA, GSX_VA, GSY_VA


def section(name, vsize, va, rsize, rptr, flags):
    return struct.pack('<8sIIIIIIHHI', name, vsize, va, rsize, rptr, 0, 0, 0, 0, flags).hex()


def apply(b):
    """section headers; run after the mods so .gsy has its final size"""
    gsc_ptr = (len(b.img) + FILE_ALIGN - 1) & ~(FILE_ALIGN - 1)
    b.cur = 'layout'
    b.raw(0x16e, '0a 00', '07 00')  # NumberOfSections 7 -> 10
    b.raw(0x1b8, struct.pack('<I', GSY_VA + b.gsy_size).hex(), '00 a0 ed 04')  # SizeOfImage ends after .gsy
    zero = '00' * 40
    b.raw(0x388, section(b'.gsx', 0xe0d000, GSX_VA, 0, 0, 0xc0000080), zero)  # havok heap and placement extras, RW
    b.raw(0x3b0, section(b'.gsc', 0x1000, GSC_VA, GSC_SIZE, gsc_ptr, 0x60000020), zero)  # caves and info blocks, RX
    b.raw(0x3d8, section(b'.gsy', b.gsy_size, GSY_VA, 0, 0, 0xc0000080), zero)  # object tables, save queue, draw pools, RW


def info(b):
    """GSXF: feature bits (1 boundaries, 2 bone clamp) and the boundary toggle mask"""
    feat = (1 if b.enabled('boundaries') else 0) | (2 if b.enabled('bone_clamp') else 0)
    b.blob(0xc40, struct.pack('<4sHHII', b'GSXF', 1, 0, feat, getattr(b, 'toggle_mask', 0)))
