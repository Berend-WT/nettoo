-- Netto — dailies inplannen van 2026-09-10 tot en met 2026-10-09
--
-- GEGENEREERD door tools/plan_dailies.py. Hierna gaat inplannen via het
-- adminpaneel ("Volgende daily samenstellen").
--
-- WAAROM ÉÉN STATEMENT
-- De vorige versie bestond uit losse inserts. De SQL-editor stopt bij de eerste
-- fout maar houdt wat daarvoor al gelukt is, en dat leverde op 6 september
-- precies twee dailies op waarna het spel stil kwam te staan op een oude
-- puzzel. Dit is één insert: hij slaagt volledig of faalt volledig.
--
-- UITVOEREN
-- Supabase dashboard -> SQL Editor -> plak dit -> Run. Datums die al bezet zijn
-- worden overgeslagen, dus opnieuw draaien kan geen kwaad. Onderaan staat een
-- controle die laat zien wat er daarna gepland staat.

insert into public.puzzles (
  question_1, question_2, question_3,
  true_answer_1, true_answer_2, true_answer_3,
  operator, scheduled_date, status, source_library_id
)
-- De literalen in VALUES zijn ongetypeerd; zonder de expliciete ::date hieronder
-- weigert Postgres de tekst in een date-kolom te zetten.
select v.question_1, v.question_2, v.question_3,
       v.true_answer_1, v.true_answer_2, v.true_answer_3,
       v.operator, v.scheduled_date::date, v.status, v.source_library_id
