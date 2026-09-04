# Netto — website-map

Alle bestanden die de website nodig heeft, in één map. Dit is een gegenereerde spiegel: bewerk deze kopie niet rechtstreeks. De canonieke site staat in de project-root.

## Inhoud

| Bestand | Wat het is |
|---|---|
| `index.html` | De volledige site (home, puzzels, race, duel, daily archive) |
| `admin.html` | Het Supabase-adminpaneel |
| `css/styles.css` | Alle styling |
| `js/core.js` | Dagpuzzel, scoring, accounts en navigatie |
| `js/puzzle-modes.js` | Library, puzzelweergave en Breinkrakers |
| `js/race.js` | Solo-race, themasets en online 1v1 |
| `js/submissions.js` | Vraag- en puzzelinsturingen |
| `js/library.js` | Kaarten, archief en algemene pagina-acties |
| `js/app.js` | Kleine frontend-bootstrap |
| `netto_frontend_puzzles.js` | Puzzeldata: 200 library + 88 race + 28 daily puzzels |
| `puzzles_embedded.js` | Oude puzzeldata (wordt nog geladen door index.html) |

## Synchroniseren

Voer dit vanuit de project-root uit na iedere frontendwijziging:

```bash
python tools/sync_website.py
python tools/sync_website.py --check
```

Externe afhankelijkheden (alleen internet nodig, geen installatie): Google Fonts en de Supabase JS SDK via CDN.

## Starten

Zit in deze map en start een statische server, bijvoorbeeld:

```bash
cd website
python -m http.server 5500
```

Open daarna <http://localhost:5500>.

## Wat je kunt testen

1. **Solo Puzzel Race** — kies tijd en set, en los zoveel mogelijk puzzels exact op.
2. **Duel (1v1)** — log in met twee accounts en speel via een open game of room-code.
3. **Puzzels-tab** — alle 200 puzzels, verdeeld over vier moeilijkheden.
4. **Daily Archive** — 28 genummerde puzzels.

Je eigen race-record staat in `localStorage` onder sleutel `netto_race_best`.
