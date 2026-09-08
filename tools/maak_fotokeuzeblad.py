# -*- coding: utf-8 -*-
"""Netto — maak het keuzeblad met fotokandidaten als miniaturen.

Draaien:  python tools/maak_fotokeuzeblad.py

Leest fotos/kandidaten.json, haalt de miniaturen op en zet ze naast elkaar in
een werkblad. Per vraag drie kandidaten met de licentie eronder. In de kolom
"Keuze" typ je 1, 2 of 3 — of je laat hem leeg als geen van drieen deugt.

Zo hoef je niet meer te zoeken, alleen te kijken en te kiezen. Welke Commons-
link bij welk nummer hoort wordt daarna automatisch ingevuld, dus je hoeft
nergens een adres over te typen.

De miniaturen komen in fotos/assets/kandidaten/ te staan. Die map hoeft niet
mee naar git; het werkblad is opnieuw te maken zolang kandidaten.json er is.
"""

import json
import os
import re
import ssl
import sys
import urllib.parse
import urllib.request

import pandas as pd
from openpyxl import Workbook
from openpyxl.drawing.image import Image as ExcelImage
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from PIL import Image as PILImage

try:
    import certifi
except ImportError:
    certifi = None

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
FOTOS = os.path.join(WORTEL, 'fotos')
VOORTGANG = os.path.join(FOTOS, 'kandidaten.json')
MINIATUREN = os.path.join(FOTOS, 'assets', 'kandidaten')
DOEL = os.path.join(WORTEL, 'vragen', 'fotokeuze.xlsx')
ONEDRIVE = os.path.join(os.path.expanduser('~'), 'OneDrive - Driestar-Wartburg')

BREED = 150   # pixels; bepaalt ook de kolombreedte
HOOG = 110    # pixels; bepaalt de rijhoogte
AGENT = 'Netto-fotokeuze/1.0 (educatief quizspel)'

# Woorden die de vraag opbouwen maar niets over het onderwerp zeggen. Eruit
# halen scheelt ruis in de zoekopdracht.
RUIS = {
    'how', 'many', 'much', 'what', 'which', 'does', 'did', 'the', 'and',
    'are', 'was', 'were', 'has', 'have', 'for', 'with', 'that', 'this',
    'about', 'average', 'approximately', 'estimated', 'contain', 'made',
    'you', 'your', 'its', 'their', 'from', 'into', 'over', 'per',
    'hoeveel', 'welk', 'welke', 'hoe', 'wat', 'een', 'de', 'het', 'van', 'in',
    'op', 'is', 'zijn', 'er', 'en', 'of', 'die', 'dat', 'met', 'voor', 'per',
    'bij', 'aan', 'te', 'tot', 'als', 'werd', 'wordt', 'heeft', 'hebben',
    'telt', 'staan', 'staat', 'duurt', 'ongeveer', 'gemiddeld', 'standaard',
    'volgens', 'totaal', 'jaar', 'meter', 'kilometer', 'centimeter',
    'millimeter', 'kilogram', 'gram', 'liter', 'ton', 'procent', 'graden',
    'seconde', 'seconden', 'minuut', 'minuten', 'uur', 'uren', 'dagen', 'dag',
    'maanden', 'miljoen', 'miljard', 'duizend', 'aantal', 'lang', 'hoog',
    'diep', 'breed', 'groot', 'zwaar', 'maximaal', 'wereldwijd', 'eerste',
    'stand', 'klassiek', 'bevat', 'kent', 'gebruikt', 'ooit',
}


def zoekterm(vraag, engels=None):
    # Commons en Unsplash zijn Engelstalig: "knipperbewegingen ogen" levert daar
    # niets op, "blinks eyes" wel. De bank heeft bij 1313 van de 1409 vragen een
    # Engelse zoekhulp staan; die gaat voor.
    bron = engels if isinstance(engels, str) and engels.strip() else vraag
    woorden = re.findall(r"[A-Za-zÀ-ÿ'’-]{3,}", str(bron))
    kern = [w for w in woorden if w.lower() not in RUIS]
    return ' '.join(kern[:4]) or str(bron)[:50]


