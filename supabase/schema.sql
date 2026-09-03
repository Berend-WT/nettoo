-- ============================================================
-- Netto — Supabase schema (volledig, idempotent)
-- Run in: Supabase Dashboard → SQL Editor → New query
-- Je mag dit bestand meerdere keren draaien; elke stap is
-- "if not exists" / "drop if exists" en herstelt oude tabellen.
-- ============================================================

-- 1) Archive plays: server-side history for Daily Archive puzzles
--    Raw guesses are stored (not scores) so factors can be re-verified.
create table if not exists public.archive_plays (
  user_id      uuid not null references auth.users(id) on delete cascade,
  puzzle_no    int  not null,
  g1           int,
  g2           int,
  g3           int,
  factor       numeric,
  completed_at timestamptz not null default now(),
  primary key (user_id, puzzle_no)
);

alter table public.archive_plays enable row level security;

drop policy if exists archive_plays_select_own on public.archive_plays;
drop policy if exists archive_plays_insert_own on public.archive_plays;
drop policy if exists archive_plays_update_own on public.archive_plays;
create policy "archive_plays_select_own" on public.archive_plays
  for select using (auth.uid() = user_id);
create policy "archive_plays_insert_own" on public.archive_plays
  for insert with check (auth.uid() = user_id);
create policy "archive_plays_update_own" on public.archive_plays
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- 2) Profiles: premium flag with expiry date (Stripe-ready later —
--    Stripe webhooks will only need to update premium_until).
create table if not exists public.profiles (
  id            uuid primary key references auth.users(id) on delete cascade,
  username      text,
  premium_until date,               -- null = no premium; future date = active
  created_at    timestamptz not null default now()
);

alter table public.profiles enable row level security;

drop policy if exists profiles_select_own on public.profiles;
drop policy if exists profiles_insert_own on public.profiles;
drop policy if exists profiles_update_own on public.profiles;
create policy "profiles_select_own" on public.profiles
  for select using (auth.uid() = id);
create policy "profiles_insert_own" on public.profiles
  for insert with check (auth.uid() = id);
create policy "profiles_update_own" on public.profiles
  for update using (auth.uid() = id) with check (auth.uid() = id);

-- Auto-create a profile row for every new signup
create or replace function public.handle_new_user()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  insert into public.profiles (id, username)
  values (new.id, new.raw_user_meta_data->>'username')
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ============================================================
-- 3) ADMIN-FUNDAMENT (moet vóór de policies: is_admin() wordt
--    daarin gebruikt)
-- ============================================================
create table if not exists public.admin_users (
  user_id uuid primary key references auth.users(id) on delete cascade
);

create or replace function public.is_admin()
returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.admin_users where user_id = auth.uid());
$$;

-- Jezelf admin maken (pas het e-mailadres aan en draai los):
--   insert into public.admin_users (user_id)
--   select id from auth.users where email = 'jij@voorbeeld.nl';

-- ============================================================
-- 4) Question submissions: spelers sturen een losse vraag
--    (antwoord optioneel) óf een complete puzzel in.
--    type='vraag'  -> q1/a1 gevuld, rest NULL (a1 mag NULL zijn)
--    type='puzzel' -> q1..a3 + operator gevuld
-- ============================================================
create table if not exists public.question_submissions (
  id           bigserial primary key,
  type         text not null default 'vraag',
  q1           text not null,
  a1           numeric,
  q2           text,
  a2           numeric,
  q3           text,
  a3           numeric,
  operator     text,
  note         text,                    -- optionele toelichting/bron van de speler
  username     text,                    -- credits: spelersnaam zoals getoond in het spel
  email        text,                    -- verouderd: alleen nog door oude rijen gevuld
  user_id      uuid references auth.users(id) on delete cascade,
  status       text not null default 'nieuw',
  reviewed_at  timestamptz,
  created_at   timestamptz not null default now()
);

-- Defensieve migratie: werkt ongeacht de vorm van een eventueel al
-- bestaande tabel. Elke ontbrekende kolom wordt toegevoegd en oude
-- NOT NULL-eisen (a1..a3 waren ooit verplicht) worden weggehaald.
do $$
declare
  col record;
