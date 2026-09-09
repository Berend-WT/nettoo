# -*- coding: utf-8 -*-
"""Netto — verwerk het afkeurblad: goedgekeurde foto's naar het spel.

Draaien:  python tools/verwerk_fotoblad_afkeuren.py

Leest vragen/fotos_afkeuren.xlsx en zet per vraag een 1 (goedgekeurd) of een 0
(afgekeurd) in de kolom Keuze van vragen/fotokeuze.xlsx. Daarna pikt
maak_fotobestand.py het op zoals elke andere handmatige keuze.

DE GRENS IS HET GETAL OP HET TABBLAD VOORTGANG
Een lege cel in "Weg?" betekent twee verschillende dingen: goedgekeurd, of nog
niet bekeken. Zonder dat onderscheid zou een half nagelopen blad alle
resterende voorstellen alsnog goedkeuren, en dat is precies de fout die we
proberen te vermijden. Alleen rijen tot en met dat rijnummer tellen mee.
"""

import os
import shutil
import sys
from datetime import date

import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AFKEUR = os.path.join(WORTEL, 'vragen', 'fotos_afkeuren.xlsx')
KEUZE = os.path.join(WORTEL, 'vragen', 'fotokeuze.xlsx')


def main():
    if not os.path.exists(AFKEUR):
        print(f'{os.path.relpath(AFKEUR, WORTEL)} bestaat niet')
        return
    boek = openpyxl.load_workbook(AFKEUR, read_only=True)
    blad = boek['Fotos']
    kop = [c.value for c in blad[1]]
    k = {naam: n for n, naam in enumerate(kop, start=1)}

    grens = blad.max_row
    if 'Voortgang' in boek.sheetnames:
        waarde = boek['Voortgang']['B1'].value
        try:
            grens = int(waarde)
        except (TypeError, ValueError):
            print('geen geldig rijnummer op het tabblad Voortgang; niets verwerkt')
            return
    if grens < 2:
        print('het tabblad Voortgang staat nog op 1: er is niets nagekeken')
        return

    goed, afgekeurd = {}, {}
    for rij in range(2, min(grens, blad.max_row) + 1):
        nr = blad.cell(rij, k['Nr']).value
        if nr is None:
            continue
        # Alles wat je in de kolom zet telt als afkeuren, of dat nu een 0 is,
        # een kruisje of een scheldwoord. Dat scheelt onthouden welk teken
        # precies de bedoeling was.
        oordeel = str(blad.cell(rij, k['Weg?']).value or '').strip()
        (afgekeurd if oordeel else goed)[int(nr)] = rij
    print(f'tot en met rij {grens}: {len(goed)} goedgekeurd, {len(afgekeurd)} weggestreept')

    shutil.copy2(KEUZE, os.path.join(
        os.path.dirname(KEUZE),
        f'_backup_afkeur_{date.today():%Y-%m-%d}_{os.path.basename(KEUZE)}'))
    keuzeboek = openpyxl.load_workbook(KEUZE)
    keuzeblad = keuzeboek['Fotokeuze']
    kk = {naam: n for n, naam in enumerate([c.value for c in keuzeblad[1]], start=1)}

    gezet = 0
    for rij in range(2, keuzeblad.max_row + 1):
        nr = keuzeblad.cell(rij, kk['Nr']).value
        if nr is None:
            continue
        nr = int(nr)
        if nr in goed:
            keuzeblad.cell(rij, kk['Keuze']).value = 1
            gezet += 1
        elif nr in afgekeurd:
            keuzeblad.cell(rij, kk['Keuze']).value = 0
            gezet += 1
    keuzeboek.save(KEUZE)
    print(f'{gezet} rijen bijgewerkt in {os.path.relpath(KEUZE, WORTEL)}')
    print('Draai nu: python tools/maak_fotobestand.py')


if __name__ == '__main__':
    main()
