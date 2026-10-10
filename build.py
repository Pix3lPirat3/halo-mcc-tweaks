"""Build a patched haloreach.dll from the original.
Needs Python 3.10+, capstone and keystone-engine (pip install capstone keystone-engine).
Usage: python build.py --dll ORIGINAL --out OUTPUT [--mods a,b,c] [--bounds T1,T2,...]
Paths come from the arguments or the HALO_REACH_DLL and HALO_REACH_OUT environment variables."""
import argparse
import importlib
import os
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import core
import layout

ALL = ['havok', 'placements', 'respawn', 'objects', 'guards', 'draw_registry', 'lighting_cache', 'boundaries', 'bone_clamp', 'stack_growth']
DEFAULT = [m for m in ALL if m != 'stack_growth']
REQUIRED = ['havok', 'placements', 'objects', 'guards', 'draw_registry']  # they share one memory layout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dll', default=os.environ.get('HALO_REACH_DLL'), help='original haloreach.dll (build 738dd2d2)')
    ap.add_argument('--out', default=os.environ.get('HALO_REACH_OUT'), help='output file or folder')
    ap.add_argument('--mods', default=','.join(DEFAULT), help='comma separated: ' + ','.join(ALL))
    ap.add_argument('--bounds', default=None, help='boundary toggle ids (default T1,T2,T4a,T4b,T5)')
    a = ap.parse_args()
    if not a.dll or not a.out:
        raise SystemExit('need --dll and --out')
    mods = [m for m in ALL if m in a.mods.split(',')]
    bad = [m for m in a.mods.split(',') if m and m not in ALL]
    if bad or [m for m in REQUIRED if m not in mods]:
        raise SystemExit('unknown or missing modules: %s' % ','.join(bad or [m for m in REQUIRED if m not in mods]))
    img = open(a.dll, 'rb').read()
    if core.sha(img) != core.ORIG_SHA:
        raise SystemExit('input is not the original build 738dd2d2')
    b = core.Build(img, mods)
    b.bounds = [t for t in a.bounds.split(',') if t] if a.bounds is not None else None
    layout.apply(b)
    for m in mods:
        b.cur = m
        importlib.import_module('mods.' + m).apply(b)
    b.cur = 'layout'
    layout.info(b)
    out = b.finish()
    n, soi = core.verify_pe(out)
    path = os.path.join(a.out, 'haloreach.dll') if os.path.isdir(a.out) or not os.path.splitext(a.out)[1] else a.out
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    open(path, 'wb').write(out)
    assert open(path, 'rb').read() == out
    print('mods %s' % ','.join(mods))
    print('patches %d, sections %d, SizeOfImage 0x%x, PE and overlap checks passed' % (len(b.patches), n, soi))
    print('sha256 %s' % core.sha(out))


if __name__ == '__main__':
    main()
