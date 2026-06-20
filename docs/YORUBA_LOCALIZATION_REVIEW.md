# Yorùbá Localization Review

Auto-generated from `prototype/src/i18n.en.js` and `prototype/src/i18n.yo.js` by `prototype/generate_yoruba_review.py`. Regenerate after any wording change so this file always matches the live demo text.

**Reviewer:** Dr. Emmanuel Alagbe Oluwabukunmi (Science Lead).

**Drafted by:** Johnson Adetooto, with ChatGPT-assisted farmer-facing wording.

**Approval signal:** flip `☐` to `☑` on every row you approve as-is. For any row that needs a revision, replace the Yorùbá text in `prototype/src/i18n.yo.js`, rerun `python prototype/generate_yoruba_review.py`, and leave the box `☐` until the new wording is in place.

**Critical rule:** the *Internal code* column drives the rule engine. Only the *English* and *Yorùbá* columns are display text. Never change the codes.

**Coccidiosis name rule (Emmanuel):** the English word `coccidiosis` is kept as the technical disease name in Yorùbá sentences. The disease is explained alongside it in farmer Yorùbá. Never invented as a fake Yorùbá disease term.


## A. UI chrome (top bar, panels, status fields, legend, result card)


## Top navigation bar

| Key | English | Yorùbá | Where shown | Approval |
| --- | --- | --- | --- | --- |
| `nav_title` | Interactive Demo, Adaptive Triage for Suspected Coccidiosis | Àpẹẹrẹ Ìfọ̀rọ̀wérọ̀, Ìtọ́nisọ́nà Tó Ń Bá Ipele Mu fún Coccidiosis | Main demo title | ☐ |
| `nav_subtitle` | Controlled browser prototype, not live WhatsApp/USSD deployment. | Àpẹẹrẹ browser tí a ń dán wò, kì í ṣe WhatsApp tàbí USSD gidi. | Subtitle under main demo title | ☐ |
| `demo_emergency` | Emergency Demo | Àpẹẹrẹ Pàjáwìrì | Emergency Demo button label | ☐ |
| `demo_act_now` | Act Now Demo | Àpẹẹrẹ Ṣe Ìgbésẹ̀ Báyìí | Act Now Demo button label | ☐ |
| `demo_keep_mon` | Keep Monitoring Demo | Àpẹẹrẹ Máa Ṣọ́ | Keep Monitoring Demo button label | ☐ |
| `sound_off` | Sound: off | Ohùn: kò sí | Sound toggle when off | ☐ |
| `sound_on` | Sound: on | Ohùn: ń ṣiṣẹ́ | Sound toggle when on (Pass 2) | ☐ |
| `restart` | Restart | Bẹ̀rẹ̀ lẹ́ẹ̀kansi | Restart button label | ☐ |


## Audio status messages (Pass 2)

| Key | English | Yorùbá | Where shown | Approval |
| --- | --- | --- | --- | --- |
| `audio_listen_now` | Listen to question | Gbọ́ ìbéèrè | Listen button label when sound is on | ☐ |
| `audio_off_hint` | Click the Sound toggle to listen | Tẹ Ohùn láti gbọ́ | Hint text shown when sound is off | ☐ |
| `yoruba_voice_unavailable` | Yorùbá text is displayed; audio support depends on device or browser voice support. | À ń fi ọ̀rọ̀ Yorùbá hàn. Ìrànlọ́wọ́ ohùn dá lé ìtìlẹ́yìn ohùn fóònù tàbí browser. | Amber banner shown under top nav when Yoruba voice is not available on device | ☐ |
| `footer_audio_note` | Audio support enabled. Browser voice availability varies. | Ìtìlẹ́yìn ohùn ti ṣiṣẹ́. Ìmọ̀ ohùn browser yàtọ̀ síra wọn. | Bilingual note shown at the bottom of the page indicating audio is enabled | ☐ |


## Panel headers

| Key | English | Yorùbá | Where shown | Approval |
| --- | --- | --- | --- | --- |
| `panel_left_title` | Farmer Experience (Phone View) | Ìrírí Àgbẹ̀ (Wíwo Fóònù) | Left panel header | ☐ |
| `panel_right_title` | Backend Preview (Anonymized) | Wíwo Backend (Láì fi orúkọ hàn) | Right panel header | ☐ |


## Phone (farmer view)

