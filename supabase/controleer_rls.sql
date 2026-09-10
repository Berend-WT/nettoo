-- Netto — zet row level security aan waar hij aan hoort, en laat zien wat er staat
--
-- UITVOEREN
-- Supabase dashboard -> SQL Editor -> plak dit -> Run. Veilig om te herhalen.
--
-- WAT ER MIS IS
-- `fix_rls_plays.sql` maakt policies voor user_plays en library_plays, en begint
-- met de zin "Op beide tabellen staat RLS aan". Dat is nooit ergens vastgelegd:
-- geen enkel SQL-bestand zet hem aan voor library_plays. Als hij ook via het
-- dashboard nooit is aangezet, dan doen die policies helemaal niets.
--
-- Een policy zonder RLS is geen halve beveiliging maar geen enkele. Postgres
-- slaat het hele policy-stelsel over en laat de tabelrechten beslissen, en die
-- staan op `grant select, insert, update on public.library_plays to
-- authenticated`. Dat betekent: elke ingelogde speler kan de voortgang van elke
-- andere speler lezen én overschrijven.
--
-- Dit is dezelfde fout als in september met de ontbrekende table-grants, maar
-- omgekeerd: toen was er wel een policy en geen recht, nu wel een recht en geen
-- werkende policy. Beide keren was er niets aan te zien.
--
-- user_plays is hier al mee rechtgezet door leaderboard_controle.sql. Dit
-- bestand doet het voor de rest en, belangrijker, laat zien hoe het er echt
-- voor staat in plaats van het aan te nemen.

-- ============================================================
-- 1. Aanzetten waar hij aan hoort
-- ============================================================
-- Idempotent: al aanstaan is geen fout.

alter table public.user_plays          enable row level security;
alter table public.library_plays       enable row level security;
alter table public.archive_plays       enable row level security;
alter table public.profiles            enable row level security;
alter table public.question_submissions enable row level security;
alter table public.user_notifications  enable row level security;

-- admin_users bepaalt wie het adminpaneel in mag. Er staat een
-- `grant select ... to authenticated` op, en zonder RLS kan dus elke ingelogde
-- speler de lijst met admin-id's uitlezen. Schrijven kan niemand — dat recht is
-- nooit gegeven — dus dit is meelezen, geen binnenkomen. Toch: niemand hoeft
-- deze tabel te kunnen zien.
--
-- admin.html leest hem nu rechtstreeks (`from('admin_users').select(...)`), dus
-- botweg de grant intrekken sluit het adminpaneel buiten. De policy hieronder
-- laat precies één rij door: die van jezelf. Genoeg om te weten of jij admin
-- bent, niet genoeg om te zien wie er nog meer is.
alter table public.admin_users enable row level security;
drop policy if exists admin_users_select_self on public.admin_users;
create policy admin_users_select_self on public.admin_users
  for select using (auth.uid() = user_id);

-- ============================================================
-- 2. Rapport
-- ============================================================
-- Wat je wilt zien: overal rls_aan = true, en policies > 0.
--
-- rls_aan = false met policies > 0 is het gevaarlijke geval: het ziet eruit
-- alsof het dicht zit terwijl alles open staat.
-- rls_aan = true met policies = 0 is het omgekeerde: alles geweigerd, en de
-- app schrijft stil niets meer weg.

select c.relname                                    as tabel,
       c.relrowsecurity                             as rls_aan,
       (select count(*) from pg_policies p
        where p.schemaname = 'public'
          and p.tablename = c.relname)              as policies,
       (select string_agg(distinct privilege_type, ', ' order by privilege_type)
        from information_schema.role_table_grants g
        where g.table_schema = 'public'
          and g.table_name = c.relname
          and g.grantee = 'authenticated')          as rechten_ingelogd,
       (select string_agg(distinct privilege_type, ', ' order by privilege_type)
        from information_schema.role_table_grants g
        where g.table_schema = 'public'
          and g.table_name = c.relname
          and g.grantee = 'anon')                   as rechten_uitgelogd
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public'
  and c.relkind = 'r'
order by c.relrowsecurity, c.relname;
