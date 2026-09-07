# -*- coding: utf-8 -*-
"""Netto — handmatig toegekende bronnen voor de reservevragen zonder bruikbare bron.

Vier geautomatiseerde rondes hebben deze 316 vragen niet kunnen bedienen. De
laatste leverde 76 "treffers" waarvan er na een strenge zeef vijf deugden; de
rest matchte op demografische tabellen, krantennamen en de tekst "120px" uit een
afbeeldingscode. Daarom hier met de hand, precies zoals bij de 81 vragen die in
gebruik zijn.

DRIE SOORTEN TOEKENNING
  bevestigd   Het antwoord klopt en de bron draagt het.
  natellen    De bron is het juiste artikel, maar noemt het getal niet als getal.
              Bij "Hoeveel landen grenzen aan Argentinië?" somt het artikel de
              vijf buurlanden op zonder ergens "vijf" te schrijven. De bron
              deugt; de telling is met de hand te doen.
  fout        Het antwoord klopt niet. Het juiste getal staat in de toelichting.
  onbruikbaar De vraag zelf deugt niet. Geen bron toegekend.

Vorm: Nr: (soort, bron, toelichting)
"""

B = {
    # ================= Biologie & gezondheid =================
    147: ('onbruikbaar', '', 'De tienduizend stappen komen uit een Japanse reclamecampagne '
          'uit 1965, niet uit onderzoek. Er is geen bron die het meet.'),
    601: ('bevestigd', 'https://nl.wikipedia.org/wiki/Smaak_(zintuig)',
          'De moderne smaakleer onderscheidt vijf basissmaken: zoet, zuur, zout, bitter en umami.'),
    603: ('bevestigd', 'https://en.wikipedia.org/wiki/Foot', 'Voet en enkel tellen samen 26 botten.'),
    610: ('bevestigd', 'https://en.wikipedia.org/wiki/Rib_cage', 'Twaalf paar ribben, dus 24 in totaal.'),
    611: ('natellen', 'https://en.wikipedia.org/wiki/List_of_skeletal_muscles_of_the_human_body',
          'Tellingen lopen van 600 tot 650, afhankelijk van welke spieren apart worden geteld.'),
    614: ('bevestigd', 'https://www.nobelprize.org/prizes/physics/1901/rontgen/facts/',
          'Röntgen maakte de eerste röntgenfoto in november 1895.'),

    # ================= Boeken =================
    748: ('bevestigd', 'https://en.wikipedia.org/wiki/Harry_Potter',
          'De zeven Engelse originelen tellen samen 1.084.170 woorden.'),

    # ================= Dagelijks leven =================
    632: ('bevestigd', 'https://en.wikipedia.org/wiki/Egg_carton',
          'Twaalf vakken. Let op: duplicaat van vraag 192.'),
    1024: ('bevestigd', 'https://en.wikipedia.org/wiki/Ream_(unit)',
           'Een riem printpapier telt 500 vel.'),
    1146: ('onbruikbaar', '', 'Het antwoord staat letterlijk in de vraag.'),
    1177: ('onbruikbaar', '', 'De vraag spreekt zichzelf tegen: "per jaar" versus "driejaarlijkse".'),
    1228: ('natellen', 'https://www.cbs.nl/nl-nl/cijfers/detail/82900NED',
           'Het CBS publiceert de woningvoorraad naar type; het percentage moet je zelf afleiden.'),

    # ================= Dieren =================
    156: ('fout', 'https://nl.wikipedia.org/wiki/Potvis',
          'Een potvis duikt tot ongeveer 2000 METER. De vraag zegt kilometer: factor duizend fout.'),
    635: ('bevestigd', 'https://en.wikipedia.org/wiki/Emu', 'Een volwassen emoe wordt 150 tot 190 cm hoog.'),
    637: ('bevestigd', 'https://en.wikipedia.org/wiki/Big_five_game',
          'De Big Five telt er vijf. Het antwoord staat wel in de naam.'),
    638: ('onbruikbaar', '', 'Een kangoeroe is een buideldier en legt geen eieren. '
          'Het antwoord nul maakt bovendien elke deelsom stuk.'),
    642: ('bevestigd', 'https://en.wikipedia.org/wiki/Ruminant', 'Een geit is een herkauwer met vier magen.'),
    643: ('bevestigd', 'https://en.wikipedia.org/wiki/Red_kangaroo', 'Mannetjes worden tot 90 kg zwaar.'),
    644: ('bevestigd', 'https://en.wikipedia.org/wiki/African_bush_elephant',
          'Een volwassen olifant eet 100 tot 200 kg plantaardig voedsel per dag.'),
    645: ('bevestigd', 'https://en.wikipedia.org/wiki/African_bush_elephant', 'Mannetjes wegen tot 6000 kg.'),
    647: ('bevestigd', 'https://en.wikipedia.org/wiki/Bengal_tiger', 'Mannetjes wegen 200 tot 240 kg.'),
    648: ('bevestigd', 'https://en.wikipedia.org/wiki/Hippopotamus', 'Volwassen dieren wegen rond 1500 kg.'),
    649: ('bevestigd', 'https://en.wikipedia.org/wiki/Emu', 'Een volwassen emoe weegt 40 tot 45 kg.'),
    650: ('bevestigd', 'https://en.wikipedia.org/wiki/Giraffe', 'Mannetjes wegen ongeveer 1200 kg.'),
    651: ('bevestigd', 'https://en.wikipedia.org/wiki/Jaguar', 'Mannetjes wegen tot ongeveer 100 kg.'),
    652: ('bevestigd', 'https://nl.wikipedia.org/wiki/Witte_neushoorn',
          'Mannetjes worden tot ruim 2000 kg zwaar.'),
    655: ('bevestigd', 'https://en.wikipedia.org/wiki/Cheetah', 'De cheetah haalt 100 tot 120 km/u.'),
    656: ('natellen', 'https://en.wikipedia.org/wiki/Jaguar',
          'Snelheden voor de jaguar worden zelden precies vermeld; 80 km/u is gangbaar.'),
    657: ('bevestigd', 'https://en.wikipedia.org/wiki/Lion', 'Een leeuw sprint tot ongeveer 80 km/u.'),
    659: ('bevestigd', 'https://en.wikipedia.org/wiki/Ruminant',
          'Vier magen. Duplicaat van vraag 152.'),
    662: ('bevestigd', 'https://en.wikipedia.org/wiki/Nile_crocodile',
          'Nijlkrokodillen worden gemiddeld 4 tot 5 meter lang.'),
    663: ('bevestigd', 'https://en.wikipedia.org/wiki/African_bush_elephant',
          'Kop-romplengte tot ongeveer 7 meter.'),
    664: ('bevestigd', 'https://en.wikipedia.org/wiki/Saltwater_crocodile',
          'Zoutwaterkrokodillen worden maximaal ongeveer 6 meter.'),
    671: ('natellen', 'https://www.iucnredlist.org/species/15951/115130419',
          'Vrijwel de hele wilde populatie leeft in Sub-Sahara Afrika; alleen in India leeft nog '
          'een kleine groep. Het percentage staat er niet als getal.'),
    672: ('natellen', 'https://en.wikipedia.org/wiki/Amazon_rainforest',
          'Schattingen lopen uiteen; honderd is een gangbare orde van grootte.'),
    675: ('bevestigd', 'https://en.wikipedia.org/wiki/Macropodidae',
          'De familie Macropodidae telt ongeveer 65 soorten.'),
    680: ('natellen', 'https://en.wikipedia.org/wiki/Amazon_rainforest',
          'Rond de 1300 vogelsoorten; tellingen verschillen per afbakening van het gebied.'),
    683: ('natellen', 'https://en.wikipedia.org/wiki/Great_white_shark',
          'De voorste functionele rij telt 24 tot 26 tanden, afhankelijk van boven- of onderkaak. '
          'De vraag moet zeggen welke.'),
    684: ('bevestigd', 'https://en.wikipedia.org/wiki/Shark_tooth',
          'Een haai versleet in zijn leven tienduizenden tanden; 20.000 is de gangbare schatting.'),
    686: ('bevestigd', 'https://en.wikipedia.org/wiki/Koala', 'Koalas slapen 18 tot 22 uur per dag.'),
    687: ('bevestigd', 'https://en.wikipedia.org/wiki/Lion', 'Leeuwen rusten tot twintig uur per dag.'),
    688: ('onbruikbaar', '', 'Het antwoord nul klopt niet — het merendeel van de giftigste slangen '
          'leeft juist in Australië — en nul maakt elke deelsom stuk.'),
    690: ('bevestigd', 'https://en.wikipedia.org/wiki/American_bison', 'Stieren wegen tot ongeveer 900 kg.'),
    1244: ('natellen', 'https://www.vlinderstichting.nl/vlinders/',
           'De Vlinderstichting houdt de Nederlandse dagvlindersoorten bij; rond de 53 soorten.'),

    # ================= Economie & geld =================
    695: ('natellen', 'https://www.wto.org/english/res_e/statis_e/statis_e.htm',
          'De WTO publiceert de wereldhandel in goederen; rond de 24 tot 26 biljoen dollar per jaar.'),
    699: ('bevestigd', 'https://en.wikipedia.org/wiki/G7', 'De G7 telt zeven landen; dat staat in de naam.'),
    700: ('bevestigd', 'https://www.ecb.europa.eu/euro/coins/html/index.nl.html',
          'De euroreeks telt acht munten: 1, 2, 5, 10, 20 en 50 cent plus 1 en 2 euro.'),
    1230: ('natellen', 'https://www.dnb.nl/betalen/',
           'DNB publiceert het aandeel pin- en contactloze betalingen; rond de 80 procent.'),

    # ================= Eten & drinken =================
    188: ('onbruikbaar', '', 'Kooktijd hangt af van grootte en begintemperatuur van het ei. '
          'Een vuistregel, geen meetbaar feit.'),
    190: ('natellen', 'https://en.wikipedia.org/wiki/Cappuccino',
          'Klassiek één shot; veel zaken gebruiken er twee. De vraag moet "klassiek" zeggen.'),
    706: ('fout', 'https://www.parmigianoreggiano.com/',
          'Parmigiano Reggiano rijpt minimaal twaalf MAANDEN, niet twaalf dagen.'),
    713: ('bevestigd', 'https://en.wikipedia.org/wiki/Five-spice_powder',
          'Vijf kruiden; het antwoord staat in de naam.'),
    714: ('natellen', 'https://ich.unesco.org/en/RL/art-of-neapolitan-pizzaiuolo-00722',
          'UNESCO erkende de Napolitaanse pizzabakkerskunst als erfgoed van Italië.'),
    718: ('natellen', 'https://www.internationaloliveoil.org/',
          'De IOC publiceert olijfolieverbruik per land; Griekenland zit rond de 12 tot 20 liter.'),
    720: ('natellen', 'https://en.wikipedia.org/wiki/Types_of_chocolate',
          'Pure chocolade begint rond 50 procent cacao; 70 is gangbaar maar geen norm.'),
    721: ('bevestigd', 'https://www.icco.org/', 'West-Afrika levert ongeveer 70 procent van de wereldcacao.'),
    723: ('natellen', 'https://en.wikipedia.org/wiki/German_sausage',
          'Schattingen lopen van driehonderd tot vijftienhonderd soorten.'),
    725: ('natellen', 'https://en.wikipedia.org/wiki/List_of_French_cheeses',
          'Frankrijk kent enkele honderden kaassoorten; de telling hangt af van de afbakening.'),
    1170: ('onbruikbaar', '', 'Er bestaat geen standaardrecept voor boterkoek met een vaste hoeveelheid.'),
    1171: ('onbruikbaar', '', 'Het suikergehalte verschilt per reep en per uitvoering.'),
    1172: ('onbruikbaar', '', 'Het gewicht van een stroopwafel is niet genormeerd.'),
    1208: ('natellen', 'https://www.cbs.nl/nl-nl/cijfers/detail/7425',
           'Het CBS publiceert melkconsumptie per hoofd; het cijfer verschilt per jaargang.'),

    # ================= Films en series =================
    731: ('bevestigd', 'https://en.wikipedia.org/wiki/Mad_Max',
          'Vijf films, met Furiosa uit 2024 als laatste.'),
    737: ('bevestigd', 'https://www.oscars.org/oscars/ceremonies/2020',
          'Parasite won vier Oscars, waaronder Beste Film.'),
    750: ('bevestigd', 'https://en.wikipedia.org/wiki/History_of_film',
          'De gebroeders Lumière hielden de eerste publieke filmvertoning in december 1895.'),

    # ================= Filosofie, psychologie en religie =================
    754: ('bevestigd', 'https://en.wikipedia.org/wiki/Hebrew_Bible',
          'De Tenach telt 24 boeken in de joodse indeling.'),
    756: ('bevestigd', 'https://en.wikipedia.org/wiki/Plato',
          'Traditioneel worden 36 dialogen aan Plato toegeschreven.'),
    758: ('bevestigd', 'https://en.wikipedia.org/wiki/Four_Noble_Truths',
          'Vier edele waarheden; dat staat in de naam.'),
    764: ('bevestigd', 'https://en.wikipedia.org/wiki/Labours_of_Hercules', 'Twaalf werken.'),
    765: ('bevestigd', 'https://en.wikipedia.org/wiki/Noble_Eightfold_Path',
          'Acht paden; dat staat in de naam.'),
    766: ('natellen', 'https://en.wikipedia.org/wiki/Hajj',
          'De hadj trekt jaarlijks ongeveer twee miljoen pelgrims.'),
    767: ('bevestigd', 'https://www.pewresearch.org/religion/',
          'Ongeveer zeven procent van de wereldbevolking is boeddhistisch.'),
    769: ('onbruikbaar', '', 'De Arthurlegende kent geen vastgelegd aantal zwaarden. '
          'Excalibur en het zwaard in de steen worden soms als één en soms als twee geteld.'),

    # ================= Gebouwen en infrastructuur =================
    770: ('natellen', 'https://en.wikipedia.org/wiki/Egyptian_pyramids',
          'Tellingen lopen van 118 tot 138, afhankelijk van wat je meetelt.'),
    772: ('bevestigd', 'https://en.wikipedia.org/wiki/Colosseum',
          'Elke van de onderste drie verdiepingen telt tachtig bogen.'),
    774: ('bevestigd', 'https://en.wikipedia.org/wiki/Cologne_Cathedral',
          'Begonnen in 1248, voltooid in 1880: 632 jaar.'),
    782: ('bevestigd', 'https://en.wikipedia.org/wiki/Channel_Tunnel',
          'Van de 50,45 km ligt 37,9 km onder zee.'),
    784: ('bevestigd', 'https://en.wikipedia.org/wiki/U.S._Route_66',
          'Route 66 was 2448 mijl, ongeveer 3945 km.'),
    786: ('bevestigd', 'https://en.wikipedia.org/wiki/Big_Ben',
          'De Elizabeth Tower is 96 meter hoog.'),
    787: ('bevestigd', 'https://en.wikipedia.org/wiki/Christ_the_Redeemer_(statue)',
          'Het beeld zelf is 30 meter hoog.'),
    789: ('fout', 'https://en.wikipedia.org/wiki/Christ_the_Redeemer_(statue)',
          'Met sokkel is het 38 meter, niet 40. Bovendien bijna-duplicaat van vraag 787.'),
    792: ('bevestigd', 'https://en.wikipedia.org/wiki/Great_Pyramid_of_Giza',
          'Oorspronkelijk 146,6 meter; door erosie nu 138,5.'),
    801: ('bevestigd', 'https://en.wikipedia.org/wiki/Neuschwanstein_Castle',
          'Het kasteel meet 65 meter.'),
    807: ('bevestigd', 'https://en.wikipedia.org/wiki/Giza_pyramid_complex',
          'Drie grote piramides. Het antwoord staat in de vraag.'),
    808: ('onbruikbaar', '', '"Rivieren bruggen telt Sydney Harbour" is geen leesbare vraag, '
          'en het antwoord nul maakt elke deelsom stuk.'),
    811: ('bevestigd', 'https://pancanal.com/en/', 'Het kanaal heeft twaalf sluizen: zes paren.'),
    812: ('bevestigd', 'https://en.wikipedia.org/wiki/El_Castillo,_Chichen_Itza',
          'Vier trappen van 91 treden plus het platform: 365.'),
    813: ('bevestigd', 'https://en.wikipedia.org/wiki/El_Castillo,_Chichen_Itza',
          '91 treden per zijde; sluit aan op vraag 812.'),
    824: ('bevestigd', 'https://en.wikipedia.org/wiki/Q1_(building)',
          'De Q1 Tower telt 78 verdiepingen.'),
    825: ('natellen', 'https://en.wikipedia.org/wiki/Tokyo_Skytree',
          'De toren heeft twee uitkijkplatforms, op 350 en 450 meter.'),
    826: ('fout', 'https://www.whitehouse.gov/about-the-white-house/the-white-house/',
          'Het Witte Huis telt zes niveaus: twee kelderlagen, twee publieke en twee woonverdiepingen. '
          'Vier is alleen juist als je de kelders niet meetelt.'),
    1189: ('fout', 'https://nl.wikipedia.org/wiki/Van_Brienenoordbrug',
           'De vraag vraagt kilometers maar het antwoord 300 staat in meters.'),
    1223: ('bevestigd', 'https://www.dezaanseschans.nl/',
           'Op de Zaanse Schans staan acht molens.'),
    1248: ('natellen', 'https://www.rijksmuseum.nl/nl/over-ons/gebouw',
           'Het aantal zuilen aan de voorgevel is nergens als getal vastgelegd; zelf tellen op een foto.'),
}
