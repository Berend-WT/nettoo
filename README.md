# Netto 🧩

Een quiz-puzzelgame waar je vragen uit een vragenbank (1.000+ vragen) combineert tot rekensommen: `a × b = c`, `a ÷ b + c = d` en meer.

## Spelmodi

| Modus | Beschrijving |
|---|---|
| **Dagpuzzel** | Elke dag één officiële puzzel, met streak en deelbare score |
| **Puzzels (Library)** | 200 puzzels opgesplitst per moeilijkheid (50 per niveau × 50 per operator), direct speelbaar zonder unlocks |
| **Puzzel Race** | 5 minuten, zoveel mogelijk puzzels exact oplossen — van makkelijk naar moeilijk, met directe feedback en eindscore. Ook **1v1-duel** via room-code (Supabase Realtime) |
| **Breinkrakers** | Uitdagende kettingpuzzels: `a (× of ÷) b + of − c = d` — 4 vragen per puzzel |
| **Daily Archive** | 28 genummerde Hard-puzzels uit het archief |

## Structuur

```
├── index.html      ← de website
├── admin.html      ← admin-paneel
├── css/ · js/      ← frontend (handgeschreven)
├── data/           ← gegenereerde puzzeldata die de browser inlaadt
│                     netto_frontend_puzzles.js  library + race + daily
│                     netto_race_sets.js         regio- en themasets
│                     netto_race_pool.js         6.000 puzzels voor de race
│                     netto_breinkrakers.js      breinkrakers
│                     netto_translations_en.js   Engelse vertalingen
├── vragen/         ← vragenbank (xlsx) + reviewbladen
├── puzzels/        ← puzzelgeneratoren (maak_*.py) + hun xlsx-uitvoer
├── fotos/          ← Commons-foto's voor de daily + de scripts eromheen
├── supabase/       ← SQL-migraties, met de hand te draaien in de SQL Editor
├── tools/          ← losse hulpscripts (sync_website.py, plan_dailies.py, …)
├── docs/           ← briefings en samenwerkingsnotities
└── website/        ← gegenereerde, zelfstandige kopie; nooit met de hand wijzigen
```

Alles in `data/` en `website/` wordt gegenereerd. Werk in de project-root en draai
daarna `python tools/sync_website.py`.

## Frontendmodules

`js/app.js` is alleen de bootstrap. De spellogica is per verantwoordelijkheid verdeeld:

- `js/core.js` — configuratie, dagelijkse puzzel, scoring, accounts en navigatie;
- `js/puzzle-modes.js` — generieke puzzelweergave, Library en Breinkrakers;
- `js/race.js` — solo-race, themasets en online 1v1;
- `js/submissions.js` — vraag- en puzzelinsturingen;
- `js/library.js` — kaarten, archief, modals en algemene pagina-acties.

De bestanden worden als gewone scripts in vaste volgorde geladen. Daardoor blijft de bestaande frontend zonder bundler werken.

## Website-kopie synchroniseren

Werk alleen in de project-root. Werk daarna de zelfstandige kopie bij en controleer hem:

```bash
python tools/sync_website.py
python tools/sync_website.py --check
```

## Lokaal draaien

```bash
python -m http.server 5500
# open http://localhost:5500
```

## Puzzelbanken opnieuw genereren

```bash
python puzzels/maak_puzzels.py          # hoofdpuzzelbank
python puzzels/maak_puzzels_race.py     # race + daily set
python puzzels/maak_breinkrakers.py     # breinkrakers (100k puzzels)
python puzzels/maak_alle_puzzels.py     # alle 4,2 miljoen mogelijke puzzels
```

## Backend

Auth en score-sync draaien op Supabase (`bqatnnouxkjdzvvhqbly`). De anon key in `js/app.js` is een publieke client key. Accounts: e-mail + wachtwoord, met wachtwoord-vergeten-flow, Nederlandse foutmeldingen, invoervalidatie en een registratielimiet van 5 per uur per browser.