| Key | English | Yorùbá | Where shown | Approval |
| --- | --- | --- | --- | --- |
| `phone_header_sub` | Poultry Health Assistant | Olùrànlọ́wọ́ Ìlera Adìẹ | Phone subtitle under brand name | ☐ |
| `phone_welcome` | Welcome. I will ask some questions about your flock so I can guide you. Reply to each question. | Ẹ kú àbọ̀. Mo máa béèrè ìbéèrè díẹ̀ nípa àwọn adìẹ rẹ kí n lè tọ́ ọ sọ́nà. Dáhùn ìbéèrè kọ̀ọ̀kan. | Welcome message bot bubble | ☐ |
| `phone_sound` | Sound off | Ohùn kò sí | Phone-area sound label when sound is off | ☐ |
| `phone_sound_on` | Sound on | Ohùn ń ṣiṣẹ́ | Phone-area sound label when sound is on (Pass 2) | ☐ |
| `phone_replay` | Replay | Tún ṣe | Phone-area replay label | ☐ |


## Progress and stage indicators

| Key | English | Yorùbá | Where shown | Approval |
| --- | --- | --- | --- | --- |
| `progress` | Progress | Ìlọsíwájú | Progress label above bar | ☐ |
| `question_n_of_14` | Question {n} of 14 | Ìbéèrè {n} nínú 14 | Question counter, {n} is replaced at render time | ☐ |
| `stage_emergency` | Emergency Check | Ìṣàyẹ̀wò Pàjáwìrì | Stage 1 chip name | ☐ |
| `stage_supporting` | Supporting Signs | Àpẹẹrẹ Ìṣàmúlò | Stage 2 chip name | ☐ |
| `stage_result` | Result | Àbájáde | Stage 3 chip name | ☐ |
| `badge_emergency` | EMERGENCY SCREENING | ÌṢÀYẸ̀WÒ PÀJÁWÌRÌ | Active-stage badge during emergency screen | ☐ |
| `badge_supporting` | SUPPORTING SIGNS | ÀPẸẸRẸ ÌṢÀMÚLÒ | Active-stage badge during supporting-sign tally | ☐ |
| `badge_result` | RESULT | ÀBÁJÁDE | Active-stage badge on the result screen | ☐ |
| `early_stop_note` | We will stop early if we have enough information to give you the right guidance. | A máa dúró kíákíá tí a bá ní ìmọ̀ tó láti fún ọ ní ìtọ́nisọ́nà tó tọ́. | Yellow lightbulb note under question | ☐ |
| `tap_to_hear` | Tap to hear question | Tẹ láti gbọ́ ìbéèrè | Pill under question, audio is Pass 2 | ☐ |
| `replay_question` | Replay Question | Tún Ìbéèrè ṣe | Replay button next to tap-to-hear | ☐ |


## Backend Preview, Session Summary section

| Key | English | Yorùbá | Where shown | Approval |
| --- | --- | --- | --- | --- |
| `session_summary` | Session Summary | Àkójọpọ̀ Ìpàdé | Section header | ☐ |
| `consent_given` | Consent given | A ti gba ìfẹ́wọ́sí | Consent row label | ☐ |
| `language_label` | Language | Èdè | Language row label | ☐ |
| `raw_phone_stored` | Raw phone stored | Ṣé a pa nọ́mbà fóònù gidi mọ́ | Raw phone row label | ☐ |
| `geography_level` | Geography level | Ìpele agbègbè | Geography row label | ☐ |
| `geography_value` | LGA only | LGA nìkan | Geography row value | ☐ |
| `session_id` | Session ID | Idi Ìpàdé | Session ID row label | ☐ |


## Backend Preview, Answers So Far section

| Key | English | Yorùbá | Where shown | Approval |
| --- | --- | --- | --- | --- |
| `answers_so_far` | Answers So Far (Internal Codes) | Àwọn Ìdáhùn Títí di Ìsisìyí (Kóòdù Inú) | Section header | ☐ |


## Backend Preview, Triage Engine Status section

