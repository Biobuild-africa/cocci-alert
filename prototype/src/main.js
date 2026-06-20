// =============================================================================
// CocciAlert main UI module
//
// SCOPE OF THIS FILE
//   Session state, render functions, controller wiring, boot. The DOM-touching
//   layer. Reads from i18n_en, i18n_yo, SCHEMA, DEMO_SCENARIOS, and the
//   engine/controller functions, but never declares them.
//
// WHAT TO EDIT WHERE
//   - All wording lives in src/i18n.en.js and src/i18n.yo.js.
//   - Demo button scenarios live in src/demo_scenarios.js.
//   - Clinical rules live in src/engine.js.
//   - Layout/CSS lives in src/styles.css.
// =============================================================================

const i18n = { en: i18n_en, yo: i18n_yo };

const ENGINE_VERSION = "0.1.0";
const SCHEMA_VERSION = "1.0";

// Per-question helper text lookup (only emergency-screen questions get one)
function getHelperText(L, key) {
  if (key === "fresh_blood")  return L.helper_fresh_blood;
  if (key === "orange_mucus") return L.helper_orange_mucus;
  if (key === "mortality")    return L.helper_mortality;
  if (key === "droppings")    return L.helper_droppings;
  return null;
}

// ----- Session state -----

const state = {
  lang: "en",
  answers: {},
  decision: null,          // null while collecting; populated when engine decides
  questionsAsked: [],      // ordered list of question keys
  sessionId: "DEMO-" + Math.random().toString(36).slice(2, 7).toUpperCase(),
  consentTimeISO: new Date().toISOString(),
  finished: false,
  // Pass 2 audio flag. Sound is OFF by default per spec; user gesture turns
  // it on via the top-bar toggle. The Audio module owns its own state too;
  // we track it here so renderers can update visual indicators.
  soundOn: false
};

