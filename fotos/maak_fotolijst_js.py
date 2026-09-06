#!/usr/bin/env python3
"""Genereert js/daily-photos.js uit de mediacatalogus.

De sfeerfoto's komen van Wikimedia Commons onder CC BY, CC BY-SA, CC0 of
publiek domein. Bij de eerste twee is naamsvermelding een licentievoorwaarde,
geen nettigheid, dus de bronvermelding moet mee naar de frontend in plaats van
alleen in een reviewbestand te blijven staan.

Draai dit opnieuw zodra er foto's bij komen of af gaan.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "fotos" / "question_media_pilot.xlsx"
ASSET_DIR = ROOT / "fotos" / "assets"
OUTPUT = ROOT / "js" / "daily-photos.js"

HEADER = """// Netto frontend module.
// Loaded as a classic script so the existing shared global scope stays intact.

// GEGENEREERD door fotos/maak_fotolijst_js.py — niet met de hand bijwerken.
//
// Gedeelde fotolijst voor de daily. Zowel het spel (sfeerfoto-rotatie) als het
// adminscherm (foto toewijzen) gebruiken deze lijst.
//
// De bronvermelding staat er bewust bij: deze foto's komen van Wikimedia
// Commons onder CC BY, CC BY-SA, CC0 of publiek domein, en bij de eerste twee
// is naamsvermelding een licentievoorwaarde.
"""


def main() -> None:
    ws = openpyxl.load_workbook(CATALOG, read_only=True)["Media"]
    header = [c for c in next(ws.iter_rows(min_row=1, max_row=1, values_only=True))]
    idx = {name: i for i, name in enumerate(header)}

    op_schijf = {p.name for p in ASSET_DIR.iterdir() if p.is_file()}
    fotos = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        bestand = os.path.basename(str(row[idx["image_file"]] or ""))
        if bestand not in op_schijf:
            continue
        titel = str(row[idx["image_title"]] or "").removesuffix(".jpg")
        maker = str(row[idx["creator"]] or "onbekende maker")
        licentie = str(row[idx["license"]] or "licentie onbekend")
        fotos.append({
            "file": bestand,
            # Titel, maker en licentie samen; de bron-URL hangt eronder als link.
            "credit": f"{titel} · {maker} · {licentie}",
            "source": str(row[idx["source_url"]] or ""),
        })

    ontbreekt = sorted(op_schijf - {f["file"] for f in fotos})
    body = ",\n".join(
        "  " + json.dumps(f, ensure_ascii=False) for f in fotos
    )
    OUTPUT.write_text(
        HEADER
        + f"window.NETTO_DAILY_PHOTOS = [\n{body},\n];\n\n"
        + "window.NETTO_DAILY_PHOTO_DIR = 'fotos/assets/';\n",
        encoding="utf-8",
    )
    print(f"Geschreven: {OUTPUT.relative_to(ROOT)} ({len(fotos)} foto's met bronvermelding)")
    if ontbreekt:
        # Zonder bronvermelding mag een foto niet mee; anders staat hij zonder
        # naamsvermelding online.
        print(f"LET OP: {len(ontbreekt)} bestand(en) zonder catalogusrij, niet opgenomen:")
        for naam in ontbreekt[:10]:
            print("  -", naam)


if __name__ == "__main__":
    main()
