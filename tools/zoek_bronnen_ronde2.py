# -*- coding: utf-8 -*-
"""Netto — tweede ronde bronnen, voor de vragen die ronde één niet vond.

Draaien:  python tools/zoek_bronnen_ronde2.py

WAT ER IN RONDE ÉÉN MISGING
Die ronde eiste dat de bewijszin een kernwoord uit de vraag bevatte. Dat is de
verkeerde eis: een artikel over de Euromast zegt "Met 185 meter is het een van
de hoogste..." en herhaalt het woord Euromast niet, want het hele artikel gaat
daar al over. Zo werd goed bewijs weggegooid.

De juiste eis is het MAATWOORD, niet het onderwerp. Het onderwerp is al
vastgesteld doordat het artikel erover gaat; wat de zin moet aantonen is dat het
getal bij het gevraagde hoort. "185 meter" bij een vraag om meters, "52 witte
toetsen" bij een vraag om toetsen, "236 afleveringen" bij een vraag om
afleveringen.

Daarnaast zoekt deze ronde breder: als het artikel over het onderwerp niets
oplevert, wordt Wikipedia doorzocht op onderwerp + antwoord samen. Zo komen
lijstartikelen in beeld ("Lijst van hoogste wolkenkrabbers") die het getal wel
noemen.
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
DOEL = os.path.join(WORTEL, 'vragen', 'bronnen_ronde2.csv')

AGENT = 'NettoPuzzle/1.0 (https://github.com/Berend-WT/nettoo; bronverificatie)'

# Woorden die geen onderwerp aanduiden. Let op: maatwoorden staan hier NIET in,
# want juist die moeten in de bewijszin terugkomen.
STOP = {
    'hoeveel', 'wat', 'welk', 'welke', 'hoe', 'veel', 'het', 'de', 'een', 'van',
    'in', 'op', 'bij', 'met', 'aan', 'voor', 'door', 'tot', 'per', 'ongeveer',
    'telt', 'heeft', 'bevat', 'werd', 'zijn', 'staat', 'staan', 'duurt',
    'weegt', 'maakt', 'volgens', 'er', 'en', 'of', 'als', 'die', 'dat', 'zich',
    'ons', 'onze', 'naar', 'uit', 'over', 'wordt', 'worden', 'kan', 'kun',
    'iedere', 'elke', 'standaard', 'gemiddeld', 'totaal', 'samen', 'ooit',
}

# Het zelfstandig naamwoord dat geteld of gemeten wordt. Dit moet in de
# bewijszin staan, samen met het getal.
MAATWOORD = re.compile(
    r'\b(meter|meters|kilometer|centimeter|millimeter|kilo|kilogram|gram|ton|'
    r'liter|hectare|graden|procent|jaar|jaren|dagen|dag|uur|uren|minuten|'
    r'seconden|toetsen|kamers|afleveringen|seizoenen|delen|boeken|hoofdstukken|'
    r'verdiepingen|treden|liften|torens|zuilen|snaren|poten|vleugels|ogen|'
    r'tanden|botten|spelers|leden|zetels|landen|eilanden|inwoners|soorten|'
    r'talen|letters|planeten|manen|ringen|wielen|motoren|stations|lijnen|'
    r'bruggen|sluizen|piramides|schepen|soldaten|punten|kaarten|stenen|'
    r'kilocalorieen|calorieen|episodes|floors|rooms|steps|elevators|storeys|'
    r'stories|feet|metres|meters|seasons|episodes|players|members|seats)\b',
    re.I)


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
        except urllib.error.HTTPError as e:
            if e.code == 429 and poging < pogingen - 1:
                time.sleep(3 * (poging + 1))
                continue
            raise
        except Exception:                                # noqa: BLE001
            if poging < pogingen - 1:
                time.sleep(2)
                continue
            raise
    return {}


def woorden(tekst):
    return [w for w in re.findall(r"[\wÀ-ſ'’-]+", str(tekst).lower())
            if w not in STOP and len(w) > 3]


EIGENNAAM = re.compile(r"\b[A-Z][\wÀ-ſ'’-]+(?:\s+(?:[A-Z][\wÀ-ſ'’-]+|van|de|der|the|of))*")


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
        k = woorden(tekst)
        if len(k) >= 2:
            uit.append(' '.join(k[:3]))
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
        uit.add('{:,}'.format(abs(n)).replace(',', '.'))
        uit.add('{:,}'.format(abs(n)).replace(',', ' '))
        uit.add('{:,}'.format(abs(n)))
    return sorted(uit, key=len, reverse=True)


def zinnen(tekst):
    return [z.strip() for z in re.split(r'(?<=[.!?])\s+', str(tekst)) if z.strip()]


def bewijs(vraag, antwoord, tekst):
    """Zoekt een zin met het getal én het gevraagde maatwoord.

    Het onderwerp hoeft niet in de zin te staan: het artikel gaat er al over.
    Wat de zin moet aantonen is dat het getal hoort bij wat er gevraagd wordt.
    """
    vs = varianten(antwoord)
    if not vs or not tekst:
        return None, None
    gevraagd = {m.group(0).lower() for m in MAATWOORD.finditer(vraag)}
    onderwerp = set(woorden(vraag))
    zwak = None
    for z in zinnen(tekst):
        if not any(re.search(rf'(?<![\d.,\-–]){re.escape(v)}(?!\d|,\d{{3}})', z)
                   for v in vs):
            continue
        zin_maten = {m.group(0).lower() for m in MAATWOORD.finditer(z)}
        if gevraagd & zin_maten:
            return z[:320], 'getal staat bij het gevraagde maatwoord'
        if onderwerp & set(woorden(z)):
            return z[:320], 'getal staat in een zin over het onderwerp'
        if zwak is None:
            zwak = z[:320]
    return (zwak, 'getal komt voor, maar zonder maatwoord') if zwak else (None, None)


def artikel_past(titel, term, vraag):
    """Gaat dit artikel herkenbaar over de vraag?

    Ronde één had deze controle wel en ronde twee niet, met als gevolg dat de
    vraag "Hoeveel landen zijn lid van de G20?" het artikel Holocaust opleverde.
    Zonder deze zeef is een treffer waardeloos, hoe overtuigend de zin ook oogt.
    """
    t = set(woorden(titel))
    return bool(t & set(woorden(term))) or bool(t & set(woorden(vraag)))


def haal_artikel(taal, term):
    """Haalt zowel de lopende tekst als de wikitekst op.

    prop=extracts levert alleen proza en laat de infobox weg — en juist daar
    staan de maten. De breedte van de Mona Lisa (53 cm) komt in de lopende tekst
    niet voor, maar staat in de wikitekst als "| breedte = 53". Zonder die
    tweede bron miste ronde één honderden vragen.
    """
    r = api(taal, {'action': 'query', 'generator': 'search', 'gsrsearch': term,
                   'gsrlimit': '1', 'prop': 'extracts|revisions',
                   'explaintext': '1', 'rvprop': 'content', 'rvslots': 'main'})
    p = ((r.get('query') or {}).get('pages') or [None])[0]
    if not p:
        return None, '', '', ''
    wikitekst = ''
    try:
        wikitekst = p['revisions'][0]['slots']['main'].get('content', '')
    except (KeyError, IndexError, TypeError):
        pass
    url = (f'https://{taal}.wikipedia.org/wiki/'
           + urllib.parse.quote(str(p.get('title', '')).replace(' ', '_')))
    return p.get('title'), p.get('extract') or '', wikitekst, url


# Infobox-parameter -> waar in de vraag naar gevraagd wordt. De parameternaam
# is zelf het maatwoord: "| breedte = 53" bewijst een vraag om de breedte.
INFOBOX = [
    (r'hoogte|height|elevation', r'\bhoog\b|\bhoogte\b|\bhoogste\b'),
    (r'breedte|width', r'\bbreed\b|\bbreedte\b'),
    (r'lengte|length', r'\blang\b|\blengte\b'),
    (r'gewicht|massa|weight|mass', r'\bweegt\b|\bgewicht\b|\bmassa\b'),
    (r'diepte|depth', r'\bdiep\b|\bdiepte\b'),
    (r'oppervlakte|area', r'vierkante|oppervlakte|\bkm²'),
    (r'inwoners|population|bevolking', r'inwoners|bevolking'),
    (r'verdiepingen|floors|floor_count', r'verdiepingen'),
    (r'afleveringen|episodes|num_episodes', r'afleveringen'),
    (r'seizoenen|seasons|num_seasons', r'seizoenen'),
    (r'speelduur|runtime|duur', r'\bduurt\b|speelduur'),
    (r'bouwjaar|opgericht|founded|established', r'in welk jaar'),
]


def infobox_bewijs(vraag, antwoord, wikitekst):
    """Zoekt een infoboxregel waarvan de parameternaam bij de vraag past."""
    vs = varianten(antwoord)
    if not vs or not wikitekst:
        return None, None
    for regel in wikitekst.splitlines():
        regel = regel.strip()
        if not regel.startswith('|') or '=' not in regel:
            continue
        naam, _, waarde = regel[1:].partition('=')
        if not any(re.search(rf'(?<![\d.,\-–]){re.escape(v)}(?!\d|,\d{{3}})', waarde)
                   for v in vs):
            continue
        for param, vraagpatroon in INFOBOX:
            if re.search(param, naam, re.I) and re.search(vraagpatroon, vraag, re.I):
                schoon = re.sub(r'<[^>]+>|\[\[|\]\]|\{\{|\}\}', ' ', regel)
                return ' '.join(schoon.split())[:320], \
                    f'infobox-veld "{naam.strip()}" bevat het antwoord'
    return None, None


def main():
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    open_vragen = d[d['Bron (bestaand)'].isna() & d['Bron (geverifieerd)'].isna()]
    print(f'{len(open_vragen)} vragen zonder enige bron\n', flush=True)

    rijen = []
    for i, (_, r) in enumerate(open_vragen.iterrows(), start=1):
        vraag = str(r['Vraag NL'])
        antwoord = r['Antwoord']
        gevonden = None

        kandidaten = zoektermen(vraag, r.get('Vraag EN (zoekhulp)'))
        # Ronde A: het artikel over het onderwerp — eerst de infobox, dan de
        # lopende tekst. De infobox is betrouwbaarder: daar staat een maat bij
        # een veldnaam in plaats van los in een zin.
        for term in kandidaten:
            for taal in ('nl', 'en'):
                titel, tekst, wikitekst, url = haal_artikel(taal, term)
                time.sleep(0.15)
                if not titel or not artikel_past(titel, term, vraag):
                    continue
                zin, waarom = infobox_bewijs(vraag, antwoord, wikitekst)
                if not zin:
                    zin, waarom = bewijs(vraag, antwoord, tekst)
                if zin and waarom != 'getal komt voor, maar zonder maatwoord':
                    gevonden = (titel, url, zin, waarom, f'artikel: {term}')
                    break
            if gevonden:
                break

        # Ronde B: doorzoek Wikipedia op onderwerp + antwoord samen, zodat ook
        # lijstartikelen in beeld komen.
        if not gevonden and kandidaten:
            for taal in ('nl', 'en'):
                term = f'{kandidaten[0]} {antwoord}'
                titel, tekst, wikitekst, url = haal_artikel(taal, term)
                time.sleep(0.15)
                if not titel or not artikel_past(titel, kandidaten[0], vraag):
                    continue
                zin, waarom = infobox_bewijs(vraag, antwoord, wikitekst)
                if not zin:
                    zin, waarom = bewijs(vraag, antwoord, tekst)
                if zin and waarom != 'getal komt voor, maar zonder maatwoord':
                    gevonden = (titel, url, zin, waarom, f'zoekopdracht: {term}')
                    break

        if gevonden:
            titel, url, zin, waarom, hoe = gevonden
            rijen.append({'Nr': int(r['Nr']), 'Status': 'bevestigd',
                          'Vraag NL': vraag, 'Antwoord': antwoord,
                          'Bron': url, 'Artikel': titel, 'Bewijszin': zin,
                          'Toelichting': waarom, 'Gevonden via': hoe})
        else:
            rijen.append({'Nr': int(r['Nr']), 'Status': 'niet gevonden',
                          'Vraag NL': vraag, 'Antwoord': antwoord,
                          'Bron': '', 'Artikel': '', 'Bewijszin': '',
                          'Toelichting': '', 'Gevonden via': ''})

        if i % 25 == 0:
            uit = pd.DataFrame(rijen)
            print(f'  {i}/{len(open_vragen)} — '
                  + ', '.join(f'{k}: {v}' for k, v in uit['Status'].value_counts().items()),
                  flush=True)
            uit.to_csv(DOEL, index=False, encoding='utf-8-sig')
        time.sleep(0.2)

    uit = pd.DataFrame(rijen)
    uit.to_csv(DOEL, index=False, encoding='utf-8-sig')
    print('\n' + uit['Status'].value_counts().to_string())
    print(f'\n-> {DOEL}')


if __name__ == '__main__':
    main()
