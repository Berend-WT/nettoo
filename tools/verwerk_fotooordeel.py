# -*- coding: utf-8 -*-
"""Netto — verwerk Codex' oordeel over de fotovoorstellen.

Draaien:  python tools/verwerk_fotooordeel.py [bestand.tsv]

Invoer is een TSV met twee kolommen: vraagnummer en 1 of 0. Een 1 zet de
voorgestelde foto in het spel, een 0 haalt hem eruit.

WAAROM DIT LANGS EEN MODEL GAAT EN NIET LANGS EEN SCRIPT
Het zoeken is te automatiseren, het beoordelen niet. Of "Flag of Thailand" bij
een vraag over het Thaise alfabet hoort, is een vraag over betekenis: het land
klopt en het onderwerp niet. Elke regel die ik daarvoor bedacht - komt de naam
van het artikel in de vraag voor, deelt de bestandsnaam een woord met het
onderwerp - haalde hooguit driekwart. Lezen wat er staat werkt beter.

Wat overblijft voor Berend is dan alleen nog smaak, niet of het klopt.
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
STANDAARD = os.path.join(WORTEL, 'docs', 'fotos_oordeel.tsv')
KEUZE = os.path.join(WORTEL, 'vragen', 'fotokeuze.xlsx')
ONDERWERP = os.path.join(WORTEL, 'fotos', 'onderwerpafbeeldingen.json')
HANDMATIG = os.path.join(WORTEL, 'fotos', 'handmatige_fotos.json')


def main():
    pad = sys.argv[1] if len(sys.argv) > 1 else STANDAARD
    if not os.path.exists(pad):
        print(f'niet gevonden: {pad}')
        return

    oordeel = {}
    for regel in open(pad, encoding='utf-8'):
        delen = regel.rstrip('\n').rstrip('\r').split('\t')
        if len(delen) < 2:
            continue
        try:
            oordeel[int(delen[0])] = int(delen[1])
        except ValueError:
            continue
    goed = {nr for nr, w in oordeel.items() if w == 1}
    weg = {nr for nr, w in oordeel.items() if w == 0}
    print(f'{len(oordeel)} oordelen gelezen: {len(goed)} goed, {len(weg)} afgekeurd')
    if not oordeel:
        return

    onderwerp = json.load(open(ONDERWERP, encoding='utf-8'))
    handmatig = json.load(open(HANDMATIG, encoding='utf-8')) if os.path.exists(HANDMATIG) else {}

    # Een goedgekeurde foto gaat als handmatige keuze het spel in. Dat is
    # hetzelfde spoor als een door Berend geplakt adres, en het werkt ook voor
    # race- en breinkrakervragen, die niet in het keuzeblad staan.
    erbij, zonder = 0, 0
    for nr in sorted(goed):
        kandidaat = (onderwerp.get(str(nr), {}).get('kandidaten') or [None])[0]
        if not kandidaat:
            zonder += 1
            continue
        handmatig[str(nr)] = {
            'titel': kandidaat['titel'], 'pagina': kandidaat['pagina'],
            'url': kandidaat['miniatuur'], 'licentie': kandidaat['licentie'],
            'maker': kandidaat['maker'], 'bron': 'oordeel Codex',
        }
        erbij += 1
    with open(HANDMATIG, 'w', encoding='utf-8') as f:
        json.dump(handmatig, f, ensure_ascii=False, indent=1)
    print(f'{erbij} foto\'s klaargezet ({zonder} zonder kandidaat overgeslagen)')

    # Afgekeurde vragen krijgen een 0 in het keuzeblad, zodat ze niet in een
    # volgende beoordelingsronde terugkomen.
    if weg:
        shutil.copy2(KEUZE, os.path.join(
            os.path.dirname(KEUZE),
            f'_backup_codex_{date.today():%Y-%m-%d}_{os.path.basename(KEUZE)}'))
        boek = openpyxl.load_workbook(KEUZE)
        blad = boek['Fotokeuze']
        k = {naam: n for n, naam in enumerate([c.value for c in blad[1]], start=1)}
        gezet = 0
        for rij in range(2, blad.max_row + 1):
            nr = blad.cell(rij, k['Nr']).value
            if nr is not None and int(nr) in weg:
                blad.cell(rij, k['Keuze']).value = 0
                gezet += 1
        boek.save(KEUZE)
        print(f'{gezet} afgekeurde vragen op 0 gezet in het keuzeblad')

    print('Draai nu: python tools/maak_fotobestand.py')


if __name__ == '__main__':
    main()
