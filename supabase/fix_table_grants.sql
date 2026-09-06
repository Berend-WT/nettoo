-- Netto — ontbrekende table-grants herstellen
--
-- PROBLEEM
-- Op vrijwel alle tabellen staan nette RLS-policies, maar de rollen anon en
-- authenticated hebben geen enkele table-grant. In Postgres werkt dat zo:
-- eerst wordt het GRANT gecontroleerd, pas daarna de RLS-policy. Zonder grant
-- komt de policy dus nooit aan bod en krijgt de client simpelweg
-- "permission denied for table ...".
--
-- Gemeten vanuit de browser met de anon-key: alleen puzzles was leesbaar (die
-- grant is net toegevoegd). library_puzzles, library_plays, user_plays,
-- archive_plays, profiles, scores, user_notifications, question_submissions en
-- admin_users gaven allemaal permission denied.
--
-- GEVOLG
-- De hele Supabase-koppeling deed feitelijk niets. Dat is ook precies wat je in
-- de data ziet: elke tabel waar de app naartoe schrijft is leeg. Alleen
-- library_puzzles en admin_users bevatten rijen, en die zijn via het dashboard
-- gevuld in plaats van via de API.
--
-- AANPAK
-- Per tabel alleen de rechten die daar nodig zijn. De RLS-policies bepalen
-- daarna nog steeds wélke rijen zichtbaar zijn; het grant zegt alleen dat de
-- rol de tabel überhaupt mag benaderen.
--
-- UITVOEREN
-- Supabase dashboard -> SQL Editor -> plak dit -> Run. Veilig om te herhalen.
--
-- LET OP: draai ook supabase/fix_rls_plays.sql als dat nog niet gebeurd is.
-- Dat bestand voegt de ontbrekende policies op user_plays en library_plays toe.
-- Grants en policies zijn allebei nodig: het een zonder het ander werkt niet.

-- ---------- Content die iedereen mag lezen ----------
-- Bevat antwoorden, maar die staan sowieso al in de statische JS-bestanden van
-- de frontend; dit verandert dus niets aan wat een speler kan zien.
grant select on public.library_puzzles to anon, authenticated;

-- Leaderboard is publiek leesbaar. Invoegen blijft geblokkeerd door de
-- bestaande policy "geen directe client insert" (with check false).
grant select on public.scores to anon, authenticated;

-- ---------- Eigen speelgegevens ----------
-- Policies beperken dit al tot auth.uid() = user_id.
grant select, insert, update on public.user_plays to authenticated;
grant select, insert, update on public.library_plays to authenticated;
grant select, insert, update on public.archive_plays to authenticated;
grant select, insert, update on public.profiles to authenticated;

-- ---------- Meldingen ----------
-- Lezen en als gelezen markeren mag de speler zelf; invoegen is via de policy
-- beperkt tot admins en loopt in de praktijk via admin_review_submission.
grant select, update on public.user_notifications to authenticated;
grant insert on public.user_notifications to authenticated;
grant usage, select on sequence public.user_notifications_id_seq to authenticated;

-- ---------- Inzendingen ----------
-- Insturen mag ook zonder account; lezen en beoordelen is via policies beperkt
-- tot de eigen inzending respectievelijk admins.
grant select, insert on public.question_submissions to anon, authenticated;
grant update on public.question_submissions to authenticated;

-- ---------- Adminstatus ----------
-- De policy laat alleen de eigen rij zien, dus dit verraadt niet wie er nog
-- meer admin is.
grant select on public.admin_users to authenticated;

-- ============================================================
-- Controle achteraf
-- ============================================================
-- Verwacht: een regel per tabel/rol met de toegekende rechten.
--
-- select table_name, grantee, string_agg(privilege_type, ', ' order by privilege_type)
--   from information_schema.role_table_grants
--  where table_schema = 'public' and grantee in ('anon','authenticated')
--  group by table_name, grantee
--  order by table_name, grantee;
