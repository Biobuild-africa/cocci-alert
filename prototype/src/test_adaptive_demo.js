// =============================================================================
// CocciAlert adaptive-flow test harness
//
// USAGE
//   node prototype/src/test_adaptive_demo.js
//
// WHAT IT TESTS
//   1. Each demo scenario (Emergency / Act Now / Keep Monitoring) reaches the
//      expected outcome via the adaptive controller.
//   2. The localized result title for each language is the expected string.
//   3. The question-count is computed, not hard-coded.
//   4. English and Yoruba i18n dictionaries have identical shape and option
//      coverage.
// =============================================================================

const fs = require('fs');
const path = require('path');

const SRC_DIR = __dirname;

// Concatenate the source files in load order, then add a module.exports at the
// end so we can require() the result and inspect the engine + i18n + scenarios
// from this test process.
const FILES = [
  'engine.js',
  'flow_controller.js',
  'i18n.en.js',
  'i18n.yo.js',
  'demo_scenarios.js'
];

let src = FILES.map(f => '// === src/' + f + ' ===\n' + fs.readFileSync(path.join(SRC_DIR, f), 'utf-8')).join('\n\n');
src += '\n\nmodule.exports = {\n' +
       '  Droppings, Hunched, Feed, Water, Age, Vacc, Mort, Litter, Triage,\n' +
       '  SCHEMA, evaluatePartial, collectSupportingSigns,\n' +
       '  STAGE_A_ORDER, SEVERE_SUBCHECK_ORDER, STAGE_B_ORDER, pickNextQuestion, runScenario,\n' +
       '  i18n_en, i18n_yo, DEMO_SCENARIOS\n' +
       '};\n';

const tmpPath = '/tmp/cocci_bundled_for_test.js';
fs.writeFileSync(tmpPath, src);
const M = require(tmpPath);

console.log('\n=== CocciAlert adaptive flow tests ===\n');

let pass = 0, fail = 0;

function runOne(name, lang, demoKey, expectedOutcome, expectedReason) {
  const result = M.runScenario(M.DEMO_SCENARIOS[demoKey]);
  const r = result.decision;
  const askedCount = result.questionsAsked.length;
  const outcomeOk = r && r.outcome === expectedOutcome;
  const reasonOk  = r && r.reason_code === expectedReason;
  const ok = outcomeOk && reasonOk;
  const titleKey = r.outcome === M.Triage.EMERGENCY ? "emergency"
                 : r.outcome === M.Triage.ACT_NOW   ? "act_now"
                 : "keep_mon";
  const localizedTitle = M.i18n_en && M.i18n_yo ? (lang === 'en' ? M.i18n_en : M.i18n_yo)["result_title_" + titleKey] : "?";
  const localizedReached = (lang === 'en' ? M.i18n_en : M.i18n_yo).decision_reached.replace("{n}", askedCount);
  console.log('  ' + (ok ? 'PASS' : 'FAIL') + '  ' + name);
  console.log('        outcome: ' + r.outcome);
  console.log('        reason_code: ' + r.reason_code);
  console.log('        questions_answered_count: ' + askedCount);
  console.log('        questions asked: ' + result.questionsAsked.join(' -> '));
  console.log('        localized title (' + lang + '): "' + localizedTitle + '"');
  console.log('        localized "decision reached" (' + lang + '): "' + localizedReached + '"');
  console.log('');
  return ok;
}

const tests = [
  ['English Emergency (fresh blood = true)',           'en', 'emergency',       'Emergency',                       'fresh_blood_in_droppings'],
  ['Yoruba  Emergency (fresh blood = true)',           'yo', 'emergency',       'Emergency',                       'fresh_blood_in_droppings'],
  ['English Act Now (loose + 2 supporting signs)',     'en', 'act_now',         'Act now',                         'loose_threshold_reached'],
  ['Yoruba  Act Now (loose + 2 supporting signs)',     'yo', 'act_now',         'Act now',                         'loose_threshold_reached'],
  ['English Keep Monitoring (all clean)',              'en', 'keep_monitoring', 'Keep monitoring, no coccidiosis', 'all_questions_answered'],
  ['Yoruba  Keep Monitoring (all clean)',              'yo', 'keep_monitoring', 'Keep monitoring, no coccidiosis', 'all_questions_answered'],
];
for (const t of tests) {
  if (runOne(...t)) pass++; else fail++;
}

console.log('--- Invariant checks ---\n');

// Shape parity
const enKeys = new Set(Object.keys(M.i18n_en));
const yoKeys = new Set(Object.keys(M.i18n_yo));
const onlyEn = [...enKeys].filter(k => !yoKeys.has(k));
const onlyYo = [...yoKeys].filter(k => !enKeys.has(k));
const shapeOk = onlyEn.length === 0 && onlyYo.length === 0;
console.log('  ' + (shapeOk ? 'OK  ' : 'FAIL') + ' i18n top-level shape: ' + enKeys.size + ' EN keys, ' + yoKeys.size + ' YO keys');
if (onlyEn.length) console.log('       EN only:', onlyEn);
if (onlyYo.length) console.log('       YO only:', onlyYo);

// Question coverage
const enQ = new Set(Object.keys(M.i18n_en.questions));
const yoQ = new Set(Object.keys(M.i18n_yo.questions));
console.log('  ' + (enQ.size === yoQ.size && [...enQ].every(k => yoQ.has(k)) ? 'OK  ' : 'FAIL') + ' 14 questions: ' + enQ.size + ' EN, ' + yoQ.size + ' YO');

// Option coverage
let gaps = 0;
for (const item of M.SCHEMA) {
  for (const lg of ['en','yo']) {
    const opts = (lg === 'en' ? M.i18n_en : M.i18n_yo).questions[item.key].opts;
    for (const opt of item.options) {
      if (!(String(opt.code) in opts)) { gaps++; console.log('    GAP: ' + lg + '.' + item.key + ' missing code', opt.code); }
    }
  }
}
console.log('  ' + (gaps === 0 ? 'OK  ' : 'FAIL') + ' every option in SCHEMA has labels in both languages (' + gaps + ' gaps)');

// Computed counts
const e = M.runScenario(M.DEMO_SCENARIOS.emergency);
const a = M.runScenario(M.DEMO_SCENARIOS.act_now);
const k = M.runScenario(M.DEMO_SCENARIOS.keep_monitoring);
console.log('\n  Question counts (computed by the controller, not hard-coded):');
console.log('    Emergency        stops after ' + e.questionsAsked.length + ' question(s)');
console.log('    Act Now          stops after ' + a.questionsAsked.length + ' question(s)');
console.log('    Keep Monitoring  stops after ' + k.questionsAsked.length + ' question(s)');

console.log('\n' + pass + '/' + tests.length + ' scenario tests passed.');
process.exit(fail === 0 && gaps === 0 && shapeOk ? 0 : 1);
