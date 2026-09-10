# -*- coding: utf-8 -*-
"""Netto — zet alle foto's uit het spel op contactvellen om ze te bekijken.

Draaien:  python tools/maak_contactvellen.py

WAAROM
De foto's zijn beoordeeld op bestandsnaam en artikelnaam. Dat is beter dan
niets, maar niet goed genoeg: van twaalf steekproeven bleken er drie fout die
op hun naam waren goedgekeurd. Een kwart. "Utrecht (16295236803).jpg" klinkt
prima bij een vraag over de Domtoren, tot je ziet dat die toren piepklein in de
mist staat tussen kantoorpanden.

Alles los opvragen kost honderden ronden. Twintig per vel maakt er vijfendertig
van, en op 300 pixels per cel is nog te zien wat er staat.

De cel draagt alleen een nummer; de vragen komen als lijst in de uitvoer te
staan. Tekst in het beeld zou bij deze schaal toch niet leesbaar zijn.
"""

import json
import os
import ssl
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from PIL import Image, ImageDraw

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOTOS = os.path.join(WORTEL, 'data', 'netto_fotos.js')
CACHE = os.path.join(WORTEL, 'fotos', 'assets', 'controle')
VELLEN = os.path.join(WORTEL, 'fotos', 'contactvellen')
KOLOMMEN, RIJEN = 5, 4
CEL = 300
AGENT = 'Netto-fotocontrole/1.0 (penoftafel@gmail.com)'

try:
    import certifi
    CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CONTEXT = ssl.create_default_context()


def haal(taak):
    nummer, url = taak
    pad = os.path.join(CACHE, f'{nummer:04d}.jpg')
    if os.path.exists(pad):
        return pad
    try:
        verzoek = urllib.request.Request(url, headers={'User-Agent': AGENT})
        with urllib.request.urlopen(verzoek, timeout=30, context=CONTEXT) as a:
            ruw = a.read()
        with open(pad, 'wb') as f:
            f.write(ruw)
        with Image.open(pad) as afb:
            # Op wit samenstellen, niet op zwart. Veel Wikimedia-bestanden zijn
            # SVG's met een doorzichtige achtergrond - een zwarte appel, zwarte
            # letters, een zwarte lijntekening. Naar RGB omzetten maakt dat
            # doorzichtige deel zwart, en dan zie je een zwart vlak terwijl de
            # browser hem netjes op de lichte kaart toont. Ik heb daar bijna
            # twee goede foto's op afgekeurd.
            afb = afb.convert('RGBA')
            vel = Image.new('RGB', afb.size, (255, 255, 255))
            vel.paste(afb, mask=afb.split()[3])
            vel.thumbnail((CEL, CEL))
            vel.save(pad, 'JPEG', quality=82)
        return pad
    except Exception:
        return None


def main():
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(VELLEN, exist_ok=True)
    tekst = open(FOTOS, encoding='utf-8').read()
    fotos = json.loads(tekst[tekst.index('{'):tekst.rindex('}') + 1])
    lijst = sorted(fotos.items())
    print(f'{len(lijst)} foto\'s ophalen ...')

    # Vier tegelijk: Wikimedia levert miniaturen snel en dit blijft ver onder
    # wat als belasting telt.
    with ThreadPoolExecutor(max_workers=4) as pool:
        paden = list(pool.map(haal, [(n, f['url']) for n, (_, f) in enumerate(lijst)]))
    gelukt = sum(1 for p in paden if p)
    print(f'{gelukt} opgehaald, {len(paden) - gelukt} mislukt')

    per_vel = KOLOMMEN * RIJEN
    regels = []
    for start in range(0, len(lijst), per_vel):
        deel = list(enumerate(lijst[start:start + per_vel], start=1))
        vel = Image.new('RGB', (KOLOMMEN * CEL, RIJEN * CEL), (240, 240, 245))
        tekenaar = ImageDraw.Draw(vel)
        for plek, (vraag, _) in deel:
            kol, rij = (plek - 1) % KOLOMMEN, (plek - 1) // KOLOMMEN
            x, y = kol * CEL, rij * CEL
            pad = paden[start + plek - 1]
            if pad and os.path.exists(pad):
                with Image.open(pad) as afb:
                    afb = afb.convert('RGB')
                    afb.thumbnail((CEL - 8, CEL - 30))
                    vel.paste(afb, (x + (CEL - afb.width) // 2, y + 26))
            tekenaar.rectangle([x, y, x + CEL - 1, y + 22], fill=(30, 40, 90))
            tekenaar.text((x + 8, y + 5), str(plek), fill=(255, 255, 255))
            tekenaar.rectangle([x, y, x + CEL - 1, y + CEL - 1], outline=(210, 210, 220))
        nummer = start // per_vel + 1
        naam = os.path.join(VELLEN, f'vel{nummer:02d}.jpg')
        vel.save(naam, 'JPEG', quality=88)
        regels.append((nummer, naam, [v for _, (v, _) in deel]))

    with open(os.path.join(VELLEN, 'vragen.txt'), 'w', encoding='utf-8') as f:
        for nummer, naam, vragen in regels:
            f.write(f'== vel {nummer:02d} ==\n')
            for plek, vraag in enumerate(vragen, start=1):
                f.write(f'{plek}\t{vraag}\n')
    print(f'{len(regels)} vellen -> {os.path.relpath(VELLEN, WORTEL)}')


if __name__ == '__main__':
    main()
