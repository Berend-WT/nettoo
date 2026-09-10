-- Netto — zorg dat het leaderboard mensen laat zien, en geef ze een keuze
--
-- UITVOEREN
-- Supabase dashboard -> SQL Editor -> plak dit -> Run. Veilig om te herhalen.
-- Onderaan staat een rapport; plak dat terug.
--
-- HET PROBLEEM
-- Ingelogd, de daily gespeeld, en toch niet op het scorebord. De functies zelf
-- werken (ze geven netjes 200 terug), maar leveren nul rijen.
--
-- Er zijn twee plekken waar iemand tussen wal en schip valt:
--
--   1. Er staat niets in user_plays. Dan is de score nooit weggeschreven.
--   2. Er staat wél iets in user_plays, maar niets in profiles. De functie
--      koppelt die twee met een gewone join, en een join zonder tegenhanger
--      laat de rij vallen. Zonder profielrij heb je geen naam, en zonder naam
--      sta je nergens.
--
-- Geval 2 is het waarschijnlijkst: profiles wordt gevuld door een trigger op
-- auth.users, en wie zich registreerde voordat die trigger bestond, of toen hij
-- faalde, heeft er geen. Dat merk je nergens aan — tot je op het scorebord
-- zoekt en jezelf niet ziet.
--
-- Deel 3 hieronder maakt de ontbrekende profielen alsnog aan.

-- ============================================================
-- 1. Zichtbaarheid: standaard aan, maar uit te zetten
-- ============================================================
-- Je hoort mee te doen zonder erom te vragen, en eruit te kunnen zonder het
-- spel te verlaten. Vandaar default true.

alter table public.profiles
  add column if not exists leaderboard_zichtbaar boolean not null default true;

-- ============================================================
-- 2. De trigger die profielen aanmaakt
-- ============================================================
-- Opnieuw neerzetten, zodat we zeker weten dat hij bestaat en aan auth.users
-- hangt. Zonder deze trigger begint het probleem meteen weer bij de volgende
-- registratie.

create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
declare
  v_basis text;
  v_naam  text;
  v_poging int := 0;
begin
  v_basis := nullif(trim(new.raw_user_meta_data->>'username'), '');
  v_basis := coalesce(v_basis, split_part(new.email, '@', 1), 'speler');
  v_naam := v_basis;
  while exists (select 1 from public.profiles where username = v_naam) loop
    v_poging := v_poging + 1;
    if v_poging > 10 then
      v_naam := v_basis || '-' || substr(new.id::text, 1, 8);
      exit;
    end if;
    v_naam := v_basis || v_poging::text;
  end loop;
  insert into public.profiles (id, username)
  values (new.id, v_naam)
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ============================================================
-- 3. Profielen aanmaken voor wie er nog geen heeft
-- ============================================================
-- Dit is de reparatie voor iedereen die al bestaat. De naam komt uit de
-- metadata van de registratie, en anders uit het deel vóór de @.
-- Botst die naam, dan komt er een cijfer achter.

do $$
declare
  u record;
  v_basis text;
  v_naam  text;
  v_poging int;
begin
  for u in
    select a.id, a.email, a.raw_user_meta_data
    from auth.users a
    left join public.profiles p on p.id = a.id
    where p.id is null
  loop
    v_basis := nullif(trim(u.raw_user_meta_data->>'username'), '');
    v_basis := coalesce(v_basis, split_part(u.email, '@', 1), 'speler');
    v_naam := v_basis;
    v_poging := 0;
    while exists (select 1 from public.profiles where username = v_naam) loop
      v_poging := v_poging + 1;
      if v_poging > 10 then
        v_naam := v_basis || '-' || substr(u.id::text, 1, 8);
        exit;
      end if;
      v_naam := v_basis || v_poging::text;
    end loop;
    insert into public.profiles (id, username) values (u.id, v_naam)
    on conflict (id) do nothing;
  end loop;
end $$;

-- ============================================================
-- 4. De functies: alleen de naam, en alleen wie zichtbaar wil zijn
-- ============================================================
-- Wat eruit komt is een spelersnaam en een score, verder niets. Geen
-- e-mailadres, geen id, geen schattingen van anderen. Wie zichzelf op onzichtbaar
-- zet verdwijnt van de lijst maar speelt gewoon door.

create or replace function public.leaderboard_dag(p_datum date)
returns table (naam text, factor numeric)
language sql security definer stable set search_path = public as $$
  select p.username, up.factor
  from public.user_plays up
  join public.profiles p on p.id = up.user_id
  where up.puzzle_date = p_datum
    and coalesce(p.leaderboard_zichtbaar, true)
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
  where coalesce(p.leaderboard_zichtbaar, true)
  order by l.lengte desc, p.username asc
  limit 50;
$$;

grant execute on function public.leaderboard_dag(date) to anon, authenticated;
grant execute on function public.leaderboard_streaks(date) to anon, authenticated;

-- ============================================================
-- 5. Rapport
-- ============================================================
-- "accounts zonder profiel" hoort 0 te zijn na deel 3.
-- Staat "dagscores" op 0 terwijl je vandaag gespeeld hebt, dan is het geval 1
-- uit de kop: de score is nooit weggeschreven, en dan ligt het aan de frontend
-- of aan de rechten op user_plays.

select 'accounts'                as wat, count(*)::text as waarde from auth.users
union all
select 'profielen',                 count(*)::text from public.profiles
union all
select 'accounts zonder profiel',   count(*)::text
  from auth.users a left join public.profiles p on p.id = a.id where p.id is null
union all
select 'dagscores (alle dagen)',    count(*)::text from public.user_plays
union all
select 'dagscores van vandaag',     count(*)::text
  from public.user_plays where puzzle_date = current_date
union all
select 'scores zonder profiel',     count(*)::text
  from public.user_plays up left join public.profiles p on p.id = up.user_id
  where p.id is null
union all
select 'op het scorebord vandaag',  count(*)::text
  from public.leaderboard_dag(current_date);
