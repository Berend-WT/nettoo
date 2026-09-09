# -*- coding: utf-8 -*-
"""Netto — zet de keuzes uit het kleine werkblad terug in het grote.

Draaien:  python tools/verwerk_fotokeuze_urgent.py

vragen/fotokeuze_urgent.xlsx bevat alleen de rijen die dringend een keuze nodig
hadden. maak_fotobestand.py leest alleen het grote blad, dus de ingevulde
kolom Keuze moet daar terechtkomen. Dit script doet dat op Nr, en raakt niets
anders aan.

Een lege Keuze wordt overgeslagen: leeg betekent "nog niet bekeken", en dat is
iets anders dan de 0 waarmee je alle drie de kandidaten afkeurt.
"""

import os
import shutil
import sys
from datetime import date

import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GROOT = os.path.join(WORTEL, 'vragen', 'fotokeuze.xlsx')
KLEIN = os.path.join(WORTEL, 'vragen', 'fotokeuze_urgent.xlsx')


def main():
    if not os.path.exists(KLEIN):
        print(f'{os.path.relpath(KLEIN, WORTEL)} bestaat niet')
        return

    klein = openpyxl.load_workbook(KLEIN, read_only=True)['Fotokeuze']
    rijen = klein.iter_rows(values_only=True)
    kop = list(next(rijen))
    i_nr, i_keuze = kop.index('Nr'), kop.index('Keuze')
    i_opm = kop.index('Opmerking') if 'Opmerking' in kop else None
    keuzes = {}
    opmerkingen = {}
    for rij in rijen:
        if rij[i_nr] is None:
            continue
        try:
            keuzes[int(rij[i_nr])] = int(rij[i_keuze])
        except (TypeError, ValueError):
            pass
        if i_opm is not None and rij[i_opm]:
            opmerkingen[int(rij[i_nr])] = rij[i_opm]
    print(f'{len(keuzes)} keuzes ingevuld')
    if not keuzes and not opmerkingen:
        return

    shutil.copy2(GROOT, os.path.join(
        os.path.dirname(GROOT),
        f'_backup_keuze_{date.today():%Y-%m-%d}_{os.path.basename(GROOT)}'))

    boek = openpyxl.load_workbook(GROOT)
    blad = boek['Fotokeuze']
    kop = [c.value for c in blad[1]]
    k = {naam: n for n, naam in enumerate(kop, start=1)}
    gezet = 0
    for r in range(2, blad.max_row + 1):
        nr = blad.cell(r, k['Nr']).value
        if nr is None:
            continue
        nr = int(nr)
        if nr in keuzes:
            blad.cell(r, k['Keuze']).value = keuzes[nr]
            gezet += 1
        if nr in opmerkingen and 'Opmerking' in k:
            blad.cell(r, k['Opmerking']).value = opmerkingen[nr]
    boek.save(GROOT)
    print(f'{gezet} rijen bijgewerkt in {os.path.relpath(GROOT, WORTEL)}')
    print('Draai nu: python tools/maak_fotobestand.py')


if __name__ == '__main__':
    main()