| Key | English | Yorùbá | Where shown | Approval |
| --- | --- | --- | --- | --- |
| `triage_engine_status` | Triage Engine Status | Ipò Engine Ìtọ́nisọ́nà | Section header | ☐ |
| `stage_label` | Stage | Ìpele | Stage row label | ☐ |
| `early_stopping` | Early stopping | Ìdúró kíákíá | Early-stopping row label | ☐ |
| `early_not_triggered` | Not triggered yet | Kò tíì ṣẹlẹ̀ | Early-stopping value while collecting | ☐ |
| `early_triggered` | Triggered | Ó ti ṣẹlẹ̀ | Early-stopping value after decision | ☐ |
| `questions_answered` | Questions answered | Àwọn ìbéèrè tí a ti dáhùn | Questions-answered row label | ☐ |
| `rationale` | Rationale | Ìdí ìpinnu | Rationale row label | ☐ |
| `current_assessment` | Current assessment | Ìṣàyẹ̀wò báyìí | Current-assessment row label | ☐ |
| `collecting_info` | Collecting information... | À ń kó ìmọ̀ jọ... | Current-assessment value while collecting | ☐ |
| `decided_emergency` | Emergency decided | Pàjáwìrì ti dájú | Current-assessment value at Emergency | ☐ |
| `decided_act_now` | Act Now decided | Ṣe Ìgbésẹ̀ Báyìí ti dájú | Current-assessment value at Act Now | ☐ |
| `decided_keep_mon` | Keep Monitoring decided | Máa Ṣọ́ ti dájú | Current-assessment value at Keep Monitoring | ☐ |


## Backend Preview, Event Log section

| Key | English | Yorùbá | Where shown | Approval |
| --- | --- | --- | --- | --- |
| `event_log_preview` | Event Log Preview (Row that would be saved) | Wíwo Event Log (Ọ̀wọ́n tó máa wà ní àkọsílẹ̀) | Section header | ☐ |


## Result Legend

| Key | English | Yorùbá | Where shown | Approval |
| --- | --- | --- | --- | --- |
| `legend_title` | Result Legend | Ìtumọ̀ àwọn àbájáde | Legend block heading | ☐ |
| `legend_emergency_title` | Emergency | Pàjáwìrì | Emergency item title | ☐ |
| `legend_emergency_desc` | Immediate veterinary help | Ìrànlọ́wọ́ dókítà ẹranko lẹ́sẹ̀kẹsẹ | Emergency item description | ☐ |
| `legend_act_title` | Act Now | Ṣe Ìgbésẹ̀ Báyìí | Act Now item title | ☐ |
| `legend_act_desc` | Take action soon | Ṣe ohun kan láìpẹ́ | Act Now item description | ☐ |
| `legend_keep_title` | Keep Monitoring | Máa Ṣọ́ | Keep Monitoring item title | ☐ |
| `legend_keep_desc` | Continue monitoring | Máa bá ìṣàyẹ̀wò lọ | Keep Monitoring item description | ☐ |
| `legend_disclaimer` | Triage only, not diagnosis or prescription. | Ìtọ́nisọ́nà nìkan, kì í ṣe ìdánimọ̀ àrùn tàbí ìpàṣẹ oogun. | Disclaimer below legend | ☐ |


## Result card content

