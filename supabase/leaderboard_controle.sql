-- Netto — controleer in één keer of het leaderboard écht kan werken
--
-- UITVOEREN
-- Supabase dashboard -> SQL Editor -> plak dit -> Run. Veilig om te herhalen.
--
-- WAAROM DIT BESTAND ER IS
-- Het leaderboard hangt aan vijf dingen die in vier eerdere SQL-bestanden zijn
-- verspreid: de tabel, de policies, de grants, de unieke index en de twee
-- functies. Is er ooit één van die bestanden niet gedraaid, dan blijft het
-- scorebord leeg zonder te zeggen waarom — de frontend krijgt gewoon een lege
-- lijst terug, precies zoals wanneer er nog niemand gespeeld heeft.
--
-- Dit bestand zet alles wat ontbreekt alsnog neer en eindigt met een rapport
-- dat per onderdeel zegt of het er is.

-- ============================================================
-- 1. Kan een speler zijn eigen score wegschrijven?
-- ============================================================
alter table public.user_plays enable row level security;

drop policy if exists user_plays_select_own on public.user_plays;
drop policy if exists user_plays_insert_own on public.user_plays;
drop policy if exists user_plays_update_own on public.user_plays;

create policy user_plays_select_own on public.user_plays
  for select using (auth.uid() = user_id);
create policy user_plays_insert_own on public.user_plays
  for insert with check (auth.uid() = user_id);
create policy user_plays_update_own on public.user_plays
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

grant select, insert, update on public.user_plays to authenticated;

-- Zonder deze index doet de upsert uit de frontend niets: PostgREST heeft een
-- unieke sleutel nodig om "bestaat al" van "nieuw" te onderscheiden.
create unique index if not exists user_plays_user_date_uniq
  on public.user_plays (user_id, puzzle_date);

-- ============================================================
-- 2. De twee functies achter het scorebord
-- ============================================================
-- Ze draaien met security definer omdat de policies hierboven een speler
-- alleen zijn eigen rijen laten zien, en dat hoort zo te blijven. Wat ze
-- teruggeven is precies wat op een scorebord thuishoort: een naam en een
-- score. Geen e-mailadressen, geen schattingen van andere spelers.

create or replace function public.leaderboard_dag(p_datum date)
returns table (naam text, factor numeric)
language sql security definer stable set search_path = public as $$
  select p.username, up.factor
  from public.user_plays up
  join public.profiles p on p.id = up.user_id
  where up.puzzle_date = p_datum
  order by up.factor asc, p.username asc
  limit 50;
$$;

create or replace function public.leaderboard_streaks(p_datum date)
returns table (naam text, streak integer)
language sql security definer stable set search_path = public as $$
  with genummerd as (
    select user_id, puzzle_date,
           puzzle_date - (row_number() over (
             partition by user_id order by puzzle_date
           ))::int as groep
    from public.user_plays
  ),
  reeksen as (
    select user_id, count(*)::int as lengte, max(puzzle_date) as laatste
    from genummerd
    group by user_id, groep
  ),
  lopend as (
    select user_id, max(lengte) as lengte
    from reeksen
    where laatste >= p_datum - 1
    group by user_id
  )
  select p.username, l.lengte
  from lopend l
  join public.profiles p on p.id = l.user_id
  order by l.lengte desc, p.username asc
  limit 50;
$$;

grant execute on function public.leaderboard_dag(date) to anon, authenticated;
grant execute on function public.leaderboard_streaks(date) to anon, authenticated;

-- ============================================================
-- 3. Rapport
-- ============================================================
-- Alles moet "ja" zeggen. Staat er ergens "NEE", dan is dat het onderdeel dat
-- het scorebord leeg houdt.
select 'tabel user_plays bestaat' as onderdeel,
       case when to_regclass('public.user_plays') is not null
            then 'ja' else 'NEE' end as status
union all
select 'unieke index op (user_id, puzzle_date)',
       case when exists (select 1 from pg_indexes
                         where schemaname = 'public'
                           and indexname = 'user_plays_user_date_uniq')
            then 'ja' else 'NEE' end
union all
select 'policies op user_plays (3 verwacht)',
       coalesce((select count(*)::text from pg_policies
                 where schemaname = 'public' and tablename = 'user_plays'), '0')
union all
select 'functie leaderboard_dag',
       case when to_regprocedure('public.leaderboard_dag(date)') is not null
            then 'ja' else 'NEE' end
union all
select 'functie leaderboard_streaks',
       case when to_regprocedure('public.leaderboard_streaks(date)') is not null
            then 'ja' else 'NEE' end
union all
select 'trigger die een profiel aanmaakt bij registratie',
       case when exists (select 1 from pg_trigger
                         where tgname = 'on_auth_user_created')
            then 'ja' else 'NEE — zonder dit heeft niemand een naam' end
union all
select 'aantal accounts', (select count(*)::text from auth.users)
union all
select 'aantal profielen', (select count(*)::text from public.profiles)
union all
select 'aantal ingediende dagscores', (select count(*)::text from public.user_plays)
union all
select 'scores voor vandaag',
       (select count(*)::text from public.user_plays where puzzle_date = current_date);
