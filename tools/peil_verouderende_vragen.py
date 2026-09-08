# -*- coding: utf-8 -*-
"""Netto — geef snel bewegende vragen een peiljaar.

Draaien:  python tools/peil_verouderende_vragen.py [--schrijf]

Negenveertig vragen dragen de markering "veroudert". Bij de meeste is dat geen
probleem: wereldproductie van tarwe of koper schommelt rond een vast getal en
"ongeveer 785 miljoen ton" blijft jaren bruikbaar.

Bij een handvol is het wel een probleem, en groter dan gedacht. Het aantal
bekende manen van Saturnus stond op 146, maar de IAU erkende in maart 2025 in
een klap 128 nieuwe en in maart 2026 nog eens elf: 285. Jupiter ging van 95 naar
115. The Simpsons stond op 35 seizoenen; dat zijn er nu 37, en seizoen 38 begint
eind september 2026.

Die vragen krijgen hier een peiljaar in de tekst. Daarmee is het antwoord niet
langer "op dit moment juist" maar permanent juist, en is bij de volgende ronde
te zien wanneer het bijgewerkt moet worden.

Let op: waar het antwoord meeverandert breekt de som van elke puzzel waarin de
vraag zit. Die worden bijgeschreven in vragen/puzzels_om_te_herbouwen.xlsx; de
puzzelbestanden blijven ongemoeid.
"""

import json
import os
import shutil
import sys
from datetime import date

# De Windows-console draait op cp1252 en struikelt over tekens als het subscript
# in CO₂. Voor de leesbaarheid van de proefdraai schakelen we naar UTF-8.
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
HERBOUW = os.path.join(WORTEL, 'vragen', 'puzzels_om_te_herbouwen.xlsx')
DATA = os.path.join(WORTEL, 'data')

BESTANDEN = ['netto_frontend_puzzles.js', 'netto_breinkrakers.js',
             'netto_race_sets.js', 'netto_race_pool.js']

# nr: (nieuwe vraagtekst, nieuw antwoord of None, bron, toelichting)
PEIL = {
    514: ('Hoeveel bekende manen heeft Saturnus (stand 2026)?', 285,
          'https://en.wikipedia.org/wiki/Moons_of_Saturn',
          'De IAU erkende in maart 2025 128 nieuwe manen (totaal 274) en in maart 2026 nog '
          'elf: 285. Het oude antwoord 146 was de stand van 2023.'),
    516: ('Hoeveel bekende manen heeft Saturnus officieel (stand 2026)?', 285,
          'https://en.wikipedia.org/wiki/Moons_of_Saturn',
          'Zelfde als vraag 514; dubbel in de bank.'),
    515: ('Hoeveel bekende manen heeft de planeet Jupiter officieel (stand 2026)?', 115,
          'https://en.wikipedia.org/wiki/Moons_of_Jupiter',
          'De IAU erkende in maart en april 2026 achttien nieuwe manen; totaal 115. Het oude '
          'antwoord 95 was de stand van 2023.'),
    1423: ('Hoeveel bekende manen heeft Jupiter (stand 2026)?', 115,
           'https://en.wikipedia.org/wiki/Moons_of_Jupiter',
           'Zelfde als vraag 515; dubbel in de bank.'),
    207: ('Hoeveel seizoenen van The Simpsons waren er uitgezonden (stand 2026)?', 37,
          'https://en.wikipedia.org/wiki/The_Simpsons',
          'Zevenendertig seizoenen uitgezonden; seizoen 38 begint op 27 september 2026. Het '
          'oude antwoord 35 was de stand van 2024.'),
    369: ('Hoeveel restaurants had McDonald’s wereldwijd eind 2024?', 43477,
          'https://corporate.mcdonalds.com/content/dam/sites/corp/nfl/pdf/Restaurants%20by%20Market%202024.pdf',
          'Het jaarverslag geeft 43.477 restaurants eind 2024. Met een vast peiljaar veroudert '
          'dit antwoord niet meer.'),
    1090: ('Hoeveel delen CO₂ per miljoen delen lucht mat NASA in 2024?', None,
           'https://climate.nasa.gov/vital-signs/carbon-dioxide/',
           'Met een peiljaar erbij hoort 425 ppm bij 2024 en veroudert het antwoord niet meer. '
           'De concentratie stijgt met ruim twee ppm per jaar.'),
    132: ('Hoeveel boeken bevat de gepubliceerde hoofdserie A Song of Ice and Fire (stand 2026)?',
          None, 'https://en.wikipedia.org/wiki/A_Song_of_Ice_and_Fire',
          'Vijf delen verschenen; The Winds of Winter is nog niet uit.'),
    1270: ('Hoeveel landen telt de NAVO (stand 2026)?', None,
           'https://www.nato.int/cps/en/natohq/topics_52044.htm',
           'Tweeendertig sinds Zweden in 2024 toetrad. Dubbel met vraag 428.'),
}


def laad(pad):
    t = open(pad, encoding='utf-8').read()
    i = t.index('=', t.index('window.')) + 1
    return json.loads(t[i:].strip().rstrip(';'))


def vragen_in(p):
    uit = []
    for i in (1, 2, 3, 4):
        genest = p.get(f'q{i}')
        if isinstance(genest, dict) and 'label' in genest:
            uit.append(genest['label'])
        elif f'q{i}_label' in p:
            uit.append(p[f'q{i}_label'])
    return uit


