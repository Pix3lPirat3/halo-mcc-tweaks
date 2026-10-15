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

BASE = ['havok', 'placements', 'respawn', 'objects', 'guards', 'draw_registry', 'lighting_cache', 'boundaries', 'bone_clamp', 'stack_growth', 'render_map', 'frame_budget']
PLAYERS = ['players', 'user_map', 'player_update', 'update_guard', 'script_lists', 'megalo', 'player_records', 'presence_records', 'event_index', 'glue_index', 'havok_proxies', 'screen_effects', 'hud_players']
EXTRA = ['rank_list', 'forge_update', 'megalo_callbacks', 'respawn_rule']  # fixes that also apply past 16 players, with 32 or 64
POST = ['state_regions']  # runs after all other mods
ALL = BASE + PLAYERS + EXTRA + POST
DEFAULT = BASE  # the full set (trial19); drop stack_growth, render_map, frame_budget for the trial16 set
REQUIRED = ['havok', 'placements', 'objects', 'guards', 'draw_registry']  # they share one memory layout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dll', default=os.environ.get('HALO_REACH_DLL'), help='original haloreach.dll (build 738dd2d2)')
    ap.add_argument('--out', default=os.environ.get('HALO_REACH_OUT'), help='output file or folder')
    ap.add_argument('--mods', default=','.join(DEFAULT), help='comma separated: ' + ','.join(ALL) + '; "default" is the first twelve, "players" is the 32 player set, "players64" the same set at 64 players plus "players_extra" (respawn rule, ranking, Forge and Megalo callback fixes) and the state_regions mod, "players128" the same at 128 players, none of them in the default')
    ap.add_argument('--bounds', default=None, help='boundary toggle ids (default T1,T2,T4a,T4b,T5)')
    a = ap.parse_args()
    if not a.dll or not a.out:
        raise SystemExit('need --dll and --out')
    groups = {'default': DEFAULT, 'players': PLAYERS, 'players64': PLAYERS + EXTRA + POST, 'players128': PLAYERS + EXTRA + POST, 'players_extra': EXTRA}
    names = a.mods.split(',')
    if len([x for x in ('players', 'players64', 'players128') if x in names]) > 1:
        raise SystemExit('players, players64 and players128 exclude each other')
    want = [x for m in names for x in groups.get(m, [m])]
    mods = [m for m in ALL if m in want]
    bad = [m for m in want if m and m not in ALL]
    if bad or [m for m in REQUIRED if m not in mods]:
        raise SystemExit('unknown or missing modules: %s' % ','.join(bad or [m for m in REQUIRED if m not in mods]))
    img = open(a.dll, 'rb').read()
    if core.sha(img) != core.ORIG_SHA:
        raise SystemExit('input is not the original build 738dd2d2')
    b = core.Build(img, mods)
    b.nplayers = 128 if 'players128' in names else 64 if 'players64' in names else 32  # width of the player mods
    b.bounds = [t for t in a.bounds.split(',') if t] if a.bounds is not None else None
    for m in [m for m in mods if m not in POST] + [m for m in mods if m in POST]:
        b.cur = m
        importlib.import_module('mods.' + m).apply(b)
    b.cur = 'layout'
    layout.apply(b)
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
