// =============================================================================
// CocciAlert English UI dictionary
//
// SCOPE OF THIS FILE
//   Every English-language string the demo displays. To change a question,
//   button label, result message, helper text, or backend-preview label in
//   English, edit only this file.
//
// LINK TO YORUBA
//   The shape of this object MUST stay identical to src/i18n.yo.js.
//   The keys here are what render templates look up.
// =============================================================================

const i18n_en = {

  // ----- Top navigation bar -----
  nav_title: "Interactive Demo, Adaptive Triage for Suspected Coccidiosis",
  nav_subtitle: "Controlled browser prototype, not live WhatsApp/USSD deployment.",
  demo_emergency: "Emergency Demo",
  demo_act_now: "Act Now Demo",
  demo_keep_mon: "Keep Monitoring Demo",
  sound_off: "Sound: off",
  sound_on: "Sound: on",
  restart: "Restart",

  // ----- Audio status messages (Pass 2) -----
  audio_listen_now: "Listen to question",
  audio_off_hint: "Click the Sound toggle to listen",
  yoruba_voice_unavailable: "Yorùbá text is displayed; audio support depends on device or browser voice support.",

  // ----- Panel headers -----
  panel_left_title: "Farmer Experience (Phone View)",
  panel_right_title: "Backend Preview (Anonymized)",

  // ----- Phone (farmer view) -----
  phone_header_sub: "Poultry Health Assistant",
  phone_welcome: "Welcome. I will ask some questions about your flock so I can guide you. Reply to each question.",
  phone_sound: "Sound off",
  phone_sound_on: "Sound on",
  phone_replay: "Replay",
  footer_audio_note: "Audio support enabled. Browser voice availability varies.",

  // ----- Progress + stage indicators -----
  progress: "Progress",
  question_n_of_14: "Question {n} of 14",
  stage_emergency: "Emergency Check",
  stage_supporting: "Supporting Signs",
  stage_result: "Result",
  badge_emergency: "EMERGENCY SCREENING",
  badge_supporting: "SUPPORTING SIGNS",
  badge_result: "RESULT",
  early_stop_note: "We will stop early if we have enough information to give you the right guidance.",
  tap_to_hear: "Tap to hear question",
  replay_question: "Replay Question",

  // ----- Backend Preview, Session Summary section -----
  session_summary: "Session Summary",
  consent_given: "Consent given",
  language_label: "Language",
  raw_phone_stored: "Raw phone stored",
  geography_level: "Geography level",
  geography_value: "LGA only",
  session_id: "Session ID",

  // ----- Backend Preview, Answers So Far section -----
  answers_so_far: "Answers So Far (Internal Codes)",

  // ----- Backend Preview, Triage Engine Status section -----
  triage_engine_status: "Triage Engine Status",
  stage_label: "Stage",
  early_stopping: "Early stopping",
  early_not_triggered: "Not triggered yet",
  early_triggered: "Triggered",
  questions_answered: "Questions answered",
  rationale: "Rationale",
  current_assessment: "Current assessment",
  collecting_info: "Collecting information...",
  decided_emergency: "Emergency decided",
  decided_act_now: "Act Now decided",
  decided_keep_mon: "Keep Monitoring decided",

  // ----- Backend Preview, Event Log section -----
  event_log_preview: "Event Log Preview (Row that would be saved)",

  // ----- Result Legend -----
  legend_title: "Result Legend",
  legend_emergency_title: "Emergency",
  legend_emergency_desc: "Immediate veterinary help",
  legend_act_title: "Act Now",
  legend_act_desc: "Take action soon",
  legend_keep_title: "Keep Monitoring",
  legend_keep_desc: "Continue monitoring",
  legend_disclaimer: "Triage only, not diagnosis or prescription.",

  // ----- Result card content -----
  result_title_emergency: "EMERGENCY",
  result_title_act_now: "ACT NOW",
  result_title_keep_mon: "KEEP MONITORING",
  result_subtitle_emergency: "Contact a veterinarian immediately.",
  result_subtitle_act_now: "Take action and contact a veterinarian soon.",
  result_subtitle_keep_mon: "No immediate action needed.",
  result_msg_emergency: "Your flock shows a danger sign that needs urgent veterinary attention. This is triage, not a diagnosis. Do not self-medicate. Isolate visibly sick birds and document droppings if possible.",
  result_msg_act_now: "Your answers suggest your flock is at risk of coccidiosis. Remove wet litter, isolate sick birds, fix leaking drinkers, and contact a veterinary officer or approved agro-vet. Do not self-medicate with antibiotics.",
  result_msg_keep_mon: "No red-flag coccidiosis pattern detected today. Maintain dry litter, biosecurity, clean water, and recheck droppings, feed, and water tomorrow. This is triage, not a diagnosis.",
  decision_reached: "Decision reached after {n} of 14 possible questions.",
  early_stopping_reason_label: "Early stopping reason",

  // ----- Per-question helper notes (only for emergency-screen questions) -----
  helper_fresh_blood: "This is the first check for danger signs.",
  helper_orange_mucus: "Orange mucus or sloughed tissue is a serious warning sign.",
  helper_mortality: "Sudden flock death needs urgent attention.",
  helper_droppings: "Droppings consistency tells us a lot about flock health.",

  // ----- The 14 questions -----
  questions: {
    fresh_blood: {
      q: "Are there visible signs of fresh blood in the droppings?",
      opts: {
        true: { text: "Yes", desc: "There is fresh blood." },
        false: { text: "No", desc: "No fresh blood visible." }
      }
    },
    orange_mucus: {
      q: "Is there orange mucus or sloughed intestinal tissue present?",
      opts: {
        true: { text: "Yes", desc: "Orange mucus or tissue visible." },
        false: { text: "No", desc: "Droppings look normal in color." }
      }
    },
    mortality: {
      q: "Has daily mortality exceeded the expected baseline for this age?",
      opts: {
        [Mort.NONE]:         { text: "No",                desc: "Mortality is normal for this age." },
        [Mort.GRADUAL]:      { text: "Gradual increase",  desc: "Slightly more deaths than usual." },
        [Mort.SUDDEN_SPIKE]: { text: "Sudden spike",      desc: "Many deaths in a short time." }
      }
    },
    droppings: {
      q: "What is the predominant consistency of the droppings?",
      opts: {
        [Droppings.NORMAL]:          { text: "Normal, firm",        desc: "Solid, well-formed droppings." },
        [Droppings.LOOSE]:           { text: "Loose",               desc: "Softer than usual but not watery." },
        [Droppings.SEVERE_DIARRHEA]: { text: "Severe diarrhea",     desc: "Very watery, mostly liquid." }
      }
    },
    hunched: {
      q: "Are birds exhibiting a hunched posture with ruffled feathers?",
      opts: {
        [Hunched.WIDESPREAD]: { text: "Widespread, over 10% of flock",  desc: "Many birds are affected." },
        [Hunched.ISOLATED]:   { text: "Isolated, under 10% of flock",   desc: "Only a few birds are affected." },
        [Hunched.NONE]:       { text: "None",                           desc: "Birds look alert and active." }
      }
    },
    huddling: {
      q: "Are birds huddling together despite adequate ambient temperatures?",
      opts: {
        true:  { text: "Yes", desc: "Birds are clumping even though it is warm." },
        false: { text: "No",  desc: "Birds are spread out normally." }
      }
    },
    paleness: {
      q: "Is there noticeable paleness or depigmentation in the skin, shanks, or combs?",
      opts: {
        true:  { text: "Yes", desc: "Skin or combs look pale." },
        false: { text: "No",  desc: "Color looks normal." }
      }
    },
    feed: {
      q: "How has daily feed intake changed over the last 48 hours?",
      opts: {
        [Feed.AT_OR_ABOVE]:      { text: "At or above target",          desc: "Birds are eating normally." },
        [Feed.SLIGHT_DROP]:      { text: "Slight drop, under 10%",      desc: "Eating a little less than usual." },
        [Feed.SIGNIFICANT_DROP]: { text: "Significant drop, over 10%",  desc: "Eating much less than usual." }
      }
    },
    water: {
      q: "How has daily water consumption changed?",
      opts: {
        [Water.NORMAL]:      { text: "Normal",            desc: "Birds are drinking as usual." },
        [Water.SLIGHT]:      { text: "Slight drop",       desc: "Drinking a little less than usual." },
        [Water.SIGNIFICANT]: { text: "Significant drop",  desc: "Drinking much less than usual." }
      }
    },
    age: {
      q: "What is the current age of the flock?",
      opts: {
        [Age.UNDER_3W]:    { text: "Less than 3 weeks", desc: "Very young chicks." },
        [Age.THREE_TO_8W]: { text: "3 to 8 weeks",      desc: "Growing birds." },
        [Age.OVER_8W]:     { text: "More than 8 weeks", desc: "Older birds." }
      }
    },
    vacc: {
      q: "Was the flock vaccinated for coccidiosis at the hatchery?",
      opts: {
        [Vacc.YES]:     { text: "Yes",     desc: "Vaccination confirmed." },
        [Vacc.NO]:      { text: "No",      desc: "Not vaccinated." },
        [Vacc.UNKNOWN]: { text: "Unknown", desc: "Not sure about vaccination." }
      }
    },
    coccidiostat: {
      q: "Is the flock currently on a dietary coccidiostat program in the feed?",
      opts: {
        true:  { text: "Yes", desc: "Coccidiostat is in the feed." },
        false: { text: "No",  desc: "No coccidiostat in the feed." }
      }
    },
    litter: {
      q: "What is the overall physical condition of the litter?",
      opts: {
        [Litter.DRY]:               { text: "Dry and friable",       desc: "Litter is dry and loose." },
        [Litter.DAMP]:              { text: "Damp",                  desc: "Litter has some wetness." },
        [Litter.HEAVILY_CAKED_WET]: { text: "Heavily caked and wet", desc: "Litter is wet and stuck together." }
      }
    },
    leaking_drinkers: {
      q: "Are there misaligned or leaking drinkers creating localized wet spots?",
      opts: {
        true:  { text: "Yes", desc: "Drinkers are leaking or off-position." },
        false: { text: "No",  desc: "Drinkers are working properly." }
      }
    }
  }
};
