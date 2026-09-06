# Briefing voor Codex — puzzelsamenstelling herzien

## Wat er mis is

Een Netto-puzzel bestaat uit drie vragen die samen een som vormen. Op dit moment
komen er regelmatig twee vragen uit dezelfde categorie in één puzzel. Gemeten in
`netto_frontend_puzzles.js`:

- **daily**: 7 van de 35 (20%)
- **library**: 35 van de 200 (18%)

Voorbeelden: `daily-035` heeft `['Taal', 'Geografie', 'Geografie']`,
`library-001` heeft `['Sterrenkunde & ruimte', 'Geografie', 'Sterrenkunde & ruimte']`.

Dat maakt een puzzel eentonig: je wil drie keer een ander soort feit, niet twee
keer aardrijkskunde.

## Opdracht

1. **Harde eis:** binnen één puzzel zijn alle drie de categorieën verschillend.
2. **Kijk breder naar het algoritme.** Puzzels moeten onderling uniek zijn, en
   idealiter ook niet twee keer hetzelfde *onderwerp* bevatten, ook niet als de
   categorie toevallig verschilt (bijvoorbeeld twee vragen over rivieren die als
   "Geografie" en "Records en vergelijkingen" geclassificeerd staan). Beoordeel
   zelf of dat haalbaar is met de beschikbare metadata en stel voor wat er nodig
   zou zijn als het niet kan.
3. Regenereer de puzzelbestanden en draai daarna `python tools/sync_website.py`.

## Waar je moet zijn

- `puzzels/maak_puzzels.py` (855 regels) — de hoofdgenerator, hier zit de
  samenstelling.
- `puzzels/maak_puzzels_race.py`, `puzzels/maak_race_pool.py`,
  `puzzels/maak_breinkrakers.py` — zelfde patroon voor de andere modi.
- `.freebuff/build_rebuilt_frontend.py` — bouwt `netto_frontend_puzzles.js`;
  die *leest* alleen categorieën (`row[3], row[6], row[9]`), stelt niets samen.
- `vragen/1000+ vragen netjes gecategoriseerd.xlsx` — de vragenbank.

## Randvoorwaarden die je niet mag breken

Deze zijn vanavond stuk voor stuk in productie tegengekomen; ze kosten je tijd
als je ze zelf moet ontdekken.

- **Operators zijn typografische Unicode-tekens**, geen ASCII: `×` (U+00D7),
  `÷` (U+00F7), `−` (U+2212) en `+` (U+002B). Dus niet `*`, `/` of `-`. De
  database-constraints en de frontend rekenen hierop.
- **De som moet exact kloppen** en op een geheel getal uitkomen:
  `a1 operator a2 = a3`. De frontend en het adminscherm valideren dit en weigeren
  puzzels waarbij het niet klopt.
- **Bestaande dailies mogen niet verschuiven.** De frontend leidt het
  daily-nummer af uit de datum (nr. 35 = 2026-09-04). Als je datums of volgorde
  van bestaande dailies verandert, breken spelershistorie en streaks. Nieuwe
  puzzels toevoegen mag; bestaande herschikken niet.
- **De datavorm ligt vast.** `window.NETTO_REBUILT_PUZZLES` met `daily`,
  `library` en `reserve`; per puzzel `q1_label`/`q1_answer` t/m
  `q3_label`/`q3_answer`, plus `operator`, `categories`, `difficulty`, `date` en
  `source_library_id`.
- **De vragenbank is vanavond opgeschoond**: 32 duplicaten verwijderd (1542 →
  1510) en categorienamen genormaliseerd. Varianten als `Politiek & recht` en
  `Bouwwerken` bestaan niet meer. Lees dus de huidige xlsx, ga niet uit van oude
  categorienamen.
- Na regenereren **altijd** `python tools/sync_website.py` draaien; anders loopt
  de `website/`-kopie achter.

## Blijf uit deze bestanden

Er wordt parallel aan gewerkt; wijzigingen daar botsen.

```
index.html, admin.html, js/**, css/**, supabase/**, fotos/**, tools/sync_website.py
```

`tools/sync_website.py` mag je wel *draaien*, niet wijzigen.

## Klaar wanneer

- Geen enkele puzzel in `daily`, `library` of `reserve` heeft twee gelijke
  categorieën. Controle:
  `[p for p in rows if len(set(p['categories'])) < len(p['categories'])]` is leeg.
- Alle sommen kloppen nog.
- Bestaande daily-datums en -nummers zijn ongewijzigd.
- `python tools/sync_website.py --check` meldt dat de kopie gelijk is.
- Je beschrijft kort wat je aan het algoritme veranderd hebt en wat er níét
  haalbaar bleek.