def alle_puzzels(data):
    if isinstance(data, list):
        return [('', p) for p in data]
    uit = []
    for sleutel, lijst in data.items():
        if isinstance(lijst, list):
            uit += [(sleutel, p) for p in lijst if isinstance(p, dict)]
    return uit


def main():
    schrijf = '--schrijf' in sys.argv
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    oud_label = {int(r['Nr']): str(r['Vraag NL']) for _, r in d.iterrows()}
    oud_antw = {int(r['Nr']): r['Antwoord'] for _, r in d.iterrows()}

    breekt = {oud_label[nr]: nr for nr, (_, a, _, _) in PEIL.items()
              if a is not None and nr in oud_label}

    print('Peiljaar toegevoegd:')
    for nr, (tekst, antw, _, _) in PEIL.items():
        was = oud_antw.get(nr)
        merk = f'  {was} -> {antw}' if antw is not None else '  (antwoord blijft)'
        print(f'  {nr:5d}{merk}')
        print(f'         {tekst}')

    rijen = []
    for naam in BESTANDEN:
        data = laad(os.path.join(DATA, naam))
        for sleutel, p in alle_puzzels(data):
            for label in vragen_in(p):
                if label in breekt:
                    nr = breekt[label]
                    rijen.append({
                        'Bestand': naam.replace('netto_', '').replace('.js', ''),
                        'Lijst': sleutel, 'Puzzel': p.get('id'),
                        'Datum': p.get('date', ''),
                        'Som': p.get('calculation') or p.get('formula', ''),
                        'Vraag Nr': nr, 'Vraag': label,
                        'Oud antwoord': oud_antw.get(nr),
                        'Vervangers met dat antwoord': 0,
                        'Advies': 'peiljaar toegevoegd, antwoord bijgewerkt',
                    })
    nieuw = pd.DataFrame(rijen)
    print(f'\npuzzels waarvan de som hierdoor breekt: {len(nieuw)}')
    if len(nieuw):
        print(nieuw.groupby('Bestand').size().to_string())

    if not schrijf:
        print('\n(proefdraai — voeg --schrijf toe om op te slaan)')
        return

    if len(nieuw):
        oud = pd.read_excel(HERBOUW, sheet_name='Te herbouwen')
        samen = pd.concat([oud, nieuw], ignore_index=True).drop_duplicates(
            subset=['Bestand', 'Lijst', 'Puzzel', 'Vraag Nr'])
        samen = samen.sort_values(['Bestand', 'Lijst', 'Puzzel'])
        samen.to_excel(HERBOUW, index=False, sheet_name='Te herbouwen')
        wb = load_workbook(HERBOUW)
        ws = wb['Te herbouwen']
        br = {'Bestand': 18, 'Lijst': 16, 'Puzzel': 16, 'Datum': 12, 'Som': 30,
              'Vraag Nr': 9, 'Vraag': 62, 'Advies': 34}
        for i, k in enumerate(samen.columns, start=1):
            ws.column_dimensions[get_column_letter(i)].width = br.get(k, 16)
            c = ws.cell(row=1, column=i)
            c.font = Font(name='Arial', bold=True, color='FFFFFF', size=11)
            c.fill = PatternFill('solid', fgColor='1F3864')
            c.alignment = Alignment(vertical='center', wrap_text=True)
        ws.row_dimensions[1].height = 30
        for rij in range(2, ws.max_row + 1):
            for kol in range(1, len(samen.columns) + 1):
                ws.cell(row=rij, column=kol).font = Font(name='Arial', size=10)
                ws.cell(row=rij, column=kol).alignment = Alignment(
                    vertical='top', wrap_text=samen.columns[kol - 1] == 'Vraag')
        ws.freeze_panes = 'A2'
        ws.auto_filter.ref = f'A1:{get_column_letter(len(samen.columns))}{ws.max_row}'
        wb.save(HERBOUW)

    shutil.copy2(REVIEW, os.path.join(
        os.path.dirname(REVIEW),
        f'_backup_peiljaar_{date.today():%Y-%m-%d}_vragen_review_compleet.xlsx'))
    boek = load_workbook(REVIEW)
    blad = boek['Vragen']
    kol = [c.value for c in blad[1]]
    i_v = kol.index('Vraag NL') + 1
    i_a = kol.index('Antwoord') + 1
    i_b = kol.index('Bron (geverifieerd)') + 1
    i_w = kol.index('Bewijszin') + 1
    i_s = kol.index('Status oude bron') + 1
    i_l = kol.index('Let op') + 1

    for rij in range(2, blad.max_row + 1):
        nr = blad.cell(row=rij, column=1).value
        if nr not in PEIL:
            continue
        tekst, antw, bron, toelichting = PEIL[nr]
        was_v = blad.cell(row=rij, column=i_v).value
        was_a = blad.cell(row=rij, column=i_a).value
        blad.cell(row=rij, column=i_v).value = tekst
        blad.cell(row=rij, column=i_b).value = bron
        blad.cell(row=rij, column=i_w).value = toelichting[:400]
        blad.cell(row=rij, column=i_s).value = 'peiljaar toegevoegd'
        if antw is not None:
            blad.cell(row=rij, column=i_a).value = antw
            blad.cell(row=rij, column=i_l).value = f'was {was_a}: {was_v}'[:250]
        else:
            blad.cell(row=rij, column=i_l).value = f'was: {was_v}'[:250]
    boek.save(REVIEW)
    print('\nvragenbank bijgewerkt')


if __name__ == '__main__':
    main()
