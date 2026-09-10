-- Netto — plan 45 dagpuzzels vooruit, aansluitend op wat er al staat
--
-- GEGENEREERD door tools/plan_dailies.py.
--
-- WAAROM DE DATUMS HIER NIET IN STAAN
-- Een eerdere versie zette de datums vast bij het genereren, vanaf de dag van
-- draaien. Draaide je hem terwijl er al tot 9 oktober gepland stond, dan botste
-- elke regel met een bestaande dag en werd er niets toegevoegd — zonder dat er
-- iets misging waar je iets van merkte. Nu rekent de SQL zelf uit waar de reeks
-- ophoudt en telt daarvandaan verder.
--
-- WAAROM ÉÉN STATEMENT
-- De versie daarvóór bestond uit losse inserts. De SQL-editor stopt bij de
-- eerste fout maar houdt wat daarvoor al gelukt is, en dat leverde op
-- 6 september twee dailies op waarna het spel stil kwam te staan op een oude
-- puzzel. Dit is één insert: hij slaagt volledig of faalt volledig.
--
-- TWEE KEER DRAAIEN KAN GEEN KWAAD
-- Een dag die al bezet is wordt overgeslagen, en een library-puzzel die al eens
-- daily is geweest ook. Dat tweede stond eerst als handmatige lijst in het
-- Python-script; als die lijst achterliep kwam dezelfde puzzel een tweede keer
-- langs. Nu kijkt de databank zelf.
--
-- UITVOEREN
-- Supabase dashboard -> SQL Editor -> plak dit -> Run. Onderaan staat een
-- controle die laat zien wat er daarna gepland staat.

insert into public.puzzles (
  question_1, question_2, question_3,
  true_answer_1, true_answer_2, true_answer_3,
  operator, scheduled_date, status, source_library_id
)
select v.question_1, v.question_2, v.question_3,
       v.true_answer_1, v.true_answer_2, v.true_answer_3,
       v.operator,
       -- Verdergaan waar de agenda ophoudt. Staat er nog niets, dan begint hij
       -- vandaag.
       (select greatest(coalesce(max(scheduled_date), current_date - 1), current_date - 1)
          from public.puzzles) + v.dagnummer::int,
       v.status, v.source_library_id
