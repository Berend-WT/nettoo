# -*- coding: utf-8 -*-
"""Netto — zet de fotokandidaten die op een oordeel wachten op contactvellen.

Draaien:  python tools/maak_wachtvellen.py

WAAROM ZE WACHTEN
378 vragen hebben wel een fotokandidaat maar geen foto in het spel. Dat is geen
vergissing: die kandidaten komen uit een zoekactie die het onderwerp uit de
vraagtekst raadt, en dat zit er ongeveer drie van de tien keer naast. "Muzen"
leverde een Maya-god op, "snaren" een foto van George Kooymans. Zeven op de tien
is te weinig om vanzelf toe te passen, dus wachten ze.

Wat ze niet kunnen is zichzelf beoordelen. Dat kan alleen door te kijken.

DIT IS HETZELFDE GEREEDSCHAP ALS maak_contactvellen.py, ANDERE BRON
Dat script toont de foto's die al in het spel staan. Dit toont wat erin zou
kunnen. Verder werkt het gelijk: twintig per vel, op wit samengesteld (een
doorzichtige SVG wordt anders een zwart vlak), met een nummerlijst ernaast.

DE UITKOMST
fotos/wachtvellen/vel01.jpg en verder, plus vragen.txt met per cel de vraag en
de bestandsnaam. Wat goedgekeurd wordt gaat via tools/verwerk_wachtoordeel.py
als handmatige keuze het spel in.
"""

import json
import os
import ssl
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import maak_fotobestand as mf

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(WORTEL, 'fotos', 'assets', 'wachtrij')
VELLEN = os.path.join(WORTEL, 'fotos', 'wachtvellen')
KOLOMMEN, RIJEN, CEL = 5, 4, 300
AGENT = 'Netto-fotocontrole/1.0 (penoftafel@gmail.com)'

try:
    import certifi
    CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    CONTEXT = ssl.create_default_context()


def wachtenden():
    """Precies de vragen die maak_fotobestand.py als 'wacht op keuze' telt."""
    hoofd = mf.lees(os.path.join(mf.FOTOS, 'hoofdafbeeldingen.json'))
    onderwerp = mf.lees(os.path.join(mf.FOTOS, 'onderwerpafbeeldingen.json'))
    oud = mf.lees(os.path.join(mf.FOTOS, 'kandidaten.json'))
    handmatig = mf.lees(os.path.join(mf.FOTOS, 'handmatige_fotos.json'))
    geblokkeerd = set(mf.lees(os.path.join(mf.FOTOS, 'geblokkeerd.json')).get('vragen', []))

    keuzes = {}
    if os.path.exists(mf.KEUZE):
        try:
            kb = pd.read_excel(mf.KEUZE, sheet_name='Fotokeuze')
            for _, r in kb.iterrows():
                try:
                    keuzes[int(r['Nr'])] = int(r['Keuze'])
                except (TypeError, ValueError):
                    continue
        except Exception:
            pass

    d = pd.read_excel(mf.REVIEW, sheet_name='Vragen')
    uit = []
    for _, r in d.iterrows():
        nr = int(r['Nr'])
        vraag = str(r['Vraag NL'])
        if vraag in geblokkeerd or str(nr) in handmatig or nr in keuzes:
            continue
        beste = (hoofd.get(str(nr), {}).get('kandidaten') or [None])[0]
        if beste and mf.geschikt_beeld(beste.get('titel', '')):
            continue   # die heeft al een infoboxfoto en komt vanzelf in het spel
        gevonden = (onderwerp.get(str(nr), {}).get('kandidaten') or [None])[0]
        if gevonden and not mf.geschikt_beeld(gevonden.get('titel', '')):
            gevonden = None
        rest = [k for k in ([gevonden] if gevonden else []) +
                [k for k in (oud.get(str(nr), {}).get('kandidaten') or [])
                 if mf.past_bij_onderwerp(k.get('titel', ''), r['Bron (geverifieerd)'])
                 and mf.geschikt_beeld(k.get('titel', ''))]]
        if rest:
            uit.append({'nr': nr, 'vraag': vraag, 'kandidaat': rest[0]})
    return uit


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
            # Op wit, niet op zwart: een doorzichtige SVG wordt anders een
            # zwart vlak en dan keur je een goede foto af.
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
    lijst = wachtenden()
    print(f'{len(lijst)} vragen wachten op een oordeel; miniaturen ophalen ...')

    with ThreadPoolExecutor(max_workers=4) as pool:
        paden = list(pool.map(haal, [(n, r['kandidaat']['miniatuur'])
                                     for n, r in enumerate(lijst)]))
    print(f'{sum(1 for p in paden if p)} opgehaald, {sum(1 for p in paden if not p)} mislukt')

    per_vel = KOLOMMEN * RIJEN
    regels = []
    for start in range(0, len(lijst), per_vel):
        deel = list(enumerate(lijst[start:start + per_vel], start=1))
        vel = Image.new('RGB', (KOLOMMEN * CEL, RIJEN * CEL), (240, 240, 245))
        tekenaar = ImageDraw.Draw(vel)
        for plek, rij in deel:
            kol, rijnr = (plek - 1) % KOLOMMEN, (plek - 1) // KOLOMMEN
            x, y = kol * CEL, rijnr * CEL
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
        vel.save(os.path.join(VELLEN, f'vel{nummer:02d}.jpg'), 'JPEG', quality=88)
        regels.append((nummer, deel))

    with open(os.path.join(VELLEN, 'vragen.txt'), 'w', encoding='utf-8') as f:
        for nummer, deel in regels:
            f.write(f'== vel {nummer:02d} ==\n')
            for plek, rij in deel:
                titel = rij['kandidaat'].get('titel', '').replace('File:', '')
                f.write(f"{plek}\t{rij['nr']}\t{rij['vraag']}\t[{titel}]\n")
    print(f'{len(regels)} vellen -> {os.path.relpath(VELLEN, WORTEL)}')


if __name__ == '__main__':
    main()
