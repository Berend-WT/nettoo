# -*- coding: utf-8 -*-
"""Netto — corrigeer antwoorden die door hun eigen bewijszin worden tegengesproken.

Draaien:  python tools/corrigeer_antwoorden.py

HOE DEZE FOUTEN ZIJN GEVONDEN
Niet met een controle op het getal, want dat is precies wat ze heeft laten
passeren. Ze kwamen boven door de bewijszinnen te lezen die geen citaat zijn
maar een notitie: "Het opgegeven 1247 was het record van 2023", "Het opgegeven
1500 komt uit geen enkele bron". Iemand had het al gezien en alleen het
antwoord niet aangepast.

Elk nieuw antwoord hieronder is opnieuw bij de bron opgehaald en de bewijszin is
de zin waarin het staat, woordelijk.

LET OP: DIT BREEKT PUZZELS
Een som als 24000 : 1500 = 16 klopt niet meer zodra 1500 in 451 verandert. Het
script noemt aan het eind welke puzzels het raakt. Die moeten opnieuw
gegenereerd worden; dat gebeurt bewust niet hier, want vragen en puzzels
repareren we nooit in dezelfde beweging.
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
DATA = os.path.join(WORTEL, 'data')

# nr: (nieuwe vraag of None, nieuw antwoord, bron, bewijszin)
CORRECTIES = {
    59: (None, 1225, 'https://nl.wikipedia.org/wiki/Geluidssnelheid',
         'Bij 15 °C op zeeniveau is de geluidssnelheid 340,3 m/s, oftewel 1225 km/u. '
         'De eerder opgegeven 1234 km/u hoort bij 20 °C.'),
    71: (None, 1279, 'https://en.wikipedia.org/wiki/Giant_pumpkin',
         'As of 2025, the largest weighed 2,819.3 lb (1,278.8 kg).'),
    360: ('Hoeveel miljoen ton groene koffiebonen produceerde de wereld in 2023?', 11,
          'https://en.wikipedia.org/wiki/Coffee',
          'In 2023, world production of green coffee beans was 11 million tonnes, '
          'led by Brazil with 31% of the total and Vietnam as a secondary producer.'),
    412: (None, 451, 'https://nl.wikipedia.org/wiki/Nederland',
          'De lengte van de landsgrens bedraagt 1027 km, terwijl de kustlijn 451 km lang is.'),
    605: (None, 7200, 'https://en.wikipedia.org/wiki/Cardiac_output',
          'For a healthy individual weighing 70 kg, the cardiac output at rest averages '
          'about 5 L/min. Vijf liter per minuut maal 1440 minuten is 7200 liter per dag.'),
    1068: ('Hoeveel schilderijen van Vincent van Gogh bezit het Van Gogh Museum?', 200,
           'https://en.wikipedia.org/wiki/Van_Gogh_Museum',
           'The museum houses the largest Van Gogh collection in the world, with 200 '
           'paintings, 400 drawings, and 700 letters by the artist.'),
    1307: (None, 5793, 'https://en.wikipedia.org/wiki/Chocolate_bar',
           "The world's largest chocolate bar was produced as a stunt by Thorntons plc "
           '(UK) on 7 October 2011. It weighed 5,792.5 kg.'),
}


def puzzels_per_vraag():
    """Waar elke vraagtekst voorkomt, zodat we kunnen zeggen wat er breekt."""
    waar = {}
    pad = os.path.join(DATA, 'netto_frontend_puzzles.js')
    tekst = open(pad, encoding='utf-8').read()
    for groep, lijst in json.loads(tekst[tekst.index('{'):tekst.rindex('}') + 1]).items():
        for p in lijst:
            for n in (1, 2, 3):
                waar.setdefault(p.get(f'q{n}_label'), []).append(f'{groep}:{p["id"]}')
    tekst = open(os.path.join(DATA, 'netto_race_pool.js'), encoding='utf-8').read()
    for p in json.loads(tekst[tekst.index('['):tekst.rindex(']') + 1]):
        for n in (1, 2, 3):
            waar.setdefault(p.get(f'q{n}_label'), []).append(f'race:{p["id"]}')
    tekst = open(os.path.join(DATA, 'netto_breinkrakers.js'), encoding='utf-8').read()
    for p in json.loads(tekst[tekst.index('['):tekst.rindex(']') + 1]):
        for n in (1, 2, 3, 4):
            waar.setdefault(p[f'q{n}']['label'], []).append(f'brein:{p["id"]}')
    return waar


def main():
    waar = puzzels_per_vraag()
    shutil.copy2(REVIEW, os.path.join(
        os.path.dirname(REVIEW),
        f'_backup_antwoord_{date.today():%Y-%m-%d}_{os.path.basename(REVIEW)}'))

    boek = openpyxl.load_workbook(REVIEW)
    blad = boek['Vragen']
    k = {naam: n for n, naam in enumerate([c.value for c in blad[1]], start=1)}

    geraakt = set()
    for rij in range(2, blad.max_row + 1):
        nr = blad.cell(rij, k['Nr']).value
        if nr is None or int(nr) not in CORRECTIES:
            continue
        nieuwe_vraag, antwoord, bron, bewijs = CORRECTIES[int(nr)]
        oude_vraag = blad.cell(rij, k['Vraag NL']).value
        oud_antwoord = blad.cell(rij, k['Antwoord']).value
        if nieuwe_vraag:
            blad.cell(rij, k['Vraag NL']).value = nieuwe_vraag
        blad.cell(rij, k['Antwoord']).value = antwoord
        blad.cell(rij, k['Bron (geverifieerd)']).value = bron
        blad.cell(rij, k['Bewijszin']).value = bewijs
        puzzels = waar.get(oude_vraag, [])
        geraakt.update(puzzels)
        print(f'Nr {nr}: {oud_antwoord} -> {antwoord}')
        print(f'   {(nieuwe_vraag or oude_vraag)[:92]}')
        if nieuwe_vraag:
            print(f'   was: {oude_vraag[:92]}')
        print(f'   raakt {len(puzzels)} puzzel(s): {", ".join(puzzels[:6])}')

    boek.save(REVIEW)
    print(f'\n{len(CORRECTIES)} vragen gecorrigeerd; {len(geraakt)} puzzels kloppen nu niet meer.')
    print('Draai na goedkeuring: puzzels/maak_unieke_puzzels.py --doel puzzels --schrijf'
          ' en --doel race --schrijf, dan puzzels/maak_breinkrakers.py.')


if __name__ == '__main__':
    main()
