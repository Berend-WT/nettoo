-- ============================================================
-- Netto — Supabase schema: archive history + profiles (premium)
-- Run this once in: Supabase Dashboard → SQL Editor → New query
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

-- 3) Question submissions: players submit their own fact-trios (no login required,
--    no email link — just a stored row that B-Force reviews in the dashboard).
create table if not exists public.question_submissions (
  id           bigserial primary key,
  q1           text not null,
  a1           numeric not null,
  q2           text not null,
  a2           numeric not null,
  q3           text not null,
  a3           numeric not null,
  operator     text  not null default '×' check (operator in ('×','÷','+','−')),
  note         text,                    -- optionele toelichting/bron van de speler
  email        text,                    -- optioneel, alleen als de speler credits wil
  user_id      uuid references auth.users(id) on delete set null,  -- null = gast
  status       text not null default 'nieuw' check (status in ('nieuw','geaccepteerd','geweigerd')),
  created_at   timestamptz not null default now()
);

alter table public.question_submissions enable row level security;

-- Iedereen (ook gasten) mag insturen; niemand mag andermans inzendingen lezen.
create policy "question_submissions_insert_anyone" on public.question_submissions
  for insert with check (true);
