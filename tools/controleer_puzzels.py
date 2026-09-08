# -*- coding: utf-8 -*-
"""Netto — controleer de gegenereerde puzzels tegen alle gestelde voorwaarden.

Draaien:  python tools/controleer_puzzels.py

Dit script gelooft de generator niet op zijn woord maar leest de weggeschreven
bestanden en toetst ze een voor een. Het bestaat omdat de voorwaarden in stappen
zijn toegevoegd en elke ronde iets kon breken wat een eerdere ronde had
opgelost — zoals de dagpuzzels, die lang buiten de unieke set bleven en pas
opvielen toen twee gelijke iconen naast elkaar stonden.

Wat er wordt getoetst:
  som          klopt a bewerking b = c echt, en staat dat ook in calculation
  antwoord     komt het antwoord overeen met de vragenbank
  uniek        komt elke vraag hoogstens een keer voor binnen de set
  categorie    drie verschillende categorieen per puzzel
  kleur        drie verschillende kleurfamilies
  icoon        drie verschillende iconen
  fotos        hoogstens twee fotovragen per puzzel
  fotoveld     draagt een puzzel met fotovragen ook echt een foto
  bewerking    zijn de vier bewerkingen ongeveer gelijk verdeeld
  niveau       zijn de vier moeilijkheden ongeveer gelijk verdeeld
"""

import json
import os
import re
import sys
from collections import Counter

import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(WORTEL, 'data')
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')


def laad(naam):
    t = open(os.path.join(DATA, naam), encoding='utf-8').read()
    return json.loads(t[t.index('=', t.index('window.')) + 1:].strip().rstrip(';'))


def uit_js(pad, anker, eind):
    t = open(pad, encoding='utf-8').read()
    b = t[t.index(anker):]
    return b[:b.index(eind)]


def rekent(op, a, b, c):
    if op == '+':
        return a + b == c
    if op == '−':
        return a - b == c
    if op == '×':
        return a * b == c
    if op == '÷':
        return b != 0 and a == b * c
    return False


def main():
    fr = laad('netto_frontend_puzzles.js')
    rp = laad('netto_race_pool.js')
    fotos = laad('netto_fotos.js')

    families = dict(re.findall(r'--categorie-([a-z0-9-]+):\s*var\(--familie-([a-z]+)\)',
                               open(os.path.join(WORTEL, 'css', 'styles.css'),
                                    encoding='utf-8').read()))
    iconen = dict(re.findall(r"'([^']+)':\s*'([^']+)'",
                             uit_js(os.path.join(WORTEL, 'js', 'core.js'),
                                    'DAILY_CATEGORY_ICON_KEYS = Object.freeze({', '});')))

    def sleutel(c):
        return re.sub(r'^-|-$', '', re.sub(r'[^a-z0-9]+', '-', c.lower().replace('&', 'en')))

    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    bank = {}
    for _, r in d.iterrows():
        try:
            bank[str(r['Vraag NL'])] = int(r['Antwoord'])
        except (TypeError, ValueError):
            pass

    sets = [('daily + bibliotheek', fr['daily'] + fr['library']),
            ('racepool', rp)]

    alles_goed = True
    for naam, ps in sets:
        fouten = Counter()
        gezien = set()
        for p in ps:
            a, b, c = p['q1_answer'], p['q2_answer'], p['q3_answer']
            if not rekent(p['operator'], a, b, c):
                fouten['som'] += 1
            if p.get('calculation') != f"{a} {p['operator']} {b} = {c}":
                fouten['calculation'] += 1
            labels = [p[f'q{i}_label'] for i in (1, 2, 3)]
            for l, w in zip(labels, (a, b, c)):
                if l in bank and bank[l] != w:
                    fouten['antwoord'] += 1
                if l in gezien:
                    fouten['dubbele vraag'] += 1
                gezien.add(l)
            cats = p.get('categories') or []
            if len(set(cats)) < 3:
                fouten['dubbele categorie'] += 1
            if len({families.get(sleutel(x)) for x in cats}) < 3:
                fouten['dubbele kleur'] += 1
            if len({iconen.get(x, 'idea') for x in cats}) < 3:
                fouten['dubbel icoon'] += 1
            n = sum(1 for l in labels if l in fotos)
            if n > 2:
                fouten['meer dan twee fotos'] += 1
            if n and not p.get('photo'):
                fouten['fotovraag zonder foto'] += 1
            if p.get('photo') and not n:
                fouten['foto zonder fotovraag'] += 1

        ops = Counter(p['operator'] for p in ps)
        niv = Counter(p['difficulty'] for p in ps)
        met = sum(1 for p in ps if p.get('photo'))
        print(f'=== {naam}: {len(ps)} puzzels')
        print(f'    bewerking {dict(ops)}')
        print(f'    niveau    {dict(niv)}')
        print(f'    met foto  {met} ({met / len(ps):.0%})')
        if fouten:
            alles_goed = False
            for k, v in fouten.items():
                print(f'    FOUT {k}: {v}')
        else:
            print('    alle voorwaarden gehaald')
        print()

    # Delen daily en bibliotheek echt een set?
    dl = {p[f'q{i}_label'] for p in fr['daily'] for i in (1, 2, 3)}
    lb = {p[f'q{i}_label'] for p in fr['library'] for i in (1, 2, 3)}
    overlap = dl & lb
    print(f'overlap daily/bibliotheek: {len(overlap)} vragen'
          f'{" — FOUT" if overlap else " (goed, ze delen een set)"}')
    print('\nALLES IN ORDE' if alles_goed and not overlap else '\nER ZIJN FOUTEN')


if __name__ == '__main__':
    main()
