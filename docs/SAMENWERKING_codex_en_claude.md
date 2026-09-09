# Samenwerking Codex ↔ Claude

Twee agents werken tegelijk in deze repo, zonder dat de eigenaar erbij is. Dit
bestand legt vast wie waar zit en hoe we elkaar bereiken.

## Wie doet wat

De verdeling is gaandeweg omgedraaid en werkt zo beter:

**Codex** — frontend. Werkgebied: `index.html`, `admin.html`, `js/**`, `css/**`.
Wie de frontend aanraakt, werkt ook `website/**` bij: dat is een kopie die
byte voor byte gelijk moet blijven, anders bereikt de wijziging geen speler.

**Claude** — data en generatoren. Werkgebied: `vragen/**`, `puzzels/**`,
`tools/**`, `fotos/**`, `supabase/**` en de gegenereerde bestanden in `data/**`.

Vaste volgorde bij reparaties: **eerst de vragen, dan de puzzels.** Nooit in één
beweging allebei, want dan is niet meer na te gaan waar een fout vandaan komt.

Kom je iets tegen buiten je eigen gebied, wijzig het dan niet zelf maar meld het
(zie hieronder). Dat is geen formaliteit: we hebben vanavond al een keer
gemerkt dat gelijktijdig schrijven in hetzelfde bestand werk stil overschrijft,
omdat git pas beschermt zodra er gecommit is.

## Hoe we elkaar bereiken

Schrijf een bestand in de repo-root; de ander leest het bij zijn volgende ronde.

- Codex → Claude: `NOTITIE_van_codex.md`
- Claude → Codex: `NOTITIE_van_claude.md`

Zet er de datum en tijd bij, en verwijder je eigen notitie zodra hij verwerkt
is. Kort en concreet: wat is er veranderd, wat moet de ander weten, wat is er
eventueel nodig.

## Vaste afspraken

- **Committen mag, en vaak.** Zolang werk niet gecommit is, kan de ander het
  overschrijven zonder dat git waarschuwt.
- **Stage alleen je eigen bestanden.** Gebruik geen `git add -A` of `git add .`;
  er staan bijna altijd wijzigingen van de ander of van de eigenaar open.
- **`vragen/1000+ vragen netjes gecategoriseerd.xlsx` is van de eigenaar.** Daar
  zit handmatig factcheckwerk in. Niet committen, niet overschrijven.
- Na het regenereren van frontend-data: `python tools/sync_website.py` draaien.
  Dat script zelf niet wijzigen.

## Stand van zaken (6 september)

De backend werkte tot vandaag helemaal niet: op vrijwel alle tabellen ontbrak de
table-grant, waardoor elke RLS-policy inert was. Dat is nu hersteld, samen met
een reeks bijbehorende fouten (uuid versus bigint bij inzendingen, een
operator-constraint die alleen ASCII toestond, een upsert met een spatie in het
onConflict-doel, en een sync die stil niets deed omdat de supabase-library met
defer laadt).

Nog niet gedraaid door de eigenaar: `supabase/backfill_dailies.sql`. Die zet de
35 bestaande dailies in de database en trekt de operator-constraint recht.

**Voor Codex relevant:** die backfill legt per daily vast uit welke
library-puzzel hij kwam (`source_library_id`). Verander je de library-indeling,
laat dan in `NOTITIE_van_codex.md` weten of bestaande `library-XXX`-id's van
betekenis veranderen — dan moet de backfill opnieuw gegenereerd worden voordat
de eigenaar hem draait.
