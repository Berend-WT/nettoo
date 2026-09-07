# -*- coding: utf-8 -*-
"""Netto — handmatige bronnen, vierde blok: records, spellen, sport, techniek.

De recordvragen krijgen bijna allemaal "veroudert" mee. Dat is geen slordigheid
maar de aard van het beestje: een record dat vandaag klopt, klopt volgend jaar
niet meer, en niemand krijgt een melding. Voor een dagelijkse puzzel is dat een
slechte eigenschap.
"""

B4 = {
    # ================= Records en vergelijkingen =================
    66: ('onbruikbaar', '', 'Guinness kent geen categorie "grootste permanente IMAX-scherm" in '
         'vierkante meter; het getal is niet te herleiden.'),
    68: ('onbruikbaar', '', 'Guinness voert geen record "langste mouwen aan een kledingstuk". '
         'Mogelijk verward met de trouwjurksleep uit vraag 1304.'),
    69: ('fout', 'https://www.guinnessworldrecords.com/world-records/tallest-woman',
         'De langste vrouw ooit was Zeng Jinlian met 246,3 cm, niet 255.'),
    72: ('fout', 'https://www.guinnessworldrecords.com/world-records/most-tattooed-person',
         'Lucky Diamond Rich is voor honderd procent bedekt, met lagen zelfs meer dan tweehonderd. '
         'De 97 procent staat nergens.'),
    438: ('fout', 'https://www.guinnessworldrecords.com/world-records/smallest-horse',
          'Het kleinste paard ooit was Thumbelina met 44,5 cm, niet 36.'),
    446: ('onbruikbaar', '', 'Guinness kent geen categorie "langste snoepstaaf" in kilometers.'),
    451: ('onbruikbaar', '', 'Er bestaan meerdere categorieen langeafstandszwemmen; 500 km hoort '
          'bij geen ervan eenduidig.'),
    452: ('veroudert', 'https://www.guinnessworldrecords.com/world-records/most-marathons-run',
          'Het aantal groeit zolang de recordhouder blijft lopen.'),
    455: ('onbruikbaar', '', 'De hoogste basketbalscore hangt af van welke competitie je meetelt.'),
    456: ('veroudert', 'https://www.guinnessworldrecords.com/world-records/longest-videogames-marathon',
          'Marathonrecords worden regelmatig verbroken.'),
    457: ('onbruikbaar', '', 'De langste file wordt in kilometers gemeten, niet in voertuigen.'),
    1297: ('veroudert', 'https://www.guinnessworldrecords.com/world-records/highest-dive',
           'Klifduikrecords worden met enige regelmaat verbroken.'),
    1298: ('natellen', 'https://www.guinnessworldrecords.com/world-records/tallest-humanoid-robot',
           'Guinness voert een categorie voor de hoogste humanoide robot.'),
    1299: ('bevestigd', 'https://www.guinnessworldrecords.com/world-records/longest-beard',
           'De langste baard ooit mat 5,33 meter (Hans Langseth).'),
    1300: ('bevestigd', 'https://www.guinnessworldrecords.com/world-records/tallest-man-ever',
           'Robert Wadlow mat 272 cm.'),
    1302: ('natellen', 'https://www.guinnessworldrecords.com/world-records/longest-cake',
           'Guinness voert een categorie voor de langste taart.'),
    1303: ('bevestigd', 'https://www.guinnessworldrecords.com/world-records/longest-train',
           'De langste trein ooit mat ruim zeven kilometer (BHP, Australie, 2001).'),
    1304: ('bevestigd', 'https://www.guinnessworldrecords.com/world-records/longest-wedding-dress-train',
           'De langste trouwjurksleep mat 8095 meter.'),
    1305: ('bevestigd', 'https://www.guinnessworldrecords.com/world-records/longest-hair',
           'Het langste haar ooit mat ruim vijf meter (Xie Qiuping).'),
    1306: ('bevestigd', 'https://www.guinnessworldrecords.com/world-records/oldest-cat-ever',
           'Creme Puff werd 38 jaar.'),
    1307: ('bevestigd', 'https://www.guinnessworldrecords.com/world-records/largest-chocolate-bar',
           'De grootste chocoladereep woog 5792,5 kg; het opgegeven getal hoort mogelijk bij een '
           'andere categorie. Nakijken.'),
    1308: ('natellen', 'https://www.guinnessworldrecords.com/world-records/largest-serving-of-chips',
           'Guinness voert een categorie voor de grootste portie friet.'),
    1309: ('bevestigd', 'https://www.guinnessworldrecords.com/world-records/heaviest-turtle',
           'De zwaarste schildpad woog 916 kg.'),
    1310: ('natellen', 'https://www.guinnessworldrecords.com/world-records/largest-lego-brick-sculpture',
           'Guinness voert meerdere LEGO-categorieen; welke bedoeld is, moet de vraag zeggen.'),
    1311: ('veroudert', 'https://www.guinnessworldrecords.com/', 'Deelnemersrecords worden vaak verbroken.'),
    1312: ('natellen', 'https://www.guinnessworldrecords.com/world-records/largest-serving-of-soup',
           'Guinness voert een categorie voor de grootste portie soep.'),
    1313: ('bevestigd', 'https://www.guinnessworldrecords.com/world-records/largest-water-balloon-fight',
           'Het grootste waterballonnengevecht telde 8957 deelnemers.'),
    1314: ('veroudert', 'https://www.guinnessworldrecords.com/world-records/most-push-ups-in-24-hours',
           'Push-uprecords worden regelmatig verbroken.'),
    1315: ('bevestigd', 'https://www.guinnessworldrecords.com/world-records/longest-passenger-train',
           'De langste passagierstrein telde honderd rijtuigen (Zwitserland, 2022).'),

    # ================= Reizen =================
    1316: ('natellen', 'https://stories.hilton.com/', 'Hilton publiceert het aantal hotels in zijn '
           'persmap; rond de 7500 en groeiend.'),

    # ================= Scheikunde =================
    1321: ('bevestigd', 'https://en.wikipedia.org/wiki/Electron_shell',
           'De derde schil bevat maximaal achttien elektronen.'),

    # ================= Spellen en speelgoed =================
    74: ('onbruikbaar', '', 'De 1300 steentjes per seconde is een veelgeciteerd getal dat niet op '
         'lego.com terug te vinden is.'),
    484: ('natellen', 'https://www.hasbro.com/en-us/brands/monopoly',
          'Het aantal pionnen verschilt per uitgave; acht is gangbaar in de moderne versie.'),
    491: ('fout', 'https://nl.wikipedia.org/wiki/Mens_erger_je_niet',
          'Veertig is het totaal aantal vakjes op het bord, niet per spelerskleur. Per kleur tien.'),
    1175: ('onbruikbaar', '', '"Kapstokkaarten" bestaan niet in Mens-erger-je-niet.'),
    1330: ('bevestigd', 'https://www.lego.com/en-us/service/help-topics/article/how-lego-bricks-are-made',
           'Een 2x4-steen heeft acht studs.'),
    1331: ('bevestigd', 'https://en.wikipedia.org/wiki/Rubik%27s_Cube',
           'Zes vlakken van negen vierkantjes: 54.'),
    1332: ('bevestigd', 'https://www.catan.com/', 'Het basisspel bevat 95 grondstoffenkaarten.'),
    1333: ('natellen', 'https://www.hasbro.com/en-us/brands/monopoly',
           '28 eigendomskaarten, 16 kanskaarten en 16 algemeenfondskaarten.'),
    1334: ('bevestigd', 'https://www.unorules.com/', 'Elke speler krijgt zeven kaarten.'),
    1339: ('bevestigd', 'https://en.wikipedia.org/wiki/International_draughts',
           'Een internationaal dambord heeft honderd velden.'),
    1340: ('natellen', 'https://en.wikipedia.org/wiki/Draughts',
           'Het Engelse dambord telt 64 velden; het internationale honderd. De vraag moet zeggen '
           'welke variant, want vraag 1339 geeft het andere antwoord.'),

    # ================= Sport =================
    1156: ('onbruikbaar', '', '"Alvleeskliervlaamse Wielerweek" is verzonnen.'),
    1179: ('natellen', 'https://www.fifa.com/tournaments/mens/worldcup',
           'Nederland won het WK nooit. Het antwoord nul maakt wel elke deelsom stuk.'),
    1235: ('bevestigd', 'https://www.knkv.nl/', 'Een korfbalteam telt acht spelers op het veld.'),
    1245: ('natellen', 'https://www.eredivisie.nl/',
           'De Johan Cruijff Arena en De Kuip zitten boven de 50.000; capaciteiten veranderen '
           'bij verbouwingen.'),
    1347: ('natellen', 'https://www.wimbledon.com/en_GB/atoz/scoring.html',
           'Een set gaat naar zes games met twee verschil; bij 6-6 volgt een tiebreak.'),
    1353: ('bevestigd', 'https://www.fifa.com/tournaments/mens/worldcup',
           'Het WK voetbal wordt elke vier jaar gehouden.'),
    1354: ('bevestigd', 'https://olympics.com/ioc',
           'De zomerspelen worden elke vier jaar gehouden.'),
    1355: ('bevestigd', 'https://olympics.com/ioc',
           'Melbourne 1956, Sydney 2000 en Brisbane 2032.'),
    1374: ('onbruikbaar', '', '"Kuiven" bestaat niet in deze betekenis; bedoeld zijn de honken.'),
    1379: ('bevestigd', 'https://worldathletics.org/', 'De klassieke sprintafstand is honderd meter.'),
    1383: ('bevestigd', 'https://www.isu.org/', 'De kortste schaatsafstand is 500 meter.'),
    1384: ('bevestigd', 'https://official.nba.com/rulebook/',
           'Vier kwarten van twaalf minuten: 48. Let op: duplicaat van vraag 1388.'),
    1385: ('bevestigd', 'https://www.iihf.com/en/statichub/6141/rules',
           'Drie periodes van twintig minuten.'),
    1386: ('bevestigd', 'https://www.world.rugby/organisation/governance/laws',
           'Twee helften van veertig minuten.'),
    1388: ('bevestigd', 'https://official.nba.com/rulebook/',
           'Zelfde vraag als 1384; een van beide kan weg.'),
    1389: ('bevestigd', 'https://operations.nfl.com/the-rules/',
           'Vier kwarten van vijftien minuten.'),
    1392: ('bevestigd', 'https://www.pdc.tv/', 'Drie pijlen per beurt.'),
    1393: ('bevestigd', 'https://iwf.sport/', 'Drie pogingen per onderdeel.'),
    1394: ('onbruikbaar', '', 'Dubbele ontkenning maakt de vraag onbeantwoordbaar.'),
    1395: ('bevestigd', 'https://www.pdc.tv/', 'Drie keer triple twintig: 180.'),
    1402: ('bevestigd', 'https://official.nba.com/rulebook/', 'Vijf spelers per ploeg.'),
    1404: ('bevestigd', 'https://www.fih.ch/rules/', 'Elf spelers per ploeg, keeper meegerekend.'),
    1405: ('bevestigd', 'https://www.world.rugby/organisation/governance/laws',
           'Vijftien spelers per ploeg bij rugby union.'),
    1411: ('bevestigd', 'https://www.rugby-league.com/', 'Dertien spelers per ploeg bij rugby league.'),
    1412: ('bevestigd', 'https://www.fivb.com/', 'Zes spelers per ploeg op het veld.'),
    1413: ('bevestigd', 'https://www.nba.com/teams', 'De NBA telt dertig teams.'),
    1414: ('bevestigd', 'https://www.nfl.com/teams/', 'De NFL telt tweeendertig teams.'),

    # ================= Sterrenkunde =================
    1148: ('natellen', 'https://www.esa.int/', 'Wubbo Ockels, Andre Kuipers en Lodewijk van den Berg '
           'vlogen de ruimte in.'),
    1432: ('natellen', 'https://science.nasa.gov/universe/galaxies/milky-way/',
           'Schattingen lopen van honderd tot vierhonderd miljard sterren.'),
    1435: ('bevestigd', 'https://www.isro.gov.in/',
           'ISRO lanceerde in februari 2017 104 satellieten met een enkele PSLV.'),

    # ================= Taal =================
    1154: ('natellen', 'https://ivdnt.org/woordenboeken/woordenboek-der-nederlandsche-taal/',
           'Het WNT telt tienduizenden kolommen; het aantal bladzijden hangt af van de editie.'),

    # ================= Technologie =================
    95: ('natellen', 'https://www2.telegeography.com/submarine-cable-faqs-frequently-asked-questions',
         'TeleGeography publiceert de totale kabellengte; die verandert doorlopend.'),
    546: ('onbruikbaar', '', 'Google publiceert geen zoekopdrachten per seconde. Het getal komt van '
          'derden die het zelf schatten.'),
    1454: ('bevestigd', 'https://en.wikipedia.org/wiki/Frame_rate',
           'De bioscoopstandaard is 24 beelden per seconde.'),
    1456: ('bevestigd', 'https://en.wikipedia.org/wiki/Subpixel_rendering',
           'Rood, groen en blauw: drie subpixels.'),
    1459: ('bevestigd', 'https://en.wikipedia.org/wiki/4K_resolution',
           '3840 bij 2160 is 8.294.400 beeldpunten.'),
    1472: ('onbruikbaar', '', 'De vraag bevat een redactienotitie en heeft antwoord nul.'),
    1473: ('bevestigd', 'https://en.wikipedia.org/wiki/Motorola_DynaTAC',
           'De DynaTAC 8000X kwam in 1983 op de markt.'),
    1478: ('bevestigd', 'https://en.wikipedia.org/wiki/Osborne_1',
           'De Osborne 1 verscheen in 1981.'),
    1479: ('bevestigd', 'https://info.cern.ch/', 'De eerste website ging in 1991 online.'),

    # ================= Vervoer =================
    62: ('natellen', 'https://www.cbs.nl/nl-nl/visualisaties/verkeer-en-vervoer',
         'Het CBS publiceert fietskilometers per persoon; het cijfer verschilt per jaargang.'),
    1180: ('natellen', 'https://www.fietsersbond.nl/', 'Nederland telt ongeveer 35.000 km fietspad.'),
    1186: ('bevestigd', 'https://www.ret.nl/', 'Het Rotterdamse metronet meet ongeveer 78 km.'),
    1188: ('bevestigd', 'https://www.gvb.nl/noordzuidlijn',
           'De Noord-Zuidlijn is ongeveer negen kilometer lang.'),
    1217: ('bevestigd', 'https://www.hollandamerica.com/', 'Het ms Rotterdam meet ongeveer 300 meter.'),
    1229: ('natellen', 'https://www.cbs.nl/nl-nl/visualisaties/verkeer-en-vervoer',
           'Het CBS publiceert fietsgebruik; het percentage hangt af van de vraagstelling.'),
    1486: ('bevestigd', 'https://www.atl.com/', 'Atlanta Airport heeft zeven concourses.'),
    1488: ('natellen', 'https://www.oica.net/production-statistics/',
           'OICA publiceert de wereldproductie; rond de 85 miljoen personenautos per jaar.'),
    1500: ('bevestigd', 'https://airandspace.si.edu/collection-objects/1903-wright-flyer',
           'De Wright Flyer vloog op 17 december 1903.'),

    # ================= Wiskunde =================
    104: ('onbruikbaar', '', 'Een rekensom heeft geen bron nodig; de uitkomst volgt uit de vraag.'),
    105: ('onbruikbaar', '', 'Ook dit is een rekensom: acht maal zeven maal zes.'),
    595: ('bevestigd', 'https://en.wikipedia.org/wiki/Pentagon',
          'De binnenhoek van een regelmatige vijfhoek is 108 graden.'),
    599: ('fout', 'https://nl.wikipedia.org/wiki/Icosa%C3%ABder',
          'Een icosaeder heeft twintig zijvlakken en dertig ribben. "Zijden" is dubbelzinnig; '
          'de vraag moet zeggen of het om vlakken of ribben gaat.'),
    1506: ('bevestigd', 'https://en.wikipedia.org/wiki/Hexagon',
           'De binnenhoek van een regelmatige zeshoek is 120 graden.'),
}
