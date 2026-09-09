# Opdracht: Engelse vraagteksten van Netto

Netto is tweetalig. De vragen staan in het Nederlands en worden vertaald met een
opzoektabel. Die vertalingen zijn machinaal gemaakt en niet nagelopen. Wat een
Engelse speler nu ziet:

    How many Earths do the Sun fit in volume?
    How many Eurovision Song Festivals won Sweden until 2024?
    How much Grammy won the Australian band AC/DC approximately?

Jouw taak: die zinnen kloppend en natuurlijk Engels maken.

## Wat je krijgt

`docs/vertalingen_engels.tsv` — 985 regels, tab-gescheiden, drie kolommen:

| kolom | inhoud |
|---|---|
| `vlag` | leeg, of `GEEN` (geen vertaling), `NL?` (Nederlandse woorden in de Engelse zin), `GEEN-?` (geen vraagteken) |
| `nederlands` | de vraag zoals hij in het spel staat — **exact overnemen, nooit wijzigen** |
| `engels` | de huidige vertaling |

Dit zijn alleen de vragen die daadwerkelijk in een puzzel zitten. De rest van de
catalogus (knoppen, schermteksten) laat je met rust.

**188 regels hebben helemaal geen vertaling** (`GEEN`). Die zijn het ergst: daar
staat nu een Nederlandse zin in het Engelse spel. Begin daar.

## Wat je oplevert

Eén bestand: `docs/vertalingen_engels_nieuw.tsv`, twee kolommen, tab-gescheiden:

    nederlands<TAB>engels

**Alleen de regels die je verandert.** Is een vertaling al goed, laat hem dan
weg — dat scheelt jou uitvoer en mij ruis. De Nederlandse kolom is de sleutel en
moet teken voor teken gelijk zijn aan de invoer, inclusief accenten en
leestekens; anders komt de verbetering nergens aan.

## Waar het op aankomt

1. **De vraag moet hetzelfde vragen.** Klopt de Nederlandse vraag niet met de
   Engelse, dan wint het Nederlands. Vertaal, verbeter niet.
2. **Het getal blijft het antwoord.** "Hoeveel duizend inwoners" is
   "How many thousand inhabitants" — niet "How many inhabitants".
3. **Begin met `How many`, `How much`, `In what year` of `What percentage`.**
   Het spel leidt de eenheid naast het invoerveld af uit die opening. Een zin
   die met iets anders begint, verliest zijn eenheid.
4. **Zet het getelde zelfstandig naamwoord vooraan in de naamwoordgroep.**
   "How many African countries border…" is goed. Het spel neemt het laatste
   meervoud van de groep als eenheid.
5. **Namen blijven staan.** Elfstedentocht, Rijksmuseum, Zuiderzee.
   Vertaal ze niet naar "Eleven Cities Tour".
6. **Peiljaren blijven staan.** "(stand 2026)" wordt "(as of 2026)".
7. Brits of Amerikaans Engels mag, als je maar één van beide kiest en
   volhoudt. Het bestaande bestand neigt naar Brits ("metres", "kilometres").

## Wat je niet doet

- `data/netto_translations_en.js` niet aanraken. Dat bestand heeft 2.386
  sleutels en CRLF-regeleindes; één misplaatste komma en de frontend laadt
  zonder foutmelding géén enkele vertaling meer. `tools/verwerk_vertalingen.py`
  zet jouw TSV er veilig in.
- Geen andere bestanden lezen dan de TSV. Alles wat je nodig hebt staat erin.
  De repo verkennen kost tokens en levert je niets.
- De Nederlandse kolom niet verbeteren, ook niet als er een fout in staat. Meld
  die onderaan je bericht en laat de regel verder met rust.

## Klaar?

Meld hoeveel regels je hebt gewijzigd en welke Nederlandse vragen je zelf
verdacht vond. Ik draai daarna `python tools/verwerk_vertalingen.py` en werk het
cachenummer bij.
