# halo-mcc-tweaks

Patches for haloreach.dll (Halo Reach in MCC). Works with MCC 1.3528 only (original DLL sha256 738dd2d24ea3aea12e1ee9aa4a61094bf116027d42004c35a19e5048608b0894).

## What it does
- Forge: 1344 placements (stock 651).
- Object limit 4096 (stock 2048).
- More draw, lighting and Havok capacity (no flicker or missing objects with many objects).
- Map boundaries and kill barriers removed.

## Use
1. Download haloreach.dll from Releases, or build it (below).
2. Close MCC.
3. Go to the MCC folder, `haloreach` subfolder. Copy `haloreach.dll` somewhere as a backup.
4. Replace it with the patched `haloreach.dll`.
5. Start MCC with anti-cheat off.

To undo: put the backup back, or verify game files in Steam.

## Build
    pip install capstone keystone-engine
    python build.py --dll path\to\original\haloreach.dll --out out

Output is `out\haloreach.dll`. Use `--mods a,b,c` to pick mods (see `build.py`).

## Notes
- Offline and custom games only.
- Everyone in a game needs the same DLL.
- An MCC update replaces the DLL. Rebuild or redownload after updates.
- Back up your maps before using it.
