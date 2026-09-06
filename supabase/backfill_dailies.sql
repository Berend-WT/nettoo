-- Netto — bestaande dailies naar de puzzles-tabel
--
-- GEGENEREERD door fotos/maak_daily_backfill_sql.py; niet met de hand bijwerken.
--
-- WAAROM
-- De dailies stonden alleen in netto_frontend_puzzles.js. De frontend leest nu
-- ingeplande dailies uit Supabase (met dat bestand als vangnet), maar de tabel
-- was leeg. Zonder rij in puzzles is er niets om een foto, bronvermelding of
-- adminbewerking aan te hangen.
--
-- OPERATOR-CONSTRAINT
-- De check op puzzles.operator liet alleen ASCII + - * / toe, terwijl het spel
-- overal de typografische tekens gebruikt: × (U+00D7), ÷ (U+00F7) en − (U+2212).
-- 30 van de 35 dailies zouden dus geweigerd zijn, en het adminscherm zou bij de
-- eerste inplanning van een library-puzzel op dezelfde fout stuklopen.
-- library_puzzles staat die tekens al wel toe; puzzles wordt hier gelijkgetrokken.
--
-- UITVOEREN
-- Supabase dashboard -> SQL Editor -> plak dit -> Run. Veilig om te herhalen:
-- een datum die al bezet is, wordt overgeslagen.

-- ---------- operator-constraint gelijktrekken ----------
do $$
declare
  c record;
begin
  for c in
    select con.conname
    from pg_constraint con
    join pg_class rel on rel.oid = con.conrelid
    join pg_namespace nsp on nsp.oid = rel.relnamespace
    where nsp.nspname = 'public'
      and rel.relname = 'puzzles'
      and con.contype = 'c'
      and pg_get_constraintdef(con.oid) ilike '%operator%'
  loop
    execute format('alter table public.puzzles drop constraint %I', c.conname);
  end loop;
end $$;

alter table public.puzzles
  add constraint puzzles_operator_check
  check (operator in ('+', '−', '×', '÷'));

-- ---------- de dailies zelf ----------


insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'In welk jaar vond de Slag bij Waterloo plaats?', 'Hoeveel hoofdstukken bevat The Hobbit?', 'In welk jaar werd het eerste succesvolle vaccin ontwikkeld?', 1815, 19, 1796, '−', '2026-08-01', 'scheduled', 'library-169'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-01');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel damstenen krijgt iedere speler bij de start van een standaard damspel?', 'Hoeveel letters heeft het Turkse alfabet?', 'Hoeveel kilocalorieën bevat een Amerikaanse McDonald’s Big Mac?', 20, 29, 580, '×', '2026-08-02', 'scheduled', 'library-168'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-02');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel kamers heeft Buckingham Palace?', 'Hoeveel dagen doet de planeet Mars erover om rond de zon te draaien?', 'Hoeveel verdiepingen hebben de Petronas Twin Towers?', 775, 687, 88, '−', '2026-08-03', 'scheduled', 'library-167'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-03');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoe lang duurde de langste voetbalwedstrijd ooit in minuten?', 'Hoe zwaar was de zwaarste pompoen ooit in kilogram?', 'In welk jaar werd de eerste drukpers met losse letters in Europa gebruikt?', 203, 1247, 1450, '+', '2026-08-04', 'scheduled', 'library-164'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-04');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel zuilen heeft de Grote Zuilenzaal van de Tempel van Karnak ongeveer?', 'Wat is de diepte van het diepste zoetwatermeer ter wereld (Baikalmeer in Rusland) in meters?', 'Hoeveel treden heeft de trap van de CN Tower ongeveer?', 134, 1642, 1776, '+', '2026-08-05', 'scheduled', 'library-162'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-05');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'In welk jaar werd de eerste moderne volkstelling gehouden?', 'Hoeveel Muzen (dochters van Zeus) telt de Griekse mythologie?', 'Hoe hoog is de Euromast in Rotterdam?', 1665, 9, 185, '÷', '2026-08-06', 'scheduled', 'library-157'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-06');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel duizend knipperbewegingen met je ogen maak je gemiddeld per dag?', 'Hoeveel kiesmannen telt het Amerikaanse Electoral College?', 'Hoeveel meter hoog is de CN Tower?', 15, 538, 553, '+', '2026-08-07', 'scheduled', 'library-155'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-07');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel spelers staan er per team op het veld bij honkbal?', 'Hoeveel afzonderlijke riffen omvat het Great Barrier Reef ongeveer?', 'Hoeveel treden heeft de Burj Khalifa in Dubai?', 9, 2900, 2909, '+', '2026-08-08', 'scheduled', 'library-154'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-08');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoe lang was de langste vrouw ooit in centimeters?', 'Hoeveel meter hoog is Angel Falls ongeveer?', 'Hoeveel kilometer per uur is de geluidssnelheid op zeeniveau afgerond?', 255, 979, 1234, '+', '2026-08-09', 'scheduled', 'library-152'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-09');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel kilogram weegt de tong van een blauwe vinvis ongeveer?', 'Hoeveel rechters telt het Internationaal Gerechtshof?', 'Hoeveel graden heeft een gestrekte hoek?', 2700, 15, 180, '÷', '2026-08-10', 'scheduled', 'library-150'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-10');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel kilo weegt een koningspinguin?', 'Hoeveel landen heeft Coca-Cola als afzetmarkt ongeveer?', 'Hoeveel ton goud wordt wereldwijd jaarlijks gewonnen?', 15, 200, 3000, '×', '2026-08-11', 'scheduled', 'library-142'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-11');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'In welk jaar werd de Magna Carta bezegeld?', 'Hoeveel aardse dagen duurt één volledige draai van Venus ongeveer?', 'Hoeveel punten heeft een try in rugby union?', 1215, 243, 5, '÷', '2026-08-12', 'scheduled', 'library-138'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-12');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel poten heeft een krab?', 'Hoeveel diagonalen heeft een regelmatige twintighoek?', 'Hoeveel filialen heeft Decathlon wereldwijd ongeveer?', 10, 170, 1700, '×', '2026-08-13', 'scheduled', 'library-125'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-13');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel kilometer fietst een Nederlander gemiddeld per jaar?', 'Hoeveel tramlijnen heeft Amsterdam?', 'Welk percentage van het aardoppervlak bestaat uit oceanen en zeeën?', 1065, 15, 71, '÷', '2026-08-14', 'scheduled', 'library-124'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-14');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'In welk jaar werd de eerste exoplaneet rond een zonachtige ster ontdekt?', 'Hoeveel liften heeft de Burj Khalifa?', 'Hoeveel diagonalen heeft een regelmatige tienhoek?', 1995, 57, 35, '÷', '2026-08-15', 'scheduled', 'library-112'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-15');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel procent van het Great Barrier Reef bestaat uit koraalriffen?', 'Hoeveel letters heeft het Thaise alfabet?', 'Hoeveel metrostations heeft de Parijse metro?', 7, 44, 308, '×', '2026-08-16', 'scheduled', 'library-110'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-16');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel treden heeft het Empire State Building van straatniveau tot het observatiedek?', 'Hoeveel afleveringen telt de serie Breaking Bad?', 'Hoeveel kilometer per uur zwemt een dolfijn gemiddeld?', 1860, 62, 30, '÷', '2026-08-17', 'scheduled', 'library-109'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-17');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'In welk jaar werd de eerste Nintendo Game Boy uitgebracht?', 'Hoeveel letters heeft het Armeense alfabet?', 'Hoe lang waren de langste mouwen aan een kledingstuk ooit in meters?', 1989, 39, 51, '÷', '2026-08-18', 'scheduled', 'library-107'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-18');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel manieren kun je 3 renners op een podium van 8 deelnemers indelen?', 'Hoeveel etappes telt de Tour de France doorgaans?', 'Hoeveel chromosomen heeft een gewone ui Allium cepa in een lichaamscel?', 336, 21, 16, '÷', '2026-08-19', 'scheduled', 'library-106'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-19');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoe zwaar was de zwaarste hamburger ooit in kilogram?', 'Hoeveel procent van het lichaam was bedekt met tatoeages bij de meest getatoeëerde man?', 'Hoeveel afleveringen telt de iconische serie Fawlty Towers?', 1164, 97, 12, '÷', '2026-08-20', 'scheduled', 'library-101'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-20');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel start- en landingsbanen heeft Schiphol?', 'Hoeveel toetsen heeft een standaard MIDI-pianotoetsenbord met vijf octaven?', 'Hoeveel dagen telt een schrikkeljaar?', 6, 61, 366, '×', '2026-08-21', 'scheduled', 'library-098'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-21');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel kilometer lang is het Baikalmeer ongeveer?', 'Hoeveel centimeter breed is de Mona Lisa?', 'Hoeveel hoofdgoden telt de Griekse mythologie op de berg Olympus (de Twaalf Olympiërs)?', 636, 53, 12, '÷', '2026-08-22', 'scheduled', 'library-097'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-22');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'In welk jaar werd de eerste internationale telefonische verbinding gemaakt?', 'Hoeveel miljard neuronen (zenuwcellen) bevat het menselijk brein naar schatting?', 'Hoeveel wielen heeft een Airbus A380?', 1892, 86, 22, '÷', '2026-08-23', 'scheduled', 'library-094'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-23');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel gram suiker zit er in een blikje Coca-Cola van 330 ml?', 'Hoeveel witte toetsen heeft een concertpiano?', 'In welk jaar werd Antarctica voor het eerst waargenomen door een expeditie?', 35, 52, 1820, '×', '2026-08-24', 'scheduled', 'library-093'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-24');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel LEGO-steentjes worden er wereldwijd per seconde gemaakt?', 'Hoeveel speelkaarten zitten er in een standaard kaartspel (zonder jokers)?', 'Hoeveel aardse uren duurt één volledige draai van Mars ongeveer?', 1300, 52, 25, '÷', '2026-08-25', 'scheduled', 'library-092'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-25');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'In welk jaar werd de eerste digitale camera ontwikkeld?', 'Hoeveel protonen heeft een neutraal atoom van goud?', 'Hoeveel gram eiwit bevat een Amerikaanse McDonald’s Big Mac?', 1975, 79, 25, '÷', '2026-08-26', 'scheduled', 'library-090'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-26');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel millimeter per jaar verschuiven de aardplaten gemiddeld?', 'Hoeveel mannen ondertekenden de Amerikaanse Onafhankelijkheidsverklaring?', 'Wat is de totale lengte van alle onderzeese internetkabels op aarde in duizend kilometer?', 25, 56, 1400, '×', '2026-08-27', 'scheduled', 'library-088'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-27');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel letters heeft het Hebreeuwse alfabet?', 'Wat is de lengte van het Panamakanaal van de Atlantische naar de Stille Oceaan in km?', 'In welk jaar werd de eerste stoomlocomotief gebouwd?', 22, 82, 1804, '×', '2026-08-28', 'scheduled', 'library-087'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-28');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel procent van de bekende plant- en diersoorten leeft in tropische regenwouden?', 'Hoeveel verdiepingen heeft Taipei 101?', 'Hoeveel is de som van de getallen 1 tot en met 100?', 50, 101, 5050, '×', '2026-08-29', 'scheduled', 'library-083'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-29');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel Grammy’s heeft Beyoncé volgens de stand na de Grammy Awards van 2025 gewonnen?', 'Welk percentage van het wereldwijde cement wordt geproduceerd in China?', 'In welk jaar werd de eerste televisie-uitzending verzorgd?', 35, 55, 1925, '×', '2026-08-30', 'scheduled', 'library-081'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-30');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel halve tonen bevat een octaaf?', 'Welk percentage van het zoete water zit vast in ijs en gletsjers?', 'Wat is de hoogte van de Burj Khalifa in Dubai in meters?', 12, 69, 828, '×', '2026-08-31', 'scheduled', 'library-080'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-08-31');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel torens heeft het Kremlin in Moskou?', 'Hoeveel meter hoog is de Golden Gate Bridge boven het water?', 'Wat is de geschatte leeftijd van de planeet Aarde in miljoenen jaren?', 20, 227, 4540, '×', '2026-09-01', 'scheduled', 'library-078'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-01');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel landen grenzen aan Zwitserland?', 'Hoeveel verdiepingen heeft de Burj Khalifa?', 'Hoe groot was het grootste permanente IMAX-scherm in vierkante meter?', 5, 163, 815, '×', '2026-09-02', 'scheduled', 'library-074'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-02');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Welk percentage van het aardoppervlak bestaat uit land?', 'Hoeveel dagen duurde de reis van de Mayflower naar Noord-Amerika?', 'In welk jaar vertrok de eerste commerciële passagiersvlucht?', 29, 66, 1914, '×', '2026-09-03', 'scheduled', 'library-073'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-03');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel naamvallen heeft het Fins?', 'Hoeveel procent van Antarctica is met ijs bedekt?', 'Hoeveel meter diep is het Tanganyikameer op het diepste punt ongeveer?', 15, 98, 1470, '×', '2026-09-04', 'scheduled', 'library-072'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-04');


-- ---------- Controle achteraf ----------
-- Verwacht: 35 rijen, oudste 2026-08-01, nieuwste 2026-09-04.
--
-- select count(*), min(scheduled_date), max(scheduled_date) from public.puzzles;
--
-- Verwacht: geen enkele rij zonder derde vraag.
-- select count(*) from public.puzzles where question_3 is null;
