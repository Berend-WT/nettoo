# -*- coding: utf-8 -*-
"""Netto — repareer de schade die het vertalen aan de Engelse teksten aanrichtte.

Draaien:  python tools/herstel_vertalingen.py [--droog]

WAT ER MIS IS
data/netto_translations_en.js is machinaal gemaakt, en op de plekken waar een
emoji in de Nederlandse tekst stond ging het mis. Drie soorten schade:

1. De emoji werd een punt. "✅ Je hebt de puzzel van vandaag al gespeeld!" werd
   ". You've already played today's puzzle!" — met een losse punt vooraan. Dat
   is wat een speler ziet als hij het spel in het Engels zet.

2. De emoji werd vertaald alsof het een woord was. "🔥 Huidige streak" werd
   "Gallus domesticus Current streak" — de Latijnse naam voor het hoenderhoen.
   "🟧 ≤2,50×" werd "Plywood ≤2,50×", multiplex.

3. De emoji verdween zonder spoor. Minder erg, maar het beeld valt weg.

WAT DIT SCRIPT DOET
Het neemt de emoji vooraan uit de Nederlandse sleutel en zet die terug voor de
Engelse tekst, na eerst de rommel weg te halen die ervoor in de plaats kwam.
Alleen de emoji aan het begin, want dat is waar de schade zit; emoji midden in
een zin zijn ongemoeid gelaten.

Wat het NIET doet is de zinnen zelf beoordelen. Er zitten ook gewone
vertaalfouten in ("Wilde Gok" werd "Wild Game"), en die staan apart in
HANDMATIG hieronder, omdat een script niet kan zien dat een zin onzin is.
"""

import argparse
import io
import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BESTAND = os.path.join(WORTEL, 'data', 'netto_translations_en.js')

EMOJI = re.compile('[\U0001F300-\U0001FAFF☀-➿⬀-⯿️✅✓✔]')
# Een beginnende emoji plus de spatie erachter.
KOP = re.compile(r'^((?:[\U0001F300-\U0001FAFF☀-➿⬀-⯿️✅✓✔]️?\s*)+)')

# Zinnen die het vertaalprogramma inhoudelijk verkeerd heeft. Een script kan
# niet zien dat een zin onzin is, dus deze staan met de hand.
HANDMATIG = {
    'Ontvangen! Je inzending wordt gereviewd — je krijgt een melding als hij geaccepteerd is. 📮':
        'Received! Your submission will be reviewed — you will get a notification if it is accepted. 📮',
    '✓ Exact — door!': '✓ Exact — keep going!',
    '🎲 Wilde Gok · Oef, rekenmachine nodig!': '🎲 Wild Guess · Oof, you need a calculator!',
    '🔥 Huidige streak: 0 dagen': '🔥 Current streak: 0 days',
    '🟧 ≤2,50×': '🟧 ≤2.50×',
    '🟨 ≤1,50×': '🟨 ≤1.50×',
    '🟩 ≤1,15×': '🟩 ≤1.15×',
    '🟥 meer': '🟥 more',
    '🎯 Scherpschutter · Heel strak in de buurt!': '🎯 Sharpshooter · Very close!',
    '💡 Scherp Inzicht · Goede schatting!': '💡 Sharp Insight · Good estimate!',
    '🧭 Goeie Richting · Redelijke ordegrootte!': '🧭 Right Direction · Reasonable order of magnitude!',
    '👑 Wiskundig Genie · Meesterlijk geschat!': '👑 Mathematical Genius · Masterly estimate!',
    'Wachtwoord vergeten? 🔑': 'Forgot your password? 🔑',
}


