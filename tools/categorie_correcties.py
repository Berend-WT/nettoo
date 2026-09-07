# -*- coding: utf-8 -*-
"""Netto — handmatig vastgestelde categoriecorrecties op de vragenbank.

WAAROM DIT BESTAND BESTAAT
De categorie van een vraag is niet louter administratie: hij bepaalt welk icoon
op de landingspagina onder de daily verschijnt. Stond een honkbalvraag onder
"Dieren", dan tekende de site een pootafdruk boven een vraag over honkbal. Bij
een steekproef van de 862 vragen die daadwerkelijk in puzzels zitten, bleken er
102 een categorie te hebben die niet bij de vraag past.

De correcties hieronder zijn stuk voor stuk met de hand vastgesteld door alle
1510 vragen te lezen. Er zit geen classificatie-algoritme achter, juist omdat
een trefwoordenmatch de fouten maakt die we hier repareren ("gitaar" bevat geen
woord dat naar Muziek wijst als je op "snaren" filtert, en "snaren" komt ook in
de harpvraag onder Boeken voor).

TWEE PRINCIPES
1. Een categorie beschrijft het ONDERWERP, niet het land. Daarom verdwijnt
   "Nederlands" als categorie: die 122 vragen krijgen hun echte onderwerp. Dat
   Nederland-zijn leeft verder als race-set, waar het thuishoort.
2. "Topografie" en "Geografie" beschreven hetzelfde ("Hoeveel landen grenzen
   aan X?" stond in allebei). Topografie gaat op in Geografie.
"""

# ---------------------------------------------------------------------------
# 1. Categorieën die verdwijnen, met waar hun vragen heen gaan.
# ---------------------------------------------------------------------------

OPGEHEVEN_CATEGORIEEN = {
    'Topografie': 'gaat volledig op in Geografie',
    'Nederlands': 'wordt een race-set; vragen krijgen hun eigen onderwerp',
}

# Topografie bevatte uitsluitend geografie: landsgrenzen, provincies, vlaggen.
TOPOGRAFIE_NAAR_GEOGRAFIE = [562, 563, 564, 565, 566, 567, 568, 1482, 1483, 1484, 1485]


# ---------------------------------------------------------------------------
# 2. De 122 vragen uit "Nederlands", op onderwerp.
# ---------------------------------------------------------------------------

