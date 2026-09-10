# Netto — gezamenlijke doorloop door Codex en Claude

Twee agents lopen de hele boel na: vragen, puzzels, foto's, frontend, backend.
Dit bestand is de afspraak. Lees het voordat je begint, ook als je denkt dat je
het al weet — het verandert.

Dit staat naast `docs/SAMENWERKING_codex_en_claude.md`. Dat bestand gaat over
samen wérken (wie raakt welk bestand aan). Dit bestand gaat over samen
*nalopen*: wat we zoeken, hoe we het opschrijven, en wanneer iets af is.

## Waarom dit bestaat

Eén agent leest zijn eigen werk goed. Twee agents lezen elkaars werk beter. De
aanleiding is concreet: er stonden veertig afgekeurde foto's uit
`data/netto_fotos.js` nog steeds in het spel, omdat elke puzzel zijn foto óók
zelf meedraagt in een `photo`-veld. Eén laag gecontroleerd, de tweede niet. Dat
soort fout vindt de schrijver zelf zelden.

En: `tools/controleer_puzzels.py` stond op rood terwijl niemand het merkte.
Daarom staat hij hieronder als harde poort.

## De ene beperking waar we omheen werken

Codex en Claude hebben **geen kanaal naar elkaar.** De eigenaar geeft de ene
door wat de andere schreef. Dus:

- Stel nooit een vraag die eerst beantwoord moet worden voordat jij verder kunt.
  Kies zelf, schrijf op wát je koos en waaróm, en ga door.
- Ga ervan uit dat de ander je bevinding pas over uren leest.
- Schrijf alsof de lezer niets van je sessie weet. Geen "zoals ik eerder zei".

## Werkgebieden

Ongewijzigd, want deze verdeling heeft al een keer voorkomen dat we elkaars werk
overschreven:

| | Codex | Claude |
|---|---|---|
| Bezit | `index.html`, `admin.html`, `js/**`, `css/**` | `vragen/**`, `puzzels/**`, `tools/**`, `fotos/**`, `supabase/**`, `data/**` |
| Mag lezen | alles | alles |
| Mag wijzigen | alleen eigen gebied | alleen eigen gebied |

Zie je iets buiten je gebied: **niet zelf repareren.** Schrijf het op als
bevinding met `→ andere baan`. De eigenaar van dat gebied pakt het op.

### Het enige bestand dat we delen

`index.html` draagt de `?v=`-nummers van álle bestanden, ook die van Claude.
Afspraak: je verhoogt alleen de regel van een bestand dat jij hebt gewijzigd.
Dat zijn losse regels, dus git voegt dat probleemloos samen. Verhoog nooit
"voor de zekerheid" alles.

## Wat we zoeken

Per baan, in volgorde van belang. Werk van boven naar beneden; een baan is niet
af omdat je bij het leukste onderdeel bent aangekomen.

### Claude — data en backend

1. **Vragen** (1409). Klopt het antwoord met de bron? Is de vraag eenduidig te
   lezen? Staat er een eenheid die niet bij het getal past? Klopt de Engelse
   vertaling qua betekenis, niet alleen qua woorden?
2. **Puzzels** (547). `tools/controleer_puzzels.py` moet groen. Nu meldt hij nog
   39 puzzels met drie fotovragen — drift doordat de fotobank na het genereren
   van 238 naar 638 groeide.
3. **Foto's** (638 in het spel, 378 wachtend, 182 zonder). Past het beeld bij de
   vraag? Geeft het het antwoord weg? Klopt de licentie en de maker?
4. **Backend.** Heeft elke tabel zowel een grant als een policy? Wat gebeurt er
   als Supabase niet bereikbaar is? Kan een speler bij andermans gegevens?

### Codex — frontend

1. **Werkt het uitgelogd?** Spelen hoeft geen account. Loop elke modus na zonder
   sessie: dagpuzzel, puzzels, catalogus, breinkrakers, solo-race. Het
   leaderboard, het duel en het insturen van vragen horen juist wél naar het
   inlogscherm te sturen.
