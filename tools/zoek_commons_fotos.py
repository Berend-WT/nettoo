# -*- coding: utf-8 -*-
"""Netto — zoek vrij herbruikbare foto's op Wikimedia Commons bij daily-vragen.

Draaien:  python tools/zoek_commons_fotos.py [aantal]

WAAROM DIT SCRIPT BESTAAT EN NIET "EVEN GOOGLEN"
Een handmatige ronde langs Google Afbeeldingen leverde veertien links op waarvan
er twaalf auteursrechtelijk beschermd waren: de perskit van McDonald's,
omslagkunst van Amazon, burjkhalifa.ae, een webshop in kantoorartikelen. Die
mogen niet op de site. Dit script vraagt Commons rechtstreeks en gooit alles weg
wat geen CC BY, CC BY-SA, CC0 of publiek domein is, dus wat er uit komt is per
definitie bruikbaar — mét de naamsvermelding die de licentie vereist.

Vragen waarvan het antwoord van de foto af te lezen is, worden overgeslagen; dat
oordeel komt uit het blad "Fotogeschiktheid" van vragen/twijfelgevallen.xlsx.
"""

import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request

import pandas as pd

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TWIJFEL = os.path.join(WORTEL, 'vragen', 'twijfelgevallen.xlsx')
DOEL = os.path.join(WORTEL, 'fotos', 'commons_voorstellen.csv')

API = 'https://commons.wikimedia.org/w/api.php'
AGENT = 'NettoPuzzle/1.0 (https://github.com/Berend-WT/nettoo; fotokeuze)'

# Alleen deze licenties. Alles anders valt af, ook "fair use" en "no known
# copyright restrictions" — die geven geen zekerheid over hergebruik.
TOEGESTAAN = {
    'cc0', 'cc-by-1.0', 'cc-by-2.0', 'cc-by-2.5', 'cc-by-3.0', 'cc-by-4.0',
    'cc-by-sa-1.0', 'cc-by-sa-2.0', 'cc-by-sa-2.5', 'cc-by-sa-3.0', 'cc-by-sa-4.0',
    'pd', 'public domain', 'cc-pd-mark',
}


def ssl_context():
    """Certificaten uit certifi in plaats van de systeemstore.

    De Windows-store op deze machine bevat een verlopen root, waardoor elke
    HTTPS-aanroep faalt. fotos/maak_fotocatalogus.py loste dat op met
    ssl._create_unverified_context(), maar dat zet de controle volledig uit en
    dan weet je niet meer met wie je praat. certifi levert een actuele bundel,
    dus de verbinding blijft gewoon geverifieerd.
    """
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def api(params):
    params = {**params, 'format': 'json', 'formatversion': '2'}
    url = f'{API}?{urllib.parse.urlencode(params)}'
    req = urllib.request.Request(url, headers={'User-Agent': AGENT})
    with urllib.request.urlopen(req, timeout=25, context=ssl_context()) as r:
        return json.loads(r.read().decode('utf-8'))


def zoek(term, limiet=8):
    """Zoekt bestanden en geeft alleen de vrij herbruikbare terug."""
    try:
        gevonden = api({
            'action': 'query', 'generator': 'search',
            'gsrsearch': f'filetype:bitmap {term}', 'gsrnamespace': '6',
            'gsrlimit': str(limiet),
            'prop': 'imageinfo', 'iiprop': 'url|extmetadata',
            'iiurlwidth': '1200',
        })
    except Exception as e:                                   # noqa: BLE001
        # Nooit stilzwijgend als "niets gevonden" doorgeven: een netwerkfout en
        # een lege zoekopdracht zien er dan hetzelfde uit, en dan zoek je een uur
        # naar een probleem dat er niet is.
        raise SystemExit(f'API-aanroep mislukt bij "{term}": {e}') from e

    uit = []
    for p in gevonden.get('query', {}).get('pages', []):
        info = (p.get('imageinfo') or [{}])[0]
        meta = info.get('extmetadata') or {}
        licentie = (meta.get('LicenseShortName', {}).get('value') or '').strip()
        sleutel = (meta.get('License', {}).get('value') or licentie).strip().lower()
        if sleutel not in TOEGESTAAN:
            continue
        maker = (meta.get('Artist', {}).get('value') or '').strip()
        for rommel in ('<', '>'):                            # ruwe html eruit
            if rommel in maker:
                import re
                maker = re.sub(r'<[^>]+>', '', maker).strip()
        uit.append({
            'titel': p.get('title', ''),
            'bestandspagina': f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(p.get('title','').replace(' ', '_'))}",
            'afbeelding': info.get('thumburl') or info.get('url', ''),
            'licentie': licentie,
            'maker': maker[:120],
        })
    return uit, ''


