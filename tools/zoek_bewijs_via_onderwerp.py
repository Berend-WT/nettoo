# -*- coding: utf-8 -*-
"""Netto — zoek bewijszin én bron via het onderwerp op Wikipedia.

Draaien:  python tools/zoek_bewijs_via_onderwerp.py

zoek_bewijszinnen.py haalt de pagina op die al bij de vraag stond. Voor 29
vragen levert dat niets: de pagina blokkeert (403), bouwt zichzelf met
JavaScript op, of noemt het getal alleen in een plaatje. Dat zijn stuk voor stuk
feiten die op Wikipedia gewoon in een zin staan — hoeveel poten een krab heeft,
hoeveel toetsen een piano.

Dit script zoekt daarom het artikel over het ONDERWERP van de vraag en haalt
daar de zinnen uit waarin het antwoord staat. Het schrijft niets naar de
vragenbank: de keuze blijft mensenwerk, want juist automatisch kiezen op "het
getal staat op de pagina" heeft de fouten veroorzaakt die we opruimen.
"""

import json
import os
import re
import sys
import time
import urllib.parse

import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zoek_hoofdafbeeldingen as zh
import zoek_onderwerpafbeeldingen as zo
import zoek_bewijszinnen as zb

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
UIT = os.path.join(WORTEL, 'vragen', 'bewijszinnen_via_onderwerp.json')
PAUZE = 0.6


def extract(taal, titel):
    d = zh.haal(f'{taal}.wikipedia.org', {
        'action': 'query', 'format': 'json', 'formatversion': '2',
        'titles': titel, 'prop': 'extracts', 'explaintext': '1',
    })
    paginas = (d.get('query', {}) or {}).get('pages', []) or []
    return paginas[0].get('extract') if paginas else None


def main():
    blad = openpyxl.load_workbook(REVIEW, read_only=True)['Vragen']
    rijen = list(blad.iter_rows(values_only=True))
    k = {naam: n for n, naam in enumerate(rijen[0])}

    doel = []
    for rij in rijen[1:]:
        if 'bestaande bron opgehaald' not in zb.plat(rij[k['Bewijszin']]):
            continue
        try:
            antwoord = int(rij[k['Antwoord']])
        except (TypeError, ValueError):
            continue
        doel.append((int(rij[k['Nr']]), str(rij[k['Vraag NL']]), antwoord))

    print(f'{len(doel)} vragen via het onderwerp opzoeken ...')
    uitkomst = []
    for teller, (nr, vraag, antwoord) in enumerate(doel, start=1):
        beste = None
        for term in zo.onderwerpen(vraag)[:3]:
            for taal in ('nl', 'en'):
                titel = zo.artikel(taal, term)
                time.sleep(PAUZE)
                if not titel or re.search(r'\((doorverwijspagina|disambiguation)\)', titel, re.I):
                    continue
                tekst = extract(taal, titel)
                time.sleep(PAUZE)
                if not tekst:
                    continue
                zinnen = zb.zinnen_met(tekst, antwoord)
                zinnen.sort(key=lambda z: -zb.raakvlak(vraag, z))
                if zinnen:
                    beste = {
                        'artikel': f'https://{taal}.wikipedia.org/wiki/'
                                   + urllib.parse.quote(titel.replace(' ', '_')),
                        'gezocht': term,
                        'zinnen': [{'zin': ' '.join(z.split()),
                                    'raakvlak': zb.raakvlak(vraag, z)} for z in zinnen[:3]],
                    }
                    break
            if beste:
                break
        uitkomst.append({'nr': nr, 'vraag': vraag, 'antwoord': antwoord,
                         **(beste or {'artikel': None, 'gezocht': None, 'zinnen': []})})
        merk = (beste['gezocht'] if beste else '-')[:28]
        print(f'  {teller:>3}/{len(doel)} Nr {nr:<5} {merk:<30} '
              f'{len(uitkomst[-1]["zinnen"])} zin(nen)  {vraag[:44]}')
        with open(UIT, 'w', encoding='utf-8') as f:
            json.dump(uitkomst, f, ensure_ascii=False, indent=1)

    raak = sum(1 for r in uitkomst if r['zinnen'])
    print(f'\n{raak} van {len(uitkomst)} met kandidaat -> {os.path.relpath(UIT, WORTEL)}')


if __name__ == '__main__':
    main()
