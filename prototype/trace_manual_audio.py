"""Manual-flow audio trace, Pass 2 verification round 2.

The earlier trace used the demo buttons, which fast-forward through the
question chain without rendering each question. That hid the per-question
speak() behaviour.

This script clicks answer buttons one at a time so each question actually
renders, the 200ms auto-read fires, and we can confirm:

  Manual English Emergency  (Q1=Yes):
      speak sequence: [Q1 text, Emergency message]
      tones:          [659.25, 523.25]
      Q2 must NEVER appear

  Manual English Act Now    (Q1=No, Q2=No, Q12=No, Q3=Loose, Q4=Widespread, Q5=Yes):
      speak sequence: [Q1, Q2, Q12, Q3, Q4, Q5, Act Now message]
      tones:          [587.33]

  Manual English Keep Mon   (all 14 healthy):
      speak sequence: [all 14 question texts, Keep Monitoring message]
      tones:          [783.99]

  Manual Yoruba Act Now     (same answers, Yoruba selected):
      speak sequence: [] (Yoruba voice not present in headless => no English
                          voice fallback, just the visible banner)
      tones:          [587.33] (language-independent, still plays)
"""

import json
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML_PATH = Path("/home/claude/cocci_trl3_repo/prototype/coccialert_live_demo.html").resolve()
OUT_DIR = Path("/home/claude/cocci_trl3_repo/prototype/screenshots")
TRACE_JSON = HTML_PATH.parent / "manual_audio_trace.json"

# Patched speak / oscillator so we can read back what happened.
HOOK_JS = r"""
window.__audio_log = { speak: [], tones: [], ctxCreated: 0 };

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
});
"""


# (key, option index to click). The order is the order the adaptive
# controller asks questions in, so the test just clicks them in turn.
EMERGENCY_CLICKS = [
    ("fresh_blood", 0),         # Yes
]

ACT_NOW_CLICKS = [
    ("fresh_blood", 1),         # No
    ("orange_mucus", 1),        # No
    ("mortality", 0),           # No (mortality NONE, asked 3rd by controller)
    ("droppings", 1),           # Loose
    ("hunched", 0),             # Widespread, >10% (sign 1)
    ("huddling", 0),            # Yes (sign 2) -> Loose + 2 signs = Act Now
]

KEEP_MON_CLICKS = [
    ("fresh_blood", 1),         # No
    ("orange_mucus", 1),        # No
    ("mortality", 0),           # No
    ("droppings", 0),           # Normal
    ("hunched", 2),             # None
    ("huddling", 1),            # No
    ("paleness", 1),            # No
    ("feed", 0),                # At/Above target
    ("water", 0),               # Normal
    ("age", 2),                 # > 8 weeks
    ("vacc", 0),                # Yes
    ("coccidiostat", 0),        # Yes
    ("litter", 0),              # Dry & friable
    ("leaking_drinkers", 1),    # No
]


def click_through(page, click_plan):
    """Click each answer one at a time, allowing time for render + speak()."""
    for key, opt_idx in click_plan:
        # The center panel always has up-to-date q-opt buttons indexed 0..n-1.
        page.click(f".q-opt[data-i='{opt_idx}']")
        # 350ms: enough for render + the 200ms readQuestion delay + a buffer.
        page.wait_for_timeout(350)
    # Final wait so result tone + spoken message register.
    page.wait_for_timeout(1100)


