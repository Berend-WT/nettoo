# -*- coding: utf-8 -*-
"""Netto — zeef de vragen die in gebruik zijn op twijfelgevallen.

Draaien:  python tools/twijfelgevallen.py

WAAROM
Alle 1510 vragen nalopen is negentien uur werk; er zijn er maar 600 in gebruik
en de rest ziet niemand. Dit script haalt uit die 600 de gevallen waar iets aan
mankeert, zodat er alleen nog een oordeel over de rest hoeft.

De soorten twijfel zijn niet allemaal even erg, en dat is precies waarom ze
gescheiden blijven:

  zelfverklappend  Het antwoord staat in de vraag. "Taipei 101" heeft 101
                   verdiepingen; "de Twaalf Olympiërs" zijn er twaalf. Dat is
                   geen schatting maar leesvaardigheid.
  fout             De vraag klopt feitelijk niet of stelt iets onmogelijks.
  definitie        Het antwoord hangt af van wat je meetelt. Heeft een krab tien
                   poten of acht poten en twee scharen? Beide is verdedigbaar,
                   en dus is er geen goed antwoord.
  bronverschil     Serieuze bronnen geven verschillende getallen. De speler kan
                   het dan nooit "goed" hebben.
  veroudert        Het antwoord verandert vanzelf. Grammy's van Beyoncé,
                   filialen van Decathlon, tramlijnen in Amsterdam. Over een jaar
                   staat er een fout getal zonder dat iemand iets deed.
  geen schatting   Het antwoord is exact bekend of uit te rekenen. Een schrikkel-
                   jaar heeft 366 dagen; een gestrekte hoek is 180 graden. Er valt
                   niets te schatten, dus de vraag meet niets.
  paarlek          Twee vragen samen verklappen elkaar. Weet je dat 29% van het
                   aardoppervlak land is, dan weet je ook dat 71% water is.

De handmatige oordelen staan in HANDMATIG en zijn stuk voor stuk vastgesteld
door de vraag naast het antwoord te leggen. De regels eronder vangen de rest.
"""

import os
import re

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRON = os.path.join(os.path.expanduser('~'), 'OneDrive - Driestar-Wartburg',
                    'Kopie van vragen_review_compleet.xlsx')
TERUGVAL = os.path.join(WORTEL, 'vragen', 'vragen_review_compleet.xlsx')
DOEL = os.path.join(WORTEL, 'vragen', 'twijfelgevallen.xlsx')

FONT = 'Arial'


# --------------------------------------------------------------------------
# Handmatig vastgesteld, na de 105 daily-vragen naast hun antwoord te leggen.
# --------------------------------------------------------------------------

