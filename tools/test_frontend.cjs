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
for (const file of ['netto_frontend_puzzles.js', 'netto_breinkrakers.js', 'netto_race_sets.js', 'netto_race_pool.js']) {
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
console.log(`${passed} frontend regression checks passed.`);
