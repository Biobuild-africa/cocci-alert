// =============================================================================
// CocciAlert rule engine, JavaScript port of engine/cocci_engine.py
//
// SCOPE OF THIS FILE
//   Internal codes and decision rules ONLY. No display text. No language.
//   Same outputs as the Python engine on identical inputs.
//
// WHAT TO EDIT WHERE
//   - To change a clinical rule, threshold, or sign list, edit this file
//     AND the matching rule in engine/cocci_engine.py so they stay in sync.
//   - All farmer-facing wording lives in src/i18n.en.js and src/i18n.yo.js.
//   - The asking order lives in src/flow_controller.js.
// =============================================================================

// ----- Enum-like constants (stable internal codes) -----

const Droppings = { NORMAL: "Normal (Firm)", LOOSE: "Loose", SEVERE_DIARRHEA: "Severe Diarrhea" };
const Hunched   = { WIDESPREAD: "Widespread (>10%)", ISOLATED: "Isolated (<10%)", NONE: "None" };
const Feed      = { AT_OR_ABOVE: "At/Above Target", SLIGHT_DROP: "Slight Drop (<10%)", SIGNIFICANT_DROP: "Significant Drop (>10%)" };
const Water     = { NORMAL: "Normal", SLIGHT: "Slight Drop", SIGNIFICANT: "Significant Drop" };
const Age       = { UNDER_3W: "< 3 weeks", THREE_TO_8W: "3 to 8 weeks", OVER_8W: "> 8 weeks" };
const Vacc      = { YES: "Yes", NO: "No", UNKNOWN: "Unknown" };
const Mort      = { NONE: "No", GRADUAL: "Gradual Increase", SUDDEN_SPIKE: "Sudden Spike" };
const Litter    = { DRY: "Dry & Friable", DAMP: "Damp", HEAVILY_CAKED_WET: "Heavily Caked & Wet" };

const Triage = {
  EMERGENCY: "Emergency",
  ACT_NOW: "Act now",
  KEEP_MONITORING: "Keep monitoring, no coccidiosis"
};

// ----- Question schema (key + valid answer codes + ui accent) -----
// Stable: this drives the controller. UI text comes from i18n.

const SCHEMA = [
  { key: "fresh_blood",      options: [{code: true,  accent: "danger"}, {code: false, accent: "safe"}] },
  { key: "orange_mucus",     options: [{code: true,  accent: "danger"}, {code: false, accent: "safe"}] },
  { key: "mortality",        options: [{code: Mort.NONE, accent: "safe"}, {code: Mort.GRADUAL, accent: "warn"}, {code: Mort.SUDDEN_SPIKE, accent: "danger"}] },
  { key: "droppings",        options: [{code: Droppings.NORMAL, accent: "safe"}, {code: Droppings.LOOSE, accent: "warn"}, {code: Droppings.SEVERE_DIARRHEA, accent: "danger"}] },
  { key: "hunched",          options: [{code: Hunched.WIDESPREAD, accent: "danger"}, {code: Hunched.ISOLATED, accent: "warn"}, {code: Hunched.NONE, accent: "safe"}] },
  { key: "huddling",         options: [{code: true, accent: "warn"}, {code: false, accent: "safe"}] },
  { key: "paleness",         options: [{code: true, accent: "warn"}, {code: false, accent: "safe"}] },
  { key: "feed",             options: [{code: Feed.AT_OR_ABOVE, accent: "safe"}, {code: Feed.SLIGHT_DROP, accent: "warn"}, {code: Feed.SIGNIFICANT_DROP, accent: "danger"}] },
  { key: "water",            options: [{code: Water.NORMAL, accent: "safe"}, {code: Water.SLIGHT, accent: "warn"}, {code: Water.SIGNIFICANT, accent: "danger"}] },
  { key: "age",              options: [{code: Age.UNDER_3W, accent: "warn"}, {code: Age.THREE_TO_8W, accent: "neutral"}, {code: Age.OVER_8W, accent: "safe"}] },
  { key: "vacc",             options: [{code: Vacc.YES, accent: "safe"}, {code: Vacc.NO, accent: "warn"}, {code: Vacc.UNKNOWN, accent: "warn"}] },
  { key: "coccidiostat",     options: [{code: true, accent: "safe"}, {code: false, accent: "warn"}] },
  { key: "litter",           options: [{code: Litter.DRY, accent: "safe"}, {code: Litter.DAMP, accent: "warn"}, {code: Litter.HEAVILY_CAKED_WET, accent: "danger"}] },
  { key: "leaking_drinkers", options: [{code: true, accent: "warn"}, {code: false, accent: "safe"}] }
];

// ----- Supporting-sign tally (operates on partial answer sets) -----