def trace_manual(browser, label, lang, click_plan):
    ctx = browser.new_context(viewport={"width": 1600, "height": 900})
    page = ctx.new_page()
    page.add_init_script(HOOK_JS)
    page.goto(f"file://{HTML_PATH}", wait_until="networkidle")
    page.click(f"#lang-{lang}-btn")
    page.wait_for_timeout(120)

    log_before = page.evaluate("window.__audio_log")
    pre_clean = (len(log_before["speak"]) == 0 and
                 len(log_before["tones"]) == 0 and
                 log_before["ctxCreated"] == 0)

    # User gesture to enable sound
    page.click("#sound-toggle")
    page.wait_for_timeout(250)

    # Once sound is on, the *initial* question render has already triggered a
    # speak() via the 200ms timer (or skipped if Yoruba voice missing). Wait
    # one more tick to be sure it lands.
    page.wait_for_timeout(150)

    click_through(page, click_plan)
    log_after = page.evaluate("window.__audio_log")
    ctx.close()

    speak_texts = [s["text"] for s in log_after["speak"]]
    speak_langs = [s["lang"] for s in log_after["speak"]]
    tone_freqs  = [round(t["freq"], 2) for t in log_after["tones"]]

    return {
        "label": label,
        "lang": lang,
        "pre_toggle_clean": pre_clean,
        "ctx_created": log_after["ctxCreated"],
        "speak_count": len(speak_texts),
        "speak_texts": speak_texts,
        "speak_langs": speak_langs,
        "tone_count": len(tone_freqs),
        "tone_freqs": tone_freqs,
    }


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        results = []
        try:
            results.append(trace_manual(browser, "Manual English Emergency",       "en", EMERGENCY_CLICKS))
            results.append(trace_manual(browser, "Manual English Act Now",         "en", ACT_NOW_CLICKS))
            results.append(trace_manual(browser, "Manual English Keep Monitoring", "en", KEEP_MON_CLICKS))
            results.append(trace_manual(browser, "Manual Yoruba Act Now",          "yo", ACT_NOW_CLICKS))
        finally:
            browser.close()

    print("\nManual-flow audio trace (Pass 2 verification round 2)")
    print("=" * 70)
    for r in results:
        print(f"\n  {r['label']}")
        print(f"    pre-toggle clean: {r['pre_toggle_clean']}     "
              f"AudioContext created on On: {r['ctx_created'] >= 1}")
        print(f"    tones played ({r['tone_count']}): {r['tone_freqs']}")
        print(f"    speak() calls ({r['speak_count']}):")
        for i, (text, lang) in enumerate(zip(r["speak_texts"], r["speak_langs"])):
            short = text if len(text) <= 70 else text[:67] + "..."
            print(f"        {i+1:2d}. [{lang}] {short}")
        if r["speak_count"] == 0:
            print(f"        (no English voice used to read Yoruba text)")

    TRACE_JSON.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\n  Saved full JSON to {TRACE_JSON.name}")

    # Critical verifications
    print("\n  Critical verifications:")
    em = results[0]
    print(f"    Emergency: Q2 never spoken                          "
          f"-> {'OK  ' if not any('orange mucus' in t.lower() for t in em['speak_texts']) else 'FAIL'}")
    print(f"    Emergency: Emergency message spoken                 "
          f"-> {'OK  ' if any('emergency' in t.lower() or 'danger sign' in t.lower() for t in em['speak_texts']) else 'FAIL'}")
    print(f"    Emergency: descending 2-note tone                   "
          f"-> {'OK  ' if em['tone_freqs'] == [659.25, 523.25] else 'FAIL'}")
    an = results[1]
    print(f"    Act Now: all six question prompts spoken            "
          f"-> {'OK  ' if an['speak_count'] >= 7 else 'FAIL ('+str(an['speak_count'])+')'}")
    print(f"    Act Now: single warm chime tone                     "
          f"-> {'OK  ' if an['tone_freqs'] == [587.33] else 'FAIL'}")
    km = results[2]
    print(f"    Keep Monitoring: all 14 questions + result spoken   "
          f"-> {'OK  ' if km['speak_count'] >= 15 else 'FAIL ('+str(km['speak_count'])+')'}")
    print(f"    Keep Monitoring: soft confirmation tone             "
          f"-> {'OK  ' if km['tone_freqs'] == [783.99] else 'FAIL'}")
    yo = results[3]
    print(f"    Yoruba: zero speak() calls (no English voice used)  "
          f"-> {'OK  ' if yo['speak_count'] == 0 else 'FAIL'}")
    print(f"    Yoruba: tone still plays (lang-independent)         "
          f"-> {'OK  ' if yo['tone_freqs'] == [587.33] else 'FAIL'}")


if __name__ == "__main__":
    main()