NEDERLANDS_NAAR_ONDERWERP = {
    # Bouwwerken en waterwerken
    61: 'Gebouwen en infrastructuur',    420: 'Gebouwen en infrastructuur',
    421: 'Gebouwen en infrastructuur',   1189: 'Gebouwen en infrastructuur',
    1191: 'Gebouwen en infrastructuur',  1213: 'Gebouwen en infrastructuur',
    1214: 'Gebouwen en infrastructuur',  1215: 'Gebouwen en infrastructuur',
    1223: 'Gebouwen en infrastructuur',  1240: 'Gebouwen en infrastructuur',
    1243: 'Gebouwen en infrastructuur',  1247: 'Gebouwen en infrastructuur',
    1248: 'Gebouwen en infrastructuur',

    # Vervoer en netwerken
    62: 'Vervoer',    63: 'Vervoer',    414: 'Vervoer',   416: 'Vervoer',
    1180: 'Vervoer',  1181: 'Vervoer',  1184: 'Vervoer',  1186: 'Vervoer',
    1188: 'Vervoer',  1196: 'Vervoer',  1217: 'Vervoer',  1229: 'Vervoer',
    1232: 'Vervoer',  1242: 'Vervoer',

    # Land en bevolking
    412: 'Geografie',   417: 'Geografie',   418: 'Geografie',   422: 'Geografie',
    1151: 'Geografie',  1162: 'Geografie',  1164: 'Geografie',  1167: 'Geografie',
    1173: 'Geografie',  1185: 'Geografie',  1187: 'Geografie',  1193: 'Geografie',
    1197: 'Geografie',  1202: 'Geografie',  1206: 'Geografie',  1218: 'Geografie',
    1225: 'Geografie',  1226: 'Geografie',  1227: 'Geografie',  1231: 'Geografie',
    1238: 'Geografie',

    # Staat en bestuur
    410: 'Politiek en recht',   413: 'Politiek en recht',
    1205: 'Politiek en recht',  1207: 'Politiek en recht',
    1219: 'Politiek en recht',

    # Sport
    1143: 'Sport',  1145: 'Sport',  1166: 'Sport',  1176: 'Sport',
    1178: 'Sport',  1179: 'Sport',  1183: 'Sport',  1200: 'Sport',
    1211: 'Sport',  1233: 'Sport',  1235: 'Sport',  1245: 'Sport',

    # Geschiedenis en koningshuis
    1144: 'Geschiedenis',  1147: 'Geschiedenis',  1149: 'Geschiedenis',
    1150: 'Geschiedenis',  1194: 'Geschiedenis',

    # Eten en drinken
    1160: 'Eten & drinken',  1170: 'Eten & drinken',  1171: 'Eten & drinken',
    1172: 'Eten & drinken',  1208: 'Eten & drinken',  1222: 'Eten & drinken',

    # Kunst, cultuur en musea
    1165: 'Kunst en cultuur',  1224: 'Kunst en cultuur',
    1234: 'Kunst en cultuur',  1239: 'Kunst en cultuur',

    # Overige onderwerpen
    411: 'Milieu en duurzaamheid',   415: 'Milieu en duurzaamheid',
    1210: 'Milieu en duurzaamheid',
    419: 'Technologie',
    1148: 'Sterrenkunde & ruimte',
    1154: 'Taal',
    1158: 'Films en series',
    1195: 'Muziek',
    1209: 'Landbouw en industrie',   1220: 'Landbouw en industrie',
    1221: 'Reizen en toerisme',
    1228: 'Dagelijks leven',
    1230: 'Economie & geld',
    1244: 'Dieren',

    # Vragen die inhoudelijk stuk zijn (zie KAPOTTE_VRAGEN). Ze krijgen het
    # dichtstbijzijnde onderwerp zodat er geen lege categorie ontstaat, maar
    # het advies is ze te schrappen.
    1146: 'Dagelijks leven',            1152: 'Economie & geld',
    1153: 'Politiek en recht',          1155: 'Muziek',
    1156: 'Sport',                      1157: 'Kunst en cultuur',
    1159: 'Geografie',                  1161: 'Vervoer',
    1163: 'Economie & geld',            1168: 'Natuurkunde',
    1169: 'Gebouwen en infrastructuur', 1174: 'Eten & drinken',
    1175: 'Spellen en speelgoed',       1177: 'Dagelijks leven',
    1182: 'Geografie',                  1190: 'Gebouwen en infrastructuur',
    1192: 'Gebouwen en infrastructuur', 1198: 'Politiek en recht',
    1199: 'Eten & drinken',             1201: 'Sport',
    1203: 'Geschiedenis',               1204: 'Politiek en recht',
    1212: 'Gebouwen en infrastructuur', 1216: 'Gebouwen en infrastructuur',
    1236: 'Gebouwen en infrastructuur', 1237: 'Economie & geld',
    1241: 'Geografie',                  1246: 'Reizen en toerisme',
}


# ---------------------------------------------------------------------------
# 3. Losse indelingsfouten in de overige categorieën.
# ---------------------------------------------------------------------------