function collectSupportingSigns(a) {
  const signs = [];
  if (a.hunched === Hunched.WIDESPREAD) signs.push("hunched_widespread");
  if (a.huddling === true) signs.push("huddling");
  if (a.paleness === true) signs.push("paleness");
  if (a.feed === Feed.SLIGHT_DROP || a.feed === Feed.SIGNIFICANT_DROP) signs.push("feed_drop");
  if (a.water === Water.SLIGHT || a.water === Water.SIGNIFICANT) signs.push("water_drop");
  if (a.age === Age.UNDER_3W) signs.push("age_under_3w");
  if (a.vacc === Vacc.NO || a.vacc === Vacc.UNKNOWN) signs.push("no_vacc");
  if (a.coccidiostat === false) signs.push("no_coccidiostat");
  if (a.mortality === Mort.GRADUAL) signs.push("gradual_mortality");
  if (a.litter === Litter.DAMP || a.litter === Litter.HEAVILY_CAKED_WET) signs.push("damp_litter");
  if (a.leaking_drinkers === true) signs.push("leaking_drinkers");
  return signs;
}

// ----- Partial decision evaluator -----
// Operates on a partial answer set. Returns:
//   null if no decision can be made yet (controller should ask more).
//   {outcome, reason_code, ...} the moment a decision is determined.
// Uses the same rules as evaluatePartial would on a fully populated set,
// so the final answer set is consistent with engine/cocci_engine.py.

function evaluatePartial(a) {
  // 1. Emergency triggers (any one fires Emergency immediately).
  if (a.fresh_blood === true) {
    return { outcome: Triage.EMERGENCY, reason_code: "fresh_blood_in_droppings",
             triggers: ["Fresh blood visible in droppings"] };
  }
  if (a.orange_mucus === true) {
    return { outcome: Triage.EMERGENCY, reason_code: "orange_mucus_or_sloughed_tissue",
             triggers: ["Orange mucus or sloughed intestinal tissue"] };
  }
  if (a.mortality === Mort.SUDDEN_SPIKE) {
    return { outcome: Triage.EMERGENCY, reason_code: "sudden_mortality_spike",
             triggers: ["Sudden mortality spike"] };
  }
  // Severe diarrhea + major systemic sign = Emergency.
  if (a.droppings === Droppings.SEVERE_DIARRHEA) {
    const majors = [];
    if (a.hunched === Hunched.WIDESPREAD) majors.push("widespread hunched posture");
    if (a.huddling === true) majors.push("widespread huddling");
    if (a.paleness === true) majors.push("noticeable paleness");
    if (a.feed === Feed.SIGNIFICANT_DROP) majors.push("significant feed drop");
    if (a.water === Water.SIGNIFICANT) majors.push("significant water drop");
    if (majors.length > 0) {
      return { outcome: Triage.EMERGENCY, reason_code: "severe_diarrhea_with_systemic",
               triggers: ["Severe diarrhea with " + majors.join(", ")] };
    }
  }

  // 2. Emergency must be fully cleared before non-emergency outcomes.
  // Cleared means: Q1, Q2, Q12, Q3 all answered. If Q3=severe, also Q4-Q8.
  const emergencyCleared = (
    a.fresh_blood !== undefined &&
    a.orange_mucus !== undefined &&
    a.mortality !== undefined &&
    a.droppings !== undefined &&
    (a.droppings !== Droppings.SEVERE_DIARRHEA ||
      (a.hunched !== undefined && a.huddling !== undefined &&
       a.paleness !== undefined && a.feed !== undefined && a.water !== undefined))
  );
  if (!emergencyCleared) return null;

  // 3. Supporting-sign tally with threshold based on Q3 droppings.
  const signs = collectSupportingSigns(a);
  const n = signs.length;
  let threshold, reason_code;
  if (a.droppings === Droppings.SEVERE_DIARRHEA) {
    threshold = 1; reason_code = "severe_threshold_reached";
  } else if (a.droppings === Droppings.LOOSE) {
    threshold = 2; reason_code = "loose_threshold_reached";
  } else {
    threshold = 3; reason_code = "normal_threshold_reached";
  }
  if (n >= threshold) {
    return { outcome: Triage.ACT_NOW, reason_code, signs, signsCount: n, threshold };
  }

  // 4. All 14 asked, no emergency, no Act-now threshold = Keep monitoring.
  const allKeys = SCHEMA.map(s => s.key);
  const allAnswered = allKeys.every(k => a[k] !== undefined);
  if (allAnswered) {
    return { outcome: Triage.KEEP_MONITORING, reason_code: "all_questions_answered",
             signs, signsCount: n, threshold };
  }

  // 5. Indeterminate, controller should ask more.
  return null;
}
