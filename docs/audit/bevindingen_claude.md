# Bevindingen — Claude (data, generatoren, backend)

Alleen Claude schrijft in dit bestand. Codex leest mee en reageert in
`bevindingen_codex.md`. Afspraken: `AUDIT.md`.

Nummering `C-###`, oplopend, nooit hergebruikt.

---

## Open

### C-008 · hoog (te bevestigen) · Supabase (puzzles_public) · open
Er staat een view `puzzles_public` in de databank met SELECT voor `anon`. Hij
komt in geen enkel bestand van deze repo voor, en hij stond niet in het
RLS-rapport omdat dat op gewone tabellen filterde.

Bij een view is dit beslissend: **een view draait standaard met de rechten van
zijn eigenaar, niet van de lezer.** De row level security op `puzzles` geldt dan
niet voor wie de view opvraagt. Alleen met `security_invoker = true` wordt de
RLS van de lezer toegepast.

Leest deze view uit `puzzles` zonder filter op status of datum, dan kan iedere
bezoeker de ingeplande dagpuzzels ophalen — de vragen én de antwoorden van
morgen. Bij een schatspel is dat het hele spel.

Zo te zien: `supabase/toon_views.sql`. Dat geeft de definitie, de
security_invoker-instelling, en wat een uitgelogde bezoeker echt terugkrijgt.

Nog niet bevestigd: de uitvoer is er nog niet. Kan ook onschuldig zijn — een
view die alleen gepubliceerde puzzels toont is precies wat de frontend nodig
heeft.

### C-006 · middel · Supabase (policies) · open
Acht policies staan live die uit geen enkel SQL-bestand in deze repo komen; ze
zijn ooit via het dashboard gemaakt en wat ze toestaan weet niemand meer.

  admin_users 1 van 2 · library_puzzles 1 van 1 · puzzles 1 van 2 ·
  question_submissions 3 van 7 · scores 2 van 2

Dat is niet los te zien van hoe Postgres policies combineert: **permissive
policies worden met OR samengevoegd.** Eén policy die `using (true)` zegt maakt
elke zorgvuldige policy ernaast betekenisloos, en in een telling zie je dat
verschil niet — twee is twee. Op `scores` en `library_puzzles` heeft ook `anon`
SELECT, dus daar telt het voor iedere bezoeker.

Zo te zien: `supabase/toon_policies.sql`, deel 1. Dat zet alles-toestaan en
alles-voor-anon bovenaan.

Nog niet beoordeeld: de uitvoer van dat script is er nog niet.

### C-007 · laag · Supabase (grants) · open
Op elke tabel staan TRUNCATE, REFERENCES en TRIGGER voor zowel `anon` als
`authenticated`. Dat komt uit de standaard-grant waarmee een Supabase-project
begint, niet uit onze eigen SQL.

Dit is de enige categorie die row level security níét afdekt: policies werken
per rij, TRUNCATE werkt op de hele tabel en gaat er langs. Een policy die
"alleen je eigen rijen" zegt houdt een TRUNCATE niet tegen.

Praktisch risico nu: klein. PostgREST, waar de anon key op uitkomt, heeft geen
route die TRUNCATE uitvoert — er is geen verzoek dat je kunt sturen. Het is een
recht dat niemand nodig heeft en dat RLS niet dekt, en dat is genoeg om het weg
te halen.

Zo te zien: `supabase/toon_policies.sql`, deel 3.

Oplossing staat in datzelfde bestand, deel 2, bewust uitgecommentarieerd: niet
tegen deze databank uitgeprobeerd.

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

### C-001 · hoog · supabase/fix_rls_plays.sql · opgelost (eigenaar draaide controleer_rls.sql, 10 sept)
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

Opgelost met `supabase/controleer_rls.sql`: RLS staat nu aan op alle tabellen die
hem horen te hebben, `admin_users` is dichtgezet tot je eigen rij, en het script
eindigt met een rapport per tabel zodat dit niet nog eens op een aanname rust.

Nog te doen: het rapport van die run is niet bekeken. Staat er ergens
`rls_aan = false` met `policies > 0`, dan is die tabel nog open. Vraag de
eigenaar om de uitvoer, of draai het script nog eens — het is idempotent.

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
