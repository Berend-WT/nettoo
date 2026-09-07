# -*- coding: utf-8 -*-
"""Netto — derde bronronde voor de reservevragen die nog niets hebben.

Draaien:  python tools/bronnen_ronde3.py [aantal]

WAT ER ANDERS IS DAN RONDE ÉÉN EN TWEE
Twee verbeteringen die pas bij het herstelwerk boven kwamen:

1. Eenheden worden genormaliseerd. "979 metres" gold niet als bewijs bij een
   vraag om meters, omdat "meter" en "metres" verschillende woorden zijn. De
   vergelijking keek naar woorden in plaats van naar betekenis.

2. Tabellen tellen mee. De vorige rondes knipten een pagina op zinseinden, en
   een tabelcel eindigt niet op een punt. Cijfers in tabellen en infoboxen
   vielen daardoor stelselmatig buiten bereik.

Verder wordt zowel de lopende tekst als de wikitekst doorzocht, en wordt het
artikel eerst nagelopen op onderwerp — zonder die zeef leverde "Hoeveel landen
zijn lid van de G20?" het artikel Holocaust op.
"""

import json
import os
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request

import pandas as pd

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
DOEL = os.path.join(WORTEL, 'vragen', 'bronnen_ronde3.csv')

AGENT = 'NettoPuzzle/1.0 (https://github.com/Berend-WT/nettoo; bronverificatie)'

STOP = {
    'hoeveel', 'wat', 'welk', 'welke', 'hoe', 'veel', 'het', 'de', 'een', 'van',
    'in', 'op', 'bij', 'met', 'aan', 'voor', 'door', 'tot', 'per', 'ongeveer',
    'telt', 'heeft', 'bevat', 'werd', 'zijn', 'staat', 'staan', 'duurt', 'weegt',
    'maakt', 'volgens', 'er', 'en', 'of', 'als', 'die', 'dat', 'zich', 'ons',
    'naar', 'uit', 'over', 'wordt', 'worden', 'kan', 'iedere', 'elke',
    'standaard', 'gemiddeld', 'totaal', 'samen', 'ooit', 'benadering',
}

BEGRIPPEN = {
    'lengte': r'meter|meters|metre|metres|kilometer|kilometre|kilometers|km',
    'kort': r'centimeter|centimetre|centimeters|inch|inches',
    'massa': r'kilogram|kilograms|kilo|kg|gram|grams|ton|tonne|tonnes|pound|pounds',
    'volume': r'liter|litre|liters|litres',
    'deel': r'percent|per cent|procent|percentage',
    'hoek': r'degrees|graden',
    'tijd': r'year|years|jaar|jaren|day|days|dagen|hour|hours|uur|minute|minutes|'
            r'minuten|second|seconds|seconden|maanden|months|weken|weeks',
    'werk': r'episodes|afleveringen|seasons|seizoenen|chapters|hoofdstukken|books|'
            r'boeken|volumes|delen|albums|songs|nummers|films|movies',
    'bouw': r'rooms|kamers|floors|storeys|stories|verdiepingen|steps|stairs|treden|'
            r'elevators|lifts|liften|towers|torens|columns|zuilen|arches|bogen',
    'soort': r'species|soorten|breeds|rassen',
    'gebied': r'countries|nations|landen|islands|eilanden|states|staten|provinces|'
              r'provincies|regions|regios',
    'mensen': r'people|inhabitants|population|inwoners|residents|bevolking',
    'lichaam': r'neurons|neuronen|bones|botten|teeth|tanden|chromosomes|chromosomen|'
               r'muscles|spieren|hearts|harten',
    'sport': r'players|spelers|members|leden|seats|zetels|teams|goals|doelpunten',
    'schaal': r'billion|miljard|million|miljoen|thousand|duizend',
    'muziek': r'strings|snaren|keys|toetsen|notes|noten|symphonies|symfonieen',
    'voertuig': r'wheels|wielen|engines|motoren|wagons|rijtuigen',
    'dier': r'legs|poten|wings|vleugels|eyes|ogen|humps|bulten|tentacles|tentakels',
}
BEGRIP_PATRONEN = [(n, re.compile(rf'\b(?:{p})\b', re.I)) for n, p in BEGRIPPEN.items()]
EIGENNAAM = re.compile(r"\b[A-Z][\wÀ-ſ'’-]+(?:\s+(?:[A-Z][\wÀ-ſ'’-]+|van|de|der|the|of))*")


