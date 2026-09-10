-- Netto — wat laat puzzles_public zien, en aan wie?
--
-- UITVOEREN
-- SQL Editor -> plak dit -> Run. Leest alleen.
--
-- WAAROM
-- `puzzles_public` heeft SELECT voor anon, komt in geen enkel bestand van de
-- repo voor, en stond niet in het RLS-rapport omdat dat op gewone tabellen
-- filterde. Het is dus een view.
--
-- Bij een view is één ding beslissend: **een view draait standaard met de
-- rechten van zijn eigenaar, niet van de lezer.** Row level security op de
-- onderliggende tabel geldt dan niet voor wie de view opvraagt. Alleen met
-- `security_invoker = true` (Postgres 15+) wordt de RLS van de lezer wél
-- toegepast.
--
-- Waar het om gaat: als deze view uit `puzzles` leest zonder filter op status
-- of datum, dan kan iedere bezoeker de ingeplande dagpuzzels ophalen —
-- inclusief de vragen en antwoorden van morgen. Dat is bij een schatspel het
-- hele spel.

select c.relname                                   as view,
       case c.relkind when 'v' then 'view'
                      when 'm' then 'materialized view'
                      else c.relkind::text end     as soort,
       coalesce((
         select option_value from pg_options_to_table(c.reloptions)
         where option_name = 'security_invoker'), 'niet gezet')
                                                   as security_invoker,
       pg_get_userbyid(c.relowner)                 as eigenaar
from pg_class c
join pg_namespace n on n.oid = c.relnamespace
where n.nspname = 'public' and c.relkind in ('v', 'm');

-- De definitie zelf. Let op een where-regel met status of scheduled_date.
select viewname as view, definition
from pg_views
where schemaname = 'public';

-- En de proef op de som: dit is wat een uitgelogde bezoeker terugkrijgt.
-- Staan hier rijen met een datum in de toekomst, dan liggen de dagpuzzels van
-- morgen op straat.
set local role anon;
select * from public.puzzles_public limit 5;
reset role;
