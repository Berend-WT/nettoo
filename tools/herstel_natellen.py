# -*- coding: utf-8 -*-
"""Netto — snelle doorloop van de 150 vragen met vertrouwen "natellen".

Draaien:  python tools/herstel_natellen.py [--schrijf]

De markering "natellen" betekent dat de bron over het juiste onderwerp gaat maar
het getal niet als getal noemt: het artikel over Argentinie somt de vijf
buurlanden op zonder ergens "vijf" te schrijven. Bij verreweg de meeste van de
honderdvijftig is dat terecht en is er niets aan de hand.

Bij dertien is er wel iets aan de hand. Drie antwoorden kloppen niet, acht
vragen zijn dubbelzinnig of verraden hun eigen antwoord, en twee horen niet in
een rekenspel thuis. Dat is wat hier wordt rechtgezet.

De drie foute antwoorden zitten geen van drieen in een puzzel, en de acht
tekstcorrecties laten het antwoord staan. Er breekt dus geen enkele som.
"""

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

# nr: (nieuw antwoord, bron, toelichting) — geen van drieen zit in een puzzel.
ANTWOORD = {
    835: (5, 'https://en.wikipedia.org/wiki/Mediterranean_Sea',
          'Marokko, Algerije, Tunesie, Libie en Egypte. De oude telling rekende de Westelijke '
          'Sahara mee, maar die grenst aan de Atlantische Oceaan, niet aan de Middellandse Zee.'),
    836: (4, 'https://en.wikipedia.org/wiki/Red_Sea',
          'Egypte, Soedan, Eritrea en Djibouti. De oude telling van zes rekende Saoedi-Arabie '
          'en Jemen mee, en dat zijn geen Afrikaanse landen.'),
    914: (7, 'https://en.wikipedia.org/wiki/North_Sea',
          'Het Verenigd Koninkrijk, Noorwegen, Denemarken, Duitsland, Nederland, Belgie en '
          'Frankrijk. Zweden ligt er via het Skagerrak aan, en de vraag zegt "direct".'),
}

# nr: (nieuwe vraagtekst, toelichting) — antwoord blijft, sommen blijven heel.
TEKST = {
    685: ('Hoeveel armen heeft een octopus?',
          'Een octopus heeft acht armen. Tentakels is het verkeerde woord: die hebben '
          'inktvissen, octopussen niet.'),
    190: ('Hoeveel shotjes espresso zitten er klassiek in een cappuccino?',
          'Klassiek een shot; veel zaken gebruiken er twee. Met "klassiek" erbij is de vraag '
          'eenduidig.'),
    598: ('Hoeveel verschillende sommen kun je gooien met twee gewone dobbelstenen?',
          'Elf sommen, van twee tot en met twaalf. Zonder het woord "sommen" kon de vraag ook '
          'als 36 ogenparen worden gelezen.'),
    683: ('Hoeveel tanden heeft een volwassen witte haai in de voorste rij van de bovenkaak?',
          'De voorste functionele rij van de bovenkaak telt 24 tanden. Zonder de kaak te '
          'noemen kon het antwoord ook 26 zijn.'),
    1340: ('Hoeveel velden telt een Engels dambord van 8 bij 8?',
           'Vierenzestig velden. De oude tekst zei "een standaard dambord", terwijl vraag 1339 '
           'diezelfde vraag stelt voor het internationale bord van 10 bij 10 en 100 antwoordt.'),
    1245: ('Hoeveel eredivisiestadions hebben een capaciteit boven de 50.000?',
           'De Johan Cruijff Arena en De Kuip. De oude vraagtekst noemde beide stadions tussen '
           'haakjes en gaf daarmee het antwoord weg.'),
    1064: ('Hoeveel UNESCO-werelderfgoedlocaties heeft China (stand 2026)?',
           'China staat op zestig locaties, achter Italie met eenenzestig. Met een peiljaar '
           'veroudert dit antwoord niet stilletjes meer.'),
    1065: ('Hoeveel UNESCO-werelderfgoedlocaties heeft Duitsland (stand 2026)?',
           'Duitsland staat op vijfenvijftig locaties, na de toevoeging van de paleizen van '
           'Lodewijk II in 2025.'),
}

# Peiljaarvragen waarbij het aantal wel is meegegroeid.
PEIL_ANTWOORD = {1064: 60, 1065: 55}

