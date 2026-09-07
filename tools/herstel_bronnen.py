# -*- coding: utf-8 -*-
"""Netto — verifieer geblokkeerde bronnen via het Internet Archive.

Draaien:  python tools/herstel_bronnen.py [geblokkeerd|nietgevonden|beide]

WAAROM HET ARCHIEF
163 bronnen blokkeren geautomatiseerd ophalen — Britannica voorop. Die pagina's
bestaan wel degelijk, ze weigeren alleen een robot. Het Internet Archive heeft er
een kopie van en serveert die zonder blokkade, dus daar is het antwoord alsnog
te controleren.

Datzelfde archief laat iets anders zien over de 83 dode links: van vijftien
steekproeven had er één een kopie. Van een pagina die ooit online stond bewaart
het archief er doorgaans wel een. Dat er niets van bestaat, wijst erop dat die
adressen nooit hebben bestaan.

TWEEDE VERBETERING
Voor de 215 pagina's die het getal niet leken te noemen, kijkt dit script ook in
tabellen en lijsten. De vorige ronde knipte de tekst in zinnen op een punt, en
een tabelcel eindigt niet op een punt — daardoor werden cijfers in tabellen
stelselmatig gemist.
"""

import gzip
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

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(WORTEL, 'vragen', 'oude_bronnen_gecontroleerd.csv')
DOEL = os.path.join(WORTEL, 'vragen', 'bronnen_hersteld.csv')

AGENT = ('Mozilla/5.0 (compatible; NettoPuzzle/1.0; '
         '+https://github.com/Berend-WT/nettoo) bronverificatie')

# Nederlands en Engels naar één begrip. Zonder deze stap gold "979 metres" niet
# als bewijs bij een vraag om meters: "meter" en "metres" zijn verschillende
# woorden, en de vergelijking keek naar woorden in plaats van naar betekenis.
BEGRIPPEN = {
    'lengte':   r'meter|meters|metre|metres|kilometer|kilometre|kilometers|km',
    'kort':     r'centimeter|centimetre|centimeters|inch|inches',
    'voet':     r'feet|foot',
    'massa':    r'kilogram|kilograms|kilo|kg|gram|grams|ton|tonne|tonnes|pound|pounds|lb',
    'volume':   r'liter|litre|liters|litres',
    'deel':     r'percent|per cent|procent|percentage',
    'hoek':     r'degrees|graden',
    'tijd':     r'year|years|jaar|jaren|day|days|dagen|hour|hours|uur|minute|minutes|'
                r'minuten|second|seconds|seconden|maanden|months',
    'aflevering': r'episodes|afleveringen|seasons|seizoenen|series',
    'hoofdstuk': r'chapters|hoofdstukken|books|boeken|volumes|delen',
    'ruimte':   r'rooms|kamers|floors|storeys|stories|verdiepingen|steps|stairs|treden|'
                r'elevators|lifts|liften|towers|torens|columns|zuilen',
    'soort':    r'species|soorten',
    'gebied':   r'countries|nations|landen|islands|eilanden|states|staten|provinces',
    'mensen':   r'people|inhabitants|population|inwoners|residents',
    'lichaam':  r'neurons|neuronen|bones|botten|teeth|tanden|chromosomes|chromosomen|'
                r'muscles|spieren',
    'sport':    r'players|spelers|members|leden|seats|zetels|teams',
    'schaal':   r'billion|miljard|million|miljoen|thousand|duizend',
    'muziek':   r'strings|snaren|keys|toetsen|notes|noten',
    'voertuig': r'wheels|wielen|engines|motoren',
}
BEGRIP_PATRONEN = [(naam, re.compile(rf'\b(?:{p})\b', re.I)) for naam, p in BEGRIPPEN.items()]


def begrippen(tekst):
    """Welke soorten maat komen in deze tekst voor?"""
    return {naam for naam, patroon in BEGRIP_PATRONEN if patroon.search(tekst)}


def context():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


CTX = context()