HANDMATIG = {
    17: ('zelfverklappend', 'De vraag noemt "de Twaalf Olympiërs"; het antwoord is 12.',
         'Herschrijf naar "Hoeveel hoofdgoden woonden er volgens de Griekse mythologie op de Olympus?"'),
    26: ('zelfverklappend', 'Het gebouw heet Taipei 101 en heeft 101 verdiepingen.',
         'Schrappen, of vervangen door de hoogte in meters (508).'),
    96: ('fout', 'Het wegdek van de Golden Gate Bridge ligt 67 m boven het water; 227 m is de '
                 'hoogte van de pylonen. De vraag en het antwoord gaan over verschillende dingen.',
         'Herschrijf naar "Hoeveel meter steken de pylonen van de Golden Gate Bridge boven het water uit?"'),
    10: ('definitie', 'Een krab heeft acht looppoten plus twee scharen. Tien is verdedigbaar, acht ook.',
         'Herschrijf naar "Hoeveel poten heeft een krab, de scharen meegerekend?"'),
    87: ('definitie', 'Het Thaise schrift heeft 44 medeklinkers en daarnaast klinkertekens. '
                      'Vraag 545 vraagt al expliciet naar de medeklinkers, met hetzelfde antwoord.',
         'Maak expliciet dat het om medeklinkers gaat, of schrap er één van de twee.'),
    24: ('bronverschil', 'Tot de 86e verdieping zijn het er ongeveer 1576, tot de 102e ongeveer 1872. '
                         'Het opgegeven antwoord 1860 hoort bij geen van beide.',
         'Vaststellen welk eindpunt bedoeld is en het antwoord daarop aanpassen.'),
    2: ('bronverschil', 'Schattingen lopen van 14.000 tot 19.000 knipperingen per dag.',
        'Schrappen; er is geen getal dat je fair kunt rekenen.'),
    7: ('bronverschil', 'Een koningspinguïn weegt 11 tot 16 kg, afhankelijk van seizoen en geslacht.',
        'Schrappen of omzetten naar de maximale massa.'),
    13: ('bronverschil', 'De Amerikaanse Big Mac staat nu op 590 kcal; 580 is een oudere waarde.',
         'Bijwerken naar 590 met de voedingswaardepagina van McDonald\'s als bron.'),
    9: ('bronverschil', 'Topsnelheden voor de tuimelaar lopen uiteen van 30 tot 40 km/u.',
        'Bron vastleggen en het antwoord daarop ijken.'),
    42: ('bronverschil', 'Welke telling "de eerste moderne volkstelling" is, verschilt per bron '
                         '(Nieuw-Frankrijk 1666, IJsland 1703, Zweden 1749).',
         'Schrappen; de vraag heeft geen onbetwist antwoord.'),
    50: ('bronverschil', 'Het Great Barrier Reef bestaat grotendeels uit rif; 7% is niet te herleiden.',
         'Nakijken wat hier eigenlijk gevraagd wordt.'),
    62: ('veroudert', 'De gemiddelde fietskilometers per Nederlander verschillen per jaar en per bron.',
         'Jaartal in de vraag zetten, of schrappen.'),
    47: ('veroudert', 'Het aantal Decathlon-filialen groeit; 1700 is een momentopname.',
         'Jaartal in de vraag zetten.'),
    55: ('veroudert', 'Grammy-aantallen veranderen elk jaar. De vraag noemt 2025, dus hij is '
                      'houdbaar tot de volgende uitreiking.',
         'Laten staan tot februari, dan bijwerken.'),
    63: ('veroudert', 'Het aantal tramlijnen in Amsterdam verandert bij elke dienstregeling.',
         'Jaartal in de vraag zetten, of schrappen.'),
    6: ('geen schatting', 'Een schrikkeljaar heeft 366 dagen. Dat weet je of je weet het niet; '
                          'schatten helpt niet.',
        'Schrappen uit de dailies; hooguit bruikbaar als opwarmer.'),
    54: ('geen schatting', 'Een gestrekte hoek is per definitie 180 graden.',
         'Schrappen.'),
    104: ('geen schatting', 'De som 1 tot en met 100 is een rekensom, geen schatting.',
          'Schrappen uit de dailies.'),
    105: ('geen schatting', 'Het aantal podiumindelingen is een rekensom (8 × 7 × 6).',
          'Schrappen uit de dailies.'),
    51: ('paarlek', 'Samen met vraag 52 (oceaanoppervlak) telt dit op tot 100%.',
         'Eén van de twee schrappen.'),
    52: ('paarlek', 'Samen met vraag 51 (landoppervlak) telt dit op tot 100%.',
         'Eén van de twee schrappen.'),
}


# --------------------------------------------------------------------------
# Regels voor de overige vragen.
# --------------------------------------------------------------------------

GETAL_WOORD = {
    'twee': 2, 'drie': 3, 'vier': 4, 'vijf': 5, 'zes': 6, 'zeven': 7, 'acht': 8,
    'negen': 9, 'tien': 10, 'elf': 11, 'twaalf': 12, 'dertien': 13, 'veertien': 14,
    'vijftien': 15, 'zestien': 16, 'twintig': 20, 'vijftig': 50, 'honderd': 100,
}

VEROUDERT = re.compile(
    r'\b(20[12]\d)\b|\bmomenteel\b|\bhuidige\b|\brecente cijfers\b|\btot en met\b|\bstand na\b',
    re.I)

# "Ongeveer" staat bewust NIET in deze regel. Netto is een schatspel: dat een
# antwoord bij benadering is, is het uitgangspunt en geen gebrek. Een eerdere
# versie van dit script vuurde daar wel op en leverde 78 valse treffers.
# Wat wél stoort:
#   "gemiddeld"  — een gemiddelde hangt af van de gekozen populatie en periode,
#                  dus twee eerlijke bronnen komen op verschillende getallen uit.
#   "afgerond op tientallen" — die formulering verraadt de orde van grootte en
#                  leest bovendien als machinetaal.
GEMIDDELDE = re.compile(r'\bgemiddeld\b', re.I)
AFRONDTAAL = re.compile(r'afgerond op|bij benadering|in tientallen|in honderdtallen', re.I)


def zelfverklappend(vraag, antwoord):
    """Staat het antwoord letterlijk of als telwoord in de vraag?"""
    try:
        a = int(float(antwoord))
    except (TypeError, ValueError):
        return None
    # Het getal zelf in de vraagtekst, als los woord.
    if re.search(rf'\b{a}\b', vraag):
        return f'Het getal {a} staat letterlijk in de vraag.'
    for woord, waarde in GETAL_WOORD.items():
        if waarde == a and re.search(rf'\b{woord}\b', vraag, re.I):
            return f'Het telwoord "{woord}" in de vraag is het antwoord.'
    return None


