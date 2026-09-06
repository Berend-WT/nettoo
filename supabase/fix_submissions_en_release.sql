-- Netto — inzendingen repareren en de daily om 12:00 Londense tijd vrijgeven
--
-- UITVOEREN
-- Supabase dashboard -> SQL Editor -> plak dit -> Run. Veilig om te herhalen.

-- ============================================================
-- 1. Inzendingen: oude verplichte kolommen weghalen
-- ============================================================
--
-- Een inzending versturen gaf:
--   null value in column "question_1" of relation "question_submissions"
--   violates not-null constraint
--
-- De tabel draagt nog kolommen mee uit een eerdere opzet: question_1,
-- question_2, proposed_answer_1, proposed_answer_2 en submitted_by. Die zijn
-- NOT NULL, terwijl de app allang de nieuwe kolommen vult (q1, a1, q2, a2, q3,
-- a3, note, username). Elke insert stuit dus op question_1.
--
-- Zelfde oorzaak als de eerdere uuid-verwarring: schema.sql gebruikt
-- "create table if not exists", de tabel bestond al in de oude vorm, en het
-- defensieve blok daaronder voegt alleen ontbrekende kolommen toe — het haalt
-- verouderde kolommen nooit weg en versoepelt hun NOT NULL niet.
--
-- Weghalen kan veilig: geen enkele regel code in de repo verwijst er nog naar
-- (gecontroleerd op js, html, py en sql), en de tabel bevat nul rijen.

alter table public.question_submissions drop column if exists question_1;
alter table public.question_submissions drop column if exists question_2;
alter table public.question_submissions drop column if exists proposed_answer_1;
alter table public.question_submissions drop column if exists proposed_answer_2;
alter table public.question_submissions drop column if exists submitted_by;

-- q1 is de enige vraag die altijd gevuld moet zijn; de rest hoort optioneel te
-- blijven, want bij type='vraag' stuurt de speler alleen die ene vraag in.
alter table public.question_submissions alter column q1 set not null;

-- ============================================================
-- 2. Daily vrijgeven om 12:00 Londense tijd
-- ============================================================
--
-- De policy liet dailies zien zodra scheduled_date <= current_date, oftewel om
-- middernacht UTC. Gewenst is 12:00 in Londen.
--
-- Twaalf uur terugrekenen vanaf de Londense klok geeft precies dat omslagpunt:
--   07 sep 11:59 Londen  ->  -12u  ->  06 sep 23:59  ->  datum 06 sep
--   07 sep 12:00 Londen  ->  -12u  ->  07 sep 00:00  ->  datum 07 sep
--
-- Door de Londense zone te gebruiken in plaats van een vaste offset klopt dit
-- vanzelf rond zomer- en wintertijd; Londen zit 's zomers op UTC+1.

drop policy if exists puzzles_select_published on public.puzzles;

create policy puzzles_select_published
  on public.puzzles for select
  to anon, authenticated
  using (
    status = 'scheduled'
    and scheduled_date <= ((now() at time zone 'Europe/London') - interval '12 hours')::date
  );

-- ============================================================
-- Controle achteraf
-- ============================================================
-- Verwacht: de oude kolommen bestaan niet meer.
-- select column_name from information_schema.columns
--  where table_schema='public' and table_name='question_submissions'
--  order by column_name;
--
-- Verwacht: het huidige omslagpunt, en welke datum daarmee vrij is.
-- select (now() at time zone 'Europe/London') as londense_tijd,
--        ((now() at time zone 'Europe/London') - interval '12 hours')::date as vrijgegeven_tot;
