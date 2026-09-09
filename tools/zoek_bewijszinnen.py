# -*- coding: utf-8 -*-
"""Netto — haal bij een vraag de zin op waarin het antwoord echt staat.

Draaien:  python tools/zoek_bewijszinnen.py [--filter plaatshouder|verdacht]

WAAROM
Een bron die "klopt" omdat het getal ergens op de pagina voorkomt, klopt niet.
"Hoeveel tramlijnen heeft Amsterdam" kreeg 15 uit "in de 15e eeuw", en de vraag
over de Duitse deelstaten kreeg 16 uit "16 nationale parken". Alleen een zin
waarin het getal én het onderwerp staan is bewijs.

Dit script haalt de bronpagina op en zoekt de zinnen waar het antwoord in staat,
in alle schrijfwijzen die ertoe doen (1860, 1,860, 1.860). Het kiest niet: het
legt de kandidaten naast elkaar in een werkbestand, met per zin hoeveel woorden
uit de vraag erin terugkomen. De keuze blijft mensenwerk, want juist het
automatisch kiezen is wat deze fouten heeft veroorzaakt.
"""

import argparse
import gzip
import html
import io
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

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
UIT = os.path.join(WORTEL, 'vragen', 'bewijszinnen_kandidaten.json')
PLAATSHOUDER = 'bestaande bron opgehaald'
AGENT = 'Netto-broncontrole/1.0 (penoftafel@gmail.com) bronverificatie voor een quizspel'

try:
    import certifi
    CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CONTEXT = ssl.create_default_context()

STOP = set('''de het een en van in op te dat die is was zijn er voor met als aan
door bij uit over naar hoeveel welke welk hoe veel jaar ongeveer wereldwijd
the of a an to in on for and is are was were how many much what which'''.split())


def plat(tekst):
    tekst = unicodedata.normalize('NFKD', str(tekst or '').lower())
    return ''.join(c for c in tekst if not unicodedata.combining(c))


def haal(url):
    verzoek = urllib.request.Request(url, headers={
        'User-Agent': AGENT, 'Accept-Encoding': 'gzip',
        'Accept': 'text/html,application/xhtml+xml'})
    with urllib.request.urlopen(verzoek, timeout=30, context=CONTEXT) as antwoord:
        rauw = antwoord.read()
        if antwoord.headers.get('Content-Encoding') == 'gzip':
            rauw = gzip.decompress(rauw)
        soort = antwoord.headers.get_content_charset() or 'utf-8'
    return rauw.decode(soort, errors='replace')


def wikipedia_tekst(url):
    """Wikipedia geeft via de API schone tekst; het scrapen van de HTML levert
    daar alleen navigatie en sjabloonrommel op."""
    m = re.match(r'https://([a-z]+)\.wikipedia\.org/wiki/(.+)', url)
    if not m:
        return None
    taal, titel = m.group(1), urllib.parse.unquote(m.group(2).split('#')[0])
    api = (f'https://{taal}.wikipedia.org/w/api.php?action=query&prop=extracts'
           f'&explaintext=1&format=json&titles={urllib.parse.quote(titel)}')
    pagina = next(iter(json.loads(haal(api))['query']['pages'].values()))
    return pagina.get('extract')


def naar_tekst(rouwe_html):
    tekst = re.sub(r'(?is)<(script|style|nav|footer|header|svg)[^>]*>.*?</\1>', ' ', rouwe_html)
    tekst = re.sub(r'(?s)<[^>]+>', ' ', tekst)
    return re.sub(r'[ \t\xa0]+', ' ', html.unescape(tekst))


def getalvormen(antwoord):
    """Dezelfde 1860 heet op de ene pagina 1,860 en op de andere 1.860."""
    n = int(antwoord)
    vormen = {str(n), f'{n:,}', f'{n:,}'.replace(',', '.'), f'{n:,}'.replace(',', ' ')}
    if n >= 1000 and n % 1000 == 0:
        vormen.add(f'{n // 1000},000' if n < 10 ** 6 else str(n))
    return {v for v in vormen if v}


def zinnen_met(tekst, antwoord):
    gevonden = []
    for zin in re.split(r'(?<=[.!?])\s+|\n+', tekst):
        zin = zin.strip()
        if not 20 <= len(zin) <= 400:
            continue
        for vorm in getalvormen(antwoord):
            # Grens eromheen, anders vindt 15 ook een treffer in 2015.
            if re.search(r'(?<![\d.,])' + re.escape(vorm) + r'(?![\d.,]?\d)', zin):
                gevonden.append(zin)
                break
    return gevonden


def raakvlak(vraag, zin):
    woorden = {w for w in re.findall(r'[a-z]{4,}', plat(vraag)) if w not in STOP}
    return sum(1 for w in woorden if w in plat(zin))


def main():
    ontleder = argparse.ArgumentParser()
    ontleder.add_argument('--filter', default='plaatshouder')
    ontleder.add_argument('--pauze', type=float, default=1.0)
    args = ontleder.parse_args()

    blad = openpyxl.load_workbook(REVIEW, read_only=True)['Vragen']
    rijen = list(blad.iter_rows(values_only=True))
    kop = list(rijen[0])
    k = {naam: n for n, naam in enumerate(kop)}

    doel = []
    for rij in rijen[1:]:
        bewijs = plat(rij[k['Bewijszin']])
        if args.filter == 'plaatshouder' and PLAATSHOUDER not in bewijs:
            continue
        try:
            antwoord = int(rij[k['Antwoord']])
        except (TypeError, ValueError):
            continue
        doel.append((int(rij[k['Nr']]), str(rij[k['Vraag NL']]), antwoord,
                     str(rij[k['Bron (geverifieerd)']] or '')))

    print(f'{len(doel)} vragen ophalen ...')
    uitkomst = []
    for teller, (nr, vraag, antwoord, bron) in enumerate(doel, start=1):
        regel = {'nr': nr, 'vraag': vraag, 'antwoord': antwoord, 'bron': bron}
        try:
            tekst = wikipedia_tekst(bron) if 'wikipedia.org' in bron else None
            if tekst is None:
                tekst = naar_tekst(haal(bron))
            kandidaten = zinnen_met(tekst, antwoord)
            kandidaten.sort(key=lambda z: -raakvlak(vraag, z))
            regel['zinnen'] = [{'zin': z, 'raakvlak': raakvlak(vraag, z)}
                               for z in kandidaten[:4]]
            regel['status'] = 'gevonden' if kandidaten else 'getal niet op de pagina'
        except Exception as fout:
            regel['zinnen'] = []
            regel['status'] = f'{type(fout).__name__}: {fout}'[:120]
        uitkomst.append(regel)
        print(f'  {teller:>3}/{len(doel)} Nr {nr:<5} {regel["status"][:44]:<46} '
              f'{len(regel["zinnen"])} zin(nen)')
        time.sleep(args.pauze)

    with open(UIT, 'w', encoding='utf-8') as f:
        json.dump(uitkomst, f, ensure_ascii=False, indent=1)
    gevonden = sum(1 for r in uitkomst if r['zinnen'])
    print(f'\n{gevonden} van {len(uitkomst)} met minstens een kandidaat '
          f'-> {os.path.relpath(UIT, WORTEL)}')


if __name__ == '__main__':
    main()
