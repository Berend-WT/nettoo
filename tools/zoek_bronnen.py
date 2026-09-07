# -*- coding: utf-8 -*-
"""Netto — zoek en verifieer bronnen bij de vragen in de bank.

Draaien:  python tools/zoek_bronnen.py [aantal] [--start N]

WAAROM DIT GEEN LINKJES PLAKKEN IS
Een bron die niemand gecontroleerd heeft is slechter dan geen bron: de rij ziet
er geverifieerd uit terwijl niemand het getal heeft nagekeken. Zo zijn de foute
antwoorden er in de eerste plaats in gekomen.

Dit script haalt daarom het Wikipedia-artikel over het onderwerp op en kijkt of
ons antwoord er letterlijk in voorkomt. Zo ja, dan bewaart het de zin waarin het
staat. Dat is bewijs dat in één oogopslag na te lezen is, en het is meteen een
controle op het antwoord zelf.

STATUSSEN
  bevestigd     Het getal staat in het artikel, in een zin die ook een kernwoord
                uit de vraag bevat. Sterkste signaal.
  getal gezien  Het getal staat in het artikel, maar niet in een zin die
                herkenbaar over de vraag gaat. Even nakijken.
  afwijkend     Het artikel noemt een ander getal bij hetzelfde kernwoord. Dit
                zijn de interessantste rijen: mogelijk klopt ons antwoord niet.
  niet gevonden Geen artikel, of het getal komt er niet in voor.
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
BANK = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
DOEL = os.path.join(WORTEL, 'vragen', 'bronnen_gevonden.csv')

AGENT = 'NettoPuzzle/1.0 (https://github.com/Berend-WT/nettoo; bronverificatie)'
TALEN = ('nl', 'en')

STOP = {
    'hoeveel', 'wat', 'welk', 'welke', 'hoe', 'lang', 'hoog', 'zwaar', 'diep',
    'breed', 'groot', 'veel', 'het', 'de', 'een', 'van', 'in', 'op', 'bij',
    'met', 'aan', 'voor', 'door', 'tot', 'per', 'ongeveer', 'gemiddeld', 'jaar',
    'meter', 'kilometer', 'procent', 'telt', 'heeft', 'bevat', 'werd', 'is',
    'zijn', 'staat', 'staan', 'duurt', 'weegt', 'maakt', 'volgens', 'er', 'en',
    'of', 'als', 'die', 'dat', 'zich', 'ons', 'onze', 'naar', 'uit', 'over',
}


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
                time.sleep(3 * (poging + 1))     # rustiger aan bij rate limiting
                continue
            raise
    return {}


def kernwoorden(vraag):
    woorden = re.findall(r"[\wÀ-ſ'’-]+", vraag.lower())
    return [w for w in woorden if w not in STOP and len(w) > 3]


EIGENNAAM = re.compile(
    r"\b[A-Z][\wÀ-ſ'’-]+(?:\s+(?:[A-Z][\wÀ-ſ'’-]+|van|de|der|het|of|the))*")


def zoektermen(vraag_nl, vraag_en):
    """Zoektermen van specifiek naar breed.

    Een eerdere versie kapte de eigennaam af tot het eerste woord: "Tower" voor
    de CN Tower, "Coca" voor Coca-Cola. Daardoor kwam er een willekeurig artikel
    terug. Nu blijft de hele hoofdletterreeks staan, en levert die niets op, dan
    wordt de vraag zelf als zoekopdracht gebruikt — de zoekmachine van Wikipedia
    kan daar prima mee overweg.
    """
    uit = []
    for tekst in (str(vraag_nl), str(vraag_en or '')):
        if not tekst.strip():
            continue
        # Vanaf woord twee, zodat de hoofdletter aan het zinsbegin niet als
        # eigennaam telt.
        rest = ' '.join(tekst.split()[1:])
        for naam in sorted(EIGENNAAM.findall(rest), key=len, reverse=True):
            naam = naam.strip(' .,?')
            if len(naam) > 3:
                uit.append(naam)

    kern = kernwoorden(str(vraag_nl))
    if len(kern) >= 2:
        uit.append(' '.join(kern[:3]))
        uit.append(' '.join(kern[:2]))
    uit.append(str(vraag_nl).rstrip('?'))

    gezien, uniek = set(), []
    for t in uit:
        if t.lower() not in gezien:
            gezien.add(t.lower())
            uniek.append(t)
    return uniek[:4]


def artikel_past(titel, term, vraag):
    """Gaat dit artikel herkenbaar over de vraag?

    Zonder deze controle kwam er bij "Twaalf Olympiërs" een Belgische
    voetballer terug, en bij "Amerikaanse McDonald" een artikel over een boycot.
    """
    t = set(kernwoorden(titel))
    return bool(t & set(kernwoorden(term))) or bool(t & set(kernwoorden(vraag)))


def artikel(taal, term):
    r = api(taal, {'action': 'query', 'generator': 'search', 'gsrsearch': term,
                   'gsrlimit': '1', 'prop': 'extracts', 'explaintext': '1',
                   'exsectionformat': 'plain'})
    paginas = (r.get('query') or {}).get('pages') or []
    if not paginas:
        return None, None, None
    p = paginas[0]
    return p.get('title'), p.get('extract') or '', \
        f"https://{taal}.wikipedia.org/wiki/{urllib.parse.quote(str(p.get('title','')).replace(' ', '_'))}"


def getalvarianten(antwoord):
    """Hoe zo'n getal in lopende tekst kan staan: 21196, 21.196, 21 196."""
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
    return [z.strip() for z in re.split(r'(?<=[.!?])\s+', tekst) if z.strip()]


