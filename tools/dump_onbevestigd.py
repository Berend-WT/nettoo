# -*- coding: utf-8 -*-
"""Netto — zet de vragen met een onbevestigde bron in een leesbare lijst.

Draaien:  python tools/dump_onbevestigd.py [uitvoerpad]

Dit zijn de vragen die wel een bron hebben, maar waarbij het ophalen van die
bron het antwoord niet bevestigde: geblokkeerd door botdetectie, onbereikbaar,
of een pagina die het getal nergens noemt. Ze worden op categorie gegroepeerd
zodat ze per onderwerp met de hand te beoordelen zijn.
"""

import os
import sys

import pandas as pd

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')


def main():
    doel = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WORTEL, 'onbevestigd.txt')
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    ver = d['Bron (geverifieerd)'].notna()
    s = d.loc[~ver & d['Bron (bestaand)'].notna()].sort_values(['Categorie', 'Nr'])

    regels, cat = [], None
    for _, r in s.iterrows():
        if r['Categorie'] != cat:
            cat = r['Categorie']
            regels += ['', f'===== {cat} =====']
        regels.append(f"{int(r['Nr'])} [{r['In gebruik']}] {r['Vraag NL']} -> {r['Antwoord']}")
        regels.append(f"     {str(r['Bron (bestaand)'])[:100]}  | {r['Status oude bron']}")

    with open(doel, 'w', encoding='utf-8') as f:
        f.write('\n'.join(regels))
    print(f'{len(s)} vragen -> {doel}')


if __name__ == '__main__':
    main()
