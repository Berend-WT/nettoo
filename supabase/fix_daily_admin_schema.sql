-- Netto — schema klaarmaken voor het admin-scherm "volgende daily samenstellen"
--
-- Twee losse problemen, allebei nodig voordat het adminscherm zin heeft.
--
-- PROBLEEM 1: statuswaarden lopen uit de pas
-- schema.sql en de RPC admin_review_submission gebruiken nieuw/geaccepteerd/
-- geweigerd, maar de live tabel heeft nog de oudere check-constraint met
-- pending/approved/rejected en default 'pending'. Gevolg: het "nieuw"-filter
-- in de admin toont niets, en op Accepteren klikken loopt op een
-- constraint-fout omdat 'geaccepteerd' niet is toegestaan.
--
-- PROBLEEM 2: de puzzles-tabel kan geen volledige daily opslaan
-- Elke puzzel heeft drie vraagteksten (zie puzzles_embedded.js: q1/q2/q3),
-- maar de tabel heeft alleen question_1 en question_2 naast drie antwoorden.
-- De derde vraag zou dus verloren gaan bij het inplannen.
--
-- UITVOEREN
-- Supabase dashboard -> SQL Editor -> plak dit -> Run.
-- Veilig om opnieuw te draaien.

-- ============================================================
-- 1. question_submissions: statuswaarden gelijktrekken
-- ============================================================

-- De check-constraint heet niet overal hetzelfde, dus opzoeken in plaats van
-- gokken. Alle check-constraints op deze tabel die over status gaan, eraf.
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
      and rel.relname = 'question_submissions'
      and con.contype = 'c'
      and pg_get_constraintdef(con.oid) ilike '%status%'
  loop
    execute format('alter table public.question_submissions drop constraint %I', c.conname);
  end loop;
end $$;

-- Bestaande rijen omzetten naar de waarden die de app gebruikt.
update public.question_submissions set status = 'nieuw'         where status = 'pending';
update public.question_submissions set status = 'geaccepteerd'  where status = 'approved';
update public.question_submissions set status = 'geweigerd'     where status = 'rejected';

alter table public.question_submissions alter column status set default 'nieuw';

alter table public.question_submissions
  add constraint question_submissions_status_check
  check (status in ('nieuw', 'geaccepteerd', 'geweigerd'));

-- ============================================================
-- 2. puzzles: derde vraagtekst + herkomst van de puzzel
-- ============================================================

-- question_3 ontbrak; zonder deze kolom verliest een ingeplande daily zijn
-- derde vraag.
alter table public.puzzles add column if not exists question_3 text;

-- Bijhouden waar een daily vandaan komt, zodat het adminscherm kan filteren op
-- "nog niet als daily gebruikt" en kan tonen of iets van een speler kwam.
alter table public.puzzles add column if not exists source_library_id text;
alter table public.puzzles add column if not exists source_submission_id bigint
  references public.question_submissions(id) on delete set null;

-- Twee dailies op dezelfde datum inplannen moet niet kunnen. scheduled_date is
-- al unique volgens het schema; deze index is een no-op als dat klopt.
create unique index if not exists puzzles_scheduled_date_uniq
  on public.puzzles (scheduled_date)
  where scheduled_date is not null;

-- Het adminscherm filtert veel op status en datum.
create index if not exists puzzles_status_date_idx
  on public.puzzles (status, scheduled_date);

-- ============================================================
-- Controle achteraf
-- ============================================================
-- Verwacht: nieuw/geaccepteerd/geweigerd, en question_3 aanwezig.
--
-- select pg_get_constraintdef(oid)
--   from pg_constraint
--  where conname = 'question_submissions_status_check';
--
-- select column_name from information_schema.columns
--  where table_schema = 'public' and table_name = 'puzzles'
--    and column_name in ('question_3','source_library_id','source_submission_id');
--
-- select status, count(*) from public.question_submissions group by status;
