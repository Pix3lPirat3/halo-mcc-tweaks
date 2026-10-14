# Branch dev (experimental)

This branch shows work in progress. It holds everything on player-limit plus changes that ran offline with scripted players at 128 but have not run in a real lobby. Expect rough edges:
- Tested offline only: Forge at 128 players, Slayer at 128, and Slayer, Juggernaut, Swat, Elite Slayer and Escalation at 64 (Escalation also at 128).
- Not tested in a real lobby. An earlier build of the event change crashed the game when a lobby cloned a game variant; the fix is only tested with an emulator.
- Incomplete: statistics, scoreboard rows past 24, spawning when every spawn point is blocked, real networked players, objective gametypes, and two record readers that still use the old array.
- Builds may crash or desync with stock peers and with other builds. Do not use them online with other people. Everyone in a game needs the same DLL.
- Each mod docstring ends with its test state.

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
    python build.py --dll path\to\original\haloreach.dll --out out --mods default,players128,megalo128

`players` is the 32 player set. `players64` and `players128` are the same mods at 64 and 128 players plus the fixes marked below and the state_regions mod. Pick one of the three. `megalo128` goes on top of `players128` (not on its own) and takes the place of the megalo and megalo_callbacks guards. The fixes also work on their own, for the 32 set add `players_extra`.

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
- state_regions (fix): the allocator that hands out game state memory never checks the end of a region. With many players the player tables fill region 4 and what sits behind it is overwritten: pools wrap, the game thread stops, and pools above 127 or 135 entries crash. This grows regions 4 and 1 of the game state (123 sites). Used by players64 and players128.
- score_list (fix): the list of scores written for the leading score has room for 18 entries and no bound. From 19 present players in Slayer it overwrote the stack check and the game closed. It stops at 16 entries.
- score_block (fix, 128 only): the score block holds 16 player scores and the team scores and flags sit right behind them. With 128 players a kill ended Slayer at once. At 128 the block is replaced by a bigger one and 43 instructions that address the team scores and flags are moved.
- megalo_records (megalo128): gametype script records, variables, timers and loops for players 16 to 127 (40 record instructions, 6 loops, the random order list, the navpoint mask, 27 Forge sandbox row instructions and 5 variable readers).
- stats_guard (megalo128): the statistics functions that use the raw player index skip players 16 and up, so those players have no statistics.
- events128 (dev128): player index up to 127 in the optional player fields of events (7 bits for five event types, a copy of the original 4 bit writer for six other callers). Changes the wire format. An earlier version crashed in a real lobby when a game variant was cloned; this fix is only tested with an emulator.

Open:
- Real networked players and session peer slots. Nothing here creates players or feeds them input.
- Three gametype script readers of the 16 record array are not guarded (they only read).
- Scoreboard rows stop at 24.
- More than 128 players.
- Players 16 and up have no statistics. Without megalo128 they also have no gametype traits or scores.
- With megalo128, two instructions in functions without a function record still read the old record array (the free for all team getter at 0x147f94 and the respawn rule at 0x149897, which respawn_rule bypasses).
- The 128 set ran offline with scripted players in Forge and in Slayer. With megalo128, Slayer, Juggernaut, Swat, Elite Slayer and Escalation ran with 64 players and Escalation with 128. Nothing here has been tried in an online lobby, and megalo128 is the least tested part. Offline and custom games only.

## Notes
- Offline and custom games only.
- Everyone in a game needs the same DLL.
- An MCC update replaces the DLL. Rebuild or redownload after updates.
- Back up your maps before using it.