| Key | English | Yorùbá | Where shown | Approval |
| --- | --- | --- | --- | --- |
| `result_title_emergency` | EMERGENCY | PÀJÁWÌRÌ | Big card title at Emergency | ☐ |
| `result_title_act_now` | ACT NOW | ṢE ÌGBÉSẸ̀ BÁYÌÍ | Big card title at Act Now | ☐ |
| `result_title_keep_mon` | KEEP MONITORING | MÁA ṢỌ́ | Big card title at Keep Monitoring | ☐ |
| `result_subtitle_emergency` | Contact a veterinarian immediately. | Pe dókítà ẹranko lẹ́sẹ̀kẹsẹ. | Subtitle under Emergency card title | ☐ |
| `result_subtitle_act_now` | Take action and contact a veterinarian soon. | Ṣe ìgbésẹ̀ kí o sì pe dókítà ẹranko láìpẹ́. | Subtitle under Act Now card title | ☐ |
| `result_subtitle_keep_mon` | No immediate action needed. | Kò sí ìgbésẹ̀ kíákíá tí a nílò. | Subtitle under Keep Monitoring card title | ☐ |
| `result_msg_emergency` | Your flock shows a danger sign that needs urgent veterinary attention. This is triage, not a diagnosis. Do not self-medicate. Isolate visibly sick birds and document droppings if possible. | Àwọn adìẹ rẹ ní àmì ewu tó nílò ìrànlọ́wọ́ dókítà ẹranko kíákíá. Èyí jẹ́ ìtọ́nisọ́nà, kì í ṣe ìdánimọ̀ àrùn. Má ṣe fi oogun fún ara rẹ. Yà àwọn adìẹ tí ó ń ṣàìsàn sílẹ̀, ya àwòrán ìgbẹ́ wọn bí ó bá ṣeé ṣe. | Full Emergency body message to farmer | ☐ |
| `result_msg_act_now` | Your answers suggest your flock is at risk of coccidiosis. Remove wet litter, isolate sick birds, fix leaking drinkers, and contact a veterinary officer or approved agro-vet. Do not self-medicate with antibiotics. | Ìdáhùn rẹ fihàn pé àwọn adìẹ rẹ wà nínú ewu coccidiosis. Yọ ohun tí wọ́n fi bo ilẹ̀ ilé adìẹ tí ó tutu kúrò. Yà àwọn adìẹ tí ó ń ṣàìsàn sílẹ̀. Tún ohun mímu omi tí ń jo ṣe. Pe dókítà ẹranko, vet, tàbí agro-vet tí a fọwọ́ sí. Má ṣe lo antibiotics láì gba ìmọ̀ràn. | Full Act Now body message to farmer | ☐ |
| `result_msg_keep_mon` | No red-flag coccidiosis pattern detected today. Maintain dry litter, biosecurity, clean water, and recheck droppings, feed, and water tomorrow. This is triage, not a diagnosis. | Kò sí àpẹẹrẹ ewu coccidiosis tó lágbára tó hàn lónìí. Jẹ́ kí ohun tí wọ́n fi bo ilẹ̀ ilé adìẹ máa gbẹ. Pa ààbò ilé adìẹ mọ́. Pèsè omi mímọ́. Tún ṣàyẹ̀wò ìgbẹ́, oúnjẹ, àti omi wọn lọ́la. Èyí jẹ́ ìtọ́nisọ́nà, kì í ṣe ìdánimọ̀ àrùn. | Full Keep Monitoring body message to farmer | ☐ |
| `decision_reached` | Decision reached after {n} of 14 possible questions. | Ìpinnu dé lẹ́yìn ìbéèrè {n} nínú àwọn ìbéèrè 14 tó ṣeé ṣe. | Stat line, {n} is replaced at render time | ☐ |
| `early_stopping_reason_label` | Early stopping reason | Ìdí ìdúró kíákíá | Stat row label, value is internal code | ☐ |


## Per-question helper notes (only emergency-screen questions show these)

| Key | English | Yorùbá | Where shown | Approval |
| --- | --- | --- | --- | --- |
| `helper_fresh_blood` | This is the first check for danger signs. | Èyí ni ìṣàyẹ̀wò àkọ́kọ́ fún àmì ewu. | Blue info note shown with Q1 | ☐ |
| `helper_orange_mucus` | Orange mucus or sloughed tissue is a serious warning sign. | Ohun alálẹ̀mọ́ aláwọ̀ ọ́sàn jẹ́ àmì ewu tó lágbára. | Blue info note shown with Q2 | ☐ |
| `helper_mortality` | Sudden flock death needs urgent attention. | Ikú adìẹ lojijì nílò ìgbésẹ̀ kíákíá. | Blue info note shown with Q12 (asked 3rd) | ☐ |
| `helper_droppings` | Droppings consistency tells us a lot about flock health. | Bí ìgbẹ́ ṣe rí ń sọ ọ̀pọ̀ nípa ìlera adìẹ. | Blue info note shown with Q3 (asked 4th) | ☐ |


## B. The 14 questions

Each question table has three sub-rows: the question text itself, then one row per answer option. The `Internal code` column shows what the engine sees regardless of language; the engine never reads the English or Yorùbá display text.


### Q1 (`fresh_blood`)

| Row ID | Kind | English | Yorùbá | Internal code | Approval |
| --- | --- | --- | --- | --- | --- |
| Q1.q | *question text* | Are there visible signs of fresh blood in the droppings? | Ṣé ẹ̀jẹ̀ pupa tí ó dà bí tuntun hàn nínú ìgbẹ́ àwọn adìẹ? | n/a | ☐ |
| Q1.true.text | option label | Yes | Bẹ́ẹ̀ni | `true` | ☐ |
| Q1.true.desc | option helper line | There is fresh blood. | Ẹ̀jẹ̀ tuntun wà. | `true` | ☐ |
| Q1.false.text | option label | No | Rárá | `false` | ☐ |
| Q1.false.desc | option helper line | No fresh blood visible. | Ẹ̀jẹ̀ tuntun kò hàn. | `false` | ☐ |



