# -*- coding: utf-8 -*-
"""Netto — controleer of antwoorden fysiek mogelijk zijn bij hun eenheid.

Draaien:  python tools/controleer_eenheden.py

WAAROM DIT NAAST DE BRONCONTROLE STAAT
Vraag 156 luidde "Hoeveel kilometer diep kan de potvis duiken?" met antwoord
2000. Een potvis duikt 2000 meter. Die fout was met geen enkele bronzoektocht te
vinden, want er is geen bron die zegt dat het antwoord fout is — je moet vraag,
eenheid en antwoord naast elkaar leggen en zien dat 2000 kilometer dieper is dan
de aarde dik is.

Deze controle kent geen enkel feit. Hij kent alleen grenzen: geen percentage
boven de honderd, geen berg hoger dan de Mount Everest, geen dier zwaarder dan
een blauwe vinvis. Wat daarbuiten valt, is fout — ongeacht welke bron erbij
staat. Daardoor zijn er vrijwel geen valse meldingen.
"""

import os
import re

import pandas as pd

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
DOEL = os.path.join(WORTEL, 'vragen', 'eenheidscontrole.csv')

# (patroon in de vraag, ondergrens, bovengrens, waarom die grens)
GRENZEN = [
    (r'hoeveel procent|welk percentage', 0, 100,
     'een percentage kan niet boven de honderd uitkomen'),
    (r'hoeveel landen', 0, 195,
     'de wereld telt 195 erkende landen'),
    (r'hoeveel kilometer diep', 0, 11,
     'het diepste punt op aarde is de Marianentrog, ongeveer 11 km'),
    (r'hoeveel meter diep', 0, 11100,
     'dieper dan de Marianentrog bestaat niet'),
    # Alleen ruimtevaart komt boven de negen kilometer uit; bij al het andere
    # dat "hoeveel kilometer hoog" heet, klopt de eenheid niet.
    (r'hoeveel kilometer hoog(?!.*(?:ruimte|satelliet|baan|iss|karman|atmosfeer))', 0, 9,
     'de Mount Everest is bijna 9 km; hoger komt op aarde niet voor'),
    (r'hoeveel meter hoog', 0, 8900,
     'hoger dan de Mount Everest bestaat niet'),
    (r'hoeveel graden celsius kookt', 50, 150,
     'water kookt rond de honderd graden'),
    (r'in welk jaar', 1, 2100,
     'een jaartal moet in het verleden of de nabije toekomst liggen'),
    (r'hoeveel spelers (?:staan|telt|heeft)', 0, 30,
     'een team heeft geen dertig spelers tegelijk op het veld'),
    (r'hoeveel uur per dag', 0, 24,
     'een dag heeft vierentwintig uur'),
    (r'hoeveel dagen (?:telt|heeft) (?:een|het) jaar', 360, 370,
     'een jaar telt 365 of 366 dagen'),
    (r'hoeveel minuten duurt', 0, 600,
     'langer dan tien uur duurt geen wedstrijd of film'),
    (r'hoeveel maanden', 0, 12,
     'een jaar telt twaalf maanden'),
    (r'hoeveel letters heeft het', 0, 200,
     'geen alfabet heeft meer dan tweehonderd letters'),
]


def main():
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    rijen = []
    for _, r in d.iterrows():
        vraag = str(r['Vraag NL'])
        try:
            antwoord = float(r['Antwoord'])
        except (TypeError, ValueError):
            continue
        for patroon, onder, boven, waarom in GRENZEN:
            if not re.search(patroon, vraag, re.I):
                continue
            if onder <= antwoord <= boven:
                break
            rijen.append({
                'Nr': int(r['Nr']),
                'In gebruik': r['In gebruik'],
                'Categorie': r['Categorie'],
                'Vraag NL': vraag,
                'Antwoord': r['Antwoord'],
                'Verwachte marge': f'{onder} tot {boven}',
                'Waarom dit niet kan': waarom,
                'Bron (geverifieerd)': r.get('Bron (geverifieerd)'),
                'Jouw besluit': None,
            })
            break

    uit = pd.DataFrame(rijen)
    if uit.empty:
        print('geen enkel antwoord viel buiten zijn grenzen')
        return
    uit = uit.sort_values(['In gebruik', 'Nr'])
    uit.to_csv(DOEL, index=False, encoding='utf-8-sig')
    print(f'{len(uit)} antwoorden vallen buiten wat fysiek kan:\n')
    for _, r in uit.iterrows():
        print(f"{int(r['Nr']):5d} [{r['In gebruik']:6s}] {str(r['Vraag NL'])[:56]:58s} = {r['Antwoord']}")
        print(f"        {r['Waarom dit niet kan']} (verwacht {r['Verwachte marge']})")
    print(f'\n-> {DOEL}')


if __name__ == '__main__':
    main()
