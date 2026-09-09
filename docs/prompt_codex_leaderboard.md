# Opdracht: ranglijst van eerdere dagen, en eenheden bij Breinkrakers

Twee klussen, allebei frontend. De eerste is het echte werk.

## 1. De ranglijst kan alleen vandaag laten zien

`js/core.js` regel ~2499 roept de ranglijst op:

    await supabaseClient.rpc('leaderboard_dag', { p_datum: TODAY_STR })

`TODAY_STR` staat daar hard. De database-functie zelf kan het wel al — kijk in
`supabase/fix_leaderboard_en_registratie.sql`: `leaderboard_dag(p_datum date)`
neemt elke datum aan en geeft de vijftig beste van die dag. Er hoeft dus niets
aan de database te gebeuren.

**Wat het moet worden:** in de ranglijst kun je terug naar eerdere dagen.

- Vorige en volgende dag, met de dagpuzzel van die datum erbij genoemd
  (nummer en datum), zodat je weet waar je naar kijkt.
- Niet verder terug dan de eerste dagpuzzel, en niet vooruit voorbij vandaag.
- Een dag zonder inzendingen geeft geen fout maar een lege lijst met uitleg.
  Dat gaat gebeuren: voor de meeste oude datums staat er nog niets in
  `user_plays`, dus die lege toestand is de normale toestand en geen randgeval.
  Test hem als eerste.
- De streak-ranglijst blijft zoals hij is. Die gaat over een reeks dagen en
  heeft geen datumkeuze nodig.
- Welke dag je bekijkt hoort in de knop of kop te staan, niet alleen in de
  navigatie. Iemand die het scherm opent moet zonder klikken zien of hij naar
  vandaag kijkt.

De datums van de dagpuzzels staan in `data/netto_frontend_puzzles.js` onder
`daily`, elk met een `date`. Neem die als bereik; verzin er geen kalender bij.

## 2. Breinkrakers missen de eenheid naast het invoerveld

Bij de dagpuzzel, de bibliotheek en de race staat rechts in het invoerveld de
eenheid: *liften*, *verdiepingen*, *km*, *× 1.000 inwoners*. Bij Breinkrakers
niet. Dat is geen ontwerpkeuze, het is vergeten.

De functie staat er al: `eenheidUit(vraag)` in `js/core.js`, en
`werkVraagDetailsBij()` laat zien hoe het label wordt opgehangen (het zet ook
`--eenheid-ruimte` en `aria-describedby`). Breinkrakers bouwen hun vragen in
`showBreinkrakersPuzzle()` in `js/puzzle-modes.js`, met vier vragen in plaats
van drie.

De eenheid is tweetalig: `eenheidUit` kijkt zelf naar `NettoI18n.language` en
leidt hem af uit de vertaalde zin. Je hoeft daar niets voor te doen.

## Denk aan

- **`website/` is een byte-voor-byte kopie.** Wijzig alleen de projectroot en
  draai daarna `python tools/sync_website.py`. Controleer met
  `python tools/sync_website.py --check`. Zonder die stap bereikt je werk geen
  enkele speler.
- **Verhoog `?v=` van elk bestand dat je wijzigt, in beide index.html.** Doe je
  dat niet, dan blijft de oude versie in de browsercache staan.
- De vorige ronde ging hierop mis: de wijziging stond wel in `index.html` maar
  niet in `website/index.html`.
