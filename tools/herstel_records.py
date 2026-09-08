# -*- coding: utf-8 -*-
"""Netto — controleer de vragen over wereldrecords en zet de fouten recht.

Draaien:  python tools/herstel_records.py [--schrijf]

Deze zeven vragen droegen de markering "veroudert" omdat records nu eenmaal
gebroken worden. Bij het nakijken bleek dat die markering bij drie ervan het
echte probleem verhulde: het antwoord was gewoon fout, en niet een beetje.
Bij twee andere klopte het antwoord juist wel én staat het record al decennia,
dus daar is "veroudert" onnodig alarmerend.

Wat er gecontroleerd is, met de stand van 2026:

  452  meeste marathons        1000 -> 1305   Horst Preisler, 1974 t/m 2004
  456  langste gamemarathon     135 -> 144    Szabolcs Csepe, oktober 2024
  1311 meeste jongleurs        1000 -> 1508   Edinburgh, 7 augustus 1998
  1297 hoogste klifduik          59 blijft    Laso Schaller sprong 58,5 meter
  1314 push-ups in 24 uur     46000 blijft    exact 46.001, Charles Servizio
  1492 grootste containerschip 24000 blijft   MSC Irina haalt 24.346 TEU
  271  Mammoth Cave             685 blijft    de gekarteerde lengte groeit nog

Twee van de drie fouten zitten in een puzzel. Zoals eerder wordt alleen de
vragenbank aangepast; welke puzzels breken komt in het herbouwoverzicht.
"""

import json
import os
import shutil
import sys
from datetime import date

import pandas as pd
from openpyxl import load_workbook

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
BANK = os.path.join(WORTEL, 'vragen', '1000+ vragen netjes gecategoriseerd.xlsx')
HERBOUW = os.path.join(WORTEL, 'vragen', 'puzzels_om_te_herbouwen.xlsx')
DATA = os.path.join(WORTEL, 'data')

BESTANDEN = ['netto_frontend_puzzles.js', 'netto_breinkrakers.js', 'netto_race_pool.js']

# nr: (nieuw antwoord of None, nieuwe vraagtekst of None, bron, toelichting)
HERSTEL = {
    452: (1305, None, 'https://www.guinnessworldrecords.com/world-records/64777-most-marathons-completed',
          'Horst Preisler liep tussen 1974 en eind 2004 1305 marathons of langer. Het opgegeven '
          '1000 was een ronde gok.'),
    456: (144, 'Hoeveel uur duurde het langste videogame-marathonrecord (stand 2026)?',
          'https://www.guinnessworldrecords.com/world-records/longest-video-games-marathon',
          'Szabolcs Csepe speelde in oktober 2024 144 uur Dance Dance Revolution. Dit record '
          'verschuift regelmatig, vandaar het peiljaar in de vraag.'),
    1311: (1508, None, 'https://www.guinnessworldrecords.com/world-records/68643-most-people-juggling-simultaneously',
           'Op 7 augustus 1998 jongleerden 1508 mensen tegelijk in Edinburgh. Dat record staat '
           'sindsdien, dus het veroudert niet.'),
}

# nr: (bron, toelichting) — antwoord klopt, markering "veroudert" was onterecht
BEVESTIGD = {
    1297: ('https://www.guinnessworldrecords.com/world-records/407825-highest-cliff-jump',
           'Laso Schaller sprong op 4 augustus 2015 van 58,5 meter, afgerond 59. Het record staat '
           'sindsdien onveranderd.'),
    1314: ('https://www.guinnessworldrecords.com/world-records/most-push-ups-in-24-hours',
           'Charles Servizio deed er 46.001 in april 1993. Het staat er dus al ruim dertig jaar; '
           'afgerond op 46.000 klopt het.'),
}


def laad(pad):
    t = open(pad, encoding='utf-8').read()
    i = t.index('=', t.index('window.')) + 1
    return json.loads(t[i:].strip().rstrip(';'))


def alle_puzzels(data):
    if isinstance(data, list):
        return [('', p) for p in data]
    return [(k, p) for k, v in data.items() if isinstance(v, list)
            for p in v if isinstance(p, dict)]


def vragen_in(p):
    uit = []
    for i in (1, 2, 3, 4):
        g = p.get(f'q{i}')
        if isinstance(g, dict) and 'label' in g:
            uit.append(g['label'])
        elif f'q{i}_label' in p:
            uit.append(p[f'q{i}_label'])
    return uit


