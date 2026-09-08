# Codex-opdracht — verwijder het concept "vraagsets"

Kopieer alles onder de streep naar Codex.

---

## Task

Repo: Netto, a Dutch daily estimation puzzle game. Vanilla JS classic scripts, no
build step, no framework, no bundler.

Remove the "vraagset" (question set) concept entirely. Race mode must always draw
from `window.NETTO_RACE_POOL`. Every set-related option, dropdown, tile, badge and
duel field disappears.

Code comments and user-facing strings in **Dutch**, matching the surrounding style.
Do not reformat lines you are not otherwise changing.

## Why (keep this in the commit message)

Sets were a keyword filter over the question bank, defined by matching words in the
question text. That made them fragile: rewriting a question silently moved it
between sets. They also held no unique content — every question in a set is in the
bank — while covering only 5.5% of race puzzles behind a settings screen most
players never open. The daily, the library and the breinkrakers never used them.

## Files to delete

```
data/netto_race_sets.js
website/data/netto_race_sets.js
vragen/genereer_sets.py
vragen/genereer_race_sets.py
vragen/sets/                     (whole folder)
puzzels/race_sets/               (whole folder)
```

## `js/race.js` — every site, in file order

`website/js/race.js` is byte-identical; copy the finished file over it.

| line (before edits) | what |
|---|---|
| 43-44 | `buildRaceQueue`: drop the `NETTO_RACE_SETS` branch. Source becomes `NETTO_RACE_POOL`, falling back to `REBUILT_DATA.race` when the pool is missing. Keep `setKeyOverride` out of the signature. |
| 76-91 | delete `RACE_SET_KEY` and the whole `RACE_SET_META` array |
| 92-94 | delete `getRaceSetKey` |
| 101 | `getRaceModeConfig`: drop `setKey` from the returned object |
| 113-115 | delete `raceSetMeta` |
| 183 | open-games list: drop the set badge, keep the duration badge. `joinOpenRaceGame` loses its `setKey` argument — update the `onclick` string and the function itself. |
| 245-247 | `renderRaceRoomSettings`: show duration only |
| 250-255 | delete `raceSetPuzzleCount` |
| 257-271 | delete `renderSettingsSets` |
| 273-277 | delete `selectRaceSet` |
| 296-303 | delete `renderRaceSetOptions` |
| ~315 | `renderRaceModeControls`: stop calling `renderRaceSetOptions` |
| 340-344 | delete `selectRaceModeSet` |
| 685 | `connectRaceRoom`: drop the `setKey` line and the field on `raceDuelSession` |
| 750 | guest handshake: drop the `setKey` line, keep `durationKey` |
| 772 | `handleRaceEvent('start')`: drop the `setKey` line, keep `durationKey` |

Also remove `setKey` wherever it is still written into a duel payload or an open-game
record after the above. Grep for `setKey` and `SET_META` and make sure nothing remains.

Functions in this file are global (no IIFE), so there is no export list to update.

## `index.html` — three places

`website/index.html` is identical; mirror it.

- line 25 — `<script src="data/netto_race_sets.js?v=29">`: delete the tag
- lines 458-459 — `<label for="raceSoloSet">Vraagset</label>` + its `<select>`: delete both
- lines 482-483 — the same pair for `raceOnlineSet`: delete both
- line 676 — `<div class="settings-sets" id="settingsSets">`: delete, and its heading/label if that leaves an empty settings block

Bump the `?v=` on every remaining changed `js`/`css` reference in both HTML files.

If `css/styles.css` has rules only used by the deleted markup (`.settings-set`,
`.settings-sets`, `.race-open-game-details b`), remove them from both copies.

## Constraints

- Backwards tolerance: an older client may still send `setKey` in a duel payload.
  Ignore it silently — do not throw.
- Do not touch the question bank, `tools/`, `puzzels/maak_*.py`, or any other data file.
- Do not add dependencies or a build step.
- Everything else keeps working: solo race, online duel, open games, the duration
  choice, the 12:00 Europe/London daily rollover.

## Done means

1. `grep -rn "setKey\|RACE_SET\|race_sets\|settingsSets" js/ index.html website/` returns nothing.
2. Opening `index.html`: a solo race starts and serves puzzles; the race setup screen
   shows only the duration choice; settings has no set tiles; no console errors.
3. `website/` mirrors every changed file with matching `?v=` values.
4. One commit, message in Dutch, explaining *why* — the repo convention is that commit
   messages justify rather than list.

Report at the end: which files you deleted, anything that still referenced sets after
your grep, and anything you chose not to remove.