from (values
    ('Hoeveel leden heeft de Nederlandse Eerste Kamer?', 'Hoeveel punten heeft een try in rugby union?', 'Hoeveel duizend knipperbewegingen met je ogen maak je gemiddeld per dag?', 75, 5, 15, '÷', '2026-09-10', 'scheduled', 'library-001'),  -- Politiek en recht / Sport / Biologie & gezondheid
    ('Hoeveel stappen telt de Mayapyramide El Castillo per zijde?', 'Hoeveel genummerde scorevakken heeft een dartbord?', 'In welk jaar werd Antarctica voor het eerst waargenomen door een expeditie?', 91, 20, 1820, '×', '2026-09-11', 'scheduled', 'library-004'),  -- Gebouwen en infrastructuur / Spellen en speelgoed / Geografie
    ('Hoeveel dagen duurt de zwangerschap van een koe?', 'Hoeveel diagonalen heeft een regelmatige twintighoek?', 'Hoeveel piercings had de persoon met de meeste piercings ooit?', 283, 170, 453, '+', '2026-09-12', 'scheduled', 'library-002'),  -- Landbouw en industrie / Wiskunde / Records en vergelijkingen
    ('Hoe lang was de langste man ooit in centimeters?', 'Hoeveel kilometer lang is de Betuweroute goederenspoorlijn?', 'Hoeveel kaarten bevat een standaard UNO-deck?', 272, 160, 112, '−', '2026-09-13', 'scheduled', 'library-003'),  -- Records en vergelijkingen / Vervoer / Spellen en speelgoed
    ('Hoeveel leden telt de Duitse Bondsdag volgens de wettelijke omvang sinds de hervorming?', 'Hoeveel kilogram weegt een volwassen mannelijke rode reuzenkangoeroe maximaal?', 'Hoeveel gram koffie gebruikt een standaard espresso van 25 ml?', 630, 90, 7, '÷', '2026-09-14', 'scheduled', 'library-005'),  -- Politiek en recht / Dieren / Eten & drinken
    ('Hoeveel meter hoog is de Tokyo Tower?', 'Hoeveel snaren heeft een standaard elektrische gitaar?', 'In welk jaar werd Google opgericht?', 333, 6, 1998, '×', '2026-09-15', 'scheduled', 'library-008'),  -- Gebouwen en infrastructuur / Muziek / Technologie
    ('Hoeveel kilogram weegt een volwassen nijlpaard?', 'Hoeveel schepen ondersteunden de geallieerde landing in Normandië?', 'Hoeveel hotels heeft Hilton wereldwijd ongeveer?', 1500, 6000, 7500, '+', '2026-09-16', 'scheduled', 'library-006'),  -- Dieren / Geschiedenis / Reizen en toerisme
    ('Hoeveel kilometer lang is het Baikalmeer ongeveer?', 'Hoeveel meter lang is een officiële atletiekbaan op de binnenbaan?', 'Hoeveel afleveringen telt de serie Friends in totaal?', 636, 400, 236, '−', '2026-09-17', 'scheduled', 'library-007'),  -- Geografie / Sport / Films en series
    ('In welk jaar begon de Koreaanse oorlog?', 'Hoeveel leden telt het Britse House of Commons?', 'Hoeveel harten heeft een octopus?', 1950, 650, 3, '÷', '2026-09-18', 'scheduled', 'library-009'),  -- Geschiedenis / Politiek en recht / Dieren
    ('Hoeveel kilocalorieën bevat een Amerikaanse McDonald’s cheeseburger?', 'Hoeveel vierkante kilometer is het Arctische zee-ijs in de zomer ongeveer minimaal?', 'Hoeveel ton maïs werd wereldwijd geproduceerd in 2023?', 300, 4000000, 1200000000, '×', '2026-09-19', 'scheduled', 'library-012'),  -- Eten & drinken / Geografie / Landbouw en industrie
    ('Hoeveel kilogram weegt de tong van een blauwe vinvis ongeveer?', 'Hoeveel vliegtuigen ondersteunden D-Day?', 'Hoeveel kilogram weegt de Great Bell, de grote klok van Big Ben?', 2700, 11000, 13700, '+', '2026-09-20', 'scheduled', 'library-010'),  -- Dieren / Geschiedenis / Gebouwen en infrastructuur
    ('Hoeveel meter diep is de Challengerdiepte in de Marianentrog?', 'In welk jaar werd de eerste reageerbuisbaby geboren?', 'Hoeveel mensen deden mee aan het grootste waterballonnengevecht ooit?', 10935, 1978, 8957, '−', '2026-09-21', 'scheduled', 'library-011'),  -- Geografie / Biologie & gezondheid / Records en vergelijkingen
    ('Wat is de gemiddelde afstand van de aarde tot de zon?', 'Hoeveel kilometer lang was de Romeinse rijksgrens, de Roman Limes, volgens UNESCO ongeveer?', 'Hoeveel KFC-restaurants zijn er wereldwijd ongeveer?', 150000000, 5000, 30000, '÷', '2026-09-22', 'scheduled', 'library-013'),  -- Sterrenkunde & ruimte / Geschiedenis / Merken en producten
    ('Hoeveel films telt de originele Back to the Future-trilogie?', 'Hoeveel etappes telt de Tour de France doorgaans?', 'Hoeveel nationale parken telt de Verenigde Staten?', 3, 21, 63, '×', '2026-09-23', 'scheduled', 'library-016'),  -- Films en series / Sport / Geografie
    ('Hoeveel procent van de bekende plant- en diersoorten leeft in tropische regenwouden?', 'Hoeveel meter hoog is de Elizabeth Tower, de toren van Big Ben?', 'In welk jaar voor Christus viel Carthago in handen van de Romeinen?', 50, 96, 146, '+', '2026-09-24', 'scheduled', 'library-014'),  -- Milieu en duurzaamheid / Gebouwen en infrastructuur / Geschiedenis
    ('Hoeveel miljoen kubieke meter aarde werd er uitgegraven voor de bouw van het Panamakanaal?', 'Hoeveel kilometer per seconde draait de aarde om de zon?', 'Wat weegt het hart van een volwassen Blauwe Vinvis in kilogram?', 210, 30, 180, '−', '2026-09-25', 'scheduled', 'library-015'),  -- Gebouwen en infrastructuur / Sterrenkunde & ruimte / Dieren
    ('Hoeveel artikelen bevat het Handvest van de Verenigde Naties?', 'Hoeveel seizoenen van The Simpsons waren er uitgezonden (stand 2026)?', 'Hoeveel landen grenzen aan het Victoriameer?', 111, 37, 3, '÷', '2026-09-26', 'scheduled', 'library-017'),  -- Politiek en recht / Films en series / Geografie
    ('Hoeveel landen heeft Coca-Cola als afzetmarkt ongeveer?', 'Hoeveel vakjes heeft een standaard Mens-erger-je-niet-bord?', 'Hoeveel stenen beelden staan er in het Terracottaleger ongeveer?', 200, 40, 8000, '×', '2026-09-27', 'scheduled', 'library-020'),  -- Merken en producten / Spellen en speelgoed / Kunst en cultuur
    ('Hoeveel toetsen heeft een standaard computertoetsenbord ongeveer?', 'Hoeveel dagen duurt de zwangerschap van een schaap?', 'Hoe lang is de langste levende man in centimeters?', 104, 147, 251, '+', '2026-09-28', 'scheduled', 'library-018'),  -- Technologie / Landbouw en industrie / Records en vergelijkingen
    ('Hoeveel uren duurde de historische Apollo 11-missie naar de maan?', 'Hoeveel meter is de afstand van de Olympische mannen-hordensprint?', 'Hoeveel procent van de wetlands is sinds 1700 wereldwijd verdwenen?', 195, 110, 85, '−', '2026-09-29', 'scheduled', 'library-019'),  -- Sterrenkunde & ruimte / Sport / Milieu en duurzaamheid
    ('Hoeveel kilometer per uur kunnen de sterkste winden op Neptunus ongeveer bereiken?', 'Hoeveel kcal heeft een middelgroot ei?', 'Welk percentage van het zoete water bevindt zich in grondwater?', 2100, 70, 30, '÷', '2026-09-30', 'scheduled', 'library-021'),  -- Sterrenkunde & ruimte / Eten & drinken / Milieu en duurzaamheid
    ('Hoeveel gram eiwit bevat een Amerikaanse McDonald’s Big Mac?', 'Hoeveel dagen duurde de reis van de Mayflower naar Noord-Amerika?', 'Wat is de autorij-afstand van Amsterdam naar Rome in km?', 25, 66, 1650, '×', '2026-10-01', 'scheduled', 'library-024'),  -- Eten & drinken / Geschiedenis / Geografie
    ('Hoeveel noten bevat een standaard majeurtoonladder inclusief het herhaalde octaaf?', 'In welk jaar werd de eerste exoplaneet rond een zonachtige ster ontdekt?', 'In welk jaar werd de eerste volledige sequentie van het menselijke genoom gepubliceerd?', 8, 1995, 2003, '+', '2026-10-02', 'scheduled', 'library-022'),  -- Muziek / Sterrenkunde & ruimte / Biologie & gezondheid
    ('In welk jaar werd het World Wide Web publiek vrijgegeven?', 'In welk jaar vond de kernramp in Tsjernobyl plaats?', 'Hoeveel schilderijen uit de serie Zonnebloemen maakte Van Gogh?', 1993, 1986, 7, '−', '2026-10-03', 'scheduled', 'library-023'),  -- Technologie / Geschiedenis / Kunst en cultuur
    ('Hoeveel winkels heeft Lidl wereldwijd ongeveer?', 'Hoeveel schilderijen van Vincent van Gogh bezit het Van Gogh Museum?', 'Hoeveel soorten telt de kangoeroefamilie (Macropodidae)?', 13000, 200, 65, '÷', '2026-10-04', 'scheduled', 'library-025'),  -- Merken en producten / Kunst en cultuur / Dieren
    ('Hoeveel volt heeft een standaard stopcontact in Nederland?', 'Hoeveel kilogram weegt een gemiddeld stenen blok van de Piramide van Cheops?', 'Hoeveel vierkante kilometer is de Noordzee ongeveer groot?', 230, 2500, 575000, '×', '2026-10-05', 'scheduled', 'library-028'),  -- Technologie / Gebouwen en infrastructuur / Geografie
    ('In welk jaar werd Microsoft Excel voor het eerst uitgebracht?', 'Hoeveel meter lang is de Brooklyn Bridge?', 'Op welke hoogte ligt het Titicacameer ongeveer boven zeeniveau?', 1985, 1825, 3810, '+', '2026-10-06', 'scheduled', 'library-026'),  -- Technologie / Gebouwen en infrastructuur / Geografie
    ('In welk jaar werd de eerste Android-telefoon uitgebracht?', 'Hoeveel soorten worst kent de Duitse keuken ongeveer?', 'Hoeveel meter breed zijn de Victoriawatervallen?', 2008, 300, 1708, '−', '2026-10-07', 'scheduled', 'library-027'),  -- Technologie / Eten & drinken / Geografie
    ('Hoeveel kilometer moet een bijenvolk gezamenlijk vliegen om één kilo honing te produceren?', 'Hoeveel gebeden per dag schrijft de islamitische traditie voor?', 'Hoeveel ton bommen werd tijdens de Blitz op Londen afgeworpen?', 90000, 5, 18000, '÷', '2026-10-08', 'scheduled', 'library-029'),  -- Dieren / Filosofie, psychologie en religie / Geschiedenis
    ('Hoeveel kamers heeft de maag van een koe?', 'Hoeveel letters heeft het Russische alfabet?', 'Hoeveel kamers heeft het Witte Huis?', 4, 33, 132, '×', '2026-10-09', 'scheduled', 'library-032')  -- Dieren / Taal / Gebouwen en infrastructuur
) as v(question_1, question_2, question_3,
       true_answer_1, true_answer_2, true_answer_3,
       operator, scheduled_date, status, source_library_id)
where not exists (
  select 1 from public.puzzles p
  where p.scheduled_date = v.scheduled_date::date
);


-- Controle: hoort een aaneengesloten reeks te tonen, zonder gaten.
select scheduled_date,
       scheduled_date - (lag(scheduled_date) over (order by scheduled_date)) as gat_in_dagen,
       left(question_1, 46) as vraag
from public.puzzles
where scheduled_date >= current_date - 1
order by scheduled_date;
