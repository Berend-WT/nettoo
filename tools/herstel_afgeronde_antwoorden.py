# -*- coding: utf-8 -*-
"""Netto — vervang grof afgeronde antwoorden door het echte getal.

Draaien:  python tools/herstel_afgeronde_antwoorden.py [--schrijf]

WAAROM
Bij deze vijf vragen stond in het bronpaneel een ander getal dan het antwoord:
de yogales telde 100.984 deelnemers terwijl het spel 100.000 verwachtte. Voor
een speler leest dat als een spel dat zichzelf tegenspreekt.

"Afgerond op duizendtallen" in de bewijszin zetten lost dat niet op maar maakt
het erger: dan legt het spel uit dat het een wíllekeurig getal van je vraagt, en
wie het echte antwoord kent zit fout. Precies de reden waarom we eerder al een
stapel afrondvragen hebben geschrapt.

Het exacte getal is hier het betere antwoord. Dat een speler 100.984 niet raadt
geeft niet — het is een schatspel, en de spelingbalk in de race vangt dat op.

WAT NIET IS AANGERAAKT
Afronding die klopt blijft staan: tin smelt bij 231,9 graden en het antwoord 232
is gewoon juist. Hetzelfde voor de hoogste hond (111,8 -> 112) en de Petronas
(451,9 -> 452). Ook antwoorden die het midden van een genoemde reeks nemen —
een emoe wordt 150 tot 190 cm hoog en het antwoord is 170 — blijven zoals ze
zijn; daar staat "ongeveer" in de vraag of het is een spreiding in de natuur.
"""

import json
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

# nr: (nieuw antwoord, toelichting)
HERSTEL = {
    323: (338226, 'Er werden 338.226 militairen geevacueerd uit Duinkerke.'),
    383: (8095, 'De langste trouwjurksleep mat 8095 meter (Caroline Arts, Cyprus, 2021).'),
    448: (26090, 'De grootste kaas woog 26.090 kilo (Wisconsin, 1988).'),
    453: (100984, 'De grootste yogales telde 100.984 deelnemers (India, 2018).'),
    1313: (8957, 'Het grootste waterballonnengevecht telde 8957 deelnemers.'),
}


def main():
    schrijf = '--schrijf' in sys.argv
    d = pd.read_excel(REVIEW, sheet_name='Vragen')
    rijen = {int(r['Nr']): r for _, r in d.iterrows()}

    for nr, (nieuw, uitleg) in HERSTEL.items():
        r = rijen[nr]
        print(f"  {nr:5d} [{r['In gebruik']}] {r['Antwoord']} -> {nieuw}")
        print(f"        {str(r['Vraag NL'])[:66]}")

    if not schrijf:
        print('\n(proefdraai — voeg --schrijf toe om op te slaan)')
        return

    for pad in (REVIEW, BANK):
        shutil.copy2(pad, os.path.join(
            os.path.dirname(pad),
            f'_backup_afronding_{date.today():%Y-%m-%d}_{os.path.basename(pad)}'))
        boek = load_workbook(pad)
        for blad in boek.worksheets:
            kop = [c.value for c in blad[1]]
            if 'Vraag NL' not in kop or 'Antwoord' not in kop:
                continue
            i_v = kop.index('Vraag NL') + 1
            i_a = kop.index('Antwoord') + 1
            i_w = kop.index('Bewijszin') + 1 if 'Bewijszin' in kop else None
            i_l = kop.index('Let op') + 1 if 'Let op' in kop else None
            for rij in range(2, blad.max_row + 1):
                tekst = blad.cell(row=rij, column=i_v).value
                nr = next((n for n, r in rijen.items()
                           if str(r['Vraag NL']) == tekst), None)
                if nr not in HERSTEL:
                    continue
                nieuw, uitleg = HERSTEL[nr]
                was = blad.cell(row=rij, column=i_a).value
                blad.cell(row=rij, column=i_a).value = nieuw
                if i_w:
                    blad.cell(row=rij, column=i_w).value = uitleg
                if i_l:
                    blad.cell(row=rij, column=i_l).value = (
                        f'was {was}, grof afgerond terwijl de bron het exacte '
                        f'getal geeft')[:250]
        boek.save(pad)
        print(f'bijgewerkt: {os.path.basename(pad)}')


if __name__ == '__main__':
    main()