### Q2 (`orange_mucus`)

| Row ID | Kind | English | Yorùbá | Internal code | Approval |
| --- | --- | --- | --- | --- | --- |
| Q2.q | *question text* | Is there orange mucus or sloughed intestinal tissue present? | Ṣé ohun alálẹ̀mọ́ aláwọ̀ ọ́sàn, tàbí nkan bí ẹran inú, hàn nínú ìgbẹ́ àwọn adìẹ? | n/a | ☐ |
| Q2.true.text | option label | Yes | Bẹ́ẹ̀ni | `true` | ☐ |
| Q2.true.desc | option helper line | Orange mucus or tissue visible. | Ohun aláwọ̀ ọ́sàn hàn. | `true` | ☐ |
| Q2.false.text | option label | No | Rárá | `false` | ☐ |
| Q2.false.desc | option helper line | Droppings look normal in color. | Àwọ̀ ìgbẹ́ jọ́ bí ti deede. | `false` | ☐ |



### Q12 (asked 3rd in adaptive flow) (`mortality`)

| Row ID | Kind | English | Yorùbá | Internal code | Approval |
| --- | --- | --- | --- | --- | --- |
| Q12 (asked 3rd in adaptive flow).q | *question text* | Has daily mortality exceeded the expected baseline for this age? | Ṣé iye adìẹ tí ń kú lojoojúmọ́ ti pọ̀ ju ohun tí o máa ń retí lọ? | n/a | ☐ |
| Q12 (asked 3rd in adaptive flow).none.text | option label | No | Rárá | `Mort.NONE` | ☐ |
| Q12 (asked 3rd in adaptive flow).none.desc | option helper line | Mortality is normal for this age. | Ikú adìẹ wà ní deede. | `Mort.NONE` | ☐ |
| Q12 (asked 3rd in adaptive flow).gradual.text | option label | Gradual increase | Ó ń pọ̀ sí i díẹ̀díẹ̀ | `Mort.GRADUAL` | ☐ |
| Q12 (asked 3rd in adaptive flow).gradual.desc | option helper line | Slightly more deaths than usual. | Ikú díẹ̀ ju ti deede lọ. | `Mort.GRADUAL` | ☐ |
| Q12 (asked 3rd in adaptive flow).sudden_spike.text | option label | Sudden spike | Ó pọ̀ sí i lojijì | `Mort.SUDDEN_SPIKE` | ☐ |
| Q12 (asked 3rd in adaptive flow).sudden_spike.desc | option helper line | Many deaths in a short time. | Adìẹ púpọ̀ kú nínú àkókò kúkúrú. | `Mort.SUDDEN_SPIKE` | ☐ |



### Q3 (asked 4th in adaptive flow) (`droppings`)

| Row ID | Kind | English | Yorùbá | Internal code | Approval |
| --- | --- | --- | --- | --- | --- |
| Q3 (asked 4th in adaptive flow).q | *question text* | What is the predominant consistency of the droppings? | Báwo ni ìgbẹ́ àwọn adìẹ ṣe rí jù lọ? | n/a | ☐ |
| Q3 (asked 4th in adaptive flow).normal.text | option label | Normal, firm | Ó dáa, ó sì ní ìdúró | `Droppings.NORMAL` | ☐ |
| Q3 (asked 4th in adaptive flow).normal.desc | option helper line | Solid, well-formed droppings. | Ìgbẹ́ le, ó dáa. | `Droppings.NORMAL` | ☐ |
| Q3 (asked 4th in adaptive flow).loose.text | option label | Loose | Ó rọ̀ | `Droppings.LOOSE` | ☐ |
| Q3 (asked 4th in adaptive flow).loose.desc | option helper line | Softer than usual but not watery. | Ó rọ̀ díẹ̀ ju ti deede lọ. | `Droppings.LOOSE` | ☐ |
| Q3 (asked 4th in adaptive flow).severe_diarrhea.text | option label | Severe diarrhea | Ó dà bí omi púpọ̀, ìgbẹ́ gbuuru tó le | `Droppings.SEVERE_DIARRHEA` | ☐ |
| Q3 (asked 4th in adaptive flow).severe_diarrhea.desc | option helper line | Very watery, mostly liquid. | Ó dà bí omi gan-an. | `Droppings.SEVERE_DIARRHEA` | ☐ |



