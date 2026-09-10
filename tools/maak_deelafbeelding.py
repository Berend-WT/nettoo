# -*- coding: utf-8 -*-
"""Netto — maak de afbeelding die bij een gedeelde link hoort.

Draaien:  python tools/maak_deelafbeelding.py

WAAROM
index.html verwees naar og-image.png, maar dat bestand bestond niet. Deel je
een link naar het spel in WhatsApp, Slack of op X, dan haalt die dienst de
og:image op en krijgt een 404. Wat je dan ziet is een kale link zonder beeld,
of een kapot vlak — precies op het moment dat iemand besluit of hij klikt.

WAT ERUIT KOMT
website/og-image.png en og-image.png in de projectmap, 1200x630 (de maat die
alle platforms verwachten), in de kleuren van het spel: diep blauw met het
gele accent uit de knoppen, en het rasterpatroon dat ook achter de site staat.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BREED, HOOG = 1200, 630
BLAUW = (37, 47, 182)      # --bg-main
GEEL = (255, 216, 74)      # --accent
WIT = (255, 255, 255)
ZACHT = (199, 204, 255)    # --accent-blue-light

VET = ['C:/Windows/Fonts/arialbd.ttf', 'C:/Windows/Fonts/segoeuib.ttf',
       '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
GEWOON = ['C:/Windows/Fonts/arial.ttf', 'C:/Windows/Fonts/segoeui.ttf',
          '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']


def lettertype(kandidaten, grootte):
    for pad in kandidaten:
        if os.path.exists(pad):
            return ImageFont.truetype(pad, grootte)
    return ImageFont.load_default()


def main():
    afb = Image.new('RGB', (BREED, HOOG), BLAUW)
    tk = ImageDraw.Draw(afb)

    # Hetzelfde raster als achter de site: lijnen om de 48 pixels, net zichtbaar.
    for x in range(0, BREED, 48):
        tk.line([(x, 0), (x, HOOG)], fill=(46, 56, 190), width=1)
    for y in range(0, HOOG, 48):
        tk.line([(0, y), (BREED, y)], fill=(46, 56, 190), width=1)

    titel = lettertype(VET, 132)
    onder = lettertype(GEWOON, 38)
    som = lettertype(VET, 46)

    tk.text((90, 150), 'NETTO', font=titel, fill=WIT)
    tk.text((96, 300), 'Drie vragen. Eén verband.', font=onder, fill=ZACHT)
    tk.text((96, 352), 'Elke dag een nieuwe puzzel.', font=onder, fill=ZACHT)

    # De som als beeldmerk: dat is waar het spel om draait.
    doos = (90, 452, 640, 540)
    tk.rounded_rectangle(doos, radius=14, fill=GEEL)
    tekst = 'a  ×  b  =  c'
    l, t, r, b = tk.textbbox((0, 0), tekst, font=som)
    tk.text((doos[0] + (doos[2] - doos[0] - (r - l)) / 2 - l,
             doos[1] + (doos[3] - doos[1] - (b - t)) / 2 - t),
            tekst, font=som, fill=(20, 22, 59))

    for map_ in (WORTEL, os.path.join(WORTEL, 'website')):
        pad = os.path.join(map_, 'og-image.png')
        afb.save(pad, 'PNG', optimize=True)
        print(f'-> {os.path.relpath(pad, WORTEL)} ({os.path.getsize(pad) // 1024} kB)')


if __name__ == '__main__':
    main()
