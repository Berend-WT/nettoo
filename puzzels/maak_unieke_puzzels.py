# -*- coding: utf-8 -*-
"""Netto — bouw puzzelsets waarin elke vraag hoogstens een keer voorkomt.

Draaien:
    python puzzels/maak_unieke_puzzels.py --doel puzzels
    python puzzels/maak_unieke_puzzels.py --doel race

DE HARDE EIS
Binnen een set komt elke vraag precies een keer voor, of helemaal niet. Met
1409 vragen en drie vragen per puzzel ligt het plafond dus op 469 puzzels per
set. Dat is geen keuze van dit script maar rekenkunde.

"Puzzels" en "Daily Archive" delen een set: wat je in de bibliotheek tegenkomt
verschijnt niet nog eens in een dagpuzzel. Race krijgt een eigen set, apart
gegenereerd, zodat een vraag daar opnieuw gebruikt mag worden — de speler
ervaart die modi als losse dingen. Binnen een race blijft elke vraag uniek.

WAAROM NIET GEWOON GRETIG PAKKEN
Wie steeds de eerst passende combinatie neemt, houdt aan het eind vragen over
die nergens meer in passen: alle partners zijn dan al opgebruikt. Daarom kiest
dit script telkens de vraag met de mínste overgebleven mogelijkheden. Dat is de
gebruikelijke manier om stranden te voorkomen en levert in de praktijk enkele
tientallen puzzels meer op.

MOEILIJKHEID
De score telt drie dingen op:
  - de bewerking      optellen is makkelijker dan delen
  - de grootte        grote getallen zijn lastiger te schatten (logaritmisch,
                      want van 10 naar 100 scheelt meer dan van 1000 naar 1090)
  - de rondheid       1000 schat je makkelijker dan 1037, dus elke nul aan het
                      eind maakt een getal makkelijker

De grenzen tussen de vier niveaus worden niet vast gekozen maar afgeleid uit de
verdeling van alle gevonden combinaties. Daardoor komt er per niveau ongeveer
evenveel uit, wat de eis was. De makkelijkste tien procent valt af, zodat de set
niet volloopt met sommen als 2 + 2 = 4.
"""

import argparse
import json
import math
import os
import random
import sys
from collections import Counter, defaultdict

import pandas as pd

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
DATA = os.path.join(WORTEL, 'data')
SPIEGEL = os.path.join(WORTEL, 'website', 'data')

OPERATORS = ('+', '−', '×', '÷')
OPERATOR_GEWICHT = {'+': 0.0, '−': 8.0, '×': 14.0, '÷': 18.0}
NIVEAUS = ('easy', 'intermediate', 'hard', 'extremely-hard')


def rondheid(n):
    """Aantal nullen aan het eind, tot maximaal drie.

    1000 telt als drie, 250 als een, 1037 als nul. Ronde getallen zijn
    makkelijker te schatten en verlagen daarom de score.
    """
    if n == 0:
        return 0
    t = 0
    while n % 10 == 0 and t < 3:
        n //= 10
        t += 1
    return t


def score_van(operator, antwoorden):
    grootte = sum(math.log10(abs(a) + 1.0) * 10.0 for a in antwoorden)
    rond = sum(rondheid(a) * 4.0 for a in antwoorden)
    return round(OPERATOR_GEWICHT[operator] + grootte - rond, 2)


def lees_vragen():
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    vragen = []
    for _, r in d.iterrows():
        try:
            a = int(r['Antwoord'])
        except (TypeError, ValueError):
            continue
        # Nul en een leveren lege sommen op: b x 1 = b laat niets te rekenen
        # over. Ze blijven wel in de bank, maar niet als puzzelvraag.
        if a < 2:
            continue
        vragen.append({'nr': int(r['Nr']), 'antwoord': a,
                       'categorie': str(r['Categorie']),
                       'tekst': str(r['Vraag NL'])})
    return vragen