# Terugkerende vertaalfouten in de vraagteksten, gevonden nadat een tester
# meldde dat er rare Engelse zinnen langskwamen.
#
# "tientallen" werd "dozens" — dozijnen, dus twaalftallen. Dat is geen stijlfout
# maar een rekenfout: "afgerond op tientallen" en "afgerond op dozijnen" vragen
# om een ander antwoord. Vijftig vragen.
#
# "afgerond" werd soms "finished". "How many days did Saigon fall to reunion
# (finished in tens of days)?" is daar het resultaat van.
#
# En de spelling liep door elkaar: 56 keer "meters" tegenover honderden keren
# "metres". Beide zijn Engels, maar niet in dezelfde zin.
ZINNEN = [
    ('(in dozens of rounded)', '(rounded to the nearest ten)'),
    ('(in hundreds of rounded)', '(rounded to the nearest hundred)'),
    ('(in dozens of meters)', '(rounded to the nearest ten metres)'),
    ('in dozens of rounded', 'rounded to the nearest ten'),
    ('in hundreds of rounded', 'rounded to the nearest hundred'),
    ('finished in tens of days', 'rounded to the nearest ten days'),
    ('finished in tens', 'rounded to the nearest ten'),
    ('finished in dozens of meters', 'rounded to the nearest ten metres'),
    ('finished in dozens', 'rounded to the nearest ten'),
    ('finished on tens', 'rounded to the nearest ten'),
    ('finished in thousands of km', 'rounded to the nearest thousand km'),
    ('finished in hundreds of km', 'rounded to the nearest hundred km'),
    ('finished in whole hours', 'rounded to the nearest whole hour'),
]

# Alleen waar het Nederlands ook echt over tientallen gaat.
DOZENS = [('in dozens', 'in tens'), ('of dozens', 'of tens'), ('dozens of', 'tens of')]

SPELLING = [('meters', 'metres'), ('meter', 'metre'),
            ('kilometers', 'kilometres'), ('kilometer', 'kilometre'),
            ('liters', 'litres'), ('liter', 'litre')]


def herstel_zinnen(d):
    """Tweede ronde: terugkerende fouten in de vraagteksten zelf."""
    import re as _re
    n_zin = n_doz = n_sp = 0
    for nl, en in list(d.items()):
        oud = en
        for a, b in ZINNEN:
            if a in en:
                en = en.replace(a, b)
        if en != oud:
            n_zin += 1
        # "dozens" alleen aanpakken als het Nederlands over tientallen gaat
        if 'dozens' in en and ('tiental' in nl.lower()):
            voor = en
            for a, b in DOZENS:
                en = en.replace(a, b)
            en = en.replace('dozens', 'tens')
            if en != voor:
                n_doz += 1
        voor = en
        for a, b in SPELLING:
            en = _re.sub(r'\b' + a + r'\b', b, en)
        if en != voor:
            n_sp += 1
        d[nl] = en
    return n_zin, n_doz, n_sp


def main():
    ontleder = argparse.ArgumentParser()
    ontleder.add_argument('--droog', action='store_true')
    args = ontleder.parse_args()

    tekst = open(BESTAND, encoding='utf-8').read()
    kop = tekst[:tekst.index('{')]
    staart = tekst[tekst.rindex('}') + 1:]
    d = json.loads(tekst[tekst.index('{'):tekst.rindex('}') + 1])

    hersteld, handmatig, ongemoeid = 0, 0, 0
    for nl, en in list(d.items()):
        if nl in HANDMATIG:
            if d[nl] != HANDMATIG[nl]:
                d[nl] = HANDMATIG[nl]
                handmatig += 1
            continue
        m = KOP.match(nl)
        if not m:
            continue
        if EMOJI.search(en):
            ongemoeid += 1
            continue
        # Weg met wat er voor de emoji in de plaats kwam: een losse punt, komma
        # of uitroepteken vooraan.
        schoon = re.sub(r'^[.,!;:]+\s*', '', en).lstrip()
        d[nl] = m.group(1).rstrip() + ' ' + schoon
        hersteld += 1

    n_zin, n_doz, n_sp = herstel_zinnen(d)
    print(f'{hersteld} emoji teruggezet')
    print(f'{n_zin} zinnen met een kapotte afrondingsinstructie hersteld')
    print(f'{n_doz} keer "dozens" -> "tens" waar het Nederlands tientallen zegt')
    print(f'{n_sp} teksten op Britse spelling gezet')
    print(f'{handmatig} zinnen met de hand rechtgezet')
    print(f'{ongemoeid} hadden hun emoji al')

    if args.droog:
        print('\ndroge run: niets geschreven')
        return
    with open(BESTAND, 'w', encoding='utf-8') as f:
        f.write(kop + json.dumps(d, ensure_ascii=False, indent=2) + staart)
    print(f'\n-> {os.path.relpath(BESTAND, WORTEL)}')


if __name__ == '__main__':
    main()