def context():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


CTX = context()


def api(taal, params, pogingen=3):
    url = f'https://{taal}.wikipedia.org/w/api.php?' + urllib.parse.urlencode(
        {**params, 'format': 'json', 'formatversion': '2'})
    req = urllib.request.Request(url, headers={'User-Agent': AGENT})
    for poging in range(pogingen):
        try:
            with urllib.request.urlopen(req, timeout=25, context=CTX) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception:                                # noqa: BLE001
            if poging < pogingen - 1:
                time.sleep(2 * (poging + 1))
                continue
            raise
    return {}


def woorden(tekst):
    return [w for w in re.findall(r"[\wÀ-ſ'’-]+", str(tekst).lower())
            if w not in STOP and len(w) > 3]


def onderwerpwoorden(tekst):
    """Woorden die het ONDERWERP aanduiden, zonder maatwoorden.

    Maatwoorden staan bewust niet in STOP, want ze moeten meetellen bij het
    beoordelen van een bewijszin. Maar bij het kiezen van een artikel richten ze
    juist schade aan: de vraag "Hoeveel meter lang wordt een zoutwaterkrokodil?"
    kwam uit bij het artikel Electricity meter, omdat "meter" in beide voorkomt.
    Voor onderwerpherkenning gaan ze er dus alsnog uit.
    """
    maten = set()
    for _, patroon in BEGRIP_PATRONEN:
        maten.update(m.group(0).lower() for m in patroon.finditer(str(tekst)))
    return [w for w in woorden(tekst) if w not in maten]


def begrippen(tekst):
    return {n for n, p in BEGRIP_PATRONEN if p.search(str(tekst))}


def zoektermen(vraag_nl, vraag_en):
    uit = []
    for tekst in (str(vraag_nl), str(vraag_en or '')):
        if not tekst.strip():
            continue
        for naam in sorted(EIGENNAAM.findall(' '.join(tekst.split()[1:])),
                           key=len, reverse=True):
            naam = naam.strip(' .,?')
            if len(naam) > 3:
                uit.append(naam)
    for tekst in (vraag_nl, vraag_en):
        k = onderwerpwoorden(tekst)
        if len(k) >= 2:
            uit.append(' '.join(k[:3]))
            uit.append(' '.join(k[:2]))
    gezien, uniek = set(), []
    for t in uit:
        if t and t.lower() not in gezien:
            gezien.add(t.lower())
            uniek.append(t)
    return uniek[:4]


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


def fragmenten(tekst, wikitekst):
    """Zinnen uit de lopende tekst plus losse regels uit de wikitekst.

    Een infoboxregel als "| hoogte = 185 m" is geen zin en zou bij een knip op
    zinseinden nooit als los fragment overblijven.
    """
    uit = [z.strip() for z in re.split(r'(?<=[.!?])\s+', str(tekst)) if z.strip()]
    for regel in str(wikitekst).splitlines():
        regel = regel.strip()
        if regel.startswith('|') and '=' in regel and len(regel) < 300:
            uit.append(' '.join(re.sub(r'<[^>]+>|\[\[|\]\]', ' ', regel).split()))
    return [f for f in uit if len(f) < 400]


def bewijs(vraag, antwoord, tekst, wikitekst):
    vs = varianten(antwoord)
    if not vs:
        return None, None
    gevraagd = begrippen(vraag)
    onderwerp = set(onderwerpwoorden(vraag))
    zwak = None
    for f in fragmenten(tekst, wikitekst):
        if not any(re.search(rf'(?<![\d.,\-–]){re.escape(v)}(?!\d|,\d{{3}})', f)
                   for v in vs):
            continue
        if gevraagd & begrippen(f):
            return f[:320], 'getal staat bij dezelfde soort maat als de vraag'
        if onderwerp & set(woorden(f)):
            return f[:320], 'getal staat in een zin over het onderwerp'
        if zwak is None:
            zwak = f[:320]
    return (zwak, 'getal komt voor zonder herkenbaar verband') if zwak else (None, None)


