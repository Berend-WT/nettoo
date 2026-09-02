#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bouw de race-pool voor de frontend uit 'puzzels/niet unieke puzzels.xlsx'.

Leest een grote steekproef uit de 5 deelbladen (samen ~4,2 mln puzzels) en
schrijft netto_race_pool.js met window.NETTO_RACE_POOL: een gemengde pool
(alle bewerkingen en moeilijkheden) waar de client per run willekeurig uit
trekt zonder herhaling binnen één run.

De bestanden zijn enorm, dus we lezen per blad een verdeeld segment
(stride-sample) in plaats van alles in geheugen te laden.
"""

from __future__ import annotations

import json
import random
import re
import time
import zipfile
import xml.etree.ElementTree as ET
from html import unescape
from pathlib import Path

POOL_FILE = Path("puzzels/niet unieke puzzels.xlsx")
OUTPUT_JS = Path("netto_race_pool.js")  # frontend-asset, blijft in de projectroot
SAMPLE_PER_SHEET = 1200  # 5 bladen → 6000 puzzels in de pool
SEED = 20260902

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

CELL_RE = re.compile(
    r'<c r="([A-Z]+)\d+"(?:\s+t="inlineStr")?\s*>'
    r'(?:<is><t[^>]*>(.*?)</t></is>|<v>(.*?)</v>)</c>',
    re.DOTALL,
)


def column_letter_to_index(letters: str) -> int:
    index = 0
    for ch in letters:
        index = index * 26 + (ord(ch.upper()) - 64)
    return index - 1


def iter_row_texts(zf: zipfile.ZipFile, sheet_path: str, chunk: int = 1 << 22):
    """Geef ruwe rij-XML-teksten als iterator (snel: string-splitting i.p.v. ET)."""
    buf = ""
    with zf.open(sheet_path) as stream:
        while True:
            data = stream.read(chunk).decode("utf-8", "replace")
            if not data:
                break
            buf += data
            end = buf.rfind("</row>")
            if end == -1:
                continue
            segment = buf[: end + 6]
            buf = buf[end + 6 :]
            for row_text in segment.split("</row>"):
                row_text = row_text.strip()
                if row_text:
                    yield row_text
    tail = buf.strip()
    if tail:
        yield tail


def parse_row(row_text: str) -> dict[int, str]:
    values: dict[int, str] = {}
    for col_letters, inline, plain in CELL_RE.findall(row_text):
        col = column_letter_to_index(col_letters)
        raw = inline or plain
        values[col] = unescape(raw) if raw else ""
    return values


def main() -> None:
    random.seed(SEED)
    puzzles = []
    with zipfile.ZipFile(POOL_FILE) as zf:
        # Volgorde van bladen volgens workbook.xml
        wb = ET.fromstring(zf.read("xl/workbook.xml"))
        rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
        rel_map = {rel.get("Id"): rel.get("Target") for rel in rels}
        sheets = []
        for sheet in wb.find("m:sheets", NS):
            rid = sheet.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
            target = rel_map[rid]
            if not target.startswith("xl/"):
                target = "xl/" + target.lstrip("/")
            sheets.append((sheet.get("name"), target))

        total_rows = 0
        stride = 849_000 // SAMPLE_PER_SHEET
        for sheet_name, sheet_path in sheets:
            started = time.time()
            taken = 0
            for row_index, row_text in enumerate(iter_row_texts(zf, sheet_path)):
                if row_index == 0:
                    continue  # header
                if row_index % stride != 0:
                    continue
                if taken >= SAMPLE_PER_SHEET:
                    break
                values = parse_row(row_text)
                try:
                    operator = values.get(1, "")
                    a1, a2, a3 = int(float(values.get(2, "0"))), int(float(values.get(5, "0"))), int(float(values.get(8, "0")))
                    q1, q2, q3 = values.get(4, ""), values.get(7, ""), values.get(10, "")
                    formula = values.get(11, "")
                    difficulty = values.get(12, "Hard")
                except (ValueError, TypeError):
                    continue
                if not (q1 and q2 and q3 and formula):
                    continue
                puzzles.append({
                    "id": f"pool-{len(puzzles)}",
                    "operator": operator,
                    "q1_label": q1, "q1_answer": a1,
                    "q2_label": q2, "q2_answer": a2,
                    "q3_label": q3, "q3_answer": a3,
                    "calculation": formula,
                    "difficulty": difficulty.lower().replace(" ", "-"),
                })
                taken += 1
                total_rows += 1
            print(f"{sheet_name}: {taken} gepakt in {time.time() - started:.0f}s (stride {stride})")

    random.shuffle(puzzles)
    print(f"Pool totaal: {len(puzzles)} puzzels")
    from collections import Counter
    print("Bewerkingen:", dict(Counter(p["operator"] for p in puzzles)))
    print("Moeilijkheid:", dict(Counter(p["difficulty"] for p in puzzles)))

    OUTPUT_JS.write_text(
        "// Netto Race-pool — gegenereerd door puzzels/maak_race_pool.py\n"
        "// Willekeurige steekproef uit 'puzzels/niet unieke puzzels.xlsx' (4,2 mln).\n"
        "// De client trekt per run willekeurig zonder herhaling binnen die run.\n"
        "window.NETTO_RACE_POOL = "
        + json.dumps(puzzles, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    print(f"Klaar: {OUTPUT_JS} ({OUTPUT_JS.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
