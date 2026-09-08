# -*- coding: utf-8 -*-
"""Netto — zet de herstelde matig-bronnen door naar het reviewblad.

Draaien:  python tools/verwerk_matig_hersteld.py

Overschrijft de bron, bewijszin en vertrouwensmarkering van de 42 vragen die
vertrouwen "matig" hadden. De oude bron gaat naar "Status oude bron", zodat
zichtbaar blijft wat er stond.
"""

import os
import shutil
from datetime import date

import pandas as pd
from openpyxl import load_workbook

from bronnen_matig_hersteld import M

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')

VERTROUWEN = {'bevestigd': 'handmatig', 'natellen': 'natellen',
              'veroudert': 'veroudert', 'fout': 'antwoord fout'}


def main():
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    verwacht = set(d.loc[d['Vertrouwen bron'] == 'matig', 'Nr'])
    if verwacht - set(M):
        print(f'LET OP — niet beoordeeld: {sorted(verwacht - set(M))}')
    if set(M) - verwacht:
        print(f'LET OP — buiten de selectie: {sorted(set(M) - verwacht)}')

    shutil.copy2(REVIEW, os.path.join(
        os.path.dirname(REVIEW),
        f'_backup_matig_{date.today():%Y-%m-%d}_vragen_review_compleet.xlsx'))
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
        if nr not in M:
            continue
        oordeel, bron, toelichting = M[nr]
        oud = blad.cell(row=rij, column=i_bron).value
        blad.cell(row=rij, column=i_st).value = f'matig vervangen (was: {oud})'[:250]
        blad.cell(row=rij, column=i_bew).value = toelichting[:400]
        if not bron:
            blad.cell(row=rij, column=i_bron).value = None
            blad.cell(row=rij, column=i_vert).value = None
            blad.cell(row=rij, column=i_st).value = f'vraag deugt niet ({oordeel})'
            continue
        blad.cell(row=rij, column=i_bron).value = bron
        blad.cell(row=rij, column=i_vert).value = VERTROUWEN.get(oordeel, oordeel)
        n += 1
    boek.save(REVIEW)

    print(pd.Series([v[0] for v in M.values()]).value_counts().to_string())
    print(f'\nbronnen vervangen: {n}')
    na = pd.read_excel(REVIEW, sheet_name='Vragen')
    print()
    print(na['Vertrouwen bron'].fillna('(geen bron)').value_counts().to_string())


if __name__ == '__main__':
    main()
