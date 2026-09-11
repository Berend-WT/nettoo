# -*- coding: utf-8 -*-
"""Netto — verwerk het oordeel over de wachtende fotokandidaten.

Draaien:  python tools/verwerk_wachtoordeel.py oordeel.json

INVOER
Een JSON met twee lijsten vraagnummers:

    {"goed": [108, 140], "fout": [17, 85]}

Goedgekeurde kandidaten gaan als handmatige keuze het spel in — hetzelfde spoor
als een door de eigenaar geplakt adres, en dat werkt ook voor race- en
breinkrakervragen, die niet in het keuzeblad staan.

Afgekeurde gaan op de blokkeerlijst, op vraagtekst. Dat is met opzet dezelfde
lijst als waarmee de eerder afgekeurde foto's zijn tegengehouden: een afkeuring
die alleen als nul in het keuzeblad landt, pakt niet bij vragen die daar niet in
staan, en dan komt dezelfde foto een ronde later gewoon terug.

WAAROM DIT NIET AUTOMATISCH KAN
De kandidaten komen uit een zoekactie die het onderwerp uit de vraagtekst raadt.
Dat levert een foto van een voetballer op bij een vraag over de twaalf
Olympiërs, en een speelgoedkrokodil bij een vraag over het hart van een
krokodil. Of een beeld ergens bij past is een vraag over betekenis; daar helpt
geen regel tegen.
"""

import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import maak_fotobestand as mf
import maak_wachtvellen as mw

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HANDMATIG = os.path.join(WORTEL, 'fotos', 'handmatige_fotos.json')
GEBLOKKEERD = os.path.join(WORTEL, 'fotos', 'geblokkeerd.json')


def main():
    if len(sys.argv) < 2:
        print('gebruik: python tools/verwerk_wachtoordeel.py oordeel.json')
        return
    oordeel = json.load(open(sys.argv[1], encoding='utf-8'))
    goed = {int(n) for n in oordeel.get('goed', [])}
    fout = {int(n) for n in oordeel.get('fout', [])}
    print(f'{len(goed)} goedgekeurd, {len(fout)} afgekeurd')

    wacht = {r['nr']: r for r in mw.wachtenden()}
    onbekend = (goed | fout) - set(wacht)
    if onbekend:
        print(f'{len(onbekend)} nummers staan niet in de wachtrij: {sorted(onbekend)[:8]}')

    handmatig = mf.lees(HANDMATIG)
    erbij = 0
    for nr in sorted(goed):
        rij = wacht.get(nr)
        if not rij:
            continue
        k = rij['kandidaat']
        handmatig[str(nr)] = {
            'titel': k['titel'], 'pagina': k['pagina'], 'url': k['miniatuur'],
            'licentie': k['licentie'], 'maker': k['maker'], 'bron': 'wachtrij beoordeeld',
        }
        erbij += 1
    with open(HANDMATIG, 'w', encoding='utf-8') as f:
        json.dump(handmatig, f, ensure_ascii=False, indent=1)
    print(f'{erbij} foto\'s toegevoegd aan handmatige_fotos.json')

    blok = mf.lees(GEBLOKKEERD)
    vragen = set(blok.get('vragen', []))
    voor = len(vragen)
    for nr in sorted(fout):
        rij = wacht.get(nr)
        if rij:
            vragen.add(rij['vraag'])
    blok['vragen'] = sorted(vragen)
    with open(GEBLOKKEERD, 'w', encoding='utf-8') as f:
        json.dump(blok, f, ensure_ascii=False, indent=1)
    print(f'{len(vragen) - voor} vragen op de blokkeerlijst (nu {len(vragen)})')
    print('\nDraai nu: python tools/maak_fotobestand.py')


if __name__ == '__main__':
    main()
