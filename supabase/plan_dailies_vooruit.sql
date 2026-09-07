-- Netto — dailies inplannen van 2026-09-07 tot en met 2026-10-06
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
    ('Hoeveel pionnen gebruikt iedere speler bij Mens-erger-je-niet?', 'Hoeveel ijsreuzen telt ons zonnestelsel?', 'Hoeveel wielen heeft een standaard fiets?', 4, 2, 2, '÷', '2026-09-07', 'scheduled', 'library-002'),  -- Spellen en speelgoed / Sterrenkunde & ruimte / Vervoer
    ('Hoeveel delen bevat Don Quichot?', 'Hoeveel landen liggen aan het Meer van Genève?', 'Hoeveel kamers heeft het menselijk hart?', 2, 2, 4, '×', '2026-09-08', 'scheduled', 'library-004'),  -- Boeken en literatuur / Geografie / Biologie & gezondheid
    ('Hoeveel wieken heeft een klassieke Nederlandse grondzeiler?', 'Hoeveel miljoen ton plastic afval lekt jaarlijks in de oceaan volgens een gangbare schatting?', 'Hoeveel chromosomenparen heeft een mens?', 4, 19, 23, '+', '2026-09-09', 'scheduled', 'library-028'),  -- Gebouwen en infrastructuur / Milieu en duurzaamheid / Biologie & gezondheid
    ('Hoeveel paar ribben heeft een mens normaal?', 'Hoeveel Oscars won de film Titanic (1997)?', 'Hoeveel officiële tijdzones heeft China?', 12, 11, 1, '−', '2026-09-10', 'scheduled', 'library-011'),  -- Biologie & gezondheid / Films en series / Geografie
    ('Hoeveel maagcompartimenten heeft een schaap?', 'Hoeveel landen delen het eiland Timor?', 'Hoeveel elementen bevat koolstofdioxide?', 4, 2, 2, '÷', '2026-09-11', 'scheduled', 'library-009'),  -- Dieren / Geografie / Scheikunde
    ('Hoeveel punten levert een safety op bij American football?', 'Hoeveel delen bevatte de oorspronkelijke publicatie van The Lord of the Rings?', 'Hoeveel snaren heeft een standaard gitaar?', 2, 3, 6, '×', '2026-09-12', 'scheduled', 'library-006'),  -- Sport / Boeken en literatuur / Muziek
    ('Hoeveel zijden heeft een hexagoon?', 'Hoeveel farao’s waren er volgens de traditionele telling tijdens de 18e dynastie van Egypte?', 'Hoeveel melktanden heeft een kind in een compleet melkgebit?', 6, 14, 20, '+', '2026-09-13', 'scheduled', 'library-029'),  -- Wiskunde / Geschiedenis / Biologie & gezondheid
    ('Hoeveel cijfers heeft een standaard ISBN-13?', 'Hoeveel punten levert een vrije worp op bij basketbal?', 'Hoeveel astronauten hebben er in de geschiedenis op de maan gelopen?', 13, 1, 12, '−', '2026-09-14', 'scheduled', 'library-012'),  -- Taal / Sport / Sterrenkunde & ruimte
    ('Hoeveel procent van het wereldwijde waterverbruik gaat naar landbouw?', 'Hoeveel afleveringen telt de originele Britse serie The Office (inclusief specials)?', 'Hoeveel lijnen heeft de metro van Rotterdam?', 70, 14, 5, '÷', '2026-09-15', 'scheduled', 'library-049'),  -- Milieu en duurzaamheid / Films en series / Vervoer
    ('Hoeveel landen grenzen aan de Dode Zee?', 'Hoeveel vleugels heeft een passagiersvliegtuig?', 'Hoeveel hartkleppen heeft het menselijk hart?', 2, 2, 4, '×', '2026-09-16', 'scheduled', 'library-008'),  -- Geografie / Vervoer / Biologie & gezondheid
    ('Hoeveel delen bevat Plato’s De Staat?', 'Uit hoeveel kuuroorden bestaat de UNESCO-site The Great Spa Towns of Europe?', 'Hoeveel EU-landen voerden de euro in bij de start van de euro in 1999?', 10, 11, 21, '+', '2026-09-17', 'scheduled', 'library-031'),  -- Filosofie, psychologie en religie / Kunst en cultuur / Economie & geld
    ('Hoeveel jaar duurde de bouw van de Hagia Sophia?', 'Hoeveel mannen liepen tijdens Apollo 11 op de maan?', 'Hoeveel farao’s hadden de drie grote piramides van Gizeh als opdrachtgever?', 5, 2, 3, '−', '2026-09-18', 'scheduled', 'library-013'),  -- Gebouwen en infrastructuur / Sterrenkunde & ruimte / Geschiedenis
    ('Hoeveel minuten officiële speeltijd heeft een basketbalwedstrijd volgens de NBA-regels?', 'Hoeveel letters bevat de domeinnaam-extensie .com?', 'Hoeveel Algemeen Fonds-kaarten bevat een klassiek Monopoly-spel?', 48, 3, 16, '÷', '2026-09-19', 'scheduled', 'library-050'),  -- Sport / Taal / Spellen en speelgoed
    ('Hoeveel bulten heeft een kameel?', 'Hoeveel koppen had Cerberus, de mythologische hond die de onderwereld bewaakt?', 'Hoeveel staten heeft Australië?', 2, 3, 6, '×', '2026-09-20', 'scheduled', 'library-010'),  -- Dieren / Filosofie, psychologie en religie / Geografie
    ('Hoeveel ogen heeft een bij?', 'Hoeveel provincies heeft Nederland?', 'Hoeveel artikelen bevat de Franse Verklaring van de Rechten van de Mens en de Burger?', 5, 12, 17, '+', '2026-09-21', 'scheduled', 'library-032'),  -- Dieren / Geografie / Politiek en recht
    ('Hoeveel hoofdstukken bevat Animal Farm?', 'Hoe lang was de langste snoepstaaf ooit in kilometer?', 'Hoeveel werelden verbindt de wereldboom Yggdrasil in de Noorse mythologie?', 10, 1, 9, '−', '2026-09-22', 'scheduled', 'library-014'),  -- Boeken en literatuur / Records en vergelijkingen / Filosofie, psychologie en religie
    ('Hoeveel gram koolhydraten bevat een Amerikaanse McDonald’s Big Mac?', 'Wat is de oppervlakte van de Sahara-woestijn in miljoen vierkante kilometer?', 'Hoeveel boeken bevat de gepubliceerde hoofdserie A Song of Ice and Fire?', 45, 9, 5, '÷', '2026-09-23', 'scheduled', 'library-053'),  -- Eten & drinken / Geografie / Boeken en literatuur
    ('Hoeveel kamers heeft het hart van een krokodil?', 'Hoeveel afgevaardigden ondertekenden de Amerikaanse Grondwet?', 'Hoe zwaar was de zwaarste hond ooit in kilogram?', 4, 39, 156, '×', '2026-09-24', 'scheduled', 'library-041'),  -- Dieren / Geschiedenis / Records en vergelijkingen
    ('Hoeveel boeken bevat de Harry Potter-hoofdserie?', 'Hoeveel aardse uren duurt één volledige draai van Jupiter ongeveer?', 'Hoeveel zuilen heeft het Parthenon aan de lange zijde?', 7, 10, 17, '+', '2026-09-25', 'scheduled', 'library-034'),  -- Boeken en literatuur / Sterrenkunde & ruimte / Gebouwen en infrastructuur
    ('Uit hoeveel leden bestaat de VN-Veiligheidsraad in totaal?', 'Hoeveel rode kaarten kreeg Zinedine Zidane in WK-finales?', 'Hoeveel poten heeft een kreeftachtige van de orde Isopoda?', 15, 1, 14, '−', '2026-09-26', 'scheduled', 'library-015'),  -- Politiek en recht / Sport / Dieren
    ('Hoeveel boeken bevat de protestantse Bijbel?', 'Hoeveel landen grenzen aan de Rode Zee?', 'Hoeveel films regisseerde Christopher Nolan vóór Oppenheimer?', 66, 6, 11, '÷', '2026-09-27', 'scheduled', 'library-054'),  -- Boeken en literatuur / Geografie / Films en series
    ('Hoeveel leden heeft de G7?', 'Hoeveel nationale talen heeft Zuid-Afrika volgens de grondwet?', 'Hoeveel centimeter hoog is de Mona Lisa?', 7, 11, 77, '×', '2026-09-28', 'scheduled', 'library-043'),  -- Economie & geld / Taal / Kunst en cultuur
    ('Hoeveel zuilen kent de islam?', 'Hoeveel torens heeft de Sagrada Família volgens het voltooide ontwerp?', 'Hoeveel nummers bevatte het album Un Verano Sin Ti van Bad Bunny?', 5, 18, 23, '+', '2026-09-29', 'scheduled', 'library-035'),  -- Filosofie, psychologie en religie / Gebouwen en infrastructuur / Muziek
    ('Hoeveel landen hadden de euro als officiële munt bij de introductie van contant eurogeld?', 'Hoeveel verschillende uitkomsten heeft het gooien met twee gewone dobbelstenen?', 'Hoeveel shotjes espresso zitten er in een cappuccino?', 12, 11, 1, '−', '2026-09-30', 'scheduled', 'library-017'),  -- Economie & geld / Wiskunde / Eten & drinken
    ('Hoeveel componenten telt het UNESCO-deel van de Neder-Germaanse Limes?', 'Hoeveel wielen heeft een tuk-tuk meestal?', 'Hoeveel oorspronkelijke meetpunten van de Struve-geodetische boog zijn als UNESCO-onderdeel opgenomen?', 102, 3, 34, '÷', '2026-10-01', 'scheduled', 'library-058'),  -- Geschiedenis / Vervoer / Geografie
    ('Hoeveel gewesten heeft België?', 'Hoeveel gram koolhydraten bevat een Amerikaanse McDonald’s cheeseburger?', 'Hoeveel meter hoog is het Vrijheidsbeeld inclusief voetstuk?', 3, 31, 93, '×', '2026-10-02', 'scheduled', 'library-048'),  -- Geografie / Eten & drinken / Gebouwen en infrastructuur
    ('Hoeveel domeinen noemt UNESCO voor immaterieel cultureel erfgoed?', 'Hoeveel stukken heeft iedere speler bij de start van schaken?', 'Hoe hoog was de hoogste zandsculptuur ooit in meters?', 5, 16, 21, '+', '2026-10-03', 'scheduled', 'library-036'),  -- Kunst en cultuur / Spellen en speelgoed / Records en vergelijkingen
    ('Hoeveel zijden heeft een octagoon?', 'Hoeveel snaren heeft een standaard elektrische gitaar?', 'Hoeveel natuurlijke manen heeft Mars?', 8, 6, 2, '−', '2026-10-04', 'scheduled', 'library-018'),  -- Wiskunde / Muziek / Sterrenkunde & ruimte
    ('Wat is de hoogte van het Vrijheidsbeeld in New York inclusief sokkel in meters?', 'Hoeveel staten telt Mexico?', 'Hoeveel poten heeft een standaard statief?', 93, 31, 3, '÷', '2026-10-05', 'scheduled', 'library-059'),  -- Gebouwen en infrastructuur / Geografie / Dagelijks leven
    ('Hoeveel landen vormen het Verenigd Koninkrijk?', 'Hoeveel tanden heeft een volwassen mens normaal?', 'Hoeveel verdiepingen heeft de Shanghai Tower?', 4, 32, 128, '×', '2026-10-06', 'scheduled', 'library-051')  -- Geografie / Biologie & gezondheid / Gebouwen en infrastructuur
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
