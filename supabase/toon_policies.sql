-- Netto — laat zien wát de policies toestaan, niet hoevéél het er zijn
--
-- UITVOEREN
-- Supabase dashboard -> SQL Editor -> plak dit -> Run. Leest alleen, verandert
-- niets. Deel 2 onderaan verandert wél iets en staat er bewust uitgecommentarieerd bij.
--
-- WAAROM DIT NODIG IS
-- Het rapport van controleer_rls.sql telt policies. Dat is niet genoeg, om een
-- reden die makkelijk te missen is: **Postgres combineert permissive policies
-- met OR.** Eén policy die `using (true)` zegt, maakt elke zorgvuldige policy
-- ernaast betekenisloos. In een telling zie je dat verschil niet — twee is twee.
--
-- En er staan er acht live die niet uit onze SQL-bestanden komen; die zijn ooit
-- via het dashboard gemaakt. Wat ze toestaan weet niemand meer:
--
--   admin_users           1 van de 2 onbekend
--   library_puzzles       1 van de 1 onbekend
--   puzzles               1 van de 2 onbekend
--   question_submissions  3 van de 7 onbekend
--   scores                2 van de 2 onbekend
--
-- Op scores en library_puzzles heeft ook `anon` SELECT, dus daar telt het
-- meteen voor iedere bezoeker.

-- ============================================================
-- 1. Wat staat elke policy toe?
-- ============================================================
-- Waar je op let:
--   * permissive = 'PERMISSIVE' met qual = 'true'  -> zet de tabel open voor
--     de genoemde rollen, hoe streng de buurpolicy ook is
--   * roles met {public} of {anon}                 -> geldt ook uitgelogd
--   * cmd = 'ALL'                                  -> lezen én schrijven
--   * with_check leeg bij INSERT/UPDATE            -> geen eis aan wat je wegschrijft

select tablename                as tabel,
       policyname               as policy,
       cmd                      as voor,
       permissive,
       roles::text              as rollen,
       coalesce(qual, '(geen)') as leesvoorwaarde,
       coalesce(with_check, '(geen)') as schrijfvoorwaarde
from pg_policies
where schemaname = 'public'
order by
  -- het verdachte bovenaan: alles-toestaan, en alles wat voor anon geldt
  (qual = 'true') desc,
  (roles::text like '%anon%' or roles::text like '%public%') desc,
  tablename, policyname;

-- ============================================================
-- 2. Rechten die row level security niet tegenhoudt
-- ============================================================
-- Op elke tabel staat TRUNCATE, REFERENCES en TRIGGER voor zowel anon als
-- authenticated. Dat komt uit de standaard-grant waarmee een Supabase-project
-- begint (`grant all on all tables in schema public`), niet uit onze eigen SQL.
--
-- Waarom dit niet hetzelfde is als de rest: **RLS geldt niet voor TRUNCATE.**
-- Policies werken per rij, TRUNCATE werkt op de hele tabel en gaat er langs.
-- Een policy die zegt "alleen je eigen rijen" houdt een TRUNCATE dus niet tegen.
--
-- Hoe erg is het nu: niet erg. PostgREST — waar de anon key op uitkomt — heeft
-- geen enkele route die TRUNCATE uitvoert. Er is geen HTTP-verzoek dat je kunt
-- sturen om hier misbruik van te maken. Het is een recht dat niemand nodig
-- heeft en dat RLS niet dekt, en dat is genoeg reden om het weg te halen.
--
-- Hetzelfde geldt voor REFERENCES (foreign keys leggen naar deze tabel) en
-- TRIGGER (triggers erop zetten). Geen van beide heeft een client ooit nodig.
--
-- Dit is de enige plek in dit bestand die iets verandert. Ik kan het niet tegen
-- jouw databank uitproberen, dus haal de commentaartekens er pas af als je het
-- gelezen hebt. Draai daarna deel 1 opnieuw: SELECT, INSERT en UPDATE horen te
-- blijven staan, precies zoals ze nu zijn.

-- revoke truncate, references, trigger
--   on all tables in schema public
--   from anon, authenticated;

-- ============================================================
-- 3. Wat er daarna hoort te staan
-- ============================================================
-- Draai dit na deel 2 om te controleren dat alleen de bedoelde rechten over zijn.

select table_name as tabel,
       grantee    as rol,
       string_agg(distinct privilege_type, ', ' order by privilege_type) as rechten
from information_schema.role_table_grants
where table_schema = 'public'
  and grantee in ('anon', 'authenticated')
group by table_name, grantee
order by table_name, grantee;