def zoeklinks(vraag, bron, engels=None):
    q = urllib.parse.quote_plus(zoekterm(vraag, engels))
    return {
        'Commons': f'https://commons.wikimedia.org/w/index.php?search={q}'
                   f'&title=Special:MediaSearch&type=image',
        'Unsplash': f'https://unsplash.com/s/photos/{q}',
        'Artikel': bron if isinstance(bron, str) and 'wikipedia.org/wiki/' in bron else '',
    }


def context():
    return ssl.create_default_context(cafile=certifi.where()) if certifi \
        else ssl.create_default_context()


def haal_miniatuur(url, pad):
    if os.path.exists(pad):
        return True
    try:
        verzoek = urllib.request.Request(url, headers={'User-Agent': AGENT})
        with urllib.request.urlopen(verzoek, context=context(), timeout=30) as a:
            ruw = a.read()
        with open(pad, 'wb') as f:
            f.write(ruw)
        # Naar een vaste hoogte schalen zodat de rijen gelijk ogen en het
        # bestand klein blijft; Excel wordt traag van volledige afbeeldingen.
        with PILImage.open(pad) as afb:
            afb = afb.convert('RGB')
            schaal = min(BREED / afb.width, HOOG / afb.height)
            afb = afb.resize((max(1, int(afb.width * schaal)),
                              max(1, int(afb.height * schaal))))
            afb.save(pad, 'JPEG', quality=80)
        return True
    except Exception:
        if os.path.exists(pad):
            os.remove(pad)
        return False


