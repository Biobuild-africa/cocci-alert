// =============================================================================
// CocciAlert audio layer (Pass 2)
//
// SCOPE OF THIS FILE
//   Browser-native text-to-speech (window.speechSynthesis) plus three
//   synthesized tones (Web Audio API OscillatorNode). Nothing here touches
//   engine.js, flow_controller.js, or any clinical logic. Audio is purely
//   additive on top of the existing adaptive flow.
//
// RULES
//   - Sound is OFF by default. The user must turn Sound On before any audio.
//   - Audio uses browser-native APIs only. No external services, no audio
//     files, no CDN dependency.
//   - If Yoruba voice is not present on the device, the Yoruba TEXT still
//     displays correctly; a small fallback note tells the reviewer that
//     Yoruba audio depends on device voice support.
//   - Toggling Sound Off cancels any ongoing speech immediately.
// =============================================================================

const Audio = (function() {

  // ----- Module state -----
  let soundOn = false;
  let yorubaVoiceAvailable = null;   // null until checked, then true/false
  let audioCtx = null;
  let voicesLoaded = false;

  // Web Audio context can only be created after a user gesture; lazy init.
  function ensureAudioContext() {
    if (audioCtx) return audioCtx;
    const Ctor = (typeof window !== "undefined") &&
                 (window.AudioContext || window.webkitAudioContext);
    if (!Ctor) return null;
    audioCtx = new Ctor();
    return audioCtx;
  }

  // ----- Tone synthesis (Web Audio) -----

  function playTone(ctx, freq, when, duration, peakGain, type) {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = type || "sine";
    osc.frequency.value = freq;
    // Short attack, exponential-ish decay for a clean tone with no clicks.
    gain.gain.setValueAtTime(0, when);
    gain.gain.linearRampToValueAtTime(peakGain, when + 0.025);
    gain.gain.linearRampToValueAtTime(0,        when + duration);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start(when);
    osc.stop(when + duration + 0.02);
  }

  // Emergency: two descending notes, serious. ~450ms total.
  function playEmergencyTone() {
    const ctx = ensureAudioContext();
    if (!ctx) return;
    const t = ctx.currentTime;
    playTone(ctx, 659.25, t,        0.20, 0.30, "sine");  // E5
    playTone(ctx, 523.25, t + 0.22, 0.25, 0.30, "sine");  // C5 (descending)
  }

  // Act Now: single warm chime. ~300ms.
  function playActNowTone() {
    const ctx = ensureAudioContext();
    if (!ctx) return;
    const t = ctx.currentTime;
    playTone(ctx, 587.33, t, 0.30, 0.22, "sine");   // D5 warm
  }

  // Keep Monitoring: soft confirmation. ~200ms.
  function playKeepMonTone() {
    const ctx = ensureAudioContext();
    if (!ctx) return;
    const t = ctx.currentTime;
    playTone(ctx, 783.99, t, 0.20, 0.14, "sine");   // G5 soft
  }

  // ----- Speech synthesis -----

  function ttsAvailable() {
    return typeof window !== "undefined" && "speechSynthesis" in window;
  }

  function pickVoice(langCode) {
    if (!ttsAvailable()) return null;
    const voices = window.speechSynthesis.getVoices();
    // langCode is "en" or "yo"
    // Try exact prefix match (e.g., "yo-NG", "en-US", "en-GB")
    const match = voices.find(v => (v.lang || "").toLowerCase().startsWith(langCode.toLowerCase()));
    return match || null;
  }

  function checkYorubaVoice() {
    if (!ttsAvailable()) { yorubaVoiceAvailable = false; return false; }
    const voices = window.speechSynthesis.getVoices();
    // If the browser has not loaded any voices at all yet, OR has loaded
    // voices but none match Yoruba, treat both as "Yoruba audio unavailable"
    // so the fallback banner is shown. If voices later finish loading and
    // a Yoruba voice appears, the voiceschanged listener will flip the flag
    // back to true and the banner is hidden on the next render.
    if (voices.length === 0) {
      yorubaVoiceAvailable = false;
      voicesLoaded = false;
      return false;
    }
    yorubaVoiceAvailable = voices.some(v => (v.lang || "").toLowerCase().startsWith("yo"));
    voicesLoaded = true;
    return yorubaVoiceAvailable;
  }

  function speak(text, langCode) {
    if (!soundOn) return false;
    if (!ttsAvailable()) return false;
    // Cancel any ongoing utterance first.
    window.speechSynthesis.cancel();
    // If Yoruba is requested but no Yoruba voice exists, do NOT fall back to
    // English voice reading Yoruba text. Display fallback note in UI instead.
    if (langCode === "yo") {
      if (yorubaVoiceAvailable === null) checkYorubaVoice();
      if (yorubaVoiceAvailable === false) return false;
    }
    const u = new SpeechSynthesisUtterance(text);
    u.lang = (langCode === "yo") ? "yo-NG" : "en-US";
    u.rate = 0.95;
    u.pitch = 1.0;
    u.volume = 1.0;
    const voice = pickVoice(langCode);
    if (voice) u.voice = voice;
    window.speechSynthesis.speak(u);
    return true;
  }

  // ----- Public API -----

  function setSoundOn(enabled) {
    soundOn = !!enabled;
    if (soundOn) {
      ensureAudioContext();
      if (yorubaVoiceAvailable === null) checkYorubaVoice();
    } else {
      if (ttsAvailable()) window.speechSynthesis.cancel();
    }
  }

  function isSoundOn() { return soundOn; }

  // Returns true / false / null.  null means "voices haven't loaded yet,
  // we don't know yet". UI should re-query after the voiceschanged event.
  function isYorubaVoiceAvailable() { return yorubaVoiceAvailable; }

  // Read a question (or any short text) in the chosen language. Idempotent
  // when sound is off (returns false silently).
  function readQuestion(text, langCode) {
    return speak(text, langCode);
  }

  // Play the appropriate tone for an outcome and then read the message
  // shortly afterwards so the tone and speech do not collide.
  function readResult(outcomeShortKey, message, langCode) {
    if (!soundOn) return;
    if (outcomeShortKey === "emergency") {
      playEmergencyTone();
      setTimeout(() => speak(message, langCode), 600);
    } else if (outcomeShortKey === "act_now") {
      playActNowTone();
      setTimeout(() => speak(message, langCode), 450);
    } else {
      playKeepMonTone();
      setTimeout(() => speak(message, langCode), 350);
    }
  }

  function stopAllAudio() {
    if (ttsAvailable()) window.speechSynthesis.cancel();
  }

  // Wire the voiceschanged event so we re-check Yoruba availability as soon
  // as the browser finishes loading its voice list.
  if (typeof window !== "undefined" && ttsAvailable()) {
    window.speechSynthesis.addEventListener("voiceschanged", () => {
      const before = yorubaVoiceAvailable;
      checkYorubaVoice();
      // If main.js attached a listener, give it a chance to re-render the note
      if (typeof window.__onVoicesChanged === "function" && before !== yorubaVoiceAvailable) {
        window.__onVoicesChanged();
      }
    });
    // Try once eagerly in case voices are already loaded
    checkYorubaVoice();
  }

  return {
    setSoundOn, isSoundOn,
    isYorubaVoiceAvailable,
    readQuestion, readResult,
    stopAllAudio,
    // Exposed for the headless test that just checks the module exists
    _ttsAvailable: ttsAvailable
  };
})();
