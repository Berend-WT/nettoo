# -*- coding: utf-8 -*-
"""Netto — haal per vraag de hoofdafbeelding van het bronartikel op.

Draaien:  python tools/zoek_hoofdafbeeldingen.py [aantal]

WAAROM DIT BETER IS DAN DE VORIGE RONDE
De eerste poging pakte de eerste drie afbeeldingen uit een artikel, in de
volgorde waarin ze in de tekst staan. Dat leverde bij de kakkerlak een
eierleggend exemplaar op en bij de Eiffeltoren bouwfoto's uit 1888: wel over het
onderwerp, maar niet de foto die je van dat onderwerp verwacht.

Elk Wikipedia-artikel heeft er precies een die dat wel is — de afbeelding
bovenaan in de infobox. De API geeft die rechtstreeks via prop=pageimages, en
dat is een enkele netwerkronde per vraag in plaats van drie. Sneller en
trefzekerder tegelijk.

Er wordt geen tweede en derde kandidaat meer gezocht. Bij de vorige ronde kwamen
die vrijwel altijd uit de zoekfunctie, en die bleek de zwakste schakel: bij een
vraag over knipperen met je ogen kwam een foto van Michael Jackson boven. Een
goede eerste is meer waard dan drie middelmatige.

LICENTIE
Zoals eerder: alleen CC BY, CC BY-SA, CC0 en publiek domein. Maker en licentie
worden bewaard voor de naamsvermelding.
"""

import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

import pandas as pd

try:
    import certifi
except ImportError:
    certifi = None

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
FOTOS = os.path.join(WORTEL, 'fotos')
VOORTGANG = os.path.join(FOTOS, 'hoofdafbeeldingen.json')

AGENT = 'Netto-hoofdafbeelding/1.0 (educatief quizspel; contact via repo)'

# Sommige vragen hebben een uitstekende bron die geen Wikipedia-artikel is —
# FAO voor landbouwcijfers, Guinness voor records, Smithsonian voor vulkanen.
# Daar valt geen infobox-afbeelding uit te halen, terwijl het onderwerp zich
# prima laat fotograferen. Voor die gevallen wijst deze lijst een artikel aan
# dat alleen voor het beeld wordt gebruikt; de bron van het antwoord verandert
# niet.
BEELDARTIKEL = {
    'Hoeveel ton bananen worden wereldwijd jaarlijks geproduceerd?':
        'https://en.wikipedia.org/wiki/Banana',
    'Hoeveel mensen namen deel aan de grootste massale yogales?':
        'https://en.wikipedia.org/wiki/Yoga',
    'Hoeveel actieve vulkanen zijn er op aarde naar schatting?':
        'https://en.wikipedia.org/wiki/Volcano',
}


def context():
    return ssl.create_default_context(cafile=certifi.where()) if certifi \
        else ssl.create_default_context()


def haal(host, params, pogingen=4):
    u = f'https://{host}/w/api.php?' + urllib.parse.urlencode(params)
    verzoek = urllib.request.Request(u, headers={'User-Agent': AGENT})
    for poging in range(pogingen):
        try:
            with urllib.request.urlopen(verzoek, context=context(), timeout=25) as a:
                return json.loads(a.read().decode('utf-8'))
        except urllib.error.HTTPError as f:
            if f.code != 429 or poging == pogingen - 1:
                return {}
            time.sleep(min(20, 3 ** poging))
        except Exception:
            if poging == pogingen - 1:
                return {}
            time.sleep(2 ** poging)
    return {}


def tekst(meta, sleutel):
    blok = (meta or {}).get(sleutel) or {}
    ruw = blok.get('value', '') if isinstance(blok, dict) else ''
    return ' '.join(re.sub(r'<[^>]+>', ' ', str(ruw)).replace('&amp;', '&').split())


def bruikbaar(meta):
    naam = tekst(meta, 'LicenseShortName')
    k = naam.casefold()
    if not (k.startswith('cc by') or k.startswith('cc0') or k.startswith('pdm')
            or 'public domain' in k):
        return None
    return naam, (tekst(meta, 'Artist') or 'onbekend')[:120]


