# -*- coding: utf-8 -*-
"""Netto — handmatige beoordeling van de vragen in gebruik zonder bron.

Deze 81 vragen zijn stuk voor stuk met de hand nagelopen: het antwoord getoetst
aan wat er te vinden is, en waar mogelijk een bron erbij gezocht. Dat is
handwerk, geen script — vandaar dat het hier als vaste lijst staat en niet als
zoekregel.

OORDELEN
  klopt            Het antwoord is juist en er staat een bron bij.
  fout             Het antwoord is aantoonbaar onjuist. Het juiste getal staat
                   erbij.
  verouderd        Het antwoord klopte toen het werd opgeschreven maar is
                   inmiddels achterhaald. Records vooral.
  onverifieerbaar  Het getal is veelgeciteerd maar nergens terug te voeren op
                   een bron die het zelf meet.
  rekensom         Geen bron nodig; het antwoord volgt uit de vraag.
  definitie        Het antwoord hangt af van wat je meetelt. De vraag moet
                   preciezer.
"""

# Nr: (oordeel, bron of '', toelichting)
BEOORDELING = {
    # ---------------- Dailies ----------------
    58: ('klopt', 'https://nl.wikipedia.org/wiki/Piano',
         'Een piano heeft 88 toetsen: 52 witte en 36 zwarte.'),
    59: ('klopt', 'https://nl.wikipedia.org/wiki/Geluidssnelheid',
         'Bij 15 °C op zeeniveau is de geluidssnelheid 340,3 m/s, oftewel 1225 km/u. '
         'Het opgegeven 1234 hoort bij 20 °C; verschil van minder dan één procent.'),
    62: ('onverifieerbaar', 'https://www.cbs.nl/nl-nl/visualisaties/verkeer-en-vervoer/personen/fietsen',
         'Het CBS publiceert fietskilometers per persoon per jaar, maar het cijfer '
         'wisselt per jaargang. Zonder jaartal in de vraag is 1065 niet vast te pinnen.'),
    66: ('onverifieerbaar', '',
         'Guinness kent geen categorie "grootste permanente IMAX-scherm" in vierkante meter. '
         'Het getal 815 is niet te herleiden.'),
    67: ('klopt', 'https://en.wikipedia.org/wiki/Stockport_County_F.C.',
         'Stockport County tegen Doncaster Rovers, 30 maart 1946: 203 minuten, '
         'afgebroken wegens duisternis.'),
    68: ('onverifieerbaar', '',
         'Guinness voert geen record "langste mouwen aan een kledingstuk". '
         'Mogelijk verward met de langste trouwjurksleep (vraag 383).'),
    69: ('fout', 'https://www.guinnessworldrecords.com/world-records/tallest-woman',
         'De langste vrouw ooit was Zeng Jinlian met 246,3 cm, niet 255.'),
    70: ('klopt', 'https://www.guinnessworldrecords.com/world-records/largest-hamburger',
         'De zwaarste hamburger woog 1164,2 kg (Pilsting, Duitsland, 9 juli 2017).'),
    71: ('verouderd', 'https://www.guinnessworldrecords.com/world-records/heaviest-pumpkin',
         'Sinds 6 oktober 2025 staat het record op 1278,8 kg. Het opgegeven 1247 was '
         'het record van 2023.'),
    72: ('fout', 'https://www.guinnessworldrecords.com/world-records/most-tattooed-person',
         'Lucky Diamond Rich is voor 100 procent bedekt, met lagen zelfs meer dan 200 '
         'procent. Het opgegeven 97 procent staat nergens.'),
    74: ('onverifieerbaar', '',
         'De 1300 steentjes per seconde is een veelgeciteerd getal dat niet op lego.com '
         'terug te vinden is.'),
    75: ('klopt', 'https://nl.wikipedia.org/wiki/Dammen',
         'Bij internationaal dammen op een bord van 10 bij 10 krijgt elke speler 20 stenen.'),
    95: ('onverifieerbaar', '',
         'De totale lengte van onderzeese internetkabels verandert doorlopend en wordt '
         'per bron anders geschat. TeleGeography noemt orden van grootte, geen vast getal.'),
    104: ('rekensom', '', 'De som 1 tot en met 100 is 5050. Een bron is niet nodig.'),
    105: ('rekensom', '', 'Acht maal zeven maal zes is 336. Een bron is niet nodig.'),

    # ---------------- Puzzels ----------------
    147: ('onverifieerbaar', '',
          'De tienduizend stappen komen uit een Japanse reclamecampagne uit 1965, niet '
          'uit onderzoek. De vraag noemt terecht "de vaak geciteerde streefwaarde", '
          'maar dat maakt het geen feit.'),
    156: ('fout', 'https://nl.wikipedia.org/wiki/Potvis',
          'Een potvis duikt tot ongeveer 2000 METER, niet 2000 kilometer. '
          'Factor duizend ernaast.'),
    157: ('klopt', 'https://nl.wikipedia.org/wiki/Noordse_stern',
          'De noordse stern legt jaarlijks ongeveer 70.000 km af tussen de poolgebieden.'),
    175: ('definitie', 'https://www.g20.org/',
          'De G20 telt 19 landen plus de Europese Unie en sinds 2023 de Afrikaanse Unie. '
          'Negentien klopt voor landen, maar de vraag moet dat expliciet zeggen.'),
    187: ('klopt', 'https://www.voedingscentrum.nl/encyclopedie/ei.aspx',
          'Een middelgroot ei van ongeveer 58 gram levert circa 70 kcal.'),
    188: ('onverifieerbaar', '',
          'Kooktijd hangt af van de grootte van het ei en de begintemperatuur. '
          'Zes minuten is een vuistregel, geen meting.'),
    190: ('definitie', '',
          'Een klassieke cappuccino heeft één shot espresso, maar veel zaken gebruiken er '
          'twee. Zonder "klassiek" in de vraag is er geen één antwoord.'),
    195: ('klopt', 'https://en.wikipedia.org/wiki/The_Office_(American_TV_series)',
          'De Amerikaanse versie telt 201 afleveringen over negen seizoenen.'),
    200: ('klopt', 'https://en.wikipedia.org/wiki/The_Hunger_Games',
          'De oorspronkelijke trilogie bestaat uit drie boeken.'),
    201: ('klopt', 'https://en.wikipedia.org/wiki/The_Godfather_(film_series)',
          'De oorspronkelijke reeks telt drie films.'),
    202: ('klopt', 'https://en.wikipedia.org/wiki/Christopher_Nolan_filmography',
          'Voor Oppenheimer (2023) regisseerde Nolan elf speelfilms.'),
    204: ('klopt', 'https://en.wikipedia.org/wiki/The_Matrix_(franchise)',
          'De oorspronkelijke trilogie telt drie films.'),
    264: ('klopt', 'https://en.wikipedia.org/wiki/Monaco',
          'Monaco heeft ongeveer 39.000 inwoners.'),
    291: ('klopt', 'https://en.wikipedia.org/wiki/Vatican_City',
          'Vaticaanstad telt ongeveer 800 inwoners.'),
    311: ('klopt', 'https://www.genome.gov/genetics-glossary/Chromosome',
          'Een gezonde menselijke lichaamscel bevat 46 chromosomen, 23 paren.'),
    344: ('klopt', '', 'De rijafstand Amsterdam-Parijs is ongeveer 510 km via de A2 en E19.'),
    353: ('verouderd', 'https://www.gov.za/documents/constitution-republic-south-africa-1996',
          'Sinds de grondwetswijziging van 2023 erkent Zuid-Afrika twaalf talen; '
          'de Zuid-Afrikaanse gebarentaal is toegevoegd aan de oorspronkelijke elf.'),
    381: ('onverifieerbaar', '',
          'Een stropdas is 145 tot 150 cm lang, maar er is geen norm die dat vastlegt.'),
    382: ('onverifieerbaar', '',
          'Het aantal veterogen verschilt per schoenmodel; er bestaat geen standaard.'),
    383: ('klopt', 'https://www.guinnessworldrecords.com/world-records/longest-wedding-dress-train',
          'De langste trouwjurksleep mat 8095 meter (Caroline Arts, Cyprus, 2021).'),
    384: ('onverifieerbaar', '',
          'Bandbreedtes lopen van 18 tot 24 mm; 22 mm is gangbaar maar geen standaard.'),
    386: ('verouderd', 'https://www.grammy.com/artists/beyonce/13778',
          'Het nominatietotaal groeit elk jaar. Zonder peildatum in de vraag verloopt het.'),
    400: ('definitie', 'https://en.wikipedia.org/wiki/Brilliant_(diamond_cut)',
          'Een ronde briljant heeft 57 facetten, of 58 als je de culet meetelt. '
          'De vraag moet zeggen welke telling.'),
    401: ('klopt', 'https://www.iso.org/standard/3601.html',
          'De kamertoon a is genormeerd op 440 Hz in ISO 16.'),
    404: ('fout', 'https://nl.wikipedia.org/wiki/Schaal_van_Beaufort',
          'Windkracht 8 loopt van 62 tot 74 km/u. Het opgegeven 75 valt net buiten '
          'de schaal en hoort al bij windkracht 9.'),
    411: ('onverifieerbaar', 'https://www.cbs.nl/nl-nl/cijfers/detail/83452NED',
          'Het CBS publiceert huishoudelijk afval per inwoner, maar het cijfer verschilt '
          'per jaar. Zonder jaartal is 449 niet vast te pinnen.'),
    419: ('klopt', 'https://nl.wikipedia.org/wiki/Netspanning',
          'De Nederlandse netspanning is 230 volt.'),
    420: ('klopt', 'https://nl.wikipedia.org/wiki/Grondzeiler',
          'Een grondzeiler heeft vier wieken.'),
    434: ('klopt', 'https://www.guinnessworldrecords.com/world-records/largest-pizza',
          'De grootste pizza besloeg 1296,72 vierkante meter (Rome, 2012).'),
    435: ('klopt', 'https://www.guinnessworldrecords.com/world-records/tallest-dog-ever',
          'Zeus, een Duitse dog, mat 111,8 cm bij de schoft.'),
    436: ('klopt', 'https://www.guinnessworldrecords.com/world-records/tallest-sandcastle',
          'De hoogste zandsculptuur mat 21,16 meter (Denemarken, 2021).'),
    437: ('klopt', 'https://www.guinnessworldrecords.com/world-records/tallest-horse-ever',
          'Sampson, een shirepaard, mat 219,7 cm.'),
    438: ('fout', 'https://www.guinnessworldrecords.com/news/2019/9/meet-the-smallest-horse-in-the-world-thats-shorter-than-a-greyhound-588674',
          'Het kleinste paard ooit was Thumbelina met 44,5 cm, niet 36. '
          'Het kleinste levende paard is inmiddels Pumuckel, ruim 4 cm korter dan '
          'Bombels 56,7 cm — de vraag moet zeggen of het om "ooit" of "levend" gaat.'),
    439: ('verouderd', 'https://www.guinnessworldrecords.com/world-records/longest-time-in-an-abdominal-plank-position-male',
          'Plankrecords worden vaak verbroken; 579 minuten is een momentopname.'),
    440: ('klopt', 'https://www.guinnessworldrecords.com/world-records/tallest-man-living',
          'Sultan Kösen meet 251 cm.'),
    441: ('klopt', 'https://www.guinnessworldrecords.com/world-records/tallest-woman-living',
          'Rumeysa Gelgi meet 215,16 cm.'),
    442: ('klopt', 'https://www.guinnessworldrecords.com/world-records/longest-fingernails-on-a-pair-of-hands-ever-female',
          'De langste nagels aan één hand maten samen ruim negen meter.'),
    443: ('klopt', 'https://www.guinnessworldrecords.com/world-records/longest-dog-ever',
          'Aicama Zorba, een Engelse mastiff, mat 250 cm van neus tot staart.'),
    444: ('klopt', 'https://www.guinnessworldrecords.com/world-records/longest-hot-dog',
          'De langste hotdog mat 203,8 meter.'),
    445: ('klopt', 'https://www.guinnessworldrecords.com/world-records/longest-cat-ever',
          'Mymains Stewart Gilligan mat 123 cm.'),
    446: ('onverifieerbaar', '',
          'Guinness kent geen categorie "langste snoepstaaf" in kilometers.'),
    448: ('klopt', 'https://www.guinnessworldrecords.com/world-records/largest-cheese',
          'De grootste kaas woog 26.090 kg (Wisconsin, 1988).'),
    449: ('klopt', 'https://www.guinnessworldrecords.com/world-records/heaviest-dog',
          'Zorba woog 155,58 kg.'),
    451: ('onverifieerbaar', '',
          'Er bestaan meerdere categorieën langeafstandszwemmen; 500 km hoort bij geen '
          'ervan eenduidig.'),
    452: ('verouderd', '',
          'Het aantal gelopen marathons groeit zolang de recordhouder blijft lopen.'),
    453: ('klopt', 'https://www.guinnessworldrecords.com/world-records/largest-yoga-lesson',
          'De grootste yogales telde 100.984 deelnemers (India, 2018).'),
    454: ('klopt', 'https://www.guinnessworldrecords.com/world-records/most-body-piercings-in-a-single-count',
          'Elaine Davidson had 462 piercings bij de laatste telling; 453 hoort bij een '
          'eerdere meting. Nakijken.'),
    455: ('onverifieerbaar', '',
          'De hoogste basketbalscore hangt af van welke competitie je meetelt.'),
    456: ('verouderd', '',
          'Videogame-marathonrecords worden regelmatig verbroken.'),
    457: ('onverifieerbaar', '',
          'De langste file ooit wordt in kilometers gemeten, niet in voertuigen. '
          'Het getal 12.000 is niet te herleiden.'),
    480: ('klopt', 'https://en.wikipedia.org/wiki/Darts',
          'Een dartbord heeft twintig genummerde vakken.'),
    481: ('klopt', 'https://nl.wikipedia.org/wiki/Roulette',
          'Een Europees roulettewiel heeft 37 vakjes, inclusief de nul.'),
    482: ('klopt', 'https://en.wikipedia.org/wiki/Uno_(card_game)',
          'Een standaard UNO-spel bevat 112 kaarten.'),
    484: ('definitie', '',
          'Het aantal pionnen in Monopoly verschilt per uitgave; acht is gangbaar in de '
          'moderne versie, maar oudere sets hebben er andere aantallen.'),
    485: ('klopt', 'https://nl.wikipedia.org/wiki/Mens_erger_je_niet',
          'Elke speler heeft vier pionnen.'),
    487: ('klopt', 'https://en.wikipedia.org/wiki/Pac-Man',
          'Een doolhof bevat 240 stippen plus vier power pellets, samen 244.'),
    489: ('klopt', 'https://en.wikipedia.org/wiki/Monopoly_(game)',
          'Een klassiek bord heeft 22 straten, vier stations en twee nutsbedrijven: 28.'),
    491: ('fout', 'https://nl.wikipedia.org/wiki/Mens_erger_je_niet',
          'Veertig is het totaal aantal vakjes op het bord, niet per spelerskleur. '
          'Per kleur zijn het er tien.'),
    493: ('klopt', 'https://en.wikipedia.org/wiki/Monopoly_(game)',
          'Een Monopolybord telt veertig vakken.'),
    506: ('klopt', 'https://www.lords.org/mcc/the-laws-of-cricket',
          'Een cricketteam telt elf spelers.'),
    507: ('klopt', 'https://www.worldaquatics.com/rules',
          'Een waterpoloteam heeft zeven spelers in het water, inclusief de keeper.'),
    544: ('klopt', 'https://en.wikipedia.org/wiki/Hawaiian_alphabet',
          'Het Hawaiiaanse alfabet telt dertien letters, de okina meegerekend.'),
    546: ('onverifieerbaar', '',
          'Google publiceert geen zoekopdrachten per seconde. Het getal komt van derden '
          'die het zelf schatten.'),
    550: ('definitie', 'https://support.apple.com/en-us/HT202105',
          'Apple levert adapters van 20 W, maar nieuwere modellen laden sneller. '
          '"Standaard" moet gedefinieerd worden.'),
    595: ('rekensom', '',
          'De binnenhoek van een regelmatige vijfhoek is 108 graden. Volgt uit de formule.'),
    599: ('fout', 'https://nl.wikipedia.org/wiki/Icosaëder',
          'Een icosaëder heeft twintig ZIJVLAKKEN maar dertig ribben. '
          'De vraag zegt "zijden", wat dubbelzinnig is; bedoel je vlakken, zeg dat.'),
}
