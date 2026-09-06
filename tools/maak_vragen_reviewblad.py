#!/usr/bin/env python3
"""Bouwt het grote reviewblad voor de volledige vragenbank.

Eén ronde per vraag: is hij leuk, klopt het antwoord, staat er een bron bij, en
verdient hij een foto. Zo hoeft de bank maar één keer doorgelopen te worden in
plaats van vier keer voor elk aspect apart.

Volgorde is bewust: vragen die nu in een puzzel zitten staan bovenaan, dailies
eerst. Wie halverwege stopt, heeft daarmee automatisch het meest zichtbare deel
gedaan.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "vragen" / "1000+ vragen netjes gecategoriseerd.xlsx"
PUZZELS = ROOT / "netto_frontend_puzzles.js"
VERTALINGEN = ROOT / "netto_translations_en.js"
OUTPUT = ROOT / "vragen" / "vragen_review_compleet.xlsx"

FONT = "Arial"
KOP_FILL = PatternFill("solid", fgColor="14163B")
INVUL_FILL = PatternFill("solid", fgColor="FFFFCC")
DAILY_FILL = PatternFill("solid", fgColor="EEF1FF")

KOLOMMEN = [
    ("Nr", 6), ("In gebruik", 11), ("Categorie", 22),
    ("Vraag NL", 50), ("Vraag EN (zoekhulp)", 50), ("Antwoord", 11),
    ("Bron (bestaand)", 40),
    ("Bron (jouw aanvulling)", 40), ("Commons-fotolink", 40),
    ("Verwijderen", 11), ("Jouw opmerking", 26),
    ("Let op", 22),
]
INVULKOLOMMEN = (8, 9, 10, 11)


def laad_gebruik() -> dict[str, str]:
    """Per vraag: in welke spelmodus hij voorkomt."""
    src = PUZZELS.read_text(encoding="utf-8")
    data = json.loads(src[src.index("=") + 1:].rstrip().rstrip(";"))
    gebruik: dict[str, str] = {}
    for naam in ("library", "reserve", "daily"):  # daily als laatste: wint
        for puzzel in data.get(naam) or []:
            for slot in ("q1", "q2", "q3"):
                vraag = (puzzel.get(f"{slot}_label") or "").strip()
                if vraag:
                    gebruik[vraag] = "daily" if naam == "daily" else "puzzel"
    return gebruik


def main() -> None:
    vertalingen = json.loads(
        VERTALINGEN.read_text(encoding="utf-8").split("=", 1)[1].rstrip().rstrip(";")
    )
    gebruik = laad_gebruik()
    df = pd.read_excel(BANK, sheet_name="Alle vragen")
    df["Vraag NL"] = df["Vraag NL"].astype(str).str.strip()

    # Sorteren: eerst dailies, dan overige puzzelvragen, dan ongebruikt.
    # Binnen elke groep op categorie, zodat verwante vragen bij elkaar staan en
    # je in één ritme kunt doorlezen.
    volgorde = {"daily": 0, "puzzel": 1, "": 2}
    df["_gebruik"] = df["Vraag NL"].map(gebruik).fillna("")
    df["_sort"] = df["_gebruik"].map(volgorde)
    df = df.sort_values(["_sort", "Categorie", "Vraag NL"], kind="stable").reset_index(drop=True)

    wb = Workbook()
    ws = wb.active
    ws.title = "Vragen"
    ws.append([naam for naam, _ in KOLOMMEN])
    for i, (_, breedte) in enumerate(KOLOMMEN, start=1):
        ws.column_dimensions[get_column_letter(i)].width = breedte
        cel = ws.cell(1, i)
        cel.font = Font(name=FONT, bold=True, color="FFFFFF", size=10)
        cel.fill = KOP_FILL
        cel.alignment = Alignment(vertical="center", wrap_text=True)
    ws.freeze_panes = "D2"

    # Kolomnamen bevatten spaties, dus itertuples geeft onbruikbare veldnamen;
    # dicts zijn hier duidelijker en breken niet bij een kolomwijziging.
    for nr, row in enumerate(df.to_dict("records"), start=1):
        vraag = row["Vraag NL"]
        bron = row.get("Bron EN")
        bron = "" if bron is None or pd.isna(bron) else str(bron)
        engels = vertalingen.get(vraag, "")
        soort = row["_gebruik"]

        opmerkingen = []
        if not bron:
            opmerkingen.append("geen bron")
        if not engels:
            opmerkingen.append("geen EN-vertaling")

        ws.append([
            nr,
            {"daily": "daily", "puzzel": "puzzel"}.get(soort, "—"),
            row["Categorie"], vraag, engels, row["Antwoord"], bron,
            "", "", "", "",
            " · ".join(opmerkingen),
        ])
        rij = ws.max_row
        for i in range(1, len(KOLOMMEN) + 1):
            cel = ws.cell(rij, i)
            cel.font = Font(name=FONT, size=10)
            cel.alignment = Alignment(vertical="top", wrap_text=True)
            if i in INVULKOLOMMEN:
                cel.fill = INVUL_FILL
            elif soort == "daily":
                cel.fill = DAILY_FILL

    uitleg = wb.create_sheet("Uitleg")
    for regel in UITLEG:
        uitleg.append([regel])
    uitleg.column_dimensions["A"].width = 104
    for rij in range(1, uitleg.max_row + 1):
        cel = uitleg.cell(rij, 1)
        cel.font = Font(name=FONT, size=11, bold=cel.value in KOPJES)
        cel.alignment = Alignment(wrap_text=True, vertical="top")

    wb.save(OUTPUT)
    telling = df["_gebruik"].value_counts()
    print(f"Geschreven: {OUTPUT.relative_to(ROOT)}")
    print(f"  {len(df)} vragen | daily: {telling.get('daily', 0)} | "
          f"puzzel: {telling.get('puzzel', 0)} | ongebruikt: {telling.get('', 0)}")


KOPJES = {
    "Wat vul je in?", "Over de foto's", "Over de bronnen", "Over de volgorde",
}

UITLEG = [
    "Vragenbank — volledige review",
    "",
    "Over de volgorde",
    "Bovenaan staan de vragen die nu in een daily zitten (lichtblauw), daarna de vragen die in een",
    "andere puzzel zitten, en onderaan de vragen die nergens gebruikt worden. Binnen elke groep",
    "gesorteerd op categorie, zodat verwante vragen bij elkaar staan.",
    "Stop je halverwege, dan heb je automatisch het deel gedaan dat spelers ook echt zien.",
    "",
    "Wat vul je in?",
    "Alleen de gele kolommen. De rest komt uit de bestanden en wordt overschreven bij hergenereren.",
    "  Bron (jouw aanvulling) — een URL waarmee het antwoord te controleren is.",
    "  Commons-fotolink — zie hieronder.",
    "  Verwijderen — 'ja' als de vraag weg moet. Saai, onduidelijk, of antwoord niet vast te stellen.",
    "  Jouw opmerking — alles wat je kwijt wil; ik lees ze allemaal.",
    "",
    "Over de bronnen",
    "In de kolom 'Bron (bestaand)' staat wat er al is. Klopt die, dan hoef je niets te doen.",
    "Ontbreekt hij of deugt hij niet, vul dan je eigen bron in. In 'Let op' staat waar er geen bron is.",
    "Het Engels is een zoekhulp, geen waarheid: die vertalingen zijn machinegemaakt en soms fout.",
    "Controleer het feit dus tegen de Nederlandse vraag, niet tegen de Engelse.",
    "",
    "Over de foto's",
    "ALLEEN links naar Wikimedia Commons, en wel naar de bestandspagina:",
    "  https://commons.wikimedia.org/wiki/File:Naam_van_bestand.jpg",
    "Dus niet de directe afbeeldings-URL, en geen plaatjes van elders op internet.",
    "Reden: op Commons staat de licentie bij het bestand, en die haal ik automatisch op. Maker,",
    "licentie en bronvermelding komen dan vanzelf goed op de site. Bij een willekeurige link van",
    "internet kan niemand dat controleren, ook ik niet.",
    "Ik weiger automatisch alles wat geen CC BY, CC BY-SA, CC0 of publiek domein is; daar hoef jij",
    "dus niet op te letten.",
    "",
    "Waar je bij een foto op let: hij mag laten zien WAAR de vraag over gaat, maar niet helpen het",
    "GETAL te schatten. Een piano bij 'hoeveel toetsen heeft een piano' is goed. Een foto waarop je",
    "het antwoord kunt natellen of aflezen niet.",
    "Niet elke vraag hoeft een foto. Bij abstracte vragen (taal, wiskunde, percentages) laat je hem leeg.",
]


if __name__ == "__main__":
    main()