begin
  for col in
    select * from (values
      ('type',        'text not null default ''vraag'''),
      ('q1',          'text'),
      ('a1',          'numeric'),
      ('q2',          'text'),
      ('a2',          'numeric'),
      ('q3',          'text'),
      ('a3',          'numeric'),
      ('operator',    'text'),
      ('note',        'text'),
      ('username',    'text'),
      ('email',       'text'),
      ('user_id',     'uuid references auth.users(id) on delete cascade'),
      ('status',      'text not null default ''nieuw'''),
      ('reviewed_at', 'timestamptz'),
      ('created_at',  'timestamptz not null default now()')
    ) as t(name, def)
  loop
    if not exists (
      select 1 from information_schema.columns
      where table_schema = 'public'
        and table_name = 'question_submissions'
        and lower(column_name) = col.name
    ) then
      execute format('alter table public.question_submissions add column %I %s', col.name, col.def);
    end if;
  end loop;

  -- oude verplichte velden soepel maken (vraag-antwoord is optioneel)
  execute 'alter table public.question_submissions alter column a1 drop not null';
  execute 'alter table public.question_submissions alter column a2 drop not null';
  execute 'alter table public.question_submissions alter column a3 drop not null';
  execute 'alter table public.question_submissions alter column q2 drop not null';
  execute 'alter table public.question_submissions alter column q3 drop not null';
  execute 'alter table public.question_submissions alter column operator drop not null';
  execute 'alter table public.question_submissions alter column operator drop default';
  execute 'alter table public.question_submissions alter column user_id drop not null';
end $$;

alter table public.question_submissions enable row level security;

drop policy if exists question_submissions_insert_anyone on public.question_submissions;
drop policy if exists question_submissions_insert_own on public.question_submissions;
drop policy if exists question_submissions_select_own on public.question_submissions;
drop policy if exists question_submissions_select_admin on public.question_submissions;
drop policy if exists question_submissions_update_admin on public.question_submissions;
create policy "question_submissions_insert_own" on public.question_submissions
  for insert with check (auth.uid() = user_id);
create policy "question_submissions_select_own" on public.question_submissions
  for select using (auth.uid() = user_id);
create policy "question_submissions_select_admin" on public.question_submissions
  for select using (public.is_admin());
create policy "question_submissions_update_admin" on public.question_submissions
  for update using (public.is_admin()) with check (public.is_admin());

-- ============================================================
-- 5) Notifications: de speler krijgt hier een melding wanneer
--    zijn inzending is beoordeeld. De app toont ze als toast.
-- ============================================================
create table if not exists public.user_notifications (
  id         bigserial primary key,
  user_id    uuid not null references auth.users(id) on delete cascade,
  type       text not null default 'info',
  message    text not null,
  read       boolean not null default false,
  created_at timestamptz not null default now()
);
alter table public.user_notifications enable row level security;

drop policy if exists notifications_select_own on public.user_notifications;
drop policy if exists notifications_update_own on public.user_notifications;
drop policy if exists notifications_insert_admin on public.user_notifications;
create policy "notifications_select_own" on public.user_notifications
  for select using (auth.uid() = user_id);
create policy "notifications_update_own" on public.user_notifications
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "notifications_insert_admin" on public.user_notifications
  for insert with check (public.is_admin());

-- ============================================================
-- 6) Review-RPC: de enige route om een inzending te beoordelen.
--    Alleen admins; de melding voor de speler wordt hier
--    server-side gegenereerd.
-- ============================================================
create or replace function public.admin_review_submission(
  p_id     bigint,
  p_status text,
  p_message text default null
)
returns void language plpgsql security definer set search_path = public as $$
declare
  v_user_id uuid;
  v_type    text;
  v_q1      text;
  v_kort    text;
begin
  if not public.is_admin() then
    raise exception 'Geen admin-rechten';
  end if;
  if p_status not in ('geaccepteerd','geweigerd') then
    raise exception 'Ongeldige status';
  end if;
  select user_id, type, q1 into v_user_id, v_type, v_q1
    from public.question_submissions where id = p_id;
  if v_user_id is null then
    raise exception 'Inzending niet gevonden';
  end if;
  update public.question_submissions
     set status = p_status, reviewed_at = now()
   where id = p_id;
  v_kort := left(coalesce(v_q1, '?'), 70);
  insert into public.user_notifications (user_id, type, message)
  values (
    v_user_id,
    case when p_status = 'geaccepteerd' then 'submission_accepted' else 'submission_denied' end,
    case
      when p_status = 'geaccepteerd' then
        'Je ' || (case when v_type = 'puzzel' then 'puzzel' else 'vraag' end)
          || ' "' || v_kort || '" is geaccepteerd! We gebruiken hem misschien in een toekomstige daily of puzzel. 🎉'
      else
        'Je ' || (case when v_type = 'puzzel' then 'puzzel' else 'vraag' end)
          || ' "' || v_kort || '" is deze keer niet geaccepteerd. Bedankt voor je inzending — blijf insturen!'
    end
  );
end;
$$;
