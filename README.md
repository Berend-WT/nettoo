# Netto 🧩

Een quiz-puzzelgame waar je vragen uit een vragenbank (1.000+ vragen) combineert tot rekensommen: `a × b = c`, `a ÷ b + c = d` en meer.

## Spelmodi

| Modus | Beschrijving |
|---|---|
| **Dagpuzzel** | Elke dag één officiële puzzel, met streak en deelbare score |
| **Puzzels (Library)** | 237 puzzels over vier niveaus, direct speelbaar zonder unlocks. Elke vraag komt in de hele set precies één keer voor |
| **Puzzel Race** | 5 minuten, zoveel mogelijk puzzels exact oplossen — van makkelijk naar moeilijk, met directe feedback en eindscore. Ook **1v1-duel** via room-code (Supabase Realtime) |
| **Breinkrakers** | Kettingpuzzels van 4 vragen: `a op1 b op2 c = d`, **van links naar rechts** gelezen. `2 + 3 × 4` is hier dus 20 en niet 14 |
| **Daily Archive** | 35 genummerde dagpuzzels uit het archief; ze delen hun vragenset met Puzzels |

## Structuur

```
├── index.html      ← de website
├── admin.html      ← admin-paneel
├── css/ · js/      ← frontend (handgeschreven)
├── data/           ← gegenereerde puzzeldata die de browser inlaadt
│                     netto_frontend_puzzles.js  library + daily
│                     netto_race_pool.js         puzzels voor de race
│                     netto_fotos.js             foto per vraag, met licentie
│                     netto_bronnen.js           bron en bewijszin per vraag
│                     netto_breinkrakers.js      breinkrakers
│                     netto_translations_en.js   Engelse vertalingen
├── vragen/         ← vragenbank (xlsx) + reviewbladen
├── puzzels/        ← puzzelgeneratoren (maak_*.py) + hun xlsx-uitvoer
├── fotos/          ← Commons-foto's voor de daily + de scripts eromheen
├── supabase/       ← SQL-migraties, met de hand te draaien in de SQL Editor
├── tools/          ← losse hulpscripts (sync_website.py, plan_dailies.py, …)
├── docs/           ← werkafspraken tussen de agents
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
python -m http.server 8765
# open http://127.0.0.1:8765
```

## Puzzelbanken opnieuw genereren

```bash
python puzzels/maak_unieke_puzzels.py --doel puzzels --schrijf   # library + daily
python puzzels/maak_unieke_puzzels.py --doel race --schrijf      # racepool
python puzzels/maak_breinkrakers.py                              # breinkrakers
python tools/controleer_puzzels.py                               # controle achteraf
```

`controleer_puzzels.py` leest de weggeschreven bestanden en niet wat de generator
bewéért: het controleert onder meer of `a op b = c` echt uitkomt, of elke vraag
maar in één puzzel staat en of geen puzzel twee vragen uit dezelfde kleurfamilie
heeft. Draai hem na elke wijziging aan de puzzeldata.

## Online zetten

De site draait op GitHub Pages en wordt gepubliceerd door
`.github/workflows/pages.yml` bij elke push naar `main`. Wat online gaat is
`website/`, niet de project-root: dezelfde frontend, zonder de vragenbank, de
generatoren en de fotominiaturen. De workflow draait eerst
`sync_website.py --check`, dus een vergeten synchronisatie laat de bouw falen in
plaats van stilletjes een oude versie te publiceren.

Eenmalig aanzetten: **Settings -> Pages -> Source: GitHub Actions**. Tot dat
gebeurd is faalt de publiceerstap met "Pages is not enabled".

Bij een nieuw webadres hoort ook een ronde in Supabase: **Authentication ->
URL Configuration**, het adres toevoegen bij *Redirect URLs* en desgewenst als
*Site URL*. Zonder dat komt iedereen die zich aanmeldt of zijn wachtwoord
vergeet op een dood linkje uit. De frontend stuurt zijn eigen adres mee
(`eigenAdres()` in `js/core.js`), maar Supabase negeert een adres dat niet in
die lijst staat.

## Backend

Auth en score-sync draaien op Supabase (`bqatnnouxkjdzvvhqbly`). De anon key in
`js/core.js` is een publieke client key.

**Spelen kan zonder account.** De dagpuzzel, de puzzels, de catalogus, de
breinkrakers en de solo-race werken uitgelogd; scores staan dan in localStorage.
Een account is nodig voor drie dingen: het leaderboard, online duels en het
insturen van vragen. Wie inlogt stuurt zijn lokaal gespeelde dagpuzzels alsnog
op (`stuurLokaleScoresOp` in `js/core.js`), zodat die niet verloren gaan.

Accounts: e-mail + wachtwoord, minimaal 6 tekens, met wachtwoord-vergeten-flow
en Nederlandse foutmeldingen.

Twee instellingen in het Supabase-dashboard horen hierbij:

- **Authentication -> Sign In / Providers -> Email**: *Confirm email* uit. Staat
  hij aan, dan verstuurt elke registratie een mail, en de ingebouwde mailserver
  van Supabase knijpt dat af tot een handvol per uur — daarna krijgt iedereen
  een 429 in plaats van een account.
- **Authentication -> Policies / Password**: minimale wachtwoordlengte 6, gelijk
  aan wat de frontend controleert.

Draai `supabase/leaderboard_controle.sql` om te zien of het scorebord alles heeft
wat het nodig heeft; dat script eindigt met een rapport per onderdeel.
