-- Netto - vervang acht dagpuzzels in de database.
--
-- ZES omdat hun som niet meer klopt. De antwoorden in de database liepen
-- achter op de vragenbank: 135.000.000 : 100.984 is geen 1350, en 5 x 163
-- is geen 1056. Alleen het getal bijwerken maakt de puzzel onoplosbaar.
--
-- TWEE omdat hun vraag niet meer in de vragenbank staat (17 en 18 augustus).
-- Die zijn ergens onderweg hernoemd of geschrapt, en wat nergens meer te
-- controleren valt hoort niet in het spel.
--
-- De vervangers komen uit de opnieuw gebouwde set en zijn zo gekozen dat
-- geen van hun vragen al in een andere dagpuzzel staat.

-- 2026-08-04: 272 − 160 = 112  (uit library-003)
update public.puzzles set
  question_1 = 'Hoe lang was de langste man ooit in centimeters?',
  true_answer_1 = 272,
  question_2 = 'Hoeveel kilometer lang is de Betuweroute goederenspoorlijn?',
  true_answer_2 = 160,
  question_3 = 'Hoeveel kaarten bevat een standaard UNO-deck?',
  true_answer_3 = 112,
  operator = '−'
where scheduled_date = '2026-08-04';

-- 2026-08-06: 630 ÷ 90 = 7  (uit library-005)
update public.puzzles set
  question_1 = 'Hoeveel leden telt de Duitse Bondsdag volgens de wettelijke omvang sinds de hervorming?',
  true_answer_1 = 630,
  question_2 = 'Hoeveel kilogram weegt een volwassen mannelijke rode reuzenkangoeroe maximaal?',
  true_answer_2 = 90,
  question_3 = 'Hoeveel gram koffie gebruikt een standaard espresso van 25 ml?',
  true_answer_3 = 7,
  operator = '÷'
where scheduled_date = '2026-08-06';

-- 2026-08-17: 300 × 4000000 = 1200000000  (uit library-012)
update public.puzzles set
  question_1 = 'Hoeveel kilocalorieën bevat een Amerikaanse McDonald’s cheeseburger?',
  true_answer_1 = 300,
  question_2 = 'Hoeveel vierkante kilometer is het Arctische zee-ijs in de zomer ongeveer minimaal?',
  true_answer_2 = 4000000,
  question_3 = 'Hoeveel ton maïs werd wereldwijd geproduceerd in 2023?',
  true_answer_3 = 1200000000,
  operator = '×'
where scheduled_date = '2026-08-17';

-- 2026-08-18: 150000000 ÷ 5000 = 30000  (uit library-013)
update public.puzzles set
  question_1 = 'Wat is de gemiddelde afstand van de aarde tot de zon?',
  true_answer_1 = 150000000,
  question_2 = 'Hoeveel kilometer lang was de Romeinse rijksgrens, de Roman Limes, volgens UNESCO ongeveer?',
  true_answer_2 = 5000,
  question_3 = 'Hoeveel KFC-restaurants zijn er wereldwijd ongeveer?',
  true_answer_3 = 30000,
  operator = '÷'
where scheduled_date = '2026-08-18';

-- 2026-08-20: 1500 + 6000 = 7500  (uit library-006)
update public.puzzles set
  question_1 = 'Hoeveel kilogram weegt een volwassen nijlpaard?',
  true_answer_1 = 1500,
  question_2 = 'Hoeveel schepen ondersteunden de geallieerde landing in Normandië?',
  true_answer_2 = 6000,
  question_3 = 'Hoeveel hotels heeft Hilton wereldwijd ongeveer?',
  true_answer_3 = 7500,
  operator = '+'
where scheduled_date = '2026-08-20';

-- 2026-08-23: 333 × 6 = 1998  (uit library-008)
update public.puzzles set
  question_1 = 'Hoeveel meter hoog is de Tokyo Tower?',
  true_answer_1 = 333,
  question_2 = 'Hoeveel snaren heeft een standaard elektrische gitaar?',
  true_answer_2 = 6,
  question_3 = 'In welk jaar werd Google opgericht?',
  true_answer_3 = 1998,
  operator = '×'
where scheduled_date = '2026-08-23';

-- 2026-09-02: 1950 ÷ 650 = 3  (uit library-009)
update public.puzzles set
  question_1 = 'In welk jaar begon de Koreaanse oorlog?',
  true_answer_1 = 1950,
  question_2 = 'Hoeveel leden telt het Britse House of Commons?',
  true_answer_2 = 650,
  question_3 = 'Hoeveel harten heeft een octopus?',
  true_answer_3 = 3,
  operator = '÷'
where scheduled_date = '2026-09-02';

-- 2026-09-08: 10935 − 1978 = 8957  (uit library-011)
update public.puzzles set
  question_1 = 'Hoeveel meter diep is de Challengerdiepte in de Marianentrog?',
  true_answer_1 = 10935,
  question_2 = 'In welk jaar werd de eerste reageerbuisbaby geboren?',
  true_answer_2 = 1978,
  question_3 = 'Hoeveel mensen deden mee aan het grootste waterballonnengevecht ooit?',
  true_answer_3 = 8957,
  operator = '−'
where scheduled_date = '2026-09-08';

-- Controle achteraf:
-- select scheduled_date, operator, true_answer_1, true_answer_2, true_answer_3
--   from public.puzzles where scheduled_date in ('2026-08-04', '2026-08-06', '2026-08-17', '2026-08-18', '2026-08-20', '2026-08-23', '2026-09-02', '2026-09-08') order by scheduled_date;