LOSSE_CORRECTIES = {
    # Stonden onder Boeken en literatuur, maar gaan nergens over een boek.
    129: 'Gebouwen en infrastructuur',   # de Afsluitdijk
    139: 'Sterrenkunde & ruimte',        # de manen van Mars
    140: 'Muziek',                       # een concert-pedaalharp
    625: 'Muziek',                       # een akoestische gitaar
    629: 'Geschiedenis',                 # de eerste universiteit

    # Stonden onder Dagelijks leven, dat een verzamelbak was geworden.
    145: 'Geografie',      # vlag van België
    631: 'Geografie',      # vlag van Zuid-Afrika
    630: 'Technologie',    # IPv4-adressen
    147: 'Biologie & gezondheid',  # stappen per dag

    # Stonden onder Dieren.
    667: 'Geografie',              # een Chinese berg
    633: 'Landbouw en industrie',  # imkerij, geen diersoort
    673: 'Kunst en cultuur',       # de Chinese dierenriem

    # Stonden onder Films en series.
    200: 'Boeken en literatuur',   # de Hunger Games-bóeken
    748: 'Boeken en literatuur',   # woorden in de Harry Potter-boeken
    746: 'Reizen en toerisme',     # themaparken van Walt Disney World

    # Stonden onder Gebouwen en infrastructuur.
    227: 'Vervoer',           # klinknagels in de romp van de Titanic
    814: 'Kunst en cultuur',  # het Terracottaleger

    # Stonden onder Geografie, maar gaan over taal, politiek of geschiedenis.
    292: 'Taal',          955: 'Taal',          956: 'Taal',   957: 'Taal',
    286: 'Politiek en recht',   928: 'Politiek en recht',
    303: 'Geschiedenis',  304: 'Geschiedenis',  305: 'Geschiedenis',
    306: 'Geschiedenis',

    # Stonden onder Geschiedenis.
    43: 'Gebouwen en infrastructuur',  # de hoogte van de Burj Khalifa
    311: 'Biologie & gezondheid',      # chromosomen in een cel
    322: 'Taal',                       # letters in het Latijnse alfabet
    344: 'Geografie',                  # rijafstand Amsterdam-Parijs
    1023: 'Wiskunde',                  # uren in een kalenderjaar
    1024: 'Dagelijks leven',           # vellen in een riem printpapier
    1059: 'Geografie',                 # de hoogte van de Mount Everest

    # Stonden onder Kunst en cultuur.
    349: 'Sterrenkunde & ruimte',       # dwergplaneten
    350: 'Wiskunde',                    # graden in een cirkel
    1061: 'Wiskunde',                   # graden in een rechte hoek
    352: 'Gebouwen en infrastructuur',  # hoogte Vrijheidsbeeld
    353: 'Taal',                        # talen in Zuid-Afrika

    # Stond onder Mode en lifestyle.
    54: 'Wiskunde',   # graden in een gestrekte hoek

    # Stonden onder Natuurkunde.
    402: 'Biologie & gezondheid',   # hartslagen per dag
    401: 'Muziek',                  # de kamertoon a
    400: 'Mode en lifestyle',       # facetten van een geslepen diamant
    403: 'Sterrenkunde & ruimte',   # baansnelheid van de aarde
    406: 'Geografie',               # de groei van de Mount Everest
    60: 'Geografie',                # verschuiving van de aardplaten
    1137: 'Sterrenkunde & ruimte',  # de Karmanlijn
    1138: 'Geografie',              # de Challengerdiepte

    # Stonden onder Politiek en recht.
    1249: 'Geografie',  1250: 'Geografie',  1268: 'Geografie',  # bevolking, landen
    430: 'Taal',        1282: 'Taal',                            # officiële talen

    # Stonden onder Records en vergelijkingen.
    458: 'Sport',                       # capaciteit van een stadion
    450: 'Gebouwen en infrastructuur',  # steenblok van de piramide van Cheops

    # Stonden onder Technologie.
    551: 'Wiskunde',   # zijden van een zeshoek
    1455: 'Vervoer',   # de Shanghai Maglev
    1461: 'Vervoer',   # de Shinkansen

    # Stonden onder Vervoer, maar het zijn bouwwerken.
    96: 'Gebouwen en infrastructuur',    # hoogte Golden Gate Bridge
    569: 'Gebouwen en infrastructuur',   # hoofdkabels Golden Gate Bridge
    1491: 'Gebouwen en infrastructuur',  # rijstroken Golden Gate Bridge
    570: 'Gebouwen en infrastructuur',   # de Kanaaltunnel
    571: 'Gebouwen en infrastructuur',   # het Suezkanaal

    # Stond onder Economie & geld.
    177: 'Politiek en recht',  # lidstaten van de EU
}


# ---------------------------------------------------------------------------
# 4. Vragen die inhoudelijk stuk zijn. Advies: schrappen.
# ---------------------------------------------------------------------------
# Deze zijn niet fout gecategoriseerd maar fout gegenereerd: samengeplakte
# vraagzinnen, redactienotities die in de vraag zijn blijven staan, eenheden die
# elkaar tegenspreken, of een aanname die feitelijk onjuist is. Ik verwijder ze
# niet zelf — dat is jouw kolom "Verwijderen".

