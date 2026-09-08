# -*- coding: utf-8 -*-
"""Netto — vervang bronnen die naar de verkeerde pagina wijzen.

Draaien:  python tools/herstel_verkeerde_bronpaginas.py [--schrijf]

HOE DEZE ZIJN GEVONDEN
De eerdere screening keek of het adres nog enig woord uit de vraag bevatte. Dat
mist het geval waarin het woord er wel in staat maar de pagina toch verkeerd is:
"Hoeveel wielen heeft een Boeing 747" wees naar het artikel over het bedrijf
Boeing, en de bewijszin was "de kosten van de 737 MAX liepen op tot US$ 18
miljard" — het antwoord 18, maar dan als geldbedrag.

Deze ronde toetst iets anders: staat het antwoord überhaupt in de bewijszin? Bij
22 van de 662 bronnen met vertrouwen "hoog" niet. Daar bovenop kwamen zes
gevallen waarin het getal in de bewijszin een geldbedrag of jaartal bleek.

Van die 28 hadden er negen een echt verkeerde pagina, waaronder drie
doorverwijspagina's: "Hoeveel landen grenzen aan Chili" wees naar het Engelse
artikel over chilipeper, "Hoeveel manen heeft Mars" naar de doorverwijspagina
voor het woord Mars, en de Chinese dierenriem naar het artikel over schorpioenen.

De overige negentien houden hun bron — die klopt — maar krijgen een bewijszin
die wel iets zegt. Antwoorden veranderen niet, dus er breekt geen enkele som.
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
BANK = os.path.join(WORTEL, 'vragen', '1000+ vragen netjes gecategoriseerd.xlsx')

# nr: (nieuwe bron, bewijszin)
VERVANG = {
    139: ('https://nl.wikipedia.org/wiki/Mars_(planeet)',
          'Mars heeft twee manen, Phobos en Deimos. De oude bron was de doorverwijspagina '
          'voor het woord Mars.'),
    292: ('https://nl.wikipedia.org/wiki/Zwitserland',
          'Zwitserland heeft vier landstalen: Duits, Frans, Italiaans en Reto-Romaans. De oude '
          'bron was HC Klein Zwitserland, een hockeyclub.'),
    348: ('https://ich.unesco.org/en/intangible-heritage-domains-00052',
          'UNESCO onderscheidt vijf domeinen van immaterieel erfgoed. De oude bron was het '
          'algemene artikel over UNESCO.'),
    388: ('https://en.wikipedia.org/wiki/Un_Verano_Sin_Ti',
          'Het album telt 23 nummers. De oude bron was het artikel over Bad Bunny zelf, met '
          'een zin over een tournee uit 2025.'),
    584: ('https://nl.wikipedia.org/wiki/Boeing_747',
          'De 747 staat op achttien wielen: vier hoofdstellen van vier plus een neuswiel van '
          'twee. De oude bron was het artikel over het bedrijf Boeing, en het getang 18 kwam '
          'daar uit een bedrag van 18 miljard dollar.'),
    673: ('https://nl.wikipedia.org/wiki/Chinese_astrologie',
          'De Chinese dierenriem telt twaalf dieren. De oude bron ging over schorpioenen.'),
    877: ('https://en.wikipedia.org/wiki/Chile',
          'Chili grenst aan Peru, Bolivia en Argentinie. De oude bron was de Engelse '
          'doorverwijspagina voor chilipeper.'),
    1158: ('https://nl.wikipedia.org/wiki/Nederlands_Film_Festival',
           'Het festival duurt tien dagen. De oude bron was het artikel over de stad Utrecht.'),
    1348: ('https://nl.wikipedia.org/wiki/Olympische_Zomerspelen_2024',
           'Australie won achttien gouden medailles in Parijs. De oude bron was het algemene '
           'artikel over de Zomerspelen.'),
}

# nr: bewijszin — bron klopt, alleen de onderbouwing deugde niet
BEWIJS = {
    23: 'De trap telt 1776 treden naar het LookOut-niveau en 2579 naar de SkyPod.',
    32: 'Zwitserland grenst aan Duitsland, Frankrijk, Italie, Oostenrijk en Liechtenstein.',
    56: 'Een octaaf is verdeeld in twaalf halve tonen.',
    99: 'De A380 staat op 22 wielen: twintig onder de hoofdstellen en twee onder de neus.',
    293: 'China houdt sinds 1949 een enkele tijdzone aan voor het hele land.',
    347: 'Het middenveld van het plafond toont negen scenes uit Genesis.',
    743: 'Breaking Bad telt vijf seizoenen.',
    832: 'De officiele meting uit 2012 komt op 21.196 kilometer. Dubbel met 779 en 858.',
    860: 'De infobox geeft een lengte van 4700 kilometer.',
    999: 'De oorlog duurde van 1618 tot 1648, dertig jaar; het staat in de naam.',
    1139: 'De meter is sinds 1983 gedefinieerd via een lichtsnelheid van exact 299.792.458 m/s.',
    1342: 'AC Milan won de Europacup I en Champions League zeven keer.',
    1343: 'Real Madrid won de Champions League vijftien keer.',
}


def main():
    schrijf = '--schrijf' in sys.argv
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    tekst_van = {int(r['Nr']): str(r['Vraag NL']) for _, r in d.iterrows()}

    print(f'bron vervangen: {len(VERVANG)}')
    for nr in sorted(VERVANG):
        print(f'  {nr:5d}  {tekst_van[nr][:56]}')
    print(f'\nalleen bewijszin bijgewerkt: {len(BEWIJS)}')

    if not schrijf:
        print('\n(proefdraai — voeg --schrijf toe om op te slaan)')
        return

    for pad in (REVIEW, BANK):
        shutil.copy2(pad, os.path.join(
            os.path.dirname(pad),
            f'_backup_bronpagina_{date.today():%Y-%m-%d}_{os.path.basename(pad)}'))
        boek = load_workbook(pad)
        for blad in boek.worksheets:
            kop = [c.value for c in blad[1]]
            if 'Vraag NL' not in kop:
                continue
            i_v = kop.index('Vraag NL') + 1
            kolommen = {n: kop.index(n) + 1 for n in
                        ('Bron EN', 'Bron (geverifieerd)', 'Bewijszin', 'Vertrouwen bron')
                        if n in kop}
            for rij in range(2, blad.max_row + 1):
                tekst = blad.cell(row=rij, column=i_v).value
                nr = next((n for n, t in tekst_van.items() if t == tekst), None)
                if nr in VERVANG:
                    bron, bewijs = VERVANG[nr]
                    for naam, waarde in (('Bron EN', bron), ('Bron (geverifieerd)', bron),
                                         ('Bewijszin', bewijs), ('Vertrouwen bron', 'handmatig')):
                        if naam in kolommen:
                            blad.cell(row=rij, column=kolommen[naam]).value = waarde
                elif nr in BEWIJS:
                    for naam, waarde in (('Bewijszin', BEWIJS[nr]),
                                         ('Vertrouwen bron', 'handmatig')):
                        if naam in kolommen:
                            blad.cell(row=rij, column=kolommen[naam]).value = waarde
        boek.save(pad)
        print(f'bijgewerkt: {os.path.basename(pad)}')


if __name__ == '__main__':
    main()
