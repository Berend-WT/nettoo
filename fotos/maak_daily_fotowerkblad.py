#!/usr/bin/env python3
"""Bouwt het invulwerkblad waarmee een redacteur foto's bij de dailies zoekt.

De vragen komen uit data/netto_frontend_puzzles.js (de bron die de frontend ook
gebruikt), zodat het werkblad niet uit de pas kan lopen met wat spelers zien.
"""
from __future__ import annotations

import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/netto_frontend_puzzles.js"
OUTPUT = Path(__file__).resolve().parent / "daily_fotos_invullijst.xlsx"

FONT = "Arial"
HEADER_FILL = PatternFill("solid", fgColor="14163B")
EXAMPLE_FILL = PatternFill("solid", fgColor="FFF7DB")
INPUT_FILL = PatternFill("solid", fgColor="FFFFCC")
THIN = Side(style="thin", color="C9CCE8")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

COLUMNS = [
    ("Daily", 8),
    ("Datum", 12),
    ("Vraag 1", 44),
    ("Antw. 1", 10),
    ("Vraag 2", 44),
    ("Antw. 2", 10),
    ("Vraag 3", 44),
    ("Antw. 3", 10),
    ("Foto bij vraag", 14),
    ("Commons-bestandspagina (URL)", 46),
    ("Maker", 22),
    ("Licentie", 16),
    ("Alt-tekst (NL)", 36),
    ("Verklapt het antwoord?", 20),
    ("Akkoord", 10),
]

# Kolommen die de redacteur invult, geel gemarkeerd.
INPUT_COLUMNS = range(9, 16)

EXAMPLE_ROW = [
    "voorbeeld", "—",
    "Hoeveel toetsen heeft een standaardpiano?", 88,
    "Hoeveel snaren heeft een gitaar?", 6,
    "Hoeveel toetsen samen?", 528,
    "q1",
    "https://commons.wikimedia.org/wiki/File:Piano_keyboard.jpg",
    "Jane Doe", "CC BY-SA 4.0",
    "Close-up van een pianoklavier",
    "nee", "ja",
]


def load_dailies() -> list[dict]:
    src = SOURCE.read_text(encoding="utf-8")
    data = json.loads(src[src.index("=") + 1:].rstrip().rstrip(";"))
    dailies = data["daily"]
    # Oplopend op datum: de oudste eerst, zodat je van voren af aan werkt.
    return sorted(dailies, key=lambda d: d.get("date") or "")


def build() -> Path:
    dailies = load_dailies()
    wb = Workbook()

    ws = wb.active
    ws.title = "Daily foto's"
    ws.append([name for name, _ in COLUMNS])
    for index, (_, width) in enumerate(COLUMNS, start=1):
        ws.column_dimensions[get_column_letter(index)].width = width
        cell = ws.cell(1, index)
        cell.font = Font(name=FONT, bold=True, color="FFFFFF", size=10)
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        cell.border = BORDER
    ws.freeze_panes = "C2"

    ws.append(EXAMPLE_ROW)
    for index in range(1, len(COLUMNS) + 1):
        cell = ws.cell(2, index)
        cell.fill = EXAMPLE_FILL
        cell.font = Font(name=FONT, italic=True, size=9)
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        cell.border = BORDER

    for daily in dailies:
        ws.append([
            daily.get("number"),
            daily.get("date"),
            daily.get("q1_label"), daily.get("q1_answer"),
            daily.get("q2_label"), daily.get("q2_answer"),
            daily.get("q3_label"), daily.get("q3_answer"),
            "", "", "", "", "", "", "",
        ])

    for row in range(3, ws.max_row + 1):
        for index in range(1, len(COLUMNS) + 1):
            cell = ws.cell(row, index)
            cell.font = Font(name=FONT, size=10)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = BORDER
            if index in INPUT_COLUMNS:
                cell.fill = INPUT_FILL
        ws.row_dimensions[row].height = 46

    guide = wb.create_sheet("Instructies")
    for line in INSTRUCTIONS:
        guide.append([line])
    guide.column_dimensions["A"].width = 108
    for row in range(1, guide.max_row + 1):
        cell = guide.cell(row, 1)
        bold = cell.value in SECTION_TITLES
        cell.font = Font(name=FONT, size=11, bold=bold)
        cell.alignment = Alignment(wrap_text=True, vertical="top")

    wb.save(OUTPUT)
    return OUTPUT


SECTION_TITLES = {
    "Wat vul je in?",
    "Wat is een goede foto?",
    "Licentie — hier niet van afwijken",
    "Zo zoek je op Wikimedia Commons",
}

INSTRUCTIONS = [
    "Foto's zoeken bij de dailies",
    "",
    "Wat vul je in?",
    "Alleen de gele kolommen. De vragen en antwoorden komen automatisch uit de spelbestanden; die niet aanpassen.",
    "Rij 2 is een ingevuld voorbeeld en mag blijven staan of weg — hij wordt bij het inlezen overgeslagen.",
    "Eén foto per daily is genoeg. Kies bij 'Foto bij vraag' welke van de drie vragen de foto illustreert (q1, q2 of q3).",
    "Past er bij geen van de drie vragen een zinnige foto? Laat de rij dan leeg. Een irrelevante foto is slechter dan geen foto.",
    "",
    "Wat is een goede foto?",
    "Sfeer en herkenning, geen informatie. De foto mag laten zien wáár de vraag over gaat, maar niet helpen het getal te schatten.",
    "Goed: een piano bij 'hoeveel toetsen heeft een piano'. De foto toont het onderwerp, je telt er geen toetsen op.",
    "Fout: een foto waarop je het antwoord kunt aflezen of natellen, of een infographic met het getal erin.",
    "Twijfel je? Vul bij 'Verklapt het antwoord?' dan 'twijfel' in, dan kijken we er samen naar.",
    "Abstracte vragen (taal, wiskunde, percentages) hebben vaak geen goede foto. Overslaan is prima.",
    "",
    "Licentie — hier niet van afwijken",
    "Alleen bestanden met CC BY, CC BY-SA, CC0 of Public Domain. Niets anders, ook niet 'even van Google'.",
    "Neem de maker exact over zoals Commons hem noemt; bij CC BY en CC BY-SA is naamsvermelding een licentievoorwaarde.",
    "Zet de link naar de Commons-BESTANDSPAGINA (commons.wikimedia.org/wiki/File:...), niet de directe afbeeldings-URL.",
    "",
    "Zo zoek je op Wikimedia Commons",
    "1. Ga naar commons.wikimedia.org en zoek op het onderwerp in het Engels (bijv. 'grand piano keyboard').",
    "2. Open een bestand dat er goed uitziet en scroll naar het kader met licentie en auteur.",
    "3. Staat er CC BY / CC BY-SA / CC0 / Public domain? Kopieer dan de URL uit je adresbalk naar de kolom.",
    "4. Vul maker, licentie en een korte Nederlandse alt-tekst in (wat zie je op de foto, één zin).",
    "",
    "Klaar met een rij? Zet 'ja' in de kolom Akkoord. Alleen rijen met 'ja' worden straks ingeladen.",
]


if __name__ == "__main__":
    print(f"Geschreven: {build()}")
