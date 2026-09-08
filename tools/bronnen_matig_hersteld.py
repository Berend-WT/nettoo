# -*- coding: utf-8 -*-
"""Netto — herstel van de 42 bronnen met vertrouwen "matig".

Deze bronnen kwamen uit de geautomatiseerde ronde. Het getal stond wel op de
gevonden pagina, maar de pagina ging vaak over iets heel anders: het gewicht van
een wombat verwees naar het artikel "Kilogram", de snelheid van een tuinslak
naar "Electricity meter", en de punten voor een touchdown naar "American Idol
season 7". Dat is precies de valse bevestiging waar de matig-markering voor
bedoeld was.

Hier krijgt elke vraag met de hand een bron over het juiste onderwerp. De
antwoorden zijn opnieuw beoordeeld; twee vragen deugen niet en een antwoord is
fout.
"""

M = {
    61: ('bevestigd', 'https://nl.wikipedia.org/wiki/Euromast',
         'De Euromast is met de Space Tower uit 1970 in totaal 185 meter hoog.'),
    186: ('bevestigd', 'https://nl.wikipedia.org/wiki/Mars_%28reep%29',
          'Een standaard Mars weegt 51 gram.'),
    207: ('veroudert', 'https://en.wikipedia.org/wiki/List_of_The_Simpsons_episodes',
          'De serie loopt door; elk vast seizoensaantal veroudert. De oude bron was de pagina '
          'van seizoen 35 zelf.'),
    352: ('bevestigd', 'https://nl.wikipedia.org/wiki/Vrijheidsbeeld_%28New_York%29',
          'Inclusief voetstuk is het beeld 93 meter hoog; het beeld alleen 46 meter.'),
    396: ('bevestigd', 'https://en.wikipedia.org/wiki/Queen_discography',
          'Queen bracht vijftien studioalbums uit.'),
    447: ('bevestigd', 'https://en.wikipedia.org/wiki/Bluey_(long-lived_dog)',
          'Bluey werd 29 jaar en 5 maanden. Bobi nam de titel in 2023 over, maar Guinness trok '
          'die in 2024 weer in. De oude bron was een lijst van oudste mensen.'),
    622: ('bevestigd', 'https://en.wikipedia.org/wiki/Harry_Potter',
          'De reeks telt zeven delen.'),
    627: ('natellen', 'https://en.wikipedia.org/wiki/Shakespeare%27s_plays',
          'Ongeveer 39 stukken; het exacte getal hangt af van welke medegeschreven stukken '
          'meetellen. Dubbel met vraag 142.'),
    653: ('natellen', 'https://en.wikipedia.org/wiki/Wombat',
          'Wombats wegen tussen de 20 en 35 kilo; dertig is een middenwaarde, geen vast getal. '
          'De oude bron was het artikel "Kilogram".'),
    665: ('bevestigd', 'https://en.wikipedia.org/wiki/Cornu_aspersum',
          'De gewone tuinslak haalt ongeveer 1,3 centimeter per seconde, oftewel bijna vijftig '
          'meter per uur. De oude bron ging over elektriciteitsmeters.'),
    678: ('natellen', 'https://en.wikipedia.org/wiki/List_of_birds_of_Australia',
          'De soortenlijst is te tellen maar wisselt met de taxonomie; rond de 830.'),
    710: ('veroudert', 'https://en.wikipedia.org/wiki/Coffee_production_in_Brazil',
          'De Braziliaanse oogst schommelt sterk per jaar rond de zestig miljoen zakken.'),
    712: ('veroudert', 'https://en.wikipedia.org/wiki/Argentine_cuisine',
          'De rundvleesconsumptie per hoofd in Argentinie daalt al jaren; rond de vijftig kilo. '
          'De oude bron was het artikel "Kilogram".'),
    715: ('natellen', 'https://en.wikipedia.org/wiki/List_of_countries_by_coffee_production',
          'De lijst is te tellen, maar hoeveel Afrikaanse landen koffie produceren hangt af van '
          'de ondergrens die je aanhoudt. De oude bron ging over de Afrikaanse Unie.'),
    739: ('bevestigd', 'https://en.wikipedia.org/wiki/Star_Wars',
          'De Skywalker-saga telt negen films. De oude bron ging over een attractie in Disneyland.'),
    763: ('bevestigd', 'https://en.wikipedia.org/wiki/Five_Pillars_of_Islam',
          'Vijf gebeden per dag. De oude bron ging over moslims in Nepal. Dubbel met vraag 211.'),
    779: ('bevestigd', 'https://nl.wikipedia.org/wiki/Chinese_Muur',
          'De officiele meting uit 2012 komt op 21.196 kilometer. Dubbel met vraag 858.'),
    790: ('bevestigd', 'https://nl.wikipedia.org/wiki/Christus_de_Verlosser_%28Rio_de_Janeiro%29',
          'Het beeld is 38 meter hoog inclusief sokkel.'),
    798: ('bevestigd', 'https://en.wikipedia.org/wiki/Tokyo_Tower',
          'De Tokyo Tower is 333 meter hoog. De oude bron was het artikel over de Skytree.'),
    799: ('bevestigd', 'https://nl.wikipedia.org/wiki/Cairo_Tower',
          'De Cairo Tower is 187 meter hoog.'),
    837: ('onbruikbaar', '',
          'De vraag spreekt zichzelf tegen: "niet op het vasteland (exclusief eilanden)". '
          'Bovendien zijn Ierland, Malta en Cyprus alle drie eilandstaten in de EU, dus het '
          'antwoord twee klopt hoe dan ook niet.'),
    929: ('bevestigd', 'https://nl.wikipedia.org/wiki/Victoriawatervallen',
          'De watervallen vormen een gordijn van 1708 meter breed.'),
    956: ('bevestigd', 'https://en.wikipedia.org/wiki/Languages_of_India',
          'De achtste bijlage van de grondwet erkent 22 talen.'),
    988: ('fout', 'https://en.wikipedia.org/wiki/Seven_Wonders_of_the_Ancient_World',
          'Het zijn er vijf, niet vier: de piramide van Gizeh en de vuurtoren van Alexandrie in '
          'Noord-Afrika, en de hangende tuinen, de Artemistempel en het mausoleum van '
          'Halicarnassus in Azie. Alleen Rhodos en Olympia lagen in Europa.'),
    1027: ('bevestigd', 'https://nl.wikipedia.org/wiki/Koreaanse_Oorlog',
           'De oorlog begon in 1950 en duurde tot 1953.'),
    1039: ('bevestigd', 'https://nl.wikipedia.org/wiki/Bolivia',
           'Bolivia werd op 6 augustus 1825 onafhankelijk.'),
    1048: ('bevestigd', 'https://en.wikipedia.org/wiki/Nelson_Mandela',
           'Mandela kwam op 11 februari 1990 vrij.'),
    1068: ('natellen', 'https://en.wikipedia.org/wiki/List_of_works_by_Vincent_van_Gogh',
           'Het Van Gogh Museum houdt ongeveer 860 schilderijen aan; negenhonderd is de ronde '
           'vuistregel. De oude bron ging over een herdenkingsmunt.'),
    1133: ('natellen', 'https://en.wikipedia.org/wiki/List_of_symphonies_by_Wolfgang_Amadeus_Mozart',
           'De genummerde symfonieen lopen tot 41, maar Mozart schreef er meer die buiten die '
           'nummering vallen.'),
    1163: ('onbruikbaar', '',
           '"De duizendguldenbiljet-collectie uit 1970" bestaat niet als begrip, en het '
           'antwoord een maakt elke deelsom stuk.'),
    1195: ('bevestigd', 'https://nl.wikipedia.org/wiki/Domtoren',
           'Het carillon van de Domtoren telt vijftig klokken. De oude bron was het algemene '
           'artikel over carillons.'),
    1249: ('veroudert', 'https://nl.wikipedia.org/wiki/Bevolking_van_China',
           'De bevolking van China krimpt sinds 2022; elk vast getal veroudert.'),
    1256: ('veroudert', 'https://en.wikipedia.org/wiki/United_States_Electoral_College',
           'Texas heeft veertig kiesmannen tot de herverdeling na de volkstelling van 2030.'),
    1296: ('bevestigd', 'https://nl.wikipedia.org/wiki/Parlement_van_Zuid-Afrika',
           'De Nationale Vergadering telt vierhonderd zetels.'),
    1352: ('bevestigd', 'https://en.wikipedia.org/wiki/Baseball',
           'Een wedstrijd telt negen innings. De oude bron ging over verlengingen.'),
    1359: ('bevestigd', 'https://en.wikipedia.org/wiki/FIFA_World_Cup',
           'Van 1930 tot en met 2022 werd het toernooi 22 keer gehouden. De oude bron was een '
           'groepspagina van het toernooi van 2026.'),
    1373: ('bevestigd', 'https://en.wikipedia.org/wiki/Marathon',
           'De marathon meet 42,195 kilometer, afgerond 42. Dubbel met vraag 1416, die om '
           'meters vraagt.'),
    1397: ('bevestigd', 'https://en.wikipedia.org/wiki/Touchdown',
           'Een touchdown levert zes punten op, met het extra point zeven. De oude bron ging '
           'over American Idol.'),
    1400: ('onbruikbaar', '',
           'Het NBA-logo is een silhouet van een basketballer en heeft geen ringen. De vraag '
           'klopt niet, en het antwoord een maakt elke deelsom stuk.'),
    1403: ('bevestigd', 'https://en.wikipedia.org/wiki/Handball',
           'Zeven spelers per ploeg op het veld. Dubbel met vraag 502. De oude bron ging over '
           'het Nederlands vrouwenteam.'),
    1448: ('bevestigd', 'https://en.wikipedia.org/wiki/SPQR',
           'SPQR telt vier letters. De oude bron ging over Latijnse vervoegingen.'),
    1461: ('bevestigd', 'https://nl.wikipedia.org/wiki/Shinkansen',
           'De eerste Shinkansen reed in 1964, het jaar van de Spelen in Tokio. Dubbel met '
           'vraag 1502.'),
}