def beoordeel(vraag, antwoord, tekst):
    """Zoekt het antwoord in het artikel en levert de zin die het bewijst.

    Er is één kernwoord genoeg voor "bevestigd", omdat het artikel al is
    nagelopen op onderwerp door artikel_past(). Bij een drempel van twee viel
    "Het paleis heeft 775 kamers" af, want de vraag levert na het schrappen van
    stopwoorden vaak maar één bruikbaar woord op ("kamers").
    """
    varianten = getalvarianten(antwoord)
    if not varianten or not tekst:
        return 'niet gevonden', '', ''
    kern = set(kernwoorden(vraag))
    beste_zin, raak = '', False
    for z in zinnen(tekst):
        # Alleen aan de voorkant streng: een cijfer, punt, komma of koppelteken
        # ervoor betekent dat het getal deel is van iets anders ("COVID-19",
        # "1553"). Aan de achterkant moet een decimaal juist wél mee, want
        # "553.3-metre-high" is het bewijs voor antwoord 553. Een duizendtal-
        # groep erna ("12,000") telt niet mee.
        if not any(re.search(rf'(?<![\d.,\-–]){re.escape(v)}(?!\d|,\d{{3}})', z)
                   for v in varianten):
            continue
        raak = True
        overlap = len(kern & set(kernwoorden(z)))
        if overlap >= 1:
            woord = 'kernwoord komt' if overlap == 1 else 'kernwoorden komen'
            return 'bevestigd', z[:300], f'{overlap} {woord} overeen'
        if not beste_zin:
            beste_zin = z[:300]
    if raak:
        # Bij kleine getallen is een losse treffer niets waard: "12" vindt elke
        # datum, elk huisnummer. Alleen met woordoverlap is het bewijs.
        try:
            klein = abs(int(float(antwoord))) < 1000
        except (TypeError, ValueError):
            klein = True
        if klein:
            return 'niet gevonden', '', 'getal wel gezien, maar te algemeen om bewijs te zijn'
        return 'getal gezien', beste_zin, 'het getal staat er wel, maar niet in een herkenbare zin'

    # Staat er een ánder getal bij hetzelfde kernwoord? Dan is ons antwoord verdacht.
    for z in zinnen(tekst):
        if len(kern & set(kernwoorden(z))) >= 3 and re.search(r'\b\d{2,}\b', z):
            return 'afwijkend', z[:300], 'artikel noemt een ander getal bij dezelfde termen'
    return 'niet gevonden', '', ''


def main():
    aantal = int(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 10**9
    start = 0
    if '--start' in sys.argv:
        start = int(sys.argv[sys.argv.index('--start') + 1])

    d = pd.read_excel(BANK, sheet_name='Vragen').sort_values('Nr')
    d = d.iloc[start:start + aantal]

    rijen = []
    for i, (_, r) in enumerate(d.iterrows(), start=1):
        vraag = str(r['Vraag NL'])
        status, bewijs, waarom, titel, url, term = 'niet gevonden', '', '', '', '', ''
        klaar = False
        for kandidaat in zoektermen(vraag, r.get('Vraag EN (zoekhulp)')):
            for taal in TALEN:
                try:
                    t, tekst, u = artikel(taal, kandidaat)
                except Exception as e:                   # noqa: BLE001
                    print(f'    fout bij nr {int(r["Nr"])}: {e}', flush=True)
                    klaar = True
                    break
                time.sleep(0.15)
                if not t or not artikel_past(t, kandidaat, vraag):
                    continue
                s_, b_, w_ = beoordeel(vraag, r['Antwoord'], tekst)
                if s_ != 'niet gevonden' or not titel:
                    status, bewijs, waarom, titel, url, term = s_, b_, w_, t, u, kandidaat
                if s_ in ('bevestigd', 'getal gezien'):
                    klaar = True
                    break
            if klaar:
                break
        rijen.append({
            'Nr': int(r['Nr']), 'Categorie': r['Categorie'], 'Vraag NL': vraag,
            'Antwoord': r['Antwoord'], 'Status': status, 'Zoekterm': term,
            'Artikel': titel or '', 'Bron': url or '',
            'Bewijszin': bewijs, 'Toelichting': waarom,
            'Bron (bestaand)': r.get('Bron (bestaand)'),
        })
        if i % 25 == 0:
            gedaan = pd.DataFrame(rijen)
            print(f'  {i}/{len(d)} — ' + ', '.join(
                f'{k}: {v}' for k, v in gedaan['Status'].value_counts().items()), flush=True)
            gedaan.to_csv(DOEL, index=False, encoding='utf-8-sig')
        time.sleep(0.25)

    uit = pd.DataFrame(rijen)
    uit.to_csv(DOEL, index=False, encoding='utf-8-sig')
    print('\n' + uit['Status'].value_counts().to_string())
    print(f'\n-> {DOEL}')


if __name__ == '__main__':
    main()
