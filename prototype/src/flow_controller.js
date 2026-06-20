// =============================================================================
// CocciAlert adaptive flow controller
//
// SCOPE OF THIS FILE
//   The order in which the controller asks the 14 questions, plus the
//   "decide-or-continue" loop. Uses the engine rules in src/engine.js; never
//   invents separate clinical logic.
//
// WHAT TO EDIT WHERE
//   - To change the asking order, edit STAGE_A_ORDER, SEVERE_SUBCHECK_ORDER,
//     and STAGE_B_ORDER below.
//   - Clinical thresholds and rules live in src/engine.js (and the Python
//     engine they mirror).
// =============================================================================

// Stage A: emergency-screen questions, asked in this order.
// Each one short-circuits the moment it triggers Emergency.
const STAGE_A_ORDER = ["fresh_blood", "orange_mucus", "mortality", "droppings"];

// If droppings answer is SEVERE_DIARRHEA, ask these next to check for major
// systemic signs. Any one in its "major" form fires Emergency.
const SEVERE_SUBCHECK_ORDER = ["hunched", "huddling", "paleness", "feed", "water"];

// Stage B: supporting-sign questions, asked one at a time. After each answer
// the engine checks if the Act-now threshold has been reached.
const STAGE_B_ORDER = ["hunched", "huddling", "paleness", "feed", "water",
                       "age", "vacc", "coccidiostat", "litter", "leaking_drinkers"];

function pickNextQuestion(answers) {
  // Stage A: emergency screen.
  for (const k of STAGE_A_ORDER) {
    if (answers[k] === undefined) return { key: k, stage: "emergency" };
  }
  // Severe-diarrhea sub-check (only when Q3 = severe).
  if (answers.droppings === Droppings.SEVERE_DIARRHEA) {
    for (const k of SEVERE_SUBCHECK_ORDER) {
      if (answers[k] === undefined) return { key: k, stage: "emergency" };
    }
  }
  // Stage B: supporting signs.
  for (const k of STAGE_B_ORDER) {
    if (answers[k] === undefined) return { key: k, stage: "supporting" };
  }
  return null;
}

// Test helper: replay a fully-specified answer set through the controller and
// stop the moment a decision fires. Returns the final state.
function runScenario(initialAnswers) {
  const localState = { answers: {}, questionsAsked: [], decision: null };
  let safety = 30;
  while (!localState.decision && safety-- > 0) {
    const next = pickNextQuestion(localState.answers);
    if (!next) break;
    if (!(next.key in initialAnswers)) break;
    localState.answers[next.key] = initialAnswers[next.key];
    localState.questionsAsked.push(next.key);
    localState.decision = evaluatePartial(localState.answers);
  }
  return localState;
}