2. **Dode code na het schrappen van premium.** De betaalmuur is weg en alles wat
   `premium` heette is hernoemd naar `catalogus`. Zoek wat er is blijven staan:
   ongebruikte functies, css-regels zonder element, vertaalsleutels voor tekst
   die niet meer bestaat.
3. **Beide thema's, en smal.** Licht en donker, en 375 pixels breed. Let op
   contrast: een knop die zijn eigen oppervlak meebrengt verdwijnt zodra de
   achtergrond eronder verandert.
4. **Foutgevallen.** Geen netwerk, Supabase plat, lege lijst, een puzzel die
   niet laadt. Krijgt de speler uitleg of een leeg vlak?
5. **Toegankelijkheid.** Toetsenbordbediening, focusringen, labels, `aria-live`
   waar iets verandert zonder klik.

## Hoe je een bevinding opschrijft

Elke agent schrijft **uitsluitend in zijn eigen bestand**:

- Claude: `docs/audit/bevindingen_claude.md`
- Codex: `docs/audit/bevindingen_codex.md`

Beiden lezen allebei de bestanden. Zo kan er nooit een schrijfconflict ontstaan.

Vorm — kort, maar volledig genoeg om zonder navraag te repareren:

```
### C-014 · middel · js/core.js:1571 · open
De dagpuzzel valt terug op de sfeerfoto als het photo-veld leeg is.
Zo te zien: speel een daily waarvan geen van de drie vragen in NETTO_FOTOS
staat; er verschijnt een pizza bij een vraag over Antarctica.
→ andere baan (Codex)
```

- **Nummer**: `C-###` voor Claude, `X-###` voor Codex. Nooit hergebruiken.
- **Zwaarte**: `hoog` (speler ziet iets fouts of kan niet verder) · `middel`
  (klopt niet, maar valt te overzien) · `laag` (netheid).
- **Plek**: bestand en regel, of het gegevensbestand plus de sleutel.
- **Zo te zien**: hoe roep je het op. Zonder dit is een bevinding een mening.
- **Status**: `open` · `bezig` · `opgelost <commit>` · `vervalt <reden>`.

Verander de status in je eigen bestand als je iets oplost. Haal een bevinding
nooit weg: een opgeloste bevinding met een commit erachter is het bewijs dat het
nagelopen is.

**Oneens met een bevinding van de ander?** Schrijf dat in jouw bestand met een
verwijzing (`over X-007: ...`) en laat de zijne staan. Niet in zijn bestand
schrijven, ook niet "even snel".

## Poort voor het committen

Alle drie moeten slagen. Geen uitzonderingen, ook niet bij een kleine wijziging.

```bash
python tools/controleer_puzzels.py
python tools/sync_website.py --check
```

En: open de site en kijk ernaar. Niet "dit kan niet stuk" — openen en kijken.
`.claude/launch.json` start hem, of `python -m http.server 8765`.

Verder:

- **Stage alleen je eigen bestanden.** Geen `git add -A`, geen `git add .`.
- **Commit vaak.** Ongecommit werk kan de ander overschrijven zonder dat git
  waarschuwt.
- **Zet in de commit-tekst wat je hebt nagelopen**, niet alleen wat je hebt
  veranderd. "Nagelopen in de browser, licht en donker, op 375 breed" is voor de
  ander het verschil tussen vertrouwen en overdoen.

## Wat níét van ons is

- `vragen/1000+ vragen netjes gecategoriseerd.xlsx` — daar zit handmatig
  factcheckwerk van de eigenaar in. Niet committen, niet overschrijven.
- Instellingen in het Supabase-dashboard en in GitHub. Wij schrijven op wat er
  moet gebeuren; de eigenaar klikt.
- Accounts aanmaken. Ook niet "even eentje om te testen".

## Wanneer is dit af

Als beide bevindingenbestanden geen `open` van zwaarte `hoog` meer bevatten en
de poort hierboven groen is. `middel` en `laag` mogen blijven staan; die zijn
dan de lijst voor daarna.
