# -*- coding: utf-8 -*-
"""Netto — bronnen voor de reservevragen: dode links en vragen zonder bron.

Draaien:  python tools/bronnen_reserve.py [aantal]

WAAROM DIT ANDERS WERKT DAN DE VORIGE RONDES
Die zochten het antwoord letterlijk in de tekst en gaven op als het er niet
stond. Voor een groot deel van deze vragen kan dat principieel niet. Het
Wikipedia-artikel over Argentinië noemt nergens het getal vijf; het somt de vijf
buurlanden op. Bij "Hoeveel landen grenzen aan X?" is het artikel wel degelijk de
juiste bron, alleen moet een mens natellen.

Daarom levert dit script twee soorten uitkomst, en houdt het die streng
gescheiden:

  bevestigd     Het getal staat in de bron, bij dezelfde soort maat als de vraag.
                Even nalezen en klaar.
  natellen      Het artikel gaat aantoonbaar over het onderwerp, maar noemt het
                getal niet als getal. De bron deugt; de telling moet met de hand.

Wat géén van beide oplevert, krijgt niets. Een bron die noch het getal noemt
noch over het onderwerp gaat, is geen bron.

De artikelkeuze is strenger dan in ronde drie. Die accepteerde een artikel zodra
één woord overeenkwam, waardoor de witte neushoorn bij de witte dolfijn uitkwam
en de nijlkrokodil bij de Nijl. Nu moet de titel een eigennaam uit de vraag
bevatten, of minstens twee onderwerpwoorden delen.
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
DOEL = os.path.join(WORTEL, 'vragen', 'bronnen_reserve.csv')

AGENT = 'NettoPuzzle/1.0 (https://github.com/Berend-WT/nettoo; bronverificatie)'

STOP = {
    'hoeveel', 'wat', 'welk', 'welke', 'hoe', 'veel', 'het', 'de', 'een', 'van',
    'in', 'op', 'bij', 'met', 'aan', 'voor', 'door', 'tot', 'per', 'ongeveer',
    'telt', 'heeft', 'bevat', 'werd', 'zijn', 'staat', 'staan', 'duurt', 'weegt',
    'maakt', 'volgens', 'er', 'en', 'of', 'als', 'die', 'dat', 'zich', 'ons',
    'naar', 'uit', 'over', 'wordt', 'worden', 'kan', 'iedere', 'elke', 'lang',
    'hoog', 'zwaar', 'diep', 'breed', 'groot', 'klein', 'standaard', 'gemiddeld',
    'totaal', 'samen', 'ooit', 'volwassen', 'klassieke', 'klassiek', 'moderne',
    'officiele', 'officiële', 'wereldwijd', 'jaarlijks',
}

BEGRIPPEN = {
    'lengte': r'meter|meters|metre|metres|kilometer|kilometre|kilometers|km',
    'kort': r'centimeter|centimetre|centimeters|inch|inches',
    'massa': r'kilogram|kilograms|kilo|kg|gram|grams|ton|tonne|tonnes|pound|pounds',
    'volume': r'liter|litre|liters|litres',
    'deel': r'percent|per cent|procent|percentage',
    'hoek': r'degrees|graden',
    'tijd': r'year|years|jaar|jaren|day|days|dagen|hour|hours|uur|minute|minutes|'
            r'minuten|second|seconds|seconden|maanden|months',
    'werk': r'episodes|afleveringen|seasons|seizoenen|chapters|hoofdstukken|books|'
            r'boeken|volumes|delen|albums|films|movies|woorden|words',
    'bouw': r'rooms|kamers|floors|storeys|stories|verdiepingen|steps|stairs|treden|'
            r'elevators|liften|towers|torens|columns|zuilen|arches|bogen|locks|sluizen',
    'soort': r'species|soorten',
    'gebied': r'countries|nations|landen|islands|eilanden|states|staten|provinces|'
              r'provincies|regions|territories|territoria|timezones|tijdzones',
    'mensen': r'people|inhabitants|population|inwoners|bevolking|visitors|bezoekers',
    'lichaam': r'bones|botten|teeth|tanden|ribs|ribben|muscles|spieren|hearts',
    'sport': r'players|spelers|members|leden|seats|zetels|teams|points|punten',
    'schaal': r'billion|miljard|million|miljoen|thousand|duizend|biljoen|trillion',
    'muziek': r'strings|snaren|keys|toetsen|notes|noten',
    'voertuig': r'wheels|wielen|engines|motoren|wagons',
    'dier': r'legs|poten|wings|vleugels|eyes|ogen|humps|bulten|stomachs|magen',
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


def maten(tekst):
    uit = set()
    for _, p in BEGRIP_PATRONEN:
        uit.update(m.group(0).lower() for m in p.finditer(str(tekst)))
    return uit


def onderwerpwoorden(tekst):
    weg = maten(tekst)
    return [w for w in woorden(tekst) if w not in weg]


def begrippen(tekst):
    return {n for n, p in BEGRIP_PATRONEN if p.search(str(tekst))}


def eigennamen(vraag_nl, vraag_en):
    uit = []
    for tekst in (str(vraag_nl), str(vraag_en or '')):
        if not tekst.strip():
            continue
        for naam in sorted(EIGENNAAM.findall(' '.join(tekst.split()[1:])),
                           key=len, reverse=True):
            naam = naam.strip(' .,?()')
            if len(naam) > 3:
                uit.append(naam)
    return uit


def zoektermen(vraag_nl, vraag_en):
    uit = list(eigennamen(vraag_nl, vraag_en))
    for tekst in (vraag_nl, vraag_en):
        k = onderwerpwoorden(tekst)
        if len(k) >= 2:
            uit.append(' '.join(k[:3]))
            uit.append(' '.join(k[:2]))
        elif k:
            uit.append(k[0])
    gezien, uniek = set(), []
    for t in uit:
        if t and t.lower() not in gezien:
            gezien.add(t.lower())
            uniek.append(t)
    return uniek[:4]


def artikel_past(titel, vraag_nl, vraag_en):
    """Strenger dan ronde drie, die op één woord al akkoord ging.

    Een titel telt als passend wanneer hij een eigennaam uit de vraag bevat, of
    minstens twee onderwerpwoorden met de vraag deelt. Op één gedeeld woord kwam
    "witte neushoorn" uit bij "witte dolfijn".
    """
    t = titel.lower()
    for naam in eigennamen(vraag_nl, vraag_en):
        if naam.lower() in t or t in naam.lower():
            return True
    return len(set(onderwerpwoorden(titel)) & set(onderwerpwoorden(vraag_nl))) >= 2


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
    uit = [z.strip() for z in re.split(r'(?<=[.!?])\s+', str(tekst)) if z.strip()]
    for regel in str(wikitekst).splitlines():
        regel = regel.strip()
        if regel.startswith('|') and '=' in regel and len(regel) < 300:
            uit.append(' '.join(re.sub(r'<[^>]+>|\[\[|\]\]', ' ', regel).split()))
    return [f for f in uit if len(f) < 400]


def bewijs(vraag, antwoord, tekst, wikitekst):
    vs = varianten(antwoord)
    if not vs:
        return None
    gevraagd = begrippen(vraag)
    for f in fragmenten(tekst, wikitekst):
        if not any(re.search(rf'(?<![\d.,\-–]){re.escape(v)}(?!\d|,\d{{3}})', f)
                   for v in vs):
            continue
        if gevraagd & begrippen(f) or not gevraagd:
            return f[:320]
    return None


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
    ver = d['Bron (geverifieerd)'].notna()
    oud = d['Bron (bestaand)'].notna()
    st = d['Status oude bron'].astype(str)
    open_vragen = d[~ver & (~oud | st.eq('DODE LINK'))].head(aantal)
    print(f'{len(open_vragen)} vragen zonder bruikbare bron\n', flush=True)

    rijen = []
    for i, (_, r) in enumerate(open_vragen.iterrows(), start=1):
        vraag = str(r['Vraag NL'])
        en = r.get('Vraag EN (zoekhulp)')
        beste = None
        for term in zoektermen(vraag, en):
            for taal in ('nl', 'en'):
                try:
                    titel, tekst, wt, url = haal(taal, term)
                except Exception:                        # noqa: BLE001
                    continue
                time.sleep(0.15)
                if not titel or not artikel_past(titel, vraag, en):
                    continue
                zin = bewijs(vraag, r['Antwoord'], tekst, wt)
                if zin:
                    beste = (titel, url, 'bevestigd', zin)
                    break
                if beste is None:
                    beste = (titel, url, 'natellen',
                             'Artikel gaat over het onderwerp maar noemt het getal niet '
                             'als getal; zelf natellen.')
            if beste and beste[2] == 'bevestigd':
                break

        if beste:
            titel, url, soort, zin = beste
            rijen.append({'Nr': int(r['Nr']), 'Uitkomst': soort, 'In gebruik': r['In gebruik'],
                          'Vraag NL': vraag, 'Antwoord': r['Antwoord'], 'Bron': url,
                          'Artikel': titel, 'Bewijs': zin})
        else:
            rijen.append({'Nr': int(r['Nr']), 'Uitkomst': 'geen bron', 'In gebruik': r['In gebruik'],
                          'Vraag NL': vraag, 'Antwoord': r['Antwoord'], 'Bron': '',
                          'Artikel': '', 'Bewijs': ''})

        if i % 10 == 0:
            uit = pd.DataFrame(rijen)
            print(f'  {i}/{len(open_vragen)} — '
                  + ', '.join(f'{k}: {v}' for k, v in uit['Uitkomst'].value_counts().items()),
                  flush=True)
            try:
                uit.to_csv(DOEL, index=False, encoding='utf-8-sig')
            except PermissionError:
                pass
        time.sleep(0.2)

    uit = pd.DataFrame(rijen)
    uit.to_csv(DOEL, index=False, encoding='utf-8-sig')
    print('\n' + uit['Uitkomst'].value_counts().to_string())
    print(f'\n-> {DOEL}')


if __name__ == '__main__':
    main()