def beoordeel(rij):
    nr = int(rij['Nr'])
    if nr in HANDMATIG:
        return HANDMATIG[nr]
    vraag = str(rij['Vraag NL'])
    antwoord = rij['Antwoord']

    reden = zelfverklappend(vraag, antwoord)
    if reden:
        return ('zelfverklappend', reden, 'Herschrijven zodat het getal niet in de vraag staat.')
    if VEROUDERT.search(vraag):
        return ('veroudert', 'De vraag hangt aan een jaartal of een actuele stand.',
                'Controleren of het antwoord nog klopt; anders het jaartal vastzetten.')
    if AFRONDTAAL.search(vraag):
        return ('afrondtaal', 'De formulering verraadt de orde van grootte en leest als machinetaal.',
                'Herschrijven zonder "afgerond op ..."; het spel rondt zelf al af.')
    if GEMIDDELDE.search(vraag):
        return ('bronverschil', 'Een gemiddelde hangt af van de gekozen populatie en periode, '
                                'dus eerlijke bronnen komen op verschillende getallen uit.',
                'Bron vastleggen zodat één getal het juiste is.')
    return None


# --------------------------------------------------------------------------
# Fotogeschiktheid.
# --------------------------------------------------------------------------
# Een foto bij de daily mag het antwoord niet bevatten. Dat gaat mis bij
# telvragen: een foto van een krab laat je de poten tellen. Het gaat níét mis
# bij grootheden die je niet kunt zien — gewicht, hoogte in meters, een jaartal,
# calorieën — want daar geeft het beeld alleen sfeer.
#
# De grens ligt bij hoeveel er te tellen valt. "Hoeveel treden heeft de Burj
# Khalifa?" is 2909; die tel je op geen enkele foto. "Hoeveel poten heeft een
# krab?" is 10, en dat lukt in één blik.

TELBAAR_OP_BEELD = re.compile(
    r'\b(poten|vleugels|ogen|koppen|bulten|tentakels|armen|torens|minaretten|zuilen|'
    r'bogen|wielen|ringen|snaren|toetsen|strepen|sterren|kleuren|zijden|hoeken|'
    r'stippen|pionnen|damstenen|manen|schoorstenen|masten|rijstroken|'
    r'start- en landingsbanen|banen|terminals|motoren|hoofdeilanden|piramides|'
    r'wieken|beelden|leeuwen|sfinxen|kamers heeft het menselijk hart)\b', re.I)

# Kaartvragen zijn een eigen categorie: "hoeveel landen grenzen aan X" is op een
# kaartafbeelding gewoon af te tellen, ongeacht het antwoord.
KAARTVRAAG = re.compile(r'\blanden (grenzen|liggen|delen|vormen)\b', re.I)

MAX_TELBAAR = 20  # daarboven telt niemand het na op een foto


def fotogeschikt(vraag, antwoord):
    try:
        a = abs(int(float(antwoord)))
    except (TypeError, ValueError):
        return 'onbekend', 'Antwoord is geen getal.'
    if KAARTVRAAG.search(vraag):
        return 'nee', 'Kaartvraag: op een kaartafbeelding tel je de landen gewoon af.'
    if TELBAAR_OP_BEELD.search(vraag) and a <= MAX_TELBAAR:
        return 'nee', f'Telvraag met antwoord {a}: dat tel je zo van de foto af.'
    if TELBAAR_OP_BEELD.search(vraag):
        return 'ja', f'Telvraag, maar {a} is te veel om op een foto na te tellen.'
    return 'ja', 'Het antwoord is niet uit een foto af te lezen.'