def waardedrietallen(waarden):
    """Alle (operator, a, b, c) op waardeniveau, met a op b = c."""
    vs = set(waarden)
    uit = []
    for a in waarden:
        for b in waarden:
            if a + b in vs:
                uit.append(('+', a, b, a + b))
            if a > b and a - b in vs:
                uit.append(('−', a, b, a - b))
            if a * b in vs:
                uit.append(('×', a, b, a * b))
            if b and a % b == 0 and a // b in vs:
                uit.append(('÷', a, b, a // b))
    return uit


def bouw(vragen, doel_aantal, seed, quota=10**9):
    rng = random.Random(seed)
    per_waarde = defaultdict(list)
    for i, q in enumerate(vragen):
        per_waarde[q['antwoord']].append(i)
    waarden = sorted(per_waarde)

    drietallen = waardedrietallen(waarden)
    scores = sorted(score_van(op, (a, b, c)) for op, a, b, c in drietallen)
    # De makkelijkste drie procent valt af. Dat is gemeten: bij tien procent
    # kost de ondergrens bijna honderd puzzels, bij drie procent nog maar
    # veertig, terwijl het echte afval — 2 + 3 = 5 — er wel buiten blijft. De
    # makkelijkste som die zo binnenkomt is 2 x 15 = 30, en dat is nog een som.
    ondergrens = scores[int(len(scores) * 0.03)]
    grenzen = [scores[int(len(scores) * f)] for f in (0.325, 0.55, 0.775)]

    def niveau_van(s):
        if s < grenzen[0]:
            return 'easy'
        if s < grenzen[1]:
            return 'intermediate'
        if s < grenzen[2]:
            return 'hard'
        return 'extremely-hard'

    # Per vakje (bewerking x niveau) de bruikbare drietallen verzamelen.
    vakjes = {(op, n): [] for op in OPERATORS for n in NIVEAUS}
    for op, a, b, c in drietallen:
        s = score_van(op, (a, b, c))
        if s < ondergrens:
            continue
        vakjes[(op, niveau_van(s))].append((a, b, c, s))
    vrij = {i for i in range(len(vragen))}
    beschikbaar = {w: len(per_waarde[w]) for w in waarden}

    # Schaarste eerst. Van de 493 antwoordwaarden worden er 334 door maar een
    # vraag gedekt; zo'n waarde verdwijnt zodra die ene vraag elders belandt.
    # Door drietallen met een schaarse waarde vooraan te zetten worden ze
    # gebruikt terwijl hun partners nog bestaan. Dat scheelde bij het uitproberen
    # ruim twintig puzzels ten opzichte van een willekeurige volgorde, en gaf
    # bovendien de gelijkmatigste verdeling over de vier niveaus.
    for lijst in vakjes.values():
        rng.shuffle(lijst)
        lijst.sort(key=lambda t: -min(beschikbaar[t[0]], beschikbaar[t[1]],
                                      beschikbaar[t[2]]))

    def kies(waarde, verboden_cats, gebruikt):
        """Pak een vrije vraag met deze waarde en een nog ongebruikte categorie.

        De categorie-eis is hard: drie vragen uit dezelfde puzzel horen uit drie
        verschillende categorieen te komen. Bij het uitproberen bleek dat maar
        zes puzzels te kosten, tegenover eenenveertig puzzels die anders een
        dubbele categorie kregen. Die ruil is de moeite waard, dus valt een
        drietal af zodra een van de drie waarden geen verse categorie meer heeft.
        """
        opties = [i for i in per_waarde[waarde]
                  if i in vrij and i not in gebruikt
                  and vragen[i]['categorie'] not in verboden_cats]
        return opties[0] if opties else None

    puzzels = []
    volgorde = [(op, n) for n in NIVEAUS for op in OPERATORS]
    leeg = set()
    per_niveau = Counter()
    while len(puzzels) < doel_aantal and len(leeg) < len(volgorde):
        for cel in volgorde:
            if len(puzzels) >= doel_aantal:
                break
            # Een vol niveau telt als leeg. Zonder dat blijft de buitenste lus
            # doordraaien zolang er ergens nog een vakje open is, en wordt een
            # vol vakje elke ronde opnieuw doorzocht. Bij een plafond van 85 zit
            # easy al vroeg vol en liep het script daar eindeloos langs; de
            # eerste poging draaide daardoor twintig minuten zonder resultaat.
            if per_niveau[cel[1]] >= quota:
                leeg.add(cel)
            if cel in leeg:
                continue
            gevonden = None
            lijst = vakjes[cel]
            for idx in range(len(lijst) - 1, -1, -1):
                a, b, c, s = lijst[idx]
                if min(beschikbaar[a], beschikbaar[b], beschikbaar[c]) < 1:
                    lijst.pop(idx)
                    continue
                gebruikt, cats, keuze = set(), set(), []
                for w in (a, b, c):
                    i = kies(w, cats, gebruikt)
                    if i is None:
                        keuze = None
                        break
                    gebruikt.add(i)
                    cats.add(vragen[i]['categorie'])
                    keuze.append(i)
                if keuze is None:
                    lijst.pop(idx)
                    continue
                gevonden = (keuze, a, b, c, s)
                lijst.pop(idx)
                break
            if gevonden is None:
                leeg.add(cel)
                continue
            keuze, a, b, c, s = gevonden
            per_niveau[cel[1]] += 1
            for i in keuze:
                vrij.discard(i)
                beschikbaar[vragen[i]['antwoord']] -= 1
            puzzels.append({'op': cel[0], 'niveau': cel[1], 'score': s,
                            'vragen': [vragen[i] for i in keuze],
                            'waarden': (a, b, c)})
    return puzzels, grenzen, ondergrens


def als_puzzel(p, nr, prefix):
    q1, q2, q3 = p['vragen']
    a, b, c = p['waarden']
    return {
        'id': f'{prefix}-{nr:03d}', 'number': nr, 'name': f'Puzzel #{nr}',
        'operator': p['op'],
        'q1_label': q1['tekst'], 'q1_answer': a,
        'q2_label': q2['tekst'], 'q2_answer': b,
        'q3_label': q3['tekst'], 'q3_answer': c,
        'calculation': f"{a} {p['op']} {b} = {c}",
        'categories': [q1['categorie'], q2['categorie'], q3['categorie']],
        'difficulty': p['niveau'], 'difficulty_score': p['score'],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--doel', choices=['puzzels', 'race'], default='puzzels')
    ap.add_argument('--aantal', type=int, default=469)
    ap.add_argument('--seed', type=int, default=None)
    ap.add_argument('--quota', type=int, default=85,
                    help='hoogstens zoveel puzzels per moeilijkheidsniveau')
    ap.add_argument('--schrijf', action='store_true')
    args = ap.parse_args()

    seed = args.seed if args.seed is not None else (7 if args.doel == 'puzzels' else 91)
    vragen = lees_vragen()
    print(f'vragen bruikbaar als puzzelvraag: {len(vragen)}')
    print(f'plafond bij drie per puzzel: {len(vragen) // 3}\n')

    # Zonder plafond loopt easy door als de moeilijke vakjes al leeg zijn, en
    # wordt dat niveau bijna drie keer zo groot als extremely-hard. Een vast
    # plafond per niveau houdt de vier bij elkaar. Het is bewust een instelling
    # en geen tweede rekenronde: dat laatste verdubbelde de looptijd tot boven
    # het kwartier, en dat is te duur voor een getal dat je ook kunt kiezen.
    puzzels, grenzen, ondergrens = bouw(vragen, args.aantal, seed, args.quota)
    print(f'plafond per niveau: {args.quota}')
    print(f'gebouwd: {len(puzzels)} puzzels')
    print(f'vragen gebruikt: {len(puzzels) * 3} van {len(vragen)}')
    print(f'ondergrens score {ondergrens} | niveaugrenzen {grenzen}\n')
    print('per bewerking :', dict(Counter(p['op'] for p in puzzels)))
    print('per niveau    :', dict(Counter(p['niveau'] for p in puzzels)))
    dubbel = sum(1 for p in puzzels
                 if len({q['categorie'] for q in p['vragen']}) < 3)
    print(f'puzzels met een dubbele categorie: {dubbel}')

    alle = [q['nr'] for p in puzzels for q in p['vragen']]
    assert len(alle) == len(set(alle)), 'een vraag komt twee keer voor'
    print('controle: elke vraag hoogstens een keer — in orde')

    if not args.schrijf:
        print('\n(proefdraai — voeg --schrijf toe om op te slaan)')
        return

    if args.doel == 'race':
        lijst = [als_puzzel(p, i, 'pool') for i, p in enumerate(puzzels, start=1)]
        schrijf_bestand('netto_race_pool.js', 'NETTO_RACE_POOL', lijst, args.doel)
        return

    # De bibliotheek wordt vervangen; de dagpuzzels blijven staan. Die dragen
    # een datum en zijn al gespeeld — dat is geschiedenis, geen voorraad. Nieuwe
    # dagpuzzels komen uit deze bibliotheek, via de databank.
    pad = os.path.join(DATA, 'netto_frontend_puzzles.js')
    ruw = open(pad, encoding='utf-8').read()
    bestaand = json.loads(ruw[ruw.index('=', ruw.index('window.')) + 1:].strip().rstrip(';'))
    bestaand['library'] = [als_puzzel(p, i, 'library')
                           for i, p in enumerate(puzzels, start=1)]
    bestaand['race'] = []
    schrijf_bestand('netto_frontend_puzzles.js', 'NETTO_REBUILT_PUZZLES',
                    bestaand, args.doel)
    print(f"dagpuzzels ongemoeid gelaten: {len(bestaand.get('daily', []))}")


def schrijf_bestand(naam, globale, inhoud, doel):
    kop = ('// Netto — unieke puzzels: elke vraag komt binnen deze set hoogstens\n'
           '// een keer voor.\n'
           f'// Gegenereerd door puzzels/maak_unieke_puzzels.py --doel {doel}\n'
           f'window.{globale} = ')
    tekst = kop + json.dumps(inhoud, ensure_ascii=False) + ';\n'
    for map_ in (DATA, SPIEGEL):
        with open(os.path.join(map_, naam), 'w', encoding='utf-8') as f:
            f.write(tekst)
    print(f'\n-> data/{naam} (en de spiegel)')


if __name__ == '__main__':
    main()
