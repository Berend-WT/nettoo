# -*- coding: utf-8 -*-
"""Netto — handmatige bronnen, tweede blok (kunst tot en met politiek).

Vervolg op bronnen_handmatig_reserve.py; zelfde soorten toekenning.
"""

B2 = {
    # ================= Kunst en cultuur =================
    1060: ('bevestigd', 'https://presse.louvre.fr/',
           'Het Louvre ontving in 2023 ongeveer 8,9 miljoen bezoekers.'),
    1062: ('natellen', 'https://en.wikipedia.org/wiki/Moai',
           'Moai lopen sterk uiteen in gewicht; 12,5 ton is een gangbaar gemiddelde voor de grotere.'),
    1064: ('natellen', 'https://whc.unesco.org/en/statesparties/cn',
           'UNESCO houdt het aantal per land bij. Het cijfer groeit jaarlijks, dus zonder peiljaar '
           'veroudert dit antwoord.'),
    1065: ('natellen', 'https://whc.unesco.org/en/statesparties/de',
           'Zelfde lijst voor Duitsland; ook dit cijfer groeit.'),
    1067: ('bevestigd', 'https://closertovaneyck.kikirpa.be/',
           'Het Lam Gods telt twaalf panelen.'),
    1157: ('onbruikbaar', '', '"Per seizoensblok" is een verzonnen meeteenheid.'),
    1239: ('natellen', 'https://www.rijksmuseum.nl/nl/zoeken',
           'De collectiedatabase is te doorzoeken; het aantal wisselt met de catalogisering.'),

    # ================= Landbouw en industrie =================
    633: ('onbruikbaar', '', 'Antwoord nul, en het aantal bijenkorven per imker ligt nergens vast.'),
    1073: ('bevestigd', 'https://en.wikipedia.org/wiki/Beehive',
           'Een sterk volk telt in de zomer 50.000 tot 60.000 bijen.'),
    1209: ('natellen', 'https://www.cbs.nl/nl-nl/cijfers/detail/7425',
           'Het CBS publiceert de melkproductie per koe; rond de 9000 liter per jaar.'),

    # ================= Merken en producten =================
    1088: ('natellen', 'https://www.aldi.nl/',
           'Aldi zit rond de 12.000 winkels wereldwijd; het aantal groeit.'),
    1089: ('fout', 'https://www.lidl.nl/',
           'Lidl passeerde 13.000 filialen. Het opgegeven 12.500 is te laag, en identiek aan dat '
           'van Aldi in vraag 1088 — twee verschillende ketens met precies hetzelfde getal.'),

    # ================= Milieu en duurzaamheid =================
    411: ('natellen', 'https://www.cbs.nl/nl-nl/cijfers/detail/83452NED',
          'Het CBS publiceert huishoudelijk afval per inwoner; het cijfer verschilt per jaargang.'),
    1096: ('bevestigd', 'https://www.ramsar.org/',
           'Ramsar houdt aan dat sinds 1700 ongeveer 85 procent van de wetlands is verdwenen.'),

    # ================= Mode en lifestyle =================
    381: ('onbruikbaar', '', 'Daslengtes lopen van 145 tot 150 cm; er is geen norm.'),
    382: ('onbruikbaar', '', 'Het aantal veterogen verschilt per schoenmodel.'),
    384: ('onbruikbaar', '', 'Bandbreedtes lopen van 18 tot 24 mm; geen standaard.'),
    1102: ('natellen', 'https://en.wikipedia.org/wiki/Dress_shirt',
           'Overhemden hebben doorgaans zes tot acht knopen aan de voorkant.'),

    # ================= Muziek =================
    1105: ('bevestigd', 'https://www.grammy.com/artists/acdc/2277',
           'AC/DC won een Grammy in 2010 voor War Machine.'),
    1107: ('bevestigd', 'https://en.wikipedia.org/wiki/AC/DC_discography',
           'AC/DC bracht zeventien studioalbums uit.'),
    1109: ('bevestigd', 'https://ich.unesco.org/en/RL/rumba-in-cuba-01185',
           'De Cubaanse rumba kent drie hoofdstijlen: yambu, guaguanco en columbia.'),
    1112: ('natellen', 'https://ich.unesco.org/en/RL/mariachi-string-music-song-and-trumpet-01061',
           'Een mariachiband telt doorgaans acht tot twaalf muzikanten.'),
    1116: ('onbruikbaar', '', 'Onafgemaakte zin: "koto-ensemble van hoort".'),
    1117: ('bevestigd', 'https://en.wikipedia.org/wiki/Krar', 'De krar heeft vijf of zes snaren.'),
    1118: ('natellen', 'https://en.wikipedia.org/wiki/Sitar',
           'Een sitar heeft achttien tot eenentwintig snaren, afhankelijk van het model.'),
    1119: ('onbruikbaar', '', 'Een djembe is een trommel en heeft geen snaren. Het antwoord nul '
           'maakt bovendien elke deelsom stuk.'),
    1121: ('bevestigd', 'https://en.wikipedia.org/wiki/Kora_(instrument)',
           'De kora heeft traditioneel eenentwintig snaren.'),
    1123: ('bevestigd', 'https://en.wikipedia.org/wiki/Tiple_(Colombian)',
           'De Colombiaanse tiple heeft twaalf snaren, in vier koren van drie.'),
    1124: ('onbruikbaar', '', 'De vraag verwart twee instrumenten: een guitarron is geen bajo sexto.'),
    1125: ('bevestigd', 'https://en.wikipedia.org/wiki/Koto_(instrument)',
           'De koto heeft dertien snaren.'),
    1128: ('natellen', 'https://newsroom.spotify.com/',
           'Streamingaantallen groeien doorlopend; zonder peildatum verloopt dit antwoord.'),
    1129: ('natellen', 'https://en.wikipedia.org/wiki/Kylie_Minogue_discography',
           'Zestien studioalbums; de discografie groeit nog.'),
    1131: ('bevestigd', 'https://en.wikipedia.org/wiki/The_Beatles_discography',
           'In het Verenigd Koninkrijk verschenen twaalf studioalbums.'),
    1155: ('onbruikbaar', '', '"Bruggetje van Sainte Annei" bestaat niet en de vraag ontkent zichzelf.'),

    # ================= Natuurkunde =================
    404: ('fout', 'https://nl.wikipedia.org/wiki/Schaal_van_Beaufort',
          'Windkracht 8 loopt van 62 tot 74 km/u. Het opgegeven 75 hoort al bij windkracht 9.'),
    1134: ('bevestigd', 'https://www.cdc.gov/niosh/noise/about/noise.html',
           'Een normaal gesprek zit rond de zestig decibel.'),
    1140: ('bevestigd', 'https://nl.wikipedia.org/wiki/Schaal_van_Beaufort',
           'Windkracht 5 loopt van 8,0 tot 10,7 meter per seconde.'),
    1141: ('bevestigd', 'https://nl.wikipedia.org/wiki/Geluidssnelheid',
           'Bij 20 graden is de geluidssnelheid 343 m/s, oftewel 1235 km/u.'),

    # ================= Politiek en recht =================
    1198: ('onbruikbaar', '', '"Koppen" is hier onzin, en het antwoord staat in de vraag.'),
    1219: ('natellen', 'https://www.rijksoverheid.nl/onderwerpen/defensie',
           'Het defensiebudget verschilt per begrotingsjaar.'),
    1251: ('bevestigd', 'https://www.un.org/en/about-us/universal-declaration-of-human-rights',
           'De Universele Verklaring telt dertig artikelen.'),
    1255: ('bevestigd', 'https://www.archives.gov/electoral-college/allocation',
           'Californie heeft 54 kiesmannen.'),
    1257: ('bevestigd', 'https://www.archives.gov/electoral-college/about',
           'Van de 538 kiesmannen zijn er 270 nodig voor een meerderheid.'),
    1258: ('onbruikbaar', '', 'Saoedi-Arabie heeft geen emiraten. Het land kent dertien provincies; '
           'de vraag noemt de verkeerde bestuurlijke eenheid.'),
    1259: ('bevestigd', 'https://www.aph.gov.au/', 'Een termijn duurt maximaal drie jaar.'),
    1260: ('bevestigd', 'https://www.parliament.nz/', 'Een parlementstermijn duurt drie jaar.'),
    1261: ('bevestigd', 'https://www.senate.gov/', 'Een senaatstermijn duurt zes jaar.'),
    1264: ('bevestigd', 'https://en.wikipedia.org/wiki/Central_African_CFA_franc',
           'Zes landen gebruiken de Centraal-Afrikaanse CFA-frank.'),
    1265: ('bevestigd', 'https://en.wikipedia.org/wiki/West_African_CFA_franc',
           'Acht landen gebruiken de West-Afrikaanse CFA-frank.'),
    1269: ('bevestigd', 'https://en.wikipedia.org/wiki/Community_of_Latin_American_and_Caribbean_States',
           'De CELAC telt 33 lidstaten.'),
    1273: ('bevestigd', 'https://asean.org/member-states/', 'De ASEAN telt tien leden.'),
    1277: ('bevestigd', 'https://www.saarc-sec.org/', 'De SAARC telt acht leden.'),
    1283: ('bevestigd', 'https://en.wikipedia.org/wiki/Provinces_of_Argentina',
           'Argentinie telt 23 provincies plus de autonome stad Buenos Aires.'),
    1287: ('onbruikbaar', '', 'De vraag vraagt naar "rechterzittingen"; bedoeld is het aantal '
           'rechters, en dat zijn er negen.'),
    1289: ('bevestigd', 'https://www.australia.gov.au/', 'Zes staten en twee territoria.'),
    1293: ('natellen', 'https://www.parliament.nz/', 'Het aantal zetels schommelt rond de 120.'),
    1294: ('bevestigd', 'https://www.aph.gov.au/', 'Het Huis van Afgevaardigden telt 151 zetels.'),
}
