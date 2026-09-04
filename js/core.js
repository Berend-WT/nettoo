// Netto frontend module.
// Loaded as a classic script so the existing shared global scope stays intact.

// =========================================================================
  // REKENMACHINE
  // =========================================================================
  let calculatorExpression = '';
  const CALC_OPENED_KEY = 'netto_calc_opened';
  function nettoNumberLocale() { return window.NettoI18n?.locale() === 'nl' ? 'nl-NL' : 'en-GB'; }
  function toggleCalculator(open) {
    const calc = document.getElementById('calculator');
    calc.classList.toggle('open', open);
    if (open) {
      localStorage.setItem(CALC_OPENED_KEY, '1');
      updateCalculatorToggleLabel();
    }
  }
  // Label alleen tonen zolang de rekenmachine nog nooit geopend is; daarna alleen het icoon.
  function updateCalculatorToggleLabel() {
    const label = document.querySelector('.calculator-toggle-label');
    if (label) label.style.display = localStorage.getItem(CALC_OPENED_KEY) ? 'none' : 'inline';
    const toggle = document.querySelector('.calculator-toggle');
    if (toggle) toggle.style.padding = localStorage.getItem(CALC_OPENED_KEY) ? '10px' : '10px 18px';
  }
  function formatCalculatorNumber(value) {
    if (!value || value === 'Fout' || value === 'Error') return value || '0';
    return value.replace(/\d+(?:\.\d+)?/g, (part) => {
      const [whole, decimal] = part.split('.');
      const formatted = Number(whole).toLocaleString(nettoNumberLocale());
      const separator = window.NettoI18n?.locale() === 'nl' ? ',' : '.';
      return decimal === undefined ? formatted : `${formatted}${separator}${decimal}`;
    });
  }

  function updateCalculatorDisplay() {
    document.getElementById('calculatorDisplay').value = formatCalculatorNumber(calculatorExpression) || '0';
  }

  function calculatorInput(value) {
    if (calculatorExpression === '0' && /\d/.test(value)) calculatorExpression = '';
    calculatorExpression += value;
    updateCalculatorDisplay();
  }
  function calculatorClear() {
    calculatorExpression = '';
    updateCalculatorDisplay();
  }
  function calculatorBackspace() {
    calculatorExpression = calculatorExpression.slice(0, -1);
    updateCalculatorDisplay();
  }
  function calculatorEvaluate() {
    try {
      const expression = calculatorExpression.replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-');
      if (!/^[0-9+*/().\s-]+$/.test(expression)) throw new Error('Ongeldige berekening');
      const result = Function(`"use strict"; return (${expression})`)();
      if (!Number.isFinite(result)) throw new Error('Ongeldige uitkomst');
      calculatorExpression = String(Number(result.toFixed(10)));
      updateCalculatorDisplay();
    } catch (error) {
      document.getElementById('calculatorDisplay').value = window.NettoI18n?.locale() === 'nl' ? 'Fout' : 'Error';
      calculatorExpression = '';
    }
  }

  // =========================================================================
  // 1. CONFIGURATIE & SUPABASE SETUP
  // =========================================================================
  // Vul hier je Supabase gegevens in zodra je die hebt:
  const SUPABASE_URL = "https://bqatnnouxkjdzvvhqbly.supabase.co"; 
  const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJxYXRubm91eGtqZHp2dmhxYmx5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODc4MzMwMDAsImV4cCI6MjEwMzQwOTAwMH0.KtjxuC3gyixJjQqKpwPd1b7wzg0VPbm-_EgeUc9iZAI"; 
  
  let supabaseClient = null;
  function initSupabaseClient() {
    if (SUPABASE_URL && SUPABASE_ANON_KEY && window.supabase) {
      supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    }
  }
  initSupabaseClient();
  if (!supabaseClient && window.supabase) initSupabaseClient();
  window.addEventListener('load', initSupabaseClient);

  // Sessie-sync: log uit op apparaat A = ook uitgelogd op apparaat B,
  // en herstel de ingelogde gebruiker bij paginalading.
  function initAuthStateListener() {
    if (!supabaseClient || supabaseClient._authListenerSet) return;
    supabaseClient._authListenerSet = true;
    supabaseClient.auth.onAuthStateChange((event, session) => {
      if (event === 'SIGNED_OUT' || !session) {
        if (currentUser) {
          currentUser = null;
          localStorage.removeItem('netto_user');
          updateUserUI();
        }
        return;
      }
      if (event === 'SIGNED_IN' && session?.user && !currentUser) {
        const u = session.user;
        currentUser = {
          id: u.id,
          email: u.email,
          username: u.user_metadata?.username || (u.email || '').split('@')[0]
        };
        localStorage.setItem('netto_user', JSON.stringify(currentUser));
        updateUserUI();
      }
    });
  }
  initAuthStateListener();
  window.addEventListener('load', initAuthStateListener);

  // Datum & Actuele Dagpuzzels (12 Geverifieerde, niet-overlappende puzzels!)
  const TODAY_STR = new Date().toISOString().split('T')[0];
  
  const LIBRARY_SETS = {
    easy: [
      { name:'Kleine basis', operator:'×', q1_label:'Hoeveel officiële talen erkent de VN?', q1_answer:6, q2_label:'Hoeveel planeten telt ons zonnestelsel?', q2_answer:8, q3_label:'Wat is 6 × 8?', q3_answer:48 },
      { name:'Kaarten & cijfers', operator:'−', q1_label:'Hoeveel speelkaarten zitten in een standaard kaartspel?', q1_answer:52, q2_label:'Hoeveel staten telt de VS?', q2_answer:50, q3_label:'Wat is het verschil?', q3_answer:2 }
    ],
    intermediate: [
      { name:'Mens & muziek', operator:'×', q1_label:'Hoeveel ribben heeft een mens?', q1_answer:24, q2_label:'Hoeveel spelers staan per team in waterpolo?', q2_answer:7, q3_label:'Hoeveel stippen staan op dominostenen?', q3_answer:168 },
      { name:'Sport & ruimte', operator:'×', q1_label:'Hoeveel holes telt een golfronde?', q1_answer:18, q2_label:'Hoeveel chromosomen heeft een menselijke cel?', q2_answer:46, q3_label:'Hoe hoog is de Burj Khalifa?', q3_answer:828 }
    ],
    hard: [
      { name:'Wereldmaten', operator:'×', q1_label:'Hoe hoog is de Eiffeltoren?', q1_answer:330, q2_label:'Op welke hoogte draait het ISS?', q2_answer:400, q3_label:'Capaciteit Narendra Modi Stadium?', q3_answer:132000 },
      { name:'Licht & menigte', operator:'÷', q1_label:'Wat is de snelheid van het licht in km/s?', q1_answer:300000, q2_label:'Hoeveel toeschouwers konden in het Colosseum?', q2_answer:50000, q3_label:'Hoeveel officiële talen erkent de VN?', q3_answer:6 }
    ],
    'extremely-hard': [
      { name:'Eilandrekensom', operator:'×', q1_label:'Hoeveel eilanden telt de Filipijnen?', q1_answer:7641, q2_label:'Hoeveel strepen heeft de Amerikaanse vlag?', q2_answer:13, q3_label:'Capaciteit Camp Nou?', q3_answer:99354 },
      { name:'Tijd & afstand', operator:'×', q1_label:'Hoeveel afleveringen heeft The Office US?', q1_answer:201, q2_label:'In welk jaar zonk de Titanic?', q2_answer:1912, q3_label:'Afstand aarde-maan in km?', q3_answer:384400 }
    ]
  };

  const PUZZLE_ARCHIVE = [
    {
      number: 1,
      name: "LEGO & De Vlag",
      operator: "×",
      q1_label: "1. Hoeveel staten telt de Verenigde Staten van Amerika?",
      q1_answer: 50,
      q2_label: "2. Hoeveel letters telt ons Latijnse alfabet?",
      q2_answer: 26,
      q3_label: "3. Hoeveel LEGO-steentjes worden er wereldwijd per seconde gemaakt?",
      q3_answer: 1300
    },
    {
      number: 2,
      name: "Torenhoge Muren",
      operator: "+",
      q1_label: "1. Hoeveel inwoners heeft Vaticaanstad ongeveer?",
      q1_answer: 800,
      q2_label: "2. Hoeveel jaar stond de Berlijnse Muur overeind (1961-1989)?",
      q2_answer: 28,
      q3_label: "3. Wat is de hoogte van de Burj Khalifa in Dubai in meters?",
      q3_answer: 828
    },
    {
      number: 3,
      name: "Van Dom naar de Maan",
      operator: "+",
      q1_label: "1. Hoeveel treden telt de Domtoren in Utrecht?",
      q1_answer: 465,
      q2_label: "2. Hoeveel uren duurde de historische Apollo 11-missie naar de maan?",
      q2_answer: 195,
      q3_label: "3. Hoeveel duizend inwoners heeft het land Luxemburg (afgerond)?",
      q3_answer: 660
    },
    {
      number: 4,
      name: "Roadtrip naar Parijs",
      operator: "+",
      q1_label: "1. Hoeveel seizoenen heeft de serie Friends?",
      q1_answer: 10,
      q2_label: "2. Hoeveel vel papier zitten er in een standaard riem printpapier?",
      q2_answer: 500,
      q3_label: "3. Wat is de autorij-afstand van Amsterdam naar Parijs in km?",
      q3_answer: 510
    },
    {
      number: 5,
      name: "Parijs & Fawlty Towers",
      operator: "+",
      q1_label: "1. Hoeveel afleveringen telt de komedieserie Fawlty Towers?",
      q1_answer: 12,
      q2_label: "2. Wat is de hoogte van de Eiffeltoren in meters (met antenne)?",
      q2_answer: 330,
      q3_label: "3. Hoeveel officiële gemeenten telt Nederland (in 2024)?",
      q3_answer: 342
    },
    {
      number: 6,
      name: "Euromast & Tour de France",
      operator: "+",
      q1_label: "1. Hoe hoog is de Euromast in Rotterdam in meters?",
      q1_answer: 185,
      q2_label: "2. Hoeveel etappes telt de Tour de France doorgaans?",
      q2_answer: 21,
      q3_label: "3. Hoeveel botten heeft een volwassen menselijk lichaam?",
      q3_answer: 206
    },
    {
      number: 7,
      name: "Pianotoetsen & Hartslag",
      operator: "+",
      q1_label: "1. Hoeveel onafhankelijke landen telt Zuid-Amerika?",
      q1_answer: 12,
      q2_label: "2. Hoeveel toetsen heeft een standaard concertpiano (zwart + wit)?",
      q2_answer: 88,
      q3_label: "3. Hoeveel duizend keer klopt een mensenhart per dag (bij rust)?",
      q3_answer: 100
    },
    {
      number: 8,
      name: "Afsluitdijk & Schaakmat",
      operator: "+",
      q1_label: "1. Hoeveel tanden heeft een volwassen mens (met verstandskiezen)?",
      q1_answer: 32,
      q2_label: "2. Hoe lang is de Afsluitdijk in kilometers (afgerond)?",
      q2_answer: 32,
      q3_label: "3. Hoeveel speelvelden heeft een schaakbord?",
      q3_answer: 64
    },
    {
      number: 9,
      name: "James Bond & De Harp",
      operator: "+",
      q1_label: "1. In hoeveel officiële 007-films speelde Roger Moore?",
      q1_answer: 7,
      q2_label: "2. Hoeveel snaren heeft een standaard concert-pedaalharp?",
      q2_answer: 47,
      q3_label: "3. Hoeveel erkende landen telt het continent Afrika?",
      q3_answer: 54
    },
    {
      number: 10,
      name: "Scrabble & Cellen",
      operator: "+",
      q1_label: "1. Hoeveel punten is de letter Z waard in de Nederlandse Scrabble?",
      q1_answer: 6,
      q2_label: "2. Hoeveel chromosomen telt een gezonde menselijke lichaamscel?",
      q2_answer: 46,
      q3_label: "3. Hoeveel witte toetsen heeft een concertpiano?",
      q3_answer: 52
    },
    {
      number: 11,
      name: "Titanic & The Simpsons",
      operator: "+",
      q1_label: "1. Hoeveel Oscars won de kaskraker Titanic (1997)?",
      q1_answer: 11,
      q2_label: "2. Hoeveel ribben heeft een menselijk lichaam in totaal (12 paar)?",
      q2_answer: 24,
      q3_label: "3. Hoeveel seizoenen telt The Simpsons inmiddels (afgerond)?",
      q3_answer: 35
    },
    {
      number: 12,
      name: "Dartbord naar Rome",
      operator: "+",
      q1_label: "1. Hoeveel genummerde scorevakken heeft een dartbord?",
      q1_answer: 20,
      q2_label: "2. Wat is de autorij-afstand van Amsterdam naar Rome in km?",
      q2_answer: 1650,
      q3_label: "3. Hoeveel treden telt de Eiffeltoren naar de top?",
      q3_answer: 1665
    }
  ];

  // Huidig actieve puzzel (standaard Puzzel #01 van vandaag)
  function normalizeLibraryPuzzle(p) {
    return {
      ...p,
      q1_label: p.q1_label || p.q1,
      q1_answer: p.q1_answer ?? p.a1,
      q2_label: p.q2_label || p.q2,
      q2_answer: p.q2_answer ?? p.a2,
      q3_label: p.q3_label || p.q3,
      q3_answer: p.q3_answer ?? p.a3
    };
  }

  let activePuzzleIndex = 0;
  const REBUILT_DATA = window.NETTO_REBUILT_PUZZLES || { library: [], daily: [], reserve: [] };
  const DAILY_PUZZLES = (REBUILT_DATA.daily || []).map(normalizeLibraryPuzzle);
  let PUZZLE_DATA = DAILY_PUZZLES[activePuzzleIndex] || PUZZLE_ARCHIVE[0];

  // Sarcastische citaten als iemand letters invoert
  const SARCASTIC_QUOTES = [
    "Woorden hebben hier geen waarde. Cijfers wel.",
    "Leuk geprobeerd Shakespeare, maar we zoeken een getal.",
    "Dit is geen Scrabble. Alleen nummers!",
    "Wiskundigen huilen als je letters in een schatting typt.",
    "Letters? Daar koop je bij de kassa niks voor.",
    "Error 404: Geen getal gevonden in je essay.",
    "Probeer je een formule in dichtvorm te schrijven?",
    "Alleen cijfers graag! Nummers liegen nooit."
  ];

  let lastToastTime = 0;
  let authMode = 'login'; // 'login' of 'register'
  let currentUser = null;
  let currentLbTab = 'today';
  let streakCalendarDate = new Date(new Date().getFullYear(), new Date().getMonth(), 1);
  // De Daily Archive gebruikt dezelfde kaart als de puzzel, maar wisselt na
  // indienen naar een aparte resultatenstaat. Zo blijven vragen en review
  // overzichtelijk en kunnen spelers met de pijlen tussen beide states gaan.
  let dailyArchivePuzzleView = false;
  let dailyReviewView = 'questions';

  // =========================================================================
  // 2. INITIALISATIE & LOCALSTORAGE SYNC
  // =========================================================================
  // Consistente nummering: Nr. 001, Nr. 028, Nr. 142 (3 cijfers)
  const puzzleNr = n => `Nr. ${String(n).padStart(3, '0')}`;

  function initApp() {
    try {
      if (document.getElementById('q1-label')) {
        document.getElementById('q1-label').textContent = PUZZLE_DATA.q1_label;
        document.getElementById('q2-label').textContent = PUZZLE_DATA.q2_label;
        document.getElementById('q3-label').textContent = PUZZLE_DATA.q3_label;
        document.getElementById('operatorBadge').textContent = PUZZLE_DATA.operator || '×';
        document.getElementById('heroDateMeta').textContent = `${puzzleNr(PUZZLE_DATA.number)} · Dagelijkse Puzzel`;
        document.getElementById('puzzleEyebrow').textContent = `Netto · ${puzzleNr(PUZZLE_DATA.number)}`;
      }

      // Koppel knoppen expliciet via event listeners
      const btnStart = document.getElementById('btnStartPuzzle');
      if (btnStart) btnStart.onclick = () => {
        dailyArchivePuzzleView = false;
        activePuzzleIndex = 0;
        PUZZLE_DATA = DAILY_PUZZLES[0] || PUZZLE_ARCHIVE[0];
        loadActivePuzzle();
        showScreen('puzzle');
      };

      const btnHamb = document.getElementById('hamburgerBtn');
      if (btnHamb) btnHamb.onclick = toggleMenu;

      const overlay = document.getElementById('overlay');
      if (overlay) overlay.onclick = toggleMenu;

      const btnCheck = document.getElementById('btnCheck');
      if (btnCheck) btnCheck.onclick = checkAnswers;

      const topUserBtn = document.getElementById('topbarUserBtn');
      if (topUserBtn) topUserBtn.onclick = openAuthModal;

      const streakButton = document.getElementById('streakButton');
      if (streakButton) streakButton.onclick = toggleStreakCalendar;
      const streakClose = document.getElementById('streakCalendarClose');
      if (streakClose) streakClose.onclick = closeStreakCalendar;
      const streakPrevious = document.getElementById('streakCalendarPrevious');
      if (streakPrevious) streakPrevious.onclick = () => moveStreakCalendarMonth(-1);
      const streakNext = document.getElementById('streakCalendarNext');
      if (streakNext) streakNext.onclick = () => moveStreakCalendarMonth(1);
      document.addEventListener('click', closeStreakCalendarOnOutsideClick);
      document.addEventListener('keydown', closeStreakCalendarOnEscape);

      initInputs();
      loadUserProfile();
      applyTheme();
      updateCalculatorToggleLabel();
      if (supabaseClient) supabaseClient.auth.getSession().then(({ data }) => {
        if (data.session?.user) {
          currentUser = { id: data.session.user.id, email: data.session.user.email, username: data.session.user.user_metadata?.username || data.session.user.email.split('@')[0] };
          localStorage.setItem('netto_user', JSON.stringify(currentUser));
          updateUserUI();
        }
      });
      checkExistingPlay();
      updateContinuePuzzleButton();
      startHeroSlideshow();
    } catch(err) {
      console.error("Fout tijdens initApp:", err);
    }
  }

  function getLocalPlays() {
    try {
      return JSON.parse(localStorage.getItem('netto_plays')) || {};
    } catch(e) {
      return {};
    }
  }

  function getLocalStreak() {
    return parseInt(localStorage.getItem('netto_streak') || '0', 10);
  }

  function updateStreakUI(streak) {
    document.getElementById('topbarStreak').textContent = streak;
    const streakButton = document.getElementById('streakButton');
    if (streakButton) {
      const action = streakButton.getAttribute('aria-expanded') === 'true' ? 'Sluit kalender' : 'Open kalender';
      streakButton.setAttribute('aria-label', `🔥 ${streak} ${streak === 1 ? 'dag' : 'dagen'} streak. ${action}`);
    }
    const pStreak = document.getElementById('profileStreak');
    if (pStreak) pStreak.textContent = `🔥 Huidige streak: ${streak} ${streak === 1 ? 'dag' : 'dagen'}`;
  }

  function localDateKey(date) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
  }

  function getPlayedDailyDates() {
    const dates = new Set();
    const dailyByNumber = new Map(DAILY_PUZZLES.map(puzzle => [Number(puzzle.number), puzzle.date]));
    Object.entries(getLocalPlays()).forEach(([key, play]) => {
      if (/^\d{4}-\d{2}-\d{2}$/.test(key)) {
        dates.add(key);
        return;
      }
      const puzzleDate = dailyByNumber.get(Number(play?.puzzleNumber));
      if (puzzleDate) dates.add(puzzleDate);
    });
    return dates;
  }

  function renderStreakCalendar() {
    const grid = document.getElementById('streakCalendarGrid');
    const monthLabel = document.getElementById('streakCalendarMonth');
    if (!grid || !monthLabel) return;
    const year = streakCalendarDate.getFullYear();
    const month = streakCalendarDate.getMonth();
    const today = new Date();
    const todayKey = localDateKey(today);
    const playedDates = getPlayedDailyDates();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const startOffset = (new Date(year, month, 1).getDay() + 6) % 7;
    const cells = Array.from({ length: startOffset }, () => '<span aria-hidden="true"></span>');
    for (let day = 1; day <= daysInMonth; day += 1) {
      const date = new Date(year, month, day);
      const key = localDateKey(date);
      const played = playedDates.has(key);
      const isToday = key === todayKey;
      const isFuture = date > new Date(today.getFullYear(), today.getMonth(), today.getDate());
      const label = new Intl.DateTimeFormat(nettoNumberLocale(), { weekday:'long', day:'numeric', month:'long', year:'numeric' }).format(date);
      cells.push(`<span class="streak-calendar-day${played ? ' is-played' : ''}${isToday ? ' is-today' : ''}${isFuture ? ' is-future' : ''}" role="gridcell" aria-label="${label}${played ? ', daily gespeeld' : ', niet gespeeld'}" title="${played ? 'Daily gespeeld' : 'Niet gespeeld'}">${day}</span>`);
    }
    monthLabel.textContent = new Intl.DateTimeFormat(nettoNumberLocale(), { month:'long', year:'numeric' }).format(streakCalendarDate);
    grid.innerHTML = cells.join('');
    const currentMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    document.getElementById('streakCalendarNext').disabled = streakCalendarDate >= currentMonth;
  }

  function toggleStreakCalendar(event) {
    event?.stopPropagation();
    const popover = document.getElementById('streakCalendarPopover');
    const button = document.getElementById('streakButton');
    if (!popover || !button) return;
    const opening = popover.hidden;
    popover.hidden = !opening;
    button.setAttribute('aria-expanded', String(opening));
    const streak = getLocalStreak();
    button.setAttribute('aria-label', `🔥 ${streak} ${streak === 1 ? 'dag' : 'dagen'} streak. ${opening ? 'Sluit kalender' : 'Open kalender'}`);
    if (opening) renderStreakCalendar();
  }

  function closeStreakCalendar() {
    const popover = document.getElementById('streakCalendarPopover');
    const button = document.getElementById('streakButton');
    if (!popover || popover.hidden) return;
    popover.hidden = true;
    button?.setAttribute('aria-expanded', 'false');
    const streak = getLocalStreak();
    button?.setAttribute('aria-label', `🔥 ${streak} ${streak === 1 ? 'dag' : 'dagen'} streak. Open kalender`);
  }

  function closeStreakCalendarOnOutsideClick(event) {
    const popover = document.getElementById('streakCalendarPopover');
    const button = document.getElementById('streakButton');
    if (!popover || popover.hidden || popover.contains(event.target) || button?.contains(event.target)) return;
    closeStreakCalendar();
  }

  function closeStreakCalendarOnEscape(event) {
    if (event.key !== 'Escape') return;
    const popover = document.getElementById('streakCalendarPopover');
    if (!popover || popover.hidden) return;
    closeStreakCalendar();
    document.getElementById('streakButton')?.focus();
  }

  function moveStreakCalendarMonth(delta) {
    const next = new Date(streakCalendarDate.getFullYear(), streakCalendarDate.getMonth() + delta, 1);
    const today = new Date();
    const currentMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    if (next > currentMonth) return;
    streakCalendarDate = next;
    renderStreakCalendar();
  }

  // =========================================================================
  // 3. LIVE DUIZENDTAL-FORMATTERING & SARCASTISCHE TOASTS
  // =========================================================================
  function formatDutchNumber(str) {
    const isDutch = window.NettoI18n?.locale() === 'nl';
    const decimalMark = isDutch ? ',' : '.';
    const groupMark = isDutch ? '.' : ',';
    const cleanPattern = isDutch ? /[^\d,]/g : /[^\d.]/g;
    let clean = str.replace(cleanPattern, '');
    let parts = clean.split(decimalMark);
    let whole = parts[0].replace(/^0+(?=\d)/, ''); // Remove leading zeros
    if (whole === '') whole = '0';

    let formattedWhole = whole.replace(/\B(?=(\d{3})+(?!\d))/g, groupMark);
    return parts.length > 1 ? `${formattedWhole}${decimalMark}${parts[1].slice(0, 2)}` : formattedWhole;
  }

  function parseFormattedNumber(str) {
    if (!str) return NaN;
    const clean = window.NettoI18n?.locale() === 'nl'
      ? str.replace(/\./g, '').replace(',', '.')
      : str.replace(/,/g, '');
    return parseFloat(clean);
  }

  function showSarcasticToast(msg, isCopy = false) {
    const now = Date.now();
    if (!isCopy && now - lastToastTime < 1800) return; // Voorkom toast-spam
    lastToastTime = now;

    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${isCopy ? 'copy-toast' : ''}`;
    
    if (isCopy) {
      toast.innerHTML = `
        <div class="toast-icon">📋</div>
        <div class="toast-body">
          <b>Gekopieerd!</b>
          <span>${msg}</span>
        </div>
      `;
    } else {
      const quote = msg || SARCASTIC_QUOTES[Math.floor(Math.random() * SARCASTIC_QUOTES.length)];
      toast.innerHTML = `
        <div class="toast-icon">🧐</div>
        <div class="toast-body">
          <b>Cijfers gevraagd</b>
          <span>${quote}</span>
        </div>
      `;
    }

    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(-10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3800);
  }

  // Neutrale melding (geen alert): voor validaties en informatie
  function showNoticeToast(msg, icon = '💡') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = 'toast copy-toast';
    toast.innerHTML = `
      <div class="toast-icon">${icon}</div>
      <div class="toast-body">
        <b>Let op</b>
        <span>${msg}</span>
      </div>
    `;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(-10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3800);
  }

  let autoCalculatedInputs = new Set();
  // Settings: auto-calculator aan/uit (default aan). Uit = geen auto-fill, overal.
  const AUTO_CALC_KEY = 'netto_auto_calc';
  function isAutoCalcEnabled() { return localStorage.getItem(AUTO_CALC_KEY) !== 'off'; }
  function toggleAutoCalc() {
    const next = isAutoCalcEnabled() ? 'off' : 'on';
    localStorage.setItem(AUTO_CALC_KEY, next);
    updateAutoCalcToggle();
    if (!isAutoCalcEnabled()) {
      // Direct alle huidige auto-ingevulde velden leegmaken.
      [...autoCalculatedInputs].forEach(id => clearAutoInput(id));
    }
    showSarcasticToast(next === 'on' ? 'Auto-calculator staat nu AAN' : 'Auto-calculator staat nu UIT', true);
  }
  function updateAutoCalcToggle() {
    const toggle = document.getElementById('autoCalcToggle');
    if (toggle) toggle.setAttribute('aria-checked', String(isAutoCalcEnabled()));
  }

  // ===== Thema: light (Netto-blauw) / dark (goud op navy) =====
  const THEME_KEY = 'netto_theme';
  function isDarkTheme() { return (localStorage.getItem(THEME_KEY) || 'light') === 'dark'; }
  function applyTheme() {
    document.documentElement.dataset.theme = isDarkTheme() ? 'dark' : 'light';
    const toggle = document.getElementById('themeToggle');
    if (toggle) toggle.setAttribute('aria-checked', String(isDarkTheme()));
  }
  function toggleTheme() {
    localStorage.setItem(THEME_KEY, isDarkTheme() ? 'light' : 'dark');
    applyTheme();
  }
  function dailyOperator() { return PUZZLE_DATA?.operator || '×'; }
  function calculateDailyValue(a, b, operator) {
    if (operator === '+') return a + b;
    if (operator === '−' || operator === '-') return a - b;
    if (operator === '×' || operator === '*') return a * b;
    if (operator === '÷' || operator === '/') return b === 0 ? NaN : a / b;
    return NaN;
  }
  function exactNumber(value) { return Number.isFinite(value) && Math.abs(value - Math.round(value)) < 1e-9 ? Math.round(value) : value; }
  function setAutoInput(id, value) {
    const input = document.getElementById(id); if (!input || !Number.isFinite(value)) return;
    input.value = formatDutchNumber(String(exactNumber(value)).replace('.', ','));
    autoCalculatedInputs.add(id); input.dataset.autoCalculated = 'true'; input.classList.add('auto-calculated');
    input.setAttribute('aria-label', 'Automatisch berekend antwoord');
  }
  function clearAutoInput(id) {
    const input = document.getElementById(id); if (!input || !autoCalculatedInputs.has(id)) return;
    input.value = ''; input.placeholder = 'Jouw schatting'; input.dataset.autoCalculated = 'false'; input.classList.remove('auto-calculated'); autoCalculatedInputs.delete(id);
  }
  function calculateDerivedValues(ids, operator) {
    if (!isAutoCalcEnabled()) return;
    const inputs = ids.map(id => document.getElementById(id));
    if (inputs.some(input => !input)) return;
    const values = inputs.map(input => parseFormattedNumber(input.value));
    const [a, b, c] = values;
    inputs.forEach((input, index) => {
      if (autoCalculatedInputs.has(input.id) && document.activeElement?.id !== input.id) clearAutoInput(input.id);
      else if (autoCalculatedInputs.has(input.id) && !Number.isFinite(values[index])) clearAutoInput(input.id);
    });
    const fresh = ids.map(id => parseFormattedNumber(document.getElementById(id).value));
    const [left, middle, result] = fresh;
    if (Number.isFinite(left) && Number.isFinite(middle) && !Number.isFinite(result)) {
      setAutoInput(ids[2], calculateDailyValue(left, middle, operator));
    } else if (Number.isFinite(left) && Number.isFinite(result) && !Number.isFinite(middle)) {
      const value = operator === '+' ? result - left : operator === '−' || operator === '-' ? left - result : operator === '×' || operator === '*' ? (left === 0 ? NaN : result / left) : operator === '÷' || operator === '/' ? (result === 0 ? NaN : left / result) : NaN;
      if (operator !== '÷' && operator !== '/' || Number.isInteger(value)) setAutoInput(ids[1], value);
    } else if (Number.isFinite(middle) && Number.isFinite(result) && !Number.isFinite(left)) {
      const value = operator === '+' ? result - middle : operator === '−' || operator === '-' ? result + middle : operator === '×' || operator === '*' ? (middle === 0 ? NaN : result / middle) : operator === '÷' || operator === '/' ? middle * result : NaN;
      if (operator !== '÷' && operator !== '/' || Number.isInteger(value)) setAutoInput(ids[0], value);
    }
  }
  function updateDailyDerivedInput() { calculateDerivedValues(['g1','g2','g3'], dailyOperator()); }
  function bindDerivedInputs(prefix, operator) {
    const ids = [`${prefix}Answer0`, `${prefix}Answer1`, `${prefix}Answer2`];
    const inputs = ids.map(id => document.getElementById(id));
    if (inputs.some(input => !input)) return;
    inputs.forEach(input => {
      input.addEventListener('focus', () => {
        input.dataset.editing = 'true';
        // Dit geldt ook voor Daily: bij focus krijgt de speler het automatische veld terug.
        if (autoCalculatedInputs.has(input.id)) clearAutoInput(input.id);
      });
      input.addEventListener('blur', () => {
        input.dataset.editing = 'false';
        if (!input.value.trim()) calculateDerivedValues(ids, operator);
      });
      input.addEventListener('input', () => {
        autoCalculatedInputs.delete(input.id);
        input.dataset.autoCalculated = 'false';
        input.placeholder = input.value.trim() ? '' : 'Jouw schatting';
        input.classList.remove('auto-calculated');
        if (!input.value.trim()) input.placeholder = 'Jouw schatting';
        calculateDerivedValues(ids, operator);
      });
    });
    calculateDerivedValues(ids, operator);
  }

  function initInputs() {
    ['g1', 'g2', 'g3'].forEach((id, index, arr) => {
      const input = document.getElementById(id);
      
      // Detecteer letters bij keydown
      input.addEventListener('keydown', (e) => {
        // Navigatie met Enter
        if (e.key === 'Enter') {
          if (index < arr.length - 1) {
            document.getElementById(arr[index + 1]).focus();
          } else {
            checkAnswers();
          }
          return;
        }

        // Toegestane besturingstoetsen
        const allowed = ['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab', 'Enter', 'Home', 'End'];
        if (allowed.includes(e.key) || e.ctrlKey || e.metaKey) return;

        // Als er een letter of ongeldig teken wordt ingedrukt
        if (!/[\d,]/.test(e.key)) {
          e.preventDefault();
          input.classList.add('shake');
          setTimeout(() => input.classList.remove('shake'), 400);
          showSarcasticToast();
        }
      });

      // Formatteer bij invoer
      input.addEventListener('input', (e) => {
        let val = input.value;
        if (/[a-zA-Z]/.test(val)) {
          showSarcasticToast();
        }
        if (val.trim() === '') {
          autoCalculatedInputs.delete(id);
          input.dataset.autoCalculated = 'false';
          input.placeholder = 'Jouw schatting';
          input.classList.remove('auto-calculated');
          updateDailyDerivedInput();
          return;
        }
        input.value = formatDutchNumber(val);
        autoCalculatedInputs.delete(id); input.dataset.autoCalculated = 'false'; input.classList.remove('auto-calculated');
        updateDailyDerivedInput();
      });
    });
  }

  // =========================================================================
  // 4. SPEL LOGICA & SCORES
  // =========================================================================
  function scoreVraag(g, w) {
    if (!g || g <= 0) return 10;
    return Math.max(g / w, w / g);
  }

  function fmt(n) {
    if (n === null || n === undefined || isNaN(Number(n))) return '';
    return Number(n).toLocaleString(nettoNumberLocale());
  }

  function getFactorRating(factor) {
    if (factor <= 1.15) return { color: 'var(--green)', bg: '#D1FAE5', emoji: '🟩', label: 'Spot on!' };
    if (factor <= 1.50) return { color: '#D97706', bg: '#FEF3C7', emoji: '🟨', label: 'Dichtbij' };
    if (factor <= 2.50) return { color: 'var(--orange)', bg: '#FFEDD5', emoji: '🟧', label: 'Ruime schatting' };
    return { color: 'var(--red)', bg: '#FEE2E2', emoji: '🟥', label: 'Ver uit de buurt' };
  }

  function getActivePuzzleKey() {
    return PUZZLE_DATA?.date || (activePuzzleIndex === 0 ? TODAY_STR : `puzzle_${PUZZLE_DATA.number}`);
  }

  function checkExistingPlay() {
    const plays = getLocalPlays();
    const pKey = getActivePuzzleKey();
    const existingPlay = plays[pKey];
    const streak = getLocalStreak();
    updateStreakUI(streak);

    if (existingPlay) {
      // Reeds gespeeld voor deze puzzel
      document.getElementById('g1').value = fmt(existingPlay.g1);
      document.getElementById('g2').value = fmt(existingPlay.g2);
      document.getElementById('g3').value = fmt(existingPlay.g3);
      ['g1', 'g2', 'g3'].forEach(id => document.getElementById(id).disabled = true);
      document.getElementById('btnCheck').style.display = 'none';
      document.getElementById('alreadyPlayedBanner').classList.add('show');
      renderResultsUI(existingPlay.g1, existingPlay.g2, existingPlay.g3, existingPlay.factor);
    }
  }

  function checkAnswers() {
    const g1 = parseFormattedNumber(document.getElementById('g1').value);
    const g2 = parseFormattedNumber(document.getElementById('g2').value);
    const g3 = parseFormattedNumber(document.getElementById('g3').value);

    if (isNaN(g1) || isNaN(g2) || isNaN(g3) || g1 <= 0 || g2 <= 0 || g3 <= 0) {
      showNoticeToast('Vul eerst alle drie de vragen in met een getal groter dan 0.');
      return;
    }

    const s1 = scoreVraag(g1, PUZZEL_ECHT().a1);
    const s2 = scoreVraag(g2, PUZZEL_ECHT().a2);
    const s3 = scoreVraag(g3, PUZZEL_ECHT().a3);
    const avgFactor = (s1 + s2 + s3) / 3;

    // Streak bijwerken (bij de dagelijkse puzzel)
    let streak = getLocalStreak();
    const plays = getLocalPlays();
    const pKey = getActivePuzzleKey();

    if (!plays[pKey] && PUZZLE_DATA?.date === TODAY_STR) {
      streak += 1;
      localStorage.setItem('netto_streak', streak.toString());
    }
    updateStreakUI(streak);

    // Opslaan in LocalStorage
    plays[pKey] = { g1, g2, g3, factor: avgFactor, puzzleNumber: PUZZLE_DATA.number, playedAt: new Date().toISOString() };
    localStorage.setItem('netto_plays', JSON.stringify(plays));
    if (!document.getElementById('streakCalendarPopover')?.hidden) renderStreakCalendar();

    // Velden uitschakelen
    ['g1', 'g2', 'g3'].forEach(id => document.getElementById(id).disabled = true);
    document.getElementById('btnCheck').style.display = 'none';

    renderResultsUI(g1, g2, g3, avgFactor);

    // Sync naar Cloud / Supabase als ingelogd
    if (PUZZLE_DATA?.date === TODAY_STR) syncPlayToCloud(TODAY_STR, g1, g2, g3, avgFactor);
  }

  function PUZZEL_ECHT() {
    return { a1: PUZZLE_DATA.q1_answer, a2: PUZZLE_DATA.q2_answer, a3: PUZZLE_DATA.q3_answer };
  }

  function renderResultsUI(g1, g2, g3, avgFactor) {
    const echt = PUZZEL_ECHT();
    const s1 = scoreVraag(g1, echt.a1);
    const s2 = scoreVraag(g2, echt.a2);
    const s3 = scoreVraag(g3, echt.a3);

    const isSpotOn1 = Math.abs(g1 - echt.a1) < 0.001;
    const isSpotOn2 = Math.abs(g2 - echt.a2) < 0.001;
    const isSpotOn3 = Math.abs(g3 - echt.a3) < 0.001;

    document.getElementById('a1').innerHTML = fmt(echt.a1) + (isSpotOn1 ? '<div class="spot-on-sub">Spot on! 🎯</div>' : `<div class="guess-sub">Jouw gok: ${fmt(g1)}</div>`);
    document.getElementById('a2').innerHTML = fmt(echt.a2) + (isSpotOn2 ? '<div class="spot-on-sub">Spot on! 🎯</div>' : `<div class="guess-sub">Jouw gok: ${fmt(g2)}</div>`);
    document.getElementById('a3').innerHTML = fmt(echt.a3) + (isSpotOn3 ? '<div class="spot-on-sub">Spot on! 🎯</div>' : `<div class="guess-sub">Jouw gok: ${fmt(g3)}</div>`);

    renderBadge('badge-q1', s1, g1, echt.a1);
    renderBadge('badge-q2', s2, g2, echt.a2);
    renderBadge('badge-q3', s3, g3, echt.a3);

    // Nauwkeurigheid (Optie A: 100 / avgFactor)
    const accuracy = Math.round(100 / avgFactor);
    document.getElementById('scoreBadge').textContent = `${accuracy}%`;
    const factorEl = document.getElementById('scoreBadgeFactor');
    if (factorEl) {
      factorEl.textContent = `Gemiddelde afwijking: ${avgFactor.toFixed(2)}×`;
    }
    
    let msg = "🎯 Meesterlijk geschat!";
    if (isSpotOn1 && isSpotOn2 && isSpotOn3) msg = "👑 100% SPOT ON! Wiskundig Orakel!";
    else if (accuracy >= 95) msg = "👑 Wiskundig Genie · Meesterlijk geschat!";
    else if (accuracy >= 85) msg = "🎯 Scherpschutter · Heel strak in de buurt!";
    else if (accuracy >= 70) msg = "💡 Scherp Inzicht · Goede schatting!";
    else if (accuracy >= 50) msg = "🧭 Goeie Richting · Redelijke ordegrootte!";
    else msg = "🎲 Wilde Gok · Oef, rekenmachine nodig!";
    document.getElementById('scoreBadgeMsg').textContent = msg;

    // Getallenbalk tekenen
    renderNumberLine(g1, g2, g3, echt.a1, echt.a2, echt.a3, PUZZLE_DATA.operator || '×');

    if (currentUser) {
      document.getElementById('cloudSyncBanner').style.display = 'none';
    } else {
      document.getElementById('cloudSyncBanner').style.display = 'flex';
    }

    document.getElementById('results').classList.add('show');
    if (dailyArchivePuzzleView) showDailyResults();
    if (activePuzzleIndex === 0) startDailyCountdown();
    else { const countdown = document.getElementById('dailyCountdown'); if (countdown) countdown.remove(); if (countdownTimer) clearInterval(countdownTimer); }
    renderDailyArchive();
  }

  function renderBadge(elemId, factor, guess, actual) {
    const el = document.getElementById(elemId);
    if (!el) return;
    const isSpotOn = guess !== undefined && actual !== undefined && Math.abs(guess - actual) < 0.001;
    if (isSpotOn) {
      el.style.background = '#10B981';
      el.style.color = '#FFFFFF';
      el.innerHTML = `🎯 Spot on!`;
      return;
    }
    const r = getFactorRating(factor);
    const qAcc = Math.round(100 / factor);
    el.style.background = r.bg;
    el.style.color = r.color;
    el.innerHTML = `${r.emoji} ${qAcc}% (${factor.toFixed(2)}×)`;
  }

  // =========================================================================
  // DE GETALLENBALK (6 PUNTEN: WERKELIJKHEID VS SCHATTINGEN)
  // =========================================================================
  function renderNumberLine(g1, g2, g3, a1, a2, a3, op) {
    const container = document.getElementById('numberlineCard');
    if (!container) return;

    const pairs = [
      { id: 1, name: 'Vraag 1', guess: g1, actual: a1, color: '#4F46E5' },
      { id: 2, name: 'Vraag 2', guess: g2, actual: a2, color: '#D97706' },
      { id: 3, name: 'Vraag 3 (Uitkomst)', guess: g3, actual: a3, color: '#059669' }
    ];

    const vals = [g1, a1, g2, a2, g3, a3].filter(v => Number.isFinite(v) && v > 0);
    const minVal = vals.length ? Math.min(...vals) : 1;
    const maxVal = vals.length ? Math.max(...vals) : 100;
    const useLog = (maxVal / Math.max(1, minVal)) > 4;

    function calcPct(val) {
      if (minVal === maxVal) return 50.0;
      let p;
      if (useLog && minVal > 0 && val > 0) {
        p = (Math.log10(val) - Math.log10(minVal)) / (Math.log10(maxVal) - Math.log10(minVal));
      } else {
        p = (val - minVal) / (maxVal - minVal);
      }
      return 8.0 + Math.max(0, Math.min(1, p)) * 84.0;
    }

    let ownCalcConsistent = false;
    if (op === '×' || op === '*' || op === 'x') {
      ownCalcConsistent = (g1 * g2 === g3);
    } else if (op === '+') {
      ownCalcConsistent = (g1 + g2 === g3);
    } else if (op === '−' || op === '-') {
      ownCalcConsistent = (g1 - g2 === g3);
    } else if (op === '÷' || op === '/') {
      ownCalcConsistent = (g2 !== 0 && g1 / g2 === g3);
    }

    const formulaTagHtml = ownCalcConsistent
      ? `<span class="numberline-formula-tag consistent">✓ Jouw som klopte onderling! (${fmt(g1)} ${op} ${fmt(g2)} = ${fmt(g3)})</span>`
      : `<span class="numberline-formula-tag">Jouw som: ${fmt(g1)} ${op} ${fmt(g2)} = ${fmt(g3)}</span>`;

    let lanesHtml = '';
    pairs.forEach(p => {
      const isSpotOn = Math.abs(p.guess - p.actual) < 0.001;
      const pctActual = calcPct(p.actual);
      const pctGuess = calcPct(p.guess);
      const minPct = Math.min(pctActual, pctGuess);
      const widthPct = Math.max(1, Math.abs(pctActual - pctGuess));

      if (isSpotOn) {
        lanesHtml += `
          <div class="numberline-lane">
            <span class="numberline-lane-label" style="color:${p.color}">${p.name}</span>
            <div class="numberline-track"></div>
            <div class="numberline-point" style="left:${pctActual}%;">
              <div class="numberline-point-marker spoton"></div>
              <div class="numberline-point-label" style="color:#065F46; border-color:#34D399;">
                Spot on! 🎯 (${fmt(p.actual)})
              </div>
            </div>
          </div>
        `;
      } else {
        lanesHtml += `
          <div class="numberline-lane">
            <span class="numberline-lane-label" style="color:${p.color}">${p.name}</span>
            <div class="numberline-track"></div>
            <div class="numberline-connector" style="left:${minPct}%; width:${widthPct}%; background:${p.color};"></div>

            <div class="numberline-point" style="left:${pctActual}%;">
              <div class="numberline-point-marker actual" style="border-color:${p.color}; background:#FFFFFF;"></div>
              <div class="numberline-point-label" style="color:${p.color};">
                🎯 ${fmt(p.actual)}
              </div>
            </div>

            <div class="numberline-point" style="left:${pctGuess}%;">
              <div class="numberline-point-marker" style="background:${p.color};"></div>
              <div class="numberline-point-label" style="color:#1E293B;">
                Jij: ${fmt(p.guess)}
              </div>
            </div>
          </div>
        `;
      }
    });

    container.innerHTML = `
      <div class="numberline-header">
        <span class="numberline-title">📏 De Getallenbalk</span>
        ${formulaTagHtml}
      </div>
      <div class="numberline-lanes">
        ${lanesHtml}
      </div>
      <div class="numberline-axis">
        <span>Min: ${fmt(minVal)}</span>
        <span>${useLog ? 'Logaritmische schaal' : 'Relatieve schaal'}</span>
        <span>Max: ${fmt(maxVal)}</span>
      </div>
      <div class="numberline-legend">
        <div class="numberline-legend-item"><span style="display:inline-block; width:10px; height:10px; border-radius:2px; transform:rotate(45deg); border:2px solid #64748B;"></span> 🎯 Echt antwoord</div>
        <div class="numberline-legend-item"><span style="display:inline-block; width:10px; height:10px; border-radius:99px; background:#64748B;"></span> ● Jouw schatting</div>
        <div class="numberline-legend-item"><span style="display:inline-block; width:10px; height:10px; border-radius:99px; background:#10B981;"></span> 🎯 Spot on!</div>
      </div>
    `;
  }

  // =========================================================================
  // 5. WORDLE-STIJL SCORE DELEN
  // =========================================================================
  function shareScore() {
    const plays = getLocalPlays();
    const pKey = getActivePuzzleKey();
    const play = plays[pKey] || plays[TODAY_STR];
    if (!play) return;

    const echt = PUZZEL_ECHT();
    const s1 = scoreVraag(play.g1, echt.a1);
    const s2 = scoreVraag(play.g2, echt.a2);
    const s3 = scoreVraag(play.g3, echt.a3);
    const streak = getLocalStreak();
    const acc = Math.round(100 / play.factor);

    function formatLine(emoji, g, a, f) {
      if (Math.abs(g - a) < 0.001) return `🎯 Spot on!`;
      const qAcc = Math.round(100 / f);
      return `${emoji} ${qAcc}% (${f.toFixed(2)}×)`;
    }

    const r1 = getFactorRating(s1);
    const r2 = getFactorRating(s2);
    const r3 = getFactorRating(s3);

    const text = `Netto #${PUZZLE_DATA.number} · Score: ${acc}% 🎯 (${play.factor.toFixed(2)}×)\n1️⃣ ${formatLine(r1.emoji, play.g1, echt.a1, s1)}\n2️⃣ ${formatLine(r2.emoji, play.g2, echt.a2, s2)}\n3️⃣ ${formatLine(r3.emoji, play.g3, echt.a3, s3)}\n🔥 Streak: ${streak} ${streak === 1 ? 'dag' : 'dagen'}\nhttps://netto.game`;

    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(() => {
        showSarcasticToast("Score gekopieerd naar klembord! Deel het in je groepsapp.", true);
      }).catch(() => fallbackPrompt(text));
    } else {
      fallbackPrompt(text);
    }
  }

  function fallbackPrompt(text) {
    prompt("Kopieer jouw uitslag:", text);
  }

  // =========================================================================
  // 6. CLOUD SYNC & AUTH (Supabase)
  // =========================================================================
  function loadUserProfile() {
    const savedUser = localStorage.getItem('netto_user');
    if (savedUser) {
      try {
        currentUser = JSON.parse(savedUser);
        updateUserUI();
      } catch(e) {}
    }
  }

  function updateUserUI() {
    const userBtn = document.getElementById('topbarUserBtn');
    if (currentUser) {
      document.getElementById('topbarUsername').textContent = currentUser.username || currentUser.email.split('@')[0];
      userBtn.classList.add('logged-in');
      const sidebarAuthLabel = document.getElementById('sidebarAuthLabel');
      if (sidebarAuthLabel) sidebarAuthLabel.textContent = `Profiel (${currentUser.username || 'Speler'})`;
      document.getElementById('profileUsername').textContent = currentUser.username || currentUser.email;
      document.getElementById('profileEmailSubtitle').textContent = currentUser.email;
      document.getElementById('cloudSyncBanner').style.display = 'none';
    } else {
      document.getElementById('topbarUsername').textContent = 'Inloggen';
      userBtn.classList.remove('logged-in');
      const sidebarLabel = document.getElementById('sidebarAuthLabel');
      if (sidebarLabel) sidebarLabel.textContent = 'Inloggen / Registreren';
    }
  }

  async function syncPlayToCloud(dateStr, g1, g2, g3, factor) {
    if (!currentUser) return;

    if (supabaseClient) {
      try {
        // Daily score blijft per datum opgeslagen.
        const { error } = await supabaseClient.from('user_plays').upsert({
          user_id: currentUser.id,
          puzzle_date: dateStr,
          g1, g2, g3, factor
        }, { onConflict: 'user_id, puzzle_date' });

        if (error) console.warn('Supabase sync error:', error);
      } catch (err) {
        console.warn('Sync failed:', err);
      }
    }
  }

  async function syncLibraryPlay(puzzle, g1, g2, g3, factor) {
    if (!currentUser || !supabaseClient || !puzzle?.id) return;
    const { error } = await supabaseClient.from('library_plays').upsert({ user_id: currentUser.id, puzzle_id: puzzle.id, g1, g2, g3, factor }, { onConflict: 'user_id,puzzle_id' });
    if (error) console.warn('Library score sync error:', error);
  }


  // ===== Auth helpers: Nederlandse foutmeldingen, validatie, rate limiting =====
  function mapAuthError(message) {
    const m = (message || '').toLowerCase();
    if (m.includes('rate limit') || m.includes('too many requests') || m.includes('email rate'))
      return 'Te veel pogingen. Probeer het over een uur opnieuw.';
    if (m.includes('invalid login credentials'))
      return 'Onjuist e-mailadres of wachtwoord.';
    if (m.includes('email not confirmed'))
      return 'Bevestig eerst je e-mailadres via de link in je inbox.';
    if (m.includes('user already registered') || m.includes('already been registered'))
      return 'Er bestaat al een account met dit e-mailadres. Log in of gebruik "Wachtwoord vergeten?".';
    if (m.includes('password should be at least') || m.includes('weak password'))
      return 'Je wachtwoord is te zwak — gebruik minimaal 8 tekens.';
    if (m.includes('invalid format') && m.includes('email'))
      return 'Dit e-mailadres ziet er niet goed uit.';
    if (m.includes('unable to validate email'))
      return 'Dit e-mailadres ziet er niet goed uit.';
    if (m.includes('failed to fetch') || m.includes('network'))
      return 'Kan geen verbinding maken met de server. Controleer je internet.';
    return 'Er ging iets mis: ' + (message || 'onbekende fout');
  }

  function showAuthError(msg) {
    const box = document.getElementById('authErrorBox');
    box.textContent = msg;
    box.style.display = 'block';
  }
  function clearAuthError() {
    const box = document.getElementById('authErrorBox');
    box.style.display = 'none';
  }

  function setAuthBusy(busy) {
    const btn = document.getElementById('authSubmitBtn');
    btn.disabled = busy;
    btn.textContent = busy ? 'Even geduld…' : (authMode === 'login' ? 'Inloggen' : 'Account Aanmaken');
    btn.style.opacity = busy ? '0.6' : '1';
  }

  // Rate limiting: max 5 signup-pogingen per uur per browser.
  const SIGNUP_LIMIT = 5;
  const SIGNUP_WINDOW_MS = 60 * 60 * 1000;
  function getSignupAttempts() {
    try {
      const raw = JSON.parse(localStorage.getItem('netto_signup_attempts') || '[]');
      const now = Date.now();
      return raw.filter(t => now - t < SIGNUP_WINDOW_MS);
    } catch (e) { return []; }
  }
  function signupRateLimited() {
    return getSignupAttempts().length >= SIGNUP_LIMIT;
  }
  function recordSignupAttempt() {
    const attempts = getSignupAttempts();
    attempts.push(Date.now());
    localStorage.setItem('netto_signup_attempts', JSON.stringify(attempts));
  }
  function signupCooldownText() {
    const attempts = getSignupAttempts();
    if (!attempts.length) return '';
    const oldest = Math.min(...attempts);
    const waitMs = SIGNUP_WINDOW_MS - (Date.now() - oldest);
    const mins = Math.max(1, Math.ceil(waitMs / 60000));
    return `Je hebt ${attempts.length} van de ${SIGNUP_LIMIT} registraties per uur gebruikt. Over ~${mins} minuten kun je weer registreren.`;
  }

  function validateAuthInput(email, password, username) {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return 'Vul een geldig e-mailadres in.';
    // Minimale wachtwoordlengte geldt alleen bij registreren: een bestaand
    // account (bijv. met een kort wachtwoord van vóór deze regel) moet
    // gewoon kunnen inloggen — Supabase bewaakt de echte verificatie.
    if (authMode === 'register') {
      if (password.length < 8) return 'Je wachtwoord moet minimaal 8 tekens zijn.';
      if (password.length > 72) return 'Je wachtwoord mag maximaal 72 tekens zijn.';
      if (username) {
        if (username.length < 3 || username.length > 20) return 'Je spelersnaam moet 3 tot 20 tekens zijn.';
      }
    } else {
      if (!password) return 'Vul je wachtwoord in.';
    }
    return null;
  }

  async function handleAuthSubmit(e) {
    e.preventDefault();
    clearAuthError();
    const email = document.getElementById('authEmail').value.trim().toLowerCase();
    const password = document.getElementById('authPassword').value;
    const username = document.getElementById('authUsername').value.trim() || email.split('@')[0];

    const validationError = validateAuthInput(email, password, username);
    if (validationError) { showAuthError(validationError); return; }

    if (!supabaseClient) {
      showAuthError('De server is momenteel niet beschikbaar. Probeer het later opnieuw — inloggen zonder server is niet mogelijk.');
      return;
    }

    if (authMode === 'register' && signupRateLimited()) {
      showAuthError('Te veel registratiepogingen. ' + signupCooldownText());
      return;
    }

    setAuthBusy(true);
    try {
      if (authMode === 'register') {
        recordSignupAttempt();
        const { data, error } = await supabaseClient.auth.signUp({
          email, password,
          options: { data: { username } }
        });
        if (error) throw error;
        if (!data.session) {
          showSarcasticToast('Account aangemaakt! Bevestig je e-mailadres via de link in je inbox, daarna kun je inloggen.', true);
          setAuthBusy(false);
          return;
        }
        currentUser = { id: data.user.id, email, username };
      } else {
        const { data, error } = await supabaseClient.auth.signInWithPassword({ email, password });
        if (error) throw error;
        currentUser = { id: data.user.id, email, username: data.user.user_metadata?.username || username };
      }
    } catch (err) {
      showAuthError(mapAuthError(err.message));
      setAuthBusy(false);
      return;
    }
    setAuthBusy(false);

    localStorage.setItem('netto_user', JSON.stringify(currentUser));
    updateUserUI();
    closeAuthModal();
    showSarcasticToast(`Welkom terug, ${currentUser.username}! Je scores zijn gesynchroniseerd.`, true);
    checkSubmissionNotifications();

    // Sync eventuele vandaag al gespeelde puzzel
    const plays = getLocalPlays();
    if (plays[TODAY_STR]) {
      const p = plays[TODAY_STR];
      syncPlayToCloud(TODAY_STR, p.g1, p.g2, p.g3, p.factor);
    }
  }

  // ===== Wachtwoord vergeten =====
  function showForgotPassword() {
    clearAuthError();
    document.getElementById('authFormView').style.display = 'none';
    document.getElementById('authForgotView').style.display = 'block';
    const email = document.getElementById('authEmail').value.trim();
    if (email) document.getElementById('forgotEmail').value = email;
  }
  function backToAuthForm() {
    document.getElementById('forgotErrorBox').style.display = 'none';
    document.getElementById('authForgotView').style.display = 'none';
    document.getElementById('authFormView').style.display = 'block';
  }
  async function handleForgotPassword(e) {
    e.preventDefault();
    const box = document.getElementById('forgotErrorBox');
    box.style.display = 'none';
    const email = document.getElementById('forgotEmail').value.trim().toLowerCase();
    if (!supabaseClient) {
      box.textContent = 'De server is momenteel niet beschikbaar. Probeer het later opnieuw.';
      box.style.display = 'block';
      return;
    }
    const btn = document.getElementById('forgotSubmitBtn');
    btn.disabled = true;
    btn.textContent = 'Versturen…';
    try {
      const { error } = await supabaseClient.auth.resetPasswordForEmail(email);
      if (error) throw error;
      backToAuthForm();
      showSarcasticToast('Resetlink verstuurd! Check je inbox (ook de spam-map).', true);
    } catch (err) {
      box.textContent = mapAuthError(err.message);
      box.style.display = 'block';
    }
    btn.disabled = false;
    btn.textContent = 'Verstuur resetlink';
  }

  function handleLogout() {
    if (supabaseClient) supabaseClient.auth.signOut();
    currentUser = null;
    localStorage.removeItem('netto_user');
    updateUserUI();
    closeAuthModal();
    showSarcasticToast("Succesvol uitgelogd.", true);
  }

  function toggleAuthMode() {
    authMode = authMode === 'login' ? 'register' : 'login';
    clearAuthError();
    document.getElementById('authTitle').textContent = authMode === 'login' ? 'Inloggen' : 'Registreren';
    document.getElementById('authSubmitBtn').textContent = authMode === 'login' ? 'Inloggen' : 'Account Aanmaken';
    document.getElementById('usernameGroup').style.display = authMode === 'register' ? 'block' : 'none';
    document.getElementById('authToggleText').textContent = authMode === 'login' ? 'Nog geen account? ' : 'Al een account? ';
    document.getElementById('authToggleLink').textContent = authMode === 'login' ? 'Registreer gratis' : 'Log hier in';
  }

  // =========================================================================
  // 7. LEADERBOARD RENDERING
  // =========================================================================
  function renderLeaderboard() {
    const list = document.getElementById('leaderboardList');
    list.innerHTML = '';

    const plays = getLocalPlays();
    const myToday = plays[TODAY_STR];
    const myStreak = getLocalStreak();

    if (currentLbTab === 'today') {
      // Mock data aangevuld met actuele speler
      let todayScores = [
        { rank: 1, name: "WiskundeKoning", factor: 1.03, streak: 12 },
        { rank: 2, name: "StatistiekNL", factor: 1.07, streak: 8 },
        { rank: 3, name: "Fermii_Fan", factor: 1.11, streak: 19 },
        { rank: 4, name: "EftelingMaster", factor: 1.14, streak: 4 },
        { rank: 5, name: "DataDaan", factor: 1.18, streak: 15 }
      ];

      if (myToday) {
        const myName = currentUser ? (currentUser.username || currentUser.email) : "Jij (deze browser)";
        todayScores.push({ rank: '•', name: `${myName} 👈`, factor: myToday.factor, streak: myStreak, isMe: true });
        todayScores.sort((a, b) => a.factor - b.factor);
      }

      todayScores.forEach((row, i) => {
        const div = document.createElement('div');
        div.className = `lb-row ${row.isMe ? 'me' : ''}`;
        div.innerHTML = `
          <div class="lb-left">
            <span class="lb-rank">#${i + 1}</span>
            <div>
              <div class="lb-name">${row.name}</div>
              <div class="lb-streak">🔥 ${row.streak}d streak</div>
            </div>
          </div>
          <span class="lb-score">${row.factor.toFixed(2)}×</span>
        `;
        list.appendChild(div);
      });
    } else {
      // Top Streaks tab
      let streaks = [
        { rank: 1, name: "Fermii_Fan", streak: 42 },
        { rank: 2, name: "WiskundeKoning", streak: 38 },
        { rank: 3, name: "DataDaan", streak: 29 },
        { rank: 4, name: "ProfessorX", streak: 21 },
        { rank: 5, name: "AnoniemeSchatters", streak: 16 }
      ];

      if (currentUser || myStreak > 0) {
        const myName = currentUser ? (currentUser.username || currentUser.email) : "Jij";
        streaks.push({ rank: '•', name: `${myName} 👈`, streak: myStreak, isMe: true });
        streaks.sort((a, b) => b.streak - a.streak);
      }

      streaks.forEach((row, i) => {
        const div = document.createElement('div');
        div.className = `lb-row ${row.isMe ? 'me' : ''}`;
        div.innerHTML = `
          <div class="lb-left">
            <span class="lb-rank">#${i + 1}</span>
            <div class="lb-name">${row.name}</div>
          </div>
          <span class="lb-score" style="color:#D97706;">🔥 ${row.streak} dagen</span>
        `;
        list.appendChild(div);
      });
    }
  }

  function switchLbTab(tab) {
    currentLbTab = tab;
    document.getElementById('tabTodayBtn').classList.toggle('active', tab === 'today');
    document.getElementById('tabStreaksBtn').classList.toggle('active', tab === 'streaks');
    renderLeaderboard();
  }

  // =========================================================================
  // 8. MODAL & SCREEN CONTROLLERS
  // =========================================================================
  function toggleMenu() {
    document.getElementById('hamburgerBtn').classList.toggle('open');
    document.getElementById('sidebar').classList.toggle('open');
    document.getElementById('overlay').classList.toggle('show');
  }

  function closeMenu() {
    document.getElementById('hamburgerBtn').classList.remove('open');
    document.getElementById('sidebar').classList.remove('open');
    document.getElementById('overlay').classList.remove('show');
  }

  let countdownTimer = null;

  function updateDailyReviewNav() {
    const nav = document.getElementById('dailyReviewNav');
    const questionsButton = document.getElementById('dailyQuestionsNav');
    const resultsButton = document.getElementById('dailyResultsNav');
    const position = document.getElementById('dailyReviewPosition');
    if (!nav || !questionsButton || !resultsButton || !position) return;
    nav.classList.add('show');
    const showingResults = dailyReviewView === 'results';
    questionsButton.disabled = !showingResults;
    resultsButton.disabled = showingResults;
    questionsButton.setAttribute('aria-disabled', String(!showingResults));
    resultsButton.setAttribute('aria-disabled', String(showingResults));
    position.textContent = showingResults ? 'Resultaat' : 'Vragen';
  }

  function showDailyResults() {
    const questions = document.getElementById('dailyQuestionView');
    const results = document.getElementById('results');
    if (!questions || !results) return;
    dailyReviewView = 'results';
    questions.style.display = 'none';
    results.classList.add('show');
    updateDailyReviewNav();
  }

  function showDailyQuestions() {
    const questions = document.getElementById('dailyQuestionView');
    const results = document.getElementById('results');
    if (!questions || !results) return;
    dailyReviewView = 'questions';
    questions.style.display = 'block';
    results.classList.remove('show');
    updateDailyReviewNav();
  }

  function resetDailyReviewView() {
    const questions = document.getElementById('dailyQuestionView');
    const nav = document.getElementById('dailyReviewNav');
    const results = document.getElementById('results');
    if (questions) questions.style.display = 'block';
    if (nav) nav.classList.remove('show');
    if (results) results.classList.remove('show');
    dailyReviewView = 'questions';
  }

  function londonMidnightTarget() {
    const now = new Date();
    const parts = new Intl.DateTimeFormat('en-GB', { timeZone:'Europe/London', year:'numeric', month:'2-digit', day:'2-digit' }).formatToParts(now);
    const date = Object.fromEntries(parts.filter(p => p.type !== 'literal').map(p => [p.type, p.value]));
    const tomorrow = new Date(Date.UTC(Number(date.year), Number(date.month) - 1, Number(date.day) + 1, 0, 0, 0));
    const london = new Intl.DateTimeFormat('en-US', { timeZone:'Europe/London', timeZoneName:'longOffset', year:'numeric' }).formatToParts(tomorrow).find(p => p.type === 'timeZoneName')?.value || 'GMT';
    const offset = london.match(/GMT([+-])(\d{2}):(\d{2})/);
    const offsetMinutes = offset ? (offset[1] === '+' ? 1 : -1) * (Number(offset[2]) * 60 + Number(offset[3])) : 0;
    return new Date(tomorrow.getTime() - offsetMinutes * 60000);
  }

  function startDailyCountdown() {
    if (activePuzzleIndex !== 0) return;
    const existing = document.getElementById('dailyCountdown');
    if (existing) existing.remove();
    if (countdownTimer) clearInterval(countdownTimer);
    const el = document.createElement('div');
    el.id = 'dailyCountdown';
    el.className = 'countdown-card';
    document.querySelector('#screen-puzzle .card').appendChild(el);
    const tick = () => {
      const ms = Math.max(0, londonMidnightTarget() - new Date());
      const h = Math.floor(ms / 3600000), m = Math.floor(ms % 3600000 / 60000), s = Math.floor(ms % 60000 / 1000);
      el.innerHTML = `<b>Volgende daily puzzle</b><span>${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}</span><small>Nieuwe puzzel om 00:00 London time</small>`;
    };
    tick(); countdownTimer = setInterval(tick, 1000);
  }

  function showScreen(name) {
    document.getElementById('screen-home').classList.toggle('active', name === 'home');
    document.getElementById('screen-puzzle').classList.toggle('active', name === 'puzzle');
    document.getElementById('libraryScreen').classList.toggle('active', name === 'library');
    document.getElementById('premiumScreen').classList.toggle('active', name === 'premium');
    document.getElementById('raceScreen').classList.toggle('active', name === 'race');
    document.getElementById('breinkrakersScreen').classList.toggle('active', name === 'breinkrakers');
    document.getElementById('settingsScreen').classList.toggle('active', name === 'settings');
    document.getElementById('submitScreen').classList.toggle('active', name === 'submit');
    document.getElementById('calculator').classList.remove('open');
    window.scrollTo(0, 0);
  }

  let archiveMonth = { year: 2026, month: 8 };
  let heroSlideIndex = 0;
  let heroSlideTimer = null;
  function monthLabel(month) { return new Intl.DateTimeFormat(nettoNumberLocale(), { month:'long', year:'numeric' }).format(new Date(archiveMonth.year, month - 1, 1)); }
  function changeArchiveMonth(delta) {
    const next = new Date(archiveMonth.year, archiveMonth.month - 1 + delta, 1);
    const active = new Date(2026, 7, 1);
    if (next > active) return;
    archiveMonth = { year: next.getFullYear(), month: next.getMonth() + 1 };
    renderDailyArchive();
  }
  function setHeroSlide(index, resetTimer = true) {
    heroSlideIndex = (index + 3) % 3;
    document.querySelectorAll('.hero-slide').forEach((slide, i) => slide.classList.toggle('active', i === heroSlideIndex));
    document.querySelectorAll('.hero-dot').forEach((dot, i) => dot.classList.toggle('active', i === heroSlideIndex));
    if (resetTimer) startHeroSlideshow();
  }
  function changeHeroSlide(delta) { setHeroSlide(heroSlideIndex + delta); }
  function startHeroSlideshow() { clearTimeout(heroSlideTimer); heroSlideTimer = setTimeout(() => { setHeroSlide(heroSlideIndex + 1, false); startHeroSlideshow(); }, 10000); }
  const LIBRARY_DIFFICULTY_ORDER = ['easy', 'intermediate', 'hard', 'extremely-hard'];
  const LIBRARY_DIFFICULTY_OFFSET = { easy: 0, intermediate: 50, hard: 100, 'extremely-hard': 150 };
  const LIBRARY_DIFFICULTY_LABEL = {
    easy: 'Easy',
    intermediate: 'Intermediate',
    hard: 'Hard',
    'extremely-hard': 'Extremely Hard'
  };

  function libraryPuzzleNumber(difficulty, index) {
    return (LIBRARY_DIFFICULTY_OFFSET[difficulty] || 0) + index + 1;
  }

  function getSavedLibraryPlays() {
    try {
      return JSON.parse(localStorage.getItem('netto_library_plays') || '{}');
    } catch (_) {
      return {};
    }
  }

  function findNextIncompleteLibraryPuzzle(puzzles = libraryPuzzles, plays = getSavedLibraryPlays()) {
    for (const difficulty of LIBRARY_DIFFICULTY_ORDER) {
      const set = puzzles.filter(puzzle => puzzle.difficulty === difficulty);
      const index = set.findIndex(puzzle => !plays[puzzle.id] && !plays[`library_${puzzle.id}`]);
      if (index >= 0) {
        return { difficulty, index, number: libraryPuzzleNumber(difficulty, index), puzzle: set[index] };
      }
    }
    return null;
  }

  function updateContinuePuzzleButton() {
    const button = document.getElementById('btnContinuePuzzle');
    if (!button) return;
    const next = findNextIncompleteLibraryPuzzle();
    button.textContent = next
      ? `Speel puzzel ${next.number} →`
      : 'Alle puzzels voltooid ✓';
  }

  function startNextPuzzle() {
    dailyArchivePuzzleView = false;
    const next = findNextIncompleteLibraryPuzzle();
    if (!next) {
      selectedDifficulty = 'easy';
      openPuzzles();
      showNoticeToast('Je hebt alle Library-puzzels voltooid. Lekker gewerkt!', '🏆');
      return;
    }
    selectedDifficulty = next.difficulty;
    openPuzzles();
    playLibraryCard(next.puzzle.id);
  }

  let selectedDifficulty = 'easy';
  let libraryIndex = 0;
  let libraryPuzzles = (REBUILT_DATA.library || []).map((p, i) => ({ ...normalizeLibraryPuzzle(p), id: p.id || `local-${i + 1}`, difficulty: p.difficulty || getPuzzleDifficulty(p) }));
  let libraryMode = 'daily';
  let libraryActivePuzzle = null;
