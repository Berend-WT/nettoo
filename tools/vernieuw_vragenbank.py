#!/usr/bin/env python3
"""Vernieuwt de vragenbank: dedupliceert echte duplicaten (zelfde feit, andere
formulering) en herstelt fout-gecategoriseerde/inconsistente categorienamen.

Alle wijzigingen zijn gebaseerd op handmatig geverifieerde clusters (zie
DUPLICATE_CLUSTERS / CATEGORY_FIXES hieronder), niet op een blinde threshold —
elke fuzzy-match kandidaat is eerst inhoudelijk beoordeeld om te voorkomen dat
bijvoorbeeld "hoeveel landen grenzen aan Polen/Soedan" (toevallig zelfde
antwoord, andere landen) als duplicaat wordt weggegooid.
"""
from pathlib import Path
from datetime import date
import openpyxl

SRC = Path("vragen/1000+ vragen netjes gecategoriseerd.xlsx")

# Elke sublist = 1 cluster van rijen (Excel-rijnummers) die hetzelfde feit
# beschrijven. Eerste rij in de lijst wordt bewaard, de rest wordt verwijderd.
DUPLICATE_CLUSTERS = [
    [1095, 1517],   # honkbal innings
    [1385, 1501],   # groene anaconda lengte
    [878, 1241],    # soera's Koran (typo-variant)
    [115, 1541],    # safety punten American football
    [78, 1357],     # landen Zuid-Amerika
    [79, 1276],     # landen Afrika
    [206, 1168],    # Eiffeltoren traptreden
    [36, 991],      # Afsluitdijk lengte
    [51, 698],      # schaken pionnen
    [17, 764, 49],  # schaakbord vakken/speelvelden
    [116, 1094, 1511],  # spelers per honkbalteam op het veld
    [385, 1146],    # ondertekenaars Onafhankelijkheidsverklaring
    [15, 1524],     # Olympische mannen-hordensprint afstand
    [683, 1182],    # speelminuten voetbalwedstrijd
    [356, 1055],    # kustlengte Waddeneilanden
    [724, 1129],    # seizoenen Friends
    [888, 1149],    # landen met euro als munt
    [388, 1089],    # aantal presidenten VS
    [897, 1141],    # zetels/leden Amerikaanse Senaat
    [682, 1525],    # etappes Tour de France
    [781, 1214],    # hoofdeilanden Japan
    [684, 1344],    # punten try rugby union
    [608, 1172],    # kamers Buckingham Palace
    [1336, 1458],   # slaapuren koala
    [904, 1510],    # spelers waterpoloteam
    [903, 1514],    # spelers volleybalteam
    [226, 287],     # diameter maan
    [697, 1520],    # holes standaard golfbaan/-ronde
    [1228, 1229],   # kamers Forbidden City
    [455, 1176],    # geboden Tien Geboden
]

# Categorienaam-varianten die puur spelling/interpunctie verschillen -> canonieke naam
CATEGORY_RENAME = {
    "Politiek & recht": "Politiek en recht",
    "Eten en drinken": "Eten & drinken",
}

# Rijen die inhoudelijk in de verkeerde categorie stonden (categorie-tekst matcht niet
# met het onderwerp van de vraag) -> canonieke categorie op basis van de vraaginhoud
CONTENT_BASED_FIXES = {
    # was 'Economie': geometrie-vraag
    "Hoeveel zijden heeft een octagoon?": "Wiskunde",
    # was 'Bouwwerken': kanalen zijn infrastructuur, geen los "Bouwwerken"-vakje (2 rijen totaal)
    "Wat is de lengte van het Panamakanaal van de Atlantische naar de Stille Oceaan in km?": "Gebouwen en infrastructuur",
    "Wat is de lengte van het Suezkanaal in Egypte in kilometers?": "Gebouwen en infrastructuur",
    # was 'Wetenschap' (generieke restcategorie met maar 3 vragen)
    "Hoeveel strepen staan er op de vlag van de Verenigde Staten?": "Geschiedenis",
    "Hoeveel actieve vulkanen zijn er op aarde naar schatting?": "Geografie",
    # was 'Natuurverschijnselen' (2 rijen, hoort bij geografie)
    "Hoeveel meter hoog is de Victoriawatervallen afgerond op tientallen?": "Geografie",
    "Hoeveel meter breed is de Victoriawatervallen bij benadering (in honderden meters afgerond)?": "Geografie",
    # was 'Nederland' (enkelvoud-typo van de bestaande categorie 'Nederlands')
    "Hoeveel provincies heeft Nederland?": "Nederlands",
    "Hoeveel windmolens staan er op de werelderfgoedlocatie Kinderdijk?": "Nederlands",
    "Hoeveel zuilen heeft het Rijksmuseum aan de voorgevel?": "Nederlands",
    "Wat is de autorij-afstand van Amsterdam naar Rome in km?": "Nederlands",
}

