// =============================================================================
// CocciAlert demo scenarios
//
// SCOPE OF THIS FILE
//   Three fully-specified answer sets that the demo buttons replay through
//   the adaptive controller. Each one is chosen so it stops at a different
//   point and produces a different outcome.
//
// WHAT TO EDIT WHERE
//   - To change which question chain a demo button shows, edit the answer
//     dict here.
//   - To change a demo button label, edit i18n.en.js / i18n.yo.js.
//   - To change which scenarios run in the headless test, edit
//     src/test_adaptive_demo.js.
// =============================================================================

const DEMO_SCENARIOS = {

  // Emergency in 1 question: fresh_blood = true short-circuits.
  emergency: {
    fresh_blood: true
  },

  // Act Now in 6 questions: Q1=no, Q2=no, Q12=no spike, Q3=loose,
  // then Q4=widespread (sign 1), Q5=yes (sign 2). Threshold reached.
  act_now: {
    fresh_blood: false,
    orange_mucus: false,
    mortality: Mort.NONE,
    droppings: Droppings.LOOSE,
    hunched: Hunched.WIDESPREAD,
    huddling: true
  },

  // Keep Monitoring in 14 questions: all 14 must be ruled out before the
  // engine can conclude no coccidiosis pattern is present.
  keep_monitoring: {
    fresh_blood: false,
    orange_mucus: false,
    mortality: Mort.NONE,
    droppings: Droppings.NORMAL,
    hunched: Hunched.NONE,
    huddling: false,
    paleness: false,
    feed: Feed.AT_OR_ABOVE,
    water: Water.NORMAL,
    age: Age.OVER_8W,
    vacc: Vacc.YES,
    coccidiostat: true,
    litter: Litter.DRY,
    leaking_drinkers: false
  }
};
