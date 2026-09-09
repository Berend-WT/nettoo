# -*- coding: utf-8 -*-
"""Netto — zoek voor de hele vragenbank de foto van het onderwerpartikel.

Draaien:  python tools/zoek_onderwerpfotos_bulk.py [--aantal N] [--opnieuw]

WAAROM DIT SCRIPT NAAST zoek_onderwerpafbeeldingen.py BESTAAT
Dat script doet per vraag zes losse verzoeken met een pauze ertussen: zoeken in
twee talen, dan de infoboxfoto, dan de licentie. Gemeten tempo 1,2 vragen per
minuut, dus voor de hele bank ruim vijftien uur. Voor 62 vragen kan dat, voor
1400 niet.

Wikipedia kan het in twee stappen:
  1. generator=search samen met prop=pageimages geeft in EEN verzoek zowel het
     gevonden artikel als de foto uit de infobox.
  2. De licenties komen per vijftig bestanden tegelijk van Commons.

Daarmee is het ongeveer een verzoek per vraag in plaats van zes, en duurt de
hele bank twintig minuten in plaats van vijftien uur.

HOE BETROUWBAAR IS DE UITKOMST
Gemeten op de eerste 44: zonder toets klopt zeventig procent. Eist de toets dat
de naam van het gevonden artikel volledig in de vraag voorkomt, dan is het
drieentachtig procent — "Coca-Cola" haalt het, "Ah-Muzen-Cab" bij een vraag over
de negen Muzen niet. Die vlag komt in het bestand te staan als "naamtreffer",
zodat de keuze om hem wel of niet automatisch toe te passen apart te maken is.
"""

import argparse
import json
import os
import re
import ssl
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

import openpyxl

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zoek_onderwerpafbeeldingen as zo

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
FOTOS = os.path.join(WORTEL, 'fotos')
UIT = os.path.join(FOTOS, 'onderwerpfotos_bulk.json')
AGENT = 'Netto-fotozoeker/1.0 (penoftafel@gmail.com) fotokeuze voor een quizspel'
PAUZE = 0.35   # ruim onder de tien verzoeken per seconde die Wikipedia toestaat
GROEP = 50     # Commons neemt vijftig titels per verzoek

try:
    import certifi
    CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CONTEXT = ssl.create_default_context()


def api(host, params, pogingen=3):
    url = f'https://{host}/w/api.php?' + urllib.parse.urlencode(params)
    verzoek = urllib.request.Request(url, headers={'User-Agent': AGENT})
    for poging in range(pogingen):
        try:
            with urllib.request.urlopen(verzoek, timeout=30, context=CONTEXT) as a:
                return json.loads(a.read().decode('utf-8'))
        except urllib.error.HTTPError as fout:
            if fout.code != 429 or poging == pogingen - 1:
                return {}
            time.sleep(4 ** poging)
        except Exception:
            if poging == pogingen - 1:
                return {}
            time.sleep(2 ** poging)
    return {}


def plat(tekst):
    tekst = unicodedata.normalize('NFKD', str(tekst or '').lower())
    return ''.join(c for c in tekst if not unicodedata.combining(c))


def naamtreffer(artikeltitel, vraag):
    """Komt de naam van het gevonden artikel volledig in de vraag voor?

    Dat is het verschil tussen "Coca-Cola" bij een vraag over een blikje cola en
    "Ah-Muzen-Cab" bij een vraag over de negen Muzen. Haakjes tellen niet mee:
    het artikel "Odin (god)" hoort gewoon bij een vraag over Odin."""
    kern = re.findall(r"[a-z0-9']{3,}", plat(artikeltitel.split('(')[0]))
    return bool(kern) and all(woord in plat(vraag) for woord in kern)


def zoek_artikel_met_foto(taal, term):
    """Zoeken en de infoboxfoto ophalen in een enkel verzoek."""
    d = api(f'{taal}.wikipedia.org', {
        'action': 'query', 'format': 'json', 'formatversion': '2',
        'generator': 'search', 'gsrsearch': term, 'gsrlimit': '1', 'gsrnamespace': '0',
        'prop': 'pageimages', 'piprop': 'name',
    })
    paginas = (d.get('query', {}) or {}).get('pages', []) or []
    if not paginas:
        return None
    pagina = paginas[0]
    titel = pagina.get('title', '')
    if re.search(r'\((doorverwijspagina|disambiguation)\)', titel, re.I):
        return None
    if not pagina.get('pageimage'):
        return None
    return titel, pagina['pageimage']


