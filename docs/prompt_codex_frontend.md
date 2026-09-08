# Codex-opdracht — Netto frontend, drie verbeteringen

Kopieer alles onder de streep naar Codex.

---

## Task

Repo: Netto, a Dutch daily estimation puzzle game. Vanilla JS classic scripts, no
build step, no framework. Add three features to the frontend. Do **not** touch the
question bank, the puzzle generators in `puzzels/`, or anything in `tools/`.

Write code comments and all user-facing strings in **Dutch**, matching the existing
style in `js/core.js`. Match the surrounding code: no TypeScript, no ES modules, no
new dependencies, no CDN links.

## Files you will touch

| file | what |
|---|---|
| `js/core.js` | all logic; loaded as a classic script with `defer` |
| `index.html` | markup + the `?v=` cache-busting param on the script tag |
| `data/netto_frontend_puzzles.js` | read-only for you — do not regenerate |
| `website/` | deploy mirror; copy any changed file here too |

Bump the `?v=` query param on every changed `js`/`css` reference in **both**
`index.html` and `website/index.html`, or the change will not reach users.

## Data you can rely on

`window.NETTO_REBUILT_PUZZLES` is `{library: [200], daily: [35], race: [88], reserve: []}`.
Every puzzle object:

```js
{ id, number, name, operator, q1_label, q1_answer, q2_label, q2_answer,
  q3_label, q3_answer, calculation, categories: [c1, c2, c3],
  difficulty, difficulty_score }
```

`daily` entries additionally carry `date` (`"2026-08-23"`) and `source_library_id`.
`operator` is one of `+ − × ÷` (note: U+2212 minus and U+00D7 multiply, not ASCII).
Answers are integers. `categories` is a 3-element array of Dutch category names;
`js/core.js` already maps those to icons.

---

## Feature 1 — Unit label in the answer field

Each question asks for a number in a specific unit (meters, days, countries…).
Today the unit lives only inside the question text, which has caused real answer
bugs. Show it in the input.

- Derive the unit from the question text. Dutch questions are shaped like
  `Hoeveel <eenheid> ...?` or `Hoeveel ... in <eenheid>?` or `Hoeveel <ding> heeft ...?`.
  Write a small `eenheidUit(vraag)` helper with an explicit list of recognised units
  (meter, kilometer, centimeter, millimeter, kilogram, gram, ton, liter, procent,
  graden, seconden, minuten, uren, dagen, maanden, jaren, …). Return `null` when
  nothing matches — most questions ask for a count, and then no label is shown.
- Render it as static grey text inside the right edge of the input, not as a
  placeholder, so it stays visible while typing.
- Never let the label affect the submitted value.

Do not hardcode a per-question table. The helper must work on the data as it is.

## Feature 2 — Source panel after answering

Once a question is answered, offer a collapsed panel showing where the answer
comes from. Everything needed is already in the question bank but is **not yet in
the frontend data**, so:

- Add a **new** generated file `data/netto_bronnen.js` setting
  `window.NETTO_BRONNEN = { "<vraagtekst>": { bron: "<url>", uitleg: "<zin>" } }`,
  keyed by the exact `q*_label` string.
- Write the generator as `tools/maak_bronnenbestand.py`, reading
  `vragen/vragen_review_compleet.xlsx` sheet `Vragen`, columns `Vraag NL`,
  `Bron (geverifieerd)`, `Bewijszin`. Follow the file layout of the existing
  scripts in `tools/` (module docstring in Dutch explaining *why*, `main()`,
  `if __name__ == '__main__':`).
- In the UI: a collapsed row labelled **"Waar komt dit vandaan?"**. Expanded it
  shows the explanation sentence and the source as a link opening in a new tab
  with `rel="noopener"`.
- If a question has no entry, render nothing at all — no empty panel.

## Feature 3 — Category colour per question

Each of the three questions in a puzzle already has its own category. Give each
question card a background tint derived from its category, so a puzzle reads as
three visually distinct steps.

- Define the palette as CSS custom properties, one per category, in the existing
  stylesheet. There are 29 categories; group them into roughly 8 colour families
  rather than inventing 29 colours.
- Text must stay readable: check contrast against the tint, and keep the existing
  dark/light behaviour working.
- No colour may be defined only inside a media query.

---

## Constraints

- Do not change any answer, question text, or puzzle sum.
- Do not add a build step, package manager, or dependency.
- Do not reformat files you did not otherwise change.
- Keep every existing feature working, including the 12:00 Europe/London daily
  rollover and the Supabase sync in `js/core.js`.

## Done means

1. `python tools/maak_bronnenbestand.py` runs and writes `data/netto_bronnen.js`.
2. Opening `index.html` locally: a puzzle plays end to end, the unit label appears
   where a unit exists, the source panel opens and links out, and the three cards
   are visibly different colours.
3. `website/` mirrors every changed file, with matching `?v=` values.
4. One commit, message in Dutch, explaining *why* each change was made — the repo
   convention is that commit messages justify rather than list.

Report at the end: which units your helper recognises, how many of the 1416
questions got a source entry, and anything you chose not to do.
