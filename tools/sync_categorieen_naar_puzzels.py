# -*- coding: utf-8 -*-
"""Netto — zet de categorieën uit de vragenbank door naar de puzzeldata.

Draaien:  python tools/sync_categorieen_naar_puzzels.py

WAAROM
De puzzelbestanden dragen per puzzel een lijstje van drie categorieën mee, één
per vraag. Die lijstjes zijn ooit meegegenereerd en daarna niet meer bijgewerkt,
terwijl de bank wél is opgeschoond. Daardoor tekende de landingspagina een
pootafdruk boven een honkbalvraag: de icoonkeuze leest die lijstjes.

Dit script raakt uitsluitend het veld "categories" aan. De samenstelling van de
puzzels — welke vragen bij elkaar staan, de operator, de antwoorden — blijft
letterlijk ongemoeid, zodat de koppeling met source_library_id in de database
intact blijft.
"""

import io
import json
import os

import pandas as pd

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK = os.path.join(WORTEL, 'vragen', '1000+ vragen netjes gecategoriseerd.xlsx')
# Alleen deze twee dragen een categories-veld. netto_race_pool.js en
# netto_breinkrakers.js hebben er geen, dus daar valt niets bij te werken.
BESTANDEN = ['data/netto_frontend_puzzles.js', 'data/netto_race_sets.js']


def lees_js(pad):
    """Haalt het JSON-deel uit een 'window.X = {...};'-bestand."""
    ruw = io.open(pad, encoding='utf-8').read()
    kop, _, rest = ruw.partition('=')
    return kop + '= ', json.loads(rest.strip().rstrip(';')), ruw


def loop_puzzels(data):
    """Levert elke puzzel-dict op, ongeacht of data een dict of lijst is."""
    groepen = data.values() if isinstance(data, dict) else [data]
    for groep in groepen:
        if isinstance(groep, list):
            for puzzel in groep:
                if isinstance(puzzel, dict):
                    yield puzzel


def main():
    bank = pd.read_excel(BANK)
    kaart = {
        str(r['Vraag NL']).strip(): str(r['Categorie']).strip()
        for _, r in bank.iterrows()
    }
    print(f'bank: {len(kaart)} unieke vragen\n')

    totaal_gewijzigd = totaal_slots = onbekend = 0
    for naam in BESTANDEN:
        pad = os.path.join(WORTEL, naam)
        if not os.path.exists(pad):
            print(f'{naam}: overgeslagen (bestaat niet)')
            continue
        kop, data, _ = lees_js(pad)

        gewijzigd = slots = mis = 0
        for puzzel in loop_puzzels(data):
            cats = puzzel.get('categories')
            if not isinstance(cats, list):
                continue
            for i, sleutel in enumerate(('q1', 'q2', 'q3')):
                if i >= len(cats):
                    break
                vraag = str(puzzel.get(f'{sleutel}_label') or '').strip()
                if not vraag:
                    continue
                slots += 1
                nieuw = kaart.get(vraag)
                if nieuw is None:
                    mis += 1
                elif cats[i] != nieuw:
                    cats[i] = nieuw
                    gewijzigd += 1

        io.open(pad, 'w', encoding='utf-8').write(
            kop + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n'
        )
        print(f'{naam}: {gewijzigd} van {slots} categorieën bijgewerkt'
              f'{f", {mis} vragen niet in de bank" if mis else ""}')
        totaal_gewijzigd += gewijzigd
        totaal_slots += slots
        onbekend += mis

    print(f'\ntotaal: {totaal_gewijzigd} van {totaal_slots} bijgewerkt, '
          f'{onbekend} vragen niet gevonden in de bank')


if __name__ == '__main__':
    main()