def licenties(bestanden):
    """Licentie, maker en miniatuur voor maximaal vijftig bestanden tegelijk."""
    uit = {}
    for start in range(0, len(bestanden), GROEP):
        deel = bestanden[start:start + GROEP]
        d = api('commons.wikimedia.org', {
            'action': 'query', 'format': 'json', 'formatversion': '2',
            'titles': '|'.join('File:' + b for b in deel), 'prop': 'imageinfo',
            'iiprop': 'url|extmetadata|mime', 'iiurlwidth': '330',
        })
        for pagina in (d.get('query', {}) or {}).get('pages', []) or []:
            info = (pagina.get('imageinfo') or [{}])[0]
            mime = str(info.get('mime', ''))
            if not mime.startswith('image/') or mime.endswith('svg+xml'):
                continue
            meta = info.get('extmetadata') or {}
            naam = zo.zh.tekst(meta, 'LicenseShortName')
            if not naam:
                continue
            kleine = naam.casefold()
            if not (kleine.startswith('cc by') or kleine.startswith('cc0')
                    or kleine.startswith('pdm') or 'public domain' in kleine):
                continue
            uit[pagina['title']] = {
                'titel': pagina['title'],
                'pagina': info.get('descriptionurl', ''),
                'miniatuur': info.get('thumburl') or info.get('url', ''),
                'licentie': naam,
                'maker': (zo.zh.tekst(meta, 'Artist') or 'onbekend')[:120],
            }
        time.sleep(PAUZE)
    return uit


def main():
    ontleder = argparse.ArgumentParser()
    ontleder.add_argument('--aantal', type=int, default=0, help='0 = alles')
    ontleder.add_argument('--opnieuw', action='store_true', help='eerdere uitkomst negeren')
    args = ontleder.parse_args()

    gedaan = {} if args.opnieuw else (
        json.load(open(UIT, encoding='utf-8')) if os.path.exists(UIT) else {})

    blad = openpyxl.load_workbook(REVIEW, read_only=True)['Vragen']
    rijen = list(blad.iter_rows(values_only=True))
    k = {naam: n for n, naam in enumerate(rijen[0])}
    vragen = [(int(r[k['Nr']]), str(r[k['Vraag NL']])) for r in rijen[1:]
              if r[k['Nr']] is not None and str(k) and str(r[k['Nr']]) not in gedaan]
    if args.aantal:
        vragen = vragen[:args.aantal]

    print(f'{len(vragen)} vragen te doen ({len(gedaan)} al bekend)')
    begin = time.time()
    bestand_van = {}

    for teller, (nr, vraag) in enumerate(vragen, start=1):
        gevonden = None
        for term in zo.onderwerpen(vraag)[:2]:
            for taal in ('nl', 'en'):
                uitslag = zoek_artikel_met_foto(taal, term)
                time.sleep(PAUZE)
                if uitslag:
                    titel, bestand = uitslag
                    gevonden = {'artikel': f'https://{taal}.wikipedia.org/wiki/'
                                           + urllib.parse.quote(titel.replace(' ', '_')),
                                'artikeltitel': titel, 'gezocht': term,
                                'bestand': bestand,
                                'naamtreffer': naamtreffer(titel, vraag)}
                    break
            if gevonden:
                break
        gedaan[str(nr)] = gevonden or {}
        if gevonden:
            bestand_van.setdefault(gevonden['bestand'], []).append(str(nr))
        if teller % 25 == 0 or teller == len(vragen):
            with open(UIT, 'w', encoding='utf-8') as f:
                json.dump(gedaan, f, ensure_ascii=False)
            verstreken = (time.time() - begin) / 60
            tempo = teller / verstreken if verstreken else 0
            resterend = (len(vragen) - teller) / tempo if tempo else 0
            print(f'  {teller}/{len(vragen)} | {tempo:.0f} per minuut | '
                  f'nog ongeveer {resterend:.0f} minuten')

    # Licenties in groepen. Veel vragen delen een bestand, dus eerst ontdubbelen.
    nodig = sorted({v['bestand'] for v in gedaan.values() if v.get('bestand')})
    print(f'\nlicenties ophalen voor {len(nodig)} unieke bestanden ...')
    info = licenties(nodig)
    print(f'{len(info)} bestanden met een bruikbare licentie')

    kandidaten = {}
    zonder_licentie = 0
    for nr, v in gedaan.items():
        if not v.get('bestand'):
            continue
        gegevens = info.get('File:' + v['bestand'].replace('_', ' '))
        if not gegevens:
            zonder_licentie += 1
            continue
        if not __import__('maak_fotobestand').geschikt_beeld(gegevens['titel']):
            continue
        kandidaten[nr] = {'kandidaten': [dict(gegevens, artikel=v['artikel'],
                                              gezocht=v['gezocht'],
                                              naamtreffer=v['naamtreffer'])],
                          'herkomst': 'onderwerpartikel'}
    with open(os.path.join(FOTOS, 'onderwerpafbeeldingen.json'), 'w', encoding='utf-8') as f:
        json.dump(kandidaten, f, ensure_ascii=False, indent=1)

    treffers = sum(1 for v in kandidaten.values() if v['kandidaten'][0]['naamtreffer'])
    print(f'\n{len(kandidaten)} vragen met een foto | {treffers} daarvan met naamtreffer')
    print(f'{zonder_licentie} afgevallen op licentie')
    print(f'-> fotos/onderwerpafbeeldingen.json')


if __name__ == '__main__':
    main()