# Vraagtekst met per ongeluk meegenomen review-notitie -> gecorrigeerde tekst
QUESTION_TEXT_FIXES = {
    "In welk jaar werd de Eerste Franse Republiek uitgeroepen (tot science hoort dit niet)?":
        "In welk jaar werd de Eerste Franse Republiek uitgeroepen?",
}


def main():
    wb = openpyxl.load_workbook(SRC)
    ws = wb["Alle vragen"]
    headers = [c.value for c in ws[1]]
    col = {name: i + 1 for i, name in enumerate(headers)}

    # --- 1. Vraagtekst-fix (review-notitie eruit) ---
    for row in range(2, ws.max_row + 1):
        cell = ws.cell(row, col["Vraag NL"])
        if cell.value in QUESTION_TEXT_FIXES:
            cell.value = QUESTION_TEXT_FIXES[cell.value]

    # --- 2. Categorie-fixes ---
    n_cat_fixed = 0
    for row in range(2, ws.max_row + 1):
        cat_cell = ws.cell(row, col["Categorie"])
        q_cell = ws.cell(row, col["Vraag NL"])
        if cat_cell.value in CATEGORY_RENAME:
            cat_cell.value = CATEGORY_RENAME[cat_cell.value]
            n_cat_fixed += 1
        # content-based fix matcht op de ORIGINELE vraagtekst; check zowel voor
        # als na de tekstfix hierboven
        q_text = q_cell.value
        if q_text in CONTENT_BASED_FIXES:
            cat_cell.value = CONTENT_BASED_FIXES[q_text]
            n_cat_fixed += 1

    # --- 3. Duplicaten verwijderen ---
    rows_to_remove = set()
    removal_log = []  # (verwijderde_rij, behouden_rij, vraag_verwijderd, vraag_behouden, antwoord)
    for cluster in DUPLICATE_CLUSTERS:
        keep = cluster[0]
        keep_q = ws.cell(keep, col["Vraag NL"]).value
        keep_a = ws.cell(keep, col["Antwoord"]).value
        for r in cluster[1:]:
            rows_to_remove.add(r)
            removal_log.append((
                r, keep,
                ws.cell(r, col["Vraag NL"]).value,
                keep_q,
                keep_a,
            ))

    # Verwijder van hoog naar laag rijnummer zodat rijverschuiving de rest niet breekt
    for r in sorted(rows_to_remove, reverse=True):
        ws.delete_rows(r, 1)

    # --- 4. Log-sheets schrijven ---
    for name in ("Verwijderde duplicaten", "Categorie-fixes log"):
        if name in wb.sheetnames:
            del wb[name]

    dup_ws = wb.create_sheet("Verwijderde duplicaten")
    dup_ws.append(["Verwijderde vraag", "Antwoord", "Behouden als (duplicaat van)", "Datum"])
    for r, keep, q_removed, q_keep, ans in removal_log:
        dup_ws.append([q_removed, ans, q_keep, str(date.today())])

    cat_ws = wb.create_sheet("Categorie-fixes log")
    cat_ws.append(["Type", "Vraag / oude naam", "Nieuwe categorie", "Datum"])
    for old, new in CATEGORY_RENAME.items():
        cat_ws.append(["Naam-normalisatie", old, new, str(date.today())])
    for q, new in CONTENT_BASED_FIXES.items():
        cat_ws.append(["Herclassificatie (verkeerde categorie)", q, new, str(date.today())])
    for old, new in QUESTION_TEXT_FIXES.items():
        cat_ws.append(["Vraagtekst gecorrigeerd", f"{old}  ->  {new}", "", str(date.today())])

    # --- 5. Overzicht bijwerken ---
    ov = wb["Overzicht"]
    next_row = ov.max_row + 2
    ov.cell(next_row, 1, "Vernieuwing " + str(date.today()))
    ov.cell(next_row + 1, 1, "Duplicaten verwijderd")
    ov.cell(next_row + 1, 2, len(rows_to_remove))
    ov.cell(next_row + 2, 1, "Categorieën gecorrigeerd/genormaliseerd")
    ov.cell(next_row + 2, 2, n_cat_fixed)
    ov.cell(next_row + 3, 1, "Totaal vragen na opschoning")
    ov.cell(next_row + 3, 2, ws.max_row - 1)

    wb.save(SRC)
    print(f"Duplicaten verwijderd: {len(rows_to_remove)}")
    print(f"Categorie-fixes: {n_cat_fixed}")
    print(f"Resterend aantal vragen: {ws.max_row - 1}")


if __name__ == "__main__":
    main()
