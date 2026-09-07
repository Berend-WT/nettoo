# -*- coding: utf-8 -*-
"""Netto — zet de handmatige reservebronnen door naar het reviewblad.

Draaien:  python tools/verwerk_reserve_bronnen.py

De vier blokken samen dekken alle 316 vragen die geen bruikbare bron hadden.
Wat er wordt weggeschreven hangt af van het oordeel:

  bevestigd    Bron plus toelichting; geldt als geverifieerd.
  natellen     Bron plus toelichting, met vertrouwen "natellen". Het artikel is
               juist maar noemt het getal niet als getal — bij "Hoeveel landen
               grenzen aan Argentinie?" staat de opsomming er wel en het woord
               vijf niet. Dat is een bruikbare bron, geen bevestiging.
  veroudert    Bron erbij, maar met de waarschuwing dat het antwoord verloopt.
  fout         Geen bron; het antwoord klopt niet en moet eerst gecorrigeerd.
  onbruikbaar  Geen bron; de vraag zelf deugt niet.

Antwoorden worden niet aangepast. Bij vragen in een puzzel breekt dat de som,
en bij reservevragen is het een keuze die de eigenaar moet maken.
"""

import os
import shutil
from datetime import date

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from bronnen_handmatig_reserve import B
from bronnen_handmatig_reserve2 import B2
from bronnen_handmatig_reserve3 import B3
from bronnen_handmatig_reserve4 import B4

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
DOEL = os.path.join(WORTEL, 'vragen', 'reserve_bronnen.xlsx')

ALLES = {}
for blok in (B, B2, B3, B4):
    ALLES.update(blok)

KLEUR = {'fout': 'F8CBCB', 'onbruikbaar': 'F2D5D5', 'veroudert': 'FBE9A5',
         'natellen': 'DDE7F5', 'bevestigd': 'D6EAD6'}
RANG = ['fout', 'onbruikbaar', 'veroudert', 'natellen', 'bevestigd']


def main():
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    rijen = []
    for _, r in d.iterrows():
        nr = int(r['Nr'])
        if nr not in ALLES:
            continue
        oordeel, bron, toelichting = ALLES[nr]
        rijen.append({'Nr': nr, 'Oordeel': oordeel, 'In gebruik': r['In gebruik'],
                      'Categorie': r['Categorie'], 'Vraag NL': r['Vraag NL'],
                      'Antwoord': r['Antwoord'], 'Bron': bron,
                      'Toelichting': toelichting, 'Jouw besluit': None})

    uit = pd.DataFrame(rijen)
    uit['_r'] = uit['Oordeel'].apply(RANG.index)
    uit = uit.sort_values(['_r', 'Nr']).drop(columns=['_r'])
    uit.to_excel(DOEL, index=False, sheet_name='Reserve bronnen')

    wb = load_workbook(DOEL)
    ws = wb['Reserve bronnen']
    br = {'Nr': 6, 'Oordeel': 14, 'In gebruik': 11, 'Categorie': 22, 'Vraag NL': 56,
          'Antwoord': 12, 'Bron': 50, 'Toelichting': 74, 'Jouw besluit': 18}
    for i, k in enumerate(uit.columns, start=1):
        ws.column_dimensions[get_column_letter(i)].width = br.get(k, 18)
        c = ws.cell(row=1, column=i)
        c.font = Font(name='Arial', bold=True, color='FFFFFF', size=11)
        c.fill = PatternFill('solid', fgColor='1F3864')
        c.alignment = Alignment(vertical='center', wrap_text=True)
    ws.row_dimensions[1].height = 28
    i_o = list(uit.columns).index('Oordeel') + 1
    for rij in range(2, ws.max_row + 1):
        for kol in range(1, len(uit.columns) + 1):
            c = ws.cell(row=rij, column=kol)
            c.font = Font(name='Arial', size=10)
            c.alignment = Alignment(vertical='top',
                                    wrap_text=uit.columns[kol - 1] in ('Vraag NL', 'Toelichting'))
        o = ws.cell(row=rij, column=i_o).value
        ws.cell(row=rij, column=i_o).fill = PatternFill('solid', fgColor=KLEUR.get(o, 'FFFFFF'))
    ws.freeze_panes = 'C2'
    ws.auto_filter.ref = f'A1:{get_column_letter(len(uit.columns))}{ws.max_row}'
    wb.save(DOEL)

    shutil.copy2(REVIEW, os.path.join(
        os.path.dirname(REVIEW),
        f'_backup_reserve_{date.today():%Y-%m-%d}_vragen_review_compleet.xlsx'))
    boek = load_workbook(REVIEW)
    blad = boek['Vragen']
    kol = [c.value for c in blad[1]]
    i_bron = kol.index('Bron (geverifieerd)') + 1
    i_bew = kol.index('Bewijszin') + 1
    i_vert = kol.index('Vertrouwen bron') + 1
    i_st = kol.index('Status oude bron') + 1

    n = 0
    for rij in range(2, blad.max_row + 1):
        nr = blad.cell(row=rij, column=1).value
        if nr not in ALLES:
            continue
        oordeel, bron, toelichting = ALLES[nr]
        if not bron:
            blad.cell(row=rij, column=i_st).value = f'geen bron mogelijk ({oordeel})'
            continue
        blad.cell(row=rij, column=i_bron).value = bron
        blad.cell(row=rij, column=i_bew).value = toelichting[:400]
        blad.cell(row=rij, column=i_vert).value = {
            'bevestigd': 'handmatig', 'natellen': 'natellen', 'veroudert': 'veroudert',
            'fout': 'antwoord fout'}.get(oordeel, oordeel)
        if oordeel == 'fout':
            blad.cell(row=rij, column=i_st).value = 'antwoord fout, zie toelichting'
        n += 1
    boek.save(REVIEW)

    print(uit['Oordeel'].value_counts().to_string())
    print(f'\nbronnen weggeschreven: {n}')

    na = pd.read_excel(REVIEW, sheet_name='Vragen')
    ver = na['Bron (geverifieerd)'].notna()
    print(f'kolom "Bron (geverifieerd)" gevuld: {int(ver.sum())} van {len(na)}')
    print(f'-> {DOEL}')


if __name__ == '__main__':
    main()
