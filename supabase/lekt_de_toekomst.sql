-- Netto — de twee vragen die na de security advisor nog openstaan
--
-- UITVOEREN
-- SQL Editor -> plak dit -> Run -> plak de uitvoer terug. Leest alleen,
-- verandert niets.
--
-- WAT DE ADVISOR AL BEVESTIGD HEEFT
-- `puzzles_public` is een SECURITY DEFINER view. Die draait met de rechten van
-- zijn maker, niet van de lezer, dus de row level security op `puzzles` geldt
-- niet voor wie de view opvraagt. En aan `anon` geeft hij rijen terug met
-- status 'scheduled'.
--
-- Wat we nog niet weten is het enige dat telt: zitten daar ook rijen bij met
-- een datum in de toekomst? Er staan dertig dagpuzzels vooruit ingepland.
-- Zo ja, dan kan iedere bezoeker de vragen van morgen ophalen, en bij een
-- schatspel met een leaderboard is dat het verschil tussen schatten en weten.
-- De antwoorden hoeven niet te lekken; de vraag opzoeken kan iedereen.

-- ============================================================
-- 1. De beslissende vraag
-- ============================================================
-- Komt hier iets terug, dan moet de view een datumfilter krijgen.
-- Blijft het leeg, dan is er niets aan de hand en kan C-008 dicht.

set local role anon;
select scheduled_date, status, question_1
from public.puzzles_public
where scheduled_date > current_date
order by scheduled_date
limit 10;
reset role;

-- ============================================================
-- 2. Wat is rls_auto_enable()?
-- ============================================================
-- Deze functie staat in geen enkel bestand van deze repo. Hij is SECURITY
-- DEFINER en uitvoerbaar door `anon`, dus door iedereen die het adres van je
-- project kent, zonder in te loggen. De naam suggereert dat hij row level
-- security aanzet.
--
-- Draait hij als eigenaar en kan iedereen hem aanroepen, dan is de vraag wat
-- hij precies doet — en of hij ook iets kan uitzetten. Dat wil ik lezen
-- voordat ik er iets over zeg.

select p.proname                        as functie,
       pg_get_functiondef(p.oid)        as definitie
from pg_proc p
join pg_namespace n on n.oid = p.pronamespace
where n.nspname = 'public'
  and p.proname = 'rls_auto_enable';

-- ============================================================
-- 3. De definitie van de view, voor de reparatie
-- ============================================================
select pg_get_viewdef('public.puzzles_public'::regclass, true) as definitie;
