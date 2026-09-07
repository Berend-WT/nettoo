# -*- coding: utf-8 -*-
"""Netto — zet de opgeschoonde reservevragen door naar bank en reviewblad.

Draaien:  python tools/pas_afrondvragen_toe.py

Wat er wél gebeurt: de vraagteksten worden herschreven en de antwoorden
aangescherpt waar dat te verantwoorden is.

Wat er níét gebeurt: schrappen. De 52 vragen die ik onbruikbaar vind krijgen een
voorstel in de kolom "Verwijderen (voorstel)", maar blijven staan. Vragen
weggooien is een besluit van de eigenaar, niet van mij — en het is het enige
onderdeel hier dat je niet met één git-commando terugdraait.
"""

import os
import shutil
from datetime import date

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from afrondvragen_correcties import CORRECTIES

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK = os.path.join(WORTEL, 'vragen', '1000+ vragen netjes gecategoriseerd.xlsx')
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
WERKKOPIE = os.path.join(os.path.expanduser('~'), 'OneDrive - Driestar-Wartburg',
                         'Kopie van vragen_review_compleet.xlsx')
DOEL = os.path.join(WORTEL, 'vragen', 'reserve_opgeschoond.xlsx')

FONT = 'Arial'
KLEUR = {'exact': 'D6EAD6', 'opschonen': 'DDE7F5', 'fout': 'FBE9A5', 'schrappen': 'F8CBCB'}


def main():
    bron = WERKKOPIE if os.path.exists(WERKKOPIE) else REVIEW
    d = pd.read_excel(bron, sheet_name='Vragen').sort_values('Nr').reset_index(drop=True)

    rijen = []
    for i, r in d.iterrows():
        nr = int(r['Nr'])
        if nr not in CORRECTIES:
            continue
        status, nieuwe_vraag, nieuw_antwoord, toelichting = CORRECTIES[nr]
        rijen.append({
            'Nr': nr,
            'Status': status,
            'Categorie': r['Categorie'],
            'Vraag (oud)': r['Vraag NL'],
            'Vraag (nieuw)': nieuwe_vraag or '',
            'Antwoord (oud)': r['Antwoord'],
            'Antwoord (nieuw)': nieuw_antwoord if nieuw_antwoord is not None else '',
            'Toelichting': toelichting or '',
            'Verwijderen (voorstel)': 'ja' if status == 'schrappen' else '',
            'Jouw besluit': None,
        })
        # De bank zelf bijwerken, behalve bij schrappen: dat blijft een besluit
        # van de eigenaar.
        if status != 'schrappen':
            if nieuwe_vraag:
                d.at[i, 'Vraag NL'] = nieuwe_vraag
            if nieuw_antwoord is not None:
                d.at[i, 'Antwoord'] = nieuw_antwoord

    uit = pd.DataFrame(rijen)
    volgorde = ['fout', 'exact', 'opschonen', 'schrappen']
    uit['_s'] = uit['Status'].apply(volgorde.index)
    uit = uit.sort_values(['_s', 'Nr']).drop(columns=['_s'])

    for pad in (BANK, REVIEW):
        if os.path.exists(pad):
            shutil.copy2(pad, os.path.join(
                os.path.dirname(pad), f'_backup_{date.today():%Y-%m-%d}_{os.path.basename(pad)}'))

    # Reviewblad bijwerken met de nieuwe teksten en antwoorden.
    boek = load_workbook(bron)
    kolommen = [c.value for c in boek['Vragen'][1]]
    i_vraag = kolommen.index('Vraag NL') + 1
    i_antw = kolommen.index('Antwoord') + 1
    for rij in range(2, boek['Vragen'].max_row + 1):
        nr = boek['Vragen'].cell(row=rij, column=1).value
        if nr in CORRECTIES:
            status, nv, na, _ = CORRECTIES[nr]
            if status != 'schrappen':
                if nv:
                    boek['Vragen'].cell(row=rij, column=i_vraag).value = nv
                if na is not None:
                    boek['Vragen'].cell(row=rij, column=i_antw).value = na
    boek.save(REVIEW)

    # De bank heeft geen Nr-kolom; koppelen gaat op de oude vraagtekst.
    origineel = pd.read_excel(os.path.join(
        os.path.dirname(BANK), f'_backup_{date.today():%Y-%m-%d}_{os.path.basename(BANK)}'))
    oud = pd.read_excel(bron, sheet_name='Vragen').set_index('Nr')
    per_tekst = {}
    for nr, (status, nv, na, _) in CORRECTIES.items():
        if status == 'schrappen' or nr not in oud.index:
            continue
        per_tekst[str(oud.at[nr, 'Vraag NL']).strip()] = (nv, na)

    geraakt = 0
    vragen, antwoorden = [], []
    for _, r in origineel.iterrows():
        sleutel = str(r['Vraag NL']).strip()
        if sleutel in per_tekst:
            nv, na = per_tekst[sleutel]
            vragen.append(nv or r['Vraag NL'])
            antwoorden.append(na if na is not None else r['Antwoord'])
            geraakt += 1
        else:
            vragen.append(r['Vraag NL'])
            antwoorden.append(r['Antwoord'])
    bank = origineel.copy()
    bank['Vraag NL'] = vragen
    bank['Antwoord'] = antwoorden
    bank.to_excel(BANK, index=False)

    with pd.ExcelWriter(DOEL, engine='openpyxl') as w:
        uit.to_excel(w, index=False, sheet_name='Reserve opgeschoond')
    opmaak(DOEL, uit)

    print(f'bron: {os.path.basename(bron)}')
    for s in volgorde:
        print(f'  {s:11s} {int((uit["Status"] == s).sum()):4d}')
    print(f'\nbank bijgewerkt: {geraakt} vragen')
    print(f'-> {DOEL}')


def opmaak(pad, df):
    wb = load_workbook(pad)
    ws = wb['Reserve opgeschoond']
    breedtes = {'Nr': 6, 'Status': 12, 'Categorie': 24, 'Vraag (oud)': 66,
                'Vraag (nieuw)': 62, 'Antwoord (oud)': 14, 'Antwoord (nieuw)': 15,
                'Toelichting': 60, 'Verwijderen (voorstel)': 18, 'Jouw besluit': 18}
    for i, k in enumerate(df.columns, start=1):
        ws.column_dimensions[get_column_letter(i)].width = breedtes.get(k, 18)
        c = ws.cell(row=1, column=i)
        c.font = Font(name=FONT, bold=True, color='FFFFFF', size=11)
        c.fill = PatternFill('solid', fgColor='1F3864')
        c.alignment = Alignment(vertical='center', wrap_text=True)
    ws.row_dimensions[1].height = 28
    i_status = list(df.columns).index('Status') + 1
    for rij in range(2, ws.max_row + 1):
        for kol in range(1, len(df.columns) + 1):
            c = ws.cell(row=rij, column=kol)
            c.font = Font(name=FONT, size=10)
            c.alignment = Alignment(vertical='top', wrap_text=kol in (4, 5, 8))
        s = ws.cell(row=rij, column=i_status).value
        ws.cell(row=rij, column=i_status).fill = PatternFill('solid', fgColor=KLEUR.get(s, 'FFFFFF'))
    ws.freeze_panes = 'C2'
    ws.auto_filter.ref = f'A1:{get_column_letter(len(df.columns))}{ws.max_row}'
    wb.save(pad)


if __name__ == '__main__':
    main()
