# -*- coding: utf-8 -*-
"""Netto — zet de met de hand goedgekeurde bewijszinnen in de vragenbank.

Draaien:  python tools/zet_bewijszinnen.py

GOEDGEKEURD staat hieronder: per vraagnummer welke kandidaatzin uit
vragen/bewijszinnen_kandidaten.json de juiste is. Die keuze is met de hand
gemaakt en dat is geen omslachtigheid maar de kern van de zaak: de fouten die we
opruimen zijn juist ontstaan doordat een script zelf koos zodra het getal ergens
op de pagina stond. "15 tramlijnen" kwam uit "de 15e eeuw", "16 deelstaten" uit
"16 nationale parken".

Wat hier niet in staat, blijft staan zoals het is. Een ontbrekende bewijszin is
vervelend; een verkeerde is een fout antwoord in wording.
"""

import json
import os
import shutil
import sys
from datetime import date

import openpyxl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
KANDIDATEN = os.path.join(WORTEL, 'vragen', 'bewijszinnen_kandidaten.json')

# vraagnummer -> welke kandidaat (0 = de eerste)
GOEDGEKEURD = {
    4: 0, 9: 0, 12: 0, 24: 0, 38: 1, 73: 0, 106: 0, 117: 0, 121: 0, 127: 0,
    176: 1, 374: 0, 379: 0, 428: 0, 474: 0, 476: 0, 490: 0, 509: 0, 510: 0,
    511: 1, 535: 0, 574: 0, 608: 1, 609: 0, 641: 0, 670: 0, 867: 0, 1267: 0,
    1338: 0, 1378: 1, 1382: 0, 1445: 0, 1477: 0,
}

# Zinnen die te kaal zijn om alleen te staan krijgen er context bij. De zin
# zelf blijft woordelijk; alleen waar hij vandaan komt wordt erbij gezet.
AANVULLING = {
    12: 'Coca-Cola over het eigen product: "35 g in a 330 ml can."',
    73: 'Gold is element 79 and its symbol is Au. Het elementnummer is het '
        'aantal protonen in de kern.',
    474: 'Take for example the case of element 74 - or as we call it in English '
         '- tungsten. Het elementnummer is het aantal protonen in de kern.',
    1378: 'Length (goal line): minimum 45 m (50 yds) maximum 90 m (100 yds). '
          'De doellijn is de breedte van het veld.',
}


def main():
    kandidaten = {r['nr']: r for r in json.load(open(KANDIDATEN, encoding='utf-8'))}
    shutil.copy2(REVIEW, os.path.join(
        os.path.dirname(REVIEW),
        f'_backup_bewijs_{date.today():%Y-%m-%d}_{os.path.basename(REVIEW)}'))

    boek = openpyxl.load_workbook(REVIEW)
    blad = boek['Vragen']
    kop = [c.value for c in blad[1]]
    k = {naam: n for n, naam in enumerate(kop, start=1)}

    gezet, gemist = 0, []
    for rij in range(2, blad.max_row + 1):
        nr = blad.cell(rij, k['Nr']).value
        if nr is None or int(nr) not in GOEDGEKEURD:
            continue
        nr = int(nr)
        keuze = GOEDGEKEURD[nr]
        zinnen = kandidaten.get(nr, {}).get('zinnen') or []
        if keuze >= len(zinnen):
            gemist.append(nr)
            continue
        zin = AANVULLING.get(nr) or ' '.join(zinnen[keuze]['zin'].split())
        blad.cell(rij, k['Bewijszin']).value = zin
        gezet += 1

    boek.save(REVIEW)
    print(f'{gezet} bewijszinnen gezet')
    if gemist:
        print(f'kandidaat niet gevonden voor: {gemist}')


if __name__ == '__main__':
    main()
