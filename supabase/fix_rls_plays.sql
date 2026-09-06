-- Netto — ontbrekende RLS-policies voor user_plays en library_plays
--
-- PROBLEEM
-- Op beide tabellen staat RLS aan, maar er bestaat geen enkele policy. In
-- Postgres betekent dat: alles geweigerd. De client schrijft er wel naartoe
-- (js/core.js: de daily-score-upsert en syncLibraryPlay), maar die writes
-- falen stil — de fout wordt alleen als console.warn gelogd.
--
-- GEVOLG
-- Dagelijkse scores en library-voortgang worden niet naar Supabase
-- gesynchroniseerd. De nieuwe Statistieken-modal leest uit deze tabellen en
-- toont daardoor lege/nul-cijfers, ook voor spelers die wel gespeeld hebben.
--
-- OPLOSSING
-- Dezelfde "eigen rij"-policies als archive_plays al heeft: een ingelogde
-- speler mag alleen zijn eigen rijen lezen en schrijven.
--
-- UITVOEREN
-- Supabase dashboard -> SQL Editor -> plak dit -> Run.
-- Veilig om opnieuw te draaien: bestaande policies worden eerst verwijderd.

-- ---------- user_plays (dagelijkse scores) ----------
drop policy if exists user_plays_select_own on public.user_plays;
drop policy if exists user_plays_insert_own on public.user_plays;
drop policy if exists user_plays_update_own on public.user_plays;

create policy user_plays_select_own
  on public.user_plays for select
  using ((select auth.uid()) = user_id);

create policy user_plays_insert_own
  on public.user_plays for insert
  with check ((select auth.uid()) = user_id);

create policy user_plays_update_own
  on public.user_plays for update
  using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);

-- ---------- library_plays (library-voortgang) ----------
drop policy if exists library_plays_select_own on public.library_plays;
drop policy if exists library_plays_insert_own on public.library_plays;
drop policy if exists library_plays_update_own on public.library_plays;

create policy library_plays_select_own
  on public.library_plays for select
  using ((select auth.uid()) = user_id);

create policy library_plays_insert_own
  on public.library_plays for insert
  with check ((select auth.uid()) = user_id);

create policy library_plays_update_own
  on public.library_plays for update
  using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);

-- ---------- Vereist voor de upserts in de client ----------
-- syncLibraryPlay gebruikt onConflict: 'user_id,puzzle_id'. Zonder unieke
-- constraint op die kolommen faalt de upsert alsnog. Idem voor de daily-upsert
-- op (user_id, puzzle_date). Deze indexen zijn no-ops als ze al bestaan.
create unique index if not exists library_plays_user_puzzle_uniq
  on public.library_plays (user_id, puzzle_id);

create unique index if not exists user_plays_user_date_uniq
  on public.user_plays (user_id, puzzle_date);

-- ---------- Controle achteraf ----------
-- Verwacht: 3 policies per tabel.
-- select tablename, policyname, cmd from pg_policies
--  where schemaname = 'public' and tablename in ('user_plays','library_plays')
--  order by tablename, policyname;
