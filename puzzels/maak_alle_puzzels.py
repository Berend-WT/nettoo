#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genereer ALLE mogelijke (niet-unieke) puzzels uit de vragenbank.

Elke vraag mag oneindig vaak worden hergebruikt. Een puzzel is een exacte
formule q1 op q2 = q3 met drie verschillende vragen, volgens de regels van
de unieke generator:

  × : beide operanden > 0 en != 1 (geen triviale 1×x = x-sommen)
  ÷ : deler > 0 en != 1, quotiënt > 0 en != 1, deling exact
  + : beide operanden > 0
  − : eerste > tweede > 0, verschil > 0

Output: 'niet unieke puzzels.xlsx' met 5 tabbladen (Deel 1 t/m Deel 5).
Excel staat maximaal 1.048.576 rijen per tabblad toe; openpyxl houdt alle
rijen in het geheugen en zou hier doodlopen. Daarom schrijft dit script
het xlsx-bestand zelf, rij voor rij, rechtstreeks in de zip-stream.

Volgorde: eerst alle ×, dan ÷, dan +, dan −; binnen elke bewerking
oplopend in antwoordwaarden (dus van makkelijk naar moeilijk).
"""

from __future__ import annotations

import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import maak_puzzels as m

INPUT = Path("vragen/1000+ vragen netjes gecategoriseerd.xlsx")
OUTPUT = Path("puzzels/niet unieke puzzels.xlsx")
SHEET_COUNT = 5
MAX_ROWS_PER_SHEET = 1_048_575  # Excel-rijlimiet minus de headerrij
OPS = ("×", "÷", "+", "−")

COL_LETTERS = [chr(65 + i) for i in range(14)]
COL_WIDTHS = [11, 12, 14, 28, 72, 14, 28, 72, 14, 28, 72, 28, 18, 16]
HEADERS = [
    "Puzzel #", "Bewerking", "Antwoord 1", "Categorie 1", "Vraag 1",
    "Antwoord 2", "Categorie 2", "Vraag 2", "Antwoord 3", "Categorie 3",
    "Vraag 3", "Exacte formule", "Difficulty", "Difficulty score",
]


def fmt(value: object) -> str:
    if isinstance(value, int):
        return str(value)
    return m.format_number(value)


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ----------------------------------------------------------------- telling

def count_by_values(counter: Counter) -> dict[str, int]:
    """Exact aantal puzzels per bewerking, puur via antwoordwaarden."""
    values = sorted(counter)
    out: dict[str, int] = {}

    total = 0
    for i, a in enumerate(values):
        if a <= 0 or a == 1:
            continue
        for b in values[i:]:
            if b <= 0 or b == 1:
                continue
            r = a * b
            if r in counter:
                if a == b:
                    ca = counter[a]
                    total += (ca * (ca - 1) // 2) * counter[r]
                else:
                    total += counter[a] * counter[b] * counter[r]
    out["×"] = total

    total = 0
    for s in values:
        if s <= 0 or s == 1:
            continue
        for d in values:
            if d <= 0:
                continue
            q, rem = divmod(d, s)
            if rem:
                continue
            if q <= 0 or q == 1 or q not in counter:
                continue
            factor = counter[q] - 1 if q == s else counter[q]
            total += counter[d] * counter[s] * factor
    out["÷"] = total

    total = 0
    for i, a in enumerate(values):
        if a <= 0:
            continue
        for b in values[i:]:
            if b <= 0:
                continue
            r = a + b
            if r in counter:
                if a == b:
                    ca = counter[a]
                    total += (ca * (ca - 1) // 2) * counter[r]
                else:
                    total += counter[a] * counter[b] * counter[r]
    out["+"] = total

    total = 0
    for a in values:
        if a <= 0:
            continue
        for b in values:
            if b <= 0 or b >= a:
                continue
            r = a - b
            if r in counter:
                factor = counter[r] - 1 if r == b else counter[r]
                total += counter[a] * counter[b] * factor
    out["−"] = total
    return out


def count_by_questions(vals: list[int], counter: Counter) -> dict[str, int]:
    """Onafhankelijke controle: tellen over losse vraagparen."""
    n = len(vals)
    times = plus = div = minus = 0
    for i in range(n):
        vi = vals[i]
        for j in range(i + 1, n):
            vj = vals[j]
            a, b = (vi, vj) if vi <= vj else (vj, vi)
            if a > 0 and b > 0 and a != 1 and b != 1:
                r = a * b
                if r in counter:
                    times += counter[r]
            if a > 0 and b > 0:
                r = a + b
                if r in counter:
                    plus += counter[r]
    for i in range(n):
        vi = vals[i]
        for j in range(n):
            if i == j:
                continue
            vj = vals[j]
            if vj > 0 and vj != 1 and vi % vj == 0:
                q = vi // vj
                if q > 0 and q != 1 and q in counter:
                    div += counter[q] - (1 if q == vj else 0)
    for i in range(n):
        vi = vals[i]
        for j in range(n):
            if i == j:
                continue
            vj = vals[j]
            if vi > vj and vj > 0:
                r = vi - vj
                if r in counter:
                    minus += counter[r] - (1 if r == vj else 0)
    return {"×": times, "÷": div, "+": plus, "−": minus}


# ------------------------------------------------------------ enumeratie

def iter_op(op: str, buckets: dict, values_sorted: list):
    """Yield (i1, i2, i3) voor elke geldige puzzel, deterministisch."""
    if op == "×":
        for ai, a in enumerate(values_sorted):
            if a <= 0 or a == 1:
                continue
            b1 = buckets[a]
            for b in values_sorted[ai:]:
                if b <= 0 or b == 1:
                    continue
                b3 = buckets.get(a * b)
                if not b3:
                    continue
                b2 = buckets[b]
                same = a == b
                for i1 in b1:
                    for i2 in b2:
                        if same and i2 <= i1:
                            continue
                        for i3 in b3:
                            yield i1, i2, i3
    elif op == "÷":
        for s in values_sorted:
            if s <= 0 or s == 1:
                continue
            b2 = buckets[s]
            for d in values_sorted:
                if d <= 0:
                    continue
                q, rem = divmod(d, s)
                if rem or q <= 0 or q == 1:
                    continue
                b3 = buckets.get(q)
                if not b3:
                    continue
                b1 = buckets[d]
                for i1 in b1:
                    for i2 in b2:
                        for i3 in b3:
                            if q == s and i3 == i2:
                                continue
                            yield i1, i2, i3
    elif op == "+":
        for ai, a in enumerate(values_sorted):
            if a <= 0:
                continue
            b1 = buckets[a]
            for b in values_sorted[ai:]:
                if b <= 0:
                    continue
                b3 = buckets.get(a + b)
                if not b3:
                    continue
                b2 = buckets[b]
                same = a == b
                for i1 in b1:
                    for i2 in b2:
                        if same and i2 <= i1:
                            continue
                        for i3 in b3:
                            yield i1, i2, i3
    elif op == "−":
        for a in values_sorted:
            if a <= 0:
                continue
            b1 = buckets[a]
            for b in values_sorted:
                if b <= 0 or b >= a:
                    continue
                r = a - b
                b3 = buckets.get(r)
                if not b3:
                    continue
                b2 = buckets[b]
                for i1 in b1:
                    for i2 in b2:
                        for i3 in b3:
                            if r == b and i3 == i2:
                                continue
                            yield i1, i2, i3


def all_puzzles(questions, buckets, values_sorted):
    """Yield (op, a, b, r, i1, i2, i3) voor elke puzzel, in vaste volgorde."""
    for op in OPS:
        for i1, i2, i3 in iter_op(op, buckets, values_sorted):
            yield (
                op,
                questions[i1].answer.numerator,
                questions[i2].answer.numerator,
                questions[i3].answer.numerator,
                i1, i2, i3,
            )


# ------------------------------------------------------------ xlsx-writer

def cols_xml() -> str:
    parts = ["<cols>"]
    for i, width in enumerate(COL_WIDTHS, start=1):
        parts.append(f'<col min="{i}" max="{i}" width="{width}" customWidth="1"/>')
    parts.append("</cols>")
    return "".join(parts)


def row_xml(row_number: int, cells: list) -> str:
    parts = [f'<row r="{row_number}">']
    for column, (kind, value) in enumerate(cells):
        ref = f"{COL_LETTERS[column]}{row_number}"
        if kind == "n":
            parts.append(f'<c r="{ref}"><v>{value}</v></c>')
        else:
            parts.append(
                f'<c r="{ref}" t="inlineStr"><is><t>{value}</t></is></c>'
            )
    parts.append("</row>")
    return "".join(parts)


def make_cells(
    puzzle_number: int, op: str, a: int, b: int, r: int,
    i1: int, i2: int, i3: int,
    esc_cat: list[str], esc_text: list[str],
) -> list:
    level, score = m.difficulty_for(op, (a, b, r))
    formula = f"{fmt(a)} {op} {fmt(b)} = {fmt(r)}"
    return [
        ("n", puzzle_number),
        ("s", op),
        ("n", a),
        ("s", esc_cat[i1]), ("s", esc_text[i1]),
        ("n", b),
        ("s", esc_cat[i2]), ("s", esc_text[i2]),
        ("n", r),
        ("s", esc_cat[i3]), ("s", esc_text[i3]),
        ("s", formula),
        ("s", level),
        ("n", score),
    ]


def write_sheet(
    zf: zipfile.ZipFile,
    sheet_index: int,
    name: str,
    expected_rows: int,
    pull_row,  # callable(puzzle_number) -> cellenlijst of None als op
) -> int:
    last_row = expected_rows + 1
    dim = f"A1:N{last_row}"
    header = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<dimension ref="{dim}"/>'
        '<sheetViews><sheetView workbookViewId="0">'
        '<pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>'
        '</sheetView></sheetViews>'
        + cols_xml()
        + "<sheetData>"
    )
    footer = f'</sheetData><autoFilter ref="{dim}"/></worksheet>'

    written = 0
    with zf.open(f"xl/worksheets/sheet{sheet_index}.xml", "w") as stream:
        stream.write(header.encode("utf-8"))
        stream.write(row_xml(1, [("s", h) for h in HEADERS]).encode("utf-8"))
        buffer: list[str] = []
        while written < expected_rows:
            cells = pull_row(written + 2)
            if cells is None:
                raise RuntimeError("Vragenlijst uitgeput vóór verwacht aantal rijen.")
            buffer.append(row_xml(written + 2, cells))
            written += 1
            if len(buffer) >= 2000:
                stream.write("".join(buffer).encode("utf-8"))
                buffer.clear()
        if buffer:
            stream.write("".join(buffer).encode("utf-8"))
        stream.write(footer.encode("utf-8"))
    if written != expected_rows:
        raise RuntimeError(f"{name}: {written} rijen != verwacht {expected_rows}")
    return written


# ------------------------------------------------------------------ main

def main() -> None:
    print(f"Inlezen: {INPUT}")
    questions, skipped = m.load_questions(INPUT)
    if skipped:
        print(f"Overgeslagen rijen in bron: {len(skipped)}")

    integer_questions = [
        q for q in questions if q.answer.denominator == 1
    ]
    non_integer = len(questions) - len(integer_questions)
    if non_integer:
        print(f"Let op: {non_integer} vragen met niet-geheel antwoord overgeslagen.")
    questions = integer_questions
    if len(questions) < 3:
        raise ValueError("Te weinig vragen met geheel antwoord.")

    vals = [q.answer.numerator for q in questions]
    counter = Counter(vals)
    buckets: dict[int, list[int]] = defaultdict(list)
    for index, value in enumerate(vals):
        buckets[value].append(index)
    values_sorted = sorted(buckets)
    print(f"Vragen: {len(questions)} | unieke antwoordwaarden: {len(counter)}")

    expected = count_by_values(counter)
    check = count_by_questions(vals, counter)
    for op in OPS:
        if expected[op] != check[op]:
            raise RuntimeError(
                f"Tellingen mismatch bij {op}: {expected[op]} vs {check[op]}"
            )
    total = sum(expected.values())
    print("Verwachte puzzels per bewerking:")
    for op in OPS:
        print(f"  {op}: {expected[op]:,}")
    print(f"  TOTAAL: {total:,}")

    base, remainder = divmod(total, SHEET_COUNT)
    sizes = [base + 1] * remainder + [base] * (SHEET_COUNT - remainder)
    if max(sizes) > MAX_ROWS_PER_SHEET:
        raise RuntimeError("Een tabblad zou de Excel-rijlimiet overschrijden.")

    esc_text = [esc(q.text) for q in questions]
    esc_cat = [esc(q.category) for q in questions]

    puzzle_iter = all_puzzles(questions, buckets, values_sorted)
    op_counts: Counter = Counter()
    op_samples: dict[str, tuple] = {}
    seen_ops: set[str] = set()
    written_total = 0
    current_op = None

    def pull_row(puzzle_number: int):
        nonlocal current_op
        item = next(puzzle_iter, None)
        if item is None:
            return None
        op, a, b, r, i1, i2, i3 = item
        if op != current_op:
            current_op = op
            if op not in seen_ops:
                seen_ops.add(op)
                op_samples[op] = (a, b, r)
        op_counts[op] += 1
        return make_cells(
            puzzle_number, op, a, b, r, i1, i2, i3, esc_cat, esc_text
        )

    print(f"Schrijven: {OUTPUT} ({SHEET_COUNT} tabbladen)...")
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as zf:
        content_types = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
            '<Default Extension="xml" ContentType="application/xml"/>',
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        ]
        for index in range(1, SHEET_COUNT + 1):
            content_types.append(
                f'<Override PartName="/xl/worksheets/sheet{index}.xml" '
                'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            )
        content_types.append(
            '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        )
        content_types.append("</Types>")
        zf.writestr("[Content_Types].xml", "".join(content_types))

        zf.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="xl/workbook.xml"/></Relationships>',
        )

        sheet_tags = "".join(
            f'<sheet name="Deel {index}" sheetId="{index}" r:id="rId{index}"/>'
            for index in range(1, SHEET_COUNT + 1)
        )
        zf.writestr(
            "xl/workbook.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f"<sheets>{sheet_tags}</sheets></workbook>",
        )

        rels = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">',
        ]
        for index in range(1, SHEET_COUNT + 1):
            rels.append(
                f'<Relationship Id="rId{index}" '
                'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
                f'Target="worksheets/sheet{index}.xml"/>'
            )
        rels.append(
            '<Relationship Id="rId6" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
            'Target="styles.xml"/></Relationships>'
        )
        zf.writestr("xl/_rels/workbook.xml.rels", "".join(rels))

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
            '<dxfs count="0"/>'
            '<tableStyles count="0" defaultTableStyle="TableStyleMedium9" defaultPivotStyle="PivotStyleLight16"/>'
            "</styleSheet>",
        )

        for index, size in enumerate(sizes, start=1):
            name = f"Deel {index}"
            count = write_sheet(zf, index, name, size, pull_row)
            written_total += count
            print(f"  {name}: {count:,} rijen klaar (totaal {written_total:,})")

    if written_total != total:
        raise RuntimeError(f"Totaal geschreven {written_total} != verwacht {total}")
    for op in OPS:
        if op_counts[op] != expected[op]:
            raise RuntimeError(f"{op}: {op_counts[op]} != verwacht {expected[op]}")

    # Rekenproef op de eerste puzzel van elke bewerking.
    for op, (a, b, r) in op_samples.items():
        if op == "×":
            ok = a * b == r
        elif op == "÷":
            ok = b > 0 and a / b == r
        elif op == "+":
            ok = a + b == r
        else:
            ok = a - b == r
        if not ok:
            raise RuntimeError(f"Rekenproef mislukt voor {op}: {a} {op} {b} = {r}")
        print(f"Rekenproef {op}: {a} {op} {b} = {r} ✓")

    size_mb = OUTPUT.stat().st_size / (1024 * 1024)
    print(f"Klaar: {written_total:,} puzzels in {OUTPUT} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