from (values
    ('Hoeveel leden heeft de Nederlandse Eerste Kamer?', 'Hoeveel landen grenzen aan Zwitserland?', 'Hoeveel duizend knipperbewegingen met je ogen maak je gemiddeld per dag?', 75, 5, 15, '÷', 1, 'scheduled', 'library-001'),  -- Politiek en recht / Geografie / Biologie & gezondheid
    ('Hoeveel landen telt Azië?', 'Hoeveel procent van het Great Barrier Reef bestaat uit koraalriffen?', 'Hoeveel meter hoog is het hoogste punt van het Millauviaduct?', 49, 7, 343, '×', 2, 'scheduled', 'library-004'),  -- Geografie / Milieu en duurzaamheid / Gebouwen en infrastructuur
    ('In welk jaar werd de Volksrepubliek China gesticht?', 'Hoeveel gram weegt een standaard Mars reep?', 'Hoeveel eitjes kan een koninginnenbij per dag leggen?', 1949, 51, 2000, '+', 3, 'scheduled', 'library-002'),  -- Geschiedenis / Eten & drinken / Dieren
    ('Hoeveel uren duurde de historische Apollo 11-missie naar de maan?', 'Hoeveel meter is de afstand van de Olympische mannen-hordensprint?', 'Hoeveel procent van de wetlands is sinds 1700 wereldwijd verdwenen?', 195, 110, 85, '−', 4, 'scheduled', 'library-003'),  -- Sterrenkunde & ruimte / Sport / Milieu en duurzaamheid
    ('Hoeveel kilometer per uur kunnen de sterkste winden op Neptunus ongeveer bereiken?', 'Hoeveel kcal heeft een middelgroot ei?', 'Hoeveel kilogram weegt een volwassen wombat?', 2100, 70, 30, '÷', 5, 'scheduled', 'library-005'),  -- Sterrenkunde & ruimte / Eten & drinken / Dieren
    ('Hoeveel kilometer lang was de Romeinse rijksgrens, de Roman Limes, volgens UNESCO ongeveer?', 'Hoeveel kleuren heeft de vlag van België?', 'Hoeveel liter water is volgens de gangbare berekening nodig om één kilogram rundvlees te produceren?', 5000, 3, 15000, '×', 6, 'scheduled', 'library-008'),  -- Geschiedenis / Geografie / Milieu en duurzaamheid
    ('Hoeveel kilogram weegt een volwassen nijlpaard?', 'Hoeveel schepen ondersteunden de geallieerde landing in Normandië?', 'Hoeveel hotels heeft Hilton wereldwijd ongeveer?', 1500, 6000, 7500, '+', 7, 'scheduled', 'library-006'),  -- Dieren / Geschiedenis / Reizen en toerisme
    ('In welk jaar werd het World Wide Web publiek vrijgegeven?', 'In welk jaar vond de kernramp in Tsjernobyl plaats?', 'Hoeveel schilderijen uit de serie Zonnebloemen maakte Van Gogh?', 1993, 1986, 7, '−', 8, 'scheduled', 'library-007'),  -- Technologie / Geschiedenis / Kunst en cultuur
    ('In welk jaar werd de eerste stoomlocomotief gebouwd?', 'Hoeveel letters heeft het Thaise alfabet?', 'Hoeveel symfonieën schreef Mozart?', 1804, 44, 41, '÷', 9, 'scheduled', 'library-009'),  -- Vervoer / Taal / Muziek
    ('Hoeveel kilocalorieën bevat een Amerikaanse McDonald’s cheeseburger?', 'Hoeveel vierkante kilometer is het Arctische zee-ijs in de zomer ongeveer minimaal?', 'Hoeveel ton maïs werd wereldwijd geproduceerd in 2023?', 300, 4000000, 1200000000, '×', 10, 'scheduled', 'library-012'),  -- Eten & drinken / Geografie / Landbouw en industrie
    ('Hoeveel inwoners heeft Monaco?', 'Hoeveel vliegtuigen ondersteunden D-Day?', 'Hoeveel bijen leven er in een sterk bijenvolk in de zomer?', 39000, 11000, 50000, '+', 11, 'scheduled', 'library-010'),  -- Geografie / Geschiedenis / Landbouw en industrie
    ('In welk jaar werd de eerste kunstmatige satelliet gelanceerd?', 'Hoeveel letters heeft het Turkse alfabet?', 'In welk jaar werd penicilline ontdekt?', 1957, 29, 1928, '−', 12, 'scheduled', 'library-011'),  -- Sterrenkunde & ruimte / Taal / Biologie & gezondheid
    ('Hoeveel kilometer moet een bijenvolk gezamenlijk vliegen om één kilo honing te produceren?', 'Hoeveel punten heeft een try in rugby union?', 'Hoeveel ton bommen werd tijdens de Blitz op Londen afgeworpen?', 90000, 5, 18000, '÷', 13, 'scheduled', 'library-013'),  -- Dieren / Sport / Geschiedenis
    ('Hoeveel medeklinkerletters heeft het Thaise alfabet?', 'Hoeveel harten heeft een octopus?', 'Hoeveel kamers heeft het Witte Huis?', 44, 3, 132, '×', 14, 'scheduled', 'library-016'),  -- Taal / Dieren / Gebouwen en infrastructuur
    ('Hoeveel miljard neuronen (zenuwcellen) bevat het menselijk brein naar schatting?', 'Hoeveel landen grenzen aan de Middellandse Zee?', 'Hoeveel graden is elke binnenhoek van een regelmatige vijfhoek?', 86, 22, 108, '+', 15, 'scheduled', 'library-014'),  -- Biologie & gezondheid / Geografie / Wiskunde
    ('Hoeveel liften heeft het Empire State Building?', 'Hoeveel poten heeft een krab?', 'Hoeveel nationale parken telt de Verenigde Staten?', 73, 10, 63, '−', 16, 'scheduled', 'library-015'),  -- Gebouwen en infrastructuur / Dieren / Geografie
    ('Hoeveel meter hoog is de Elizabeth Tower, de toren van Big Ben?', 'Hoeveel poten heeft een standaard statief?', 'Hoeveel kilometer per uur zwemt een dolfijn op zijn snelst?', 96, 3, 32, '÷', 17, 'scheduled', 'library-017'),  -- Gebouwen en infrastructuur / Dagelijks leven / Dieren
    ('Hoeveel volt heeft een standaard stopcontact in Nederland?', 'Hoeveel delen bevat Plato’s De Staat?', 'Hoeveel kilometer lang is het Great Barrier Reef ongeveer?', 230, 10, 2300, '×', 18, 'scheduled', 'library-020'),  -- Technologie / Filosofie, psychologie en religie / Geografie
    ('In welk jaar werd de eerste radio-uitzending gemaakt?', 'Hoeveel basis-ingrediënten heeft een klassieke pizza Margherita?', 'In welk jaar bereikte de eerste expeditie de Noordpool volgens de traditionele erkenning?', 1906, 3, 1909, '+', 19, 'scheduled', 'library-018'),  -- Technologie / Eten & drinken / Geschiedenis
    ('Hoeveel stippen staan er in totaal op een standaard set van 28 dominostenen?', 'Hoeveel procent van het menselijk lichaam bestaat ongeveer uit water?', 'Hoeveel meter hoog zijn de Victoriawatervallen?', 168, 60, 108, '−', 20, 'scheduled', 'library-019'),  -- Spellen en speelgoed / Biologie & gezondheid / Geografie
    ('Hoeveel graden Celsius is het smeltpunt van tin ongeveer?', 'Hoeveel noten bevat een standaard majeurtoonladder inclusief het herhaalde octaaf?', 'Welk percentage van het aardoppervlak bestaat uit land?', 232, 8, 29, '÷', 21, 'scheduled', 'library-021'),  -- Scheikunde / Muziek / Milieu en duurzaamheid
    ('Hoeveel meter lang is een officiële atletiekbaan op de binnenbaan?', 'Hoeveel torens heeft de Sagrada Família volgens het voltooide ontwerp?', 'Hoeveel liter bloed pompt een mensenhart gemiddeld per dag rond?', 400, 18, 7200, '×', 22, 'scheduled', 'library-024'),  -- Sport / Gebouwen en infrastructuur / Biologie & gezondheid
    ('Hoeveel LEGO-steentjes worden er wereldwijd per seconde gemaakt?', 'Hoeveel kilometer lang is de Niger?', 'Wat is de geschatte temperatuur aan het oppervlak van de zon?', 1300, 4200, 5500, '+', 23, 'scheduled', 'library-022'),  -- Spellen en speelgoed / Geografie / Sterrenkunde & ruimte
    ('Hoeveel liter zuurstof ademt een mens gemiddeld per dag in?', 'Hoeveel kilometer lang is de Nederlandse kustlijn ongeveer?', 'Hoeveel Grammy-nominaties had Beyoncé volgens de Grammy’s vóór de uitreiking van 2025?', 550, 451, 99, '−', 24, 'scheduled', 'library-023'),  -- Biologie & gezondheid / Geografie / Muziek
    ('In welk jaar werd Antarctica voor het eerst waargenomen door een expeditie?', 'Hoeveel soorten telt de kangoeroefamilie (Macropodidae)?', 'Hoeveel jaar bestond de Berlijnse Muur?', 1820, 65, 28, '÷', 25, 'scheduled', 'library-025'),  -- Geografie / Dieren / Geschiedenis
    ('Hoeveel smaakpapillen heeft een menselijke tong ongeveer?', 'Hoeveel kilometer van de Maas ligt in Nederland?', 'Hoeveel klinknagels houden de metalen delen van de Eiffeltoren bij elkaar?', 10000, 250, 2500000, '×', 26, 'scheduled', 'library-028'),  -- Biologie & gezondheid / Geografie / Gebouwen en infrastructuur
    ('Hoeveel metrostations heeft de Parijse metro?', 'Hoe groot was de grootste pizza ooit in vierkante meter?', 'In welk jaar werd de eerste moderne krant gepubliceerd?', 308, 1297, 1605, '+', 27, 'scheduled', 'library-026'),  -- Vervoer / Records en vergelijkingen / Boeken en literatuur
    ('Hoeveel duizend inwoners heeft Amsterdam?', 'Hoe lang duurde de langste plank ooit in minuten?', 'Hoeveel treden telt de wenteltrap in het Vrijheidsbeeld naar de kroon?', 933, 579, 354, '−', 28, 'scheduled', 'library-027'),  -- Geografie / Records en vergelijkingen / Gebouwen en infrastructuur
    ('Hoeveel soldaten namen deel aan de landing in Normandië op D-Day?', 'Hoeveel vogelsoorten telt het Amazonegebied?', 'Hoeveel zetels telt de Nieuw-Zeelandse Kamer van Afgevaardigden?', 156000, 1300, 120, '÷', 29, 'scheduled', 'library-029'),  -- Geschiedenis / Dieren / Politiek en recht
    ('Hoeveel landen heeft Coca-Cola als afzetmarkt ongeveer?', 'Hoeveel boeken bevat de Harry Potter-hoofdserie?', 'Wat is de totale lengte van alle onderzeese internetkabels op aarde in duizend kilometer?', 200, 7, 1400, '×', 30, 'scheduled', 'library-032'),  -- Merken en producten / Boeken en literatuur / Technologie
    ('Hoeveel kilometer per uur waait wind bij windkracht 8 volgens de schaal van Beaufort?', 'Hoeveel seizoenen van The Simpsons waren er uitgezonden (stand 2026)?', 'Hoeveel artikelen bevat het Handvest van de Verenigde Naties?', 74, 37, 111, '+', 31, 'scheduled', 'library-030'),  -- Natuurkunde / Films en series / Politiek en recht
    ('Hoeveel procent van Antarctica is met ijs bedekt?', 'Welk percentage van het zoete water zit vast in ijs en gletsjers?', 'Hoe oud werd de oudste hond volgens Guinness World Records in jaren?', 98, 69, 29, '−', 32, 'scheduled', 'library-031'),  -- Geografie / Milieu en duurzaamheid / Records en vergelijkingen
    ('Hoeveel delen CO₂ per miljoen delen lucht zat er rond het pre-industriële referentiejaar in de atmosfeer?', 'Hoeveel komedies schreef Shakespeare volgens de traditionele genre-indeling?', 'Hoeveel zijvlakken heeft een icosaeder?', 280, 14, 20, '÷', 33, 'scheduled', 'library-033'),  -- Milieu en duurzaamheid / Boeken en literatuur / Wiskunde
    ('Welk percentage van het mariene afval bestaat volgens UNEP minstens uit plastic?', 'Hoeveel studioalbums bracht Michael Jackson uit?', 'Hoeveel schepen werden ingezet bij de evacuatie van Duinkerke?', 85, 10, 850, '×', 34, 'scheduled', 'library-036'),  -- Milieu en duurzaamheid / Muziek / Geschiedenis
    ('Hoeveel kaarten bevat een standaard UNO-deck?', 'Hoeveel verdiepingen heeft One World Trade Center?', 'Hoeveel mogelijke worpen zijn er met drie gewone dobbelstenen?', 112, 104, 216, '+', 35, 'scheduled', 'library-034'),  -- Spellen en speelgoed / Gebouwen en infrastructuur / Wiskunde
    ('Hoeveel miljard LEGO-steentjes zijn er sinds 1958 wereldwijd in totaal geproduceerd?', 'Wat is de autorij-afstand van Amsterdam naar Parijs in km?', 'Hoeveel graden heeft een rechte hoek?', 600, 510, 90, '−', 36, 'scheduled', 'library-035'),  -- Spellen en speelgoed / Geografie / Wiskunde
    ('In welk jaar voer de eerste moderne onderzeeër succesvol?', 'Hoeveel schilderijen van Vincent van Gogh bezit het Van Gogh Museum?', 'Hoeveel Muzen (dochters van Zeus) telt de Griekse mythologie?', 1800, 200, 9, '÷', 37, 'scheduled', 'library-037'),  -- Vervoer / Kunst en cultuur / Filosofie, psychologie en religie
    ('Hoeveel landen telt Afrika?', 'Hoeveel landen ondertekenden de UNESCO-grondwet in 1945?', 'In welk jaar werd Google opgericht?', 54, 37, 1998, '×', 38, 'scheduled', 'library-040'),  -- Geografie / Kunst en cultuur / Technologie
    ('In welk jaar voer de eerste nucleaire onderzeeër uit?', 'Hoeveel centimeter breed is de Mona Lisa?', 'In welk jaar werd de eerste Android-telefoon uitgebracht?', 1955, 53, 2008, '+', 39, 'scheduled', 'library-038'),  -- Vervoer / Kunst en cultuur / Technologie
    ('Wat is de dakhoogte van het Empire State Building in New York in meters?', 'Wat weegt het hart van een volwassen Blauwe Vinvis in kilogram?', 'Hoeveel afleveringen telt de Amerikaanse versie van The Office?', 381, 180, 201, '−', 40, 'scheduled', 'library-039'),  -- Gebouwen en infrastructuur / Dieren / Films en series
    ('Hoeveel eilanden telt Indonesië officieel (2024)?', 'Hoeveel diagonalen heeft een regelmatige twintighoek?', 'Hoeveel procent van het aardoppervlak bestaat uit water en land samen?', 17000, 170, 100, '÷', 41, 'scheduled', 'library-041'),  -- Geografie / Wiskunde / Milieu en duurzaamheid
    ('Wat is de snelheid van het licht in vacuüm in kilometer per seconde?', 'Hoeveel procent van het wereldwijde waterverbruik gaat naar landbouw?', 'Hoeveel bitcoins kunnen er maximaal worden gecreëerd?', 300000, 70, 21000000, '×', 42, 'scheduled', 'library-044'),  -- Natuurkunde / Milieu en duurzaamheid / Economie & geld
    ('Wat is de snelheid van het geluid in droge lucht bij 20°C in km/u?', 'Hoeveel kilocalorieën bevat een Amerikaanse McDonald’s Big Mac?', 'In welk jaar vond de Slag bij Waterloo plaats?', 1235, 580, 1815, '+', 43, 'scheduled', 'library-042'),  -- Natuurkunde / Eten & drinken / Geschiedenis
    ('Hoe zwaar was de grootste chocoladereep ooit in kilogram?', 'In welk jaar werd de Mount Everest voor het eerst succesvol beklommen?', 'Hoeveel pixels breed is een standaard 4K Ultra HD videoscherm?', 5793, 1953, 3840, '−', 44, 'scheduled', 'library-043'),  -- Records en vergelijkingen / Geschiedenis / Technologie
    ('Hoeveel ton bananen worden wereldwijd jaarlijks geproduceerd?', 'Hoeveel actieve vulkanen zijn er op aarde naar schatting?', 'Wat is de totale geschatte lengte van alle bloedvaten in een volwassen menselijk lichaam in kilometers?', 135000000, 1350, 100000, '÷', 45, 'scheduled', 'library-045')  -- Landbouw en industrie / Geografie / Biologie & gezondheid
) as v(question_1, question_2, question_3,
       true_answer_1, true_answer_2, true_answer_3,
       operator, dagnummer, status, source_library_id)
where not exists (
  select 1 from public.puzzles p
  where p.scheduled_date =
    (select greatest(coalesce(max(scheduled_date), current_date - 1), current_date - 1)
       from public.puzzles) + v.dagnummer::int
)
and not exists (
  select 1 from public.puzzles p
  where p.source_library_id = v.source_library_id
);


-- Controle: hoort een aaneengesloten reeks te tonen, zonder gaten.
-- Staat er een getal groter dan 1 in gat_in_dagen, dan mist er een dag.
select scheduled_date,
       scheduled_date - (lag(scheduled_date) over (order by scheduled_date)) as gat_in_dagen,
       left(question_1, 46) as vraag
from public.puzzles
where scheduled_date >= current_date - 1
order by scheduled_date;
