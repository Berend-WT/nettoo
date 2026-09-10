# Bevindingen — Claude (data, generatoren, backend)

Alleen Claude schrijft in dit bestand. Codex leest mee en reageert in
`bevindingen_codex.md`. Afspraken: `AUDIT.md`.

Nummering `C-###`, oplopend, nooit hergebruikt.

---

## Open

### C-001 · hoog · supabase/fix_rls_plays.sql · open
Op `library_plays` staat row level security nergens aan, terwijl er wel policies
én een grant op staan. Een policy zonder RLS is geen halve beveiliging maar geen
enkele: Postgres slaat het policy-stelsel dan over en laat de tabelrechten
beslissen, en die staan op `grant select, insert, update ... to authenticated`.
Elke ingelogde speler kan dus de library-voortgang van elke andere speler lezen
en overschrijven.

`fix_rls_plays.sql` opent met de zin "Op beide tabellen staat RLS aan". Dat is
nooit ergens vastgelegd — geen enkel SQL-bestand zet hem aan voor deze tabel. De
aanname zelf is de fout.

Zo te zien: `select relname, relrowsecurity from pg_class where relname =
'library_plays';` Staat er `false`, dan is de tabel open.

Oplossing klaargezet in `supabase/controleer_rls.sql`. Dat bestand zet RLS aan op
alle tabellen die hem horen te hebben en eindigt met een rapport per tabel, zodat
dit niet nog eens op een aanname hoeft te rusten. **De eigenaar moet het draaien.**

### C-002 · middel · data/netto_frontend_puzzles.js, data/netto_race_pool.js · open
39 puzzels (22 in bibliotheek + daily, 17 in de racepool) hebben alle drie hun
vragen met een foto, terwijl de generator er hooguit twee toestaat
(`MAX_FOTOS_PER_PUZZEL`). Daardoor staat `tools/controleer_puzzels.py` op rood.

Dit is drift, geen generatiefout: de puzzels zijn gebouwd toen de fotobank 238
foto's had, en die is daarna naar 638 gegroeid. De speler ziet er niets van —
er komt één foto per puzzel in beeld.

Zo te zien: `python tools/controleer_puzzels.py`, regel "FOUT meer dan twee
fotos".

Opties, geen van beide gratis: opnieuw genereren husselt alle puzzels door
elkaar (en breekt de `source_library_id` van de dailies in de databank), of de
regel wordt verlaagd tot een waarschuwing omdat hij alleen over generatie gaat
en niet over wat de speler ziet. Neig naar het tweede, maar niet vlak voor
release doorvoeren zonder dat de eigenaar meekijkt.

### C-003 · middel · Supabase (dagpuzzels) · open
De dagpuzzels zijn gepland tot 2026-10-09. Daarna heeft het spel geen puzzel van
de dag, en dat is het eerste wat een bezoeker ziet. Ongeveer dertig dagen vanaf
nu.

Zo te zien: `select max(scheduled_date) from public.puzzles where status =
'scheduled';`

Oplossing bestaat al: `tools/plan_dailies.py` plus
`supabase/plan_dailies_vooruit.sql`. Het is een terugkerende handeling, geen
eenmalige — zou een herinnering moeten worden.

### C-004 · laag · vragen/, fotos/ · open
378 vragen hebben een fotokandidaat die op een oordeel wacht, 182 hebben er geen
enkele. Het spel werkt zonder; dit is dekking, geen fout. Staat hier zodat het
niet stilletjes voor "af" doorgaat.

### C-005 · laag · Supabase (auth.users) · open
Tijdens het testen van de wachtwoordvalidatie is er één registratie afgevuurd op
`test@voorbeeld.nl`. Die kwam terug met HTTP 429 (snelheidslimiet) en leverde
geen sessie op, dus vrijwel zeker is er niets aangemaakt. Zeker weten kan alleen
in het dashboard.

Zo te zien: Authentication -> Users, zoek op `voorbeeld.nl`. Staat hij er, weg
ermee.

---

## Afgehandeld

### C-000 · hoog · data/netto_frontend_puzzels.js · opgelost c78f79a
Veertig bij de visuele controle afgekeurde foto's stonden nog in het spel. Ze
waren uit `data/netto_fotos.js` gehaald, maar elke puzzel draagt zijn foto óók
zelf mee in een `photo`-veld, en de frontend leest dat veld eerst. 25 puzzels
toonden nog de afgekeurde foto — onder meer een schaakbord bij "hoeveel
speelvelden heeft een schaakbord".

Opgelost met `tools/herstel_puzzelfotos.py` (het veld loopt weer mee met de
bank) plus `nogInDeBank()` in `js/photo-credits.js` als vangnet.

Waarom dit hier blijft staan: het is de reden dat deze doorloop bestaat. Eén
laag gecontroleerd, de tweede niet, en niets dat waarschuwde.
