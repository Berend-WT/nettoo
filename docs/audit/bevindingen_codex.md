# Bevindingen — Codex (frontend)

Alleen Codex schrijft in dit bestand. Claude leest mee en reageert in
`bevindingen_claude.md`. Afspraken: `AUDIT.md`.

Nummering `X-###`, oplopend, nooit hergebruikt.

Vorm per bevinding:

```
### X-001 · hoog|middel|laag · bestand:regel · open|bezig|opgelost <commit>|vervalt <reden>
Wat er niet klopt, in één of twee zinnen.
Zo te zien: hoe roep je het op.
→ andere baan (Claude)     <- alleen als het buiten de frontend ligt
```

---

## Open

### X-001 · middel · js/submissions.js:7 en js/library.js:230 · bezig
Uitgelogd opende Vraag insturen het hele formulier en de ranglijst eerst een
tussenpagina, terwijl de afgesproken ingangen direct naar inloggen moeten gaan.
Zo te zien: zonder sessie via het menu Vraag insturen of Leaderboard openen.
Reparatie staat lokaal: beide functies stoppen na openAuthModal() voor gasten.
Browsercontrole: beide ingangen openen nu het inlogformulier; geen account aangemaakt.
Nog geen commit: de verplichte puzzelcontrole is rood, zie X-003.

### X-002 · middel · js/race.js:492 · bezig
De race riep de gedeelde vraagdetailhelper niet aan. Eenheden ontbraken en alle
drie invoervelden hadden voor schermlezers alleen de naam Your estimate.
Zo te zien: uitgelogd Solo-race starten; vergelijk de velden met een Daily.
Reparatie staat lokaal: werkVraagDetailsBij() na opbouw van de drie kaarten.
Hercontrole in de browser moet nog: browserverbinding viel uit. Geen commit.

### X-003 · middel · tools/controleer_puzzels.py · open
De harde commitpoort is rood: 22 daily/bibliotheekpuzzels en 17 racepuzzels
hebben meer dan twee fotovragen. Dit bevestigt C-002, geen nieuwe datavariant.
Zo te zien: python tools/controleer_puzzels.py meldt ER ZIJN FOUTEN.
Geen generator, puzzel of controleregel gewijzigd. Geen commit zolang deze poort rood is.
→ andere baan (Claude)

### X-004 · middel · js/race.js:116 en js/race.js:165 · open
Een verbroken lobbyverbinding is niet te onderscheiden van geen open spellen.
ensureRaceLobby() keert stil terug zonder client; CHANNEL_ERROR/TIMED_OUT
zetten de kanaalstatus terug maar tonen geen fout. renderOpenGames() toont bij
een lege lijst altijd Nog geen open games. Maak de eerste.
Zo te zien: laad de online-race met niet beschikbare Supabase-client, of laat
het presence-kanaal een time-out geven en vernieuw de lijst.
Codepad gecontroleerd; netwerkfout nog niet geïnjecteerd in de browser.

### X-005 · middel · index.html:934 · open
Labels voor authUsername, authEmail en authPassword missen een for-koppeling.
De browserboom noemt de e-mailinvoer daardoor you@example.com en het wachtwoord
alleen naar de placeholder. De registratie- en vergeten-wachtwoordacties zijn
anchors zonder href en zonder toetsenbordrol.
Zo te zien: open Inloggen, inspecteer de toegankelijke veldnamen en loop met Tab
door het formulier. Veldnamen in browserboom bevestigd; volledige Tab-doorloop
nog uit te voeren. Focusbeheer van de modal eveneens nog nalopen.

### X-006 · middel · js/library.js:127 en js/library.js:132 · open
Een ontbrekende geselecteerde puzzel keert stil terug uit de renderer; er wordt
geen melding getoond en een eerder weergegeven puzzel kan blijven staan.
Zo te zien: een lege geselecteerde moeilijkheid/cataloguslijst of een index
buiten de actuele lijst doorgeven en de puzzelweergave openen.
Codepad vastgesteld; lege-datafixture nog niet in de browser getest.

## Doorloop en keuzes — 10 september 2026

- Afspraken gelezen: deze opdracht, docs/audit/AUDIT.md en
  docs/SAMENWERKING_codex_en_claude.md; ook C-000 t/m C-005 gelezen.
- C-001 betreft nog een open hoge bevinding. Een ontbrekende SQL-regel in de
  repo bewijst niet de actuele dashboardstatus; die live controle laat ik bij
  Claude/eigenaar. Deze audit is dus niet afgerond.
- Daily en Breinkraker 1 openen uitgelogd met gelabelde invoervelden en eenheden.
  Solo-race start en toont timer en vragen zonder account.
- Duel aanmaken opent uitgelogd het inlogformulier vóór een room wordt gemaakt.
  Er is geen account gemaakt, geen inzending verstuurd en geen score ingeleverd.
- Volledige eind-tot-eindruns van alle vijf modi zijn nog niet afgevinkt.
  Catalogus en gewone puzzels moeten deze ronde nog in de browser worden getest.
- Zoekactie naar premium/Premium in index.html, js/ en css/ geeft geen treffers.
  Dit is alleen de naamcontrole, niet een bewijs dat alle ongebruikte code weg is.
- Op 375px de lichte inlogmodal bekeken: formulier past binnen de smalle kolom.
  Daarna liep de browserverbinding vast (ook een reset van de viewport mislukte).
  Donker, volledige smalle doorloop en toetsenbordbediening blijven open.
  De tijdelijke viewport kan nog op 375x812 staan.
- Foutgevallen zijn deels codeonderzoek, geen geslaagde offline-browsertest.
- De eerder gevraagde contrastfix van All puzzles zat bij de start al in de
  schone werkboom; daarvoor in deze audit geen nieuwe wijziging gemaakt.
- Geen bestanden in Claude's werkgebied gewijzigd. De frontendreparaties
  blijven ongecommit totdat alle afgesproken poorten groen zijn.

---

## Afgehandeld

_(nog niets)_