def main():
    if not os.path.exists(VOORTGANG):
        print('nog geen kandidaten — draai eerst tools/zoek_fotokandidaten.py')
        return
    os.makedirs(MINIATUREN, exist_ok=True)
    with open(VOORTGANG, encoding='utf-8') as f:
        kandidaten = json.load(f)

    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    # Ook de vragen zonder kandidaat komen erin: juist daar moet je zelf zoeken,
    # en dan wil je de zoeklinks bij de hand hebben in plaats van in een tweede
    # bestand. De rij is dan leeg op de fotokolommen na.
    d = d[d['In gebruik'].isin(['daily', 'puzzel'])].copy()
    d['_r'] = d['In gebruik'].map({'daily': 0, 'puzzel': 1}).fillna(2)
    d = d.sort_values(['_r', 'Nr'])

    wb = Workbook()
    ws = wb.active
    ws.title = 'Fotokeuze'
    koppen = ['Nr', 'In gebruik', 'Vraag', 'Antwoord',
              'Foto 1', 'Foto 2', 'Foto 3', 'Keuze', 'Gevonden via',
              'Commons', 'Unsplash', 'Artikel', 'Opmerking']
    breedtes = [6, 11, 48, 11, 22, 22, 22, 9, 13, 11, 11, 11, 22]
    for i, (k, b) in enumerate(zip(koppen, breedtes), start=1):
        ws.column_dimensions[get_column_letter(i)].width = b
        c = ws.cell(row=1, column=i, value=k)
        c.font = Font(name='Arial', bold=True, color='FFFFFF', size=11)
        c.fill = PatternFill('solid', fgColor='2E7D32' if k == 'Keuze' else '1F3864')
        c.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    ws.row_dimensions[1].height = 26
    rand = Side(style='thin', color='D0D0D0')

    rij = 2
    gevuld = 0
    for _, r in d.iterrows():
        blok = kandidaten.get(str(int(r['Nr'])), {})
        lijst = blok.get('kandidaten') or []
        ws.row_dimensions[rij].height = (HOOG * 0.78 + 22) if lijst else 30
        for kol, waarde in ((1, int(r['Nr'])), (2, r['In gebruik']),
                            (3, str(r['Vraag NL'])), (4, r['Antwoord'])):
            c = ws.cell(row=rij, column=kol, value=waarde)
            c.font = Font(name='Arial', size=10)
            c.alignment = Alignment(vertical='center', wrap_text=(kol == 3))

        for i, kand in enumerate(lijst[:3]):
            kol = 5 + i
            naam = f"{int(r['Nr'])}_{i}.jpg"
            pad = os.path.join(MINIATUREN, naam)
            if kand.get('miniatuur') and haal_miniatuur(kand['miniatuur'], pad):
                try:
                    afb = ExcelImage(pad)
                    afb.anchor = f'{get_column_letter(kol)}{rij}'
                    ws.add_image(afb)
                except Exception:
                    pass
            # De licentie komt als celtekst achter de afbeelding te staan; hij
            # is nodig voor de naamsvermelding en moet zichtbaar blijven.
            c = ws.cell(row=rij, column=kol)
            c.value = kand.get('licentie', '')
            c.font = Font(name='Arial', size=7, color='808080')
            c.alignment = Alignment(horizontal='center', vertical='bottom')
            c.border = Border(left=rand, right=rand, top=rand, bottom=rand)

        k = ws.cell(row=rij, column=8)
        k.fill = PatternFill('solid', fgColor='FFF9E0')
        k.alignment = Alignment(horizontal='center', vertical='center')
        k.font = Font(name='Arial', size=12, bold=True)

        # Foto's uit het bronartikel gaan gegarandeerd over het juiste
        # onderwerp; die uit de zoekfunctie lang niet altijd. Dat verschil moet
        # zichtbaar zijn, anders kost het beoordelen alsnog tijd.
        h = ws.cell(row=rij, column=9, value=blok.get('herkomst', 'zelf zoeken'))
        h.font = Font(name='Arial', size=9)
        h.alignment = Alignment(horizontal='center', vertical='center')
        h.fill = PatternFill('solid',
                             fgColor='D6EAD6' if blok.get('herkomst') == 'artikel'
                             else 'FBE9A5' if lijst else 'F0F0F0')

        # Drie klikbare zoeklinks per rij, zodat afkeuren geen doodlopende weg is.
        for i, (naam, adres) in enumerate(
                zoeklinks(r['Vraag NL'], r.get('Bron (geverifieerd)'),
                          r.get('Vraag EN (zoekhulp)')).items()):
            c = ws.cell(row=rij, column=10 + i)
            if not adres:
                continue
            c.hyperlink = adres
            c.value = naam.lower()
            c.font = Font(name='Arial', size=9, color='0563C1', underline='single')
            c.alignment = Alignment(horizontal='center', vertical='center')
        ws.cell(row=rij, column=13).fill = PatternFill('solid', fgColor='FBFBFB')
        rij += 1
        gevuld += 1

    ws.freeze_panes = 'E2'
    ws.auto_filter.ref = f'A1:{get_column_letter(len(koppen))}{ws.max_row}'
    wb.save(DOEL)

    # De links horen bij de nummers; ze gaan mee in een tweede blad zodat de
    # keuze later automatisch omgezet kan worden naar een adres.
    regels = []
    for nr, blok in kandidaten.items():
        for i, kand in enumerate(blok.get('kandidaten') or [], start=1):
            regels.append({'Nr': int(nr), 'Keuze': i, 'Commons-pagina': kand['pagina'],
                           'Licentie': kand['licentie'], 'Maker': kand['maker']})
    with pd.ExcelWriter(DOEL, engine='openpyxl', mode='a') as w:
        pd.DataFrame(regels).to_excel(w, index=False, sheet_name='Links')

    if os.path.isdir(ONEDRIVE):
        import shutil
        shutil.copy2(DOEL, os.path.join(ONEDRIVE, os.path.basename(DOEL)))
    print(f'{gevuld} vragen met kandidaten in het keuzeblad')
    print(f'-> {DOEL}')


if __name__ == '__main__':
    main()
