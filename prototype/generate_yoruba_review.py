"""Regenerate docs/YORUBA_LOCALIZATION_REVIEW.md from the live i18n source files.

This script reads:
  prototype/src/engine.js       (needs Mort/Droppings/Hunched/... enum codes)
  prototype/src/i18n.en.js      (English strings)
  prototype/src/i18n.yo.js      (Yoruba strings)

It then emits a markdown table with every English/Yoruba pair, the stable
internal code, and an unchecked approval box ☐ in the last column for Emmanuel.

The point: whatever wording is currently in i18n.yo.js is what Emmanuel sees,
so when he ticks every box we know the demo text is approved as-is.

Usage:
  python prototype/generate_yoruba_review.py
"""

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT.parent / "docs" / "YORUBA_LOCALIZATION_REVIEW.md"

# Use Node to evaluate the JS source files and dump i18n as JSON. We include
# engine.js because i18n files reference Mort.NONE, Droppings.LOOSE, etc.
NODE_DUMP_SCRIPT = """
const fs = require('fs');
const path = require('path');
const SRC = process.argv[1];
const files = ['engine.js', 'i18n.en.js', 'i18n.yo.js'];
let src = files.map(f => fs.readFileSync(path.join(SRC, f), 'utf-8')).join('\\n');
src += '\\nmodule.exports = {en: i18n_en, yo: i18n_yo};';
const tmpPath = '/tmp/cocci_i18n_dump.js';
fs.writeFileSync(tmpPath, src);
delete require.cache[tmpPath];
const data = require(tmpPath);
process.stdout.write(JSON.stringify(data));
"""

def load_i18n():
    res = subprocess.run(
        ["node", "-e", NODE_DUMP_SCRIPT, str(SRC)],
        capture_output=True, text=True
    )
    if res.returncode != 0:
        raise RuntimeError(f"Node loader failed:\nstdout: {res.stdout}\nstderr: {res.stderr}")
    return json.loads(res.stdout)


# Internal code labels (for the "Internal code" column). For booleans we just
# show `true` / `false`. For enum values, we show the literal JS value the
# engine uses (kept short here for readability).
def code_label(code_value):
    if isinstance(code_value, bool):
        return f"`{str(code_value).lower()}`"
    return f'`"{code_value}"`'


def section(title, body):
    return f"\n## {title}\n\n{body}\n"


def md_row(*cells):
    return "| " + " | ".join(cells) + " |"


def md_table(headers, rows):
    out = [md_row(*headers), md_row(*(["---"] * len(headers)))]
    out.extend(md_row(*r) for r in rows)
    return "\n".join(out)


