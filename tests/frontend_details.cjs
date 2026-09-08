// Draaien: node tests/frontend_details.cjs
// Geïsoleerde controles zonder browseropslag of netwerkverzoeken.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const core = fs.readFileSync(path.join(root, 'js/core.js'), 'utf8');
const race = fs.readFileSync(path.join(root, 'js/race.js'), 'utf8');
const opslag = new Map();
const velden = new Map();
function veld(id) {
  if (!velden.has(id)) velden.set(id, {value:'',textContent:'',attributen:{},style:{setProperty(){}},setAttribute(k,v){this.attributen[k]=v;},querySelector(){return veld(id+'Range');},querySelectorAll(){return [];}});
  return velden.get(id);
}
const context = vm.createContext({Intl, Date,
  localStorage:{getItem:k=>opslag.get(k)??null,setItem:(k,v)=>opslag.set(k,v)},
  document:{getElementById:veld}
});
vm.runInContext(core.slice(core.indexOf('  const VRAAG_EENHEDEN'),core.indexOf('  function categorieKleurVariabele')),context);
vm.runInContext(core.slice(core.indexOf('  function nettoDagSleutel'),core.indexOf('  // Geen const:')),context);
vm.runInContext(race.slice(race.indexOf('  const RACE_TOTAL_SECONDS'),race.indexOf('  let raceQueue')),context);
vm.runInContext(race.slice(race.indexOf('  function getRaceModeConfig'),race.indexOf('  function raceDurationMeta')),context);
vm.runInContext(race.slice(race.indexOf('  function renderRaceTolerantieOptions'),race.indexOf('  function renderRaceModeControls')),context);
for (const [vraag, verwacht] of [
  ['Hoeveel duizend inwoners heeft Rotterdam?', '× 1.000'],
  ['Hoeveel miljoen inwoners heeft Mexico?', '× 1.000.000'],
  ['Hoeveel miljard mensen zijn er?', '× 1.000.000.000'],
  ['Hoeveel miljard kilometer legt licht af?', 'miljard km'],
  ['Hoeveel poten heeft een krab?', null],
  ['Hoeveel bezoekers komen er per jaar?', null],
  ['Wat is de afstand in km?', 'km'],
  ['Wat is de snelheid in km/u?', 'km/u'],
  ['Wat is de oppervlakte in km²?', 'km²'],
  ['Hoeveel dagen zitten er in een week?', 'dagen'],
  ['Hoeveel gram weegt dit?', 'g'],
  ['Welk percentage is water?', '%']
]) assert.equal(context.eenheidUit(vraag), verwacht, vraag);
console.log('Eenheden, afkortingen en schaalwoorden kloppen.');
const sleutels=['perfect','scherp','netjes','ruim','grof'];
for(const mode of ['solo','online']) {
  context.saveRaceModeConfig(mode,{durationKey:'blitz'});
  sleutels.forEach((key,index)=>{
    context.selectRaceTolerantie(mode,key);
    assert.equal(context.getRaceModeConfig(mode).toleranceKey,key);
    assert.equal(context.getRaceModeConfig(mode).durationKey,'blitz');
    const naam=mode==='solo'?'Solo':'Online';
    assert.equal(veld('race'+naam+'TolerancesRange').value,String(index));
    const meta=context.raceTolerantieMeta(key);
    assert.equal(veld('race'+naam+'TolerancesRange').attributen['aria-valuetext'],meta.label+' '+meta.name);
    assert.equal(veld('race'+naam+'ToleranceNote').textContent,meta.uitleg);
  });
}
assert.ok(opslag.has('netto_race_mode_config'));
context.selectRaceTolerantie('solo','onbekend');
assert.equal(context.getRaceModeConfig('solo').toleranceKey,'grof');
console.log('Vijf standen, uitleg, aria en bestaande opslag blijven gelijk.');
for(const [tijd,dag] of [['2026-09-08T10:59:59Z','2026-09-07'],['2026-09-08T11:00:00Z','2026-09-08'],['2026-01-08T11:59:59Z','2026-01-07'],['2026-01-08T12:00:00Z','2026-01-08']])assert.equal(context.nettoDagSleutel(new Date(tijd)),dag);
console.log('Dagwissel om 12:00 Londen klopt in zomer- en wintertijd.');
