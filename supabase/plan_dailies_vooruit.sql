-- Netto — dailies inplannen voor de komende dagen
--
-- GEGENEREERD door een eenmalig script; hierna gaat inplannen via het
-- adminpaneel ("Volgende daily samenstellen").
--
-- WAAROM
-- Het archief liep tot 4 september, maar het is inmiddels 6 september. De
-- frontend toonde daardoor de daily van de 4e alsof het die van vandaag was, en
-- js/core.js slaat een score alleen op wanneer de gespeelde puzzel exact de
-- daily van vandaag is. Gevolg: spelen leverde niets op en het leaderboard bleef
-- leeg. Dit vult het gat en geeft ruim een week voorsprong.
--
-- Gekozen uit library-puzzels die nog niet als daily zijn gebruikt, met drie
-- verschillende categorieën per puzzel en gespreid over de vier bewerkingen.
--
-- UITVOEREN
-- Supabase dashboard -> SQL Editor -> plak dit -> Run. Bezette datums worden
-- overgeslagen, dus opnieuw draaien kan geen kwaad.


insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel soldaten telde het leger van Napoleon tijdens de invasie van Rusland?', 'Hoeveel centimeter meten de dunne en dikke darm samen, volledig uitgestrekt?', 'Hoeveel officiële inwoners heeft Vaticaanstad?', 600000, 750, 800, '÷', '2026-09-05', 'scheduled', 'library-122'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-05');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel seizoenen heeft The Sopranos?', 'Hoeveel spelers staan er tegelijk op het veld bij een honkbalwedstrijd?', 'Hoeveel graden is elke binnenhoek van een regelmatige vijfhoek?', 6, 18, 108, '×', '2026-09-06', 'scheduled', 'library-060'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-06');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel boeken bevat The Chronicles of Narnia?', 'Hoeveel lijnen heeft de metro van Londen volgens de klassieke Underground-indeling?', 'Hoeveel groepen heeft het moderne periodiek systeem?', 7, 11, 18, '+', '2026-09-07', 'scheduled', 'library-056'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-07');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel ton bananen worden wereldwijd jaarlijks geproduceerd?', 'Hoeveel mensen namen deel aan de grootste massale yogales?', 'Hoeveel actieve vulkanen zijn er op aarde naar schatting?', 135000000, 100000, 1350, '÷', '2026-09-08', 'scheduled', 'library-140'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-08');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel deelstaten (Bundesländer) telt Duitsland?', 'Hoeveel verdiepingen heeft het Empire State Building?', 'Hoeveel jaar duurden de Punische oorlogen samen?', 16, 102, 118, '+', '2026-09-09', 'scheduled', 'library-129'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-09');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel kilogram weegt de Great Bell, de grote klok van Big Ben?', 'Hoeveel watt laadt een standaard iPhone snellader?', 'Hoeveel kilometer lang is de langste grot ter wereld, Mammoth Cave, ongeveer?', 13700, 20, 685, '÷', '2026-09-10', 'scheduled', 'library-123'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-10');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel landen liggen op het Iberisch Schiereiland?', 'Hoeveel landen ondertekenden de UNESCO-grondwet in 1945?', 'Hoeveel artikelen bevat het Handvest van de Verenigde Naties?', 3, 37, 111, '×', '2026-09-11', 'scheduled', 'library-075'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-11');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel vierkante kilometer is Antarctica ongeveer groot?', 'Hoeveel haren heeft een mens gemiddeld op zijn hoofd (afgerond)?', 'Hoeveel artikelen bevat de Nederlandse Grondwet?', 14200000, 100000, 142, '÷', '2026-09-12', 'scheduled', 'library-120'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-12');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'In welk jaar eindigde de Tweede Wereldoorlog in Europa?', 'In welk jaar werd de eerste volledige kaart van de wereldbol gemaakt?', 'Hoeveel piercings had de persoon met de meeste piercings ooit?', 1945, 1492, 453, '−', '2026-09-13', 'scheduled', 'library-156'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-13');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel officiële ringen heeft Uranus?', 'Hoeveel wielen heeft een Boeing 747 volgens de standaardconfiguratie?', 'Hoeveel procent van het landoppervlak van de aarde is bedekt met bos?', 13, 18, 31, '+', '2026-09-14', 'scheduled', 'library-187'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-14');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel gewesten heeft België?', 'Hoeveel gram koolhydraten bevat een Amerikaanse McDonald’s cheeseburger?', 'Hoeveel meter hoog is het Vrijheidsbeeld inclusief voetstuk?', 3, 31, 93, '×', '2026-09-15', 'scheduled', 'library-048'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-15');

insert into public.puzzles (question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, operator, scheduled_date, status, source_library_id)
select 'Hoeveel bekende manen heeft de planeet Jupiter officieel?', 'Hoeveel kilometer lang is de Grand Canyon ongeveer?', 'Hoeveel meter hoog is One World Trade Center?', 95, 446, 541, '+', '2026-09-16', 'scheduled', 'library-174'
where not exists (select 1 from public.puzzles where scheduled_date = '2026-09-16');


-- Controle: verwacht een reeks zonder gaten tot en met 2026-09-16.
-- select scheduled_date, question_1 from public.puzzles order by scheduled_date desc limit 15;