KAPOTTE_VRAGEN = {
    1033: 'Twee vragen aan elkaar geplakt, en feitelijk omgekeerd: Japan viel de VS aan bij Pearl Harbor, niet andersom.',
    1472: 'Bevat de redactienotitie "nee Toyota is auto (1885 Daimler - dit zit niet in Azië)".',
    1063: 'Bevat de redactienotitie "sorry dat zit niet in Europa!"; "natuursonden" is bovendien geen woord.',
    985: 'Geen getalsvraag: vraagt naar een naam, terwijl het spel een getal nodig heeft.',
    1058: 'Schrijffout "In welk year"; ook een bijna-duplicaat van vraag 337.',
    837: 'Onleesbaar geformuleerd ("liggen er niet op het vasteland (exclusief eilanden) als eilandstaten").',
    1070: 'Onleesbaar: "sleutelvakken" gemeten "in cm hoogte" slaat nergens op.',
    808: 'Onleesbaar: "rivieren bruggen telt Sydney Harbour".',
    777: 'Vraagt naar kilometers maar wil de hoogte van een standbeeld in meters.',
    1374: '"Kuiven" bestaat niet in deze betekenis; bedoeld zijn honkholtes of bases.',
    1394: 'Dubbele ontkenning ("telt een etappe bijna nooit") maakt het onbeantwoordbaar.',
    1376: '"Europese voetbalkampioenscompetitie" bestaat niet als toernooi met landen.',
    1400: '"Rings" is Engels blijven staan; het NBA-logo heeft geen ringen.',
    1420: '"NASA-mannetjes missies" is geen Nederlands.',
    1116: 'Onafgemaakte zin: "koto-ensemble van hoort".',
    1119: 'Feitelijk onjuist: een djembé is een trommel en heeft geen snaren.',
    1124: 'Verwart twee instrumenten: een guitarrón is geen bajo sexto.',
    1287: 'Vraagt naar "rechterzittingen"; bedoeld is het aantal rechters.',
    1258: 'Feitelijk onjuist: Saoedi-Arabië heeft geen emiraten.',
    1146: 'Het antwoord staat letterlijk in de vraag ("vier cijfers plus twee letters").',
    1152: 'Onleesbaar: "banen ... in het monetaire bestuur".',
    1153: '"Biljarten in het Binnenhof" is verzonnen.',
    1155: '"Bruggetje van Sainte Anneï" bestaat niet; de vraag ontkent zichzelf.',
    1156: '"Alvleeskliervlaamse Wielerweek" is verzonnen (alvleesklier = orgaan).',
    1157: 'Verzonnen meeteenheid: "per seizoensblok".',
    1159: 'Amsterdam is één gemeente zonder dorpen; onbeantwoordbaar.',
    1161: 'Onleesbaar: "duikboten ... standaard per vloot".',
    1163: 'Verzonnen: er bestaat geen "duizendguldenbiljet-collectie uit 1970".',
    1168: 'Water kookt niet anders in een Nederlandse keuken; verzonnen premisse.',
    1169: 'Verzonnen aantal grafkelders, niet verifieerbaar.',
    1174: 'Verzonnen: kaasmarkten worden niet als weektotaal geteld.',
    1175: '"Kapstokkaarten" bestaan niet in Mens-erger-je-niet.',
    1177: 'Spreekt zichzelf tegen: "per jaar" versus "driejaarlijkse".',
    1182: 'De Bollenstreek heeft geen gedefinieerde kustlijnlengte.',
    1190: 'Vraagt kilometers maar wil tientallen meters.',
    1192: 'Vraagt kilometers maar wil tientallen meters.',
    1198: '"Koppen" is hier onzin; het antwoord staat in de vraag.',
    1199: 'Verzonnen: er bestaat geen standaard "kroegbord van biertjes".',
    1201: 'Een nationaal kampioenschap heeft per definitie één land.',
    1203: 'De VOC kocht geen landen; feitelijk onjuiste premisse.',
    1204: 'Verzonnen stemming; zo werkt de EU-talenregeling niet.',
    1212: 'Verwart diepte met doorvaarthoogte.',
    1216: 'Onleesbaar: "Maasvlakte²-stormvloedkering maasvlakte".',
    1236: 'Het aantal stenen per m² is geen vaststaand getal.',
    1237: 'Verzonnen: "het Energiepunt" is geen beurs.',
    1241: 'Het antwoord staat in de vraag; "UdK-tier" bestaat niet.',
    1246: '"Wilde knuffels ... qua attracties" is onleesbaar.',
}


# ---------------------------------------------------------------------------
# 5. Schrijffouten in vragen die verder prima zijn.
# ---------------------------------------------------------------------------

SPELFOUTEN = {
    633: ('producert', 'produceert'),
    690: ('Hoeveelkg', 'Hoeveel kg'),
    717: ('theedrinkt', 'drinkt'),
    956: ('erkennt', 'erkent'),
    955: ('officiele', 'officiële'),
    718: ('drinkt', 'gebruikt'),  # je drinkt geen olijfolie
}


def alle_correcties():
    """Bouwt de volledige map van vraagnummer -> nieuwe categorie."""
    samen = {}
    for nr in TOPOGRAFIE_NAAR_GEOGRAFIE:
        samen[nr] = 'Geografie'
    samen.update(NEDERLANDS_NAAR_ONDERWERP)
    samen.update(LOSSE_CORRECTIES)
    return samen
