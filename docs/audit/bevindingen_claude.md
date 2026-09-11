# Bevindingen — Claude (data, generatoren, backend)

Alleen Claude schrijft in dit bestand. Codex leest mee en reageert in
`bevindingen_codex.md`. Afspraken: `AUDIT.md`.

Nummering `C-###`, oplopend, nooit hergebruikt.

---

## Open

### C-013 · middel · repo is publiek · open — besluit nodig
De repo staat op public, dus alles erin is voor iedereen te downloaden. Dat is
de prijs van gratis GitHub Pages, en voor de code prima. Voor twee bestanden
wil ik het even hardop zeggen:

- `vragen/1000+ vragen netjes gecategoriseerd.xlsx` — jouw handmatige
  factcheckwerk. In de werkafspraken staat dat dit bestand niet achteloos
  gecommit mag worden; het staat er wel in, en nu dus ook publiek.
- `vragen/vragen_review_compleet.xlsx` — de complete vragenbank met alle 1409
  antwoorden en bronnen.

Hoe erg is het werkelijk? Minder dan het klinkt. De antwoorden van de
bibliotheek- en racepuzzels zitten sowieso in `data/netto_frontend_puzzles.js`,
want de browser rekent de score uit en heeft ze dus nodig. En de dagpuzzel van
morgen is niet te achterhalen (zie C-014). Wat er extra bij komt is de hele
vijver waaruit toekomstige dailies worden getrokken — om daar iets aan te hebben
moet je 1409 antwoorden uit je hoofd leren.

Wat wél weegt is het eerste punt: het is jouw werk, en de afspraak was dat het
er niet in zou staan.

Besluit nodig, want dit is niet aan mij:
1. laten staan — het is toch al gepubliceerd;
2. uit de repo halen met `git rm --cached` — stopt verdere verspreiding, maar
   het bestand blijft in de geschiedenis staan en is via elke oude commit nog
   op te halen;
3. echt weg — geschiedenis herschrijven en force-pushen. Dat werkt, maar het is
   onomkeerbaar en breekt elke kloon die iemand al heeft.

### C-014 · vervalt (geen lek) · Supabase (puzzles) · afgehandeld 10 sept
Nagegaan of iemand de dagpuzzel van morgen kan opvragen. Dit is de scherpere
versie van C-008: de app bevraagt niet de view `puzzles_public` maar de tabel
`puzzles` zelf, en beperkt zich daar met een eigen filter
`scheduled_date=lte.<vandaag>`. Een filter dat de client meestuurt, kan de
client ook weglaten.

Gemeten op de live site met de publieke anon key uit de pagina:

    toekomst (gt vandaag)    -> 200, 0 rijen
    verleden+vandaag (lte)   -> 200, 5 rijen, nieuwste 2026-09-10
    zonder datumfilter       -> 200, 5 rijen, nieuwste 2026-09-10

Ook zónder datumfilter komt er niets nieuwer dan vandaag terug. De policy op
`puzzles` dwingt de grens dus serverkant af, en niet de client. Dat is precies
zoals het hoort.

Meteen ook een antwoord op een deel van C-006: de onbekende policy op `puzzles`
doet het goede.

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

### C-003 · middel · Supabase (dagpuzzels) · klaargezet, wacht op de eigenaar
De dagpuzzels lopen tot 2026-10-09. Daarna heeft het spel niets te tonen op de
pagina waar iedereen binnenkomt.

`supabase/plan_dailies_vooruit.sql` staat klaar met 45 dagen; er blijven daarna
156 bruikbare library-puzzels over. **De eigenaar moet hem draaien.**

Bij het klaarzetten bleek de generator twee ontwerpfouten te hebben, en allebei
speelden ze juist op het moment dat je hem nodig hebt:

- Hij zette de datums vast bij het genereren, vanaf de dag van draaien. Met een
  agenda die al tot 9 oktober liep botste elke regel met een bestaande dag en
  werd er niets ingevoegd — zonder zichtbare fout. Je zou pas op 10 oktober
  merken dat je niets had gedaan. De SQL rekent nu zelf uit waar de reeks
  ophoudt.
- De lijst met al gebruikte library-puzzels stond met de hand in het
  Python-script, met in het commentaar de query om hem bij te werken. Loopt die
  achter, dan komt dezelfde puzzel een tweede keer langs. Nu kijkt de databank.

### C-015 · laag · Supabase (opslag + auth) · open
Twee kleine dingen uit de security advisor die nog openstaan, allebei één
handeling in het dashboard:

- De publieke bucket `daily-images` laat zich oplijsten (zie C-010).
- Leaked password protection staat uit (zie C-012).

### C-016 · vervalt (geen fout) · live site · afgehandeld 10 sept
De console van de live site leek fouten te geven: twee 404's en een 401. Bij
navraag in een verse tab: geen enkele melding. Het waren restanten van mijn
eigen HEAD-verzoeken in dezelfde tab, die in de buffer bleven staan.

