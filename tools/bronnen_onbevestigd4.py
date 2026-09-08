# -*- coding: utf-8 -*-
"""Netto — handmatige herbeoordeling van onbevestigde bronnen, blok 4.

Muziek tot en met sterrenkunde. Vervolg op blok 3.

De sterrenkundevragen wijzen bijna allemaal naar de juiste NASA-feitenpagina.
Die pagina's zetten hun getallen alleen in een tabelwidget die door een script
wordt opgebouwd, waardoor een gewone ophaalpoging de cijfers niet ziet. De bron
deugt dus; alleen de controle erop kon niet automatisch. Waar het getal
vaststaat is er een tweede, wel leesbare bron bij gezet.
"""

O4 = {
    # ================= Muziek =================
    57: ('bevestigd', 'https://en.wikipedia.org/wiki/Musical_keyboard',
         'Vijf octaven van twaalf halve tonen plus de afsluitende toets geven 61 toetsen.'),
    140: ('bevestigd', 'https://en.wikipedia.org/wiki/Pedal_harp',
          'Een concertpedaalharp heeft 47 snaren. De oude bron ging over de Divina Commedia.'),
    393: ('bevestigd', 'https://en.wikipedia.org/wiki/Violin',
          'Een viool heeft vier snaren: G, D, A en E.'),
    625: ('bevestigd', 'https://en.wikipedia.org/wiki/Acoustic_guitar',
          'Een standaard akoestische gitaar heeft zes snaren. De oude bron ging over haiku.'),
    1111: ('bevestigd', 'https://en.wikipedia.org/wiki/Staff_(music)',
           'Een notenbalk heeft vijf lijnen en vier tussenruimtes.'),
    1126: ('bevestigd', 'https://en.wikipedia.org/wiki/Bass_guitar',
           'Een standaard basgitaar heeft vier snaren: E, A, D en G.'),

    # ================= Natuurkunde =================
    409: ('bevestigd', 'https://en.wikipedia.org/wiki/Speed_of_light',
          'De lichtsnelheid is exact 299.792,458 km/s, afgerond driehonderdduizend.'),
    1135: ('bevestigd', 'https://en.wikipedia.org/wiki/Lightning',
           'De lucht in een bliksemkanaal loopt op tot ongeveer 30.000 graden Celsius.'),
    1142: ('bevestigd', 'https://en.wikipedia.org/wiki/Speed_of_light',
           'Afgerond driehonderdduizend kilometer per seconde. Dubbel met vraag 409.'),

    # ================= Politiek en recht =================
    427: ('bevestigd', 'https://en.wikipedia.org/wiki/United_Nations_Security_Council',
          'China, Frankrijk, Rusland, het Verenigd Koninkrijk en de Verenigde Staten.'),

    # ================= Reizen en toerisme =================
    459: ('bevestigd', 'https://en.wikipedia.org/wiki/Disney_Experiences',
          'Er zijn zes resorts: Anaheim, Orlando, Tokio, Parijs, Hongkong en Shanghai.'),
    1317: ('veroudert', 'https://en.wikipedia.org/wiki/Hartsfield%E2%80%93Jackson_Atlanta_International_Airport',
           'Atlanta verwerkte ruim honderd miljoen passagiers; het cijfer verschilt per jaar.'),

    # ================= Scheikunde =================
    460: ('bevestigd', 'https://en.wikipedia.org/wiki/Properties_of_water',
          'H2O bestaat uit twee waterstofatomen en een zuurstofatoom: drie atomen.'),
    464: ('bevestigd', 'https://en.wikipedia.org/wiki/Sodium_bicarbonate',
          'NaHCO3 bevat vier elementen: natrium, waterstof, koolstof en zuurstof.'),
    465: ('bevestigd', 'https://en.wikipedia.org/wiki/Sodium_chloride',
          'NaCl bevat twee elementen: natrium en chloor.'),
    467: ('bevestigd', 'https://en.wikipedia.org/wiki/Aluminium',
          'Aluminium smelt bij 660,3 graden Celsius.'),
    468: ('bevestigd', 'https://en.wikipedia.org/wiki/Tin',
          'Tin smelt bij 231,9 graden Celsius.'),
    1318: ('bevestigd', 'https://en.wikipedia.org/wiki/Methane',
           'CH4 bestaat uit een koolstofatoom en vier waterstofatomen: vijf atomen.'),
    1319: ('bevestigd', 'https://en.wikipedia.org/wiki/Sodium_bicarbonate',
           'Azijnzuur en natriumbicarbonaat geven koolstofdioxide, water en natriumacetaat.'),
    1325: ('bevestigd', 'https://www.usgs.gov/special-topics/water-science-school/science/ph-and-water',
           'De pH-schaal is logaritmisch; twee stappen betekent een factor honderd.'),

    # ================= Spellen en speelgoed =================
    488: ('bevestigd', 'https://en.wikipedia.org/wiki/Dominoes',
          'Een dubbel-zes set van 28 stenen draagt in totaal 168 ogen.'),
    1336: ('veroudert', 'https://en.wikipedia.org/wiki/Lego',
           'Het totaal aantal geproduceerde steentjes groeit doorlopend. De oude bron verwees '
           'naar een UNESCO-werelderfgoedlijst.'),
    1337: ('bevestigd', 'https://en.wikipedia.org/wiki/Rules_of_chess',
           'Elke speler begint met acht pionnen. De oude bron verwees naar een Jenga-spel.'),

    # ================= Sport =================
    496: ('bevestigd', 'https://en.wikipedia.org/wiki/110_metres_hurdles',
          'De olympische hordensprint voor mannen gaat over 110 meter.'),
    498: ('bevestigd', 'https://en.wikipedia.org/wiki/Basketball',
          'Een NBA-wedstrijd bestaat uit vier kwarten van twaalf minuten: 48 minuten.'),
    500: ('bevestigd', 'https://en.wikipedia.org/wiki/Free_throw',
          'Een rake vrije worp levert een punt op.'),
    502: ('bevestigd', 'https://en.wikipedia.org/wiki/Handball',
          'Elk team heeft zeven spelers op het veld: zes veldspelers en een keeper.'),
    504: ('bevestigd', 'https://en.wikipedia.org/wiki/Basketball',
          'Vijf spelers per team, samen tien op het veld.'),
    1350: ('natellen', 'https://en.wikipedia.org/wiki/Miniature_golf',
           'Achttien holes is de gangbare baanlengte, maar geen voorschrift.'),
    1390: ('bevestigd', 'https://en.wikipedia.org/wiki/Rugby_union',
           'Een wedstrijd duurt tweemaal veertig minuten.'),
    1391: ('bevestigd', 'https://en.wikipedia.org/wiki/Ice_hockey',
           'Een wedstrijd bestaat uit drie periodes van twintig minuten.'),
    1401: ('bevestigd', 'https://en.wikipedia.org/wiki/Association_football',
           'Twee helften van 45 minuten, samen negentig.'),
    1406: ('bevestigd', 'https://en.wikipedia.org/wiki/Ice_hockey',
           'Zes spelers per team inclusief keeper, samen twaalf op het ijs.'),
    1407: ('bevestigd', 'https://en.wikipedia.org/wiki/Basketball',
           'Vijf spelers per team tegelijk op het veld. Dubbel met vraag 504.'),
    1409: ('bevestigd', 'https://en.wikipedia.org/wiki/Volleyball',
           'Zes spelers per team op het veld.'),
    1410: ('bevestigd', 'https://en.wikipedia.org/wiki/Association_football',
           'Elf spelers per team, samen tweeentwintig.'),
    1415: ('bevestigd', 'https://en.wikipedia.org/wiki/Water_polo',
           'Zeven spelers per team in het water: zes veldspelers en een keeper.'),
    1416: ('bevestigd', 'https://en.wikipedia.org/wiki/Marathon',
           'De marathonafstand is sinds 1921 vastgelegd op 42,195 kilometer.'),
    1418: ('bevestigd', 'https://en.wikipedia.org/wiki/Ten-pin_bowling',
           'Twaalf strikes op rij geven de maximale score van 300.'),

    # ================= Sterrenkunde en ruimte =================
    84: ('bevestigd', 'https://en.wikipedia.org/wiki/Age_of_the_Earth',
         'De aarde is ongeveer 4,54 miljard jaar oud, oftewel 4540 miljoen.'),
    349: ('natellen', 'https://science.nasa.gov/dwarf-planets/',
          'NASA noemt er vijf: Pluto, Ceres, Makemake, Haumea en Eris. Het aantal erkende '
          'dwergplaneten kan groeien. De oude bron verwees naar de Sixtijnse Kapel.'),
    508: ('bevestigd', 'https://en.wikipedia.org/wiki/Sun',
          'Het volume van de zon is ongeveer 1,3 miljoen keer dat van de aarde. De oude bron '
          'verwees naar een UNESCO-werelderfgoedlijst.'),
    514: ('veroudert', 'https://en.wikipedia.org/wiki/Moons_of_Saturn',
          'Saturnus stond op 146 bevestigde manen; er komen er regelmatig bij.'),
    515: ('veroudert', 'https://en.wikipedia.org/wiki/Moons_of_Jupiter',
          'Jupiter stond op 95 bevestigde manen; er komen er regelmatig bij.'),
    516: ('veroudert', 'https://en.wikipedia.org/wiki/Moons_of_Saturn',
          'Zelfde als vraag 514; dubbel in de bank.'),
    520: ('bevestigd', 'https://en.wikipedia.org/wiki/International_Space_Station',
          'Aan boord ligt ongeveer dertien kilometer bekabeling. De oude bron verwees naar een '
          'veilingverslag van Christie\'s.'),
    521: ('bevestigd', 'https://en.wikipedia.org/wiki/Mars',
          'Mars staat gemiddeld ongeveer 228 miljoen kilometer van de zon.'),
    522: ('bevestigd', 'https://en.wikipedia.org/wiki/Neptune',
          'Neptunus staat gemiddeld ongeveer 4,5 miljard kilometer van de zon.'),
    525: ('bevestigd', 'https://en.wikipedia.org/wiki/Light-year',
          'Een lichtjaar is 9,4607 biljoen kilometer, oftewel 9460 miljard. De oude bron '
          'verwees naar een UNESCO-werelderfgoedlijst.'),
    530: ('bevestigd', 'https://en.wikipedia.org/wiki/Apollo_11',
          'De missie duurde 195 uur en 18 minuten.'),
    536: ('bevestigd', 'https://en.wikipedia.org/wiki/Astronomical_unit',
          'De astronomische eenheid is ongeveer 150 miljoen kilometer.'),
    1423: ('veroudert', 'https://en.wikipedia.org/wiki/Moons_of_Jupiter',
           'Zelfde als vraag 515; dubbel in de bank.'),
    1426: ('bevestigd', 'https://en.wikipedia.org/wiki/Jupiter',
           'De equatoriale diameter van Jupiter is 139.820 kilometer.'),
    1428: ('bevestigd', 'https://en.wikipedia.org/wiki/Sun',
           'De diameter van de zon is ongeveer 1.392.700 kilometer.'),
    1429: ('bevestigd', 'https://en.wikipedia.org/wiki/Jupiter',
           'Jupiter staat gemiddeld ongeveer 778 miljoen kilometer van de zon.'),
    1437: ('bevestigd', 'https://en.wikipedia.org/wiki/Salyut_1',
           'Saljoet 1 werd op 19 april 1971 gelanceerd. De oude bron ging over Skylab, dat pas '
           'in 1973 volgde.'),
    1439: ('bevestigd', 'https://en.wikipedia.org/wiki/International_Space_Station',
           'Het ISS draait met ongeveer 27.600 kilometer per uur om de aarde.'),
    1440: ('bevestigd', 'https://en.wikipedia.org/wiki/International_Space_Station',
           'Zelfde als vraag 1439; dubbel in de bank.'),
    1442: ('bevestigd', 'https://en.wikipedia.org/wiki/Moon',
           'De maan heeft een diameter van 3474 kilometer.'),
}
