# -*- coding: utf-8 -*-
"""Netto — laat vlaggen, kaarten en logo's alsnog toe als kandidaat.

Draaien:  python tools/vul_svg_kandidaten_aan.py

WAT ER MIS WAS
De zoekronde gooide elke SVG weg. Dat kwam uit de tijd dat een SVG los in een
img-tag terechtkwam, waar hij onvoorspelbaar groot werd of met de verkeerde
letters. Maar Commons rastert een SVG zelf: vraag je om een miniatuur van 330
pixels breed, dan krijg je een PNG terug. Die bezwaren gelden dus niet.

Wat we ermee weggooiden was geen rommel: 216 bestanden, goed voor 437 vragen.
De vlag van Zwitserland bij een vraag over Zwitserland, de kaart van Antarctica,
het logo van Feyenoord. Voor een schatvraag is dat vaak beter beeld dan een
willekeurige foto, want een vlag of kaart is eenduidig.

Dit script vult alleen aan: bestaande kandidaten blijven staan.
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zoek_onderwerpfotos_bulk as b
import maak_fotobestand as mf

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOTOS = os.path.join(WORTEL, 'fotos')
BULK = os.path.join(FOTOS, 'onderwerpfotos_bulk.json')
DOEL = os.path.join(FOTOS, 'onderwerpafbeeldingen.json')


def licenties(bestanden, sta_svg=True):
    """Zelfde als in de bulkzoeker, maar SVG mag mee. De miniatuur die Commons
    teruggeeft is dan een PNG, dus de frontend merkt er niets van."""
    uit = {}
    for start in range(0, len(bestanden), 50):
        deel = bestanden[start:start + 50]
        d = b.api('commons.wikimedia.org', {
            'action': 'query', 'format': 'json', 'formatversion': '2',
            'titles': '|'.join('File:' + x for x in deel), 'prop': 'imageinfo',
            'iiprop': 'url|extmetadata|mime', 'iiurlwidth': '330',
        })
        for pagina in (d.get('query', {}) or {}).get('pages', []) or []:
            info = (pagina.get('imageinfo') or [{}])[0]
            if not info:
                continue
            mime = str(info.get('mime', ''))
            if not mime.startswith('image/'):
                continue
            if mime.endswith('svg+xml') and not (sta_svg and info.get('thumburl')):
                continue
            meta = info.get('extmetadata') or {}
            naam = b.zo.zh.tekst(meta, 'LicenseShortName')
            kleine = naam.casefold()
            if not (kleine.startswith('cc by') or kleine.startswith('cc0')
                    or kleine.startswith('pdm') or 'public domain' in kleine):
                continue
            uit[pagina['title']] = {
                'titel': pagina['title'],
                'pagina': info.get('descriptionurl', ''),
                'miniatuur': info.get('thumburl') or info.get('url', ''),
                'licentie': naam,
                'maker': (b.zo.zh.tekst(meta, 'Artist') or 'onbekend')[:120],
            }
        time.sleep(0.35)
    return uit


def main():
    bulk = json.load(open(BULK, encoding='utf-8'))
    doel = json.load(open(DOEL, encoding='utf-8'))
    ontbreekt = sorted({v['bestand'] for nr, v in bulk.items()
                        if v.get('bestand') and nr not in doel})
    print(f'{len(doel)} vragen hebben al een kandidaat; {len(ontbreekt)} bestanden opnieuw proberen')

    info = licenties(ontbreekt)
    print(f'{len(info)} daarvan hebben een bruikbare licentie')

    erbij, geweigerd = 0, 0
    for nr, v in bulk.items():
        if nr in doel or not v.get('bestand'):
            continue
        gegevens = info.get('File:' + v['bestand'].replace('_', ' '))
        if not gegevens:
            continue
        if not mf.geschikt_beeld(gegevens['titel']):
            geweigerd += 1
            continue
        # Zelfde eis als bij de rest: bij een gewoon woord moet het gevonden
        # artikel dat woord in zijn titel hebben, anders is het toeval.
        term = v.get('gezocht', '')
        if not term[:1].isupper() and not b.naamtreffer(v.get('artikeltitel', ''), term):
            titelwoorden = b.plat(v.get('artikeltitel', ''))
            if not any(w[:3] and w[:3] in titelwoorden
                       for w in b.plat(term).split()):
                continue
        doel[nr] = {'kandidaten': [dict(gegevens, artikel=v['artikel'],
                                        gezocht=term, naamtreffer=v['naamtreffer'])],
                    'herkomst': 'onderwerpartikel'}
        erbij += 1

    json.dump(doel, open(DOEL, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{erbij} vragen erbij ({geweigerd} afgekeurd op ongeschikt beeld)')
    print(f'totaal nu {len(doel)} vragen met een kandidaat -> {os.path.relpath(DOEL, WORTEL)}')


if __name__ == '__main__':
    main()
