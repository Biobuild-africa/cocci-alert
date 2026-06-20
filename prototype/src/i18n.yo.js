// =============================================================================
// CocciAlert Yoruba (Yorùbá) UI dictionary
//
// SCOPE OF THIS FILE
//   Every Yoruba-language string the demo displays. To change any Yoruba
//   wording, edit only this file.
//
// APPROVAL STATUS
//   This file is the SOURCE OF TRUTH for what Emmanuel reviews in
//   docs/YORUBA_LOCALIZATION_REVIEW.md. The review file is generated
//   from this dictionary plus src/i18n.en.js (see
//   prototype/generate_yoruba_review.py).
//
// COCCIDIOSIS NAME RULE (from Emmanuel)
//   The English word "coccidiosis" is kept as the technical disease name in
//   Yoruba sentences. The disease is explained in farmer Yoruba alongside it
//   (àrùn inú adìẹ tí ó lè fa ìgbẹ́ gbuuru...), not invented as a fake
//   Yoruba disease term.
//
// LINK TO ENGLISH
//   The shape of this object MUST stay identical to src/i18n.en.js.
// =============================================================================

const i18n_yo = {

  // ----- Top navigation bar -----
  nav_title: "Àpẹẹrẹ Ìfọ̀rọ̀wérọ̀, Ìtọ́nisọ́nà Tó Ń Bá Ipele Mu fún Coccidiosis",
  nav_subtitle: "Àpẹẹrẹ browser tí a ń dán wò, kì í ṣe WhatsApp tàbí USSD gidi.",
  demo_emergency: "Àpẹẹrẹ Pàjáwìrì",
  demo_act_now: "Àpẹẹrẹ Ṣe Ìgbésẹ̀ Báyìí",
  demo_keep_mon: "Àpẹẹrẹ Máa Ṣọ́",
  sound_off: "Ohùn: kò sí",
  sound_on: "Ohùn: ń ṣiṣẹ́",
  restart: "Bẹ̀rẹ̀ lẹ́ẹ̀kansi",

  // ----- Audio status messages (Pass 2) -----
  audio_listen_now: "Gbọ́ ìbéèrè",
  audio_off_hint: "Tẹ Ohùn láti gbọ́",
  yoruba_voice_unavailable: "À ń fi ọ̀rọ̀ Yorùbá hàn. Ìrànlọ́wọ́ ohùn dá lé ìtìlẹ́yìn ohùn fóònù tàbí browser.",

  // ----- Panel headers -----
  panel_left_title: "Ìrírí Àgbẹ̀ (Wíwo Fóònù)",
  panel_right_title: "Wíwo Backend (Láì fi orúkọ hàn)",

  // ----- Phone (farmer view) -----
  phone_header_sub: "Olùrànlọ́wọ́ Ìlera Adìẹ",
  phone_welcome: "Ẹ kú àbọ̀. Mo máa béèrè ìbéèrè díẹ̀ nípa àwọn adìẹ rẹ kí n lè tọ́ ọ sọ́nà. Dáhùn ìbéèrè kọ̀ọ̀kan.",
  phone_sound: "Ohùn kò sí",
  phone_sound_on: "Ohùn ń ṣiṣẹ́",
  phone_replay: "Tún ṣe",
  footer_audio_note: "Ìtìlẹ́yìn ohùn ti ṣiṣẹ́. Ìmọ̀ ohùn browser yàtọ̀ síra wọn.",

  // ----- Progress + stage indicators -----
  progress: "Ìlọsíwájú",
  question_n_of_14: "Ìbéèrè {n} nínú 14",
  stage_emergency: "Ìṣàyẹ̀wò Pàjáwìrì",
  stage_supporting: "Àpẹẹrẹ Ìṣàmúlò",
  stage_result: "Àbájáde",
  badge_emergency: "ÌṢÀYẸ̀WÒ PÀJÁWÌRÌ",
  badge_supporting: "ÀPẸẸRẸ ÌṢÀMÚLÒ",
  badge_result: "ÀBÁJÁDE",
  early_stop_note: "A máa dúró kíákíá tí a bá ní ìmọ̀ tó láti fún ọ ní ìtọ́nisọ́nà tó tọ́.",
  tap_to_hear: "Tẹ láti gbọ́ ìbéèrè",
  replay_question: "Tún Ìbéèrè ṣe",

  // ----- Backend Preview, Session Summary section -----
  session_summary: "Àkójọpọ̀ Ìpàdé",
  consent_given: "A ti gba ìfẹ́wọ́sí",
  language_label: "Èdè",
  raw_phone_stored: "Ṣé a pa nọ́mbà fóònù gidi mọ́",
  geography_level: "Ìpele agbègbè",
  geography_value: "LGA nìkan",
  session_id: "Idi Ìpàdé",

  // ----- Backend Preview, Answers So Far section -----
  answers_so_far: "Àwọn Ìdáhùn Títí di Ìsisìyí (Kóòdù Inú)",

  // ----- Backend Preview, Triage Engine Status section -----
  triage_engine_status: "Ipò Engine Ìtọ́nisọ́nà",
  stage_label: "Ìpele",
  early_stopping: "Ìdúró kíákíá",
  early_not_triggered: "Kò tíì ṣẹlẹ̀",
  early_triggered: "Ó ti ṣẹlẹ̀",
  questions_answered: "Àwọn ìbéèrè tí a ti dáhùn",
  rationale: "Ìdí ìpinnu",
  current_assessment: "Ìṣàyẹ̀wò báyìí",
  collecting_info: "À ń kó ìmọ̀ jọ...",
  decided_emergency: "Pàjáwìrì ti dájú",
  decided_act_now: "Ṣe Ìgbésẹ̀ Báyìí ti dájú",
  decided_keep_mon: "Máa Ṣọ́ ti dájú",

  // ----- Backend Preview, Event Log section -----
  event_log_preview: "Wíwo Event Log (Ọ̀wọ́n tó máa wà ní àkọsílẹ̀)",

  // ----- Result Legend -----
  legend_title: "Ìtumọ̀ àwọn àbájáde",
  legend_emergency_title: "Pàjáwìrì",
  legend_emergency_desc: "Ìrànlọ́wọ́ dókítà ẹranko lẹ́sẹ̀kẹsẹ",
  legend_act_title: "Ṣe Ìgbésẹ̀ Báyìí",
  legend_act_desc: "Ṣe ohun kan láìpẹ́",
  legend_keep_title: "Máa Ṣọ́",
  legend_keep_desc: "Máa bá ìṣàyẹ̀wò lọ",
  legend_disclaimer: "Ìtọ́nisọ́nà nìkan, kì í ṣe ìdánimọ̀ àrùn tàbí ìpàṣẹ oogun.",

  // ----- Result card content -----
  result_title_emergency: "PÀJÁWÌRÌ",
  result_title_act_now: "ṢE ÌGBÉSẸ̀ BÁYÌÍ",
  result_title_keep_mon: "MÁA ṢỌ́",
  result_subtitle_emergency: "Pe dókítà ẹranko lẹ́sẹ̀kẹsẹ.",
  result_subtitle_act_now: "Ṣe ìgbésẹ̀ kí o sì pe dókítà ẹranko láìpẹ́.",
  result_subtitle_keep_mon: "Kò sí ìgbésẹ̀ kíákíá tí a nílò.",
  result_msg_emergency: "Àwọn adìẹ rẹ ní àmì ewu tó nílò ìrànlọ́wọ́ dókítà ẹranko kíákíá. Èyí jẹ́ ìtọ́nisọ́nà, kì í ṣe ìdánimọ̀ àrùn. Má ṣe fi oogun fún ara rẹ. Yà àwọn adìẹ tí ó ń ṣàìsàn sílẹ̀, ya àwòrán ìgbẹ́ wọn bí ó bá ṣeé ṣe.",
  result_msg_act_now: "Ìdáhùn rẹ fihàn pé àwọn adìẹ rẹ wà nínú ewu coccidiosis. Yọ ohun tí wọ́n fi bo ilẹ̀ ilé adìẹ tí ó tutu kúrò. Yà àwọn adìẹ tí ó ń ṣàìsàn sílẹ̀. Tún ohun mímu omi tí ń jo ṣe. Pe dókítà ẹranko, vet, tàbí agro-vet tí a fọwọ́ sí. Má ṣe lo antibiotics láì gba ìmọ̀ràn.",
  result_msg_keep_mon: "Kò sí àpẹẹrẹ ewu coccidiosis tó lágbára tó hàn lónìí. Jẹ́ kí ohun tí wọ́n fi bo ilẹ̀ ilé adìẹ máa gbẹ. Pa ààbò ilé adìẹ mọ́. Pèsè omi mímọ́. Tún ṣàyẹ̀wò ìgbẹ́, oúnjẹ, àti omi wọn lọ́la. Èyí jẹ́ ìtọ́nisọ́nà, kì í ṣe ìdánimọ̀ àrùn.",
  decision_reached: "Ìpinnu dé lẹ́yìn ìbéèrè {n} nínú àwọn ìbéèrè 14 tó ṣeé ṣe.",
  early_stopping_reason_label: "Ìdí ìdúró kíákíá",

  // ----- Per-question helper notes (only for emergency-screen questions) -----
  helper_fresh_blood: "Èyí ni ìṣàyẹ̀wò àkọ́kọ́ fún àmì ewu.",
  helper_orange_mucus: "Ohun alálẹ̀mọ́ aláwọ̀ ọ́sàn jẹ́ àmì ewu tó lágbára.",
  helper_mortality: "Ikú adìẹ lojijì nílò ìgbésẹ̀ kíákíá.",
  helper_droppings: "Bí ìgbẹ́ ṣe rí ń sọ ọ̀pọ̀ nípa ìlera adìẹ.",

  // ----- The 14 questions -----
  questions: {
    fresh_blood: {
      q: "Ṣé ẹ̀jẹ̀ pupa tí ó dà bí tuntun hàn nínú ìgbẹ́ àwọn adìẹ?",
      opts: {
        true:  { text: "Bẹ́ẹ̀ni", desc: "Ẹ̀jẹ̀ tuntun wà." },
        false: { text: "Rárá",    desc: "Ẹ̀jẹ̀ tuntun kò hàn." }
      }
    },
    orange_mucus: {
      q: "Ṣé ohun alálẹ̀mọ́ aláwọ̀ ọ́sàn, tàbí nkan bí ẹran inú, hàn nínú ìgbẹ́ àwọn adìẹ?",
      opts: {
        true:  { text: "Bẹ́ẹ̀ni", desc: "Ohun aláwọ̀ ọ́sàn hàn." },
        false: { text: "Rárá",    desc: "Àwọ̀ ìgbẹ́ jọ́ bí ti deede." }
      }
    },
    mortality: {
      q: "Ṣé iye adìẹ tí ń kú lojoojúmọ́ ti pọ̀ ju ohun tí o máa ń retí lọ?",
      opts: {
        [Mort.NONE]:         { text: "Rárá",                       desc: "Ikú adìẹ wà ní deede." },
        [Mort.GRADUAL]:      { text: "Ó ń pọ̀ sí i díẹ̀díẹ̀",        desc: "Ikú díẹ̀ ju ti deede lọ." },
        [Mort.SUDDEN_SPIKE]: { text: "Ó pọ̀ sí i lojijì",           desc: "Adìẹ púpọ̀ kú nínú àkókò kúkúrú." }
      }
    },
    droppings: {
      q: "Báwo ni ìgbẹ́ àwọn adìẹ ṣe rí jù lọ?",
      opts: {
        [Droppings.NORMAL]:          { text: "Ó dáa, ó sì ní ìdúró",                          desc: "Ìgbẹ́ le, ó dáa." },
        [Droppings.LOOSE]:           { text: "Ó rọ̀",                                          desc: "Ó rọ̀ díẹ̀ ju ti deede lọ." },
        [Droppings.SEVERE_DIARRHEA]: { text: "Ó dà bí omi púpọ̀, ìgbẹ́ gbuuru tó le",          desc: "Ó dà bí omi gan-an." }
      }
    },
    hunched: {
      q: "Ṣé àwọn adìẹ ń wọ́ ara wọn sílẹ̀, tí ìyẹ́ wọn sì ń rú?",
      opts: {
        [Hunched.WIDESPREAD]: { text: "Bẹ́ẹ̀ni, ó pọ̀ ju 10% lọ",         desc: "Àwọn adìẹ púpọ̀ ni ó kàn." },
        [Hunched.ISOLATED]:   { text: "Díẹ̀ nìkan, kéré ju 10% lọ",      desc: "Adìẹ díẹ̀ nìkan ni ó kàn." },
        [Hunched.NONE]:       { text: "Rárá",                            desc: "Àwọn adìẹ wà ní ìjọ́gun dáadáa." }
      }
    },
    huddling: {
      q: "Ṣé àwọn adìẹ ń kó ara wọn jọ bí ẹni pé òtútù ń mú wọn, bó tilẹ̀ jẹ́ pé ilé adìẹ kò tútù?",
      opts: {
        true:  { text: "Bẹ́ẹ̀ni", desc: "Wọ́n ń kó ara wọn jọ pẹ̀lú òtútù." },
        false: { text: "Rárá",    desc: "Wọ́n túká dáadáa." }
      }
    },
    paleness: {
      q: "Ṣé awọ ara, ẹsẹ̀, tàbí àpá pupa lórí àwọn adìẹ ti ń pálẹ̀ ju bó ṣe yẹ lọ?",
      opts: {
        true:  { text: "Bẹ́ẹ̀ni", desc: "Awọ tàbí àpá pupa pálẹ̀." },
        false: { text: "Rárá",    desc: "Àwọ̀ jọ́ bí ti deede." }
      }
    },
    feed: {
      q: "Báwo ni iye oúnjẹ tí àwọn adìẹ ń jẹ ṣe yí padà ní ọjọ́ méjì sẹ́yìn?",
      opts: {
        [Feed.AT_OR_ABOVE]:      { text: "Wọ́n ń jẹun bó ṣe yẹ tàbí ju bẹ́ẹ̀ lọ",   desc: "Wọ́n ń jẹun bí ti deede." },
        [Feed.SLIGHT_DROP]:      { text: "Wọ́n ń jẹun díẹ̀ kere ju ti tẹ́lẹ̀ lọ",   desc: "Wọ́n ń jẹun díẹ̀." },
        [Feed.SIGNIFICANT_DROP]: { text: "Wọ́n ń jẹun púpọ̀ kere ju ti tẹ́lẹ̀ lọ", desc: "Wọ́n kò jẹun rárá." }
      }
    },
    water: {
      q: "Báwo ni mímu omi àwọn adìẹ ṣe yí padà?",
      opts: {
        [Water.NORMAL]:      { text: "Deede",                                       desc: "Wọ́n ń mu omi bí ti deede." },
        [Water.SLIGHT]:      { text: "Wọ́n ń mu omi díẹ̀ kere ju ti tẹ́lẹ̀ lọ",     desc: "Mímu omi dín kù díẹ̀." },
        [Water.SIGNIFICANT]: { text: "Wọ́n ń mu omi púpọ̀ kere ju ti tẹ́lẹ̀ lọ",    desc: "Mímu omi dín kù púpọ̀." }
      }
    },
    age: {
      q: "Ọmọ ọ̀sẹ̀ mélòó ni àwọn adìẹ wọ̀nyí?",
      opts: {
        [Age.UNDER_3W]:    { text: "Kéré ju ọ̀sẹ̀ mẹ́ta lọ",          desc: "Àwọn ọmọ kéékèèké." },
        [Age.THREE_TO_8W]: { text: "Láàárín ọ̀sẹ̀ mẹ́ta sí mẹ́jọ",     desc: "Àwọn adìẹ tí ń dàgbà." },
        [Age.OVER_8W]:     { text: "Ju ọ̀sẹ̀ mẹ́jọ lọ",                desc: "Àwọn adìẹ àgbà." }
      }
    },
    vacc: {
      q: "Níbi tí wọ́n ti yọ àwọn adìẹ náà, ṣé wọ́n fún wọn ní ajẹsára lòdì sí coccidiosis?",
      opts: {
        [Vacc.YES]:     { text: "Bẹ́ẹ̀ni", desc: "A fún wọn ní ajẹsára." },
        [Vacc.NO]:      { text: "Rárá",    desc: "A kò fún wọn ní ajẹsára." },
        [Vacc.UNKNOWN]: { text: "Mi ò mọ̀", desc: "Mi kò mọ̀ àfojúsùn ajẹsára." }
      }
    },
    coccidiostat: {
      q: "Ṣé oúnjẹ tí o ń fún àwọn adìẹ ní ohun ìdènà coccidiosis nínú rẹ̀ báyìí?",
      opts: {
        true:  { text: "Bẹ́ẹ̀ni", desc: "Ohun ìdènà wà nínú oúnjẹ." },
        false: { text: "Rárá",    desc: "Kò sí ohun ìdènà nínú oúnjẹ." }
      }
    },
    litter: {
      q: "Báwo ni ohun tí wọ́n fi bo ilẹ̀ ilé adìẹ ṣe rí lápapọ̀?",
      opts: {
        [Litter.DRY]:               { text: "Ó gbẹ, ó sì tú dáadáa",        desc: "Ó gbẹ, kò tutu." },
        [Litter.DAMP]:              { text: "Ó tutu díẹ̀",                  desc: "Ó ní omi díẹ̀ nínú." },
        [Litter.HEAVILY_CAKED_WET]: { text: "Ó dì pọ̀, ó sì tutu gan-an",   desc: "Ó tutu gan-an, ó sì dì pọ̀." }
      }
    },
    leaking_drinkers: {
      q: "Ṣé omi ń jo láti inú ohun tí adìẹ fi ń mu omi, tàbí ohun náà kò dúró dáadáa, tó sì ń mú kí ìtẹ́ adìẹ tutu ní àwọn ibi kan?",
      opts: {
        true:  { text: "Bẹ́ẹ̀ni", desc: "Omi ń jo." },
        false: { text: "Rárá",    desc: "Ohun mímu omi ń ṣiṣẹ́ dáadáa." }
      }
    }
  }
};