def main():
    bron = BRON if os.path.exists(BRON) else TERUGVAL
    d = pd.read_excel(bron, sheet_name='Vragen')
    inuse = d[d['In gebruik'].astype(str).isin(['daily', 'puzzel'])].copy()

    rijen = []
    for _, r in inuse.iterrows():
        oordeel = beoordeel(r)
        if not oordeel:
            continue
        soort, waarom, voorstel = oordeel
        rijen.append({
            'Nr': int(r['Nr']),
            'In gebruik': r['In gebruik'],
            'Soort twijfel': soort,
            'Categorie': r['Categorie'],
            'Vraag NL': r['Vraag NL'],
            'Antwoord': r['Antwoord'],
            'Waarom': waarom,
            'Voorstel': voorstel,
            'Bron (bestaand)': r.get('Bron (bestaand)'),
            'Jouw besluit': None,
        })

    uit = pd.DataFrame(rijen)
    volgorde = ['fout', 'zelfverklappend', 'definitie', 'geen schatting',
                'paarlek', 'bronverschil', 'veroudert', 'afrondtaal']
    uit['_s'] = uit['Soort twijfel'].apply(volgorde.index)
    uit['_g'] = (uit['In gebruik'] != 'daily').astype(int)
    uit = uit.sort_values(['_g', '_s', 'Nr']).drop(columns=['_s', '_g'])

    # Tweede blad: welke daily-vragen veilig een foto kunnen krijgen.
    twijfel_nrs = set(uit['Nr'])
    foto = []
    for _, r in inuse[inuse['In gebruik'] == 'daily'].iterrows():
        kan, waarom = fotogeschikt(str(r['Vraag NL']), r['Antwoord'])
        foto.append({
            'Nr': int(r['Nr']),
            'Foto mogelijk': kan,
            'Waarom': waarom,
            'Ook twijfelgeval': 'ja' if int(r['Nr']) in twijfel_nrs else '',
            'Categorie': r['Categorie'],
            'Vraag NL': r['Vraag NL'],
            'Antwoord': r['Antwoord'],
            'Commons-link (door mij)': None,
        })
    fotos = pd.DataFrame(foto).sort_values(['Foto mogelijk', 'Nr'])

    with pd.ExcelWriter(DOEL, engine='openpyxl') as w:
        uit.to_excel(w, index=False, sheet_name='Twijfelgevallen')
        fotos.to_excel(w, index=False, sheet_name='Fotogeschiktheid')
    opmaak(DOEL, uit)

    kan = int((fotos['Foto mogelijk'] == 'ja').sum())
    geen = int((fotos['Foto mogelijk'] == 'nee').sum())
    print(f'\nfoto mogelijk : {kan} van de 105 dailies')
    print(f'foto verklapt : {geen}')
    for _, r in fotos[fotos['Foto mogelijk'] == 'nee'].iterrows():
        print(f"    {int(r['Nr']):4d}  {str(r['Vraag NL'])[:58]}")

    print(f'bron: {os.path.basename(bron)}')
    print(f'in gebruik: {len(inuse)}  ->  twijfelgevallen: {len(uit)}')
    print()
    for soort in volgorde:
        n = int((uit['Soort twijfel'] == soort).sum())
        nd = int(((uit['Soort twijfel'] == soort) & (uit['In gebruik'] == 'daily')).sum())
        print(f'  {soort:16s} {n:4d}   (waarvan daily: {nd})')
    print(f'\n-> {DOEL}')


def opmaak(pad, df):
    kleur = {
        'fout': 'F8CBCB', 'zelfverklappend': 'FBD9A5', 'definitie': 'FBE9A5',
        'geen schatting': 'DDE7F5', 'paarlek': 'E4DAF0',
        'bronverschil': 'E8E8E8', 'veroudert': 'DCEEDC', 'afrondtaal': 'F2E2D5',
    }
    wb = load_workbook(pad)
    ws = wb['Twijfelgevallen']
    breedtes = {'Nr': 6, 'In gebruik': 10, 'Soort twijfel': 17, 'Categorie': 24,
                'Vraag NL': 62, 'Antwoord': 10, 'Waarom': 66, 'Voorstel': 58,
                'Bron (bestaand)': 34, 'Jouw besluit': 20}
    for i, kol in enumerate(df.columns, start=1):
        ws.column_dimensions[get_column_letter(i)].width = breedtes.get(kol, 18)
        c = ws.cell(row=1, column=i)
        c.font = Font(name=FONT, bold=True, color='FFFFFF', size=11)
        c.fill = PatternFill('solid', fgColor='1F3864')
        c.alignment = Alignment(vertical='center', wrap_text=True)
    ws.row_dimensions[1].height = 28

    i_soort = list(df.columns).index('Soort twijfel') + 1
    for rij in range(2, ws.max_row + 1):
        soort = ws.cell(row=rij, column=i_soort).value
        for kol in range(1, len(df.columns) + 1):
            c = ws.cell(row=rij, column=kol)
            c.font = Font(name=FONT, size=10)
            c.alignment = Alignment(vertical='top', wrap_text=kol in (5, 7, 8))
        ws.cell(row=rij, column=i_soort).fill = PatternFill(
            'solid', fgColor=kleur.get(soort, 'FFFFFF'))
    ws.freeze_panes = 'C2'
    ws.auto_filter.ref = f'A1:{get_column_letter(len(df.columns))}{ws.max_row}'
    wb.save(pad)


if __name__ == '__main__':
    main()