def artikel_past(titel, term, vraag):
    """Gaat dit artikel over het onderwerp van de vraag?

    Kijkt naar onderwerpwoorden, niet naar maatwoorden — anders past elk artikel
    met "meter" in de titel bij elke vraag die naar meters vraagt.
    """
    t = set(onderwerpwoorden(titel))
    return bool(t & set(onderwerpwoorden(term))) or bool(t & set(onderwerpwoorden(vraag)))


def haal(taal, term):
    r = api(taal, {'action': 'query', 'generator': 'search', 'gsrsearch': term,
                   'gsrlimit': '1', 'prop': 'extracts|revisions',
                   'explaintext': '1', 'rvprop': 'content', 'rvslots': 'main'})
    p = ((r.get('query') or {}).get('pages') or [None])[0]
    if not p:
        return None, '', '', ''
    wt = ''
    try:
        wt = p['revisions'][0]['slots']['main'].get('content', '')
    except (KeyError, IndexError, TypeError):
        pass
    return (p.get('title'), p.get('extract') or '', wt,
            f"https://{taal}.wikipedia.org/wiki/"
            + urllib.parse.quote(str(p.get('title', '')).replace(' ', '_')))


def main():
    aantal = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 9
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    open_vragen = d[d['Bron (bestaand)'].isna() & d['Bron (geverifieerd)'].isna()]
    open_vragen = open_vragen[open_vragen['In gebruik'] == '—'].head(aantal)
    print(f'{len(open_vragen)} reservevragen zonder bron\n', flush=True)

    rijen = []
    for i, (_, r) in enumerate(open_vragen.iterrows(), start=1):
        vraag = str(r['Vraag NL'])
        gevonden = None
        for term in zoektermen(vraag, r.get('Vraag EN (zoekhulp)')):
            for taal in ('nl', 'en'):
                try:
                    titel, tekst, wt, url = haal(taal, term)
                except Exception:                        # noqa: BLE001
                    continue
                time.sleep(0.15)
                if not titel or not artikel_past(titel, term, vraag):
                    continue
                zin, waarom = bewijs(vraag, r['Antwoord'], tekst, wt)
                if zin and waarom != 'getal komt voor zonder herkenbaar verband':
                    gevonden = (titel, url, zin, waarom)
                    break
            if gevonden:
                break

        if gevonden:
            titel, url, zin, waarom = gevonden
            rijen.append({'Nr': int(r['Nr']), 'Status': 'bevestigd',
                          'Vraag NL': vraag, 'Antwoord': r['Antwoord'],
                          'Bron': url, 'Artikel': titel, 'Bewijszin': zin,
                          'Toelichting': waarom})
        else:
            rijen.append({'Nr': int(r['Nr']), 'Status': 'niet gevonden',
                          'Vraag NL': vraag, 'Antwoord': r['Antwoord'],
                          'Bron': '', 'Artikel': '', 'Bewijszin': '', 'Toelichting': ''})

        if i % 25 == 0:
            uit = pd.DataFrame(rijen)
            print(f'  {i}/{len(open_vragen)} — '
                  + ', '.join(f'{k}: {v}' for k, v in uit['Status'].value_counts().items()),
                  flush=True)
            try:
                uit.to_csv(DOEL, index=False, encoding='utf-8-sig')
            except PermissionError:
                pass
        time.sleep(0.2)

    uit = pd.DataFrame(rijen)
    uit.to_csv(DOEL, index=False, encoding='utf-8-sig')
    print('\n' + uit['Status'].value_counts().to_string())
    print(f'\n-> {DOEL}')


if __name__ == '__main__':
    main()
