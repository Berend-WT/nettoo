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
├── index.html                  ← de website
├── admin.html                  ← admin-paneel
├── css/ · js/                  ← frontend
├── netto_frontend_puzzles.js   ← puzzeldata voor de site (library + race + daily)
├── netto_breinkrakers.js       ← breinkrakers-puzzeldata
├── puzzles_embedded.js         ← dagpuzzels
├── vragen/                     ← vragenbank (xlsx) + duplicaten-review
├── puzzels/                    ← puzzelbanken (xlsx) + generatoren (maak_*.py)
└── website/                    ← losse, zelfstandige kopie voor lokale tests
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