def hoofdafbeelding(bron):
    """De infobox-afbeelding van het bronartikel, met licentie erbij."""
    m = re.match(r'https://([a-z]+)\.wikipedia\.org/wiki/(.+)', str(bron))
    if not m:
        return None
    taal, titel = m.group(1), urllib.parse.unquote(m.group(2))
    d = haal(f'{taal}.wikipedia.org', {
        'action': 'query', 'format': 'json', 'formatversion': '2',
        'titles': titel, 'prop': 'pageimages', 'piprop': 'original|name',
    })
    paginas = (d.get('query', {}) or {}).get('pages', []) or []
    if not paginas:
        return None
    naam = paginas[0].get('pageimage')
    if not naam:
        return None
    # Het bestand staat vrijwel altijd op Commons; daar staat de licentie.
    c = haal('commons.wikimedia.org', {
        'action': 'query', 'format': 'json', 'formatversion': '2',
        'titles': 'File:' + naam, 'prop': 'imageinfo',
        'iiprop': 'url|extmetadata|size|mime', 'iiurlwidth': '320',
    })
    cp = (c.get('query', {}) or {}).get('pages', []) or []
    if not cp or 'missing' in cp[0]:
        return None
    info = (cp[0].get('imageinfo') or [{}])[0]
    if not str(info.get('mime', '')).startswith('image/'):
        return None
    if str(info.get('mime', '')).endswith('svg+xml'):
        return None
    v = bruikbaar(info.get('extmetadata') or {})
    if not v:
        return None
    licentie, maker = v
    t = 'File:' + naam
    return {'titel': t,
            'pagina': 'https://commons.wikimedia.org/wiki/'
                      + urllib.parse.quote(t.replace(' ', '_'), safe=":/(),!'"),
            'miniatuur': info.get('thumburl') or info.get('url'),
            'licentie': licentie, 'maker': maker,
            'breedte': info.get('width'), 'hoogte': info.get('height')}


def main():
    grens = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else None
    os.makedirs(FOTOS, exist_ok=True)
    gedaan = {}
    if os.path.exists(VOORTGANG):
        with open(VOORTGANG, encoding='utf-8') as f:
            gedaan = json.load(f)

    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    d = d[d['In gebruik'].isin(['daily', 'puzzel'])].copy()
    d['_r'] = d['In gebruik'].map({'daily': 0, 'puzzel': 1})
    d = d.sort_values(['_r', 'Nr'])

    open_nog = [r for _, r in d.iterrows() if str(int(r['Nr'])) not in gedaan]
    if grens:
        open_nog = open_nog[:grens]
    print(f'{len(gedaan)} al gedaan, {len(open_nog)} te gaan', flush=True)

    for n, r in enumerate(open_nog, start=1):
        nr = int(r['Nr'])
        foto = hoofdafbeelding(BEELDARTIKEL.get(str(r['Vraag NL']),
                                                r['Bron (geverifieerd)']))
        gedaan[str(nr)] = {'kandidaten': [foto] if foto else [],
                           'herkomst': 'hoofdafbeelding' if foto else 'niets'}
        if n % 20 == 0 or n == len(open_nog):
            with open(VOORTGANG, 'w', encoding='utf-8') as f:
                json.dump(gedaan, f, ensure_ascii=False, indent=1)
            raak = sum(1 for v in gedaan.values() if v['kandidaten'])
            print(f'  {n}/{len(open_nog)} — {raak} van {len(gedaan)} met foto', flush=True)
        # Twee verzoeken per vraag. Bij 0,15 seconde ertussen kwam dat neer op
        # ruim tien per seconde, en dan geeft Wikipedia stilzwijgend niets meer
        # terug: van 25 vragen leverden er 18 ten onrechte niets op, terwijl
        # dezelfde vraag los aangeroepen wel een foto gaf.
        time.sleep(0.6)

    with open(VOORTGANG, 'w', encoding='utf-8') as f:
        json.dump(gedaan, f, ensure_ascii=False, indent=1)
    raak = sum(1 for v in gedaan.values() if v['kandidaten'])
    print(f'\n{raak} van {len(gedaan)} vragen hebben een hoofdafbeelding')
    print(f'-> {VOORTGANG}')


if __name__ == '__main__':
    main()
