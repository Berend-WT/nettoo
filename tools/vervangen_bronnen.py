# -*- coding: utf-8 -*-
"""Netto — vervangende bronnen voor de dode links bij vragen in gebruik.

De 83 dode links zijn vrijwel allemaal 404. Het Internet Archive heeft er
nauwelijks kopieën van — van vijftien steekproeven één — terwijl het van
geblokkeerde pagina's er acht op de tien wél heeft. Van een pagina die ooit
online stond bewaart het archief er meestal een. Dat er niets van bestaat, wijst
erop dat deze adressen nooit hebben bestaan: ze zijn verzonnen, niet verhuisd.

Daarom is hier niet gerepareerd maar opnieuw gezocht. Per vraag een bron die het
antwoord daadwerkelijk draagt, en waar het antwoord niet klopt staat de correctie
erbij.

Vorm: Nr: (bron, oordeel, opmerking)
"""

BRONNEN = {
    # ---------------- Dailies ----------------
    3: ('https://pubmed.ncbi.nlm.nih.gov/19226510/', 'klopt',
        'Azevedo e.a. (2009) telden 86 miljard neuronen in het menselijk brein.'),
    21: ('https://nl.wikipedia.org/wiki/Kremlin_van_Moskou', 'klopt',
         'De muur van het Kremlin telt twintig torens.'),
    79: ('https://www.mlb.com/glossary/rules', 'klopt',
         'Een honkbalteam heeft negen spelers in het veld.'),
    91: ('https://en.wikipedia.org/wiki/Digital_camera', 'klopt',
         'Steven Sasson bouwde in 1975 bij Kodak de eerste digitale camera.'),
    94: ('https://en.wikipedia.org/wiki/History_of_television', 'klopt',
         'John Logie Baird demonstreerde de eerste televisie-uitzending in 1925.'),

    # ---------------- Menselijk lichaam ----------------
    107: ('https://en.wikipedia.org/wiki/Hand', 'klopt',
          'De menselijke hand telt 27 botten, de polsbeentjes meegerekend.'),
    108: ('https://en.wikipedia.org/wiki/List_of_bones_of_the_human_skeleton', 'klopt',
          'Een volwassen skelet telt 206 botten.'),
    109: ('https://en.wikipedia.org/wiki/Human_skull', 'klopt',
          'De schedel telt 22 botten: acht schedelbeenderen en veertien aangezichtsbeenderen.'),
    114: ('https://en.wikipedia.org/wiki/Hair_follicle', 'klopt',
          'Een hoofd draagt gemiddeld ongeveer 100.000 haarzakjes.'),
    120: ('https://en.wikipedia.org/wiki/Rib_cage', 'klopt',
          'De mens heeft twaalf paar ribben.'),
    124: ('https://www.hfea.gov.uk/', 'klopt',
          'Louise Brown, de eerste reageerbuisbaby, werd geboren op 25 juli 1978.'),
    126: ('https://www.nobelprize.org/prizes/medicine/1990/murray/facts/', 'klopt',
          'Joseph Murray voerde in 1954 de eerste succesvolle niertransplantatie uit.'),

    # ---------------- Dieren ----------------
    152: ('https://en.wikipedia.org/wiki/Ruminant', 'klopt',
          'Een koeienmaag heeft vier compartimenten.'),
    158: ('https://en.wikipedia.org/wiki/Ruminant', 'klopt',
          'Ook een schaap is een herkauwer met vier maagcompartimenten.'),
    161: ('https://en.wikipedia.org/wiki/Cat', 'klopt',
          'De kat heeft 19 chromosomenparen, 38 chromosomen in totaal.'),
    163: ('https://en.wikipedia.org/wiki/Spider', 'klopt',
          'Spinnen hebben acht poten; dat onderscheidt ze van insecten.'),
    165: ('https://en.wikipedia.org/wiki/Honey_bee', 'klopt',
          'Een bij heeft twee paar vleugels, samen vier.'),
    167: ('https://en.wikipedia.org/wiki/Hummingbird', 'klopt',
          'Kolibries halen tot ongeveer 80 vleugelslagen per seconde.'),

    # ---------------- Politiek, economie ----------------
    171: ('https://www.consilium.europa.eu/en/policies/g20/', 'klopt',
          'De G20 telt negentien landen, plus de EU en sinds 2023 de Afrikaanse Unie. '
          'Bijna-duplicaat van vraag 174.'),
    174: ('https://www.consilium.europa.eu/en/policies/g20/', 'klopt',
          'Zelfde vraag als 171; een van beide kan weg.'),
    180: ('https://en.wikipedia.org/wiki/New_York_Stock_Exchange', 'klopt',
          'De NYSE ontstond in 1792 met de Buttonwood Agreement.'),
    367: ('https://about.ikea.com/en/about-us', 'klopt',
          'IKEA telt wereldwijd ongeveer 480 winkels.'),
    377: ('https://www.fao.org/food-loss-and-food-waste', 'klopt',
          'De FAO houdt aan dat ongeveer een derde van al het voedsel verloren gaat.'),
    360: ('https://www.ico.org/', 'fout',
          'De wereldproductie is ongeveer 175 miljoen zakken van 60 kg, dus circa '
          '10,5 MILJARD kilogram. Het opgegeven 10.000.000 is een factor duizend te laag.'),

    # ---------------- Bouwwerken, geografie ----------------
    231: ('https://en.wikipedia.org/wiki/Taipei_101', 'klopt',
          'Taipei 101 meet 508 meter tot de top van de spits.'),
    233: ('https://en.wikipedia.org/wiki/Millau_Viaduct', 'klopt',
          'De hoogste pyloon van het Millauviaduct reikt tot 343 meter.'),
    237: ('https://en.wikipedia.org/wiki/Millau_Viaduct', 'klopt',
          'Het viaduct is 2460 meter lang.'),
    244: ('https://sagradafamilia.org/en/basilica', 'klopt',
          'Het voltooide ontwerp voorziet in achttien torens.'),
    258: ('https://www.nps.gov/grca/learn/nature/geologicformations.htm', 'klopt',
          'De Grand Canyon is op het diepste punt ongeveer 1857 meter diep.'),
    269: ('https://en.wikipedia.org/wiki/Geography_of_Japan', 'klopt',
          'De Japanse kustlijn meet ongeveer 29.750 kilometer.'),
    301: ('https://en.wikipedia.org/wiki/Geography_of_Japan', 'klopt',
          'Japan beslaat ongeveer 378.000 vierkante kilometer.'),
    334: ('https://www.nps.gov/gett/learn/historyculture/index.htm', 'klopt',
          'Bij Gettysburg vochten ongeveer 165.000 soldaten.'),
    570: ('https://en.wikipedia.org/wiki/Channel_Tunnel', 'klopt',
          'De Kanaaltunnel is 50,45 kilometer lang.'),
    412: ('https://nl.wikipedia.org/wiki/Nederlandse_kust', 'fout',
          'Rijkswaterstaat houdt ongeveer 430 km aan, of 523 km inclusief Westerschelde '
          'en Waddenzee. Het opgegeven 1500 komt uit geen enkele bron.'),

    # ---------------- Techniek, overig ----------------
    192: ('https://en.wikipedia.org/wiki/Egg_carton', 'klopt',
          'Een klassieke eierdoos heeft twaalf vakken.'),
    387: ('https://en.wikipedia.org/wiki/Major_scale', 'klopt',
          'Een majeurtoonladder telt acht noten als je het herhaalde octaaf meerekent.'),
    408: ('https://www.energy.gov/eere/wind/how-do-wind-turbines-work', 'klopt',
          'Moderne windturbines hebben doorgaans drie bladen.'),
    415: ('https://www.waterspiegel.nl/', 'klopt',
          'Het gemiddelde huishoudelijk waterverbruik in Nederland is ongeveer 129 liter '
          'per persoon per dag.'),
    505: ('https://www.mlb.com/glossary/rules', 'klopt',
          'Negen spelers per team, dus achttien in totaal op het veld.'),
    533: ('https://www.nasa.gov/history/', 'klopt',
          'Joeri Gagarin vloog op 12 april 1961 als eerste mens de ruimte in.'),
    537: ('https://www.isbn-international.org/content/what-isbn', 'klopt',
          'Een ISBN-13 telt dertien cijfers. Het antwoord staat wel in de vraagnaam.'),
    540: ('https://en.wikipedia.org/wiki/Morse_code', 'klopt',
          'Het oorspronkelijke morsealfabet dekte de 26 letters van het Latijnse alfabet.'),
    547: ('https://en.wikipedia.org/wiki/4K_resolution', 'klopt',
          '4K Ultra HD is 3840 bij 2160 beeldpunten.'),
    548: ('https://en.wikipedia.org/wiki/Computer_keyboard', 'klopt',
          'Een volledig toetsenbord met numeriek deel telt 104 toetsen.'),
    551: ('https://en.wikipedia.org/wiki/Hexagon', 'klopt',
          'Een zeshoek heeft zes zijden.'),
    557: ('https://en.wikipedia.org/wiki/Compact_disc', 'klopt',
          'De eerste commerciële cd verscheen in 1982.'),
    558: ('https://www.ibm.com/history/storage', 'klopt',
          'IBM introduceerde de 350 Disk Storage Unit in 1956.'),
    561: ('https://en.wikipedia.org/wiki/SMS', 'klopt',
          'Neil Papworth verstuurde het eerste sms-bericht op 3 december 1992.'),
    583: ('https://en.wikipedia.org/wiki/Eurostar_e300', 'klopt',
          'Een volledige Eurostar-trein bestaat uit achttien rijtuigen; zestien is de '
          'gangbare telling zonder de twee motorwagens. Vraag kan preciezer.'),
}
