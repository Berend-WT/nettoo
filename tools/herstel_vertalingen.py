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

    print(f'{hersteld} emoji teruggezet')
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
