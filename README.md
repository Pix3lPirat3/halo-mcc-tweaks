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
Mods that push the player limit past 16, to 32, 64 or 128. They are not in the default build. Build them on top of the default set:

    python build.py --dll path\to\original\haloreach.dll --out out --mods default,players
    python build.py --dll path\to\original\haloreach.dll --out out --mods default,players64
    python build.py --dll path\to\original\haloreach.dll --out out --mods default,players128

`players` is the 32 player set. `players64` and `players128` are the same mods at 64 and 128 players plus the fixes marked below and the state_regions mod. Pick one of the three. The fixes also work on their own, for the 32 set add `players_extra`.

Each mod fixes one system that is stock 16 wide. They are separate so other modders can see what has to be addressed:
- players: players datum, simulated input region and one index bound, 16 to 32 or 64.
- user_map: player to local user map and its mask table, so players 20 and up are not taken for local users. At 64 the block grows to 0x298 bytes and its later fields move, at 128 it is 0x4d8 bytes.
- player_update: per tick update tables (action flags, respawn list) and action entries for players 16 and up (a 64 bit mask at 64, a bit string at 128).
- script_lists: script lists of players and team players stop at 16 entries.
- megalo: gametype script records, player references, random order and traits only see players 0 to 15.
- player_records: control record and player registration skip index 16 and up.
- presence_records: per tick presence record builder and the water cache it used to corrupt.
- event_index: 4 bit player index in network events no longer turns into a boot event.
- glue_index: glue handle index 12 bits on the wire.
- havok_proxies: physics proxy pool 16 to 64, and 152 at 128 players.
- screen_effects: screen effect pool, one entry per player, 136 at 128 players (64 at most otherwise).
- hud_players: HUD per player array 16 to 32, 64 or 128.
- rank_list (fix): player ranking list stops at 16 entries. Past 32 it overran the collision pair cache and hung the game at about 50 players.
- forge_update (fix): Forge per player update skips player 16 and up, it wrote into the score block.
- megalo_callbacks (fix): per tick gametype script callbacks, the record initialiser, the player index change and the navpoint functions treat index 16 and up as no player.
- respawn_rule (fix): players 16 and up read the respawn rule from other memory and could stay dead for minutes. They now get no wait rule.
- state_regions (fix): the allocator that hands out game state memory never checks the end of a region. With many players the player tables fill region 4 and what sits behind it is overwritten: pools wrap, the game thread stops, and pools above 127 or 135 entries crash. This grows regions 4 and 1 of the game state (about 190 sites). Used by players64 and players128.

Open:
- Real networked players and session peer slots. Nothing here creates players or feeds them input.
- Three gametype script readers of the 16 record array are not guarded (they only read).
- Scoreboard rows stop at 24.
- More than 128 players.
- Players 16 and up have no gametype traits, scores or statistics.
- Not tested with real gametypes. Offline and custom games only. The 128 set and the new mods are built and checked against the original DLL, not yet played here.

## Notes
- Offline and custom games only.
- Everyone in a game needs the same DLL.
- An MCC update replaces the DLL. Rebuild or redownload after updates.
- Back up your maps before using it.
