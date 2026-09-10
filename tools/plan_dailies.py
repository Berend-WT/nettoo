# -*- coding: utf-8 -*-
"""Netto — genereert de SQL om dailies vooruit in te plannen.

Draaien:  python tools/plan_dailies.py [aantal_dagen]

WAAROM DIT ANDERS IS DAN DE VORIGE VERSIE
De vorige plan-SQL bestond uit twaalf losse insert-statements. De SQL-editor van
Supabase voert die één voor één uit en stopt bij de eerste fout, maar houdt wat
daarvoor al gelukt is. Op 6 september leverde dat precies twee dailies op en
daarna niets — zonder dat zichtbaar was dat er iets was misgegaan. Vandaag stond
het spel daardoor stil op de puzzel van gisteren.

Deze versie schrijft één insert met een VALUES-lijst. Die slaagt volledig of
faalt volledig met één foutmelding, en sluit af met een select die laat zien wat
er nu gepland staat. Half slagen kan niet meer.

KEUZE VAN DE PUZZELS
Alleen library-puzzels die nog nooit als daily zijn gebruikt, met drie
verschillende categorieën, gespreid over de vier bewerkingen.
"""

import io
import json
import os
import sys
from datetime import date, timedelta

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUZZELS = os.path.join(WORTEL, 'data/netto_frontend_puzzles.js')
DOEL = os.path.join(WORTEL, 'supabase', 'plan_dailies_vooruit.sql')

# De source_library_id's die al als daily in de database staan. Bijwerken met:
#   select source_library_id from public.puzzles where source_library_id is not null;
AL_GEBRUIKT = {
    'library-060', 'library-072', 'library-073', 'library-074', 'library-078',
    'library-080', 'library-081', 'library-083', 'library-087', 'library-088',
    'library-090', 'library-092', 'library-093', 'library-094', 'library-097',
    'library-098', 'library-101', 'library-106', 'library-107', 'library-109',
    'library-110', 'library-112', 'library-122', 'library-124', 'library-125',
    'library-138', 'library-142', 'library-150', 'library-152', 'library-154',
    'library-155', 'library-157', 'library-162', 'library-164', 'library-167',
    'library-168', 'library-169',
}


def sql_tekst(waarde):
    return "'" + str(waarde).replace("'", "''") + "'"


