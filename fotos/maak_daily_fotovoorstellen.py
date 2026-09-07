#!/usr/bin/env python3
"""Zoekt automatisch fotovoorstellen bij de dailies op Wikimedia Commons.

Hergebruikt de Commons-logica uit maak_fotocatalogus.py (zoeken, licentie
filteren, metadata en download), maar dan per daily in plaats van per
library-puzzel.

Het doel is niet om de keuze te maken, maar om die voor te bereiden: per daily
één kandidaat met complete bronvermelding, zodat een redacteur alleen nog
goedkeurt of afkeurt.

Gebruik:
    python fotos/maak_daily_fotovoorstellen.py --limit 5      # proef
    python fotos/maak_daily_fotovoorstellen.py                # alle dailies
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import maak_fotocatalogus as catalogus  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "fotos" / "assets" / "daily"

# Vraagwoorden, eenheden en werkwoorden dragen niets bij aan een beeldzoekopdracht.
STOPWORDS = {
    # vraag- en functiewoorden
    'how', 'many', 'much', 'what', 'which', 'who', 'where', 'when',
    'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for', 'from', 'by', 'with',
    'is', 'are', 'was', 'were', 'does', 'do', 'did', 'has', 'have', 'had', 'be',
    'there', 'it', 'its', 'you', 'your', 'they', 'their', 'about', 'approximately',
    'roughly', 'total', 'up', 'and', 'or', 'per', 'into', 'out', 'that', 'this',
    'these', 'those', 'each', 'every', 'all', 'one', 'ever', 'average', 'start',
    'end', 'most', 'least', 'standard', 'current',
    # eenheden en hoeveelheden
    'percent', 'percentage', 'year', 'years', 'day', 'days', 'hour', 'hours',
    'minute', 'minutes', 'second', 'seconds', 'week', 'weeks', 'month', 'months',
    'meter', 'meters', 'metre', 'metres', 'kilometer', 'kilometers', 'kilometre',
    'kilometres', 'km', 'centimeter', 'centimeters', 'centimetres', 'mile', 'miles',
    'kilogram', 'kilograms', 'kg', 'gram', 'grams', 'ton', 'tons', 'tonnes',
    'liter', 'liters', 'litre', 'litres', 'degrees', 'thousand', 'million',
    'billion', 'number', 'numbers', 'amount',
    # werkwoorden die in deze vraagvorm terugkeren
    'take', 'takes', 'took', 'travel', 'travels', 'contains', 'contain', 'consists',
    'consist', 'counts', 'count', 'weigh', 'weighs', 'make', 'makes', 'get', 'gets',
    'last', 'lasted', 'held', 'go', 'goes', 'need', 'needs', 'use', 'uses',
    'measure', 'measures', 'reach', 'reaches', 'live', 'lives', 'fit', 'fits',
    # bijvoeglijke maatwoorden
    'long', 'deep', 'high', 'wide', 'tall', 'big', 'large', 'small', 'longest',
    'deepest', 'highest', 'widest', 'tallest', 'biggest', 'largest', 'smallest',
}


def load_dailies() -> list[dict]:
    src = (ROOT / "data/netto_frontend_puzzles.js").read_text(encoding="utf-8")
    data = json.loads(src[src.index("=") + 1:].rstrip().rstrip(";"))
    return sorted(data["daily"], key=lambda d: d.get("date") or "")


def load_translations() -> dict[str, str]:
    src = (ROOT / "data/netto_translations_en.js").read_text(encoding="utf-8")
    return json.loads(src[src.index("=") + 1:].rstrip().rstrip(";"))


def search_term_for(question_nl: str, translations: dict[str, str]) -> str:
    """Leidt een Engelse zoekterm af uit een Nederlandse vraag.

    Eigennamen (Antarctica, Mayflower, Lake Tanganyika) zijn veruit het sterkste
    signaal voor Commons, dus die krijgen voorrang. Zonder eigennaam vallen we
    terug op de overgebleven inhoudswoorden.
    """
    english = translations.get(question_nl, question_nl)
    # Bezitsvormen leveren onbruikbare zoektermen op ("whale's" vindt niets).
    english = re.sub(r"'s\b", "", english)
    woorden = re.findall(r"[A-Za-z][A-Za-z-]+", english)
    if not woorden:
        return english[:60]

    # Het eerste woord is altijd een vraagwoord; hoofdletters daar zeggen niets.
    eigennamen = [w for w in woorden[1:] if w[0].isupper()]
    if eigennamen:
        return " ".join(eigennamen[:3])

    # Zonder eigennaam: in deze vraagvorm staat het onderwerp achteraan
    # ("How many kilograms does a blue whale tongue weigh" -> "blue whale tongue"),
    # dus de laatste inhoudswoorden zijn bruikbaarder dan de eerste.
    inhoud = [w for w in woorden if w.casefold() not in STOPWORDS]
    return " ".join(inhoud[-3:]) if inhoud else english[:60]


def slot_keuzes(worksheet: Path | None) -> dict[int, str]:
    """Leest per daily welk vraagslot een foto moet krijgen, indien ingevuld."""
    if not worksheet or not worksheet.exists():
        return {}
    try:
        import openpyxl
        ws = openpyxl.load_workbook(worksheet, read_only=True)["Daily foto's"]
    except Exception:
        return {}
    keuzes = {}
    for row in ws.iter_rows(min_row=3, values_only=True):
        nummer, slot = row[0], row[8]
        if isinstance(nummer, int) and isinstance(slot, str) and slot.strip():
            keuzes[nummer] = slot.strip().lower()
    return keuzes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="0 = alle dailies")
    parser.add_argument("--worksheet", type=Path, default=None,
                        help="Ingevuld werkblad, voor de slotkeuze per daily")
    args = parser.parse_args()

    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    dailies = load_dailies()
    if args.limit:
        dailies = dailies[:args.limit]
    translations = load_translations()
    keuzes = slot_keuzes(args.worksheet)

    resultaten = []
    for daily in dailies:
        nummer = daily.get("number")
        slot = keuzes.get(nummer, "q1")
        vraag = daily.get(f"{slot}_label") or daily.get("q1_label") or ""
        term = search_term_for(vraag, translations)
        regel = {"nummer": nummer, "datum": daily.get("date"), "slot": slot,
                 "vraag": vraag, "zoekterm": term}
        try:
            kandidaten = catalogus.choose_commons_candidates(term)
            if not kandidaten:
                regel["status"] = "geen kandidaat gevonden"
            else:
                item = kandidaten[0]
                bestand = ASSET_DIR / f"daily-{nummer:03d}.jpg"
                catalogus.download_image_item(item, bestand)
                regel.update(
                    status="ok",
                    titel=str(item.get("title") or ""),
                    bestand=str(bestand.relative_to(ROOT)).replace("\\", "/"),
                    maker=str(item.get("creator") or "onbekend"),
                    licentie=str(item.get("license") or "onbekend"),
                    bron=str(item.get("foreign_landing_url") or item.get("detail_url") or ""),
                )
        except Exception as err:  # netwerk, licentie, download
            regel["status"] = f"mislukt: {type(err).__name__}: {str(err)[:70]}"
        resultaten.append(regel)
        print(f"#{nummer} [{slot}] {term!r} -> {regel['status']}"
              + (f" · {regel.get('titel','')[:50]}" if regel.get("titel") else ""))

    gelukt = sum(1 for r in resultaten if r["status"] == "ok")
    print(f"\n{gelukt}/{len(resultaten)} voorstellen gevonden")
    (ROOT / "fotos" / "daily_fotovoorstellen.json").write_text(
        json.dumps(resultaten, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Details: fotos/daily_fotovoorstellen.json")


if __name__ == "__main__":
    main()
