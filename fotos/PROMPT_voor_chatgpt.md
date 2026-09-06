# Prompt voor ChatGPT (Astra, effort: high)

**Model:** GPT-6 Astra. **Effort:** high (niet ultra — het zijn 105 korte oordelen, geen diep redeneerwerk).
**Bijlage:** `daily_vragen_review_input.json`

Plak onderstaande prompt en voeg dat JSON-bestand toe.

---

Je controleert de vragen van Netto, een Nederlands dagelijks schattingsspel. Een puzzel bestaat uit drie vragen met getalsmatige antwoorden die samen een som vormen (a × b = c, of met + − ÷). Spelers schatten de antwoorden; hoe dichter bij het echte getal, hoe beter hun score.

In de bijlage staan 105 vragen als JSON-array. Per vraag: `id`, `nl` (de Nederlandse vraag), `antwoord` (het correcte getal), `en_huidig` (de huidige Engelse vertaling) en `handmatig` (of die vertaling door een mens is nagekeken — bij vrijwel alle staat dit op false).

Beoordeel elke vraag op drie punten.

**1. Vertaalcontrole.** Klopt `en_huidig` inhoudelijk met `nl`? Let vooral op vaktermen: één van deze vertalingen maakte van "naamvallen" (grammatical cases) het woord "names", waardoor het antwoord 15 niet meer bij de Engelse vraag hoorde. Dat is precies de fout die je zoekt. Een vertaling die stroef loopt maar hetzelfde vraagt, is goed genoeg; een vertaling die iets anders vraagt, is fout.

Let er ook op of het antwoord nog logisch is bij de Engelse vraag. Vraagt de Nederlandse versie naar meters en de Engelse naar voet, dan klopt het getal niet meer.

**2. Zoekterm voor een foto.** Geef een Engelse zoekterm van 1–4 woorden waarmee je op Wikimedia Commons een goede sfeerfoto bij deze vraag vindt. Denk aan wat je op de foto zou willen zien: het onderwerp, niet de meeteenheid. Bij "Hoeveel kilo weegt de tong van een blauwe vinvis?" is "blue whale" beter dan "whale tongue weight". Bestaat er geen zinnig beeld bij (abstracte taal-, wiskunde- of percentagevragen), geef dan `null` — een irrelevante foto is slechter dan geen foto.

**3. Hint-risico.** Zou een foto bij deze vraag het antwoord kunnen verklappen? De foto mag laten zien wáár de vraag over gaat, maar niet helpen het getal te schatten. Een piano bij "hoeveel toetsen heeft een piano" is prima — je telt er geen toetsen op. Een foto waarop je het antwoord kunt natellen of aflezen niet. Antwoord met `laag`, `midden` of `hoog`.

Geef uitsluitend JSON terug, een array met exact 105 objecten, in dezelfde volgorde als de invoer:

```json
[
  {
    "id": "1-q1",
    "vertaling_klopt": true,
    "en_correctie": null,
    "toelichting": null,
    "zoekterm": "Battle of Waterloo",
    "hint_risico": "laag"
  }
]
```

Regels voor de uitvoer:
- `vertaling_klopt`: false zodra de Engelse vraag iets anders vraagt dan de Nederlandse, of het antwoord er niet meer bij past.
- `en_correctie`: bij false de verbeterde Engelse vraag, anders `null`.
- `toelichting`: bij false één korte zin over wat er misging, anders `null`.
- `zoekterm`: 1–4 Engelse woorden, of `null`.
- `hint_risico`: `laag`, `midden` of `hoog`.

Geen tekst buiten de JSON.
