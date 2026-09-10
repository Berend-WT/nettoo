# Opdracht voor Codex — frontend nalopen

Plak dit als eerste bericht in een nieuwe Codex-sessie in deze repo.

Aanbevolen: **GPT-5 Codex, reasoning effort high.** Het werk is lezen en
beoordelen, niet veel typen; daar is denktijd meer waard dan snelheid.

---

Je werkt in de Netto-repo, samen met Claude. Lees eerst deze drie bestanden, in
deze volgorde:

1. `docs/audit/AUDIT.md` — de afspraken. Werkgebieden, hoe je een bevinding
   opschrijft, en de poort waar je doorheen moet voordat je commit.
2. `docs/audit/bevindingen_claude.md` — wat Claude tot nu toe gevonden heeft.
   Eén daarvan (C-001) raakt de backend en ligt bij de eigenaar.
3. `docs/SAMENWERKING_codex_en_claude.md` — de bestaande werkverdeling.

Jouw gebied is de frontend: `index.html`, `admin.html`, `js/**`, `css/**`, en de
kopie in `website/**` die daarbij hoort. Blijf daarbinnen. Kom je iets tegen in
de data, de generatoren of de backend, repareer het dan niet maar schrijf het op
met `→ andere baan (Claude)`.

Schrijf je bevindingen uitsluitend in `docs/audit/bevindingen_codex.md`. Niet in
dat van Claude, ook niet om iets te verbeteren.

## Wat er net veranderd is, zodat je niet schrikt

- **Premium bestaat niet meer.** De betaalmuur voor de Library is weg en alles
  wat `premium` heette is hernoemd naar `catalogus` — 182 plekken, mechanisch.
  Dat is precies het soort verandering waar iets van blijft liggen. Zoek naar
  ongebruikte functies, css-regels zonder element, en vertaalsleutels voor tekst
  die niet meer bestaat.
- **Spelen hoeft geen account.** Dagpuzzel, puzzels, catalogus, breinkrakers en
  solo-race werken uitgelogd. Het leaderboard, het online duel en het insturen
  van vragen sturen juist wél naar het inlogscherm.
- **Registreren is versoepeld**: zes tekens, geen e-mailbevestiging, en de
  client-side registratieteller is eruit.
- **De site gaat naar GitHub Pages**, op een subpad (`/nettoo/`). Alle paden
  moeten relatief blijven.

## Waar ik je vooral op wil hebben

In volgorde. Werk van boven naar beneden.

1. **Uitgelogd.** Loop elke modus na zonder sessie. Werkt spelen echt overal, en
   sturen de drie afgeschermde dingen echt naar het inlogscherm?
2. **Resten van premium.** Zie hierboven.
3. **Licht en donker, en 375 pixels breed.** Let op contrast. Er zat net een
   knop die zijn eigen oppervlak meebracht en daardoor onzichtbaar werd zodra de
   achtergrond eronder veranderde — die fout kan er vaker in zitten.
4. **Foutgevallen.** Geen netwerk, Supabase plat, lege lijst, puzzel laadt niet.
   Krijgt de speler uitleg, of een leeg vlak?
5. **Toegankelijkheid.** Toetsenbord, focusringen, labels, `aria-live` waar iets
   verandert zonder klik.

## Twee dingen die je niet moet doen

- **Geen accounts aanmaken**, ook niet om te testen. De eigenaar doet dat.
- **Geen `git add -A`.** Stage alleen je eigen bestanden; er staat bijna altijd
  werk van iemand anders open.

## Voordat je commit

```bash
python tools/controleer_puzzels.py
python tools/sync_website.py --check
```

Let op: `controleer_puzzels.py` staat op dit moment op rood door C-002 (39
puzzels met drie fotovragen). Dat is bekend en ligt bij Claude. Alles wat er
verder bij komt is wel van jou.

En open de site echt in een browser. Niet "dit kan niet stuk" — openen en
kijken.
