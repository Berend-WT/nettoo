# -*- coding: utf-8 -*-
"""Netto — maak de invullijst voor foto's bij de vragen.

Draaien:  python tools/maak_fotolijst.py

Alle vragen met hun geverifieerde bron en een lege kolom om een fotolink in te
zetten. Vragen die in een daily of puzzel zitten staan bovenaan, want daar is
een foto het eerst zichtbaar.

De eenentwintig links die er al stonden zijn meegenomen in een aparte kolom,
maar ze deugen niet als bron voor een afbeelding: het zijn losse CDN-adressen
van willekeurige websites, en bij zulke adressen is de licentie niet na te gaan.
Bij Wikimedia Commons kan dat wel, omdat elke bestandspagina de licentie
vermeldt. Vandaar dat de invulkolom om een Commons-bestandspagina vraagt.

Het bestand gaat naar de OneDrive-map, niet naar de repo — het is werk in
uitvoering.
"""

import os
import shutil

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
DOEL = os.path.join(WORTEL, 'vragen', 'vragen_bronnen_fotos.xlsx')
ONEDRIVE = os.path.join(os.path.expanduser('~'), 'OneDrive - Driestar-Wartburg')

VOLGORDE = {'daily': 0, 'puzzel': 1}


def main():
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    uit = pd.DataFrame({
        'Nr': d['Nr'],
        'In gebruik': d['In gebruik'],
        'Categorie': d['Categorie'],
        'Vraag NL': d['Vraag NL'],
        'Antwoord': d['Antwoord'],
        'Bron': d['Bron (geverifieerd)'],
        'Vertrouwen': d['Vertrouwen bron'],
        'Waarom die bron': d['Bewijszin'],
        'Fotolink (Commons)': None,
        'Oude fotolink': d['Commons-fotolink'],
    })
    uit['_r'] = uit['In gebruik'].map(VOLGORDE).fillna(2)
    uit = uit.sort_values(['_r', 'Categorie', 'Nr']).drop(columns=['_r'])
    uit.to_excel(DOEL, index=False, sheet_name='Fotos')

    wb = load_workbook(DOEL)
    ws = wb['Fotos']
    br = {'Nr': 6, 'In gebruik': 11, 'Categorie': 22, 'Vraag NL': 58, 'Antwoord': 12,
          'Bron': 48, 'Vertrouwen': 13, 'Waarom die bron': 64,
          'Fotolink (Commons)': 46, 'Oude fotolink': 30}
    for i, k in enumerate(uit.columns, start=1):
        ws.column_dimensions[get_column_letter(i)].width = br.get(k, 18)
        c = ws.cell(row=1, column=i)
        c.font = Font(name='Arial', bold=True, color='FFFFFF', size=11)
        # De invulkolom krijgt een eigen kleur zodat meteen zichtbaar is
        # waar getypt moet worden.
        c.fill = PatternFill('solid',
                             fgColor='2E7D32' if k == 'Fotolink (Commons)' else '1F3864')
        c.alignment = Alignment(vertical='center', wrap_text=True)
    ws.row_dimensions[1].height = 30

    i_f = list(uit.columns).index('Fotolink (Commons)') + 1
    i_g = list(uit.columns).index('In gebruik') + 1
    for rij in range(2, ws.max_row + 1):
        for kol in range(1, len(uit.columns) + 1):
            c = ws.cell(row=rij, column=kol)
            c.font = Font(name='Arial', size=10)
            c.alignment = Alignment(vertical='top',
                                    wrap_text=uit.columns[kol - 1] in
                                    ('Vraag NL', 'Waarom die bron'))
        ws.cell(row=rij, column=i_f).fill = PatternFill('solid', fgColor='FFF9E0')
        g = ws.cell(row=rij, column=i_g).value
        if g in VOLGORDE:
            ws.cell(row=rij, column=i_g).fill = PatternFill(
                'solid', fgColor='D6EAD6' if g == 'daily' else 'E8F0DC')
    ws.freeze_panes = 'D2'
    ws.auto_filter.ref = f'A1:{get_column_letter(len(uit.columns))}{ws.max_row}'
    wb.save(DOEL)

    if os.path.isdir(ONEDRIVE):
        shutil.copy2(DOEL, os.path.join(ONEDRIVE, os.path.basename(DOEL)))
        print(f'-> {os.path.join(ONEDRIVE, os.path.basename(DOEL))}')
    print(f'-> {DOEL}')
    print(f'{len(uit)} vragen, waarvan {int((uit["In gebruik"] != "—").sum())} in gebruik')


if __name__ == '__main__':
    main()
