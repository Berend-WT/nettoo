# Codex-opdracht ronde 4 — foto's op alle puzzelschermen, plus een bronnenpagina

Kopieer alles onder de streep naar Codex.

---

## Task

Repo: Netto, a Dutch daily estimation puzzle game. Vanilla JS classic scripts, no
build step, no framework, no dependencies. Comments and user-facing strings in
**Dutch**, matching the surrounding code.

Two jobs. Mirror every changed file into `website/` and bump the `?v=` on every
changed `js`/`css` reference in **both** `index.html` and `website/index.html`.

**Stay out of these — someone else is working in them right now:**
`vragen/`, `puzzels/`, `tools/`, and every file under `data/`. Read `data/` freely,
never write to it.

## The data you get

Puzzles now carry their own photo. `window.NETTO_REBUILT_PUZZLES.library[n]`,
`.daily[n]` and every entry of `window.NETTO_RACE_POOL` may have:

```js
photo: {
  url:      "https://thumb.wikimedia.org/.../330px-Foo.jpg",
  pagina:   "https://commons.wikimedia.org/wiki/File:Foo.jpg",
  licentie: "CC BY-SA 4.0",
  maker:    "Hans Hillewaert",
  vraag:    2            // 1, 2 or 3 — which question the photo belongs to
}
```

Coverage: daily 32/35, library 165/240, race pool 186/272. A puzzle without a
photo simply has no `photo` key — render nothing, no placeholder.

## 1 — Show the photo on the library, premium and race screens

The Daily already does this. `renderDailyPhoto()` and `gekoppeldeFoto()` in
`js/core.js` are the working example: they prefer an editorial `image_path`, then
`puzzle.photo`, then a decorative rotation, and they render the credit through
`renderDailyPhotoCredit()`.

The other three screens have no photo element at all:

| screen | container | rendered by |
|---|---|---|
| bibliotheek | `#libraryQuestionList` | `js/library.js` |
| premium | `#premiumQuestionList` | `js/library.js` |
| race | `#raceQuestionList` | `js/race.js` |

Add the photo to each, reusing the Daily's markup and CSS classes
(`.daily-photo` and friends) rather than inventing a second style. On wide screens
the Daily pins it as a polaroid on the card edge — see the `@media (min-width:
1000px)` block near the top of `css/refinement.css`. Match that.

- The caption must name the question it belongs to, as the Daily does
  ("Bij vraag 2 ↗").
- **The credit is not optional.** CC BY and CC BY-SA require attribution, and
  `maker` plus `licentie` are in the data for exactly that reason. A photo without
  its credit must not be rendered.
- In the race the photo must not slow anything down: set `loading="lazy"` and
  never let a missing image shift the layout.

## 2 — A page listing every photo credit

Add a screen reachable from the menu, "Fotoverantwoording" / "Photo credits",
listing every distinct photo in use: thumbnail, maker, licence, and a link to the
Commons file page.

- Build it from the data at runtime — do not hardcode a list, and do not write a
  new file into `data/`.
- De-duplicate on `pagina`: the same photo can serve more than one puzzle.
- Sort by maker, then by licence.
- Link out with `target="_blank" rel="noopener"`.
- Say at the top, in one sentence, that the photos come from Wikimedia Commons and
  are used under the licence named per photo.

## Constraints

- Do not change any question, answer, or puzzle sum.
- Do not add a build step, package manager, or dependency.
- Do not reformat files you did not otherwise change.
- Everything keeps working: the Daily, the library, the race and its duel, the
  12:00 Europe/London rollover.

## Done means

1. Opening `index.html`: a library puzzle with a photo shows it with its credit;
   one without shows nothing and no gap.
2. The same in the race and on the premium screen.
3. The credits page lists every photo once, with a working Commons link.
4. `website/` mirrors every changed file with matching `?v=` values.
5. One commit, message in Dutch, explaining *why* — the repo convention is that
   commit messages justify rather than list.

Report at the end: how many distinct photos the credits page found, and anything
you chose not to do.
