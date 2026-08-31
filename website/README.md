# Netto — website-map

Alle bestanden die de website nodig heeft, in één map. Bewerk of commit alleen **dit kopietje** niet — de echte site staat in de project-root.

## Inhoud

| Bestand | Wat het is |
|---|---|
| `index.html` | De volledige site (home, puzzels, race, duel, daily archive) |
| `css/styles.css` | Alle styling |
| `js/app.js` | Alle logica (auth, puzzels, race, duel via Supabase realtime) |
| `netto_frontend_puzzles.js` | Puzzeldata: 200 library + 88 race + 28 daily puzzels |
| `puzzles_embedded.js` | Oude puzzeldata (wordt nog geladen door index.html) |

Externe afhankelijkheden (alleen internet nodig, geen installatie): Google Fonts en de Supabase JS SDK via CDN.

## Starten

Zit in deze map en start een statische server, bijv.:

```bash
cd website
python -m http.server 5500
```

Open daarna <http://localhost:5500> in de browser. (Andere poort mag ook, bijv. 8000.)

## Wat je kunt testen

1. **Solo Puzzel Race** — Puzzel Race → Start race: 5 minuten, easy → moeilijk, ✓/✗-balk, eindscore + review.
2. **Duel (1v1)** — log in met twee accounts (twee apparaten of browsers), één speler "Maak duel", de ander join't met de room-code, host start.
3. **Puzzels-tab** — alle 200 puzzels direct speelbaar, geen unlocks.
4. **Daily Archive** — 28 genummerde puzzels.

## Bekende testactie

Je eigen race-record staat in `localStorage` onder sleutel `netto_race_best`. Resetten via de console:

```js
localStorage.removeItem('netto_race_best')
```