# nr: reden — beide reservevragen, dus geen puzzel raakt ze kwijt.
VERVALT = {
    1179: 'Antwoord nul maakt elke deelsom stuk, net als bij de tien vragen die hierom al zijn '
          'geschrapt. Dat Nederland het WK nooit won is juist, maar onbruikbaar als rekenwaarde.',
    1128: 'Een streamingaantal van tien cijfers dat dagelijks verandert is geen schatvraag. '
          'Zonder peildatum is het bovendien nooit meer juist.',
}


def main():
    schrijf = '--schrijf' in sys.argv
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    huidig = {int(r['Nr']): (str(r['Vraag NL']), r['Antwoord'], r['In gebruik'])
              for _, r in d.iterrows()}

    print('Antwoord gecorrigeerd:')
    for nr, (nieuw, _, _) in ANTWOORD.items():
        v, a, g = huidig[nr]
        print(f'  {nr:5d} [{g}]  {a} -> {nieuw}   {v[:60]}')
    print('\nVraagtekst gecorrigeerd (antwoord blijft):')
    for nr, (tekst, _) in TEKST.items():
        v, a, g = huidig[nr]
        extra = f'   {a} -> {PEIL_ANTWOORD[nr]}' if nr in PEIL_ANTWOORD else ''
        print(f'  {nr:5d} [{g}]{extra}\n         was: {v[:74]}\n         is:  {tekst[:74]}')
    print('\nVervallen:')
    for nr in VERVALT:
        v, a, g = huidig[nr]
        print(f'  {nr:5d} [{g}]  {v[:66]} -> {a}')

    inpuzzel = [nr for nr in list(ANTWOORD) + list(VERVALT) + list(PEIL_ANTWOORD)
                if huidig[nr][2] in ('puzzel', 'daily')]
    print(f"\nhiervan in een puzzel: {inpuzzel if inpuzzel else 'geen — er breekt geen som'}")

    if not schrijf:
        print('\n(proefdraai — voeg --schrijf toe om op te slaan)')
        return

    shutil.copy2(REVIEW, os.path.join(
        os.path.dirname(REVIEW),
        f'_backup_natellen_{date.today():%Y-%m-%d}_vragen_review_compleet.xlsx'))
    boek = load_workbook(REVIEW)
    blad = boek['Vragen']
    kol = [c.value for c in blad[1]]
    i_v = kol.index('Vraag NL') + 1
    i_a = kol.index('Antwoord') + 1
    i_b = kol.index('Bron (geverifieerd)') + 1
    i_w = kol.index('Bewijszin') + 1
    i_t = kol.index('Vertrouwen bron') + 1
    i_s = kol.index('Status oude bron') + 1
    i_l = kol.index('Let op') + 1

    teweg = []
    for rij in range(2, blad.max_row + 1):
        nr = blad.cell(row=rij, column=1).value
        if nr in VERVALT:
            teweg.append(rij)
        elif nr in ANTWOORD:
            nieuw, bron, toelichting = ANTWOORD[nr]
            was = blad.cell(row=rij, column=i_a).value
            blad.cell(row=rij, column=i_a).value = nieuw
            blad.cell(row=rij, column=i_b).value = bron
            blad.cell(row=rij, column=i_w).value = toelichting[:400]
            blad.cell(row=rij, column=i_t).value = 'handmatig'
            blad.cell(row=rij, column=i_s).value = 'antwoord gecorrigeerd'
            blad.cell(row=rij, column=i_l).value = f'was {was}. {toelichting}'[:250]
        elif nr in TEKST:
            tekst, toelichting = TEKST[nr]
            was = blad.cell(row=rij, column=i_v).value
            blad.cell(row=rij, column=i_v).value = tekst
            blad.cell(row=rij, column=i_w).value = toelichting[:400]
            blad.cell(row=rij, column=i_t).value = 'handmatig'
            blad.cell(row=rij, column=i_s).value = 'vraagtekst gecorrigeerd'
            blad.cell(row=rij, column=i_l).value = f'was: {was}'[:250]
            if nr in PEIL_ANTWOORD:
                blad.cell(row=rij, column=i_a).value = PEIL_ANTWOORD[nr]
    for rij in sorted(teweg, reverse=True):
        blad.delete_rows(rij)
    boek.save(REVIEW)

    na = pd.read_excel(REVIEW, sheet_name='Vragen')
    print(f'\nvragen over: {len(na)}')
    print(na['Vertrouwen bron'].fillna('(leeg)').value_counts().to_string())


if __name__ == '__main__':
    main()
