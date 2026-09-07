# -*- coding: utf-8 -*-
"""Netto — controleer antwoorden tegen de gestructureerde data van Wikidata.

Draaien:  python tools/verifieer_wikidata.py

WAAROM NAAST zoek_bronnen.py
zoek_bronnen.py zoekt het getal in lopende tekst. Dat werkt breed maar blijft
tekstherkenning: het kan een jaartal voor een aantal aanzien. Wikidata levert
voor een deel van de vragen een machineleesbare waarde bij een expliciete
eigenschap — de hoogte van een gebouw is P2048, de lengte van een rivier P2043.
Daar valt niets verkeerd te lezen, en dus is dit het sterkste signaal dat er is.

Het bereik is beperkt: ongeveer 230 van de 1458 vragen vragen naar zo'n
eigenschap. Voor die 230 is het antwoord hierna echt gecontroleerd.

De SPARQL-service van Wikidata lag eruit tijdens het bouwen (1 verzoek per
minuut), vandaar dat dit script de gewone MediaWiki-API gebruikt.
"""

import json
import os
import re
import ssl
import time
import urllib.parse
import urllib.request

import pandas as pd

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANK = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
DOEL = os.path.join(WORTEL, 'vragen', 'wikidata_controle.csv')

AGENT = 'NettoPuzzle/1.0 (https://github.com/Berend-WT/nettoo; antwoordcontrole)'

# Vraagpatroon -> Wikidata-eigenschap. De volgorde telt: het eerste patroon dat
# past wint, dus specifieke patronen staan boven algemene.
EIGENSCHAPPEN = [
    (r'hoeveel meter hoog is (?:de |het )?(?:mount|k2\b|berg)', 'P2044', 'hoogte boven zeeniveau'),
    (r'hoeveel meter hoog', 'P2048', 'hoogte'),
    (r'hoeveel meter breed', 'P2049', 'breedte'),
    (r'hoeveel (?:kilometer|meter) lang', 'P2043', 'lengte'),
    (r'hoeveel (?:miljoen |duizend )?inwoners', 'P1082', 'inwonertal'),
    (r'hoeveel (?:vierkante kilometer|km²)', 'P2046', 'oppervlakte'),
    (r'hoeveel afleveringen', 'P1113', 'aantal afleveringen'),
    (r'hoeveel seizoenen', 'P2437', 'aantal seizoenen'),
    (r'hoeveel (?:minuten|uur) duurt de film', 'P2047', 'speelduur'),
    (r'hoeveel (?:kilogram|kilo|ton) weegt', 'P2067', 'massa'),
    (r'diameter', 'P2386', 'diameter'),
]

def context():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


CTX = context()


def api(params, pogingen=4):
    url = 'https://www.wikidata.org/w/api.php?' + urllib.parse.urlencode(
        {**params, 'format': 'json', 'formatversion': '2'})
    req = urllib.request.Request(url, headers={'User-Agent': AGENT})
    for poging in range(pogingen):
        try:
            with urllib.request.urlopen(req, timeout=25, context=CTX) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 429 and poging < pogingen - 1:
                time.sleep(5 * (poging + 1))
                continue
            raise
        except Exception:                                # noqa: BLE001
            if poging < pogingen - 1:
                time.sleep(2)
                continue
            raise
    return {}


EIGENNAAM = re.compile(r"\b[A-Z][\wÀ-ſ'’-]+(?:\s+(?:[A-Z][\wÀ-ſ'’-]+|van|de|der|the|of))*")


def onderwerp(vraag):
    namen = EIGENNAAM.findall(' '.join(str(vraag).split()[1:]))
    return max((n.strip(' .,?') for n in namen), key=len, default='')


def entiteit(naam):
    for taal in ('nl', 'en'):
        r = api({'action': 'wbsearchentities', 'search': naam,
                 'language': taal, 'uselang': taal, 'limit': 1})
        t = r.get('search') or []
        if t:
            return t[0]['id'], t[0].get('label', '')
        time.sleep(0.2)
    return None, None


# Wikidata geeft bij elk getal een eenheid als Q-nummer. Die weggooien maakte de
# controle waardeloos: de Kanaaltunnel kwam terug als 50450 (meter) tegenover ons
# antwoord 50 (kilometer), en dat las als een afwijking van 100.000%.
NAAR_BASIS = {
    'Q11573': 1.0,        # meter
    'Q828224': 1000.0,    # kilometer
    'Q174728': 0.01,      # centimeter
    'Q3710': 0.3048,      # voet
    'Q253276': 1609.344,  # mijl
    'Q11570': 1.0,        # kilogram
    'Q11573_massa': 1.0,
    'Q191118': 1000.0,    # ton
    'Q712226': 1e6,       # vierkante kilometer
    'Q25343': 1.0,        # vierkante meter
    'Q11574': 1.0,        # seconde
    'Q7727': 60.0,        # minuut
    'Q25235': 3600.0,     # uur
}
# In welke maat ons eigen antwoord staat. Dit moet uit de vráág komen, niet uit
# de eigenschap: "Hoeveel meter lang is de Brooklyn Bridge?" en "Hoeveel
# kilometer lang is de Kanaaltunnel?" hebben allebei P2043, maar een factor
# duizend verschil. Een eerdere versie nam voor lengtes altijd kilometers aan en
# meldde daardoor 1825 tegenover 1825,4 als een afwijking van 99.875 procent.
# De volgorde telt: "vierkante kilometer" moet vóór "kilometer" worden herkend.
# De meervoud-s moet mee: \bkilometer\b matcht niet op "in kilometers", en
# daardoor werd de diameter van de aarde (12742 km) vergeleken met 12742 meter.
VRAAGEENHEID = [
    (r'vierkante kilometers?|\bkm²', 1e6),
    (r'vierkante meters?', 1.0),
    (r'\bkilometers?\b|\bkm\b', 1000.0),
    (r'\bcentimeters?\b|\bcm\b', 0.01),
    (r'\bmeters?\b', 1.0),
    (r'\bton(?:nen)?\b', 1000.0),
    (r'\bkilogram\b|\bkilo\b|\bkg\b', 1.0),
    (r'\bminuten\b', 60.0),
    (r'\buur\b', 3600.0),
    (r'\bmiljoen\b', 1e6),
    (r'\bduizend\b', 1e3),
    (r'\bmiljard\b', 1e9),
]


