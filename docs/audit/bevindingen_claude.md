# Bevindingen — Claude (data, generatoren, backend)

Alleen Claude schrijft in dit bestand. Codex leest mee en reageert in
`bevindingen_codex.md`. Afspraken: `AUDIT.md`.

Nummering `C-###`, oplopend, nooit hergebruikt.

---

## Open

### C-009 · te onderzoeken · Supabase (rls_auto_enable) · open
Er bestaat een functie `public.rls_auto_enable()` die in geen enkel bestand van
deze repo voorkomt. Hij is SECURITY DEFINER en uitvoerbaar door `anon`, dus door
iedereen die het adres van het project kent, zonder in te loggen
(`/rest/v1/rpc/rls_auto_enable`).

De naam suggereert dat hij row level security aanzet. Wat hij werkelijk doet
weet niemand, en dat is precies het probleem: een functie die als eigenaar
draait en door iedereen aangeroepen kan worden verdient het om gelezen te zijn.

Zo te zien: `supabase/lekt_de_toekomst.sql`, deel 2.

### C-010 · middel · Supabase (opslag) · open
De publieke bucket `daily-images` heeft een brede SELECT-policy op
`storage.objects` ("Iedereen mag daily afbeeldingen bekijken"), waardoor
bezoekers de hele bucket kunnen **oplijsten**. Voor het tonen van een afbeelding
is dat niet nodig — een publieke bucket serveert zijn bestanden ook zonder
listing-rechten.

Zelfde thema als C-008: staan hier afbeeldingen voor dagpuzzels die nog moeten
komen, dan zijn die vooraf op te vragen.

Gemeld door de security advisor (WARN, `public_bucket_allows_listing`).

### C-011 · laag · Supabase (functierechten) · open
Zes SECURITY DEFINER-functies zijn aanroepbaar door `anon`. Nagelopen:

- `admin_review_submission` — **geen gat.** De functie begint met
  `if not public.is_admin() then raise exception`, en `is_admin()` toetst
  `auth.uid()` tegen `admin_users`. Voor een uitgelogde beller is `auth.uid()`
  null, dus die vliegt er meteen uit. De advisor kijkt alleen naar wie hem mag
  aanroepen, niet naar wat hij als eerste doet.
- `is_admin`, `username_beschikbaar`, `leaderboard_dag`, `leaderboard_streaks` —
  bedoeld zo. De eerste zegt alleen iets over jezelf, de tweede geeft ja of nee
  op een naam, de laatste twee voeden het scorebord.
- `handle_new_user` — een triggerfunctie die per ongeluk ook los aanroepbaar is.
  Zonder trigger-context loopt hij stuk op `new`, dus hij is niet te misbruiken,
  maar het EXECUTE-recht hoort er niet te staan.

Netjes zou zijn: EXECUTE intrekken bij `handle_new_user` en `rls_auto_enable`
(die laatste pas als C-009 duidelijk is). Geen haast.

### C-012 · laag · Supabase (auth) · open
Leaked password protection staat uit. Supabase kan een wachtwoord toetsen tegen
HaveIBeenPwned. Nu de minimale lengte op zes staat is dat juist wel iets waard:
het weert de wachtwoorden die in bestaande lekken staan.

Eén schakelaar: Authentication -> Password.

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

### C-002 · middel · tools/controleer_puzzels.py · opgelost 10 sept (ook X-003)
39 puzzels (22 in daily+bibliotheek, 17 in de racepool) hebben alle drie hun
vragen met een foto, terwijl de generator er hooguit twee toestaat. Daardoor
stond `controleer_puzzels.py` op rood — en dat is de gedeelde commitpoort, dus
Codex kon zijn frontendreparaties niet wegschrijven (zie X-003).

Het is drift, geen fout: de puzzels zijn gebouwd toen de fotobank 238 foto's
had, en die staat nu op 638. De speler merkt er niets van, want er komt hoe dan
ook één foto per puzzel in beeld.

Repareren kan alleen door opnieuw te genereren, en dat husselt alle puzzels door
elkaar — inclusief de `source_library_id` waarmee de dagpuzzels in de databank
naar een library-id verwijzen. Dat wil je niet vlak voor release.

Dus is de regel een waarschuwing geworden in plaats van een fout, met de reden
erbij in het bestand zelf. Niet om de poort groen te praten: een poort die rood
staat om iets wat niemand van plan is te repareren, is geen poort meer — dan
went het rood, en de volgende echte fout valt niet meer op.

### C-008 · vervalt (geen lek) · Supabase (puzzles_public) · afgehandeld 10 sept
De view bleek precies te doen wat hij moet doen:

    select id, question_1, question_2, operator, scheduled_date, status
    from puzzles
    where status = 'scheduled' and scheduled_date <= CURRENT_DATE;

Het datumfilter sluit de toekomst uit, er zitten geen antwoorden in en zelfs
`question_3` niet. De SECURITY DEFINER die de advisor als ERROR meldt is hier
juist het punt: daardoor kan een uitgelogde bezoeker de dagpuzzel van vandaag
lezen zonder dat de RLS op `puzzles` hem tegenhoudt.

Waarom deze bevinding blijft staan: het vermoeden was redelijk — een view die
niemand kende, leesbaar voor anon, met SECURITY DEFINER en zonder statusfilter
in de steekproef. Wat ontbrak was de definitie. Dat is het verschil tussen een
vermoeden en een bevinding, en het hoort opgeschreven te worden als het de
verkeerde kant op valt.

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