# Map of i18n.en keys -> human-friendly section + row label for the UI chrome
# block. Keys are grouped so Emmanuel can scan by area of the screen.
UI_GROUPS = [
    ("Top navigation bar", [
        ("nav_title",      "Main demo title"),
        ("nav_subtitle",   "Subtitle under main demo title"),
        ("demo_emergency", "Emergency Demo button label"),
        ("demo_act_now",   "Act Now Demo button label"),
        ("demo_keep_mon",  "Keep Monitoring Demo button label"),
        ("sound_off",      "Sound toggle when off"),
        ("sound_on",       "Sound toggle when on (Pass 2)"),
        ("restart",        "Restart button label"),
    ]),
    ("Audio status messages (Pass 2)", [
        ("audio_listen_now",          "Listen button label when sound is on"),
        ("audio_off_hint",            "Hint text shown when sound is off"),
        ("yoruba_voice_unavailable",  "Amber banner shown under top nav when Yoruba voice is not available on device"),
        ("footer_audio_note",         "Bilingual note shown at the bottom of the page indicating audio is enabled"),
    ]),
    ("Panel headers", [
        ("panel_left_title",  "Left panel header"),
        ("panel_right_title", "Right panel header"),
    ]),
    ("Phone (farmer view)", [
        ("phone_header_sub",  "Phone subtitle under brand name"),
        ("phone_welcome",     "Welcome message bot bubble"),
        ("phone_sound",       "Phone-area sound label when sound is off"),
        ("phone_sound_on",    "Phone-area sound label when sound is on (Pass 2)"),
        ("phone_replay",      "Phone-area replay label"),
    ]),
    ("Progress and stage indicators", [
        ("progress",          "Progress label above bar"),
        ("question_n_of_14",  "Question counter, {n} is replaced at render time"),
        ("stage_emergency",   "Stage 1 chip name"),
        ("stage_supporting",  "Stage 2 chip name"),
        ("stage_result",      "Stage 3 chip name"),
        ("badge_emergency",   "Active-stage badge during emergency screen"),
        ("badge_supporting",  "Active-stage badge during supporting-sign tally"),
        ("badge_result",      "Active-stage badge on the result screen"),
        ("early_stop_note",   "Yellow lightbulb note under question"),
        ("tap_to_hear",       "Pill under question, audio is Pass 2"),
        ("replay_question",   "Replay button next to tap-to-hear"),
    ]),
    ("Backend Preview, Session Summary section", [
        ("session_summary",   "Section header"),
        ("consent_given",     "Consent row label"),
        ("language_label",    "Language row label"),
        ("raw_phone_stored",  "Raw phone row label"),
        ("geography_level",   "Geography row label"),
        ("geography_value",   "Geography row value"),
        ("session_id",        "Session ID row label"),
    ]),
    ("Backend Preview, Answers So Far section", [
        ("answers_so_far",    "Section header"),
    ]),
    ("Backend Preview, Triage Engine Status section", [
        ("triage_engine_status", "Section header"),
        ("stage_label",          "Stage row label"),
        ("early_stopping",       "Early-stopping row label"),
        ("early_not_triggered",  "Early-stopping value while collecting"),
        ("early_triggered",      "Early-stopping value after decision"),
        ("questions_answered",   "Questions-answered row label"),
        ("rationale",            "Rationale row label"),
        ("current_assessment",   "Current-assessment row label"),
        ("collecting_info",      "Current-assessment value while collecting"),
        ("decided_emergency",    "Current-assessment value at Emergency"),
        ("decided_act_now",      "Current-assessment value at Act Now"),
        ("decided_keep_mon",     "Current-assessment value at Keep Monitoring"),
    ]),
    ("Backend Preview, Event Log section", [
        ("event_log_preview",    "Section header"),
    ]),
    ("Result Legend", [
        ("legend_title",            "Legend block heading"),
        ("legend_emergency_title",  "Emergency item title"),
        ("legend_emergency_desc",   "Emergency item description"),
        ("legend_act_title",        "Act Now item title"),
        ("legend_act_desc",         "Act Now item description"),
        ("legend_keep_title",       "Keep Monitoring item title"),
        ("legend_keep_desc",        "Keep Monitoring item description"),
        ("legend_disclaimer",       "Disclaimer below legend"),
    ]),
    ("Result card content", [
        ("result_title_emergency",      "Big card title at Emergency"),
        ("result_title_act_now",        "Big card title at Act Now"),
        ("result_title_keep_mon",       "Big card title at Keep Monitoring"),
        ("result_subtitle_emergency",   "Subtitle under Emergency card title"),
        ("result_subtitle_act_now",     "Subtitle under Act Now card title"),
        ("result_subtitle_keep_mon",    "Subtitle under Keep Monitoring card title"),
        ("result_msg_emergency",        "Full Emergency body message to farmer"),
        ("result_msg_act_now",          "Full Act Now body message to farmer"),
        ("result_msg_keep_mon",         "Full Keep Monitoring body message to farmer"),
        ("decision_reached",            "Stat line, {n} is replaced at render time"),
        ("early_stopping_reason_label", "Stat row label, value is internal code"),
    ]),
    ("Per-question helper notes (only emergency-screen questions show these)", [
        ("helper_fresh_blood",  "Blue info note shown with Q1"),
        ("helper_orange_mucus", "Blue info note shown with Q2"),
        ("helper_mortality",    "Blue info note shown with Q12 (asked 3rd)"),
        ("helper_droppings",    "Blue info note shown with Q3 (asked 4th)"),
    ]),
]


# Internal codes per question key (matches the SCHEMA in engine.js). Used
# for showing Emmanuel which English/Yoruba label maps to which engine code.
QUESTION_ORDER = [
    ("fresh_blood",      "Q1",  [(True, "true"), (False, "false")]),
    ("orange_mucus",     "Q2",  [(True, "true"), (False, "false")]),
    ("mortality",        "Q12 (asked 3rd in adaptive flow)", [("No","Mort.NONE"), ("Gradual Increase","Mort.GRADUAL"), ("Sudden Spike","Mort.SUDDEN_SPIKE")]),
    ("droppings",        "Q3 (asked 4th in adaptive flow)",  [("Normal (Firm)","Droppings.NORMAL"), ("Loose","Droppings.LOOSE"), ("Severe Diarrhea","Droppings.SEVERE_DIARRHEA")]),
    ("hunched",          "Q4",  [("Widespread (>10%)","Hunched.WIDESPREAD"), ("Isolated (<10%)","Hunched.ISOLATED"), ("None","Hunched.NONE")]),
    ("huddling",         "Q5",  [(True,"true"), (False,"false")]),
    ("paleness",         "Q6",  [(True,"true"), (False,"false")]),
    ("feed",             "Q7",  [("At/Above Target","Feed.AT_OR_ABOVE"), ("Slight Drop (<10%)","Feed.SLIGHT_DROP"), ("Significant Drop (>10%)","Feed.SIGNIFICANT_DROP")]),
    ("water",            "Q8",  [("Normal","Water.NORMAL"), ("Slight Drop","Water.SLIGHT"), ("Significant Drop","Water.SIGNIFICANT")]),
    ("age",              "Q9",  [("< 3 weeks","Age.UNDER_3W"), ("3 to 8 weeks","Age.THREE_TO_8W"), ("> 8 weeks","Age.OVER_8W")]),
    ("vacc",             "Q10", [("Yes","Vacc.YES"), ("No","Vacc.NO"), ("Unknown","Vacc.UNKNOWN")]),
    ("coccidiostat",     "Q11", [(True,"true"), (False,"false")]),
    ("litter",           "Q13", [("Dry & Friable","Litter.DRY"), ("Damp","Litter.DAMP"), ("Heavily Caked & Wet","Litter.HEAVILY_CAKED_WET")]),
    ("leaking_drinkers", "Q14", [(True,"true"), (False,"false")]),
]


