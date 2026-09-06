// Netto frontend module.
// Loaded as a classic script so the existing shared global scope stays intact.

// GEGENEREERD door fotos/maak_fotolijst_js.py — niet met de hand bijwerken.
//
// Gedeelde fotolijst voor de daily. Zowel het spel (sfeerfoto-rotatie) als het
// adminscherm (foto toewijzen) gebruiken deze lijst.
//
// De bronvermelding staat er bewust bij: deze foto's komen van Wikimedia
// Commons onder CC BY, CC BY-SA, CC0 of publiek domein, en bij de eerste twee
// is naamsvermelding een licentievoorwaarde.
window.NETTO_DAILY_PHOTOS = [
  {"file": "media-001-pia17172-saturn-eclipse-mosaic-bright-crop-jpg.jpg", "credit": "PIA17172 Saturn eclipse mosaic bright crop · NASA / JPL-Caltech / Space Science Institute · Public domain", "source": "https://commons.wikimedia.org/wiki/File:PIA17172_Saturn_eclipse_mosaic_bright_crop.jpg"},
  {"file": "media-002-bicycle-reflections-jpg.jpg", "credit": "Bicycle reflections · Tomascastelazo · CC BY-SA 3.0", "source": "https://commons.wikimedia.org/wiki/File:Bicycle_reflections.jpg"},
  {"file": "media-003-a380-f-wwea-legt-2-jpg.jpg", "credit": "A380 F-WWEA LEGT 2 · Keta · CC BY-SA 2.5", "source": "https://commons.wikimedia.org/wiki/File:A380_F-WWEA_LEGT_2.jpg"},
  {"file": "media-004-2000-human-heart-photo-jpg.jpg", "credit": "2000 Human Heart Photo · OpenStax Anatomy and Physiology · CC BY 4.0", "source": "https://commons.wikimedia.org/wiki/File:2000_Human_Heart_Photo.jpg"},
  {"file": "media-005-sydney-harbour-bridge-night-jpg.jpg", "credit": "Sydney Harbour Bridge night · Diliff · CC BY-SA 3.0", "source": "https://commons.wikimedia.org/wiki/File:Sydney_Harbour_Bridge_night.jpg"},
  {"file": "media-006-wilson-american-football-jpg.jpg", "credit": "Wilson American football · Torsten Bolten · CC BY-SA 3.0", "source": "https://commons.wikimedia.org/wiki/File:Wilson_American_football.jpg"},
  {"file": "media-007-golden-gate-bridge-by-night-jpg.jpg", "credit": "Golden Gate Bridge by night · Image taken by Daniel Schwen · CC BY-SA 3.0", "source": "https://commons.wikimedia.org/wiki/File:Golden_Gate_Bridge_by_night.jpg"},
  {"file": "media-008-dead-sea-by-david-shankbone-jpg.jpg", "credit": "Dead Sea by David Shankbone · David Shankbone · CC BY-SA 3.0", "source": "https://commons.wikimedia.org/wiki/File:Dead_Sea_by_David_Shankbone.jpg"},
  {"file": "media-009-flock-of-sheep-jpg.jpg", "credit": "Flock of sheep · Keith Weller · Public domain", "source": "https://commons.wikimedia.org/wiki/File:Flock_of_sheep.jpg"},
  {"file": "media-010-07-camel-profile-near-silverton-nsw-07-07-2007-jpg.jpg", "credit": "07. Camel Profile, near Silverton, NSW, 07.07.2007 · Jjron · CC BY-SA 3.0", "source": "https://commons.wikimedia.org/wiki/File:07._Camel_Profile,_near_Silverton,_NSW,_07.07.2007.jpg"},
  {"file": "media-011-rms-titanic-3-jpg.jpg", "credit": "RMS Titanic 3 · Francis Godolphin Osbourne Stuart · Public domain", "source": "https://commons.wikimedia.org/wiki/File:RMS_Titanic_3.jpg"},
  {"file": "media-012-aldrin-apollo-11-jpg.jpg", "credit": "Aldrin Apollo 11 · Neil A. Armstrong · Public domain", "source": "https://commons.wikimedia.org/wiki/File:Aldrin_Apollo_11.jpg"},
  {"file": "media-013-hagia-sophia-laengsschnitt-jpg.jpg", "credit": "Hagia-Sophia-Laengsschnitt · Wilhelm Lübke / Max Semrau: Grundriß der Kunstgeschichte. 14. Auflage. Paul Neff Verlag, Esslingen, 1908; German Wikipedia, original upload 28. Aug 2004 by Rainer Zenz · Public domain", "source": "https://commons.wikimedia.org/wiki/File:Hagia-Sophia-Laengsschnitt.jpg"},
  {"file": "media-014-candy-cane-on-tree-jpg.jpg", "credit": "Candy cane on tree · Matt Reinbold · CC BY 2.0", "source": "https://commons.wikimedia.org/wiki/File:Candy_cane_on_tree.jpg"},
  {"file": "media-015-united-nations-security-council-jpg.jpg", "credit": "United Nations Security Council · Patrick Gruban · CC BY-SA 2.0", "source": "https://commons.wikimedia.org/wiki/File:United_Nations_Security_Council.jpg"},
  {"file": "media-016-eq-it-na-pizza-margherita-sep2005-sml-jpg.jpg", "credit": "Eq it-na pizza-margherita sep2005 sml · Valerio Capello at English Wikipedia · CC BY-SA 3.0", "source": "https://commons.wikimedia.org/wiki/File:Eq_it-na_pizza-margherita_sep2005_sml.jpg"},
  {"file": "media-017-euro-stardikomplekt-jpg.jpg", "credit": "EURO stardikomplekt.JPG · Dmitry G · CC BY-SA 3.0", "source": "https://commons.wikimedia.org/wiki/File:EURO_stardikomplekt.JPG"},
  {"file": "media-018-marssunset-jpg.jpg", "credit": "MarsSunset · NASA/JPL/Texas A&M/Cornell · Public domain", "source": "https://commons.wikimedia.org/wiki/File:MarsSunset.jpg"},
  {"file": "media-019-klm-boeing-737-at-amsterdam-airport-schiphol-2016-jpg.jpg", "credit": "KLM Boeing 737 at Amsterdam Airport Schiphol 2016 · Intermedichbo · CC BY-SA 4.0", "source": "https://commons.wikimedia.org/wiki/File:KLM_Boeing_737_at_Amsterdam_Airport_Schiphol_2016.jpg"},
  {"file": "media-020-tower-bridge-london-feb-2006-jpg.jpg", "credit": "Tower Bridge London Feb 2006 · Diliff · CC BY-SA 3.0", "source": "https://commons.wikimedia.org/wiki/File:Tower_Bridge_London_Feb_2006.jpg"},
  {"file": "media-021-shakespeare-jpg.jpg", "credit": "Shakespeare · Attributed to John Taylor · Public domain", "source": "https://commons.wikimedia.org/wiki/File:Shakespeare.jpg"},
  {"file": "media-022-xysticus-spec-6890-jpg.jpg", "credit": "Xysticus.spec.6890 · Olaf Leillinger · CC BY-SA 3.0", "source": "https://commons.wikimedia.org/wiki/File:Xysticus.spec.6890.jpg"},
  {"file": "media-023-ecliptic-vs-equator-full-globe-png.jpg", "credit": "Ecliptic vs equator full globe.png · Tfr000 (talk) 19:12, 3 April 2012 (UTC) · CC BY-SA 3.0", "source": "https://commons.wikimedia.org/wiki/File:Ecliptic_vs_equator_full_globe.png"},
  {"file": "media-024-07-camel-profile-near-silverton-nsw-07-07-2007-jpg.jpg", "credit": "07. Camel Profile, near Silverton, NSW, 07.07.2007 · Jjron · CC BY-SA 3.0", "source": "https://commons.wikimedia.org/wiki/File:07._Camel_Profile,_near_Silverton,_NSW,_07.07.2007.jpg"},
  {"file": "media-025-frederic-edwin-church-south-american-landscape-jpg.jpg", "credit": "Frederic Edwin Church - South American landscape · Frederic Edwin Church · Public domain", "source": "https://commons.wikimedia.org/wiki/File:Frederic_Edwin_Church_-_South_American_landscape.jpg"},
];

window.NETTO_DAILY_PHOTO_DIR = 'fotos/assets/';
