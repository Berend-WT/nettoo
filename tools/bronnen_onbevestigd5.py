# -*- coding: utf-8 -*-
"""Netto — handmatige herbeoordeling van onbevestigde bronnen, blok 5.

Taal, technologie, vervoer en wiskunde. Laatste blok.

De wiskundevragen zijn het duidelijkste voorbeeld van het bronprobleem in deze
groep: het aantal graden in een cirkel verwees naar een museumpagina over de
David, het aantal uren in een jaar naar de val van de Berlijnse Muur. Zulke
antwoorden volgen uit een definitie of een berekening en hebben geen vindplaats
nodig — maar dan moet er ook geen willekeurige vindplaats bij staan.
"""

O5 = {
    # ================= Taal =================
    85: ('bevestigd', 'https://en.wikipedia.org/wiki/Armenian_alphabet',
         'Het Armeense alfabet telt sinds de veertiende eeuw 38 of 39 letters; 39 met de '
         'toegevoegde letter o.'),
    87: ('bevestigd', 'https://en.wikipedia.org/wiki/Thai_script',
         'Het Thaise schrift telt 44 medeklinkertekens.'),
    89: ('bevestigd', 'https://en.wikipedia.org/wiki/Finnish_language',
         'Het Fins kent vijftien naamvallen.'),
    322: ('bevestigd', 'https://en.wikipedia.org/wiki/Latin_alphabet',
          'Het moderne Latijnse alfabet telt 26 letters. De oude bron ging over de zeven '
          'wereldwonderen.'),
    538: ('bevestigd', 'https://en.wikipedia.org/wiki/.com',
          'De extensie .com bestaat uit drie letters.'),
    539: ('bevestigd', 'https://en.wikipedia.org/wiki/Latin_alphabet',
          'Het klassieke Latijnse alfabet telde 23 letters; J, U en W kwamen later.'),
    545: ('bevestigd', 'https://en.wikipedia.org/wiki/Thai_script',
          'Vierenveertig medeklinkertekens. Dubbel met vraag 87, die hetzelfde vraagt in '
          'andere bewoording.'),
    1446: ('bevestigd', 'https://en.wikipedia.org/wiki/Hangul',
           'Het moderne Hangul kent 24 basisjamo: veertien medeklinkers en tien klinkers.'),
    1449: ('bevestigd', 'https://en.wikipedia.org/wiki/German_declension',
           'Het Duits kent vier naamvallen: nominatief, genitief, datief en accusatief.'),

    # ================= Technologie =================
    93: ('fout', 'https://en.wikipedia.org/wiki/History_of_the_telephone',
         'De eerste internationale telefoonverbinding kwam in 1891 tot stand tussen Londen en '
         'Parijs; Parijs en Brussel waren al in 1887 verbonden. Het opgegeven 1892 hoort bij '
         'de binnenlandse lijn New York-Chicago.'),
    555: ('bevestigd', 'https://en.wikipedia.org/wiki/Barcode',
          'De eerste barcode werd op 26 juni 1974 gescand in een supermarkt in Troy, Ohio.'),
    556: ('natellen', 'https://en.wikipedia.org/wiki/History_of_photography',
          'Niepce maakte in 1816 zijn eerste camerabeelden, maar wat "de eerste camera" is '
          'hangt af van de definitie; de camera obscura is veel ouder.'),
    560: ('natellen', 'https://en.wikipedia.org/wiki/History_of_radio',
          'Fessenden zond in 1906 uit, maar of dat de eerste radio-uitzending was is betwist.'),
    1475: ('bevestigd', 'https://en.wikipedia.org/wiki/Computer_mouse',
           'Douglas Engelbart ontwierp de eerste muis in 1964.'),
    1481: ('bevestigd', 'https://en.wikipedia.org/wiki/1080p',
           'Full HD is 1920 bij 1080, samen 2.073.600 beeldpunten: 2074 duizend.'),

    # ================= Vervoer =================
    97: ('veroudert', 'https://en.wikipedia.org/wiki/Paris_M%C3%A9tro',
         'De Parijse metro telt ruim driehonderd stations; het net wordt uitgebreid.'),
    227: ('natellen', 'https://en.wikipedia.org/wiki/RMS_Titanic',
          'De drie miljoen klinknagels is een gangbare schatting, geen telling. De oude bron '
          'verwees naar een UNESCO-werelderfgoedlijst.'),
    572: ('bevestigd', 'https://en.wikipedia.org/wiki/TGV',
          'De TGV rijdt in reguliere dienst maximaal 320 kilometer per uur.'),
    585: ('bevestigd', 'https://en.wikipedia.org/wiki/Formula_One_car',
          'Een Formule 1-auto heeft vier wielen.'),
    588: ('bevestigd', 'https://en.wikipedia.org/wiki/Auto_rickshaw',
          'Een tuk-tuk heeft doorgaans drie wielen.'),
    589: ('bevestigd', 'https://en.wikipedia.org/wiki/Benz_Patent-Motorwagen',
          'Karl Benz reed in 1886 met de eerste auto met verbrandingsmotor.'),
    590: ('natellen', 'https://en.wikipedia.org/wiki/Nautilus_(1800_submarine)',
          'Fultons Nautilus voer in 1800, maar "eerste moderne onderzeeer" is geen vastgelegde '
          'categorie.'),
    591: ('bevestigd', 'https://en.wikipedia.org/wiki/USS_Nautilus_(SSN-571)',
          'De USS Nautilus voer in januari 1955 voor het eerst op kernkracht uit.'),
    1492: ('veroudert', 'https://en.wikipedia.org/wiki/List_of_largest_container_ships',
           'De grootste containerschepen zitten rond de 24.000 TEU; er komen grotere bij.'),
    1494: ('natellen', 'https://en.wikipedia.org/wiki/Transportation_in_New_York_City',
           'New York heeft rond de dertienduizend verkeerslichten; het exacte getal wisselt.'),
    1495: ('bevestigd', 'https://en.wikipedia.org/wiki/Bogie',
           'Drie draaistellen van twee assen geven zes assen en dus twaalf wielen.'),
    1496: ('bevestigd', 'https://en.wikipedia.org/wiki/Car',
           'Een standaard personenauto heeft vier wielen.'),
    1497: ('natellen', 'https://en.wikipedia.org/wiki/Double-decker_bus',
           'Een tweeassige dubbeldekker heeft zes wielen: twee voor en vier achter. Bij drie '
           'assen worden het er acht.'),
    1498: ('natellen', 'https://en.wikipedia.org/wiki/Transit_bus',
           'Een tweeassige stadsbus heeft zes wielen; gelede bussen hebben er meer.'),
    1499: ('bevestigd', 'https://en.wikipedia.org/wiki/Tram',
           'Vier assen geven acht wielen.'),
    1502: ('bevestigd', 'https://en.wikipedia.org/wiki/Shinkansen',
           'De Tokaido-Shinkansen begon op 1 oktober 1964 met commerciele dienst.'),

    # ================= Wiskunde =================
    102: ('bevestigd', 'https://en.wikipedia.org/wiki/Diagonal',
          'Een n-hoek heeft n(n-3)/2 diagonalen; voor tien is dat 35.'),
    103: ('bevestigd', 'https://en.wikipedia.org/wiki/Diagonal',
          'Twintig maal zeventien gedeeld door twee is 170.'),
    350: ('bevestigd', 'https://en.wikipedia.org/wiki/Degree_(angle)',
          'Een volledige cirkel meet per definitie 360 graden. De oude bron verwees naar een '
          'museumpagina over de David.'),
    594: ('bevestigd', 'https://en.wikipedia.org/wiki/Power_set',
          'Een verzameling met n elementen heeft 2^n deelverzamelingen; 2^8 is 256.'),
    596: ('bevestigd', 'https://en.wikipedia.org/wiki/Dice',
          'Zes mogelijkheden per dobbelsteen, drie dobbelstenen: 6^3 is 216.'),
    598: ('natellen', 'https://en.wikipedia.org/wiki/Dice',
          'Elf verschillende sommen, van twee tot twaalf. Als "uitkomst" het ogenpaar betekent '
          'zijn het er 36; de vraag moet zeggen welke van de twee bedoeld is.'),
    600: ('bevestigd', 'https://en.wikipedia.org/wiki/Octagon',
          'Een achthoek heeft acht zijden; het staat in de naam. De oude bron was een '
          'energiestatistiek.'),
    1023: ('bevestigd', 'https://en.wikipedia.org/wiki/Year',
           '365 dagen maal 24 uur is 8760. De oude bron ging over de val van de Berlijnse Muur.'),
    1061: ('bevestigd', 'https://en.wikipedia.org/wiki/Right_angle',
           'Een rechte hoek is per definitie negentig graden.'),
    1509: ('bevestigd', 'https://en.wikipedia.org/wiki/Divisor',
           '720 is 2^4 maal 3^2 maal 5; het aantal delers is 5 maal 3 maal 2 is 30.'),
    1510: ('bevestigd', 'https://en.wikipedia.org/wiki/Minute',
           'Een minuut telt per definitie zestig seconden.'),
}