def vraageenheid(vraag):
    for patroon, factor in VRAAGEENHEID:
        if re.search(patroon, vraag, re.I):
            return factor
    return 1.0


def waarde(qid, prop):
    """Geeft (waarde in basiseenheid, jaartal) van de meest actuele claim.

    Voor inwonertallen staan er tientallen claims, één per volkstelling. De
    eerste pakken leverde het cijfer van 1869 voor Argentinië op. Daarom wint
    hier de claim met het recentste 'point in time' (P585).
    """
    r = api({'action': 'wbgetclaims', 'entity': qid, 'property': prop})
    claims = (r.get('claims') or {}).get(prop) or []
    beste, beste_jaar = None, -9999
    for c in claims:
        dv = c['mainsnak'].get('datavalue', {}).get('value')
        if not isinstance(dv, dict) or 'amount' not in dv:
            continue
        bedrag = float(dv['amount'].lstrip('+'))
        eenheid = str(dv.get('unit', '')).rstrip('/').split('/')[-1]
        factor = NAAR_BASIS.get(eenheid)
        if factor is None and eenheid not in ('1', ''):
            continue                                  # onbekende eenheid: overslaan
        bedrag *= (factor or 1.0)

        jaar = 0
        for q in (c.get('qualifiers') or {}).get('P585', []):
            tijd = q.get('datavalue', {}).get('value', {}).get('time', '')
            m = re.match(r'[+-](\d{4})', tijd)
            if m:
                jaar = int(m.group(1))
        if jaar >= beste_jaar:
            beste, beste_jaar = bedrag, jaar
    return beste, (beste_jaar if beste_jaar > 0 else None)


def main():
    d = pd.read_excel(BANK, sheet_name='Vragen').sort_values('Nr')
    rijen = []
    for _, r in d.iterrows():
        vraag = str(r['Vraag NL'])
        prop = label = None
        for patroon, p, l in EIGENSCHAPPEN:
            if re.search(patroon, vraag, re.I):
                prop, label = p, l
                break
        if not prop:
            continue
        naam = onderwerp(vraag)
        if len(naam) < 4:
            continue

        try:
            qid, gevonden_label = entiteit(naam)
            w, jaar = waarde(qid, prop) if qid else (None, None)
        except Exception as e:                           # noqa: BLE001
            print(f'  fout bij nr {int(r["Nr"])}: {e}', flush=True)
            continue

        # Gaat het item wel over ons onderwerp? Zonder deze controle werd
        # "de originele Britse serie The Office" vergeleken met The Office US,
        # en de provincie Utrecht met de stad Utrecht.
        past = bool(set(re.findall(r'\w{4,}', (gevonden_label or '').lower()))
                    & set(re.findall(r'\w{4,}', naam.lower())))

        ons = r['Antwoord']
        oordeel, afwijking = 'geen waarde', ''
        if w is None:
            oordeel = 'geen waarde'
        elif not past:
            oordeel = 'ander onderwerp'
        else:
            try:
                ons_basis = float(ons) * vraageenheid(vraag)
                afw = abs(w - ons_basis) / max(abs(w), 1) * 100
                afwijking = f'{afw:.1f}%'
                oordeel = 'klopt' if afw <= 3 else ('bijna' if afw <= 10 else 'WIJKT AF')
            except (TypeError, ValueError):
                oordeel = 'niet vergelijkbaar'

        rijen.append({
            'Nr': int(r['Nr']), 'Vraag NL': vraag, 'Ons antwoord': ons,
            'Eigenschap': f'{prop} ({label})', 'Onderwerp': naam,
            'Wikidata-item': gevonden_label or '', 'Wikidata-waarde': w,
            'Peiljaar': jaar or '', 'Oordeel': oordeel, 'Afwijking': afwijking,
            'Bron': f'https://www.wikidata.org/wiki/{qid}' if qid else '',
        })
        if len(rijen) % 20 == 0:
            print(f'  {len(rijen)} gecontroleerd', flush=True)
            pd.DataFrame(rijen).to_csv(DOEL, index=False, encoding='utf-8-sig')
        time.sleep(0.4)

    uit = pd.DataFrame(rijen)
    uit.to_csv(DOEL, index=False, encoding='utf-8-sig')
    print('\n' + uit['Oordeel'].value_counts().to_string())
    print(f'\n-> {DOEL}')


if __name__ == '__main__':
    main()
