# -*- coding: utf-8 -*-
"""Netto — breng de vragenbank gelijk met het reviewblad.

Draaien:  python tools/synchroniseer_bank.py [--schrijf]

De puzzelgeneratoren in puzzels/ lezen uit de bank, niet uit het reviewblad.
Alle correcties van vandaag — gewijzigde antwoorden, herschreven vraagteksten,
peiljaren, geverifieerde bronnen — staan alleen in het reviewblad. Zolang die
twee uiteenlopen zou een nieuwe puzzelronde de oude, foute getallen gebruiken.

Het reviewblad is de leidende versie: het bevat alles wat de bank had, plus het
werk van vandaag. De bank wordt daarom opnieuw opgebouwd uit het reviewblad, in
zijn eigen kolomindeling zodat de generatoren er niets van merken.

De kolom Status komt uit de bank en zegt uit welke ronde een vraag stamt. Die
wordt op vraagtekst teruggezocht; bij de zesentwintig herschreven vragen lukt
dat niet meer en blijft hij leeg. Dat is geen verlies: Status stuurt niets aan,
het is herkomstinformatie.
"""

import os
import shutil
import sys
from datetime import date

import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK = os.path.join(WORTEL, 'vragen', '1000+ vragen netjes gecategoriseerd.xlsx')
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')


def main():
    schrijf = '--schrijf' in sys.argv
    oud = pd.read_excel(BANK)
    r = pd.read_excel(REVIEW, sheet_name='Vragen')

    status = dict(zip(oud['Vraag NL'].astype(str), oud['Status']))
    nieuw = pd.DataFrame({
        'Categorie': r['Categorie'],
        'Vraag NL': r['Vraag NL'],
        'Antwoord': r['Antwoord'],
        'Bron EN': r['Bron (geverifieerd)'],
        'Status': [status.get(str(v)) for v in r['Vraag NL']],
    })

    print(f'bank was {len(oud)} rijen, wordt {len(nieuw)}')
    print(f'Bron EN gevuld: {int(oud["Bron EN"].notna().sum())} -> '
          f'{int(nieuw["Bron EN"].notna().sum())}')
    print(f'Status teruggevonden: {int(nieuw["Status"].notna().sum())} van '
          f'{int(oud["Status"].notna().sum())}')

    verschil = set(oud['Vraag NL'].astype(str)) ^ set(nieuw['Vraag NL'].astype(str))
    print(f'verschillende vraagteksten: {len(verschil)}')

    if not schrijf:
        print('\n(proefdraai — voeg --schrijf toe om op te slaan)')
        return

    shutil.copy2(BANK, os.path.join(
        os.path.dirname(BANK),
        f'_backup_sync_{date.today():%Y-%m-%d}_{os.path.basename(BANK)}'))
    nieuw.to_excel(BANK, index=False)
    print(f'\n-> {BANK}')


if __name__ == '__main__':
    main()
