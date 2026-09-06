-- Netto — echt leaderboard en registratie die niet breekt op een dubbele naam
--
-- UITVOEREN
-- Supabase dashboard -> SQL Editor -> plak dit -> Run. Veilig om te herhalen.

-- ============================================================
-- 1. Registreren brak bij een dubbele spelersnaam
-- ============================================================
--
-- Vult iemand geen naam in, dan pakt de frontend het deel vóór de @ uit het
-- e-mailadres. profiles.username is uniek, en handle_new_user ving alleen een
-- dubbele id af ("on conflict (id) do nothing"), niet een dubbele naam. Twee
-- mensen met info@ als voorvoegsel, of twee die allebei "Berend" kiezen, en de
-- tweede kon niet registreren — met een databasefout in plaats van een nette
-- melding, want de fout ontstond ín de trigger.
--
-- De frontend controleert nu vooraf of een naam vrij is. Deze trigger is het
-- vangnet voor het geval twee mensen tegelijk registreren: dan krijgt de
-- tweede er een cijfer achter in plaats van een mislukte registratie.

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

  -- Bezet? Dan een cijfer erachter tot het lukt. Tien pogingen is ruim; daarna
  -- valt hij terug op iets wat gegarandeerd uniek is.
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

-- Vooraf kunnen controleren of een naam vrij is, zonder profiles open te zetten:
-- deze functie geeft alleen ja of nee terug, geen enkele rij.
create or replace function public.username_beschikbaar(p_naam text)
returns boolean language sql security definer stable set search_path = public as $$
  select not exists (
    select 1 from public.profiles where lower(username) = lower(trim(p_naam))
  );
$$;

grant execute on function public.username_beschikbaar(text) to anon, authenticated;

-- ============================================================
-- 2. Een leaderboard met echte spelers
-- ============================================================
--
-- Het leaderboard toonde verzonnen namen ("WiskundeKoning", "StatistiekNL")
-- terwijl het inlogscherm belooft dat je erop komt te staan.
--
-- Een gewone query kan dit niet leveren: de policies op user_plays en profiles
-- laten een speler alleen zijn eigen rijen zien, en dat hoort zo te blijven.
-- Deze twee functies draaien daarom met security definer en geven uitsluitend
-- terug wat op een scorebord thuishoort: een naam en een score. Geen
-- e-mailadressen, geen ingevulde schattingen van andere spelers.

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

-- Streaks worden hier uit de daadwerkelijke plays berekend en niet uit
-- profiles.current_streak: die kolom wordt door de app nooit gevuld, en een
-- streak die de client aanlevert is te vervalsen door localStorage aan te
-- passen. Uit de speeldata afgeleid kan dat niet.
create or replace function public.leaderboard_streaks(p_datum date)
returns table (naam text, streak integer)
language sql security definer stable set search_path = public as $$
  with genummerd as (
    -- Opeenvolgende speeldagen krijgen dezelfde groepswaarde: datum minus het
    -- rangnummer blijft gelijk zolang er geen dag ontbreekt.
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
    -- Alleen reeksen die nog leven: vandaag gespeeld, of gisteren en vandaag
    -- nog niet.
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
-- Controle achteraf
-- ============================================================
-- select public.username_beschikbaar('Berend');
-- select * from public.leaderboard_dag(current_date);
-- select * from public.leaderboard_streaks(current_date);
