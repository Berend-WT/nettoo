// =========================================================================
  // REKENMACHINE
  // =========================================================================
  let calculatorExpression = '';
  function toggleCalculator(open) {
    document.getElementById('calculator').classList.toggle('open', open);
  }
  function formatCalculatorNumber(value) {
    if (!value || value === 'Fout') return value || '0';
    return value.replace(/\d+(?:\.\d+)?/g, (part) => {
      const [whole, decimal] = part.split('.');
      const formatted = Number(whole).toLocaleString('nl-NL');
      return decimal === undefined ? formatted : `${formatted},${decimal}`;
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
      document.getElementById('calculatorDisplay').value = 'Fout';
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

  // =========================================================================
  // 2. INITIALISATIE & LOCALSTORAGE SYNC
  // =========================================================================
  function initApp() {
    try {
      console.log("Netto: initApp gestart...");
      if (document.getElementById('q1-label')) {
        document.getElementById('q1-label').textContent = PUZZLE_DATA.q1_label;
        document.getElementById('q2-label').textContent = PUZZLE_DATA.q2_label;
        document.getElementById('q3-label').textContent = PUZZLE_DATA.q3_label;
        document.getElementById('operatorBadge').textContent = PUZZLE_DATA.operator || '×';
        document.getElementById('heroDateMeta').textContent = `Nr. 00${PUZZLE_DATA.number} · Dagelijkse Puzzel`;
        document.getElementById('puzzleEyebrow').textContent = `Netto · nr. 00${PUZZLE_DATA.number}`;
      }

      // Koppel knoppen expliciet via event listeners
      const btnStart = document.getElementById('btnStartPuzzle');
      if (btnStart) btnStart.onclick = () => showScreen('puzzle');

      const btnHamb = document.getElementById('hamburgerBtn');
      if (btnHamb) btnHamb.onclick = toggleMenu;

      const overlay = document.getElementById('overlay');
      if (overlay) overlay.onclick = toggleMenu;

      const btnCheck = document.getElementById('btnCheck');
      if (btnCheck) btnCheck.onclick = checkAnswers;

      const topUserBtn = document.getElementById('topbarUserBtn');
      if (topUserBtn) topUserBtn.onclick = openAuthModal;

      initInputs();
      loadUserProfile();
      if (supabaseClient) supabaseClient.auth.getSession().then(({ data }) => {
        if (data.session?.user) {
          currentUser = { id: data.session.user.id, email: data.session.user.email, username: data.session.user.user_metadata?.username || data.session.user.email.split('@')[0] };
          localStorage.setItem('netto_user', JSON.stringify(currentUser));
          updateUserUI();
        }
      });
      checkExistingPlay();
      startHeroSlideshow();
      console.log("Netto: initApp succesvol afgerond!");
    } catch(err) {
      console.error("Fout tijdens initApp:", err);
    }
  }

  // Zorg dat initApp ALTIJD draait (ook als DOM al geladen is)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
  } else {
    initApp();
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
    document.getElementById('topbarStreak').textContent = `🔥 ${streak}`;
    const pStreak = document.getElementById('profileStreak');
    if (pStreak) pStreak.textContent = `🔥 Huidige streak: ${streak} ${streak === 1 ? 'dag' : 'dagen'}`;
  }

  // =========================================================================
  // 3. LIVE DUIZENDTAL-FORMATTERING & SARCASTISCHE TOASTS
  // =========================================================================
  function formatDutchNumber(str) {
    // Alleen cijfers en eventueel één komma
    let clean = str.replace(/[^\d,]/g, '');
    let parts = clean.split(',');
    let whole = parts[0].replace(/^0+(?=\d)/, ''); // Remove leading zeros
    if (whole === '') whole = '0';
    
    // Voeg punten toe voor duizendtallen
    let formattedWhole = whole.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    return parts.length > 1 ? `${formattedWhole},${parts[1].slice(0, 2)}` : formattedWhole;
  }

  function parseFormattedNumber(str) {
    if (!str) return NaN;
    let clean = str.replace(/\./g, '').replace(',', '.');
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

  let autoCalculatedInputs = new Set();
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
    input.value = ''; input.placeholder = 'Your guess'; input.dataset.autoCalculated = 'false'; input.classList.remove('auto-calculated'); autoCalculatedInputs.delete(id);
  }
  function calculateDerivedValues(ids, operator) {
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
        input.placeholder = input.value.trim() ? '' : 'Your guess';
        input.classList.remove('auto-calculated');
        if (!input.value.trim()) input.placeholder = 'Your guess';
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
          input.placeholder = 'Your guess';
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
    return Number(n).toLocaleString('nl-NL');
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
      alert('Vul eerst alle drie de vragen in met een getal groter dan 0.');
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

    document.getElementById('a1').textContent = fmt(echt.a1);
    document.getElementById('a2').textContent = fmt(echt.a2);
    document.getElementById('a3').textContent = fmt(echt.a3);

    renderBadge('badge-q1', s1);
    renderBadge('badge-q2', s2);
    renderBadge('badge-q3', s3);

    document.getElementById('scoreBadge').textContent = avgFactor.toFixed(2) + '×';
    
    let msg = "🎯 Meesterlijk geschat!";
    if (avgFactor > 1.15) msg = "👏 Heel goed in de buurt!";
    if (avgFactor > 1.50) msg = "🧐 Redelijke inschatting!";
    if (avgFactor > 2.50) msg = "😅 Oef, rekenmachine nodig!";
    document.getElementById('scoreBadgeMsg').textContent = msg;

    if (currentUser) {
      document.getElementById('cloudSyncBanner').style.display = 'none';
    } else {
      document.getElementById('cloudSyncBanner').style.display = 'flex';
    }

    document.getElementById('results').classList.add('show');
    if (activePuzzleIndex === 0) startDailyCountdown();
    else { const countdown = document.getElementById('dailyCountdown'); if (countdown) countdown.remove(); if (countdownTimer) clearInterval(countdownTimer); }
    renderDailyArchive();
  }

  function renderBadge(elemId, factor) {
    const r = getFactorRating(factor);
    const el = document.getElementById(elemId);
    el.style.background = r.bg;
    el.style.color = r.color;
    el.innerHTML = `${r.emoji} ${factor.toFixed(2)}×`;
  }

  // =========================================================================
  // 5. WORDLE-STIJL SCORE DELEN
  // =========================================================================
  function shareScore() {
    const plays = getLocalPlays();
    const play = plays[TODAY_STR];
    if (!play) return;

    const echt = PUZZEL_ECHT();
    const r1 = getFactorRating(scoreVraag(play.g1, echt.a1));
    const r2 = getFactorRating(scoreVraag(play.g2, echt.a2));
    const r3 = getFactorRating(scoreVraag(play.g3, echt.a3));
    const streak = getLocalStreak();

    const text = `Netto #${PUZZLE_DATA.number} · Factor ${play.factor.toFixed(2)}× 🎯\n1️⃣ ${r1.emoji} ${scoreVraag(play.g1, echt.a1).toFixed(2)}×\n2️⃣ ${r2.emoji} ${scoreVraag(play.g2, echt.a2).toFixed(2)}×\n3️⃣ ${r3.emoji} ${scoreVraag(play.g3, echt.a3).toFixed(2)}×\n🔥 Streak: ${streak} ${streak === 1 ? 'dag' : 'dagen'}\nhttps://netto.game`;

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
    if (currentUser) {
      document.getElementById('topbarUsername').textContent = `👤 ${currentUser.username || currentUser.email.split('@')[0]}`;
      document.getElementById('sidebarAuthLabel').textContent = `Profiel (${currentUser.username || 'Speler'})`;
      document.getElementById('profileUsername').textContent = currentUser.username || currentUser.email;
      document.getElementById('profileEmailSubtitle').textContent = currentUser.email;
      document.getElementById('cloudSyncBanner').style.display = 'none';
    } else {
      document.getElementById('topbarUsername').textContent = 'Inloggen';
      document.getElementById('sidebarAuthLabel').textContent = 'Inloggen / Registreren';
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
      }      } else {
      console.log(`[Cloud Mock Sync] Score voor ${dateStr} gesynchroniseerd voor gebruiker ${currentUser.email}`);
    }
  }

  async function syncLibraryPlay(puzzle, g1, g2, g3, factor) {
    if (!currentUser || !supabaseClient || !puzzle?.id) return;
    const { error } = await supabaseClient.from('library_plays').upsert({ user_id: currentUser.id, puzzle_id: puzzle.id, g1, g2, g3, factor }, { onConflict: 'user_id,puzzle_id' });
    if (error) console.warn('Library score sync error:', error);
  }


  async function handleAuthSubmit(e) {
    e.preventDefault();
    const email = document.getElementById('authEmail').value.trim();
    const password = document.getElementById('authPassword').value;
    const username = document.getElementById('authUsername').value.trim() || email.split('@')[0];

    if (supabaseClient) {
      try {
        if (authMode === 'register') {
          const { data, error } = await supabaseClient.auth.signUp({
            email, password,
            options: { data: { username } }
          });
          if (error) throw error;
          currentUser = { id: data.user.id, email, username };
        } else {
          const { data, error } = await supabaseClient.auth.signInWithPassword({ email, password });
          if (error) throw error;
          currentUser = { id: data.user.id, email, username: data.user.user_metadata?.username || username };
        }
      } catch (err) {
        alert("Inloggen mislukt: " + err.message);
        return;
      }
    } else {
      // Offline / Test Fallback simulatie
      currentUser = {
        id: 'mock-user-' + Math.random().toString(36).substr(2, 9),
        email: email,
        username: username
      };
    }

    localStorage.setItem('netto_user', JSON.stringify(currentUser));
    updateUserUI();
    closeAuthModal();
    showSarcasticToast(`Welkom terug, ${currentUser.username}! Je scores zijn gesynchroniseerd.`, true);

    // Sync eventuele vandaag al gespeelde puzzel
    const plays = getLocalPlays();
    if (plays[TODAY_STR]) {
      const p = plays[TODAY_STR];
      syncPlayToCloud(TODAY_STR, p.g1, p.g2, p.g3, p.factor);
    }
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
    document.getElementById('calculator').classList.remove('open');
    window.scrollTo(0, 0);
  }

  let archiveMonth = { year: 2026, month: 8 };
  let heroSlideIndex = 0;
  let heroSlideTimer = null;
  function monthLabel(month) { return new Intl.DateTimeFormat('nl-NL', { month:'long', year:'numeric' }).format(new Date(archiveMonth.year, month - 1, 1)); }
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
  function startNextPuzzle() { selectPuzzle(Math.min(activePuzzleIndex + 1, DAILY_PUZZLES.length - 1)); }
  let selectedDifficulty = 'easy';
  let libraryIndex = 0;
  let libraryPuzzles = (REBUILT_DATA.library || []).map((p, i) => ({ ...normalizeLibraryPuzzle(p), id: p.id || `local-${i + 1}`, difficulty: p.difficulty || getPuzzleDifficulty(p) }));
  let libraryMode = 'daily';
  let libraryActivePuzzle = null;

  // ===== Puzzle countdown timer (Puzzels-tab én Library ✦) =====
  // Per-difficulty time budget (seconds). Harder puzzles get more thinking time.
  const LIBRARY_TIMER_SECONDS = {
    'easy': 60,
    'intermediate': 90,
    'hard': 120,
    'extremely-hard': 180,
  };
  const puzzleTimerIntervals = {};

  function stopPuzzleTimer(prefix) {
    if (puzzleTimerIntervals[prefix]) { clearInterval(puzzleTimerIntervals[prefix]); delete puzzleTimerIntervals[prefix]; }
  }
  function stopLibraryTimer() { stopPuzzleTimer('library'); }

  function startPuzzleTimer(prefix, difficulty) {
    stopPuzzleTimer(prefix);
    const el = document.getElementById(prefix + 'Timer');
    if (!el) return;
    const total = LIBRARY_TIMER_SECONDS[difficulty] ?? 120;
    let remaining = total;
    const render = () => {
      const m = Math.floor(remaining / 60);
      const s = remaining % 60;
      el.textContent = `⏱ ${m}:${s.toString().padStart(2, '0')}`;
      el.classList.toggle('warn', remaining <= 30 && remaining > 10);
      el.classList.toggle('crit', remaining <= 10);
    };
    render();
    puzzleTimerIntervals[prefix] = setInterval(() => {
      remaining -= 1;
      if (remaining <= 0) {
        stopPuzzleTimer(prefix);
        el.textContent = '⏱ 0:00';
        el.classList.add('crit');
        submitPuzzleView(prefix, true);
        return;
      }
      render();
    }, 1000);
  }

  // ===== Generieke puzzle-view (werkt voor 'library' én 'premium' prefix) =====
  function renderPuzzleView(prefix, p, progressLabel, moveAction) {
    const listEl = document.getElementById(prefix + 'QuestionList');
    if (!listEl || !p) return;
    document.getElementById(prefix + 'Progress').textContent = progressLabel;
    document.getElementById(prefix + 'Equation').style.display = 'none';
    const autoCalcNote = localStorage.getItem('netto_auto_calc_note_seen') === 'true' ? '' : `<div class="auto-calc-note" role="status" aria-live="polite">↳ Antwoorden worden automatisch berekend als de berekening klopt.</div>`;
    listEl.innerHTML = [[p.q1_label,p.q1_answer],[p.q2_label,p.q2_answer],[p.q3_label,p.q3_answer]].map((q,i) => `<div class="q-block"><div class="q-label">${q[0] || 'Vraag niet beschikbaar'}</div><div class="input-wrapper"><input type="text" class="library-answer-input daily-style-input" id="${prefix}Answer${i}" inputmode="numeric" placeholder="Your guess"></div></div>${i < 2 ? `<div class="connector"><div class="connector-line"></div><div class="connector-badge ${i === 1 ? 'eq' : ''}">${i === 0 ? (p.operator || '×') : '='}</div><div class="connector-line"></div></div>` : ''}`).join('') + autoCalcNote + `<button class="btn-check" onclick="submit${prefix === 'library' ? 'Library' : 'Premium'}Puzzle()">Check mijn score</button>`;
    if (autoCalcNote) localStorage.setItem('netto_auto_calc_note_seen', 'true');
    if (prefix === 'library') libraryActivePuzzle = p; else premiumActivePuzzle = p;
    bindDerivedInputs(prefix, p.operator || '×');
    startPuzzleTimer(prefix, p.difficulty);
  }

  function submitPuzzleView(prefix, auto = false) {
    const active = prefix === 'library' ? libraryActivePuzzle : premiumActivePuzzle;
    if (!active) return;
    stopPuzzleTimer(prefix);
    const guesses = [0,1,2].map(i => parseFormattedNumber(document.getElementById(`${prefix}Answer${i}`).value));
    if (guesses.some(v => !Number.isFinite(v) || v <= 0)) {
      if (auto) {
        // Timer expired with incomplete input: fill blanks with 1 so scoring
        // still runs (max deviation), and show feedback instead of blocking.
        for (let i = 0; i < 3; i++) {
          const inp = document.getElementById(`${prefix}Answer${i}`);
          if (inp && (!Number.isFinite(guesses[i]) || guesses[i] <= 0)) inp.value = '1';
        }
        guesses.forEach((v, i) => { if (!Number.isFinite(v) || v <= 0) guesses[i] = 1; });
      } else {
        alert('Vul alle drie de vragen in met een getal groter dan 0.');
        return;
      }
    }
    const answers = [active.q1_answer,active.q2_answer,active.q3_answer];
    const factor = answers.reduce((sum,a,i) => sum + scoreVraag(guesses[i],a),0) / 3;
    const plays = JSON.parse(localStorage.getItem('netto_library_plays') || '{}'); plays[active.id] = { factor, guesses, completedAt:new Date().toISOString() }; localStorage.setItem('netto_library_plays',JSON.stringify(plays));
    const nextAction = prefix === 'library' ? 'libraryMove(1)' : 'premiumPuzzleMove(1)';
    document.getElementById(prefix + 'QuestionList').innerHTML = answers.map((a,i) => `<div class="library-question"><b>Vraag ${i+1}</b>${[active.q1_label,active.q2_label,active.q3_label][i]}<br><strong>Echt antwoord: ${fmt(a)} · ${scoreVraag(guesses[i],a).toFixed(2)}×</strong></div>`).join('') + `<div class="score-badge-container"><div class="score-badge-title">Jouw gemiddelde afwijking</div><div class="score-badge-val" style="color:${scoreColor(factor)}">${factor.toFixed(2)}×</div></div><button class="btn-check" onclick="${nextAction}">Volgende puzzel →</button>`;
    syncLibraryPlay(active, guesses[0], guesses[1], guesses[2], factor);
    if (prefix === 'library') renderLibraryCards(); else renderPremiumPuzzles();
  }

  function openDailyPuzzles() {
    closeMenu(); openLibraryScreen('daily');
  }

  function openPuzzles() {
    closeMenu(); openLibraryScreen('library');
  }

  function openLibrary() {
    closeMenu(); openPremiumLibrary();
  }

  function isPremiumUnlocked() { return localStorage.getItem('netto_premium_unlocked') === 'true'; }

  // ===== LIBRARY ✦ (eigen pagina, premium) =====
  let premiumView = 'puzzles';            // 'puzzels' | 'vragen'
  let allPremiumPuzzles = [];             // library + daily puzzles met bron-label
  let premiumPuzzleList = [];             // actuele gefilterde lijst
  let premiumPuzzleIndex = 0;
  let premiumActivePuzzle = null;
  let allPremiumVragen = [];              // alle losse vragen

  function openPremiumLibrary() {
    closeMenu();
    buildPremiumData(); // altijd opnieuw: libraryPuzzles kan door Supabase-merge zijn bijgewerkt
    const unlocked = isPremiumUnlocked();
    document.getElementById('premiumLock').style.display = unlocked ? 'none' : 'block';
    document.getElementById('premiumContent').style.display = unlocked ? 'block' : 'none';
    document.getElementById('premiumPuzzleView').style.display = 'none';
    renderPremiumStats();
    populatePremiumFilters();
    setPremiumView(premiumView, null);
    showScreen('premium');
    document.getElementById('premiumScreen').classList.add('active');
  }

  function closePremiumScreen() {
    document.getElementById('premiumScreen').classList.remove('active');
    stopPuzzleTimer('premium');
    showScreen('home');
  }

  function unlockPremiumLibrary() {
    localStorage.setItem('netto_premium_unlocked', 'true');
    openPremiumLibrary();
  }

  function buildPremiumData() {
    // Alle puzzels: 100 library + alle daily's, elk met bron-label en stabiele id.
    allPremiumPuzzles = [
      ...libraryPuzzles.map(p => ({ ...p, source: 'Puzzels' })),
      ...DAILY_PUZZLES.map((p, i) => ({ ...p, source: 'Daily Archive', id: p.id || `daily-${p.date || p.number || i + 1}` })),
    ];
    // Alle losse vragen (3 per puzzel).
    allPremiumVragen = [];
    allPremiumPuzzles.forEach((p, pi) => {
      [p.q1_label, p.q2_label, p.q3_label].forEach((label, qi) => {
        allPremiumVragen.push({
          id: `${p.id}-q${qi + 1}`,
          label: label || 'Vraag niet beschikbaar',
          answer: [p.q1_answer, p.q2_answer, p.q3_answer][qi],
          category: (p.categories && p.categories[0]) || 'Algemeen',
          operator: p.operator || '×',
          source: p.source || 'Puzzels',
          puzzleName: p.name || `Puzzel ${pi + 1}`,
        });
      });
    });
  }

  function renderPremiumStats() {
    const plays = JSON.parse(localStorage.getItem('netto_library_plays') || '{}');
    const played = allPremiumPuzzles.filter(p => plays[p.id]).length;
    document.getElementById('premiumStats').innerHTML = `<div class="library-stat"><b>${allPremiumPuzzles.length}</b><span>Puzzels</span></div><div class="library-stat"><b>${allPremiumVragen.length}</b><span>Vragen</span></div><div class="library-stat"><b>${played}</b><span>Gespeeld door jou</span></div>`;
  }

  function populatePremiumFilters() {
    const catSelect = document.getElementById('premiumCategory');
    const vragenSelect = document.getElementById('vragenCategory');
    if (!catSelect || !vragenSelect) return;
    const categories = [...new Set(allPremiumPuzzles.flatMap(p => p.categories || []))].sort((a,b) => a.localeCompare(b));
    const options = '<option value="">Alle categorieën</option>' + categories.map(c => `<option value="${c.replace(/"/g, '&quot;')}">${c}</option>`).join('');
    catSelect.innerHTML = options;
    vragenSelect.innerHTML = options;
  }

  function setPremiumView(view, button) {
    premiumView = view;
    document.querySelectorAll('#premiumViewToggle button').forEach((b, i) => b.classList.toggle('active', (['puzzles','vragen'][i]) === view));
    document.getElementById('premiumPuzzlesView').style.display = view === 'puzzles' ? 'block' : 'none';
    document.getElementById('premiumVragenView').style.display = view === 'vragen' ? 'block' : 'none';
    document.getElementById('premiumPuzzleView').style.display = 'none';
    if (view === 'puzzles') renderPremiumPuzzles(); else renderPremiumVragen();
  }

  function renderPremiumPuzzles() {
    const search = (document.getElementById('premiumSearch')?.value || '').trim().toLowerCase();
    const operator = document.getElementById('premiumOperator')?.value || '';
    const difficulty = document.getElementById('premiumDifficulty')?.value || '';
    const category = document.getElementById('premiumCategory')?.value || '';
    premiumPuzzleList = allPremiumPuzzles.filter(p => (!operator || p.operator === operator) && (!difficulty || p.difficulty === difficulty) && (!category || (p.categories || []).includes(category)) && (!search || [p.name,p.q1_label,p.q2_label,p.q3_label].join(' ').toLowerCase().includes(search)));
    document.getElementById('premiumPuzzleCount').textContent = `${premiumPuzzleList.length} puzzel${premiumPuzzleList.length === 1 ? '' : 's'} gevonden`;
    const plays = JSON.parse(localStorage.getItem('netto_library_plays') || '{}');
    document.getElementById('premiumPuzzleGrid').innerHTML = premiumPuzzleList.map((p, i) => {
      const play = plays[p.id];
      const color = play ? scoreColor(play.factor) : '';
      const label = play ? `Score ${play.factor.toFixed(2)}×` : 'Open puzzle →';
      return `<article class="library-flip-card" role="button" tabindex="0" onclick="playPremiumPuzzle('${p.id}')" onkeydown="if(event.key==='Enter'||event.key===' ') { event.preventDefault(); playPremiumPuzzle('${p.id}'); }"><div class="library-flip-card-inner"><div class="library-flip-front ${play ? 'played' : ''}" style="${play ? `background:${color};` : ''}"><strong>#${i + 1}</strong><span>${label}</span><span class="premium-source-badge">${p.source || 'Puzzels'}</span></div></div></article>`;
    }).join('') || '<div class="premium-lock">Geen puzzels gevonden.</div>';
  }

  function renderPremiumVragen() {
    const search = (document.getElementById('vragenSearch')?.value || '').trim().toLowerCase();
    const category = document.getElementById('vragenCategory')?.value || '';
    const vragen = allPremiumVragen.filter(v => (!category || v.category === category) && (!search || (v.label + ' ' + v.puzzleName).toLowerCase().includes(search)));
    document.getElementById('vragenCount').textContent = `${vragen.length} vraag${vragen.length === 1 ? '' : 'en'} gevonden · klik op een kaart voor het antwoord`;
    document.getElementById('vragenGrid').innerHTML = vragen.map((v, i) => `<article class="library-flip-card" role="button" tabindex="0" data-vraag="${i}" onclick="toggleVraagCard(this)" onkeydown="if(event.key==='Enter'||event.key===' ') { event.preventDefault(); toggleVraagCard(this); }"><div class="library-flip-card-inner"><div class="vraag-flip-front"><div class="vraag-tekst">${v.label}</div><div class="vraag-meta"><span class="vraag-categorie">${v.category}</span><span>${v.operator}</span></div></div><div class="vraag-flip-back"><div><div class="vraag-bron">${v.puzzleName} · ${v.source}</div><div class="vraag-tekst" style="color:#fff;">${v.label}</div></div><div class="vraag-antwoord">${fmt(v.answer)}</div></div></div></article>`).join('');
  }

  function toggleVraagCard(cardEl) { cardEl.classList.toggle('revealed'); }

  function playPremiumPuzzle(id) {
    const index = premiumPuzzleList.findIndex(p => p.id === id);
    if (index < 0) return;
    premiumPuzzleIndex = index;
    document.getElementById('premiumPuzzlesView').style.display = 'none';
    document.getElementById('premiumVragenView').style.display = 'none';
    document.getElementById('premiumPuzzleView').style.display = 'block';
    renderPremiumPuzzleView();
  }

  function premiumPuzzleMove(direction) {
    const next = Math.max(0, Math.min(premiumPuzzleList.length - 1, premiumPuzzleIndex + direction));
    premiumPuzzleIndex = next;
    renderPremiumPuzzleView();
  }

  function openLibraryScreen(mode) {
    libraryMode = mode;
    document.getElementById('libraryFilters').style.display = 'flex';
    document.getElementById('libraryStats').style.display = 'grid';
    document.getElementById('dailyDateControls').style.display = mode === 'daily' ? 'flex' : 'none';
    document.getElementById('aboutPanel').style.display = 'none';
    showScreen('library');
    document.getElementById('libraryScreen').classList.add('active');
    document.getElementById('libraryDifficulties').style.display = mode === 'library' ? 'grid' : 'none';
    document.getElementById('libraryCardGrid').style.display = mode === 'library' ? 'grid' : 'none';
    document.getElementById('libraryDifficulties').querySelectorAll('button').forEach((button, index) => { const level = ['easy','intermediate','hard','extremely-hard'][index]; const count = libraryPuzzles.filter(p => p.difficulty === level).length; const locked = level !== 'easy' && !hasCompletedDifficulty(level === 'intermediate' ? 'easy' : level === 'hard' ? 'intermediate' : 'hard'); button.innerHTML = `${level === 'extremely-hard' ? 'Extremely Hard' : level[0].toUpperCase() + level.slice(1)} ${locked ? '🔒' : ''}<span>${locked ? 'Locked' : `${count} puzzels`}</span>`; button.disabled = locked; button.classList.toggle('active', level === selectedDifficulty); });
    document.getElementById('libraryPuzzleView').style.display = 'none';
    document.getElementById('dailyPuzzleList').style.display = mode === 'daily' ? 'block' : 'none';      document.getElementById('libraryTitle').textContent = mode === 'daily' ? 'Daily Archive' : 'Puzzels';
    document.getElementById('aboutPanel').style.display = 'none';
    document.getElementById('librarySubtitle').textContent = mode === 'daily' ? 'Elke puzzel sinds dag één. Speel ze opnieuw.' : 'Kies een difficulty en speel alle puzzels.';
    document.querySelectorAll('#libraryFilters button').forEach((b,i) => b.classList.toggle('active', mode === ['daily','library'][i]));
    renderLibraryStats();
    if (mode === 'daily') renderDailyArchive();
    else { renderLibraryCards(); loadLibraryFromSupabase(); }
  }

  function selectLibraryView(mode, button) { openLibraryScreen(mode); }
  function openAbout() { closeMenu(); showScreen('library'); document.getElementById('libraryScreen').classList.add('active'); document.getElementById('libraryTitle').textContent='About Us'; document.getElementById('librarySubtitle').textContent='Waarom we Netto bouwen.'; document.getElementById('libraryFilters').style.display='none'; document.getElementById('libraryDifficulties').style.display='none'; document.getElementById('dailyPuzzleList').style.display='none'; document.getElementById('libraryPuzzleView').style.display='none'; document.getElementById('libraryStats').style.display='none'; document.getElementById('aboutPanel').style.display='block'; }
  function closeLibraryScreen() { document.getElementById('libraryScreen').classList.remove('active'); stopLibraryTimer(); showScreen('home'); }
  function closeLibrary() { closeLibraryScreen(); }


  function renderLibraryStats() {
    const plays = getLocalPlays();
    const completed = Object.keys(plays).length;
    document.getElementById('libraryStats').innerHTML = `<div class="library-stat"><b>${completed}</b><span>Puzzels gespeeld</span></div><div class="library-stat"><b>${DAILY_PUZZLES.length}</b><span>Daily puzzels</span></div><div class="library-stat"><b>${libraryPuzzles.length}</b><span>Library puzzels</span></div>`;
  }

  function getLibrarySet(level) { return libraryPuzzles.filter(p => p.difficulty === level).slice(0,25); }
  function selectLibraryDifficulty(level, button) {
    selectedDifficulty = level;
    document.querySelectorAll('#libraryDifficulties button').forEach(b => b.classList.remove('active'));
    if (button) button.classList.add('active');
    renderLibraryCards();
  }
  function libraryPlayFor(p) { try { return JSON.parse(localStorage.getItem('netto_library_plays') || '{}')[p.id]; } catch (_) { return null; } }
  function libraryProgressIndex(set) {
    const plays = JSON.parse(localStorage.getItem('netto_library_plays') || '{}');
    let index = 0;
    while (index < set.length && plays[set[index].id]) index += 1;
    return index;
  }
  function renderLibraryCards() {
    const grid = document.getElementById('libraryCardGrid');
    const source = getLibrarySet(selectedDifficulty);
    const nextIndex = libraryProgressIndex(source);
    grid.innerHTML = source.map((p, i) => {
      const play = libraryPlayFor(p);
      const isCompleted = Boolean(play);
      const isNext = !isCompleted && i === nextIndex;
      const canOpen = isCompleted || isNext;
      const color = play ? scoreColor(play.factor) : '';
      const frontStyle = play ? `background:${color};` : '';
      const label = play ? `Score ${play.factor.toFixed(2)}×` : (isNext ? 'Open puzzle →' : '');
      return `<article class="library-flip-card ${canOpen ? 'is-open' : 'is-locked'}" role="button" tabindex="${canOpen ? '0' : '-1'}" aria-label="${canOpen ? `Open puzzel ${i + 1}` : `Puzzel ${i + 1} vergrendeld`}" ${canOpen ? `onclick="playLibraryCard('${p.id}')" onkeydown="if(event.key==='Enter'||event.key===' ') { event.preventDefault(); playLibraryCard('${p.id}'); }"` : ''}><div class="library-flip-card-inner"><div class="library-flip-front ${play ? 'played' : ''}" style="${frontStyle}"><strong>#${i + 1}</strong><span>${label}</span></div></div></article>`;
    }).join('');
  }
  function playLibraryCard(id) {
    const set = getLibrarySet(selectedDifficulty); const index = set.findIndex(p => p.id === id);
    if (index < 0) return; libraryIndex = index; document.getElementById('libraryCardGrid').style.display = 'none'; document.getElementById('libraryDifficulties').style.display = 'none'; document.getElementById('libraryPuzzleView').style.display = 'block'; renderLibraryPuzzle();
  }

  function showLibraryAnswers(index) {
    const p = libraryPuzzles[index]; if (!p) return;
    alert(`${p.q1_label}\nAntwoord: ${fmt(p.q1_answer)}\n\n${p.q2_label}\nAntwoord: ${fmt(p.q2_answer)}\n\n${p.q3_label}\nAntwoord: ${fmt(p.q3_answer)}`);
  }

  function renderDailyArchive() {
    const list = document.getElementById('dailyPuzzleList');
    const plays = getLocalPlays(); list.innerHTML = '';
    const selectedMonth = archiveMonth.month;
    const selectedYear = archiveMonth.year;
    const monthDays = new Date(selectedYear, selectedMonth, 0).getDate();
    const monthNav = document.getElementById('activeArchiveMonth');
    if (monthNav) monthNav.textContent = monthLabel(selectedMonth);
    const nextButton = document.getElementById('nextMonthBtn');
    if (nextButton) nextButton.disabled = selectedYear === 2026 && selectedMonth === 8;
    const previousButton = document.getElementById('previousMonthBtn');
    if (previousButton) previousButton.disabled = selectedYear <= 2026 && selectedMonth <= 8 && selectedYear === 2026;
    const activeDate = new Date(2026, 7, 28);
    const monthKey = `${selectedYear}-${String(selectedMonth).padStart(2,'0')}`;
    const activeMonthKey = `${activeDate.getFullYear()}-${String(activeDate.getMonth() + 1).padStart(2,'0')}`;
    const availableDays = monthKey === activeMonthKey ? activeDate.getDate() : (new Date(selectedYear, selectedMonth - 1, 1) < new Date(activeDate.getFullYear(), activeDate.getMonth(), 1) ? monthDays : 0);
    const monthPuzzles = DAILY_PUZZLES.filter(p => {
      const date = p.date || `${selectedYear}-${String(selectedMonth).padStart(2,'0')}-${String(DAILY_PUZZLES.indexOf(p) + 1).padStart(2,'0')}`;
      return date.startsWith(monthKey) && Number(date.slice(-2)) <= availableDays;
    }).sort((a,b) => String(b.date || '').localeCompare(String(a.date || '')));
    monthPuzzles.forEach((p, idx) => {
      const puzzleDate = p.date ? new Date(`${p.date}T00:00:00`) : new Date(selectedYear, selectedMonth - 1, Math.min(idx + 1, monthDays));
      const play = plays[p.date || `puzzle_${p.number || idx + 1}`];
      const row = document.createElement('div'); row.className = 'daily-archive-row';
      const dateLabel = new Intl.DateTimeFormat('nl-NL', { day:'numeric', month:'long' }).format(puzzleDate);
      row.innerHTML = `<span class="archive-number">${String(p.number || idx + 1).padStart(3,'0')}</span><div><div class="archive-name">${p.name || `Daily Puzzle #${p.number || idx + 1}`}</div><div class="archive-date">${dateLabel}</div></div><span class="archive-score" style="color:${play ? scoreColor(play.factor) : '#92959D'}">${play ? play.factor.toFixed(2)+'×' : '—'}</span><span class="archive-status ${play ? 'complete' : ''}">${play ? 'COMPLETE ✓' : 'PLAY →'}</span>`;
      row.onclick = () => { activePuzzleIndex = DAILY_PUZZLES.indexOf(p); PUZZLE_DATA = p; loadActivePuzzle(); closeLibraryScreen(); showScreen('puzzle'); };
      list.appendChild(row);
    });
  }

  // Dynamische scorekleur: vloeiende gradient groen (1.00) -> geel (~1.5) -> rood (2.0+).
  function scoreColor(factor) {
    const f = Math.max(1, Number(factor) || 1);
    const H_GREEN = 145, H_YELLOW = 48, H_RED = 0;
    let h;
    if (f <= 1) h = H_GREEN;
    else if (f <= 1.5) h = H_GREEN + (H_YELLOW - H_GREEN) * ((f - 1) / 0.5);
    else if (f <= 2) h = H_YELLOW + (H_RED - H_YELLOW) * ((f - 1.5) / 0.5);
    else h = H_RED;
    return `hsl(${Math.round(h)}, 74%, 45%)`;
  }

  function getPuzzleDifficulty(p) {
    const max = Math.max(Number(p.a1), Number(p.a2), Number(p.a3));
    if (max <= 100 && ['+','−'].includes(p.operator)) return 'easy';
    if (max <= 1000 && ['+','−','×'].includes(p.operator)) return 'intermediate';
    if (max <= 100000) return 'hard';
    return 'extremely-hard';
  }

  async function loadLibraryFromSupabase() {
    const localPuzzles = [...(REBUILT_DATA.library || []), ...(REBUILT_DATA.reserve || [])].map((p, i) => ({ ...normalizeLibraryPuzzle(p), id: p.id || `local-${i + 1}`, difficulty: p.difficulty || getPuzzleDifficulty(p) }));
    const uniquePuzzles = new Map(localPuzzles.map(p => [p.id, p]));
    libraryPuzzles = [...uniquePuzzles.values()];
    renderLibraryCards();
    renderDifficultyCounts(Object.fromEntries(['easy','intermediate','hard','extremely-hard'].map(d => [d, libraryPuzzles.filter(p => p.difficulty === d).length])));
    if (!supabaseClient) return;
    const { data, error } = await supabaseClient.from('library_puzzles').select('*').order('puzzle_number');
    if (!error && data?.length) {
      const merged = new Map(libraryPuzzles.map(p => [p.id, p]));
      data.map(normalizeLibraryPuzzle).forEach(p => merged.set(p.id || `remote-${merged.size + 1}`, p));
      libraryPuzzles = [...merged.values()];
      renderDifficultyCounts(Object.fromEntries(['easy','intermediate','hard','extremely-hard'].map(d => [d, libraryPuzzles.filter(p => p.difficulty === d).length])));
    } else if (error) {
      console.warn('Supabase library fallback naar lokale JSON:', error);
    }
  }

  function renderDifficultyCounts(counts) {
    document.querySelectorAll('#libraryDifficulties button').forEach(button => { const match = button.getAttribute('onclick').match(/'([^']+)'/); if (match) button.querySelector('span').textContent = `${counts[match[1]] || 0} puzzels`; });
  }

  function hasCompletedDifficulty(level) { const set = libraryPuzzles.filter(p => p.difficulty === level); const plays = JSON.parse(localStorage.getItem('netto_library_plays') || '{}'); return set.length > 0 && set.every(p => plays[p.id]); }

  function hasLibraryProgress(level, index) {
    if (index === 0) return true;
    const set = libraryPuzzles.filter(p => p.difficulty === level);
    const plays = JSON.parse(localStorage.getItem('netto_library_plays') || '{}');
    return Boolean(set[index - 1] && plays[set[index - 1].id]);
  }

  function selectDifficulty(level) {
    if (!currentUser) { openAuthModal(); return; }
    if (level !== 'easy' && !hasCompletedDifficulty(level === 'intermediate' ? 'easy' : level === 'hard' ? 'intermediate' : 'hard')) { showSarcasticToast('🔒 Speel eerst het vorige difficulty-level uit.'); return; }
    selectedDifficulty = level; libraryIndex = 0;
    const set = libraryPuzzles.filter(p => p.difficulty === level);
    if (!set.length) { showSarcasticToast('Deze difficulty bevat nog geen geladen puzzels.'); return; }
    document.getElementById('libraryDifficulties').style.display = 'none'; document.getElementById('dailyPuzzleList').style.display = 'none'; document.getElementById('libraryCardGrid').style.display = 'none'; document.getElementById('libraryPuzzleView').style.display = 'block'; renderLibraryPuzzle();
  }

  function renderLibraryPuzzle() {
    const p = libraryPuzzles.filter(x => x.difficulty === selectedDifficulty)[libraryIndex]; if (!p) return;
    if (!hasLibraryProgress(selectedDifficulty, libraryIndex)) { showSarcasticToast('🔒 Rond eerst de vorige puzzel af.'); return; }
    renderPuzzleView('library', p, `${selectedDifficulty.replace('-', ' ')} · puzzel ${libraryIndex + 1}`);
  }

  function renderPremiumPuzzleView() {
    const p = premiumPuzzleList[premiumPuzzleIndex]; if (!p) return;
    premiumActivePuzzle = p;
    renderPuzzleView('premium', p, `Library ✦ · ${p.source === 'Daily Archive' ? 'daily' : 'puzzel'} ${premiumPuzzleIndex + 1}`);
  }

  function submitLibraryPuzzle(auto = false) { submitPuzzleView('library', auto); }
  function submitPremiumPuzzle(auto = false) { submitPuzzleView('premium', auto); }

  function jumpToLibraryPuzzle(index) { libraryIndex = index; renderLibraryPuzzle(); }

  function renderLibraryProgressBlocks() {
    const set = libraryPuzzles.filter(p => p.difficulty === selectedDifficulty).slice(0,25);
    const plays = JSON.parse(localStorage.getItem('netto_library_plays') || '{}');
  }

  function libraryMove(direction) {    const set = libraryPuzzles.filter(p => p.difficulty === selectedDifficulty); const next = Math.max(0, Math.min(set.length - 1, libraryIndex + direction)); if (!hasLibraryProgress(selectedDifficulty, next)) { showSarcasticToast('🔒 Rond eerst de vorige puzzel af.'); return; } libraryIndex = next; renderLibraryPuzzle(); }

  function openArchiveModal() { openDailyPuzzles(); }
  function closeArchiveModal() { closeLibrary(); }

  function renderArchiveList() {
    const list = document.getElementById('archiveList');
    list.innerHTML = '';

    const plays = getLocalPlays();

    PUZZLE_ARCHIVE.forEach((p, idx) => {
      const pKey = `puzzle_${p.number || activePuzzleIndex + 1}`;
      const play = plays[pKey] || (idx === 0 ? plays[TODAY_STR] : null);
      
      const div = document.createElement('div');
      div.className = `lb-row ${idx === activePuzzleIndex ? 'me' : ''}`;
      div.style.cursor = 'pointer';
      div.onclick = () => selectPuzzle(idx);

      let statusBadge = `<span style="color:#6B7280; font-size:12px;">Nog niet gespeeld →</span>`;
      if (play) {
        statusBadge = `<span style="color:var(--green); font-weight:700; font-size:12px;">✅ Factor ${play.factor.toFixed(2)}×</span>`;
      }

      div.innerHTML = `
        <div class="lb-left">
          <span class="lb-rank">#${p.number.toString().padStart(2, '0')}</span>
          <div>
            <div class="lb-name">${p.name || `Puzzel #${p.number}`}</div>
            <div style="font-size:11px; color:#4C519C;">${p.operator === '×' ? 'Vermenigvuldiging (×)' : 'Optelling (+)'}</div>
          </div>
        </div>
        ${statusBadge}
      `;
      list.appendChild(div);
    });
  }

  function selectPuzzle(index) {
    activePuzzleIndex = index;
    PUZZLE_DATA = DAILY_PUZZLES[index] || PUZZLE_ARCHIVE[index];
    closeArchiveModal();
    loadActivePuzzle();
    showScreen('puzzle');
  }

  function loadActivePuzzle() {
    document.getElementById('q1-label').textContent = PUZZLE_DATA.q1_label;
    document.getElementById('q2-label').textContent = PUZZLE_DATA.q2_label;
    document.getElementById('q3-label').textContent = PUZZLE_DATA.q3_label;
    document.getElementById('operatorBadge').textContent = PUZZLE_DATA.operator || '×';
    document.getElementById('heroDateMeta').textContent = `Daily · ${PUZZLE_DATA.name || `Puzzel #${activePuzzleIndex + 1}`}`;
    document.getElementById('puzzleEyebrow').textContent = `Netto · nr. 00${PUZZLE_DATA.number}`;

    // Reset velden en uitslag
    ['g1', 'g2', 'g3'].forEach(id => {
      const input = document.getElementById(id);
      input.value = '';
      input.placeholder = 'Your guess';
      input.dataset.autoCalculated = 'false';
      input.classList.remove('auto-calculated');
      input.disabled = false;
    });
    autoCalculatedInputs.clear();
    document.getElementById('results').classList.remove('show');
    document.getElementById('alreadyPlayedBanner').classList.remove('show');
    document.getElementById('btnCheck').style.display = 'block';

    checkExistingPlay();
  }

  function goHome() {
    showScreen('home');
    closeMenu();
  }

  function openLeaderboardModal() {
    closeMenu();
    renderLeaderboard();
    document.getElementById('modalLeaderboard').classList.add('active');
  }

  function closeLeaderboardModal() {
    document.getElementById('modalLeaderboard').classList.remove('active');
  }

  function openAuthModal() {
    closeMenu();
    if (currentUser) {
      document.getElementById('authLoggedInView').style.display = 'block';
      document.getElementById('authFormView').style.display = 'none';
    } else {
      document.getElementById('authLoggedInView').style.display = 'none';
      document.getElementById('authFormView').style.display = 'block';
    }
    document.getElementById('modalAuth').classList.add('active');
  }

  function closeAuthModal() {
    document.getElementById('modalAuth').classList.remove('active');
  }

  function closeModalOnBg(e, modalId) {
    if (e.target.id === modalId) {
      document.getElementById(modalId).classList.remove('active');
    }
  }

  // Expliciet binden aan window zodat inline onclick ALTIJD werkt
  window.toggleMenu = toggleMenu;
  window.closeMenu = closeMenu;
  window.showScreen = showScreen;
  window.goHome = goHome;
  window.openArchiveModal = openArchiveModal;
  window.closeArchiveModal = closeArchiveModal;
  window.selectPuzzle = selectPuzzle;
  window.openLeaderboardModal = openLeaderboardModal;
  window.closeLeaderboardModal = closeLeaderboardModal;
  window.openAuthModal = openAuthModal;
  window.closeAuthModal = closeAuthModal;
  window.closeModalOnBg = closeModalOnBg;
  window.checkAnswers = checkAnswers;
  window.shareScore = shareScore;
  window.toggleAuthMode = toggleAuthMode;
  window.handleAuthSubmit = handleAuthSubmit;
  window.handleLogout = handleLogout;
  window.switchLbTab = switchLbTab;
  window.changeArchiveMonth = changeArchiveMonth;
  window.changeHeroSlide = changeHeroSlide;
  window.setHeroSlide = setHeroSlide;
  window.startNextPuzzle = startNextPuzzle;
  window.openDailyPuzzles = openDailyPuzzles;
  window.openPuzzles = openPuzzles;
  window.openPremiumLibrary = openPremiumLibrary;
  window.closePremiumScreen = closePremiumScreen;
  window.setPremiumView = setPremiumView;
  window.renderPremiumPuzzles = renderPremiumPuzzles;
  window.renderPremiumVragen = renderPremiumVragen;
  window.playPremiumPuzzle = playPremiumPuzzle;
  window.premiumPuzzleMove = premiumPuzzleMove;
  window.submitPremiumPuzzle = submitPremiumPuzzle;
  window.toggleVraagCard = toggleVraagCard;
  window.unlockPremiumLibrary = unlockPremiumLibrary;
  window.selectLibraryView = selectLibraryView;    window.selectDifficulty = selectDifficulty;
  window.selectLibraryDifficulty = selectLibraryDifficulty;
  window.playLibraryCard = playLibraryCard;
  window.jumpToLibraryPuzzle = jumpToLibraryPuzzle;
  window.libraryMove = libraryMove;
  window.submitLibraryPuzzle = submitLibraryPuzzle;
  window.unlockPremiumLibrary = unlockPremiumLibrary;
  window.showLibraryAnswers = showLibraryAnswers;
  window.changeArchiveMonth = changeArchiveMonth;
