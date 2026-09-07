# -*- coding: utf-8 -*-
"""Netto — controleer de bronnen die er al stonden maar nooit zijn nagekeken.

Draaien:  python tools/controleer_oude_bronnen.py [aantal]

WAAROM
496 vragen hebben een bron uit een eerdere ronde die nooit is geverifieerd.
Britannica, NASA, WHO, UNESCO — degelijke adressen, maar niemand heeft
gecontroleerd of het gevraagde getal er daadwerkelijk staat. Zo'n rij ziet er
betrouwbaarder uit dan een leeg vakje, terwijl een leeg vakje tenminste niet
liegt.

Dit script haalt elke bronpagina op en zoekt het antwoord in de tekst, met de
zin eromheen als bewijs.

WAT EEN UITKOMST BETEKENT
  bevestigd     Het getal staat op de pagina, in een zin die over het gevraagde
                gaat. De bron klopt.
  getal gezien  Het getal staat op de pagina, maar niet in een herkenbare zin.
  niet gevonden Het getal staat er niet. Dat betekent niet meteen dat de bron
                fout is: veel pagina's laden hun inhoud met javascript, of
                zetten het getal in een tabel of afbeelding. Wel een reden om
                zelf te kijken.
  onbereikbaar  De pagina gaf een foutmelding of blokkeerde het ophalen.
"""

import gzip
import io
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
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
DOEL = os.path.join(WORTEL, 'vragen', 'oude_bronnen_gecontroleerd.csv')

AGENT = ('Mozilla/5.0 (compatible; NettoPuzzle/1.0; '
         '+https://github.com/Berend-WT/nettoo) bronverificatie')

MAATWOORD = re.compile(
    r'\b(meter|meters|metre|metres|feet|foot|kilometer|kilometre|centimeter|'
    r'kilogram|kilo|gram|ton|tonne|pound|liter|litre|percent|procent|degrees|'
    r'graden|year|years|jaar|day|days|dagen|hour|hours|uur|minute|minutes|'
    r'chapters|hoofdstukken|episodes|afleveringen|seasons|seizoenen|rooms|'
    r'kamers|floors|verdiepingen|steps|treden|species|soorten|countries|landen|'
    r'islands|eilanden|people|inhabitants|inwoners|neurons|neuronen|bones|'
    r'botten|teeth|tanden|players|spelers|members|leden|seats|zetels|'
    r'chromosomes|chromosomen|billion|miljard|million|miljoen)\b', re.I)


def context():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


CTX = context()


def haal_pagina(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': AGENT,
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'nl,en;q=0.9',
        'Accept-Encoding': 'gzip',
    })
    with urllib.request.urlopen(req, timeout=20, context=CTX) as r:
        ruw = r.read()
        if r.headers.get('Content-Encoding') == 'gzip':
            ruw = gzip.decompress(ruw)
        soort = r.headers.get('Content-Type', '')
    if 'html' not in soort and 'text' not in soort:
        return ''
    tekst = ruw.decode('utf-8', errors='replace')
    # Script en stijl eruit; die zitten vol getallen die niets betekenen.
    tekst = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', tekst)
    tekst = re.sub(r'(?s)<[^>]+>', ' ', tekst)
    tekst = (tekst.replace('&nbsp;', ' ').replace('&amp;', '&')
             .replace('&#39;', "'").replace('&quot;', '"'))
    return ' '.join(tekst.split())


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


def zoek_bewijs(vraag, antwoord, tekst):
    vs = varianten(antwoord)
    if not vs or not tekst:
        return 'niet gevonden', ''
    gevraagd = {m.group(0).lower() for m in MAATWOORD.finditer(vraag)}
    zwak = ''
    for zin in re.split(r'(?<=[.!?])\s+', tekst):
        if len(zin) > 400:
            continue
        if not any(re.search(rf'(?<![\d.,\-–]){re.escape(v)}(?!\d|,\d{{3}})', zin)
                   for v in vs):
            continue
        maten = {m.group(0).lower() for m in MAATWOORD.finditer(zin)}
        if gevraagd & maten or not gevraagd:
            return 'bevestigd', zin.strip()[:320]
        if not zwak:
            zwak = zin.strip()[:320]
    return ('getal gezien', zwak) if zwak else ('niet gevonden', '')


def bewaar(df, pad):
    """Schrijft weg, ook als het doelbestand in Excel openstaat.

    De eerste volledige run klapte na 175 van de 496 regels eruit met een
    PermissionError omdat het bestand op dat moment geopend was. Tussentijds
    wegschrijven is bedoeld om werk te behouden; dan mag het niet juist de
    oorzaak zijn dat alles verloren gaat.
    """
    try:
        df.to_csv(pad, index=False, encoding='utf-8-sig')
        return pad
    except PermissionError:
        wijk = pad.replace('.csv', '_nieuw.csv')
        df.to_csv(wijk, index=False, encoding='utf-8-sig')
        return wijk


def main():
    aantal = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 10 ** 9
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    oud = d[d['Bron (bestaand)'].notna() & d['Bron (geverifieerd)'].isna()]

    # Hervatten waar een vorige run stopte, zodat al opgehaalde pagina's niet
    # nog een keer bij vreemde servers worden opgevraagd.
    rijen, gedaan = [], set()
    if os.path.exists(DOEL):
        eerder = pd.read_csv(DOEL)
        rijen = eerder.to_dict('records')
        gedaan = set(int(n) for n in eerder['Nr'])
        print(f'{len(gedaan)} al gedaan in een eerdere run', flush=True)
    oud = oud[~oud['Nr'].isin(gedaan)].head(aantal)
    print(f'{len(oud)} nog te controleren\n', flush=True)
    for i, (_, r) in enumerate(oud.iterrows(), start=1):
        url = str(r['Bron (bestaand)']).strip()
        status, bewijs = 'onbereikbaar', ''
        if url.startswith('http'):
            try:
                tekst = haal_pagina(url)
                status, bewijs = zoek_bewijs(str(r['Vraag NL']), r['Antwoord'], tekst)
            except urllib.error.HTTPError as e:
                status, bewijs = 'onbereikbaar', f'HTTP {e.code}'
            except Exception as e:                       # noqa: BLE001
                status, bewijs = 'onbereikbaar', str(e)[:80]
        else:
            status, bewijs = 'geen url', url[:80]

        rijen.append({'Nr': int(r['Nr']), 'In gebruik': r['In gebruik'],
                      'Vraag NL': r['Vraag NL'], 'Antwoord': r['Antwoord'],
                      'Bron': url, 'Uitkomst': status, 'Bewijszin': bewijs})
        if i % 25 == 0:
            uit = pd.DataFrame(rijen)
            print(f'  {i}/{len(oud)} — '
                  + ', '.join(f'{k}: {v}' for k, v in uit['Uitkomst'].value_counts().items()),
                  flush=True)
            bewaar(uit, DOEL)
        time.sleep(0.6)                                  # beleefd tegen vreemde servers

    uit = pd.DataFrame(rijen)
    pad = bewaar(uit, DOEL)
    print('\n' + uit['Uitkomst'].value_counts().to_string())
    if pad != DOEL:
        print(f'LET OP: {DOEL} stond open; weggeschreven naar {pad}')
    print(f'\n-> {pad}')


if __name__ == '__main__':
    main()
