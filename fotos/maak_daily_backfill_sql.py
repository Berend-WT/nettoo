#!/usr/bin/env python3
"""Genereert de SQL die de bestaande dailies naar de puzzles-tabel schrijft.

De 35 dailies leven nu alleen in data/netto_frontend_puzzles.js. Zolang ze niet in de
database staan, kan er geen foto, bronvermelding of adminbewerking aan hangen —
al die velden zitten immers op de puzzelrij.

Het script leest dezelfde bron als de frontend, zodat de backfill niet uit de
pas kan lopen met wat spelers zien.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/netto_frontend_puzzles.js"
OUTPUT = ROOT / "supabase" / "backfill_dailies.sql"

HEADER = """-- Netto — bestaande dailies naar de puzzles-tabel
--
-- GEGENEREERD door fotos/maak_daily_backfill_sql.py; niet met de hand bijwerken.
--
-- WAAROM
-- De dailies stonden alleen in data/netto_frontend_puzzles.js. De frontend leest nu
-- ingeplande dailies uit Supabase (met dat bestand als vangnet), maar de tabel
-- was leeg. Zonder rij in puzzles is er niets om een foto, bronvermelding of
-- adminbewerking aan te hangen.
--
-- OPERATOR-CONSTRAINT
-- De check op puzzles.operator liet alleen ASCII + - * / toe, terwijl het spel
-- overal de typografische tekens gebruikt: × (U+00D7), ÷ (U+00F7) en − (U+2212).
-- 30 van de 35 dailies zouden dus geweigerd zijn, en het adminscherm zou bij de
-- eerste inplanning van een library-puzzel op dezelfde fout stuklopen.
-- library_puzzles staat die tekens al wel toe; puzzles wordt hier gelijkgetrokken.
--
-- UITVOEREN
-- Supabase dashboard -> SQL Editor -> plak dit -> Run. Veilig om te herhalen:
-- een datum die al bezet is, wordt overgeslagen.

-- ---------- operator-constraint gelijktrekken ----------
do $$
declare
  c record;
begin
  for c in
    select con.conname
    from pg_constraint con
    join pg_class rel on rel.oid = con.conrelid
    join pg_namespace nsp on nsp.oid = rel.relnamespace
    where nsp.nspname = 'public'
      and rel.relname = 'puzzles'
      and con.contype = 'c'
      and pg_get_constraintdef(con.oid) ilike '%operator%'
  loop
    execute format('alter table public.puzzles drop constraint %I', c.conname);
  end loop;
end $$;

alter table public.puzzles
  add constraint puzzles_operator_check
  check (operator in ('+', '−', '×', '÷'));

-- ---------- de dailies zelf ----------
"""

FOOTER = """
-- ---------- Controle achteraf ----------
-- Verwacht: 35 rijen, oudste 2026-08-01, nieuwste 2026-09-04.
--
-- select count(*), min(scheduled_date), max(scheduled_date) from public.puzzles;
--
-- Verwacht: geen enkele rij zonder derde vraag.
-- select count(*) from public.puzzles where question_3 is null;
"""


def sql_str(value) -> str:
    if value is None or value == "":
        return "null"
    return "'" + str(value).replace("'", "''") + "'"


def sql_num(value) -> str:
    return "null" if value is None else str(value)


def main() -> None:
    src = SOURCE.read_text(encoding="utf-8")
    data = json.loads(src[src.index("=") + 1:].rstrip().rstrip(";"))
    dailies = sorted(data["daily"], key=lambda d: d.get("date") or "")

    regels = [HEADER]
    for daily in dailies:
        # Alleen invoegen als die datum nog vrij is, zodat opnieuw draaien niets
        # dubbel doet en handmatig ingeplande dailies met rust worden gelaten.
        regels.append(
            "insert into public.puzzles "
            "(question_1, question_2, question_3, true_answer_1, true_answer_2, true_answer_3, "
            "operator, scheduled_date, status, source_library_id)\n"
            "select {q1}, {q2}, {q3}, {a1}, {a2}, {a3}, {op}, {date}, 'scheduled', {lib}\n"
            "where not exists (select 1 from public.puzzles where scheduled_date = {date});".format(
                q1=sql_str(daily.get("q1_label")),
                q2=sql_str(daily.get("q2_label")),
                q3=sql_str(daily.get("q3_label")),
                a1=sql_num(daily.get("q1_answer")),
                a2=sql_num(daily.get("q2_answer")),
                a3=sql_num(daily.get("q3_answer")),
                op=sql_str(daily.get("operator")),
                date=sql_str(daily.get("date")),
                lib=sql_str(daily.get("source_library_id")),
            )
        )
    regels.append(FOOTER)

    OUTPUT.write_text("\n\n".join(regels), encoding="utf-8")
    print(f"Geschreven: {OUTPUT.relative_to(ROOT)} ({len(dailies)} dailies)")


if __name__ == "__main__":
    main()