def haal(url, timeout=25):
    req = urllib.request.Request(url, headers={
        'User-Agent': AGENT, 'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'nl,en;q=0.9', 'Accept-Encoding': 'gzip'})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as r:
        ruw = r.read()
        if r.headers.get('Content-Encoding') == 'gzip':
            ruw = gzip.decompress(ruw)
        soort = r.headers.get('Content-Type', '')
    if 'html' not in soort and 'text' not in soort:
        return ''
    return ruw.decode('utf-8', errors='replace')


def naar_fragmenten(html):
    """Splitst een pagina in leesbare brokken.

    De vorige ronde knipte op zinseinden. Een tabelcel eindigt niet op een punt,
    dus stonden cijfers in tabellen buiten bereik. Hier worden blokelementen
    eerst tot losse fragmenten gemaakt, zodat een cel op zichzelf telt.
    """
    html = re.sub(r'(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>', ' ', html)
    html = re.sub(r'(?i)</(td|th|li|p|div|tr|h[1-6]|dd|dt)>', '   ', html)
    html = re.sub(r'(?i)<br\s*/?>', '   ', html)
    tekst = re.sub(r'(?s)<[^>]+>', ' ', html)
    for a, b in (('&nbsp;', ' '), ('&amp;', '&'), ('&#39;', "'"), ('&quot;', '"'),
                 ('&ndash;', '-'), ('&mdash;', '-')):
        tekst = tekst.replace(a, b)
    brokken = []
    for blok in tekst.split(' '):
        blok = ' '.join(blok.split())
        if not blok:
            continue
        # Lange lappen alsnog op zinnen knippen.
        brokken.extend(z.strip() for z in re.split(r'(?<=[.!?])\s+', blok) if z.strip())
    return [b for b in brokken if len(b) < 400]


def varianten(antwoord):
    try:
        n = int(float(antwoord))
    except (TypeError, ValueError):
        return []
    s = str(abs(n))
    uit = {s}
    if len(s) > 3:
        uit.add('{:,}'.format(abs(n)))
        uit.add('{:,}'.format(abs(n)).replace(',', '.'))
        uit.add('{:,}'.format(abs(n)).replace(',', ' '))
    return sorted(uit, key=len, reverse=True)


def zoek(vraag, antwoord, html):
    vs = varianten(antwoord)
    if not vs or not html:
        return 'niet gevonden', ''
    gevraagd = begrippen(vraag)
    zwak = ''
    for brok in naar_fragmenten(html):
        if not any(re.search(rf'(?<![\d.,\-–]){re.escape(v)}(?!\d|,\d{{3}})', brok)
                   for v in vs):
            continue
        if gevraagd & begrippen(brok) or not gevraagd:
            return 'bevestigd', brok[:320]
        if not zwak:
            zwak = brok[:320]
    return ('getal gezien', zwak) if zwak else ('niet gevonden', '')


def archiefkopie(url):
    q = 'https://archive.org/wayback/available?' + urllib.parse.urlencode({'url': url})
    req = urllib.request.Request(q, headers={'User-Agent': AGENT})
    with urllib.request.urlopen(req, timeout=25, context=CTX) as r:
        d = json.loads(r.read().decode('utf-8'))
    s = (d.get('archived_snapshots') or {}).get('closest') or {}
    return s.get('url') if s.get('available') else None


def main():
    welke = sys.argv[1] if len(sys.argv) > 1 else 'beide'
    d = pd.read_csv(BRON)
    bewijs = d['Bewijszin'].astype(str)

    geblokkeerd = d[(d['Uitkomst'] == 'onbereikbaar') & bewijs.str.contains('403')]
    nietgevonden = d[d['Uitkomst'] == 'niet gevonden']

    taken = []
    if welke in ('geblokkeerd', 'beide'):
        taken.append(('geblokkeerd', geblokkeerd))
    if welke in ('nietgevonden', 'beide'):
        taken.append(('niet gevonden', nietgevonden))

    rijen = []
    for soort, sub in taken:
        print(f'\n=== {soort}: {len(sub)} bronnen ===', flush=True)
        for i, (_, r) in enumerate(sub.iterrows(), start=1):
            url = str(r['Bron'])
            uitkomst, zin, gebruikte = 'niet gevonden', '', url
            try:
                if soort == 'geblokkeerd':
                    kopie = archiefkopie(url)
                    time.sleep(0.3)
                    if not kopie:
                        uitkomst = 'geen archiefkopie'
                    else:
                        gebruikte = kopie
                        uitkomst, zin = zoek(str(r['Vraag NL']), r['Antwoord'], haal(kopie, 30))
                else:
                    uitkomst, zin = zoek(str(r['Vraag NL']), r['Antwoord'], haal(url))
            except urllib.error.HTTPError as e:
                uitkomst, zin = 'onbereikbaar', f'HTTP {e.code}'
            except Exception as e:                       # noqa: BLE001
                uitkomst, zin = 'onbereikbaar', str(e)[:70]

            rijen.append({'Nr': int(r['Nr']), 'Groep': soort,
                          'In gebruik': r['In gebruik'], 'Vraag NL': r['Vraag NL'],
                          'Antwoord': r['Antwoord'], 'Oorspronkelijke bron': url,
                          'Gebruikte bron': gebruikte, 'Uitkomst': uitkomst,
                          'Bewijszin': zin})
            if i % 25 == 0:
                uit = pd.DataFrame(rijen)
                print(f'  {i}/{len(sub)} — '
                      + ', '.join(f'{k}: {v}' for k, v in uit['Uitkomst'].value_counts().items()),
                      flush=True)
                try:
                    uit.to_csv(DOEL, index=False, encoding='utf-8-sig')
                except PermissionError:
                    pass
            time.sleep(0.4)

    uit = pd.DataFrame(rijen)
    uit.to_csv(DOEL, index=False, encoding='utf-8-sig')
    print('\n' + uit.groupby('Groep')['Uitkomst'].value_counts().to_string())
    print(f'\n-> {DOEL}')


if __name__ == '__main__':
    main()