### Q4 (`hunched`)

| Row ID | Kind | English | Yorùbá | Internal code | Approval |
| --- | --- | --- | --- | --- | --- |
| Q4.q | *question text* | Are birds exhibiting a hunched posture with ruffled feathers? | Ṣé àwọn adìẹ ń wọ́ ara wọn sílẹ̀, tí ìyẹ́ wọn sì ń rú? | n/a | ☐ |
| Q4.widespread.text | option label | Widespread, over 10% of flock | Bẹ́ẹ̀ni, ó pọ̀ ju 10% lọ | `Hunched.WIDESPREAD` | ☐ |
| Q4.widespread.desc | option helper line | Many birds are affected. | Àwọn adìẹ púpọ̀ ni ó kàn. | `Hunched.WIDESPREAD` | ☐ |
| Q4.isolated.text | option label | Isolated, under 10% of flock | Díẹ̀ nìkan, kéré ju 10% lọ | `Hunched.ISOLATED` | ☐ |
| Q4.isolated.desc | option helper line | Only a few birds are affected. | Adìẹ díẹ̀ nìkan ni ó kàn. | `Hunched.ISOLATED` | ☐ |
| Q4.none.text | option label | None | Rárá | `Hunched.NONE` | ☐ |
| Q4.none.desc | option helper line | Birds look alert and active. | Àwọn adìẹ wà ní ìjọ́gun dáadáa. | `Hunched.NONE` | ☐ |



### Q5 (`huddling`)

| Row ID | Kind | English | Yorùbá | Internal code | Approval |
| --- | --- | --- | --- | --- | --- |
| Q5.q | *question text* | Are birds huddling together despite adequate ambient temperatures? | Ṣé àwọn adìẹ ń kó ara wọn jọ bí ẹni pé òtútù ń mú wọn, bó tilẹ̀ jẹ́ pé ilé adìẹ kò tútù? | n/a | ☐ |
| Q5.true.text | option label | Yes | Bẹ́ẹ̀ni | `true` | ☐ |
| Q5.true.desc | option helper line | Birds are clumping even though it is warm. | Wọ́n ń kó ara wọn jọ pẹ̀lú òtútù. | `true` | ☐ |
| Q5.false.text | option label | No | Rárá | `false` | ☐ |
| Q5.false.desc | option helper line | Birds are spread out normally. | Wọ́n túká dáadáa. | `false` | ☐ |



### Q6 (`paleness`)

| Row ID | Kind | English | Yorùbá | Internal code | Approval |
| --- | --- | --- | --- | --- | --- |
| Q6.q | *question text* | Is there noticeable paleness or depigmentation in the skin, shanks, or combs? | Ṣé awọ ara, ẹsẹ̀, tàbí àpá pupa lórí àwọn adìẹ ti ń pálẹ̀ ju bó ṣe yẹ lọ? | n/a | ☐ |
| Q6.true.text | option label | Yes | Bẹ́ẹ̀ni | `true` | ☐ |
| Q6.true.desc | option helper line | Skin or combs look pale. | Awọ tàbí àpá pupa pálẹ̀. | `true` | ☐ |
| Q6.false.text | option label | No | Rárá | `false` | ☐ |
| Q6.false.desc | option helper line | Color looks normal. | Àwọ̀ jọ́ bí ti deede. | `false` | ☐ |



### Q7 (`feed`)

