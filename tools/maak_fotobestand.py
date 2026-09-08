# -*- coding: utf-8 -*-
"""Netto — koppel foto's aan vragen en schrijf ze weg voor de frontend.

Draaien:  python tools/maak_fotobestand.py

WELKE FOTO EEN VRAAG KRIJGT, IN DEZE VOLGORDE
  1. Jouw keuze in vragen/fotokeuze.xlsx, kolom "Keuze". Een 1, 2 of 3 wijst een
     van de getoonde kandidaten aan; een 0 betekent dat je ze alle drie hebt
     afgekeurd en dat de vraag geen foto krijgt.
  2. De hoofdafbeelding uit de infobox van het bronartikel. Dat is de foto die
     je van een onderwerp verwacht.
  3. De eerste kandidaat uit de oudere zoekronde.

Zolang het keuzeblad leeg is wint dus vanzelf de hoofdafbeelding, en zodra je
een rij invult overschrijft die keuze het automatische voorstel. Opnieuw draaien
na het invullen is genoeg; er gaat niets verloren.

WAT ERUIT KOMT
data/netto_fotos.js met per vraagtekst het adres van de afbeelding, de
Commons-bestandspagina, de licentie en de maker. Die laatste twee zijn nodig
voor de naamsvermelding: CC BY en CC BY-SA eisen dat, en zonder die gegevens is
achteraf niet meer na te gaan van wie een foto is.
"""

import json
import os
import sys

import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
KEUZE = os.path.join(WORTEL, 'vragen', 'fotokeuze.xlsx')
FOTOS = os.path.join(WORTEL, 'fotos')
DATA = os.path.join(WORTEL, 'data')
SPIEGEL = os.path.join(WORTEL, 'website', 'data')


def lees(pad):
    if not os.path.exists(pad):
        return {}
    with open(pad, encoding='utf-8') as f:
        return json.load(f)


def main():
    hoofd = lees(os.path.join(FOTOS, 'hoofdafbeeldingen.json'))
    oud = lees(os.path.join(FOTOS, 'kandidaten.json'))

    # Handmatige keuzes, als het blad al is ingevuld.
    keuzes = {}
    if os.path.exists(KEUZE):
        try:
            kb = pd.read_excel(KEUZE, sheet_name='Fotokeuze')
            for _, r in kb.iterrows():
                try:
                    k = int(r['Keuze'])
                except (TypeError, ValueError):
                    continue
                keuzes[int(r['Nr'])] = k
        except Exception as fout:
            print(f'keuzeblad niet gelezen ({fout}); alleen automatische keuze')

    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    uit = {}
    telling = {'keuze': 0, 'hoofdafbeelding': 0, 'oude kandidaat': 0,
               'afgekeurd': 0, 'geen': 0}

    for _, r in d.iterrows():
        nr = int(r['Nr'])
        vraag = str(r['Vraag NL'])
        # De kandidatenlijst zoals die in het keuzeblad stond: hoofdafbeelding
        # vooraan, daarna wat de oudere ronde vond.
        beste = (hoofd.get(str(nr), {}).get('kandidaten') or [None])[0]
        rest = [k for k in (oud.get(str(nr), {}).get('kandidaten') or [])
                if not beste or k.get('titel') != beste.get('titel')]
        lijst = ([beste] if beste else []) + rest[:2]

        keuze = keuzes.get(nr)
        if keuze == 0:
            telling['afgekeurd'] += 1
            continue
        if keuze and 1 <= keuze <= len(lijst):
            gekozen, herkomst = lijst[keuze - 1], 'keuze'
        elif beste:
            gekozen, herkomst = beste, 'hoofdafbeelding'
        elif lijst:
            gekozen, herkomst = lijst[0], 'oude kandidaat'
        else:
            telling['geen'] += 1
            continue

        telling[herkomst] += 1
        uit[vraag] = {'url': gekozen['miniatuur'], 'pagina': gekozen['pagina'],
                      'licentie': gekozen['licentie'], 'maker': gekozen['maker']}

    kop = ('// Netto — foto per vraag, gekoppeld op vraagtekst.\n'
           '// Gegenereerd door tools/maak_fotobestand.py\n'
           '// Alleen CC BY, CC BY-SA, CC0 en publiek domein; maker en licentie\n'
           '// staan erbij omdat de eerste twee naamsvermelding eisen.\n'
           'window.NETTO_FOTOS = ')
    tekst = kop + json.dumps(uit, ensure_ascii=False) + ';\n'
    for map_ in (DATA, SPIEGEL):
        with open(os.path.join(map_, 'netto_fotos.js'), 'w', encoding='utf-8') as f:
            f.write(tekst)

    for k, v in telling.items():
        print(f'  {k:16s} {v}')
    print(f'\n{len(uit)} vragen met een foto -> data/netto_fotos.js')


if __name__ == '__main__':
    main()
