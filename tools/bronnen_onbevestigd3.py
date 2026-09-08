# -*- coding: utf-8 -*-
"""Netto — handmatige herbeoordeling van onbevestigde bronnen, blok 3.

Geschiedenis, kunst, landbouw, merken en milieu. Vervolg op blok 2.

Een terugkerend geval in dit blok: de bron is de juiste instantie — FAO, USGS,
UNEP, worldsteel — maar wijst naar een databankportaal of een themapagina in
plaats van naar een cijfer. Zulke cijfers wisselen bovendien per jaargang. Die
krijgen "natellen" of "veroudert": de vindplaats klopt, de bevestiging ontbreekt.

Ook bevestigd: de UNESCO-adressen die als opvulling over losse vragen waren
verspreid, horen echt bij een handvol vragen uit dit deel van de bank. Lijst 1631
is de Neder-Germaanse Limes en 1613 de Great Spa Towns — precies de twee vragen
die ze hier terugkrijgen.
"""

O3 = {
    # ================= Geschiedenis =================
    42: ('fout', 'https://en.wikipedia.org/wiki/1666_census_of_New_France',
         'De volkstelling van Jean Talon begon op 21 maart 1666, niet in 1665. Bovendien is '
         '"eerste moderne volkstelling ter wereld" betwist; het was de eerste van Noord-Amerika.'),
    306: ('bevestigd', 'https://en.wikipedia.org/wiki/Erdapfel',
          'Martin Behaim maakte in 1492 de Erdapfel, de oudste bewaarde wereldbol.'),
    310: ('bevestigd', 'https://en.wikipedia.org/wiki/Constitution_of_the_United_States',
          'Negenendertig van de tweeenveertig aanwezige afgevaardigden ondertekenden.'),
    312: ('bevestigd', 'https://whc.unesco.org/en/list/1631/',
          'De Neder-Germaanse Limes bestaat uit 102 onderdelen.'),
    313: ('bevestigd', 'https://en.wikipedia.org/wiki/List_of_pharaohs',
          'De indeling van Manetho kent 31 dynastieen.'),
    314: ('bevestigd', 'https://en.wikipedia.org/wiki/Giza_pyramid_complex',
          'Cheops, Chefren en Mykerinos gaven elk opdracht tot een van de drie piramides.'),
    315: ('natellen', 'https://en.wikipedia.org/wiki/Eighteenth_Dynasty_of_Egypt',
          'De lijst telt veertien of vijftien farao\'s, afhankelijk van of Smenkhkare apart '
          'wordt gerekend.'),
    318: ('bevestigd', 'https://en.wikipedia.org/wiki/Elizabeth_II',
          'Zij regeerde van 1952 tot 2022, zeventig jaar.'),
    319: ('bevestigd', 'https://en.wikipedia.org/wiki/Punic_Wars',
          'Van 264 tot 146 voor Christus is 118 jaar tussen begin en eind.'),
    320: ('bevestigd', 'https://whc.unesco.org/en/list/430/',
          'UNESCO beschrijft de rijksgrens als een lijn van ongeveer vijfduizend kilometer.'),
    321: ('bevestigd', 'https://en.wikipedia.org/wiki/Thirteen_Colonies',
          'Dertien koloniën verklaarden zich in 1776 onafhankelijk.'),
    323: ('bevestigd', 'https://en.wikipedia.org/wiki/Dunkirk_evacuation',
          'Er werden 338.226 militairen geevacueerd.'),
    325: ('natellen', 'https://en.wikipedia.org/wiki/Normandy_landings',
          'De drie luchtlandingsdivisies samen komen op ruwweg 23.000 man; het getal verschilt '
          'per bron en per definitie van "gedropt".'),
    327: ('natellen', 'https://en.wikipedia.org/wiki/Normandy_landings',
          'Ongeveer 7000 vaartuigen namen deel, waarvan een deel landingsvaartuigen. Zesduizend '
          'is een gangbare afronding, geen vaststaand getal.'),
    328: ('bevestigd', 'https://en.wikipedia.org/wiki/Spanish_Armada',
          'De vloot telde ongeveer 130 schepen.'),
    329: ('natellen', 'https://en.wikipedia.org/wiki/Dunkirk_evacuation',
          'De "kleine schepen" worden meestal op rond de 850 geteld, maar de lijsten lopen uiteen.'),
    330: ('bevestigd', 'https://en.wikipedia.org/wiki/Battle_of_Waterloo',
          'Frans, Brits-geallieerd en Pruisisch leger samen komen op ruim 190.000 man.'),
    331: ('bevestigd', 'https://en.wikipedia.org/wiki/Battle_of_Waterloo',
          'Napoleon had ongeveer 73.000 man bij Waterloo.'),
    332: ('bevestigd', 'https://en.wikipedia.org/wiki/French_invasion_of_Russia',
          'De Grande Armee telde bij de inval ongeveer 600.000 man.'),
    629: ('bevestigd', 'https://en.wikipedia.org/wiki/University_of_al-Qarawiyyin',
          'Al-Qarawiyyin in Fez werd in 859 gesticht en geldt als de oudste nog werkende '
          'universiteit.'),
    997: ('bevestigd', 'https://en.wikipedia.org/wiki/American_Revolutionary_War',
          'De oorlog liep van 1775 tot 1783, acht jaar.'),
    1006: ('natellen', 'https://en.wikipedia.org/wiki/Silk_Road',
           'De zevenduizend kilometer is een gangbare schatting; de route had geen vaste lengte.'),
    1009: ('bevestigd', 'https://en.wikipedia.org/wiki/Exposition_Universelle_(1889)',
           'De wereldtentoonstelling trok ongeveer 32 miljoen bezoekers.'),
    1010: ('bevestigd', 'https://en.wikipedia.org/wiki/World%27s_Columbian_Exposition',
           'De tentoonstelling in Chicago trok ongeveer 27,5 miljoen bezoekers.'),
    1019: ('bevestigd', 'https://en.wikipedia.org/wiki/Normandy_landings',
           'Op D-Day landden ongeveer 156.000 geallieerde militairen.'),
    1022: ('natellen', 'https://en.wikipedia.org/wiki/The_Blitz',
           'De achttienduizend ton geldt voor Londen alleen; tellingen verschillen per periode.'),
    1025: ('natellen', 'https://en.wikipedia.org/wiki/Normandy_landings',
           'Ongeveer elfduizend vliegtuigen namen deel; de tellingen lopen uiteen met de '
           'gekozen afbakening.'),

    # ================= Kunst en cultuur =================
    345: ('bevestigd', 'https://en.wikipedia.org/wiki/David_(Michelangelo)',
          'Het beeld is 517 centimeter hoog, zonder sokkel.'),
    351: ('bevestigd', 'https://en.wikipedia.org/wiki/UNESCO',
          'Zevenendertig landen ondertekenden de grondwet in november 1945.'),
    1071: ('bevestigd', 'https://whc.unesco.org/en/list/1613/',
           'De Great Spa Towns of Europe liggen in zeven landen.'),
    1072: ('bevestigd', 'https://en.wikipedia.org/wiki/Salvator_Mundi_(Leonardo)',
           'Het schilderij bracht in november 2017 450.312.500 dollar op bij Christie\'s.'),

    # ================= Landbouw en industrie =================
    45: ('veroudert', 'https://www.usgs.gov/centers/national-minerals-information-center/gold-statistics-and-information',
         'De USGS publiceert de mijnproductie jaarlijks; die schommelt rond de drieduizend ton.'),
    46: ('veroudert', 'https://www.usgs.gov/centers/national-minerals-information-center/cement-statistics-and-information',
         'Het Chinese aandeel ligt al jaren rond de helft, maar verschilt per jaargang.'),
    357: ('bevestigd', 'https://en.wikipedia.org/wiki/Cattle',
          'De draagtijd van een rund is ongeveer 283 dagen.'),
    358: ('fout', 'https://en.wikipedia.org/wiki/Sheep',
          'De draagtijd van een schaap is gemiddeld 147 dagen, met een spreiding van 142 tot '
          '152. Het opgegeven 152 is de bovengrens, niet het gemiddelde.'),
    361: ('veroudert', 'https://www.fao.org/statistics/en/',
          'Het aandeel van de wereldbevolking in de landbouw daalt gestaag; rond de kwart.'),
    362: ('veroudert', 'https://www.fao.org/faostat/en/#data/QCL',
          'FAOSTAT geeft de bananenproductie per jaar; rond de 135 miljoen ton.'),
    363: ('veroudert', 'https://www.usgs.gov/centers/national-minerals-information-center/copper-statistics-and-information',
          'De koperproductie ligt rond de 22 miljoen ton en verschilt per jaargang.'),
    364: ('veroudert', 'https://www.fao.org/faostat/en/#data/QCL',
          'FAOSTAT geeft de maisproductie per jaar; rond de 1,2 miljard ton.'),
    365: ('veroudert', 'https://www.fao.org/faostat/en/#data/QCL',
          'De suikerproductie ligt rond de 180 miljoen ton en verschilt per jaargang.'),
    366: ('veroudert', 'https://www.ilo.org/industries-and-sectors/agriculture-plantations-other-rural-sectors',
          'De ILO houdt ongeveer een miljard werkenden in de landbouw aan; het cijfer daalt.'),
    1074: ('bevestigd', 'https://en.wikipedia.org/wiki/Goat',
           'De draagtijd van een geit is ongeveer 150 dagen.'),
    1075: ('bevestigd', 'https://en.wikipedia.org/wiki/Domestic_pig',
           'De draagtijd van een varken is 114 dagen: drie maanden, drie weken en drie dagen.'),
    1076: ('natellen', 'https://en.wikipedia.org/wiki/Automotive_industry',
           'Ongeveer 900 kilo staal per auto is een gangbare vuistregel; het verschilt sterk '
           'per model.'),
    1078: ('veroudert', 'https://www.fao.org/faostat/en/#data/QCL',
           'FAOSTAT geeft de aardappelproductie per jaar; rond de 383 miljoen ton.'),
    1079: ('veroudert', 'https://www.usgs.gov/centers/national-minerals-information-center/aluminum-statistics-and-information',
           'De aluminiumproductie ligt rond de 70 miljoen ton en groeit.'),
    1080: ('veroudert', 'https://www.usgs.gov/centers/national-minerals-information-center/cement-statistics-and-information',
           'De cementproductie ligt rond de vier miljard ton.'),
    1081: ('veroudert', 'https://www.unep.org/interactives/beat-plastic-pollution/',
           'UNEP houdt ongeveer 400 miljoen ton plastic per jaar aan.'),
    1082: ('veroudert', 'https://www.fao.org/faostat/en/#data/QCL',
           'FAOSTAT geeft de rijstproductie per jaar; rond de 530 miljoen ton gepelde rijst.'),
    1083: ('veroudert', 'https://worldsteel.org/steel-topics/statistics/annual-crude-steel-production/',
           'Worldsteel publiceert de ruwstaalproductie per jaar; rond de 1,9 miljard ton.'),
    1084: ('veroudert', 'https://www.fao.org/faostat/en/#data/QCL',
           'FAOSTAT geeft de tarweproductie per jaar; rond de 785 miljoen ton.'),
    1086: ('veroudert', 'https://worldsteel.org/steel-topics/statistics/annual-crude-steel-production/',
           'Het Chinese aandeel ligt rond de vijftig procent en verschilt per jaargang.'),

    # ================= Merken en producten =================
    47: ('veroudert', 'https://en.wikipedia.org/wiki/Decathlon_(retailer)',
         'Decathlon heeft ruim 1700 winkels; het aantal groeit.'),
    368: ('veroudert', 'https://en.wikipedia.org/wiki/Starbucks',
          'Starbucks passeerde 40.000 vestigingen; het aantal groeit per kwartaal.'),
    369: ('veroudert', 'https://corporate.mcdonalds.com/content/dam/sites/corp/nfl/pdf/Restaurants%20by%20Market%202023.pdf',
          'Eind 2023 waren het er 41.822, inmiddels ruim 43.000. Het antwoord 42.000 klopt '
          'als afronding voor 2023 maar loopt achter.'),
    1087: ('veroudert', 'https://en.wikipedia.org/wiki/KFC',
           'KFC heeft rond de 30.000 vestigingen; het aantal groeit.'),

    # ================= Milieu en duurzaamheid =================
    50: ('natellen', 'https://en.wikipedia.org/wiki/Great_Barrier_Reef',
         'Koraalrif beslaat ongeveer zeven procent van het beschermde gebied; dat is een '
         'afgeleide van oppervlaktecijfers, geen genoemd getal.'),
    51: ('bevestigd', 'https://en.wikipedia.org/wiki/Earth',
         'Land beslaat 29 procent van het aardoppervlak.'),
    52: ('bevestigd', 'https://en.wikipedia.org/wiki/Earth',
         'Water beslaat 71 procent van het aardoppervlak.'),
    53: ('bevestigd', 'https://www.usgs.gov/special-topics/water-science-school/science/where-earths-water',
         'Bijna zeventig procent van het zoete water zit vast in ijs en gletsjers.'),
    370: ('veroudert', 'https://www.fao.org/interactive/forest-resources-assessment/2020/en/',
          'De FAO-beoordeling van 2020 geeft een netto verlies van rond de 4,7 miljoen hectare '
          'per jaar; de volgende ronde geeft een ander cijfer.'),
    371: ('natellen', 'https://en.wikipedia.org/wiki/Water_footprint',
          'De vijftienduizend liter is de gangbare mondiale gemiddelde watervoetafdruk; de '
          'spreiding per productiesysteem is enorm.'),
    372: ('veroudert', 'https://www.unep.org/interactives/beat-plastic-pollution/',
          'De schatting van jaarlijkse plasticlekkage naar zee wordt regelmatig bijgesteld.'),
    378: ('bevestigd', 'https://en.wikipedia.org/wiki/Water_resources',
          'Ongeveer zeventig procent van het zoetwatergebruik gaat naar landbouw.'),
    1090: ('veroudert', 'https://climate.nasa.gov/vital-signs/carbon-dioxide/',
           'De CO2-concentratie stijgt jaarlijks met ruim twee ppm; elk vast getal veroudert.'),
    1091: ('bevestigd', 'https://en.wikipedia.org/wiki/Carbon_dioxide_in_Earth%27s_atmosphere',
           'De pre-industriele concentratie wordt op ongeveer 280 ppm gesteld.'),
    1094: ('natellen', 'https://www.fao.org/food-loss-reduction/en/',
           'De dertig procent volgt uit de verhouding tussen voedselverlies en landgebruik; '
           'de FAO noemt dat percentage niet als zodanig.'),
    1095: ('natellen', 'https://www.fao.org/interactive/forest-resources-assessment/2020/en/',
           'De FAO meldt dat ongeveer een derde van de bossen primair bos is. Of dat hetzelfde '
           'is als "oorspronkelijke bossen die over zijn" is een interpretatie.'),
    1097: ('bevestigd', 'https://en.wikipedia.org/wiki/Global_Assessment_Report_on_Biodiversity_and_Ecosystem_Services',
           'Het IPBES-rapport uit 2019 noemt ongeveer een miljoen bedreigde soorten.'),
    1098: ('veroudert', 'https://www.unep.org/interactives/beat-plastic-pollution/',
           'UNEP houdt ongeveer 400 miljoen ton plastic afval per jaar aan; dubbel met 1081.'),
    1099: ('bevestigd', 'https://www.unep.org/interactives/beat-plastic-pollution/',
           'UNEP stelt dat minstens 85 procent van het mariene afval uit plastic bestaat.'),
    1100: ('veroudert', 'https://www.oecd.org/environment/plastics/',
           'De OESO-verdeling tussen storten, verbranden en recyclen wisselt per editie.'),
}