| Row ID | Kind | English | Yorùbá | Internal code | Approval |
| --- | --- | --- | --- | --- | --- |
| Q7.q | *question text* | How has daily feed intake changed over the last 48 hours? | Báwo ni iye oúnjẹ tí àwọn adìẹ ń jẹ ṣe yí padà ní ọjọ́ méjì sẹ́yìn? | n/a | ☐ |
| Q7.at_or_above.text | option label | At or above target | Wọ́n ń jẹun bó ṣe yẹ tàbí ju bẹ́ẹ̀ lọ | `Feed.AT_OR_ABOVE` | ☐ |
| Q7.at_or_above.desc | option helper line | Birds are eating normally. | Wọ́n ń jẹun bí ti deede. | `Feed.AT_OR_ABOVE` | ☐ |
| Q7.slight_drop.text | option label | Slight drop, under 10% | Wọ́n ń jẹun díẹ̀ kere ju ti tẹ́lẹ̀ lọ | `Feed.SLIGHT_DROP` | ☐ |
| Q7.slight_drop.desc | option helper line | Eating a little less than usual. | Wọ́n ń jẹun díẹ̀. | `Feed.SLIGHT_DROP` | ☐ |
| Q7.significant_drop.text | option label | Significant drop, over 10% | Wọ́n ń jẹun púpọ̀ kere ju ti tẹ́lẹ̀ lọ | `Feed.SIGNIFICANT_DROP` | ☐ |
| Q7.significant_drop.desc | option helper line | Eating much less than usual. | Wọ́n kò jẹun rárá. | `Feed.SIGNIFICANT_DROP` | ☐ |



### Q8 (`water`)

| Row ID | Kind | English | Yorùbá | Internal code | Approval |
| --- | --- | --- | --- | --- | --- |
| Q8.q | *question text* | How has daily water consumption changed? | Báwo ni mímu omi àwọn adìẹ ṣe yí padà? | n/a | ☐ |
| Q8.normal.text | option label | Normal | Deede | `Water.NORMAL` | ☐ |
| Q8.normal.desc | option helper line | Birds are drinking as usual. | Wọ́n ń mu omi bí ti deede. | `Water.NORMAL` | ☐ |
| Q8.slight.text | option label | Slight drop | Wọ́n ń mu omi díẹ̀ kere ju ti tẹ́lẹ̀ lọ | `Water.SLIGHT` | ☐ |
| Q8.slight.desc | option helper line | Drinking a little less than usual. | Mímu omi dín kù díẹ̀. | `Water.SLIGHT` | ☐ |
| Q8.significant.text | option label | Significant drop | Wọ́n ń mu omi púpọ̀ kere ju ti tẹ́lẹ̀ lọ | `Water.SIGNIFICANT` | ☐ |
| Q8.significant.desc | option helper line | Drinking much less than usual. | Mímu omi dín kù púpọ̀. | `Water.SIGNIFICANT` | ☐ |



### Q9 (`age`)

| Row ID | Kind | English | Yorùbá | Internal code | Approval |
| --- | --- | --- | --- | --- | --- |
| Q9.q | *question text* | What is the current age of the flock? | Ọmọ ọ̀sẹ̀ mélòó ni àwọn adìẹ wọ̀nyí? | n/a | ☐ |
| Q9.under_3w.text | option label | Less than 3 weeks | Kéré ju ọ̀sẹ̀ mẹ́ta lọ | `Age.UNDER_3W` | ☐ |
| Q9.under_3w.desc | option helper line | Very young chicks. | Àwọn ọmọ kéékèèké. | `Age.UNDER_3W` | ☐ |
| Q9.three_to_8w.text | option label | 3 to 8 weeks | Láàárín ọ̀sẹ̀ mẹ́ta sí mẹ́jọ | `Age.THREE_TO_8W` | ☐ |
| Q9.three_to_8w.desc | option helper line | Growing birds. | Àwọn adìẹ tí ń dàgbà. | `Age.THREE_TO_8W` | ☐ |
| Q9.over_8w.text | option label | More than 8 weeks | Ju ọ̀sẹ̀ mẹ́jọ lọ | `Age.OVER_8W` | ☐ |
| Q9.over_8w.desc | option helper line | Older birds. | Àwọn adìẹ àgbà. | `Age.OVER_8W` | ☐ |



### Q10 (`vacc`)

| Row ID | Kind | English | Yorùbá | Internal code | Approval |
| --- | --- | --- | --- | --- | --- |
| Q10.q | *question text* | Was the flock vaccinated for coccidiosis at the hatchery? | Níbi tí wọ́n ti yọ àwọn adìẹ náà, ṣé wọ́n fún wọn ní ajẹsára lòdì sí coccidiosis? | n/a | ☐ |
| Q10.yes.text | option label | Yes | Bẹ́ẹ̀ni | `Vacc.YES` | ☐ |
| Q10.yes.desc | option helper line | Vaccination confirmed. | A fún wọn ní ajẹsára. | `Vacc.YES` | ☐ |
| Q10.no.text | option label | No | Rárá | `Vacc.NO` | ☐ |
| Q10.no.desc | option helper line | Not vaccinated. | A kò fún wọn ní ajẹsára. | `Vacc.NO` | ☐ |
| Q10.unknown.text | option label | Unknown | Mi ò mọ̀ | `Vacc.UNKNOWN` | ☐ |
| Q10.unknown.desc | option helper line | Not sure about vaccination. | Mi kò mọ̀ àfojúsùn ajẹsára. | `Vacc.UNKNOWN` | ☐ |