function t() { return i18n[state.lang]; }
function esc(s) {
  if (s === null || s === undefined) return "";
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")
                   .replace(/"/g,"&quot;").replace(/'/g,"&#39;");
}

// ----- Render -----

function render() {
  renderNav();
  renderLeftPanel();
  renderCenterPanel();
  renderRightPanel();
}

function renderNav() {
  const L = t();
  document.getElementById("nav-title").textContent = L.nav_title;
  document.getElementById("nav-subtitle").textContent = L.nav_subtitle;
  document.getElementById("demo-emergency-btn").textContent = L.demo_emergency;
  document.getElementById("demo-act-now-btn").textContent = L.demo_act_now;
  document.getElementById("demo-keep-mon-btn").textContent = L.demo_keep_mon;
  // Pass 2: sound toggle reflects current state and the speaker/mute icon flips
  const soundLabel = state.soundOn ? L.sound_on : L.sound_off;
  const soundIcon  = state.soundOn ? "🔊" : "🔇";
  document.getElementById("sound-toggle").innerHTML = soundIcon + " " + esc(soundLabel);
  document.getElementById("sound-toggle").classList.toggle("on", state.soundOn);
  document.getElementById("restart-btn").innerHTML = "↺ " + esc(L.restart);
  document.getElementById("lang-en-btn").classList.toggle("active", state.lang === "en");
  document.getElementById("lang-yo-btn").classList.toggle("active", state.lang === "yo");
  // Footer audio note: bilingual, updated on every render
  const footerNote = document.getElementById("footer-audio-note");
  if (footerNote) footerNote.textContent = L.footer_audio_note;
  // Yoruba-voice fallback banner: visible only when Yoruba is selected,
  // sound is on, and the browser has no Yoruba voice loaded.
  renderYorubaVoiceNote(L);
}

function renderYorubaVoiceNote(L) {
  const banner = document.getElementById("yoruba-voice-banner");
  if (!banner) return;
  const yoSelected = state.lang === "yo";
  const yoVoice = Audio.isYorubaVoiceAvailable();
  // Show only when Yoruba selected, sound on, and voice missing or unknown=false
  const shouldShow = yoSelected && state.soundOn && yoVoice === false;
  banner.style.display = shouldShow ? "" : "none";
  banner.textContent = L.yoruba_voice_unavailable;
}

function renderLeftPanel() {
  const L = t();
  document.getElementById("panel-left-title").textContent = L.panel_left_title;
  document.getElementById("phone-header-sub").textContent = L.phone_header_sub;
  document.getElementById("phone-session-id").textContent = state.sessionId;
  // Phone sound label tracks the actual top-bar sound state
  document.getElementById("phone-sound-label").textContent = state.soundOn ? L.phone_sound_on : L.phone_sound;
  document.getElementById("phone-replay-label").textContent = L.phone_replay;

  const body = document.getElementById("phone-body");
  body.innerHTML = "";
  body.appendChild(makeBubble("bot", L.phone_welcome, "10:30"));

  state.questionsAsked.forEach((qKey, idx) => {
    const qLoc = L.questions[qKey];
    const answer = state.answers[qKey];
    const optLabel = qLoc.opts[String(answer)].text;
    const num = idx + 1;
    body.appendChild(makeBubble("bot-q", "Q" + num + ". " + qLoc.q, "10:3" + (1+idx)));
    body.appendChild(makeBubble("user", optLabel, "10:3" + (1+idx)));
  });

  if (state.finished && state.decision) {
    const titleKey = "result_title_" + outcomeShortKey(state.decision.outcome);
    body.appendChild(makeBubble("bot", "→ " + L[titleKey], "10:40"));
  } else if (!state.finished) {
    const next = pickNextQuestion(state.answers);
    if (next) {
      const qLoc = L.questions[next.key];
      const num = state.questionsAsked.length + 1;
      const optsHtml = SCHEMA.find(s => s.key === next.key).options.map((opt, i) => {
        const text = qLoc.opts[String(opt.code)].text;
        return '<div class="phone-opt">' + (i+1) + ". " + esc(text) + "</div>";
      }).join("");
      const wrap = document.createElement("div");
      wrap.appendChild(makeBubble("bot-q", "Q" + num + ". " + qLoc.q, "10:3" + Math.min(9, num)));
      const optsDiv = document.createElement("div");
      optsDiv.className = "phone-options";
      optsDiv.innerHTML = optsHtml;
      wrap.appendChild(optsDiv);
      body.appendChild(wrap);
    }
  }

  body.scrollTop = body.scrollHeight;
}

function makeBubble(klass, text, ts) {
  const div = document.createElement("div");
  div.className = "bubble " + klass;
  div.innerHTML = esc(text) + '<span class="ts">' + esc(ts) + " AM</span>";
  return div;
}

function renderCenterPanel() {
  const L = t();
  const panel = document.getElementById("center-panel");

  if (state.finished && state.decision) {
    panel.innerHTML = renderResultHtml(L);
    // Pass 2 wiring: play tone + read result message when sound is on.
    // Tone choice and timing live in audio.js, not here.
    if (state.soundOn) {
      const okey = outcomeShortKey(state.decision.outcome);
      const msg = L["result_msg_" + okey];
      // small delay so the visual result lands before audio
      setTimeout(() => Audio.readResult(okey, msg, state.lang), 150);
    }
    return;
  }

  const next = pickNextQuestion(state.answers);
  if (!next) {
    panel.innerHTML = '<div class="panel-title">' + esc(L.stage_result) + '</div>';
    return;
  }

  const qLoc = L.questions[next.key];
  const schemaItem = SCHEMA.find(s => s.key === next.key);
  const helper = getHelperText(L, next.key);
  const totalQ = SCHEMA.length;
  const askedSoFar = state.questionsAsked.length;
  const pct = Math.round((askedSoFar / totalQ) * 100);
  const questionNum = askedSoFar + 1;

  const stageBadgeClass = next.stage === "emergency" ? "emergency" : "supporting";
  const stageBadgeLabel = next.stage === "emergency" ? L.badge_emergency : L.badge_supporting;

  const stageActiveIdx = next.stage === "emergency" ? 0 : 1;
  const stagesHtml = ['emergency','supporting','result'].map((s, i) => {
    const label = i === 0 ? L.stage_emergency : i === 1 ? L.stage_supporting : L.stage_result;
    const active = i === stageActiveIdx ? "active" : "";
    return '<div class="stage ' + active + '"><div class="stage-num">' + (i+1) + '</div>' + esc(label) + '</div>' +
           (i < 2 ? '<span class="stage-arrow">›</span>' : '');
  }).join("");

  const optsHtml = schemaItem.options.map((opt, i) => {
    const optLoc = qLoc.opts[String(opt.code)];
    return '<button class="q-opt" data-i="' + i + '">' +
           '  <div class="q-opt-num ' + opt.accent + '">' + (i+1) + '</div>' +
           '  <div>' +
           '    <div class="q-opt-text">' + esc(optLoc.text) + '</div>' +
           '    <div class="q-opt-desc">' + esc(optLoc.desc) + '</div>' +
           '  </div>' +
           '</button>';
  }).join("");

  panel.innerHTML =
    '<div class="progress-row">' +
    '  <span class="progress-label">' + esc(L.progress) + '</span>' +
    '  <span class="progress-count">' + esc(L.question_n_of_14.replace("{n}", questionNum)) + '</span>' +
    '</div>' +
    '<div class="progress-bar"><div class="progress-bar-fill" style="width:' + pct + '%;"></div></div>' +
    '<div class="progress-pct">' + pct + '%</div>' +
    '<div class="stages">' + stagesHtml + '</div>' +
    '<div class="stage-badge ' + stageBadgeClass + '">' + esc(stageBadgeLabel) + '</div>' +
    '<div class="q-text">Q' + questionNum + '. ' + esc(qLoc.q) + '</div>' +
    (helper ? '<div class="q-helper"><span class="q-helper-icon">ℹ</span><span>' + esc(helper) + '</span></div>' : '') +
    '<div class="q-options">' + optsHtml + '</div>' +
    '<div class="replay-row">' +
    '  <button class="replay-pill replay-btn ' + (state.soundOn ? 'active' : 'inactive') + '" id="listen-btn" type="button">🔊 ' + esc(state.soundOn ? L.audio_listen_now : L.tap_to_hear) + '</button>' +
    '  <button class="replay-pill replay-btn ' + (state.soundOn ? 'active' : 'inactive') + '" id="replay-btn-q" type="button">↺ ' + esc(L.replay_question) + '</button>' +
    '</div>' +
    '<div class="early-stop-note">' +
    '  <span>💡</span><span>' + esc(L.early_stop_note) + '</span>' +
    '</div>';

  panel.querySelectorAll(".q-opt").forEach(b => {
    b.addEventListener("click", () => onAnswer(next.key, schemaItem.options[parseInt(b.dataset.i,10)].code));
  });
  // Pass 2 wiring: Listen and Replay both read the current question text.
  // No-op when sound is off (Audio.readQuestion returns false silently).
  const onReplay = () => {
    if (state.soundOn) Audio.readQuestion(qLoc.q, state.lang);
  };
  const listenEl = panel.querySelector("#listen-btn");
  const replayEl = panel.querySelector("#replay-btn-q");
  if (listenEl) listenEl.addEventListener("click", onReplay);
  if (replayEl) replayEl.addEventListener("click", onReplay);

  // Auto-read the question once on render when sound is on. The small delay
  // lets the visual update register first.
  if (state.soundOn) {
    setTimeout(() => Audio.readQuestion(qLoc.q, state.lang), 200);
  }
}

function outcomeShortKey(outcome) {
  if (outcome === Triage.EMERGENCY) return "emergency";
  if (outcome === Triage.ACT_NOW) return "act_now";
  return "keep_mon";
}

function renderResultHtml(L) {
  const r = state.decision;
  const okey = outcomeShortKey(r.outcome);
  const titleClass = okey === "emergency" ? "emergency" : okey === "act_now" ? "act-now" : "keep-mon";
  const icon = okey === "emergency" ? "⚠" : okey === "act_now" ? "⚠" : "✓";
  const title = L["result_title_" + okey];
  const subtitle = L["result_subtitle_" + okey];
  const msg = L["result_msg_" + okey];
  const askedCount = state.questionsAsked.length;
  const decisionLine = L.decision_reached.replace("{n}", askedCount);

  return '' +
    '<div class="stage-badge result">' + esc(L.badge_result) + '</div>' +
    '<div class="result-card">' +
    '  <div class="result-card-header ' + titleClass + '">' +
    '    <div class="result-icon">' + icon + '</div>' +
    '    <div>' +
    '      <div class="result-title">' + esc(title) + '</div>' +
    '      <div class="result-subtitle">' + esc(subtitle) + '</div>' +
    '    </div>' +
    '  </div>' +
    '  <div class="result-body">' +
    '    <div class="result-message">' + esc(msg) + '</div>' +
    '    <div class="result-stat">' +
    '      <span class="result-stat-label">' + esc(decisionLine) + '</span>' +
    '    </div>' +
    '    <div class="result-stat">' +
    '      <span class="result-stat-label">' + esc(L.early_stopping_reason_label) + '</span>' +
    '      <span class="result-stat-value">' + esc(r.reason_code) + '</span>' +
    '    </div>' +
    '    <div class="result-stat">' +
    '      <span class="result-stat-label">' + esc(L.questions_answered) + '</span>' +
    '      <span class="result-stat-value">' + askedCount + " / 14" + '</span>' +
    '    </div>' +
    '    <div class="result-disclaimer">' + esc(L.legend_disclaimer) + '</div>' +
    '  </div>' +
    '</div>';
}

function renderRightPanel() {
  const L = t();
  document.getElementById("panel-right-title").textContent = L.panel_right_title;
  document.getElementById("legend-title").textContent = L.legend_title;
  document.getElementById("legend-emergency-title").textContent = L.legend_emergency_title;
  document.getElementById("legend-emergency-desc").textContent = L.legend_emergency_desc;
  document.getElementById("legend-act-title").textContent = L.legend_act_title;
  document.getElementById("legend-act-desc").textContent = L.legend_act_desc;
  document.getElementById("legend-keep-title").textContent = L.legend_keep_title;
  document.getElementById("legend-keep-desc").textContent = L.legend_keep_desc;
  document.getElementById("legend-disclaimer").textContent = L.legend_disclaimer;

  const bp = document.getElementById("backend-preview");
  const langValue = state.lang === "en" ? "English" : "Yorùbá";

  let html = '<div class="bp-section">' +
    '  <div class="bp-section-title">' + esc(L.session_summary) + '</div>' +
    '  <div class="bp-row"><span class="bp-row-label">✓ ' + esc(L.consent_given) + '</span><span class="bp-row-value true">true</span></div>' +
    '  <div class="bp-row"><span class="bp-row-label">🌐 ' + esc(L.language_label) + '</span><span class="bp-row-value">' + esc(langValue) + '</span></div>' +
    '  <div class="bp-row"><span class="bp-row-label">📞 ' + esc(L.raw_phone_stored) + '</span><span class="bp-row-value false">false</span></div>' +
    '  <div class="bp-row"><span class="bp-row-label">📍 ' + esc(L.geography_level) + '</span><span class="bp-row-value">' + esc(L.geography_value) + '</span></div>' +
    '  <div class="bp-row"><span class="bp-row-label">🆔 ' + esc(L.session_id) + '</span><span class="bp-row-value">' + esc(state.sessionId) + '</span></div>' +
    '</div>';

  html += '<div class="bp-section">' +
    '  <div class="bp-section-title">' + esc(L.answers_so_far) + '</div>';
  if (state.questionsAsked.length === 0) {
    html += '<div style="font-size:0.78rem; color: var(--muted); font-style: italic;">' + esc(L.collecting_info) + '</div>';
  } else {
    state.questionsAsked.forEach((qKey, idx) => {
      const ansCode = state.answers[qKey];
      const display = typeof ansCode === "boolean" ? String(ansCode) : '"' + ansCode + '"';
      html += '<div class="bp-answer-row"><span class="bp-answer-q">Q' + (idx+1) + '</span><span>' + esc(qKey) + '</span><span class="bp-answer-eq">=</span><span>' + esc(display) + '</span></div>';
    });
  }
  html += '</div>';

  const askedCount = state.questionsAsked.length;
  let stageLabel, earlyStop, currentAssessment, currentAssessmentClass, rationale;
  if (state.finished && state.decision) {
    const okey = outcomeShortKey(state.decision.outcome);
    stageLabel = L.stage_result;
    earlyStop = L.early_triggered;
    currentAssessment = L["decided_" + okey];
    currentAssessmentClass = "";
    rationale = state.decision.reason_code;
  } else {
    const next = pickNextQuestion(state.answers);
    stageLabel = (next && next.stage === "emergency") ? L.stage_emergency : L.stage_supporting;
    earlyStop = L.early_not_triggered;
    currentAssessment = L.collecting_info;
    currentAssessmentClass = "blue";
    rationale = "—";
  }
  html += '<div class="bp-section">' +
    '  <div class="bp-section-title">' + esc(L.triage_engine_status) + '</div>' +
    '  <div class="bp-row"><span class="bp-row-label">' + esc(L.stage_label) + '</span><span class="bp-row-value">' + esc(stageLabel) + '</span></div>' +
    '  <div class="bp-row"><span class="bp-row-label">' + esc(L.early_stopping) + '</span><span class="bp-row-value">' + esc(earlyStop) + '</span></div>' +
    '  <div class="bp-row"><span class="bp-row-label">' + esc(L.questions_answered) + '</span><span class="bp-row-value">' + askedCount + ' / 14</span></div>' +
    '  <div class="bp-row"><span class="bp-row-label">' + esc(L.rationale) + '</span><span class="bp-row-value">' + esc(rationale) + '</span></div>' +
    '  <div class="bp-row"><span class="bp-row-label">' + esc(L.current_assessment) + '</span><span class="bp-row-value ' + currentAssessmentClass + '">' + esc(currentAssessment) + '</span></div>' +
    '</div>';

  const log = buildEventLogObject();
  html += '<div class="bp-section">' +
    '  <div class="bp-section-title">' + esc(L.event_log_preview) + '</div>' +
    '  <div class="event-log-code">' + formatEventLog(log) + '</div>' +
    '</div>';

  bp.innerHTML = html;
}

function buildEventLogObject() {
  return {
    session_id: state.sessionId,
    timestamp: state.consentTimeISO,
    language_selected: state.lang,
    consent: true,
    raw_phone_stored: false,
    geography_level: "LGA",
    questions_answered_count: state.questionsAsked.length,
    questions_not_asked_due_to_early_stopping: SCHEMA.map(s => s.key).filter(k => !(k in state.answers)),
    triage_outcome: state.decision ? outcomeShortKey(state.decision.outcome) : null,
    triage_rationale_code: state.decision ? state.decision.reason_code : null,
    early_stopping_reason: state.decision ? state.decision.reason_code : null,
    engine_version: ENGINE_VERSION,
    schema_version: SCHEMA_VERSION
  };
}

function formatEventLog(log) {
  function val(v) {
    if (v === null) return '<span class="b">null</span>';
    if (typeof v === "boolean") return '<span class="b">' + v + '</span>';
    if (typeof v === "number") return '<span class="n">' + v + '</span>';
    if (Array.isArray(v)) {
      if (v.length === 0) return '[]';
      return '[' + v.map(x => '<span class="s">"' + esc(x) + '"</span>').join(", ") + ']';
    }
    return '<span class="s">"' + esc(String(v)) + '"</span>';
  }
  const keys = Object.keys(log);
  const lines = keys.map((k, i) => {
    const isLast = i === keys.length - 1;
    return '  <span class="k">"' + k + '"</span>: ' + val(log[k]) + (isLast ? "" : ",");
  });
  return "{\n" + lines.join("\n") + "\n}";
}

// ----- Controller wiring -----

function onAnswer(key, code) {
  state.answers[key] = code;
  state.questionsAsked.push(key);
  state.decision = evaluatePartial(state.answers);
  if (state.decision) state.finished = true;
  render();
}

function runDemo(key) {
  resetState();
  const target = DEMO_SCENARIOS[key];
  let safety = 30;
  while (!state.decision && safety-- > 0) {
    const next = pickNextQuestion(state.answers);
    if (!next) break;
    if (!(next.key in target)) break;
    state.answers[next.key] = target[next.key];
    state.questionsAsked.push(next.key);
    state.decision = evaluatePartial(state.answers);
    if (state.decision) state.finished = true;
  }
  render();
}

function resetState() {
  state.answers = {};
  state.decision = null;
  state.questionsAsked = [];
  state.sessionId = "DEMO-" + Math.random().toString(36).slice(2, 7).toUpperCase();
  state.consentTimeISO = new Date().toISOString();
  state.finished = false;
}

function setLang(lang) {
  state.lang = lang;
  render();
}

// ----- Boot (browser only) -----

if (typeof document !== "undefined") {
  document.getElementById("lang-en-btn").addEventListener("click", () => setLang("en"));
  document.getElementById("lang-yo-btn").addEventListener("click", () => setLang("yo"));
  document.getElementById("demo-emergency-btn").addEventListener("click", () => runDemo("emergency"));
  document.getElementById("demo-act-now-btn").addEventListener("click", () => runDemo("act_now"));
  document.getElementById("demo-keep-mon-btn").addEventListener("click", () => runDemo("keep_monitoring"));
  document.getElementById("restart-btn").addEventListener("click", () => { resetState(); render(); });
  // Pass 2: Sound On/Off toggle. The Audio module handles its own internal
  // state too; we keep state.soundOn in sync so the renderer can update icons.
  document.getElementById("sound-toggle").addEventListener("click", () => {
    state.soundOn = !state.soundOn;
    Audio.setSoundOn(state.soundOn);
    if (!state.soundOn) Audio.stopAllAudio();
    render();
  });
  // Re-render the Yoruba-voice banner whenever the browser finishes loading
  // voices (this often arrives asynchronously after page load).
  window.__onVoicesChanged = () => { if (state.lang === "yo") render(); };
  render();
}