Waarom dit blijft staan: ik had dit bijna als bevinding opgeschreven. Een
console-buffer die over herladingen heen blijft staan is precies het soort
meetfout dat je een avond kost.

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

### C-006 · vervalt (geen gat) · Supabase (policies) · afgehandeld 11 sept
De acht policies die niet uit deze repo kwamen zijn nagelezen. Geen ervan zet
iets open dat dicht hoort te zijn.

Twee staan op `true`, en dat leek het gevaarlijke geval:

- `library_puzzles` "Iedereen kan library puzzels lezen" — bevat de
  bibliotheekpuzzels mét antwoorden, leesbaar voor iedereen. Dat is geen lek:
  diezelfde antwoorden staan in `data/netto_frontend_puzzles.js`, dat elke
  browser downloadt om je score te kunnen uitrekenen. Zo werkt een spel dat aan
  de clientkant rekent.
- `scores` "leaderboard leesbaar" — de tabel is leeg (0 rijen) en de app gebruikt
  hem niet; ons scorebord draait op `user_plays`. Er valt dus niets te lezen.
  Wel iets om te onthouden: schrijft er ooit iets naar deze tabel, dan is het
  meteen voor iedereen leesbaar.

De rest toetst netjes op `auth.uid()` of `is_admin()`.

WAT MIJN QUERY NIET LIET ZIEN
Ik vroeg `qual` op, en dat veld is leeg bij INSERT-policies — daar telt
`with_check`. Van de acht INSERT-policies kon ik dus niet zien wát ze eisen, en
juist één ervan heet "iedereen mag vragen insturen" op een tabel waar `anon`
INSERT-rechten heeft. Dat is precies het soort naam waar je niet op moet gokken.

Daarom gemeten in plaats van gevraagd, met een lege insert vanaf de live site:
blokkeert RLS hem, dan volgt 403 "row-level security"; laat RLS hem door, dan
struikelt hij pas op een kolom-eis. Zo ontstaat er geen rij.

  question_submissions -> 401, "new row violates row-level security policy"
  profiles, user_plays, library_plays, archive_plays,
  user_notifications, scores, puzzles, admin_users -> 401, "permission denied"

Geen enkele tabel accepteert een schrijfactie van een uitgelogde bezoeker.

### C-017 · laag · Supabase (policies) · open
Twee policies op `question_submissions` hangen aan een e-mailadres in plaats van
aan `is_admin()`:

  "alleen admin keurt goed of af"  -> (auth.jwt() ->> 'email') = 'berendschroten@gmail.com'
  "alleen admin leest inzendingen" -> idem

Ze doen naast de `is_admin()`-policies hetzelfde werk, en permissive policies
worden met OR samengevoegd, dus er gaat niets mis. Maar ze koppelen beheerrechten
aan een adres dat kan veranderen, en ze maken het beeld troebel: zeven policies
op één tabel, waarvan vier hetzelfde doen.

Opruimen mag, hoeft niet vandaag, en is de keuze van de eigenaar — het zijn zijn
rechten.

### Nacht van 10 september — leaderboard, teksten en contrast
Op verzoek van de eigenaar doorgewerkt terwijl hij sliep. Alles gecommit en
gepusht; de live site draait het.

- **Het leaderboard laat nu mensen zien.** De oorzaak was de ontbrekende
  profielrij: de functie koppelt `user_plays` aan `profiles` met een gewone
  join, en zonder tegenhanger verdwijnt de rij. Na `leaderboard_werkend.sql`
  staan er drie spelers op.
- **Kijken mag zonder account.** De inlogmuur die Codex ervoor zette (X-001)
  blokkeerde ook de knop op het resultatenscherm. Die knop bestond al; hij werd
  onderschept. Meedoen vraagt nog steeds een account, met een uitnodiging onder
  de lijst.
- **Alleen de spelersnaam** op het bord; het e-mailadres kan er niet meer in
  belanden.
- **Zichtbaarheid uit te zetten** in Instellingen, standaard aan, bewaard in het
  profiel en niet in localStorage.
- **31 kapotte Engelse teksten.** Bij het machinaal vertalen sneuvelden emoji,
  soms met onzin ervoor in de plaats: "🔥 Huidige streak" werd "Gallus
  domesticus Current streak", "🟧 ≤2,50×" werd "Plywood ≤2,50×".
- **De deel-link wees naar netto.game**, waar dit spel niet staat, en de
  deelafbeelding bestond niet. Beide gerepareerd.
- **Contrast doorgemeten**, zeven schermen, beide thema's: van 20 unieke
  tekortkomingen naar 0. De ernstigste was de score op het scorebord in donkere
  modus — verhouding 1,18 waar 4,5 de ondergrens is, dus het belangrijkste getal
  op een scorebord was onleesbaar.

Wat ik daarvan meeneem: drie van deze fouten waren dezelfde fout — een
achtergrondkleur die als tekstkleur werd gebruikt. Eén ervan had ik zelf net
gemaakt.

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
