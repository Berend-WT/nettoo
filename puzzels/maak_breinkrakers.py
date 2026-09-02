#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genereer Breinkrakers-puzzels: 4 vragen in één formule.

Formule: a (× of ÷) b (+ of −) c = d  — standaard rekenvolgorde, dus
(a op1 b) op2 c = d. Alle vier de vragen komen uit de vragenbank, zijn
binnen één puzzel altijd verschillend en de formule klopt exact.

Output:
  1. breinkrakers.xlsx        — 100.000 puzzels (tabblad Breinkrakers + Overzicht)
  2. netto_breinkrakers.js    — 200 uitgekozen speelpuzzels voor de frontend

Theoretisch bestaan er ~475 miljoen combinaties; dit script schrijft een
kwaliteitsselectie met een moeilijkheidsramp (kleine h1 → grote h1).
"""

from __future__ import annotations

import json
import math
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import maak_puzzels as m

INPUT = Path("vragen/1000+ vragen netjes gecategoriseerd.xlsx")
OUTPUT_XLSX = Path("puzzels/breinkrakers.xlsx")
OUTPUT_JS = Path("netto_breinkrakers.js")  # frontend-asset, blijft in de projectroot
TARGET_ROWS = 100_000
FRONTEND_TARGET = 200
FRONTEND_REUSE_CAP = 4
MAX_PLAY_VALUE = 1_000_000

BK_WEIGHTS = {"×": 14.0, "÷": 18.0, "+": 0.0, "−": 8.0}
COL_LETTERS = [chr(65 + i) for i in range(18)]
COL_WIDTHS = [11, 30, 11, 11, 14, 26, 66, 14, 26, 66, 14, 26, 66, 14, 26, 66, 16, 12]
HEADERS = [
    "Puzzel #", "Formule", "Bewerking 1", "Bewerking 2",
    "Antwoord 1", "Categorie 1", "Vraag 1",
    "Antwoord 2", "Categorie 2", "Vraag 2",
    "Antwoord 3", "Categorie 3", "Vraag 3",
    "Antwoord 4", "Categorie 4", "Vraag 4",
    "Difficulty", "Difficulty score",
]


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def bk_score(op1: str, op2: str, values) -> float:
    return round(
        BK_WEIGHTS[op1] + BK_WEIGHTS[op2]
        + sum(math.log10(abs(float(v)) + 1.0) * 10.0 for v in values), 2)


def bk_level(score: float) -> str:
    if score < 35:
        return "Easy"
    if score < 60:
        return "Intermediate"
    if score < 90:
        return "Hard"
    return "Extremely Hard"


# ------------------------------------------------------------- xlsx-writer

def row_xml(row_number: int, cells: list) -> str:
    parts = [f'<row r="{row_number}">']
    for column, (kind, value) in enumerate(cells):
        ref = f"{COL_LETTERS[column]}{row_number}"
        if kind == "n":
            parts.append(f'<c r="{ref}"><v>{value}</v></c>')
        else:
            parts.append(f'<c r="{ref}" t="inlineStr"><is><t>{value}</t></is></c>')
    parts.append("</row>")
    return "".join(parts)


def cols_xml() -> str:
    parts = ["<cols>"]
    for i, width in enumerate(COL_WIDTHS, start=1):
        parts.append(f'<col min="{i}" max="{i}" width="{width}" customWidth="1"/>')
    parts.append("</cols>")
    return "".join(parts)


def write_data_sheet(zf: zipfile.ZipFile, name: str, rows: list) -> None:
    last_row = len(rows) + 1
    dim = f"A1:{COL_LETTERS[-1]}{last_row}"
    header = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<dimension ref="{dim}"/>'
        '<sheetViews><sheetView workbookViewId="0">'
        '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
        '</sheetView></sheetViews>'
        + cols_xml() + "<sheetData>"
    )
    footer = f'</sheetData><autoFilter ref="{dim}"/></worksheet>'
    with zf.open(f"xl/worksheets/sheet1.xml", "w") as stream:
        stream.write(header.encode("utf-8"))
        stream.write(row_xml(1, [("s", h) for h in HEADERS]).encode("utf-8"))
        buffer: list[str] = []
        for index, cells in enumerate(rows, start=2):
            buffer.append(row_xml(index, cells))
            if len(buffer) >= 2000:
                stream.write("".join(buffer).encode("utf-8"))
                buffer.clear()
        if buffer:
            stream.write("".join(buffer).encode("utf-8"))
        stream.write(footer.encode("utf-8"))


def write_overview_sheet(zf: zipfile.ZipFile, stats: dict) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<dimension ref="A1:B20"/><sheetData>',
    ]
    row_number = 0

    def add(label: str, value: object) -> None:
        nonlocal row_number
        row_number += 1
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            value_cell = f'<c r="B{row_number}"><v>{value}</v></c>'
        else:
            value_cell = f'<c r="B{row_number}" t="inlineStr"><is><t>{esc(str(value))}</t></is></c>'
        lines.append(
            f'<row r="{row_number}">'
            f'<c r="A{row_number}" t="inlineStr"><is><t>{esc(str(label))}</t></is></c>'
            f'{value_cell}</row>'
        )

    for key, value in stats.items():
        add(key, value)
    lines.append("</sheetData></worksheet>")
    with zf.open("xl/worksheets/sheet2.xml", "w") as stream:
        stream.write("".join(lines).encode("utf-8"))


def write_xlsx(path: Path, rows: list, stats: dict) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
            "</Types>",
        )
        zf.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            "</Relationships>",
        )
        zf.writestr(
            "xl/workbook.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            "<sheets>"
            '<sheet name="Breinkrakers" sheetId="1" r:id="rId1"/>'
            '<sheet name="Overzicht" sheetId="2" r:id="rId2"/>'
            "</sheets></workbook>",
        )
        zf.writestr(
            "xl/_rels/workbook.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            "</Relationships>",
        )
        zf.writestr(
            "xl/styles.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<fonts count="1"><font><sz val="11"/><name val="Calibri"/><family val="2"/></font></fonts>'
            '<fills count="2"><fill><patternFill patternType="none"/></fill>'
            '<fill><patternFill patternType="gray125"/></fill></fills>'
            '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
            '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
            '<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>'
            '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
            "</styleSheet>",
        )
        write_data_sheet(zf, "Breinkrakers", rows)
        write_overview_sheet(zf, stats)


# ------------------------------------------------------------------ main

def main() -> None:
    print(f"Inlezen: {INPUT}")
    questions, skipped = m.load_questions(INPUT)
    questions = [q for q in questions if q.answer.denominator == 1]
    vals_all = [q.answer.numerator for q in questions]
    cB = Counter(vals_all)
    buckets: dict[int, list[int]] = defaultdict(list)
    for index, value in enumerate(vals_all):
        buckets[value].append(index)
    V = sorted(buckets)
    vset = set(V)
    n = len(V)
    print(f"Vragen: {len(questions)} | unieke waarden: {n}")

    # 1. halve sommen: a op1 b = h1 (op1 in {×, ÷}), waarde-niveau
    half_pairs: dict[int, list[tuple[int, int, str]]] = defaultdict(list)
    for i, a in enumerate(V):
        for j in range(i, n):
            b = V[j]
            if a > 0 and b > 0 and a != 1 and b != 1:
                half_pairs[a * b].append((a, b, "×"))
    for a in V:
        for b in V:
            if b > 0 and b != 1 and a % b == 0:
                h = a // b
                if h > 0 and h != 1:
                    half_pairs[h].append((a, b, "÷"))

    cursors: dict[int, int] = defaultdict(int)

    def take_id(value: int, avoid: set[int]) -> int | None:
        bucket = buckets[value]
        size = len(bucket)
        start = cursors[value] % size
        for k in range(size):
            idx = (start + k) % size
            qid = bucket[idx]
            if qid not in avoid:
                cursors[value] = (idx + 1) % size
                return qid
        return None

    keys = sorted(half_pairs)
    usable_keys = []
    for h1 in keys:
        if diffmap_pair_count(h1, V, vset) > 0 or summap_pair_count(h1, V, vset) > 0:
            usable_keys.append(h1)
    print(f"Bruikbare h1-sleutels: {len(usable_keys):,}")
    total_budget = TARGET_ROWS
    rows: list[tuple] = []
    seen_combo: set[tuple] = set()
    keys_zero = 0
    combos_seen = 0

    # Meerdere passes over de sleutels tot het budget op is: sleutels met
    # veel combinaties leveren in latere passes nog extra rijen.
    emitted_per_key: dict[int, int] = {}
    used_combo_indices: dict[int, set[int]] = defaultdict(set)
    key_data: dict[int, tuple] = {}
    combos_seen = 0
    for h1 in usable_keys:
        pl = half_pairs[h1]
        plus_list = [(c, c + h1, "+") for c in V if (c + h1) in vset and (c + h1) >= 2]
        minus_list = [(c, h1 - c, "−") for c in V if c < h1 and (h1 - c) in vset and (h1 - c) >= 2]
        combos_total = len(pl) * (len(plus_list) + len(minus_list))
        key_data[h1] = (pl, plus_list, minus_list, combos_total)
        combos_seen += combos_total

    pass_index = 0
    while total_budget > 0:
        pass_index += 1
        progress = 0
        active_keys = [h1 for h1 in usable_keys if key_data[h1][3] - emitted_per_key.get(h1, 0) > 0]
        for position, h1 in enumerate(active_keys):
            if total_budget <= 0:
                break
            pl, plus_list, minus_list, combos_total = key_data[h1]
            already = emitted_per_key.get(h1, 0)
            remaining_combos = combos_total - already
            used = used_combo_indices[h1]
            cap = min(remaining_combos, max(1, total_budget // max(1, len(active_keys) - position) + (1 if total_budget % max(1, len(active_keys) - position) else 0)))
            emitted = 0
            offset = (position + already) % combos_total  # rotatie voor variatie
            prev_ids: dict[tuple, tuple] = {}
            for step in range(combos_total):
                if emitted >= cap or total_budget <= 0:
                    break
                combo_index = (offset + step) % combos_total
                if combo_index in used:
                    continue
                pi = combo_index // (len(plus_list) + len(minus_list))
                ci = combo_index % (len(plus_list) + len(minus_list))
                a, b, op1 = pl[pi]
                if ci < len(plus_list):
                    c, d, op2 = plus_list[ci]
                else:
                    c, d, op2 = minus_list[ci - len(plus_list)]
                combo_key = (a, op1, b, op2, c)
                ids = assign_ids(a, b, op1, c, d, buckets, take_id)
                if ids is None:
                    continue
                if ids == prev_ids.get(combo_key):
                    continue  # geen nieuwe unieke vragen voor deze combinatie
                prev_ids[combo_key] = ids
                used.add(combo_index)
                seen_combo.add(combo_key)
                score = bk_score(op1, op2, (a, b, c, d))
                rows.append((a, b, op1, c, op2, d, ids, score, bk_level(score)))
                emitted += 1
                progress += 1
                total_budget -= 1
            emitted_per_key[h1] = already + emitted
            if emitted == 0 and already == 0:
                keys_zero += 1
        print(f"  pass {pass_index}: +{progress:,} rijen | budget over: {total_budget:,}")
        if progress == 0:
            break
    print(f"Waarde-combinaties gezien: {combos_seen:,} | sleutels zonder rij: {keys_zero:,} | budget over: {total_budget:,}")

    print(f"Geselecteerd: {len(rows):,} puzzels")
    levels = Counter(r[8] for r in rows)
    for level in ("Easy", "Intermediate", "Hard", "Extremely Hard"):
        print(f"  {level}: {levels[level]:,}")

    # 2. Excel schrijven (rijen zijn al op moeilijkheid gerampdoor h1 oplopend)
    esc_text = [esc(q.text) for q in questions]
    esc_cat = [esc(q.category) for q in questions]
    xlsx_rows = []
    for number, (a, b, op1, c, op2, d, ids, score, level) in enumerate(rows, start=1):
        i1, i2, i3, i4 = ids
        formula = f"{a} {op1} {b} {op2} {c} = {d}"
        answers = (a, b, c, d)
        cats = [esc_cat[ids[k]] for k in range(4)]
        texts = [esc_text[ids[k]] for k in range(4)]
        cells = [
            ("n", number), ("s", formula), ("s", op1), ("s", op2),
        ]
        for k in range(4):
            cells += [("n", answers[k]), ("s", cats[k]), ("s", texts[k])]
        cells += [("s", level), ("n", score)]
        xlsx_rows.append(cells)

    op1_counts = Counter(r[2] for r in rows)
    op2_counts = Counter(r[4] for r in rows)
    stats = {
        "Bronbestand": INPUT.name,
        "Vragen in bank": len(questions),
        "Puzzels in bestand": len(rows),
        "Vermenigvuldig-helft (×)": op1_counts["×"],
        "Deel-helft (÷)": op1_counts["÷"],
        "Plus als tweede (+)": op2_counts["+"],
        "Min als tweede (−)": op2_counts["−"],
        "Easy": levels["Easy"],
        "Intermediate": levels["Intermediate"],
        "Hard": levels["Hard"],
        "Extremely Hard": levels["Extremely Hard"],
        "Theoretisch totaal in ruimte": 475_432_273,
    }
    print(f"Schrijven: {OUTPUT_XLSX} ...")
    write_xlsx(OUTPUT_XLSX, xlsx_rows, stats)

    # 3. Frontend-subset: 200 speelpuzzels met een bewuste niveau-mix
    candidates = [r for r in rows if max(r[0], r[1], r[5], r[3]) <= MAX_PLAY_VALUE]
    candidates.sort(key=lambda r: r[7])
    cat_spread = lambda r: len({questions[i].category for i in r[6]})
    quotas = {"Easy": 8, "Intermediate": 60, "Hard": 90, "Extremely Hard": 42}
    chosen: list[tuple] = []
    uses: Counter = Counter()
    front_seen: set[tuple] = set()
    for level in ("Easy", "Intermediate", "Hard", "Extremely Hard"):
        quota = quotas[level]
        filled = 0
        for r in candidates:
            if filled >= quota or len(chosen) >= FRONTEND_TARGET:
                break
            if r[8] != level:
                continue
            ids = r[6]
            key = (r[0], r[2], r[1], r[4], r[3])
            if key in front_seen:
                continue
            if any(uses[i] >= FRONTEND_REUSE_CAP for i in ids):
                continue
            if len(chosen) < FRONTEND_TARGET // 2 and cat_spread(r) < 2:
                continue
            front_seen.add(key)
            chosen.append(r)
            uses.update(ids)
            filled += 1
    chosen.sort(key=lambda r: r[7])
    print(f"Frontend-subset: {len(chosen)} puzzels | max vraaghergebruik: {max(uses.values())}")
    front_levels = Counter(r[8] for r in chosen)
    for level in ("Easy", "Intermediate", "Hard", "Extremely Hard"):
        print(f"  frontend {level}: {front_levels[level]}")

    puzzles = []
    for number, (a, b, op1, c, op2, d, ids, score, level) in enumerate(chosen, start=1):
        puzzles.append({
            "id": f"bk-{number}",
            "number": number,
            "op1": op1,
            "op2": op2,
            "formula": f"{a} {op1} {b} {op2} {c} = {d}",
            "difficulty": level.lower().replace(" ", "-"),
            "difficulty_score": score,
            "q1": {"label": questions[ids[0]].text, "answer": a, "category": questions[ids[0]].category},
            "q2": {"label": questions[ids[1]].text, "answer": b, "category": questions[ids[1]].category},
            "q3": {"label": questions[ids[2]].text, "answer": c, "category": questions[ids[2]].category},
            "q4": {"label": questions[ids[3]].text, "answer": d, "category": questions[ids[3]].category},
        })
        # Rekenproef per puzzel
        h1 = a * b if op1 == "×" else a // b
        expected = h1 + c if op2 == "+" else h1 - c
        assert expected == d, f"Rekenfout: {a} {op1} {b} {op2} {c} = {expected} != {d}"
    assert len({p["id"] for p in puzzles}) == len(puzzles)

    OUTPUT_JS.write_text(
        "// Netto Breinkrakers — gegenereerd door maak_breinkrakers.py\n"
        "// Formule: a (× of ÷) b (+ of −) c = d — standaard rekenvolgorde.\n"
        "window.NETTO_BREINKRAKERS = "
        + json.dumps(puzzles, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    size_mb = OUTPUT_XLSX.stat().st_size / (1024 * 1024)
    print(f"Klaar: {OUTPUT_XLSX} ({size_mb:.1f} MB, {len(rows):,} puzzels) + {OUTPUT_JS} ({len(puzzles)} speelpuzzels)")


def _stride_positions(total: int, take: int) -> set[int]:
    if take >= total:
        return set(range(total))
    return {(total * j) // take for j in range(take)}


def diffmap_pair_count(h1: int, V: list, vset: set) -> int:
    count = 0
    for c in V:
        if (c + h1) in vset and (c + h1) >= 2:
            count += 1
    return count


def summap_pair_count(h1: int, V: list, vset: set) -> int:
    count = 0
    for c in V:
        if c < h1 and (h1 - c) in vset and (h1 - c) >= 2:
            count += 1
    return count


def assign_ids(a, b, op1, c, d, buckets, take_id):
    used: set[int] = set()
    ids = []
    for value in (a, b, c, d):
        qid = take_id(value, used)
        if qid is None:
            # fallback: zoek welke id dan ook die nog niet gebruikt is
            for qid2 in buckets[value]:
                if qid2 not in used:
                    qid = qid2
                    break
            if qid is None:
                return None
        ids.append(qid)
        used.add(qid)
    return tuple(ids)


if __name__ == "__main__":
    main()
