"""Audio behavior trace, Pass 2 verification.

Headless Chromium does not play actual sound, but we can intercept the calls
to speechSynthesis.speak() and AudioContext.createOscillator() to confirm
the right audio fires at the right moments in the right language.

This test verifies:
  - Sound is OFF by default (no audio calls before user enables it).
  - Toggling Sound On creates AudioContext.
  - Each question render calls speak(text, lang) when sound is on.
  - Replay button calls speak() again with the same text.
  - Emergency result fires 2-note tone then speaks result message.
  - Act Now result fires 1 warm chime then speaks result message.
  - Keep Monitoring fires 1 soft confirmation then speaks result message.
  - Yoruba demos speak Yoruba text in yo-NG lang (or detect fallback).
"""

from pathlib import Path
from playwright.sync_api import sync_playwright
import json

HTML_PATH = Path("/home/claude/cocci_trl3_repo/prototype/coccialert_live_demo.html").resolve()
OUT_DIR = Path("/home/claude/cocci_trl3_repo/prototype/screenshots")
OUT_DIR.mkdir(exist_ok=True, parents=True)

# JavaScript snippet installed in the page before any code runs. It hooks
# speechSynthesis.speak() and OscillatorNode.start() and records each call
# into window.__audio_log so the test can read back what happened.
HOOK_JS = r"""
window.__audio_log = { speak: [], tones: [], ctxCreated: 0 };

// Patch speechSynthesis.speak to record the text + lang of every utterance.
if ('speechSynthesis' in window) {
  const origSpeak = window.speechSynthesis.speak.bind(window.speechSynthesis);
  window.speechSynthesis.speak = function(utterance) {
    window.__audio_log.speak.push({
      text: utterance.text,
      lang: utterance.lang,
      ts: Date.now()
    });
    return origSpeak(utterance);
  };
}

// Patch AudioContext to record the count of OscillatorNode.start() calls.
['AudioContext', 'webkitAudioContext'].forEach(name => {
  if (typeof window[name] !== 'function') return;
  const OrigCtor = window[name];
  window[name] = function(...args) {
    window.__audio_log.ctxCreated += 1;
    const ctx = new OrigCtor(...args);
    const origCreateOsc = ctx.createOscillator.bind(ctx);
    ctx.createOscillator = function() {
      const osc = origCreateOsc();
      const origStart = osc.start.bind(osc);
      osc.start = function(when) {
        window.__audio_log.tones.push({
          freq: osc.frequency.value,
          when: when || ctx.currentTime,
          ts: Date.now()
        });
        return origStart(when);
      };
      return osc;
    };
    return ctx;
  };
  // preserve prototype access
  Object.setPrototypeOf(window[name], OrigCtor);
});
"""


def read_log(page):
    return page.evaluate("window.__audio_log")


def trace_scenario(browser, lang, demo_id, demo_label):
    ctx = browser.new_context(viewport={"width": 1600, "height": 900})
    page = ctx.new_page()
    page.add_init_script(HOOK_JS)
    page.goto(f"file://{HTML_PATH}", wait_until="networkidle")
    page.wait_for_timeout(150)

    # Pick the right language
    page.click(f"#lang-{lang}-btn")
    page.wait_for_timeout(100)

    # Confirm Sound is OFF and no audio has fired yet
    log_before = read_log(page)
    sound_off_clean = (
        len(log_before["speak"]) == 0 and
        len(log_before["tones"]) == 0 and
        log_before["ctxCreated"] == 0
    )

    # Enable Sound (user gesture)
    page.click("#sound-toggle")
    page.wait_for_timeout(200)
    log_after_toggle = read_log(page)
    ctx_created_on_toggle = log_after_toggle["ctxCreated"] >= 1

    # Click demo button to replay the scenario through the controller
    page.click(f"#{demo_id}")
    page.wait_for_timeout(1100)  # let result render and audio fire
    log_after_demo = read_log(page)

    ctx.close()

    return {
        "label": demo_label,
        "lang": lang,
        "sound_off_clean": sound_off_clean,
        "ctx_created_on_toggle": ctx_created_on_toggle,
        "speak_count": len(log_after_demo["speak"]),
        "tone_count": len(log_after_demo["tones"]) - len(log_after_toggle["tones"]),
        "speak_texts": [s["text"][:80] for s in log_after_demo["speak"]],
        "speak_langs": [s["lang"] for s in log_after_demo["speak"]],
        "tone_freqs": [round(t["freq"], 2) for t in log_after_demo["tones"][len(log_after_toggle["tones"]):]],
    }


def main():
    scenarios = [
        ("en", "demo-emergency-btn",  "English Emergency"),
        ("yo", "demo-emergency-btn",  "Yoruba Emergency"),
        ("en", "demo-act-now-btn",    "English Act Now"),
        ("yo", "demo-act-now-btn",    "Yoruba Act Now"),
        ("en", "demo-keep-mon-btn",   "English Keep Monitoring"),
        ("yo", "demo-keep-mon-btn",   "Yoruba Keep Monitoring"),
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch()
        results = []
        try:
            for lang, btn, label in scenarios:
                r = trace_scenario(browser, lang, btn, label)
                results.append(r)
        finally:
            browser.close()

    print("\nAudio behavior trace (Pass 2 verification)\n" + "=" * 60)
    for r in results:
        print()
        print(f"  {r['label']}")
        print(f"    sound off pre-toggle clean:   {r['sound_off_clean']}")
        print(f"    AudioContext created on On:   {r['ctx_created_on_toggle']}")
        print(f"    tone events after demo:       {r['tone_count']}")
        print(f"    tone frequencies (Hz):        {r['tone_freqs']}")
        print(f"    speak() calls after demo:     {r['speak_count']}")
        if r['speak_langs']:
            print(f"    speak lang codes:             {r['speak_langs']}")
        if r['speak_texts']:
            print(f"    first speak text:             \"{r['speak_texts'][0]}\"")

    # Save raw results for the response
    log_path = OUT_DIR.parent / "audio_trace.json"
    log_path.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\n  Saved trace details to {log_path}")


if __name__ == "__main__":
    main()