def main():
    schrijf = '--schrijf' in sys.argv
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    tekst_van = {int(r['Nr']): str(r['Vraag NL']) for _, r in d.iterrows()}
    antw_van = {int(r['Nr']): r['Antwoord'] for _, r in d.iterrows()}

    print('Antwoord gecorrigeerd:')
    for nr, (nieuw, _, _, _) in HERSTEL.items():
        print(f'  {nr:5d}  {antw_van[nr]} -> {nieuw}   {tekst_van[nr][:52]}')
    print('\nAntwoord klopt, markering "veroudert" weggehaald:')
    for nr in BEVESTIGD:
        print(f'  {nr:5d}  {antw_van[nr]}   {tekst_van[nr][:52]}')

    breekt = {tekst_van[nr]: nr for nr in HERSTEL}
    rijen = []
    for naam in BESTANDEN:
        for sleutel, p in alle_puzzels(laad(os.path.join(DATA, naam))):
            for label in vragen_in(p):
                if label in breekt:
                    rijen.append({
                        'Bestand': naam.replace('netto_', '').replace('.js', ''),
                        'Lijst': sleutel, 'Puzzel': p.get('id'),
                        'Datum': p.get('date', ''),
                        'Som': p.get('calculation') or p.get('formula', ''),
                        'Vraag Nr': breekt[label], 'Vraag': label,
                        'Oud antwoord': antw_van[breekt[label]],
                        'Vervangers met dat antwoord': 0,
                        'Advies': 'recordantwoord gecorrigeerd'})
    nieuw_df = pd.DataFrame(rijen)
    print(f'\npuzzels die hierdoor breken: {len(nieuw_df)}')

    if not schrijf:
        print('\n(proefdraai — voeg --schrijf toe om op te slaan)')
        return

    if len(nieuw_df) and os.path.exists(HERBOUW):
        oud = pd.read_excel(HERBOUW, sheet_name='Te herbouwen')
        pd.concat([oud, nieuw_df], ignore_index=True).drop_duplicates(
            subset=['Bestand', 'Lijst', 'Puzzel', 'Vraag Nr']).to_excel(
            HERBOUW, index=False, sheet_name='Te herbouwen')

    for pad in (REVIEW, BANK):
        shutil.copy2(pad, os.path.join(
            os.path.dirname(pad),
            f'_backup_records_{date.today():%Y-%m-%d}_{os.path.basename(pad)}'))
        boek = load_workbook(pad)
        for blad in boek.worksheets:
            kop = [c.value for c in blad[1]]
            if 'Vraag NL' not in kop or 'Antwoord' not in kop:
                continue
            i_v = kop.index('Vraag NL') + 1
            i_a = kop.index('Antwoord') + 1
            i_b = kop.index('Bron EN') + 1 if 'Bron EN' in kop else None
            i_g = kop.index('Bron (geverifieerd)') + 1 if 'Bron (geverifieerd)' in kop else None
            i_w = kop.index('Bewijszin') + 1 if 'Bewijszin' in kop else None
            i_t = kop.index('Vertrouwen bron') + 1 if 'Vertrouwen bron' in kop else None
            i_l = kop.index('Let op') + 1 if 'Let op' in kop else None
            for rij in range(2, blad.max_row + 1):
                tekst = blad.cell(row=rij, column=i_v).value
                nr = next((n for n, t in tekst_van.items() if t == tekst), None)
                if nr in HERSTEL:
                    nieuw, nieuwe_tekst, bron, uitleg = HERSTEL[nr]
                    was = blad.cell(row=rij, column=i_a).value
                    blad.cell(row=rij, column=i_a).value = nieuw
                    if nieuwe_tekst:
                        blad.cell(row=rij, column=i_v).value = nieuwe_tekst
                    for kol, waarde in ((i_b, bron), (i_g, bron), (i_w, uitleg[:400]),
                                        (i_t, 'handmatig'),
                                        (i_l, f'was {was}. {uitleg}'[:250])):
                        if kol:
                            blad.cell(row=rij, column=kol).value = waarde
                elif nr in BEVESTIGD:
                    bron, uitleg = BEVESTIGD[nr]
                    for kol, waarde in ((i_b, bron), (i_g, bron), (i_w, uitleg[:400]),
                                        (i_t, 'handmatig')):
                        if kol:
                            blad.cell(row=rij, column=kol).value = waarde
        boek.save(pad)
        print(f'bijgewerkt: {os.path.basename(pad)}')


if __name__ == '__main__':
    main()
