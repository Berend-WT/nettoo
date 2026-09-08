# -*- coding: utf-8 -*-
"""Netto — haal per vraag bruikbare fotokandidaten van Wikimedia Commons.

Draaien:  python tools/zoek_fotokandidaten.py [aantal]

Zonder aantal worden alle vragen in gebruik gedaan (dailies eerst). Het script
onthoudt wat het al heeft opgehaald in fotos/kandidaten.json, dus afbreken en
later verdergaan kan gewoon.

TWEE MANIEREN VAN ZOEKEN, IN DEZE VOLGORDE
Eerst de afbeeldingen die in het bronartikel zelf staan. Dat werkt beter dan
zoeken: het artikel gaat per definitie over het juiste onderwerp, dus een foto
eruit slaat nooit de plank mis. Bij de vraag over de Euromast levert zoeken op
"Euromast Rotterdam" ook foto's van andere Rotterdamse torens; het artikel niet.

Pas als het artikel niets bruikbaars heeft, valt het script terug op de
zoekfunctie van Commons met trefwoorden uit de vraag.

LICENTIE
Alleen bestanden waarvan Commons meldt dat ze CC BY, CC BY-SA, CC0 of publiek
domein zijn. De rest wordt overgeslagen. Van elk bestand worden de maker, de
licentie en de bestandspagina bewaard, zodat de naamsvermelding later klopt.
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
VOORTGANG = os.path.join(FOTOS, 'kandidaten.json')

COMMONS = 'https://commons.wikimedia.org/w/api.php'
AGENT = 'Netto-fotokandidaten/1.0 (educatief quizspel; contact via repo)'

# Bestandsnamen die op vrijwel elk Wikipedia-artikel staan en nooit over het
# onderwerp gaan: iconen, vlaggetjes, logo's van onderhoudssjablonen.
ROMMEL = re.compile(
    r'(commons-logo|wiki(pedia|media|source|quote|data)|edit-|ambox|question_book|'
    r'crystal|nuvola|folder|symbol_|icon|_icon|disambig|padlock|red_pencil|'
    r'star_(full|half|empty)|increase|decrease|steady|flag_of|coat_of_arms|'
    r'location_map|blue_pencil|magnify-clip|portal|gnome-|text_document|'
    r'information_icon|question,_web_fundamentals|office-book)', re.I)

RUIS = {
    'hoeveel', 'how', 'many', 'much', 'what', 'welk', 'welke', 'hoe', 'wat',
    'een', 'de', 'het', 'van', 'in', 'op', 'is', 'are', 'the', 'a', 'an', 'of',
    'zijn', 'er', 'en', 'and', 'or', 'die', 'dat', 'met', 'with', 'voor',
    'per', 'bij', 'aan', 'te', 'tot', 'als', 'does', 'do', 'has', 'have',
    'werd', 'wordt', 'heeft', 'hebben', 'telt', 'staan', 'staat', 'duurt',
    'ongeveer', 'about', 'gemiddeld', 'average', 'standaard', 'standard',
    'volgens', 'according', 'totaal', 'total', 'jaar', 'year', 'meter',
    'metres', 'meters', 'kilometer', 'kilometers', 'centimeter', 'millimeter',
    'kilogram', 'gram', 'liter', 'litres', 'ton', 'tons', 'procent', 'percent',
    'percentage', 'graden', 'degrees', 'seconde', 'seconden', 'seconds',
    'minuut', 'minuten', 'minutes', 'uur', 'hours', 'dagen', 'dag', 'days',
    'maanden', 'months', 'miljoen', 'million', 'miljard', 'billion', 'duizend',
    'thousand', 'aantal', 'number', 'lang', 'long', 'hoog', 'high', 'tall',
    'diep', 'deep', 'breed', 'wide', 'groot', 'large', 'zwaar', 'heavy',
    'maximaal', 'wereldwijd', 'worldwide', 'eerste', 'first', 'stand',
}


def context():
    if certifi:
        return ssl.create_default_context(cafile=certifi.where())
    return ssl.create_default_context()


def haal(endpoint, params, pogingen=4):
    vraag = urllib.parse.urlencode(params)
    verzoek = urllib.request.Request(
        f'{endpoint}?{vraag}',
        headers={'User-Agent': AGENT, 'Accept': 'application/json'})
    for poging in range(pogingen):
        try:
            with urllib.request.urlopen(verzoek, context=context(), timeout=30) as antwoord:
                return json.loads(antwoord.read().decode('utf-8'))
        except urllib.error.HTTPError as fout:
            if fout.code != 429 or poging == pogingen - 1:
                return {}
            time.sleep(min(20, 2 ** poging))
        except Exception:
            if poging == pogingen - 1:
                return {}
            time.sleep(1.5 ** poging)
    return {}


def tekstwaarde(meta, sleutel):
    blok = (meta or {}).get(sleutel) or {}
    ruw = blok.get('value', '') if isinstance(blok, dict) else ''
    return ' '.join(re.sub(r'<[^>]+>', ' ', str(ruw)).replace('&amp;', '&').split())


def bruikbaar(meta):
    """Geeft (licentienaam, maker) als het bestand herbruikbaar is, anders None."""
    naam = tekstwaarde(meta, 'LicenseShortName')
    k = naam.casefold()
    if not (k.startswith('cc by') or k.startswith('cc0') or k.startswith('pdm')
            or 'public domain' in k):
        return None
    return naam, (tekstwaarde(meta, 'Artist') or 'onbekend')[:120]


def bestandsinfo(titels):
    """Vraagt licentie en miniatuur op voor een reeks Commons-bestandstitels."""
    uit = []
    for i in range(0, len(titels), 20):
        data = haal(COMMONS, {
            'action': 'query', 'format': 'json', 'formatversion': '2',
            'titles': '|'.join(titels[i:i + 20]),
            'prop': 'imageinfo',
            'iiprop': 'url|extmetadata|size|mime',
            'iiurlwidth': '320',
        })
        for pagina in (data.get('query', {}) or {}).get('pages', []) or []:
            info = (pagina.get('imageinfo') or [{}])[0]
            if not str(info.get('mime', '')).startswith('image/'):
                continue
            if str(info.get('mime', '')).endswith('svg+xml'):
                continue
            vergunning = bruikbaar(info.get('extmetadata') or {})
            if not vergunning:
                continue
            licentie, maker = vergunning
            titel = str(pagina.get('title') or '')
            uit.append({
                'titel': titel,
                'pagina': 'https://commons.wikimedia.org/wiki/'
                          + urllib.parse.quote(titel.replace(' ', '_'), safe=":/(),!'"),
                'miniatuur': info.get('thumburl') or info.get('url'),
                'licentie': licentie,
                'maker': maker,
                'breedte': info.get('width'), 'hoogte': info.get('height'),
            })
        time.sleep(0.2)
    return uit


def uit_artikel(bron, hoeveel=3):
    """Afbeeldingen die in het bronartikel staan, in volgorde van voorkomen."""
    m = re.match(r'https://([a-z]+)\.wikipedia\.org/wiki/(.+)', str(bron))
    if not m:
        return []
    taal, titel = m.group(1), urllib.parse.unquote(m.group(2))
    data = haal(f'https://{taal}.wikipedia.org/w/api.php', {
        'action': 'query', 'format': 'json', 'formatversion': '2',
        'titles': titel, 'prop': 'images', 'imlimit': '40',
    })
    paginas = (data.get('query', {}) or {}).get('pages', []) or []
    if not paginas:
        return []
    namen = [b.get('title', '') for b in (paginas[0].get('images') or [])]
    namen = [n for n in namen if not ROMMEL.search(n)
             and not n.lower().endswith(('.svg', '.ogg', '.oga', '.webm'))]
    return bestandsinfo(namen[:12])[:hoeveel]


def uit_zoeken(nl, en, hoeveel=3):
    bron = en if isinstance(en, str) and en.strip() else nl
    woorden = re.findall(r"[A-Za-zÀ-ÿ'’-]{3,}", str(bron))
    term = ' '.join([w for w in woorden if w.lower() not in RUIS][:5])
    if not term:
        return []
    data = haal(COMMONS, {
        'action': 'query', 'format': 'json', 'formatversion': '2',
        'generator': 'search', 'gsrsearch': f'{term} filetype:bitmap',
        'gsrnamespace': '6', 'gsrlimit': '12',
        'prop': 'imageinfo', 'iiprop': 'url|extmetadata|size|mime',
        'iiurlwidth': '320',
    })
    namen = [p.get('title', '') for p in (data.get('query', {}) or {}).get('pages', []) or []]
    namen = [n for n in namen if not ROMMEL.search(n)]
    return bestandsinfo(namen[:12])[:hoeveel]


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
    en_kol = ('Vraag EN (zoekhulp)' if 'Vraag EN (zoekhulp)' in d.columns else None)

    open_nog = [r for _, r in d.iterrows() if str(int(r['Nr'])) not in gedaan]
    if grens:
        open_nog = open_nog[:grens]
    print(f'{len(gedaan)} al gedaan, {len(open_nog)} te gaan')

    for n, r in enumerate(open_nog, start=1):
        nr = int(r['Nr'])
        kand = uit_artikel(r['Bron (geverifieerd)'])
        herkomst = 'artikel'
        if not kand:
            kand = uit_zoeken(r['Vraag NL'], r[en_kol] if en_kol else None)
            herkomst = 'zoeken'
        gedaan[str(nr)] = {'herkomst': herkomst if kand else 'niets',
                           'kandidaten': kand}
        if n % 10 == 0 or n == len(open_nog):
            with open(VOORTGANG, 'w', encoding='utf-8') as f:
                json.dump(gedaan, f, ensure_ascii=False, indent=1)
            raak = sum(1 for v in gedaan.values() if v['kandidaten'])
            print(f'  {n}/{len(open_nog)} — {raak} van {len(gedaan)} met kandidaten')
        time.sleep(0.25)

    with open(VOORTGANG, 'w', encoding='utf-8') as f:
        json.dump(gedaan, f, ensure_ascii=False, indent=1)
    raak = sum(1 for v in gedaan.values() if v['kandidaten'])
    uit_art = sum(1 for v in gedaan.values() if v['herkomst'] == 'artikel')
    print(f'\n{raak} van {len(gedaan)} vragen hebben kandidaten '
          f'({uit_art} uit het bronartikel)')
    print(f'-> {VOORTGANG}')


if __name__ == '__main__':
    main()
