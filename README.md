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

## Player limit (optional)
Mods that push the player limit past 16 (tested to 32 players, with HUD). They are not in the default build. Build them on top of the default set:

    python build.py --dll path\to\original\haloreach.dll --out out --mods default,players

Each one fixes one system that is stock 16 wide. They are separate so other modders can see what has to be addressed:
- players: players datum, simulated input region and one index bound, 16 to 32.
- user_map: player to local user map and its mask table, so players 20 and up are not taken for local users.
- player_update: per tick update tables (action flags, respawn list) and action entries for players 16 to 31.
- script_lists: script lists of players and team players stop at 16 entries.
- megalo: gametype script records, player references, random order and traits only see players 0 to 15.
- player_records: control record and player registration skip index 16 and up.
- presence_records: per tick presence record builder and the water cache it used to corrupt.
- event_index: 4 bit player index in network events no longer turns into a boot event.
- glue_index: glue handle index 12 bits on the wire.
- havok_proxies: physics proxy pool 16 to 64.
- hud_players: HUD per player array 16 to 32.

Not done:
- Bots and host side tools are not included, nothing here creates players or feeds them input.
- Real networked players, session peer slots, spawning entry 31 and 33 or more players are open.
- Players 16 and up have no gametype traits, scores or statistics.
- Offline and custom games only. Built and checked against the original DLL, not yet played with the other mods here.

## Notes
- Offline and custom games only.
- Everyone in a game needs the same DLL.
- An MCC update replaces the DLL. Rebuild or redownload after updates.
- Back up your maps before using it.
