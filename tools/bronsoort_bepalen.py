# -*- coding: utf-8 -*-
"""Netto — bepaal per bronloze vraag wélke bron er nodig is.

Draaien:  python tools/bronsoort_bepalen.py

WAAROM
"399 vragen zonder bron" is geen werkbare lijst. "40 Guinness-records, 30
voedingswaarden, 12 CBS-cijfers" wel, want dan is per groep één bron genoeg in
plaats van veertig losse zoekopdrachten.

Wikipedia dekt deze vragen niet, en dat is geen tekortkoming van het zoeken maar
van de bron: records en voedingswaarden worden daar simpelweg niet opgenomen.
Een deel is bovendien helemaal niet te bronnen — een rekensom heeft geen bron,
en "de vaak geciteerde streefwaarde" van tienduizend stappen is een gezegde, geen
meting.
"""

import os
import re

import pandas as pd

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
RONDE2 = os.path.join(WORTEL, 'vragen', 'bronnen_ronde2.csv')
DOEL = os.path.join(WORTEL, 'vragen', 'bronsoort_nodig.csv')

# Volgorde telt: het eerste patroon dat past wint.
SOORTEN = [
    ('rekensom — geen bron mogelijk',
     r'\bsom van de getallen\b|hoeveel manieren kun je|hoeveel diagonalen|'
     r'hoeveel zijden heeft|graden heeft een|hoeveel is de som',
     'Dit is een berekening, geen feit. Een bron bestaat niet en is niet nodig.'),

    ('Guinness World Records',
     r'\b(langste|grootste|zwaarste|kleinste|hoogste|meeste|oudste|snelste|verste)\b'
     r'[^?]*\booit\b|guinness|\brecord\b',
     'guinnessworldrecords.com — records staan niet op Wikipedia.'),

    ('voedingswaarde',
     r'\b(kcal|kilocalorie|calorie|gram eiwit|gram suiker|gram koolhydraten|'
     r'gram vet|voedingswaarde)\b',
     'Voedingscentrum (NL) of de USDA FoodData Central (internationaal).'),

    ('CBS of nationaal statistiekbureau',
     r'gemiddelde nederlander|nederlander gemiddeld|per nederlander|'
     r'hoeveel procent van de nederlanders|nederlandse huishoudens',
     'CBS StatLine — deze cijfers staan niet op Wikipedia.'),

    ('bedrijfscijfer',
     r'wereldwijd (?:ongeveer|per|jaarlijks)|hoeveel (?:filialen|winkels|restaurants)|'
     r'verkocht .* wereldwijd|hoeveel .* per seconde',
     'Jaarverslag of persmap van het bedrijf zelf.'),

    ('sportbond of competitie',
     r'hoeveel (?:etappes|holes|innings|periodes|pogingen)|'
     r'speeltijd|hoeveel punten levert|hoeveel spelers',
     'Het reglement van de bond (FIFA, NBA, UCI, World Rugby).'),

    ('praktijkkennis — bron twijfelachtig',
     r'hoe lang kook|hoeveel stappen per dag|vaak geciteerde|'
     r'hoeveel minuten kook',
     'Er is geen gezaghebbende bron; dit is een vuistregel. Overweeg te schrappen.'),

    ('natuurgegevens',
     r'\b(soorten|dier|vogel|vinvis|potvis|stern|olifant|tijger|leeuw|kolibrie|'
     r'lemuur|kangoeroe|koala|krokodil|anaconda)\b',
     'IUCN Red List, of een naslagwerk als de Encyclopedia of Life.'),
]


def main():
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    zonder = d[d['Bron (bestaand)'].isna() & d['Bron (geverifieerd)'].isna()].copy()

    # Wat ronde twee alsnog vond, valt af.
    if os.path.exists(RONDE2):
        r2 = pd.read_csv(RONDE2)
        gevonden = set(r2[r2['Status'] == 'bevestigd']['Nr'])
        zonder = zonder[~zonder['Nr'].isin(gevonden)]
        print(f'ronde twee vond er alsnog {len(gevonden)}')

    rijen = []
    for _, r in zonder.iterrows():
        vraag = str(r['Vraag NL'])
        soort, advies = 'algemeen naslagwerk', 'Handmatig opzoeken; geen vaste bron aan te wijzen.'
        for naam, patroon, hulp in SOORTEN:
            if re.search(patroon, vraag, re.I):
                soort, advies = naam, hulp
                break
        rijen.append({
            'Nr': int(r['Nr']), 'In gebruik': r['In gebruik'],
            'Categorie': r['Categorie'], 'Vraag NL': vraag,
            'Antwoord': r['Antwoord'],
            'Welke bron nodig': soort, 'Waar te vinden': advies,
            'Bron (door jou)': None,
        })

    uit = pd.DataFrame(rijen).sort_values(['Welke bron nodig', 'In gebruik', 'Nr'])
    uit.to_csv(DOEL, index=False, encoding='utf-8-sig')

    print(f'\n{len(uit)} vragen nog zonder bron, verdeeld naar wat ze nodig hebben:\n')
    for soort, groep in uit.groupby('Welke bron nodig'):
        inuse = int((groep['In gebruik'] != '—').sum())
        print(f'  {soort:38s} {len(groep):4d}   (waarvan in gebruik: {inuse})')
    print(f'\n-> {DOEL}')


if __name__ == '__main__':
    main()
