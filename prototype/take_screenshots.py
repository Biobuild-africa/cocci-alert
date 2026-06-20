"""Screenshot Pass 1 demo states.

Workflow per shot:
  1. Open the local HTML file
  2. Click language button (en or yo)
  3. Click demo button (Emergency / Act Now / Keep Monitoring)
  4. Wait briefly for the controller to settle
  5. Take a full-page screenshot
"""

import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML_PATH = Path("/home/claude/cocci_trl3_repo/prototype/coccialert_live_demo.html").resolve()
OUT_DIR = Path("/home/claude/cocci_trl3_repo/prototype/screenshots")
OUT_DIR.mkdir(exist_ok=True, parents=True)

# (filename, lang, demo_button_id)
SHOTS = [
    ("01_english_emergency.png",        "en", "demo-emergency-btn"),
    ("02_yoruba_emergency.png",         "yo", "demo-emergency-btn"),
    ("03_english_act_now.png",          "en", "demo-act-now-btn"),
    ("04_yoruba_act_now.png",           "yo", "demo-act-now-btn"),
    ("05_english_keep_monitoring.png",  "en", "demo-keep-mon-btn"),
    ("06_yoruba_keep_monitoring.png",   "yo", "demo-keep-mon-btn"),
]

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            for filename, lang, demo_id in SHOTS:
                ctx = browser.new_context(viewport={"width": 1600, "height": 1100})
                page = ctx.new_page()
                url = f"file://{HTML_PATH}"
                page.goto(url, wait_until="networkidle")
                # Set language
                page.click(f"#lang-{lang}-btn")
                page.wait_for_timeout(150)
                # Pass 2: enable Sound On so the audio UI state is visible.
                # The headless Chromium does not actually play audio but the
                # visual indicators (toggle in 'on' state, active replay
                # buttons, Yoruba voice fallback banner if applicable) update.
                page.click("#sound-toggle")
                page.wait_for_timeout(200)
                # Click demo button
                page.click(f"#{demo_id}")
                page.wait_for_timeout(500)
                # Full-page screenshot
                out = OUT_DIR / filename
                page.screenshot(path=str(out), full_page=True)
                print(f"  saved {out.name}: {out.stat().st_size // 1024} KB")
                ctx.close()

            # Bonus: a close-up of the event-log preview block for one scenario
            # (Act Now / English) so the reviewer can see the JSON clearly.
            ctx = browser.new_context(viewport={"width": 1600, "height": 1100})
            page = ctx.new_page()
            page.goto(f"file://{HTML_PATH}", wait_until="networkidle")
            page.click("#lang-en-btn")
            page.click("#demo-act-now-btn")
            page.wait_for_timeout(500)
            # Locate the event-log code element specifically
            log_box = page.locator(".event-log-code")
            out = OUT_DIR / "07_event_log_preview_act_now_en.png"
            log_box.screenshot(path=str(out))
            print(f"  saved {out.name}: {out.stat().st_size // 1024} KB")
            ctx.close()
        finally:
            browser.close()

if __name__ == "__main__":
    main()
