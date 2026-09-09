# -*- coding: utf-8 -*-
"""Netto — werkblad waarin je alleen de slechte foto's wegstreept.

Draaien:  python tools/maak_fotoblad_afkeuren.py

WAAROM ANDERSOM
Het gewone keuzeblad vraagt per vraag een keuze uit drie kandidaten. Voor de
vragen waarvan de bron een Wikipedia-artikel is hoeft dat niet: die krijgen de
infoboxfoto en die klopt per definitie. Wat overblijft zijn de vragen waar de
foto is geraden uit de vraagtekst. Gemeten op een steekproef van 26 klopt daar
ongeveer driekwart van.

Driekwart is te weinig om ongezien toe te passen, maar te veel om alles opnieuw
te laten uitzoeken. Dus staat er per rij één voorstel, en streep je alleen weg
wat niet deugt — ongeveer een op de vier. Dat is drie keer minder werk dan
kiezen, en wat overblijft is door een mens goedgekeurd in plaats van door een
script geraden.

INVULLEN
  kolom "Weg?"      een 0, een x of het woord nee bij een foto die niet deugt.
                    Leeg laten betekent: deze is goed.
  tabblad Voortgang tot welke rij je gekeken hebt. Zonder dat getal weet het
                    verwerkingsscript niet of een lege regel "goedgekeurd"
                    betekent of "nog niet bekeken", en dat verschil bepaalt of
                    er een foto in het spel komt.
"""

import os
import sys

import openpyxl
from openpyxl.drawing.image import Image as XlImage
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Het downloaden en schalen van miniaturen staat al in het keuzeblad-script;
# tweemaal dezelfde code onderhouden is vragen om verschil.
from maak_fotokeuzeblad import haal_miniatuur

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
FOTOS = os.path.join(WORTEL, 'fotos')
MINIATUREN = os.path.join(FOTOS, 'assets', 'kandidaten')
UIT = os.path.join(WORTEL, 'vragen', 'fotos_afkeuren.xlsx')
RANG = {'daily': 0, 'puzzel': 1, 'race': 2, 'breinkraker': 3}
KOLOMMEN = ['Nr', 'In gebruik', 'Vraag', 'Antwoord', 'Foto', 'Weg?',
            'Gezocht op', 'Naamtreffer', 'Bestand', 'Commons']
BREEDTES = [6, 12, 62, 10, 26, 8, 18, 12, 34, 12]


def main():
    import json
    hoofd = json.load(open(os.path.join(FOTOS, 'hoofdafbeeldingen.json'), encoding='utf-8'))
    onderwerp = json.load(open(os.path.join(FOTOS, 'onderwerpafbeeldingen.json'), encoding='utf-8'))
    met_infobox = {nr for nr, v in hoofd.items() if v.get('kandidaten')}

    blad = openpyxl.load_workbook(REVIEW, read_only=True)['Vragen']
    rijen = list(blad.iter_rows(values_only=True))
    k = {naam: n for n, naam in enumerate(rijen[0])}

    te_doen = []
    for r in rijen[1:]:
        if r[k['Nr']] is None:
            continue
        nr = str(int(r[k['Nr']]))
        gebruik = r[k['In gebruik']]
        if gebruik not in RANG or nr in met_infobox:
            continue
        kandidaat = (onderwerp.get(nr, {}).get('kandidaten') or [None])[0]
        if not kandidaat:
            continue
        # Sorteren op zichtbaarheid, en daarbinnen op de naamtreffer: klopt de
        # naam van het gevonden artikel met de vraag, dan is het voorstel
        # sterker. Zo staat het beste bovenaan en is een half nagelopen blad
        # nog steeds het meest bruikbare deel.
        te_doen.append((RANG[gebruik], 0 if kandidaat.get('naamtreffer') else 1,
                        int(nr), gebruik, str(r[k['Vraag NL']]),
                        r[k['Antwoord']], kandidaat))
    te_doen.sort()
    print(f'{len(te_doen)} voorstellen om na te lopen')

    boek = openpyxl.Workbook()
    ws = boek.active
    ws.title = 'Fotos'
    donker = PatternFill('solid', fgColor='1F3864')
    rood = PatternFill('solid', fgColor='FCE4E4')
    for n, (naam, breedte) in enumerate(zip(KOLOMMEN, BREEDTES), start=1):
        cel = ws.cell(1, n, naam)
        cel.font = Font(bold=True, color='FFFFFF')
        cel.fill = donker
        cel.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        ws.column_dimensions[get_column_letter(n)].width = breedte
    ws.row_dimensions[1].height = 28
    ws.freeze_panes = 'C2'

    meegenomen = 0
    for rij, (_, _, nr, gebruik, vraag, antwoord, kandidaat) in enumerate(te_doen, start=2):
        waarden = [nr, gebruik, vraag, antwoord, None, None,
                   kandidaat.get('gezocht', ''),
                   'ja' if kandidaat.get('naamtreffer') else 'nee',
                   kandidaat['titel'].replace('File:', ''), 'commons']
        for kol, waarde in enumerate(waarden, start=1):
            cel = ws.cell(rij, kol, waarde)
            cel.alignment = Alignment(vertical='center', wrap_text=(kol == 3))
            if KOLOMMEN[kol - 1] == 'Weg?':
                cel.fill = rood
            if KOLOMMEN[kol - 1] == 'Commons' and kandidaat.get('pagina'):
                cel.hyperlink = kandidaat['pagina']
                cel.font = Font(color='0563C1', underline='single')
        pad = os.path.join(MINIATUREN, f'{nr}_0.jpg')
        # Het keuzeblad haalt alleen miniaturen op voor daily- en puzzelvragen.
        # Race en breinkrakers staan hier ook in, dus die ontbreken nog. Een rij
        # zonder plaatje valt niet te beoordelen, dus die halen we alsnog.
        if not os.path.exists(pad) and kandidaat.get('miniatuur'):
            haal_miniatuur(kandidaat['miniatuur'], pad)
        if os.path.exists(pad):
            try:
                beeld = XlImage(pad)
                ws.add_image(beeld, f'E{rij}')
                meegenomen += 1
            except Exception:
                pass
        ws.row_dimensions[rij].height = 96

    ws.auto_filter.ref = f'A1:{get_column_letter(len(KOLOMMEN))}{ws.max_row}'

    voortgang = boek.create_sheet('Voortgang')
    voortgang['A1'] = 'Tot en met welke rij van het tabblad Fotos heb je gekeken?'
    voortgang['A1'].font = Font(bold=True)
    voortgang.column_dimensions['A'].width = 62
    voortgang['B1'] = 1
    voortgang['B1'].fill = PatternFill('solid', fgColor='FFF2CC')
    voortgang['A3'] = ('Alles tot en met dat rijnummer geldt als bekeken. Een lege "Weg?" '
                       'daarbinnen betekent goedgekeurd; daarbuiten betekent het nog niets.')
    voortgang['A4'] = 'Je hoeft niet in een keer klaar te zijn. Vul het getal in tot waar je kwam.'

    boek.save(UIT)
    print(f'{os.path.relpath(UIT, WORTEL)}: {len(te_doen)} rijen, {meegenomen} miniaturen, '
          f'{os.path.getsize(UIT) / 1024:.0f} KB')


if __name__ == '__main__':
    main()