# Commons is Engelstalig: een Nederlandse vraagzin levert nul resultaten. De
# werkmap heeft daarom een kolom "Vraag EN (zoekhulp)". Daaruit halen we het
# onderwerp, niet de vraag — "How many rooms does Buckingham Palace have?" moet
# "Buckingham Palace" worden.
STOPWOORDEN = {
    'how', 'many', 'much', 'what', 'is', 'the', 'in', 'which', 'year', 'was',
    'were', 'does', 'do', 'did', 'has', 'have', 'a', 'an', 'of', 'are', 'there',
    'about', 'approximately', 'long', 'high', 'tall', 'heavy', 'deep', 'wide',
    'percentage', 'percent', 'total', 'average', 'per', 'and', 'or', 'to', 'at',
    'on', 'for', 'from', 'by', 'its', 'it', 'that', 'this', 'standard', 'first',
}


def zoektermen(vraag_en, vraag_nl):
    """Levert zoektermen op van specifiek naar breed.

    Commons combineert woorden met AND, dus een lange term vindt niets:
    "Allium cepa" geeft vijf treffers, "chromosomes ordinary onion Allium" nul.
    Daarom proberen we kort na lang, tot er iets beet heeft.
    """
    tekst = str(vraag_en if isinstance(vraag_en, str) and vraag_en.strip() else vraag_nl)
    for teken in '?,()':
        tekst = tekst.replace(teken, ' ')
    woorden = tekst.split()

    kandidaten = []
    # Eigennamen wegen het zwaarst: "Buckingham Palace", "Burj Khalifa".
    eigennamen = [w for w in woorden[1:] if w[:1].isupper()]
    if len(eigennamen) >= 2:
        kandidaten.append(' '.join(eigennamen[:3]))
        kandidaten.append(' '.join(eigennamen[:2]))
    elif eigennamen:
        kandidaten.append(eigennamen[0])

    kern = [w for w in woorden if w.lower().strip('.') not in STOPWOORDEN and len(w) > 2]
    # De laatste inhoudswoorden dragen meestal het onderwerp: "...does a king
    # penguin weigh" -> "king penguin".
    for n in (3, 2):
        if len(kern) >= n:
            kandidaten.append(' '.join(kern[-n:]))
            kandidaten.append(' '.join(kern[:n]))
    if kern:
        kandidaten.append(kern[-1])

    gezien, uniek = set(), []
    for k in kandidaten:
        k = k.strip()
        if k and k.lower() not in gezien:
            gezien.add(k.lower())
            uniek.append(k)
    return uniek[:5]


def main():
    aantal = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    fotos = pd.read_excel(TWIJFEL, sheet_name='Fotogeschiktheid')
    bron = os.path.join(os.path.expanduser('~'), 'OneDrive - Driestar-Wartburg',
                        'Kopie van vragen_review_compleet.xlsx')
    if not os.path.exists(bron):
        bron = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
    engels = pd.read_excel(bron, sheet_name='Vragen')[['Nr', 'Vraag EN (zoekhulp)']]
    fotos = fotos.merge(engels, on='Nr', how='left')

    kandidaten = fotos[fotos['Foto mogelijk'] == 'ja'].sort_values('Nr').head(aantal)

    rijen, zonder = [], 0
    for i, (_, r) in enumerate(kandidaten.iterrows(), start=1):
        treffers, term = [], ''
        for kandidaat in zoektermen(r.get('Vraag EN (zoekhulp)'), r['Vraag NL']):
            term = kandidaat
            treffers, _ = zoek(kandidaat)
            if treffers:
                break
            time.sleep(0.2)
        beste = treffers[0] if treffers else None
        if not beste:
            zonder += 1
        rijen.append({
            'Nr': int(r['Nr']),
            'Vraag NL': r['Vraag NL'],
            'Zoekterm': term,
            'Commons-bestandspagina': beste['bestandspagina'] if beste else '',
            'Afbeelding': beste['afbeelding'] if beste else '',
            'Licentie': beste['licentie'] if beste else 'geen vrije treffer',
            'Maker': beste['maker'] if beste else '',
            'Alternatieven': len(treffers),
        })
        print(f"  {i:3d}/{len(kandidaten)}  nr {int(r['Nr']):4d}  "
              f"{'OK  ' + beste['licentie'] if beste else 'geen vrije treffer'}")
        time.sleep(0.35)                                     # beleefd tegen de API

    pd.DataFrame(rijen).to_csv(DOEL, index=False, encoding='utf-8-sig')
    print(f'\n{len(rijen) - zonder} van {len(rijen)} vragen kregen een vrij herbruikbare foto')
    print(f'-> {DOEL}')


if __name__ == '__main__':
    main()
