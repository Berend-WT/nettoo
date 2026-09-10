# -*- coding: utf-8 -*-
"""Netto — laat de foto op elke puzzel weer kloppen met data/netto_fotos.js.

Draaien:  python tools/herstel_puzzelfotos.py [--droog]

WAAROM DIT NODIG IS
Een puzzel draagt zijn foto zelf mee, in het veld "photo". Dat veld is gevuld op
het moment dat de puzzel werd gegenereerd, en blijft daarna staan. De fotobank
verandert wel: er komen foto's bij, en er gaan er af.

Dat ging mis bij de visuele controle. Veertig foto's zijn afgekeurd en uit
data/netto_fotos.js gehaald, maar in vijfentwintig puzzels stond diezelfde foto
nog in het photo-veld. De frontend leest dat veld eerst, dus het schaakbord bij
"hoeveel speelvelden heeft een schaakbord" stond gewoon nog in het spel — precies
de fout die de blokkeerlijst moest voorkomen, een laag dieper.

WAT DIT SCRIPT DOET
netto_fotos.js is de enige waarheid. Per puzzel:
  - staat de foto bij een vraag die daar nog in staat, dan blijven we daarbij en
    verversen we adres, licentie en maker;
  - anders nemen we de eerste vraag van de drie die er nog wel een heeft;
  - heeft geen van de drie er een, dan gaat het veld weg.

De puzzels zelf blijven ongemoeid. Alleen het photo-veld gaat mee met de bank,
zodat opnieuw genereren — en dus alle vragen door elkaar husselen — niet nodig is.
"""

import argparse
import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(WORTEL, 'data')
BESTANDEN = ('netto_frontend_puzzles.js', 'netto_race_pool.js')


def laad(naam):
    tekst = open(os.path.join(DATA, naam), encoding='utf-8').read()
    m = re.search(r'^(.*?=\s*)([\[{].*[\]}]);(\s*)$', tekst, re.S)
    if not m:
        raise SystemExit(f'{naam}: geen toewijzing gevonden')
    return m.group(1), json.loads(m.group(2)), m.group(3)


def puzzellijsten(data):
    if isinstance(data, list):
        return [data]
    return [v for v in data.values() if isinstance(v, list)]


def main():
    ontleder = argparse.ArgumentParser()
    ontleder.add_argument('--droog', action='store_true', help='alleen tellen, niets schrijven')
    args = ontleder.parse_args()

    tekst = open(os.path.join(DATA, 'netto_fotos.js'), encoding='utf-8').read()
    fotos = json.loads(tekst[tekst.index('{'):tekst.rindex('}') + 1])
    print(f'{len(fotos)} foto\'s in de bank')

    for naam in BESTANDEN:
        kop, data, staart = laad(naam)
        telling = {'ongewijzigd': 0, 'ververst': 0, 'verplaatst': 0, 'weggehaald': 0,
                   'toegevoegd': 0}
        for lijst in puzzellijsten(data):
            for p in lijst:
                if not isinstance(p, dict) or 'q1_label' not in p:
                    continue
                bij = [(i, fotos[p[f'q{i}_label']]) for i in (1, 2, 3)
                       if p.get(f'q{i}_label') in fotos]
                huidig = p.get('photo')
                nr = huidig.get('vraag') if isinstance(huidig, dict) else None
                keuze = next((k for k in bij if k[0] == nr), None) or (bij[0] if bij else None)

                if not keuze:
                    if huidig:
                        p.pop('photo')
                        telling['weggehaald'] += 1
                    continue
                i, f = keuze
                nieuw = {'url': f['url'], 'pagina': f['pagina'],
                         'licentie': f['licentie'], 'maker': f['maker'], 'vraag': i}
                if not huidig:
                    telling['toegevoegd'] += 1
                elif nr != i:
                    telling['verplaatst'] += 1
                elif nieuw != huidig:
                    telling['ververst'] += 1
                else:
                    telling['ongewijzigd'] += 1
                p['photo'] = nieuw

        print(f'\n{naam}')
        for k, v in telling.items():
            print(f'  {k:14s} {v}')
        if not args.droog:
            with open(os.path.join(DATA, naam), 'w', encoding='utf-8') as f:
                f.write(kop + json.dumps(data, ensure_ascii=False) + ';' + staart)

    if args.droog:
        print('\ndroge run: niets geschreven')
    else:
        print('\nDraai nu: python tools/sync_website.py')


if __name__ == '__main__':
    main()
