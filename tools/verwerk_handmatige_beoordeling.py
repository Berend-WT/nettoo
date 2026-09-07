# -*- coding: utf-8 -*-
"""Netto — zet de handmatige beoordeling om in een werkmap en het reviewblad.

Draaien:  python tools/verwerk_handmatige_beoordeling.py

De bronnen die bij een goedgekeurd antwoord horen gaan het reviewblad in. De
antwoorden zelf worden NIET aangepast: elke vraag hier zit in een puzzel, en een
ander antwoord breekt de som van die puzzel. Dat hoort bij de puzzelrevisie.
"""

import os
import shutil
from datetime import date

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from handmatige_beoordeling import BEOORDELING

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
DOEL = os.path.join(WORTEL, 'vragen', 'handmatig_beoordeeld.xlsx')

KLEUR = {'fout': 'F8CBCB', 'verouderd': 'FBE9A5', 'definitie': 'FBD9A5',
         'onverifieerbaar': 'E8E8E8', 'rekensom': 'DDE7F5', 'klopt': 'D6EAD6'}
RANG = ['fout', 'verouderd', 'definitie', 'onverifieerbaar', 'rekensom', 'klopt']


def main():
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    rijen = []
    for _, r in d.iterrows():
        nr = int(r['Nr'])
        if nr not in BEOORDELING:
            continue
        oordeel, bron, toelichting = BEOORDELING[nr]
        rijen.append({
            'Nr': nr, 'Oordeel': oordeel, 'In gebruik': r['In gebruik'],
            'Categorie': r['Categorie'], 'Vraag NL': r['Vraag NL'],
            'Antwoord': r['Antwoord'], 'Toelichting': toelichting,
            'Bron': bron, 'Jouw besluit': None,
        })

    uit = pd.DataFrame(rijen)
    uit['_r'] = uit['Oordeel'].apply(RANG.index)
    uit = uit.sort_values(['_r', 'In gebruik', 'Nr']).drop(columns=['_r'])
    uit.to_excel(DOEL, index=False, sheet_name='Handmatig beoordeeld')

    wb = load_workbook(DOEL)
    ws = wb['Handmatig beoordeeld']
    breedtes = {'Nr': 6, 'Oordeel': 16, 'In gebruik': 11, 'Categorie': 22,
                'Vraag NL': 58, 'Antwoord': 11, 'Toelichting': 74, 'Bron': 46,
                'Jouw besluit': 18}
    for i, k in enumerate(uit.columns, start=1):
        ws.column_dimensions[get_column_letter(i)].width = breedtes.get(k, 18)
        c = ws.cell(row=1, column=i)
        c.font = Font(name='Arial', bold=True, color='FFFFFF', size=11)
        c.fill = PatternFill('solid', fgColor='1F3864')
        c.alignment = Alignment(vertical='center', wrap_text=True)
    ws.row_dimensions[1].height = 28
    i_oordeel = list(uit.columns).index('Oordeel') + 1
    for rij in range(2, ws.max_row + 1):
        for kol in range(1, len(uit.columns) + 1):
            c = ws.cell(row=rij, column=kol)
            c.font = Font(name='Arial', size=10)
            c.alignment = Alignment(vertical='top',
                                    wrap_text=uit.columns[kol - 1] in ('Vraag NL', 'Toelichting'))
        o = ws.cell(row=rij, column=i_oordeel).value
        ws.cell(row=rij, column=i_oordeel).fill = PatternFill('solid', fgColor=KLEUR.get(o, 'FFFFFF'))
    ws.freeze_panes = 'C2'
    ws.auto_filter.ref = f'A1:{get_column_letter(len(uit.columns))}{ws.max_row}'
    wb.save(DOEL)

    # Bronnen wegschrijven waar het antwoord standhoudt.
    shutil.copy2(REVIEW, os.path.join(
        os.path.dirname(REVIEW),
        f'_backup_handmatig_{date.today():%Y-%m-%d}_vragen_review_compleet.xlsx'))
    boek = load_workbook(REVIEW)
    blad = boek['Vragen']
    kol = [c.value for c in blad[1]]
    i_bron = kol.index('Bron (geverifieerd)') + 1
    i_bew = kol.index('Bewijszin') + 1
    i_vert = kol.index('Vertrouwen bron') + 1
    n = 0
    for rij in range(2, blad.max_row + 1):
        nr = blad.cell(row=rij, column=1).value
        if nr not in BEOORDELING:
            continue
        oordeel, bron, toelichting = BEOORDELING[nr]
        if bron and oordeel in ('klopt', 'definitie', 'verouderd'):
            blad.cell(row=rij, column=i_bron).value = bron
            blad.cell(row=rij, column=i_bew).value = toelichting[:400]
            blad.cell(row=rij, column=i_vert).value = 'handmatig'
            n += 1
    boek.save(REVIEW)

    print(uit['Oordeel'].value_counts().to_string())
    print(f'\nbronnen weggeschreven naar het reviewblad: {n}')
    print(f'-> {DOEL}')


if __name__ == '__main__':
    main()