### Q11 (`coccidiostat`)

| Row ID | Kind | English | Yorùbá | Internal code | Approval |
| --- | --- | --- | --- | --- | --- |
| Q11.q | *question text* | Is the flock currently on a dietary coccidiostat program in the feed? | Ṣé oúnjẹ tí o ń fún àwọn adìẹ ní ohun ìdènà coccidiosis nínú rẹ̀ báyìí? | n/a | ☐ |
| Q11.true.text | option label | Yes | Bẹ́ẹ̀ni | `true` | ☐ |
| Q11.true.desc | option helper line | Coccidiostat is in the feed. | Ohun ìdènà wà nínú oúnjẹ. | `true` | ☐ |
| Q11.false.text | option label | No | Rárá | `false` | ☐ |
| Q11.false.desc | option helper line | No coccidiostat in the feed. | Kò sí ohun ìdènà nínú oúnjẹ. | `false` | ☐ |



### Q13 (`litter`)

| Row ID | Kind | English | Yorùbá | Internal code | Approval |
| --- | --- | --- | --- | --- | --- |
| Q13.q | *question text* | What is the overall physical condition of the litter? | Báwo ni ohun tí wọ́n fi bo ilẹ̀ ilé adìẹ ṣe rí lápapọ̀? | n/a | ☐ |
| Q13.dry.text | option label | Dry and friable | Ó gbẹ, ó sì tú dáadáa | `Litter.DRY` | ☐ |
| Q13.dry.desc | option helper line | Litter is dry and loose. | Ó gbẹ, kò tutu. | `Litter.DRY` | ☐ |
| Q13.damp.text | option label | Damp | Ó tutu díẹ̀ | `Litter.DAMP` | ☐ |
| Q13.damp.desc | option helper line | Litter has some wetness. | Ó ní omi díẹ̀ nínú. | `Litter.DAMP` | ☐ |
| Q13.heavily_caked_wet.text | option label | Heavily caked and wet | Ó dì pọ̀, ó sì tutu gan-an | `Litter.HEAVILY_CAKED_WET` | ☐ |
| Q13.heavily_caked_wet.desc | option helper line | Litter is wet and stuck together. | Ó tutu gan-an, ó sì dì pọ̀. | `Litter.HEAVILY_CAKED_WET` | ☐ |



### Q14 (`leaking_drinkers`)

| Row ID | Kind | English | Yorùbá | Internal code | Approval |
| --- | --- | --- | --- | --- | --- |
| Q14.q | *question text* | Are there misaligned or leaking drinkers creating localized wet spots? | Ṣé omi ń jo láti inú ohun tí adìẹ fi ń mu omi, tàbí ohun náà kò dúró dáadáa, tó sì ń mú kí ìtẹ́ adìẹ tutu ní àwọn ibi kan? | n/a | ☐ |
| Q14.true.text | option label | Yes | Bẹ́ẹ̀ni | `true` | ☐ |
| Q14.true.desc | option helper line | Drinkers are leaking or off-position. | Omi ń jo. | `true` | ☐ |
| Q14.false.text | option label | No | Rárá | `false` | ☐ |
| Q14.false.desc | option helper line | Drinkers are working properly. | Ohun mímu omi ń ṣiṣẹ́ dáadáa. | `false` | ☐ |



---

## How approval works

1. Tick `☐` to `☑` on every row you approve.
2. For any row that needs revision, replace the Yorùbá text in `prototype/src/i18n.yo.js` directly.
3. Re-run `python prototype/generate_yoruba_review.py` so this file is regenerated from the new wording.
4. Re-run `python prototype/build.py` so `prototype/coccialert_live_demo.html` is rebuilt with the new Yorùbá.
5. Re-run `node prototype/src/test_adaptive_demo.js` to confirm the 6 scenarios still pass.

Once every row is `☑`, this file is the approval record and the demo Yorùbá is signed off.
