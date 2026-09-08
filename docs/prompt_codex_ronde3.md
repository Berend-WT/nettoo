# Codex-opdracht ronde 3 — schuifbalk, leaderboard-archief, schaalwoorden

Kopieer alles onder de streep naar Codex.

---

## Task

Repo: Netto, a Dutch daily estimation puzzle game. Vanilla JS classic scripts, no
build step, no framework, no bundler, no dependencies. Comments and user-facing
strings in **Dutch**, matching the surrounding code.

Three jobs, independent of each other. Do them in this order.

Bump the `?v=` on every changed `js`/`css` reference in **both** `index.html` and
`website/index.html`, and mirror every changed file into `website/`. Do not touch
the question bank, `tools/`, `puzzels/`, or any file under `vragen/`.

---

## 1 — Turn the race tolerance picker into a real slider

`js/race.js` already has a working tolerance feature: `RACE_TOLERANTIES`,
`RACE_TOLERANTIE_META`, `raceTolerantieMeta`, `renderRaceTolerantieOptions`,
`selectRaceTolerantie`, and five `<button data-tolerance>` elements in
`index.html` (ids `raceSoloTolerances`, `raceOnlineTolerances`) plus a note line
(`raceSoloToleranceNote`, `raceOnlineToleranceNote`).

Replace the five buttons with **one `<input type="range">`** with five discrete
stops — the shape of an effort slider, not a row of buttons.

- `min="0" max="4" step="1"`, mapped in order to `perfect, scherp, netjes, ruim, grof`.
- The five labels (`1,00×` … `2,00×`) sit **under the track**, evenly spaced, and
  the active one is highlighted. Use a grid, not absolute positioning.
- Moving the thumb updates the note line live (`RACE_TOLERANTIE_META[...].uitleg`),
  on `input`, not only on `change`.
- Keyboard: arrow keys must move it, and the range needs `aria-valuetext` set to
  the human label (`"1,25× Netjes"`) so a screen reader announces something
  meaningful instead of the raw index.
- Keep the stored key in `RACE_MODE_CONFIG_KEY` exactly as it is (`toleranceKey`),
  so existing saved preferences and the duel handshake keep working untouched.
- `selectRaceTolerantie(mode, key)` stays the public entry point; the slider calls
  it. Keep the name exported on `window` in `js/library.js`.

Style it in `css/styles.css` next to `.race-tolerance-options`, which you replace.
The track must stay usable at the mobile width the rest of the race setup uses.

## 2 — Leaderboard archive per day

`js/core.js` has `renderLeaderboard()` with two tabs, `currentLbTab` of `'today'`
or `'streaks'`. The daily tab calls
`supabaseClient.rpc('leaderboard_dag', { p_datum: TODAY_STR })`.

**First, verify before you build.** That RPC already takes a date, but nobody has
checked whether it returns rows for older dates — that depends on the RLS policy.
Call it once with a date a few days back. If it returns nothing for past dates,
**stop and report that**; the fix is then database work and not this task.

If it does work:

- Add a day stepper to the daily tab only: `◀ dinsdag 8 september ▶`.
- Never past today, never before the first daily. Get that lower bound from the
  earliest `date` in `window.NETTO_REBUILT_PUZZLES.daily`, and treat an empty list
  as "no archive available" rather than crashing.
- Hide the stepper entirely on the streaks tab — a streak is a running total and a
  date means nothing there.
- Show the date in Dutch, and in English when the interface is English. The repo
  has `statsCopy(nl, en)` for exactly this.
- Empty day: say that nobody played that day, not that the leaderboard is broken.
  Those are different failures and the current code already distinguishes them.

## 3 — Let `eenheidUit` recognise scale words

`eenheidUit(vraag)` in `js/core.js` returns a unit label for the answer field. It
handles `duizend|miljoen|miljard` only when they sit in front of a known unit.

It therefore misses the case that actually caused wrong answers in this project:

```
Hoeveel duizend inwoners heeft Rotterdam?      -> null, should be "× 1.000"
Hoeveel miljoen inwoners heeft Mexico?         -> null, should be "× 1.000.000"
Hoeveel miljard kilometer legt licht af...?    -> handled, keep it that way
```

A counted noun is not a unit, but the **scale** is the part that misleads people:
someone types the full population instead of the number in thousands.

- When a scale word appears after `hoeveel` and is not followed by a known unit,
  return the scale on its own, formatted as `× 1.000` / `× 1.000.000` / `× 1.000.000.000`.
- Do not invent a unit for the noun itself. `Hoeveel poten heeft een krab?` must
  keep returning `null` — it already does, and that is correct.
- Add the new cases to whatever tests or checks you write; at minimum verify by
  hand that the five examples above behave as stated.

---

## Constraints

- Do not change any question, answer, or puzzle sum.
- Do not add a build step, package manager, or dependency.
- Do not reformat files you did not otherwise change.
- Everything keeps working: solo race, online duel, open games, the duration
  choice, the 12:00 Europe/London daily rollover, the Supabase sync.

## Done means

1. Opening `index.html`: the tolerance slider moves with mouse and arrow keys, the
   note updates live, and the choice survives a reload.
2. The leaderboard shows a working day stepper on the daily tab and none on streaks
   — or you reported that the RPC refuses older dates and stopped.
3. `eenheidUit` returns the scale for the three scale examples and still `null` for
   the crab.
4. `website/` mirrors every changed file with matching `?v=` values.
5. One commit, message in Dutch, explaining *why* — the repo convention is that
   commit messages justify rather than list.

Report at the end: what the leaderboard RPC did with an old date, and anything you
chose not to do.