def md_escape(s):
    if s is None: return ""
    return str(s).replace("|", "\\|").replace("\n", " ")


def emit_review():
    data = load_i18n()
    en, yo = data["en"], data["yo"]

    parts = []
    parts.append("# Yorùbá Localization Review\n")
    parts.append(
        "Auto-generated from `prototype/src/i18n.en.js` and `prototype/src/i18n.yo.js` "
        "by `prototype/generate_yoruba_review.py`. Regenerate after any wording change "
        "so this file always matches the live demo text.\n\n"
        "**Reviewer:** Dr. Emmanuel Alagbe Oluwabukunmi (Science Lead).\n\n"
        "**Drafted by:** Johnson Adetooto, with ChatGPT-assisted farmer-facing wording.\n\n"
        "**Approval signal:** flip `☐` to `☑` on every row you approve as-is. "
        "For any row that needs a revision, replace the Yorùbá text in `prototype/src/i18n.yo.js`, "
        "rerun `python prototype/generate_yoruba_review.py`, and leave the box `☐` until the new "
        "wording is in place.\n\n"
        "**Critical rule:** the *Internal code* column drives the rule engine. Only the *English* "
        "and *Yorùbá* columns are display text. Never change the codes.\n\n"
        "**Coccidiosis name rule (Emmanuel):** the English word `coccidiosis` is kept as the "
        "technical disease name in Yorùbá sentences. The disease is explained alongside it "
        "in farmer Yorùbá. Never invented as a fake Yorùbá disease term.\n"
    )

    # ----- A. UI chrome groups -----
    parts.append("\n## A. UI chrome (top bar, panels, status fields, legend, result card)\n")
    for section_title, items in UI_GROUPS:
        rows = []
        for key, note in items:
            rows.append((
                f"`{key}`",
                md_escape(en[key]),
                md_escape(yo[key]),
                md_escape(note),
                "☐"
            ))
        body = md_table(["Key", "English", "Yorùbá", "Where shown", "Approval"], rows)
        parts.append(section(section_title, body))

    # ----- B. Questions -----
    parts.append("\n## B. The 14 questions\n")
    parts.append(
        "Each question table has three sub-rows: the question text itself, then one row per "
        "answer option. The `Internal code` column shows what the engine sees regardless of "
        "language; the engine never reads the English or Yorùbá display text.\n"
    )
    for key, q_label, opts_spec in QUESTION_ORDER:
        en_q  = en["questions"][key]
        yo_q  = yo["questions"][key]
        rows = []
        # Question text row
        rows.append((
            f"{q_label}.q",
            "*question text*",
            md_escape(en_q["q"]),
            md_escape(yo_q["q"]),
            "n/a",
            "☐"
        ))
        # Option rows
        for code, code_repr in opts_spec:
            en_opt = en_q["opts"].get(str(code).lower() if isinstance(code,bool) else code, {})
            yo_opt = yo_q["opts"].get(str(code).lower() if isinstance(code,bool) else code, {})
            rows.append((
                f"{q_label}.{code_repr.split('.')[-1].lower() if '.' in code_repr else code_repr}.text",
                "option label",
                md_escape(en_opt.get("text","")),
                md_escape(yo_opt.get("text","")),
                f"`{code_repr}`",
                "☐"
            ))
            rows.append((
                f"{q_label}.{code_repr.split('.')[-1].lower() if '.' in code_repr else code_repr}.desc",
                "option helper line",
                md_escape(en_opt.get("desc","")),
                md_escape(yo_opt.get("desc","")),
                f"`{code_repr}`",
                "☐"
            ))
        parts.append("\n### " + q_label + " (`" + key + "`)\n")
        parts.append(md_table(["Row ID","Kind","English","Yorùbá","Internal code","Approval"], rows))
        parts.append("\n")

    # ----- Footer -----
    parts.append(
        "\n---\n\n"
        "## How approval works\n\n"
        "1. Tick `☐` to `☑` on every row you approve.\n"
        "2. For any row that needs revision, replace the Yorùbá text in `prototype/src/i18n.yo.js` directly.\n"
        "3. Re-run `python prototype/generate_yoruba_review.py` so this file is regenerated from the new wording.\n"
        "4. Re-run `python prototype/build.py` so `prototype/coccialert_live_demo.html` is rebuilt with the new Yorùbá.\n"
        "5. Re-run `node prototype/src/test_adaptive_demo.js` to confirm the 6 scenarios still pass.\n\n"
        "Once every row is `☑`, this file is the approval record and the demo Yorùbá is signed off.\n"
    )

    OUT.write_text("\n".join(parts), encoding="utf-8")
    return OUT


if __name__ == "__main__":
    out = emit_review()
    print(f"Wrote: {out}")
    print(f"  Size: {out.stat().st_size / 1024:.1f} KB")
