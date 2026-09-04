(() => {
  'use strict';

  const STORAGE_KEY = 'netto_language';
  const SUPPORTED = new Set(['en', 'nl']);
  const savedLanguage = localStorage.getItem(STORAGE_KEY);
  const language = SUPPORTED.has(savedLanguage) ? savedLanguage : 'en';

  const ui = {
    'Netto · dagelijkse schatting': 'Netto · daily estimation',
    'Schat drie feiten, vind het verband. Elke dag een nieuwe puzzel.': 'Estimate three facts and find the connection. A new puzzle every day.',
    'Drie vragen. Eén verband. Elke dag een nieuwe puzzel.': 'Three questions. One connection. A new puzzle every day.',
    'Speler en streak': 'Player and streak',
    'Jouw daily’s': 'Your dailies',
    'Streakkalender': 'Streak calendar',
    'Kalender sluiten': 'Close calendar',
    'Vorige maand': 'Previous month',
    'Volgende maand': 'Next month',
    'Speeldagen in deze maand': 'Days played this month',
    'Daily gespeeld': 'Daily played',
    'Niet gespeeld': 'Not played',
    'ma': 'Mon',
    'di': 'Tue',
    'wo': 'Wed',
    'do': 'Thu',
    'vr': 'Fri',
    'za': 'Sat',
    'zo': 'Sun',
    'Inloggen': 'Log in',
    'Uitloggen': 'Log out',
    'dagelijkse schatting': 'daily estimation',
    'Spelen': 'Play',
    'Puzzels': 'Puzzles',
    'Puzzel': 'Puzzle',
    'PUZZEL': 'PUZZLE',
    'Puzzel Race': 'Puzzle Race',
    'Breinkrakers': 'Brain Teasers',
    'BREINKRAKERS': 'BRAIN TEASERS',
    'Meer': 'More',
    'Hoe werkt het?': 'How does it work?',
    'Vraag insturen': 'Submit a question',
    'Netto · dagelijkse schatting': 'Netto · daily estimation',
    'Drie vragen.': 'Three questions.',
    'Eén verband.': 'One connection.',
    'Schat drie feiten. De derde volgt uit de eerste twee — weet je er één goed, dan kun je de rest afleiden. Elke dag een nieuwe puzzel.': 'Estimate three facts. The third follows from the first two — know one and you can work out the rest. A new puzzle every day.',
    'Start dagelijkse puzzel': 'Start today’s puzzle',
    'De Daily': 'The Daily',
    'Schat drie feiten. Gebruik het verband om slimmer te spelen.': 'Estimate three facts. Use the connection to play smarter.',
    'Speel de Daily': 'Play today’s Daily',
    'Snel verder': 'Quick actions',
    'Ga verder': 'Continue',
    'Ga verder waar je gebleven was': 'Pick up where you left off',
    'Vind je volgende uitdaging': 'Find your next challenge',
    'Zoek op categorie, operator en niveau': 'Browse by category, operator and level',
    'Ontdek Netto': 'Explore Netto',
    'Meer manieren om te spelen': 'More ways to play',
    'Netto · speel verder': 'Netto · keep playing',
    'Nog één': 'One more',
    'puzzel.': 'puzzle.',
    'Ga verder waar je gebleven was en ontdek of je schatting nog scherper kan.': 'Continue where you left off and see if your estimates can get even sharper.',
    'Netto · voor nieuwsgierige mensen': 'Netto · for curious minds',
    'Duik in de': 'Dive into the',
    'Library.': 'Library.',
    'Doorzoek categorieën, operators en difficulties en vind jouw volgende uitdaging.': 'Browse categories, operators and difficulty levels to find your next challenge.',
    'Open Library →': 'Open Library →',
    'PUZZEL RACE': 'PUZZLE RACE',
    'OPEN GAMES': 'OPEN GAMES',
    'Kies je modus': 'Choose your mode',
    "Uitleg van feit-trio's, de wiskunde-twist en de multiplier": 'Learn about fact trios, the math twist and the multiplier',
    'Kies een moeilijkheid en speel alle puzzels': 'Choose a difficulty and play every puzzle',
    'Kies een moeilijkheid en speel alle puzzels.': 'Choose a difficulty and play every puzzle.',
    'Solo, online of met vrienden': 'Solo, online or with friends',
    '4 vragen in één formule': '4 questions in one formula',
    'Alle dagpuzzels sinds dag één': 'Every daily puzzle since day one',
    'Schat het': 'Estimate',
    'slim.': 'smart.',
    'Je hebt de puzzel van vandaag al gespeeld!': 'You have already played today’s puzzle!',
    'Bekijk ranglijst': 'View leaderboard',
    'Check mijn score': 'Check my score',
    'Vragen': 'Questions',
    'Vraag': 'Question',
    'Resultaat': 'Result',
    'Nauwkeurigheid': 'Accuracy',
    'Gem. factor: 1.00×': 'Avg. factor: 1.00×',
    '🎯 Meesterlijk geschat!': '🎯 Masterful estimate!',
    'Wil je meedoen in het': 'Want to join the',
    'Log in / Registreer': 'Log in / Sign up',
    'Elke puzzel opnieuw spelen.': 'Replay every puzzle.',
    'Onze missie': 'Our mission',
    'Netto maakt nieuwsgierigheid speelbaar. We verbinden alledaagse feiten met slimme rekensommen, zodat je niet alleen gokt, maar leert denken in verhoudingen.': 'Netto makes curiosity playable. We connect everyday facts through clever calculations, so you learn to think in proportions instead of merely guessing.',
    'Elke puzzel is een kleine ontdekking: drie vragen, één verband en altijd een kans om dichter bij de waarheid te komen.': 'Every puzzle is a small discovery: three questions, one connection and always a chance to get closer to the truth.',
    'Hoe werkt Netto?': 'How does Netto work?',
    '1. De drie vragen & de wiskunde-twist': '1. Three questions and the math twist',
    'Elke puzzel geeft je': 'Every puzzle gives you',
    'drie feiten-vragen': 'three fact questions',
    '. Je schat een getal per vraag. Maar er is een twist: de drie antwoorden hangen aan elkaar via een som.': '. You estimate a number for each question. But there is a twist: the three answers are connected by an equation.',
    'Voorbeeld:': 'Example:',
    '— de derde volgt uit de eerste twee. Ken je er één goed, dan kun je de rest afleiden.': '— the third follows from the first two. Know one and you can work out the rest.',
    '2. Scoren & de multiplier': '2. Scoring and the multiplier',
    'Per vraag krijg je een': 'For each question you receive a',
    'factor': 'factor',
    '(multiplier). Die is': '(multiplier). It is',
    'als je exact raadt en loopt op naarmate je verder van het echte antwoord zit:': 'when your answer is exact and increases the further you are from the real answer:',
    'Spot on! Bijna perfect': 'Spot on! Almost perfect',
    'Dichtbij, mooie schatting': 'Close — nice estimate',
    'Ruime schatting': 'Wide estimate',
    'meer': 'more',
    'Ver uit de buurt': 'Far off',
    'Je': 'Your',
    'eindfactor': 'final factor',
    'is het gemiddelde van de drie vragen. Hoe lager, hoe beter.': 'is the average across the three questions. Lower is better.',
    '3. Bonus & meer': '3. Bonuses and more',
    '— speel elke dag en bouw een reeks op.': '— play every day and build a streak.',
    '— 5 minuten zoveel mogelijk exact goed, van makkelijk naar moeilijk.': '— get as many exact answers as possible in 5 minutes, from easy to hard.',
    '— live duel via een open game of room-code; wie de meeste goed heeft wint.': '— play a live duel through an open game or room code; most correct answers wins.',
    'Vraagsets wisselen': 'Switch question sets',
    '— pas je race aan met regio- of thema-sets in': '— customise your race with regional or themed sets in',
    '— een ketting van 4 vragen in één formule.': '— a chain of 4 questions in one formula.',
    'laden…': 'loading…',
    '← Vorige': '← Previous',
    'Volgende →': 'Next →',
    '← Terug': '← Back',
    'NETTO · NIEUWE MODUS': 'NETTO · NEW MODE',
    'Alleen': 'Solo',
    'NETTO · PUZZEL RACE': 'NETTO · PUZZLE RACE',
    'Kies je vraagset en tempo. Los in de tijdslimiet zoveel mogelijk puzzels exact op.': 'Choose your question set and pace. Solve as many puzzles exactly as you can before time runs out.',
    'Vraagset': 'Question set',
    'De puzzels worden per run willekeurig gekozen, zonder herhaling.': 'Puzzles are chosen randomly for each run, without repeats.',
    'Tempo': 'Pace',
    '3 minuten': '3 minutes',
    '5 minuten': '5 minutes',
    '10 minuten': '10 minutes',
    'Snel': 'Fast',
    'Start solo race': 'Start solo race',
    'Vind een tegenstander.': 'Find an opponent.',
    'Zet de schakelaar op Open en je game verschijnt voor iedereen in de lijst rechts — of zet hem op Closed en deel je persoonlijke code.': 'Set the switch to Open and your game appears in the list — or choose Closed and share your personal code.',
    'Tijd': 'Time',
    'Type game': 'Game type',
    'Iedereen ziet jouw game in de lijst rechts en kan direct joinen.': 'Everyone can see your game in the list and join instantly.',
    'Maak open game →': 'Create open game →',
    'Een closed game werkt met een persoonlijke code en start nooit automatisch.': 'A closed game uses a personal code and never starts automatically.',
    'Maak closed game →': 'Create closed game →',
    'Wie speelt er?': 'Who is playing?',
    'Open games laden…': 'Loading open games…',
    'Sluit aan met een code': 'Join with a code',
    'Heb je een code gekregen van iemand? Vul hem hier in en je komt direct in de closed game.': 'Got a code from someone? Enter it here to join the closed game.',
    'Jouw game staat in de lijst "Wie speelt er?" rechts. Andere spelers joinen direct — zodra er iemand binnen is, telt het duel automatisch af (of je start zelf).': 'Your game is visible in the list. Other players can join instantly — once someone joins, the duel counts down automatically (or you can start it yourself).',
    'Room-code': 'Room code',
    '📋 Kopieer': '📋 Copy',
    'Verbinden…': 'Connecting…',
    'Start duel →': 'Start duel →',
    'Annuleren': 'Cancel',
    'tijd over': 'time left',
    'goed': 'correct',
    'reeks': 'streak',
    'Jouw reeks': 'Your run',
    'Check en door →': 'Check and continue →',
    'Enter in het laatste veld gaat ook meteen door.': 'Press Enter in the last field to continue immediately.',
    'PUZZEL RACE · RESULTAAT': 'PUZZLE RACE · RESULT',
    'Jouw score': 'Your score',
    'puzzels exact goed': 'puzzles exactly right',
    'Alle ingediende puzzels': 'All submitted puzzles',
    'Nog een race →': 'Race again →',
    'NETTO · BREINKRAKERS': 'NETTO · BRAIN TEASERS',
    'Vier vragen vormen samen één formule. Kies een puzzel en vul alle vier de antwoorden in.': 'Four questions form one equation. Choose a puzzle and enter all four answers.',
    'Gespeeld': 'Played',
    'Volledig exact': 'Completely exact',
    'Gemiddelde score': 'Average score',
    'Voortgang wissen': 'Reset progress',
    '← Alle Breinkrakers': '← All Brain Teasers',
    'BREINKRAKERS · KLAAR': 'BRAIN TEASERS · COMPLETE',
    'Alle puzzels gespeeld 🎉': 'All puzzles completed 🎉',
    'gemiddelde afwijking': 'average deviation',
    'Terug naar alle puzzels →': 'Back to all puzzles →',
    'NETTO · SETTINGS': 'NETTO · SETTINGS',
    'NETTO · INSTELLINGEN': 'NETTO · SETTINGS',
    'Taal': 'Language',
    'Website-taal': 'Website language',
    'Kies Engels of Nederlands. Je keuze wordt op dit apparaat onthouden.': 'Choose English or Dutch. Your choice is saved on this device.',
    'Uiterlijk': 'Appearance',
    'Donkere modus': 'Dark mode',
    'Warm goud op diepe navy. Uit = klassieke Netto-blauw.': 'Warm gold on deep navy. Off = classic Netto blue.',
    'Rekenmachine': 'Calculator',
    'Auto-calculator': 'Auto calculator',
    'Vult automatisch het derde antwoord in zodra je er twee hebt. Aan = helpend, uit = pure puzzelmodus.': 'Automatically fills the third answer once you have two. On = assisted, off = pure puzzle mode.',
    'Race-vraagset': 'Race question set',
    'alleen solo race · duel gebruikt altijd de standaardset': 'solo race only · duels always use the standard set',
    'De gekozen set geldt vanaf je volgende solo-race. Daily-puzzels, Puzzels en Breinkrakers blijven onveranderd.': 'The selected set applies to your next solo race. Dailies, Puzzles and Brain Teasers stay unchanged.',
    'NETTO · VRAAG INSTUREN': 'NETTO · SUBMIT A QUESTION',
    'NETTO · JOUW FEITEN': 'NETTO · YOUR FACTS',
    'Stuur je': 'Submit your',
    'vraag in.': 'question.',
    'Elke inzending wordt gereviewd. Word je vraag geaccepteerd, dan gebruiken we hem misschien in een toekomstige daily of puzzel — je krijgt daar dan een melding van.': 'Every submission is reviewed. If your question is accepted, we may use it in a future daily or puzzle — and you will be notified.',
    'Inloggen verplicht.': 'Login required.',
    '❓ Vraag': '❓ Question',
    '🧩 Puzzel': '🧩 Puzzle',
    'Heb je een leuk feit met een getal als antwoord? Stuur het in — het antwoord mag je ook overslaan, dan zoeken wij het uit.': 'Know a fun fact with a number as its answer? Send it in — you may leave the answer blank and we will research it.',
    'Vraag 3 (resultaat)': 'Question 3 (result)',
    'Bewerking': 'Operator',
    '× keer': '× multiply',
    '÷ deel': '÷ divide',
    '+ plus': '+ add',
    '− min': '− subtract',
    'Credits-naam': 'Credit name',
    'optioneel': 'optional',
    'Toelichting': 'Notes',
    'Vul alles in om je som te zien.': 'Complete everything to see your equation.',
    'Verstuur inzending': 'Submit',
    'Je inzending wordt gereviewd door B-Force. Bij acceptatie kan je vraag of puzzel in een toekomstige daily of puzzel verschijnen, en krijg je een melding in het spel. Met de credits-naam (optioneel) staat je naam erbij.': 'Your submission will be reviewed by B-Force. If accepted, your question or puzzle may appear in a future daily or puzzle and you will receive an in-game notification. Add an optional credit name to be credited.',
    'Snelle rekenmachine': 'Quick calculator',
    'Sluit rekenmachine': 'Close calculator',
    'Rekenmachine display': 'Calculator display',
    'NETTO · LIBRARY ✦': 'NETTO · LIBRARY ✦',
    'Alle puzzels en vragen doorzoekbaar.': 'Search every puzzle and question.',
    'Doorzoek alle puzzels op operator, categorie en difficulty, en blader door alle losse vragen.': 'Search all puzzles by operator, category and difficulty, and browse every individual question.',
    'Ontgrendel Library': 'Unlock Library',
    'Testmodus: simuleert aankoop lokaal in je browser.': 'Test mode: simulates a purchase locally in your browser.',
    'Alle operators': 'All operators',
    'Alle difficulties': 'All difficulties',
    'Alle categorieën': 'All categories',
    'Leaderboard 🏆': 'Leaderboard 🏆',
    'Wie zat er vandaag het dichtst op de waarheid?': 'Who got closest to the truth today?',
    'Vandaag': 'Today',
    'Mijn Profiel 👤': 'My Profile 👤',
    'ingelogd als gebruiker': 'logged in as user',
    'GEBRUIKERSNAAM': 'USERNAME',
    'Speler': 'Player',
    'Uitloggen': 'Log out',
    'Synchroniseer je scores over al je apparaten & sta op het leaderboard.': 'Sync your scores across all your devices and appear on the leaderboard.',
    'Spelersnaam (uniek)': 'Player name (unique)',
    '3–20 tekens': '3–20 characters',
    'E-mailadres': 'Email address',
    'Wachtwoord': 'Password',
    'Minimaal 8 tekens': 'At least 8 characters',
    'Nog geen account?': 'No account yet?',
    'Registreer gratis': 'Sign up free',
    'Wachtwoord vergeten?': 'Forgot your password?',
    'Wachtwoord vergeten? 🔑': 'Forgot your password? 🔑',
    'Vul je e-mailadres in en we sturen je een link om een nieuw wachtwoord in te stellen.': 'Enter your email address and we will send you a link to set a new password.',
    'Verstuur resetlink': 'Send reset link',
    '← Terug naar inloggen': '← Back to login',
    'Jouw schatting': 'Your estimate',
    'Automatisch berekend antwoord': 'Automatically calculated answer',
    'Gekopieerd!': 'Copied!',
    'Cijfers gevraagd': 'Numbers only',
    'Let op': 'Heads up',
    'Vraag niet beschikbaar': 'Question unavailable',
    'Open kalender': 'Open calendar',
    'Sluit kalender': 'Close calendar',
    'Bekijk de vragen': 'View questions',
    'Bekijk het resultaat': 'View result',
    'Review navigatie': 'Review navigation',
    'Open games vernieuwen': 'Refresh open games',
    'Voortgang Breinkrakers': 'Brain Teaser progress',
    'Formule-skelet': 'Equation outline',
    'Zoek in puzzels…': 'Search puzzles…',
    'Zoek in vragen…': 'Search questions…',
    'bijv. MathMasterNL': 'e.g. MathMaster',
    'jouw@email.nl': 'you@example.com',
    'hoe je naam in het spel komt': 'the name shown in the game',
    'Bron, context of een leuke noot': 'Source, context or a fun note',
    'Antwoord': 'Answer',
    'Antwoord (mag leeg)': 'Answer (may be blank)',
    'Netto — naar de landingpagina': 'Netto — go to the home screen'
    ,
    'Log in met je Supabase-account. Alleen een account dat in': 'Log in with your Supabase account. Only an account listed in',
    'staat krijgt toegang.': 'is granted access.',
    'E-mailadres voor reset': 'Email address for reset',
    'Resetlink sturen': 'Send reset link',
    'Nieuw wachtwoord': 'New password',
    'Herhaal wachtwoord': 'Repeat password',
    'Opslaan': 'Save',
    'Nieuwe reviews': 'New reviews',
    'Vraag- & puzzel-review': 'Question and puzzle review',
    'Inzendingen van spelers. Accepteren of weigeren stuurt automatisch een melding naar de speler. Fouten in de berekening zie je direct.': 'Player submissions. Accepting or rejecting automatically notifies the player. Calculation errors are shown immediately.',
    'Nieuw': 'New',
    'Geaccepteerd': 'Accepted',
    'Geweigerd': 'Rejected',
    'Laden…': 'Loading…',
    'Resetlink verstuurd. Controleer je e-mail.': 'Reset link sent. Check your email.',
    'De wachtwoorden komen niet overeen.': 'The passwords do not match.',
    'Wachtwoord gewijzigd. Log opnieuw in.': 'Password changed. Log in again.',
    'Uitgelogd.': 'Logged out.'
    ,
    'geaccepteerd': 'accepted',
    'geweigerd': 'rejected',
    'nieuw': 'new',
    'Accepteren': 'Accept',
    'Weigeren': 'Reject',
    'anoniem': 'anonymous',
    'losse vraag · antwoord': 'single question · answer',
    'onbekend': 'unknown',
    '⚠ Antwoord ontbreekt — zoek het zelf uit voor acceptatie.': '⚠ Answer missing — research it before accepting.',
    'Dit dashboard leest alleen gegevens waarvoor jouw Supabase-tabellen en RLS-policies toegang geven. Een ontbrekende optionele tabel wordt als een streepje getoond.': 'This dashboard only reads data allowed by your Supabase tables and RLS policies. A missing optional table is shown as a dash.'
  };

  const dynamicRules = [
    [/\bPuzzel (\d+) van (\d+)\b/g, 'Puzzle $1 of $2'],
    [/\bPuzzel (\d+)\b/g, 'Puzzle $1'],
    [/\bVraag (\d+)\b/g, 'Question $1'],
    [/\b(\d+) puzzels? gevonden\b/g, '$1 puzzles found'],
    [/\b(\d+) vragen? gevonden\b/g, '$1 questions found'],
    [/\b(\d+) puzzels\b/g, '$1 puzzles'],
    [/\b(\d+) vragen\b/g, '$1 questions'],
    [/\b(\d+) dagen\b/g, '$1 days'],
    [/\b1 dag\b/g, '1 day'],
    [/\bJouw gok:\s*/g, 'Your estimate: '],
    [/\bEcht antwoord:\s*/g, 'Correct answer: '],
    [/\bGemiddelde afwijking:\s*/g, 'Average deviation: '],
    [/\bJouw gemiddelde afwijking\b/g, 'Your average deviation'],
    [/\bHuidige streak:\s*/g, 'Current streak: '],
    [/\bVolgende puzzel\b/g, 'Next puzzle'],
    [/\bSpeel puzzel (\d+)\b/g, 'Play puzzle $1'],
    [/\bAlle puzzels voltooid\b/g, 'All puzzles completed'],
    [/\bVolgende daily puzzle\b/g, 'Next daily puzzle'],
    [/\bDagelijkse Puzzel\b/g, 'Daily Puzzle'],
    [/\bNieuwe puzzel om\b/g, 'New puzzle at'],
    [/\bOpen puzzel\b/gi, 'Open puzzle'],
    [/\bOpen Breinkraker\b/g, 'Open Brain Teaser'],
    [/\bgespeeld door jou\b/gi, 'played by you'],
    [/\bgespeeld\b/gi, 'played'],
    [/\bNiet exact\b/g, 'Not exact'],
    [/\bdoor!\b/g, 'continue!'],
    [/\bJouw record:\s*/g, 'Your record: '],
    [/\bexact goed\b/g, 'exact answers'],
    [/\bgoed\b/g, 'correct'],
    [/\breeks\b/g, 'streak'],
    [/\bNog geen record gezet — word de eerste\.\b/g, 'No record yet — be the first.'],
    [/\bTegenstander\b/g, 'Opponent'],
    [/\btegenstander\b/g, 'opponent'],
    [/\bJij wint!\b/g, 'You win!'],
    [/\bwint\b/g, 'wins'],
    [/\bGelijkspel\b/g, 'Draw'],
    [/\btegen\b/g, 'versus'],
    [/\bOpen game actief\b/g, 'Open game active'],
    [/\bGeen open games\b/g, 'No open games'],
    [/\bNog geen open games\. Maak de eerste\.\b/g, 'No open games yet. Create the first one.'],
    [/\bKalender sluiten\b/g, 'Close calendar'],
    [/\bOpen kalender\b/g, 'Open calendar'],
    [/\bdaily gespeeld\b/gi, 'daily played'],
    [/\bniet gespeeld\b/gi, 'not played'],
    [/\bmaand\b/g, 'month'],
    [/\bInloggen \/ Registreren\b/g, 'Log in / Sign up'],
    [/\bProfiel \(([^)]+)\)/g, 'Profile ($1)']
    ,
    [/\bGeen nieuw-inzendingen\.\b/g, 'No new submissions.'],
    [/\bGeen geaccepteerd-inzendingen\.\b/g, 'No accepted submissions.'],
    [/\bGeen geweigerd-inzendingen\.\b/g, 'No rejected submissions.'],
    [/\bmoet ([^ ]+) zijn\b/g, 'should be $1'],
    [/\bAdmincontrole mislukt:\s*/g, 'Admin check failed: '],
    [/\bDit account staat niet in admin_users\.\b/g, 'This account is not listed in admin_users.'],
    [/\bKon niet laden:\s*/g, 'Could not load: '],
    [/\bInzending #(\d+) geaccepteerd\. Speler is op de hoogte gebracht\.\b/g, 'Submission #$1 accepted. The player has been notified.'],
    [/\bInzending #(\d+) geweigerd\. Speler is op de hoogte gebracht\.\b/g, 'Submission #$1 rejected. The player has been notified.']
  ];

  const generatedCatalog = window.NETTO_TRANSLATIONS_EN || {};
  const skippedTags = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE']);
  const translatedText = new WeakMap();
  const translatedAttributes = new WeakMap();

  function translateCore(source) {
    if (language !== 'en' || !source) return source;
    const exactUi = ui[source];
    if (exactUi) return exactUi;
    const generated = generatedCatalog[source];
    const dynamicLabel = /^(?:Puzzel|Vraag) \d+(?: van \d+)?$/.test(source);
    if (generated && !dynamicLabel) return generated;
    let result = source;
    for (const [pattern, replacement] of dynamicRules) result = result.replace(pattern, replacement);
    if (result !== source) return result;
    return generated || source;
  }

  function translatePreservingWhitespace(value) {
    if (language !== 'en' || typeof value !== 'string') return value;
    const match = value.match(/^(\s*)([\s\S]*?)(\s*)$/);
    if (!match || !match[2]) return value;
    return match[1] + translateCore(match[2]) + match[3];
  }

  function translateTextNode(node) {
    if (!node.parentElement || skippedTags.has(node.parentElement.tagName) || node.parentElement.closest('[data-i18n-skip]')) return;
    if (translatedText.get(node) === node.nodeValue) return;
    const translated = translatePreservingWhitespace(node.nodeValue);
    if (translated !== node.nodeValue) {
      translatedText.set(node, translated);
      node.nodeValue = translated;
    } else {
      translatedText.delete(node);
    }
  }

  function translateElement(element) {
    if (!(element instanceof Element) || skippedTags.has(element.tagName) || element.closest('[data-i18n-skip]')) return;
    let translatedForElement = translatedAttributes.get(element);
    if (!translatedForElement) {
      translatedForElement = new Map();
      translatedAttributes.set(element, translatedForElement);
    }
    for (const attribute of ['aria-label', 'title', 'placeholder']) {
      if (!element.hasAttribute(attribute)) continue;
      const current = element.getAttribute(attribute);
      if (translatedForElement.get(attribute) === current) continue;
      const translated = translateCore(current);
      if (translated !== current) {
        translatedForElement.set(attribute, translated);
        element.setAttribute(attribute, translated);
      } else {
        translatedForElement.delete(attribute);
      }
    }
  }

  function translateTree(root) {
    if (language !== 'en' || !root) return;
    if (root.nodeType === Node.TEXT_NODE) {
      translateTextNode(root);
      return;
    }
    if (root.nodeType !== Node.ELEMENT_NODE && root.nodeType !== Node.DOCUMENT_NODE) return;
    if (root.nodeType === Node.ELEMENT_NODE) translateElement(root);
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      if (node.nodeType === Node.TEXT_NODE) translateTextNode(node);
      else translateElement(node);
    }
  }

  function updateLanguageControls() {
    document.querySelectorAll('[data-language]').forEach((button) => {
      const active = button.dataset.language === language;
      button.setAttribute('aria-checked', String(active));
      button.classList.toggle('is-active', active);
    });
  }

  function setLanguage(nextLanguage) {
    if (!SUPPORTED.has(nextLanguage) || nextLanguage === language) return;
    localStorage.setItem(STORAGE_KEY, nextLanguage);
    window.location.reload();
  }

  function locale() {
    return language;
  }

  window.NettoI18n = Object.freeze({
    language,
    locale,
    setLanguage,
    t: translateCore,
    translateTree,
    updateLanguageControls
  });

  document.documentElement.lang = language;
  if (language === 'en') {
    if (document.title === 'Netto · dagelijkse schatting') document.title = ui['Netto · dagelijkse schatting'];
    const description = document.querySelector('meta[name="description"]');
    if (description) description.content = ui['Schat drie feiten, vind het verband. Elke dag een nieuwe puzzel.'];
    document.querySelectorAll('meta[property="og:title"], meta[name="twitter:title"]').forEach((meta) => { meta.content = ui['Netto · dagelijkse schatting']; });
    document.querySelectorAll('meta[property="og:description"], meta[name="twitter:description"]').forEach((meta) => { meta.content = ui['Drie vragen. Eén verband. Elke dag een nieuwe puzzel.']; });
  }

  document.addEventListener('DOMContentLoaded', () => {
    translateTree(document.body);
    updateLanguageControls();
    const observer = new MutationObserver((mutations) => {
      for (const mutation of mutations) {
        if (mutation.type === 'characterData') translateTextNode(mutation.target);
        if (mutation.type === 'attributes') translateElement(mutation.target);
        for (const node of mutation.addedNodes) translateTree(node);
      }
      updateLanguageControls();
    });
    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true,
      attributes: true,
      attributeFilter: ['aria-label', 'title', 'placeholder']
    });
  });
})();
