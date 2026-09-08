# -*- coding: utf-8 -*-
"""Netto — handmatige herbeoordeling van onbevestigde bronnen, blok 1.

Biologie tot en met filosofie. Dit zijn vragen die wel een bron hadden, maar
waarbij het ophalen van die bron het antwoord niet bevestigde.

Bij het doorlopen viel op dat een groot deel van de opgegeven bronnen niets met
de vraag te maken heeft. Een handvol adressen — vooral UNESCO-lijstpagina's,
mathworld.wolfram.com/PolygonDiagonal.html en physics.nist.gov — staat verspreid
over tientallen losstaande vragen. De darmlengte verwees naar UNESCO-lijst 1187,
het aantal hartslagen per dag naar de lichtsnelheid. Zulke bronnen zijn niet
verouderd of verplaatst; ze zijn nooit bij de vraag gekozen. Ze worden hier
vervangen in plaats van gerepareerd.

Oordelen zoals in bronnen_handmatig_reserve.py: bevestigd, natellen, veroudert,
fout, onbruikbaar.
"""

O = {
    # ================= Biologie en gezondheid =================
    1: ('bevestigd', 'https://en.wikipedia.org/wiki/Onion',
        'Allium cepa is diploid met 2n = 16 chromosomen.'),
    2: ('natellen', 'https://www.aao.org/eye-health/tips-prevention/how-often-do-you-blink',
        'Een mens knippert vijftien tot twintig keer per minuut. Over een waakdag van zestien '
        'uur komt dat op ruwweg vijftienduizend; het getal moet zelf worden uitgerekend.'),
    110: ('bevestigd', 'https://en.wikipedia.org/wiki/Human_gastrointestinal_tract',
          'De dunne darm meet ongeveer 6,5 meter en de dikke darm 1,5 meter; samen rond de '
          '750 centimeter. De oude bron verwees naar een UNESCO-werelderfgoedlijst.'),
    111: ('bevestigd', 'https://en.wikipedia.org/wiki/Egg_cell',
          'Een eicel is haploid en bevat 23 chromosomen.'),
    112: ('bevestigd', 'https://en.wikipedia.org/wiki/Pea',
          'Pisum sativum heeft 2n = 14 chromosomen; het gewas waarmee Mendel werkte.'),
    113: ('bevestigd', 'https://www.genome.gov/genetics-glossary/Chromosome',
          'De mens heeft 23 chromosomenparen, samen 46 chromosomen.'),
    115: ('bevestigd', 'https://en.wikipedia.org/wiki/Heart_valve',
          'Het hart heeft vier kleppen: mitralis, tricuspidalis, aorta en pulmonalis.'),
    116: ('bevestigd', 'https://en.wikipedia.org/wiki/Heart',
          'Het menselijk hart heeft vier kamers: twee boezems en twee ventrikels.'),
    118: ('bevestigd', 'https://en.wikipedia.org/wiki/Heart_rate',
          'Bij zeventig slagen per minuut komt tachtig jaar uit op ongeveer drie miljard slagen.'),
    119: ('bevestigd', 'https://en.wikipedia.org/wiki/Saliva',
          'De speekselklieren produceren dagelijks ongeveer 0,5 tot 1,5 liter. De oude bron '
          'verwees naar een UNESCO-werelderfgoedlijst.'),
    128: ('natellen', 'https://en.wikipedia.org/wiki/Circulatory_system',
          'De honderdduizend kilometer is een gangbare schatting, geen meting. Geen bron kan '
          'dit exact bevestigen.'),
    402: ('bevestigd', 'https://en.wikipedia.org/wiki/Heart_rate',
          'Zeventig slagen per minuut maal 1440 minuten is 100.800 slagen per dag. De oude '
          'bron wees naar de lichtsnelheid bij NIST.'),
    602: ('bevestigd', 'https://en.wikipedia.org/wiki/Human_microbiome',
          'Sender, Fuchs en Milo kwamen in 2016 uit op ongeveer 38 biljoen bacterien tegenover '
          '30 biljoen menselijke cellen.'),
    604: ('bevestigd', 'https://en.wikipedia.org/wiki/Heart_rate',
          'Zeventig slagen per minuut geeft ruim honderdduizend slagen per dag.'),
    605: ('natellen', 'https://en.wikipedia.org/wiki/Cardiac_output',
          'Ongeveer vijf liter per minuut maal 1440 minuten geeft rond de 7200 liter per dag. '
          'De oude bron ging over diagonalen in veelhoeken.'),
    607: ('natellen', 'https://en.wikipedia.org/wiki/Breathing',
          'Volgt uit ademvolume maal ademfrequentie; de 550 liter is een afgeleide schatting, '
          'geen gepubliceerd getal.'),
    612: ('bevestigd', 'https://en.wikipedia.org/wiki/Human_skin',
          'De huid van een volwassene beslaat ongeveer 1,8 vierkante meter, oftewel 18.000 '
          'vierkante centimeter.'),
    613: ('bevestigd', 'https://en.wikipedia.org/wiki/Blood_transfusion',
          'James Blundell voerde in 1818 de eerste geslaagde transfusie van mens op mens uit.'),
    616: ('bevestigd', 'https://www.genome.gov/genetics-glossary/Deoxyribonucleic-Acid',
          'DNA bestaat uit vier basen: adenine, thymine, guanine en cytosine.'),

    # ================= Boeken en literatuur =================
    5: ('bevestigd', 'https://en.wikipedia.org/wiki/The_Hobbit',
        'The Hobbit telt negentien hoofdstukken.'),
    132: ('veroudert', 'https://en.wikipedia.org/wiki/A_Song_of_Ice_and_Fire',
          'Vijf delen verschenen; de reeks is niet af, dus dit getal kan veranderen.'),
    137: ('bevestigd', 'https://en.wikipedia.org/wiki/Animal_Farm',
          'Animal Farm telt tien hoofdstukken.'),
    138: ('bevestigd', 'https://en.wikipedia.org/wiki/Shakespeare%27s_plays',
          'De First Folio deelt de stukken in als veertien komedies, tien koningsdrama\'s en '
          'twaalf tragedies.'),
    142: ('natellen', 'https://en.wikipedia.org/wiki/Shakespeare%27s_plays',
          'De telling van 39 stukken telt Edward III en The Two Noble Kinsmen mee. Andere '
          'tellingen komen op 37 of 38 uit; de vraag noemt terecht "meest gebruikte telling".'),
    143: ('bevestigd', 'https://en.wikipedia.org/wiki/Inferno_(Dante)',
          'Inferno telt 34 zangen; Purgatorio en Paradiso elk 33.'),
    619: ('bevestigd', 'https://en.wikipedia.org/wiki/Hebrew_Bible',
          'De Tenach telt volgens de joodse indeling 24 boeken.'),
    620: ('bevestigd', 'https://en.wikipedia.org/wiki/Biblical_canon',
          'De katholieke canon telt 73 boeken: 46 in het Oude en 27 in het Nieuwe Testament.'),
    624: ('bevestigd', 'https://en.wikipedia.org/wiki/Alice%27s_Adventures_in_Wonderland',
          'Het boek telt twaalf hoofdstukken.'),

    # ================= Dagelijks leven =================
    146: ('bevestigd', 'https://en.wikipedia.org/wiki/Tripod',
          'Een statief staat per definitie op drie poten; het woord betekent drievoet.'),

    # ================= Dieren =================
    8: ('bevestigd', 'https://en.wikipedia.org/wiki/Blue_whale',
        'De tong van een blauwe vinvis weegt ongeveer 2,7 ton.'),
    148: ('bevestigd', 'https://oceanservice.noaa.gov/facts/seastars.html',
          'De gewone zeester heeft vijf armen; de vraag noemt de vijfarmige soort expliciet.'),
    151: ('bevestigd', 'https://en.wikipedia.org/wiki/Octopus',
          'Een octopus heeft drie harten: twee kieuwharten en een lichaamshart.'),
    153: ('bevestigd', 'https://en.wikipedia.org/wiki/Cockroach',
          'Het buisvormige hart van een kakkerlak heeft dertien kamers.'),
    154: ('bevestigd', 'https://en.wikipedia.org/wiki/Crocodilia',
          'Krokodilachtigen zijn de enige reptielen met een volledig gescheiden vierkamerhart.'),
    155: ('bevestigd', 'https://en.wikipedia.org/wiki/Hummingbird',
          'De hartslag van een kolibrie loopt tijdens het vliegen op tot rond de 1200 slagen '
          'per minuut. De oude bron verwees naar een UNESCO-werelderfgoedlijst.'),
    159: ('bevestigd', 'https://en.wikipedia.org/wiki/Bee',
          'Een bij heeft vijf ogen: twee samengestelde en drie enkelvoudige punctogen.'),
    168: ('bevestigd', 'https://en.wikipedia.org/wiki/Blue_whale',
          'Het gewogen hart van een gestrande blauwe vinvis kwam uit op ongeveer 180 kilo.'),
    636: ('bevestigd', 'https://en.wikipedia.org/wiki/Elephant',
          'De draagtijd van een olifant is ongeveer 22 maanden, rond de 660 dagen.'),
    639: ('bevestigd', 'https://en.wikipedia.org/wiki/Queen_bee',
          'Een koningin legt op het hoogtepunt van het seizoen tot tweeduizend eitjes per dag.'),
    654: ('natellen', 'https://en.wikipedia.org/wiki/Honey',
          'De negentigduizend kilometer is een gangbare vuistregel uit de imkerij, afgeleid uit '
          'vluchtafstand maal aantal vluchten. Geen gemeten getal.'),
    669: ('bevestigd', 'https://en.wikipedia.org/wiki/Insect',
          'Insecten hebben per definitie zes poten; het is het kenmerk van de klasse.'),
    681: ('natellen', 'https://en.wikipedia.org/wiki/Elephant',
          'De veertigduizend spieren is het klassieke getal. Recenter onderzoek telt ongeveer '
          '90.000 spierbundels; welk getal geldt hangt af van de telwijze.'),
    682: ('bevestigd', 'https://en.wikipedia.org/wiki/Cat_anatomy',
          'Een volwassen kat heeft dertig blijvende tanden.'),
    685: ('natellen', 'https://en.wikipedia.org/wiki/Octopus',
          'Een octopus heeft acht armen. De vraag zegt "tentakels", en dat is bij een octopus '
          'juist het woord dat niet klopt — inktvissen hebben tentakels, octopussen armen.'),

    # ================= Economie en geld =================
    169: ('fout', 'https://economy-finance.ec.europa.eu/euro/eu-countries-and-euro_en',
          'Elf landen voerden de euro in 1999 in. Het opgegeven 21 is het aantal eurolanden van '
          'nu, niet dat bij de start.'),
    170: ('bevestigd', 'https://en.wikipedia.org/wiki/Bitcoin',
          'Het protocol begrenst de uitgifte op 21 miljoen bitcoin. Het whitepaper waarnaar '
          'werd verwezen noemt dat getal nergens; het volgt uit de broncode.'),
    694: ('bevestigd', 'https://en.wikipedia.org/wiki/Nasdaq-100',
          'De index bevat honderd niet-financiele bedrijven; het staat in de naam.'),
    696: ('bevestigd', 'https://en.wikipedia.org/wiki/Euro',
          'Een euro is verdeeld in honderd cent.'),
    701: ('bevestigd', 'https://en.wikipedia.org/wiki/Euro_banknotes',
          'De reeks kent zeven coupures: 5, 10, 20, 50, 100, 200 en 500 euro.'),
    702: ('bevestigd', 'https://en.wikipedia.org/wiki/Euro_coins',
          'Er zijn acht munten: 1, 2, 5, 10, 20 en 50 cent plus 1 en 2 euro.'),

    # ================= Eten en drinken =================
    11: ('bevestigd', 'https://en.wikipedia.org/wiki/Big_Mac',
         'De Amerikaanse Big Mac bevat ongeveer 25 gram eiwit.'),
    13: ('bevestigd', 'https://en.wikipedia.org/wiki/Big_Mac',
         'De Amerikaanse Big Mac bevat ongeveer 580 kilocalorieen.'),
    182: ('natellen', 'https://en.wikipedia.org/wiki/Pizza_Margherita',
          'Tomaat, mozzarella en basilicum zijn het klassieke drietal, maar of deeg en olijfolie '
          'meetellen als basisingredient is een keuze, geen feit.'),
    184: ('bevestigd', 'https://en.wikipedia.org/wiki/Big_Mac',
          'De Amerikaanse Big Mac bevat ongeveer 45 gram koolhydraten.'),
    185: ('natellen', 'https://en.wikipedia.org/wiki/McDonald%27s',
          'De Amerikaanse cheeseburger zit rond de 31 gram koolhydraten. De voedingswaarde '
          'staat alleen op de productpagina van de keten, en die is niet op te halen.'),
    189: ('fout', '',
          'McDonald\'s telt sinds 1994 geen verkochte hamburgers meer en publiceert dit getal '
          'niet. Schattingen liggen tussen 2,4 en 6,5 miljard per jaar; 44 miljard is een orde '
          'van grootte te hoog.'),
    703: ('fout', 'https://corporate.mcdonalds.com/content/dam/sites/corp/nfl/pdf/Restaurants%20by%20Market%202023.pdf',
          'Het jaarverslag geeft 41.822 restaurants eind 2023, niet 41.198.'),
    708: ('onbruikbaar', '',
          'Chocoladerepen hebben geen standaardgewicht; het verschilt per merk en land.'),
    709: ('natellen', 'https://en.wikipedia.org/wiki/McDonald%27s',
          'De Amerikaanse cheeseburger zit rond de 300 kilocalorieen; alleen de productpagina '
          'van de keten geeft het exacte getal en die is niet op te halen.'),
    727: ('natellen', 'https://en.wikipedia.org/wiki/List_of_countries_with_McDonald%27s_restaurants',
          'De keten meldt "meer dan honderd landen". De lijst is te tellen, maar het exacte '
          'getal hangt af van de peildatum.'),

    # ================= Films en series =================
    14: ('bevestigd', 'https://en.wikipedia.org/wiki/Fawlty_Towers',
         'Fawlty Towers telt twaalf afleveringen in twee reeksen van zes.'),

    # ================= Filosofie, psychologie en religie =================
    16: ('bevestigd', 'https://en.wikipedia.org/wiki/Muses',
         'De Griekse mythologie kent negen Muzen, dochters van Zeus en Mnemosyne. De oude bron '
         'verwees naar een informatieblad over DNA.'),
    209: ('bevestigd', 'https://en.wikipedia.org/wiki/Titans',
          'De eerste generatie telt twaalf Titanen: zes zonen en zes dochters van Ouranos en Gaia.'),
    210: ('bevestigd', 'https://en.wikipedia.org/wiki/Republic_(Plato)',
          'De Staat is verdeeld in tien boeken.'),
    211: ('bevestigd', 'https://en.wikipedia.org/wiki/Salah',
          'De islamitische traditie schrijft vijf dagelijkse gebeden voor.'),
    215: ('bevestigd', 'https://en.wikipedia.org/wiki/Yggdrasil',
          'Yggdrasil verbindt negen werelden. De oude bron ging over Canadese provincies.'),
    216: ('bevestigd', 'https://en.wikipedia.org/wiki/Five_Pillars_of_Islam',
          'De islam kent vijf zuilen.'),
}
