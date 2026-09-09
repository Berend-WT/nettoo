// Run: node tools/test_frontend.cjs [project-root] [optional-staged-js-directory]
// Isolated clock/storage/DOM doubles: never writes player data or contacts Supabase.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = process.argv[2] || path.resolve(__dirname, '..');
const stage = process.argv[3];
let now = Date.parse('2026-09-05T12:00:00Z');
let sequence = 0;
const intervals = new Map(), frames = new Map(), storage = new Map(), nodes = new Map();
function element(id = '') {
  const classes = new Set();
  return { id, value: '', textContent: '', innerHTML: '', style: {}, dataset: {}, children: [],
    classList: { add: (...names) => names.forEach(n => classes.add(n)), remove: (...names) => names.forEach(n => classes.delete(n)), contains: n => classes.has(n), toggle(n, on) { on = on ?? !classes.has(n); on ? classes.add(n) : classes.delete(n); } },
    setAttribute() {}, removeAttribute() {}, addEventListener(type, fn) { this['on' + type] = fn; },
    appendChild(child) { this.children.push(child); }, remove() {}, focus() { context.document.activeElement = this; },
    querySelector() { return element(); }, querySelectorAll() { return []; }
  };
}
class ClockDate extends Date { constructor(...args) { super(...(args.length ? args : [now])); } static now() { return now; } }
const context = vm.createContext({ console, Date: ClockDate, Intl, Math, Set, Map, URLSearchParams,
  localStorage: { getItem: key => storage.get(key) ?? null, setItem: (key, value) => storage.set(key, String(value)), removeItem: key => storage.delete(key) },
  document: { activeElement: null, getElementById(id) { if (!nodes.has(id)) nodes.set(id, element(id)); return nodes.get(id); }, querySelector: () => element(), querySelectorAll: () => [], createElement: () => element(), addEventListener() {} },
  setInterval(fn) { const id = ++sequence; intervals.set(id, fn); return id; }, clearInterval: id => intervals.delete(id),
  requestAnimationFrame(fn) { const id = ++sequence; frames.set(id, fn); return id; }, cancelAnimationFrame: id => frames.delete(id),
  setTimeout() {}, clearTimeout() {}, addEventListener() {}, scrollTo() {},
  NettoI18n: { locale: () => 'en', t: text => text }
});
context.window = context;
for (const file of ['netto_frontend_puzzles.js', 'netto_breinkrakers.js', 'netto_race_pool.js']) {
  vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), context, { filename: file });
}
for (const file of ['core.js', 'puzzle-modes.js', 'race.js', 'submissions.js', 'library.js']) {
  const staged = stage && path.join(stage, file);
  const source = staged && fs.existsSync(staged) ? staged : path.join(root, 'js', file);
  vm.runInContext(fs.readFileSync(source, 'utf8'), context, { filename: file });
}
const run = code => vm.runInContext(code, context);
run('launchConfetti = () => {};'); // Visual effect is covered by browser smoke testing.
const get = id => context.document.getElementById(id);
let passed = 0;
function test(name, fn) { fn(); passed++; console.log('PASS ' + name); }
test('All classic modules load together, including window exports', () => assert.equal(typeof context.openBreinkrakers, 'function'));
test('Archive includes September and bounds month navigation', () => {
  assert.equal(run('archiveMonth.month'), 9);
  run('renderDailyArchive()');
  assert.equal(get('dailyPuzzleList').children.length, 4);
  run('changeArchiveMonth(1)'); assert.equal(run('archiveMonth.month'), 9);
  run('changeArchiveMonth(-1)'); assert.equal(run('archiveMonth.month'), 8);
  run('changeArchiveMonth(-1)'); assert.equal(run('archiveMonth.month'), 8);
});
test('An incomplete manual submission keeps the timer running', () => {
  run("libraryActivePuzzle = libraryPuzzles[0]; startPuzzleTimer('library','easy'); submitPuzzleView('library');");
  assert.equal(intervals.size, 1);
  assert.equal(storage.has('netto_library_plays'), false);
});
test('Library deadline catches up after a throttled tab and submits once', () => {
  now += 61000;
  [...intervals.values()].forEach(fn => fn());
  assert.equal(intervals.size, 0);
  assert.equal(Object.keys(JSON.parse(storage.get('netto_library_plays'))).length, 1);
  assert.match(get('libraryQuestionList').innerHTML, /Volgende puzzel/);
});
test('Leaving a timed puzzle cancels auto-submission', () => {
  run("startPuzzleTimer('library','easy'); showScreen('home');");
  assert.equal(intervals.size, 0);
});
test('Next unfinished puzzle uses holes and global numbering', () => {
  const puzzles = run('libraryPuzzles');
  const easy = puzzles.filter(p => p.difficulty === 'easy');
  const played = Object.fromEntries(easy.map(p => [p.id, {factor: 1}]));
  delete played[easy[10].id]; storage.set('netto_library_plays', JSON.stringify(played));
  assert.equal(run('findNextIncompleteLibraryPuzzle().number'), 11);
  played[easy[10].id] = {factor: 1}; storage.set('netto_library_plays', JSON.stringify(played));
  assert.equal(run('findNextIncompleteLibraryPuzzle().number'), 51);
});
test('Brain Teaser auto-calc respects Off and updates inverse answers', () => {
  run('bkActivePuzzle = BK_DATA[0];');
  [get('bkAnswer0'),get('bkAnswer1'),get('bkAnswer2'),get('bkAnswer3')].forEach(n => n.value = '');
  get('bkAnswer0').value='2'; get('bkAnswer1').value='2'; get('bkAnswer2').value='4';
  storage.set('netto_auto_calc','off'); run('bkTryAutoFill()'); assert.equal(get('bkAnswer3').value,'');
  storage.set('netto_auto_calc','on'); run('bkTryAutoFill()'); assert.equal(get('bkAnswer3').value,'8');
  get('bkAnswer0').value=''; get('bkAnswer3').value='8'; run("autoCalculatedInputs.clear(); bkTryAutoFill();");
  assert.equal(get('bkAnswer0').value,'2');
  get('bkAnswer3').value='10'; run('bkTryAutoFill()'); assert.equal(get('bkAnswer0').value,'3');
});
test('Brain Teaser completion is retained and chooses next missing puzzle', () => {
  run("bkState = { index:0, results:[] }; bkActivePuzzle=BK_DATA[0]; bkSubmitted=false;");
  ['2','2','4','8'].forEach((v,i)=>get('bkAnswer'+i).value=v);
  run('submitBreinkrakers()');
  const saved=JSON.parse(storage.get('netto_breinkrakers_progress'));
  assert.equal(saved.results[0].factor,1); assert.equal(saved.index,1);
});
test('Race progress is fractional for each duration and ends exactly once', () => {
  run('var finishes = 0; finishRace = () => { finishes++; stopRaceTimer(); raceState=null; };');
  for (const total of [180,300,600]) {
    run(`raceState={totalSeconds:${total},remaining:${total},timerId:null,endsAt:null}; startRaceTimer();`);
    now+=250;
    const fn=[...frames.values()][0]; frames.clear(); fn();
    assert.ok(Math.abs(run('raceState.progress') - .25/total)<1e-9);
    now+=total*1000;
    const end=[...frames.values()][0]; frames.clear(); end();
    assert.equal(frames.size,0);
  }
  assert.equal(run('finishes'),3);
});
test('Late race submission cannot score after deadline', () => {
  run('raceState={endsAt:Date.now()-1,timerId:null}; submitPuzzleRace();');
  assert.equal(run('finishes'),4);
});
test('Seeded duel queues match for both players', () => {
  const left=run("buildRaceQueue(12345,'standaard').map(p=>p.id).join(',')");
  assert.ok(left.length>0);
  assert.equal(left,run("buildRaceQueue(12345,'standaard').map(p=>p.id).join(',')"));
});
test('Daily statistics reject invalid dates and non-daily progress', () => {
  storage.set('netto_plays', JSON.stringify({
    '2026-09-03': {factor: 2}, '2026-09-04': {factor: 1},
    '2026-02-31': {factor: 1}, '2027-01-01': {factor: 1},
    library_1: {factor: 1, puzzleNumber: 1}, '2026-09-02': {factor: 0}
  }));
  storage.set('netto_streak', '999');
  assert.equal(run('getDailyStatsSnapshot().entries.length'), 2);
  assert.equal(run('getDailyStatsSnapshot().averageAccuracy'), 75);
  assert.equal(run('getDailyStatsSnapshot().currentStreak'), 2);
  assert.equal(run('getLocalStreak()'), 2);
  assert.equal(run('getDailyStatsSnapshot().buckets.join(",")'), '1,0,0,1,0');
});
test('Statistics empty state disables sharing and uses an em dash', () => {
  storage.set('netto_plays', '{}');
  run('renderStatsModal()');
  assert.equal(get('statsShareButton').disabled, true);
  assert.equal(get('statsEmpty').hidden, false);
  assert.equal(get('statsAccuracy').textContent, '—');
});
test('Streak tolerates today unfinished but breaks after a missed day', () => {
  assert.equal(run("statsTrailingStreak(['2026-09-02','2026-09-03'])"), 0);
  assert.equal(run("statsTrailingStreak(['2026-09-03','2026-09-04','2026-09-05'])"), 3);
  assert.equal(run("statsLongestStreak(['2026-08-30','2026-08-31','2026-09-01'])"), 3);
});
test('Mode statistics isolate puzzle, brain teaser and race scores', () => {
  const id = run('libraryPuzzles[0].id');
  storage.set('netto_library_plays', JSON.stringify({[id]: {factor:1}, unknown: {factor:2}}));
  storage.set('netto_breinkrakers_progress', JSON.stringify({results:[{factor:2,exact:false}]}));
  storage.set('netto_race_stats', JSON.stringify([{factor:1,exact:true},{factor:2,exact:false}]));
  run("statsMode='puzzles';renderStatsModal()");
  assert.equal(get('statsPlayed').textContent,'1');
  assert.equal(get('statsSpotOn').textContent,'1');
  run("statsMode='brain';renderStatsModal()");
  assert.equal(get('statsAccuracy').textContent,'50%');
  assert.equal(get('statsSpotOn').textContent,'0');
  run("statsMode='race';renderStatsModal()");
  assert.equal(get('statsPlayed').textContent,'2');
  assert.equal(get('statsSpotOnRate').textContent,'50%');
  assert.equal(get('statsCalendarButton').hidden,true);
  run("statsMode='daily'");
});
test('Daily review replaces inputs and can return to the questions', () => {
  run('showDailyResults()');
  assert.equal(get('dailyQuestionView').style.display,'none');
  assert.equal(get('results').classList.contains('show'),true);
  run('showDailyQuestions()');
  assert.equal(get('dailyQuestionView').style.display,'block');
  assert.equal(get('results').classList.contains('show'),false);
  run('resetDailyReviewView()');
  assert.equal(get('screen-puzzle').classList.contains('is-review'),false);
});
test('Ratio graph is symmetric, unit-independent and clips extreme estimates', () => {
  assert.equal(run('dailyRatioPoint(4,4).y'),142);
  assert.equal(run('dailyRatioPoint(2,4).y'),run('dailyRatioPoint(40000000,80000000).y'));
  assert.equal(run('dailyRatioPoint(2,1).y + dailyRatioPoint(1,2).y'),284);
  assert.equal(run('dailyRatioPoint(1000,1).clipped'),true);
  assert.equal(run('dailyRatioPoint(1,1000).y'),244);
  run('renderNumberLine(4,2,80000000,4,4,40000000)');
  assert.equal((get('numberlineCard').innerHTML.match(/class="ratio-chart histogram-chart"/g)||[]).length,1);
  assert.ok(!get('numberlineCard').innerHTML.includes('NaN'));
});
test('Histogram selection uses actual question data and explicit demo labels', () => {
  run('renderNumberLine(4,2,8,4,4,16); selectDailyReviewQuestion(1)');
  assert.ok(get('numberlineCard').innerHTML.includes('Sample data, not real players'));
  assert.ok(!get('numberlineCard').innerHTML.includes('Yellow line: you'));
  assert.ok(get('numberlineCard').innerHTML.includes('2× too low'));
  assert.equal(get('selectedReviewQuestion').textContent,run('PUZZLE_DATA.q2_label'));
  assert.equal((get('numberlineCard').innerHTML.match(/class="hist-bar"/g)||[]).length,12);
  run('renderNumberLine(999999,1,1,1,1,1)');
  assert.ok(get('numberlineCard').innerHTML.includes('outside the scale'));
});
test('Daily equation checks every operator and decimal rounding', () => {
  for (const expression of ['dailyEquationMatches(4,2,8,"×")','dailyEquationMatches(8,2,4,"÷")','dailyEquationMatches(0.1,0.2,0.3,"+")','dailyEquationMatches(8,2,6,"−")']) assert.equal(run(expression),true);
  assert.equal(run('dailyEquationMatches(4,2,9,"×")'),false);
  assert.equal(run('dailyEquationMatches(4,0,1,"÷")'),false);
});
test('An inconsistent daily submission never saves or opens results', () => {
  run("PUZZLE_DATA={...PUZZLE_DATA,operator:'×'};resetDailyReviewView()");
  get('g1').value='4';get('g2').value='2';get('g3').value='9';
  const before=storage.get('netto_plays');
  run('checkAnswers()');
  assert.equal(storage.get('netto_plays'),before);
  assert.equal(get('dailyEquationError').hidden,false);
  assert.equal(get('results').classList.contains('show'),false);
});
test('Review starts with an overview and switches to question detail', () => {
  run('renderNumberLine(4,2,8,4,4,16)');
  assert.equal(get('numberlineCard').classList.contains('is-overview'),true);
  assert.ok(get('numberlineCard').innerHTML.includes('overview-row is-exact'));
  run('selectDailyReviewQuestion(2)');
  assert.equal(get('numberlineCard').classList.contains('is-overview'),false);
});
test('Score reveal settles on real score and respects reduced motion', () => {
  frames.clear();
  run('revealDailyScore(72,true)');
  assert.equal(get('scoreBadge').textContent,'100%');
  now += 1000;
  const pending=[...frames.values()];frames.clear();pending.forEach(fn=>fn());
  assert.equal(get('scoreBadge').textContent,'72%');
  context.matchMedia=()=>({matches:true});
  run('revealDailyScore(45,true)');
  assert.equal(get('scoreBadge').textContent,'45%');
  assert.equal(frames.size,0);
});
test('Histogram uses round ticks while keeping the exact answer', () => {
  assert.equal(run('dailyHistogramTicks(9).includes(9)'),true);
  assert.equal(run('dailyHistogramTicks(9).includes(4.5)'),false);
  assert.equal(run('dailyHistogramTicks(9).every(Number.isInteger)'),true);
  assert.equal(run('dailyHistogramTicks(80000000).includes(80000000)'),true);
});
console.log(`${passed} frontend regression checks passed.`);
