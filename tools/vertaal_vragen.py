# -*- coding: utf-8 -*-
"""Netto — de Engelse vraagteksten opnieuw nalopen, in behapbare stukken.

Draaien:
    python tools/vertaal_vragen.py --uit 1        exporteer blok 1
    python tools/vertaal_vragen.py --in blok01.json    pas correcties toe
    python tools/vertaal_vragen.py --stand       hoeveel is er nagelopen

WAAROM DIT IN BLOKKEN GAAT
De Engelse vertaling is machinaal gemaakt en de kwaliteit wisselt. Een
steekproef van 35 gaf zes vertalingen die echt fout waren en zes die krom
liepen; op 1683 vragen zijn dat er een paar honderd. De systematische fouten
zijn er met patronen uit gehaald ("tientallen" dat "dozens" werd, kapotte
afrondingsinstructies, Amerikaanse naast Britse spelling), maar de rest is elke
keer iets anders: een omgedraaide betekenis, een verkeerd woord, een naam op de
verkeerde plek. Daar helpt geen patroon tegen; die moeten stuk voor stuk gelezen.

Vandaar blokken. Elk blok gaat als JSON de deur uit, wordt nagelopen, en komt
als JSON terug. Wat al nagelopen is staat in vertaald_nagelopen.json, zodat een
onderbroken ronde niet opnieuw hoeft te beginnen — en zodat achteraf te zien is
wat er wél en niet langs een mens is geweest.

WAT ER NIET GEBEURT
De Nederlandse vragen blijven ongemoeid. Dit raakt alleen de Engelse kant, dus
een fout hier kan het spel in het Nederlands niet breken.
"""

import argparse
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORTEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BESTAND = os.path.join(WORTEL, 'data', 'netto_translations_en.js')
STAND = os.path.join(WORTEL, 'vragen', 'vertaald_nagelopen.json')
BLOKKEN = os.path.join(WORTEL, 'vragen', 'vertaalblokken')
PER_BLOK = 120


def laad():
    tekst = open(BESTAND, encoding='utf-8').read()
    kop = tekst[:tekst.index('{')]
    staart = tekst[tekst.rindex('}') + 1:]
    return kop, json.loads(tekst[tekst.index('{'):tekst.rindex('}') + 1]), staart


def schrijf(kop, d, staart):
    with open(BESTAND, 'w', encoding='utf-8') as f:
        f.write(kop + json.dumps(d, ensure_ascii=False, indent=2) + staart)


def nagelopen():
    if not os.path.exists(STAND):
        return set()
    return set(json.load(open(STAND, encoding='utf-8')).get('nagelopen', []))


def bewaar_nagelopen(sleutels):
    os.makedirs(os.path.dirname(STAND), exist_ok=True)
    json.dump({'nagelopen': sorted(sleutels)},
              open(STAND, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def in_gebruik():
    """De vraagteksten die echt in een puzzel staan.

    Van de 1683 vertaalde vragen komen er 786 in geen enkele puzzel voor — oude
    vragen, varianten die het niet haalden, en 39 met een volgnummer ervoor
    ("1. Hoe hoog is de Euromast...") die nooit ergens op kunnen matchen. Een
    speler ziet er 897. Die gaan dus eerst; de rest is er nog steeds, maar
    niemand wacht erop.
    """
    import re as _re
    uit = set()
    for naam in ('netto_frontend_puzzles.js', 'netto_race_pool.js', 'netto_breinkrakers.js'):
        pad = os.path.join(WORTEL, 'data', naam)
        if not os.path.exists(pad):
            continue
        tekst = open(pad, encoding='utf-8').read()
        data = json.loads(_re.search(r'=\s*([\[{].*[\]}]);?\s*$', tekst, _re.S).group(1))
        groepen = data.values() if isinstance(data, dict) else [data]
        for groep in groepen:
            if not isinstance(groep, list):
                continue
            for p in groep:
                for i in (1, 2, 3, 4):
                    label = p.get(f'q{i}_label')
                    if label:
                        uit.add(label)
    return uit


def vragen(d):
    """Alleen de vraagteksten; interfaceteksten blijven buiten deze ronde.

    In gebruik eerst, want dat is wat een speler vandaag voor zijn neus krijgt.
    """
    alle = {nl: en for nl, en in d.items() if nl.strip().endswith('?')}
    gebruikt = in_gebruik()
    return dict(sorted(alle.items(), key=lambda kv: (kv[0] not in gebruikt, kv[0])))


def main():
    o = argparse.ArgumentParser()
    o.add_argument('--uit', type=int, help='exporteer blok N')
    o.add_argument('--in', dest='invoer', help='pas een nagelopen blok toe')
    o.add_argument('--stand', action='store_true')
    o.add_argument('--klaar', help='markeer alle vragen uit dit blok als nagelopen')
    a = o.parse_args()

    _, d, _ = laad()
    alle = vragen(d)
    klaar = nagelopen()
    open_nog = [nl for nl in alle if nl not in klaar]   # volgorde uit vragen()

    if a.stand or not (a.uit or a.invoer or a.klaar):
        print(f'{len(alle)} vraagteksten')
        print(f'{len(klaar)} nagelopen, {len(open_nog)} te gaan')
        if open_nog:
            print(f'{(len(open_nog) + PER_BLOK - 1) // PER_BLOK} blokken van {PER_BLOK} te gaan')
        return

    if a.uit:
        os.makedirs(BLOKKEN, exist_ok=True)
        deel = open_nog[:PER_BLOK]
        pad = os.path.join(BLOKKEN, f'blok{a.uit:02d}.json')
        json.dump([{'nl': nl, 'en': alle[nl]} for nl in deel],
                  open(pad, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f'{len(deel)} vragen -> {os.path.relpath(pad, WORTEL)}')
        return

    # Een blok afvinken zonder correcties: de meeste vertalingen zijn goed, en
    # die hoeven niet woord voor woord teruggestuurd om als gelezen te tellen.
    if a.klaar:
        blok = json.load(open(a.klaar, encoding='utf-8'))
        for regel in blok:
            klaar.add(regel['nl'])
        bewaar_nagelopen(klaar)
        print(f'{len(blok)} vragen afgevinkt; {len(klaar)} van de {len(alle)} nagelopen')
        return

    # Terug: een lijst {nl, en}. Alleen en wordt overgenomen; nl is de sleutel
    # en die moet bestaan, anders is er iets misgegaan bij het bewerken.
    kop, d, staart = laad()
    binnen = json.load(open(a.invoer, encoding='utf-8'))
    gewijzigd, gelijk, onbekend = 0, 0, []
    for regel in binnen:
        nl, en = regel['nl'], regel['en']
        if nl not in d:
            onbekend.append(nl)
            continue
        if d[nl] != en:
            d[nl] = en
            gewijzigd += 1
        else:
            gelijk += 1
        klaar.add(nl)
    schrijf(kop, d, staart)
    bewaar_nagelopen(klaar)
    print(f'{gewijzigd} vertalingen vervangen, {gelijk} ongewijzigd gelaten')
    if onbekend:
        print(f'{len(onbekend)} sleutels niet gevonden:')
        for nl in onbekend[:5]:
            print('   ', nl)
    print(f'{len(klaar)} van de {len(alle)} vraagteksten nagelopen')


if __name__ == '__main__':
    main()
