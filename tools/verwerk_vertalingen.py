# -*- coding: utf-8 -*-
"""Netto — zet verbeterde Engelse vraagteksten in de vertaalcatalogus.

Draaien:  python tools/verwerk_vertalingen.py [bestand.tsv]

Invoer is een TSV met twee kolommen: de Nederlandse vraag zoals hij in de
catalogus staat, en de nieuwe Engelse zin. Een kopregel mag, lege regels ook.

WAAROM NIET RECHTSTREEKS IN HET JS-BESTAND
netto_translations_en.js is een object van 2.386 sleutels met CRLF-regeleindes.
Met de hand bijwerken gaat een keer goed en daarna niet meer: een ontbrekende
komma of een verkeerd ontsnapt aanhalingsteken maakt het hele bestand stuk, en
dan laadt de frontend zonder foutmelding gewoon geen enkele vertaling meer.

Een sleutel die niet in de catalogus staat wordt toegevoegd; dat is precies wat
er moet gebeuren voor de vragen die nu helemaal geen vertaling hebben.
"""

import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BESTANDEN = [os.path.join(WORTEL, 'data', 'netto_translations_en.js'),
             os.path.join(WORTEL, 'website', 'data', 'netto_translations_en.js')]
KOP = ('// Generated offline from the canonical Dutch frontend and puzzle data.\r\n'
       'window.NETTO_TRANSLATIONS_EN = {\r\n')


def lees_tsv(pad):
    nieuw = {}
    with open(pad, encoding='utf-8') as f:
        for regel in f:
            regel = regel.rstrip('\n').rstrip('\r')
            if not regel.strip():
                continue
            delen = regel.split('\t')
            if len(delen) < 2:
                continue
            nl, en = delen[-2].strip(), delen[-1].strip()
            if not nl or not en or nl.lower() in ('nederlands', 'vlag'):
                continue
            nieuw[nl] = en
    return nieuw


def main():
    pad = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        WORTEL, 'docs', 'vertalingen_engels_nieuw.tsv')
    if not os.path.exists(pad):
        print(f'niet gevonden: {pad}')
        return
    nieuw = lees_tsv(pad)
    print(f'{len(nieuw)} regels gelezen uit {os.path.relpath(pad, WORTEL)}')

    with open(BESTANDEN[0], encoding='utf-8') as f:
        tekst = f.read()
    catalogus = json.loads(tekst[tekst.index('{'):tekst.rindex('}') + 1])

    gewijzigd = toegevoegd = gelijk = 0
    for nl, en in nieuw.items():
        if nl not in catalogus:
            toegevoegd += 1
        elif catalogus[nl] != en:
            gewijzigd += 1
        else:
            gelijk += 1
            continue
        catalogus[nl] = en

    # Zelfde vorm als het bestaande bestand: twee spaties inspringen, de
    # volgorde van invoeging, CRLF. Zo blijft het verschil in git leesbaar.
    regels = [f'  {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}'
              for k, v in catalogus.items()]
    uit = KOP + ',\r\n'.join(regels) + '\r\n};\r\n'
    for bestand in BESTANDEN:
        with open(bestand, 'w', encoding='utf-8', newline='') as f:
            f.write(uit)

    # Controle: het bestand moet nog steeds geldige JSON bevatten.
    with open(BESTANDEN[0], encoding='utf-8') as f:
        proef = f.read()
    json.loads(proef[proef.index('{'):proef.rindex('}') + 1])
    print(f'gewijzigd {gewijzigd} | nieuw {toegevoegd} | ongewijzigd {gelijk}'
          f' | catalogus telt nu {len(catalogus)} sleutels')
    print('Vergeet het cachenummer van netto_translations_en.js niet in beide index.html.')


if __name__ == '__main__':
    main()