def main():
    dagen = int(sys.argv[1]) if len(sys.argv) > 1 else 30

    ruw = io.open(PUZZELS, encoding='utf-8').read()
    data = json.loads(ruw.split('=', 1)[1].strip().rstrip(';'))

    kandidaten = []
    for p in data.get('library', []):
        if p.get('id') in AL_GEBRUIKT:
            continue
        cats = p.get('categories') or []
        if len(cats) != 3 or len(set(cats)) != 3:
            continue
        if not all(p.get(f'q{i}_label') for i in (1, 2, 3)):
            continue
        kandidaten.append(p)

    # Spreiden over de bewerkingen: rondgaan langs ÷ × + − zodat er geen week
    # met alleen delingen ontstaat.
    per_operator = {}
    for p in kandidaten:
        per_operator.setdefault(p['operator'], []).append(p)
    volgorde = [op for op in ('÷', '×', '+', '−') if per_operator.get(op)]

    gekozen, i = [], 0
    while len(gekozen) < dagen and any(per_operator.values()):
        op = volgorde[i % len(volgorde)]
        i += 1
        if per_operator.get(op):
            gekozen.append(per_operator[op].pop(0))

    if len(gekozen) < dagen:
        print(f'LET OP: maar {len(gekozen)} bruikbare puzzels voor {dagen} dagen.')
        dagen = len(gekozen)

    regels = []
    for n, p in enumerate(gekozen[:dagen], start=1):
        waarden = '    (' + ', '.join([
            sql_tekst(p['q1_label']), sql_tekst(p['q2_label']), sql_tekst(p['q3_label']),
            str(p['q1_answer']), str(p['q2_answer']), str(p['q3_answer']),
            sql_tekst(p['operator']), str(n),
            "'scheduled'", sql_tekst(p['id']),
        ]) + ')'
        # De komma hoort vóór het commentaar: staat hij erachter, dan valt hij
        # binnen het commentaar en is de hele VALUES-lijst syntactisch stuk.
        if n < dagen:
            waarden += ','
        regels.append(waarden + '  -- ' + ' / '.join(p['categories']))

    sql = f"""-- Netto — plan {dagen} dagpuzzels vooruit, aansluitend op wat er al staat
--
-- GEGENEREERD door tools/plan_dailies.py.
--
-- WAAROM DE DATUMS HIER NIET IN STAAN
-- Een eerdere versie zette de datums vast bij het genereren, vanaf de dag van
-- draaien. Draaide je hem terwijl er al tot 9 oktober gepland stond, dan botste
-- elke regel met een bestaande dag en werd er niets toegevoegd — zonder dat er
-- iets misging waar je iets van merkte. Nu rekent de SQL zelf uit waar de reeks
-- ophoudt en telt daarvandaan verder.
--
-- WAAROM ÉÉN STATEMENT
-- De versie daarvóór bestond uit losse inserts. De SQL-editor stopt bij de
-- eerste fout maar houdt wat daarvoor al gelukt is, en dat leverde op
-- 6 september twee dailies op waarna het spel stil kwam te staan op een oude
-- puzzel. Dit is één insert: hij slaagt volledig of faalt volledig.
--
-- TWEE KEER DRAAIEN KAN GEEN KWAAD
-- Een dag die al bezet is wordt overgeslagen, en een library-puzzel die al eens
-- daily is geweest ook. Dat tweede stond eerst als handmatige lijst in het
-- Python-script; als die lijst achterliep kwam dezelfde puzzel een tweede keer
-- langs. Nu kijkt de databank zelf.
--
-- UITVOEREN
-- Supabase dashboard -> SQL Editor -> plak dit -> Run. Onderaan staat een
-- controle die laat zien wat er daarna gepland staat.

insert into public.puzzles (
  question_1, question_2, question_3,
  true_answer_1, true_answer_2, true_answer_3,
  operator, scheduled_date, status, source_library_id
)
select v.question_1, v.question_2, v.question_3,
       v.true_answer_1, v.true_answer_2, v.true_answer_3,
       v.operator,
       -- Verdergaan waar de agenda ophoudt. Staat er nog niets, dan begint hij
       -- vandaag.
       (select greatest(coalesce(max(scheduled_date), current_date - 1), current_date - 1)
          from public.puzzles) + v.dagnummer::int,
       v.status, v.source_library_id
from (values
{chr(10).join(regels)}
) as v(question_1, question_2, question_3,
       true_answer_1, true_answer_2, true_answer_3,
       operator, dagnummer, status, source_library_id)
where not exists (
  select 1 from public.puzzles p
  where p.scheduled_date =
    (select greatest(coalesce(max(scheduled_date), current_date - 1), current_date - 1)
       from public.puzzles) + v.dagnummer::int
)
and not exists (
  select 1 from public.puzzles p
  where p.source_library_id = v.source_library_id
);


-- Controle: hoort een aaneengesloten reeks te tonen, zonder gaten.
-- Staat er een getal groter dan 1 in gat_in_dagen, dan mist er een dag.
select scheduled_date,
       scheduled_date - (lag(scheduled_date) over (order by scheduled_date)) as gat_in_dagen,
       left(question_1, 46) as vraag
from public.puzzles
where scheduled_date >= current_date - 1
order by scheduled_date;
"""

    io.open(DOEL, 'w', encoding='utf-8').write(sql)
    print(f'{dagen} dagpuzzels klaargezet; de SQL hangt ze achter de laatste '
          f'geplande dag aan')
    print(f'{len(kandidaten)} bruikbare library-puzzels beschikbaar, '
          f'{len(kandidaten) - dagen} blijven over')
    print(f'-> {DOEL}')


if __name__ == '__main__':
    main()
