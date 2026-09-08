# -*- coding: utf-8 -*-
"""Netto — herstel binnen de groep met vertrouwen "hoog".

controleer_hoog_vertrouwen.py haalde 68 van de 685 bronnen naar boven waarvan
het adres geen enkel woord uit de vraag bevat. Verreweg de meeste daarvan zijn
ruis van die toets zelf: de vraag is Nederlands en het artikel Engels, dus
"Hoeveel poten heeft een krab" valt door de mand bij en.wikipedia.org/wiki/Crab
terwijl die bron gewoon deugt.

Wat overblijft is het volgende. Drie bronnen gaan echt over iets anders: de
eerste passagiersvlucht verwees naar de Eerste Wereldoorlog, de omzwervingen van
Odysseus naar de Alpenconventie, en de kleuren van een Rubiks kubus naar de
spelregels van Catan. Bij tien andere klopt het onderwerp wel, maar is de
bewijszin een toevalstreffer — bij de bogen van het Pont du Gard werd "ruim 6
meter breed" als bewijs voor zes bogen genomen, en bij het aantal vleugels van
een kever de regel "Last Updated: Sep 4, 2025".

Twee antwoorden houden een kanttekening: het aantal landen aan de Noordzee hangt
af van of Zweden meetelt, en de twee gigabytevragen zijn dubbel met elkaar.
"""

H = {
    100: ('bevestigd', 'https://en.wikipedia.org/wiki/St._Petersburg%E2%80%93Tampa_Airboat_Line',
          'De eerste lijnvlucht met betalende passagiers vertrok op 1 januari 1914. De oude '
          'bron was het artikel over de Eerste Wereldoorlog.'),
    166: ('bevestigd', 'https://en.wikipedia.org/wiki/Beetle',
          'Een kever heeft vier vleugels: twee dekschilden en daaronder twee vliesvleugels. '
          'De oude bewijszin was de datum waarop het artikel was bijgewerkt.'),
    219: ('bevestigd', 'https://en.wikipedia.org/wiki/Pont_du_Gard',
          'De onderste booglaag telt zes bogen. De oude bewijszin ging over de breedte van het '
          'onderste dek, niet over het aantal bogen.'),
    519: ('bevestigd', 'https://en.wikipedia.org/wiki/Ice_giant',
          'Uranus en Neptunus zijn de twee ijsreuzen. De oude bewijszin was "2 min read".'),
    543: ('bevestigd', 'https://en.wikipedia.org/wiki/Russian_alphabet',
          'Het Russische alfabet telt 33 letters. De oude bron rekende het harde en zachte '
          'teken er apart uit en kwam daardoor op 32.'),
    582: ('bevestigd', 'https://en.wikipedia.org/wiki/Wing',
          'Een passagiersvliegtuig heeft twee vleugels. De oude bewijszin was een menu-item.'),
    692: ('bevestigd', 'https://en.wikipedia.org/wiki/S%26P_500',
          'De index bevat vijfhonderd bedrijven; het staat in de naam.'),
    762: ('bevestigd', 'https://en.wikipedia.org/wiki/Odyssey',
          'Odysseus deed er tien jaar over om na de val van Troje thuis te komen. De oude bron '
          'was de website van de Alpenconventie.'),
    892: ('bevestigd', 'https://en.wikipedia.org/wiki/Libya',
          'Libie grenst aan Egypte, Soedan, Tsjaad, Niger, Algerije en Tunesie. De oude '
          'bewijszin ging over olie-export.'),
    914: ('natellen', 'https://en.wikipedia.org/wiki/North_Sea',
          'Zeven landen grenzen direct aan de Noordzee; met Zweden erbij, dat er via het '
          'Skagerrak aan ligt, worden het er acht. De vraag zegt "direct" en past daarmee '
          'eerder bij zeven.'),
    1326: ('bevestigd', 'https://en.wikipedia.org/wiki/Carbon-14',
           'Koolstof-14 heeft zes protonen en acht neutronen. De oude bewijszin was een '
           'isotoopverhouding.'),
    1335: ('bevestigd', 'https://en.wikipedia.org/wiki/Rubik%27s_Cube',
           'De kubus heeft zes kleuren, een per zijvlak. De oude bron waren de spelregels '
           'van Catan.'),
    1450: ('natellen', 'https://en.wikipedia.org/wiki/Latin_declension',
           'De traditionele indeling kent zes naamvallen; met de locativus erbij zeven. De '
           'oude bewijszin ging over literaire traditie.'),
    1457: ('fout', 'https://physics.nist.gov/cuu/Units/binary.html',
           'De vraag zegt "precies een gigabyte", en dan is het antwoord 1000 megabyte. De '
           '1024 hoort bij de gibibyte. Vraag 1458 stelt dezelfde vraag wel goed.'),
    1458: ('bevestigd', 'https://physics.nist.gov/cuu/Units/binary.html',
           'Volgens de binaire definitie zijn het er 1024. Deze vraag is correct gesteld; '
           'vraag 1457 vraagt hetzelfde zonder die voorwaarde.'),
    1270: ('veroudert', 'https://www.nato.int/cps/en/natohq/topics_52044.htm',
           'De NAVO telt 32 leden sinds Zweden in 2024 toetrad; dat kan opnieuw veranderen. '
           'Dubbel met vraag 428.'),
}
