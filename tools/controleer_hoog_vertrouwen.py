# -*- coding: utf-8 -*-
"""Netto — zoek verdachte bronnen binnen de groep met vertrouwen "hoog".

Draaien:  python tools/controleer_hoog_vertrouwen.py [uitvoerpad]

De 42 bronnen met vertrouwen "matig" bleken vaak het juiste getal op een pagina
over een heel ander onderwerp te vinden. Die kwamen uit dezelfde ronde als de
685 met vertrouwen "hoog", dus is het de vraag of daar hetzelfde in zit.

De toets is grof maar goedkoop: haal de inhoudswoorden uit de vraag en kijk of
er minstens een van terugkomt in het adres van de bron. Een artikel dat "wombat"
heet komt zo langs, "Kilogram" niet. Het is nadrukkelijk geen bewijs van fout —
"Hoeveel poten heeft een krab" met en.wikipedia.org/wiki/Crab valt door de mand
op de taal, niet op de inhoud — maar het brengt de gevallen boven die het
nakijken waard zijn.
"""

import os
import re
import sys

import pandas as pd

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')

STOP = {
    'hoeveel', 'wat', 'welk', 'welke', 'hoe', 'wie', 'waar', 'jaar', 'jaren',
    'een', 'de', 'het', 'van', 'in', 'op', 'is', 'zijn', 'er', 'en', 'of',
    'die', 'dat', 'met', 'voor', 'per', 'bij', 'aan', 'te', 'tot', 'als',
    'werd', 'wordt', 'heeft', 'hebben', 'telt', 'staan', 'staat', 'duurt',
    'ongeveer', 'gemiddeld', 'gemiddelde', 'standaard', 'volgens', 'totaal',
    'meter', 'kilometer', 'centimeter', 'millimeter', 'kilogram', 'gram',
    'liter', 'ton', 'procent', 'graden', 'seconde', 'seconden', 'minuut',
    'minuten', 'uur', 'uren', 'dagen', 'dag', 'maanden', 'miljoen', 'miljard',
    'duizend', 'aantal', 'lang', 'hoog', 'diep', 'breed', 'groot', 'zwaar',
    'maximaal', 'wereldwijd', 'eerste', 'nieuwe', 'oude', 'grootste', 'kleinste',
}


def woorden(vraag):
    ws = re.findall(r'[a-zA-Zàâçéèêëîïôûùüÿñæœáíóúäöü]{4,}', str(vraag).lower())
    return [w for w in ws if w not in STOP]


def main():
    doel = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WORTEL, 'verdacht_hoog.txt')
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    s = d[d['Vertrouwen bron'] == 'hoog']

    verdacht = []
    for _, r in s.iterrows():
        adres = str(r['Bron (geverifieerd)']).lower()
        ws = woorden(r['Vraag NL'])
        if not ws:
            continue
        # Ook de stam telt mee: "piramides" moet "pyramid" niet raken, maar
        # "olifant" moet wel op "olifant" in een Nederlands adres passen.
        if any(w[:5] in adres for w in ws):
            continue
        verdacht.append(r)

    regels = []
    for r in verdacht:
        regels.append(f"{int(r['Nr'])} [{r['In gebruik']}] {r['Vraag NL']} -> {r['Antwoord']}")
        regels.append(f"     {r['Bron (geverifieerd)']}")
        regels.append(f"     bewijs: {str(r['Bewijszin'])[:160]}")
    with open(doel, 'w', encoding='utf-8') as f:
        f.write('\n'.join(regels))

    print(f'{len(s)} met vertrouwen hoog, {len(verdacht)} zonder woordoverlap -> {doel}')


if __name__ == '__main__':
    main()
