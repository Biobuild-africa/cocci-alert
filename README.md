# CocciAlert

**A privacy-protected USSD/WhatsApp poultry-health triage and informal-sector data system for Nigerian smallholders.**

CocciAlert converts smallholder poultry health events into anonymized, consented, LGA-aggregated food-system resilience data, addressing the lack of formal disease records in Nigeria's informal poultry sector.

This repository contains the **TRL 3-4 evidence pack** prepared in support of the [FCI4Africa Open Call 1](https://opencalls.fci4africa.eu) proposal (Horizon Europe HORIZON-CL6-2024-FARM2FORK-01-11), submitted under **Option B · Challenge 5: Limited transparency and data obstructing the integration of the informal sector**.

---

## Why this exists

Smallholder poultry farms contribute roughly 65 to 77% of total chicken production in Nigeria (Bamidele et al., 2022, *Vet Med Int* 2022:7746144), and operate almost entirely outside formal disease-recording systems. Coccidiosis is a major and largely preventable cause of flock mortality, yet:

- No structured event-level data exists at LGA scale
- Farmers default to inappropriate over-the-counter antibiotic use, contributing to AMR
- Buyers cannot distinguish risk-managed from unmanaged sources
- The FCI4Africa Food Systems Dashboard has no informal-sector poultry-health layer

CocciAlert is a **triage tool, not a diagnostic tool**. It helps a farmer decide whether a flock needs no action, immediate management changes, or a veterinarian, and in doing so, generates one of the first structured, anonymized, LGA-level poultry-health event datasets for informal smallholder poultry systems in Nigeria.

---

## What's in this repository

The complete **TRL 3-4 evidence pack**:

| Folder | Contents |
|---|---|
| `docs/` | Clinical decision logic, TRL validation memo, expert review pack |
| `engine/` | Deterministic Python rule engine encoding the clinical decision tree |
| `validation/` | 31-scenario validation harness + run logs |
| `integration/` | End-to-end controlled prototype: input → engine → consent → anonymized log |
| `data/` | Event-log schema (CSV) + 50-record synthetic anonymized dataset |
| `prototype/` | Interactive adaptive-triage demo (bilingual, modular source + bundled HTML), and an older static USSD/WhatsApp mock for reference |

### TRL 3, Clinical logic formalised and encoded

- **`docs/decision_tree.md`**, The bounded decision tree authored by Dr. Emmanuel Alagbe Oluwabukunmi (PhD, animal science / poultry-specialised). 14 closed-form questions, 12 supporting signs, three triage outputs (Emergency / Act now / Keep monitoring).
- **`engine/cocci_engine.py`**, One-to-one Python encoding. 280 lines, no external dependencies. Two clinical ambiguities parameterised for clean Phase-1 resolution.
- **`validation/cocci_scenarios.py`**, 31 synthetic scenarios spanning the decision space. **Result: 31/31 match expected outcomes.**

### TRL 4, Controlled prototype integration

- **`integration/integration_demo.py`**, End-to-end pipeline including consent capture, salted SHA-256 user-ID anonymization, and schema-compliant event-log emission.
- **`data/event_log_schema.csv`**, 29-field schema with privacy classifications, geographic resolution capped at LGA level.
- **`data/sample_event_log_50.csv`**, 50 synthetic anonymized records across 12 LGAs in 5 Nigerian states, 92% consent rate, mixed USSD/WhatsApp and Yoruba/English.
- **`prototype/coccialert_live_demo.html`**, Self-contained interactive adaptive-triage demo. Three-panel layout (phone view, current question, anonymized backend preview). Adaptive early stopping per Emmanuel's decision tree. Bilingual English and Yorùbá. Open directly by double-clicking.
- **`prototype/coccialert_demo.html`**, Older static farmer-facing visual mock, kept for reference. The live demo above is the main TRL prototype.
- **`prototype/src/`**, Modular editable source for the live demo. See "Editing the interactive demo" below.

### Honest scope statement

This evidence pack establishes **TRL 3-4 in a controlled prototype**. It does **not** claim:

- Clinical field validation
- Real farmer deployment
- Aflatoxin or other disease diagnosis
- Replacement of veterinary services

It **does** establish:

- Expert-formalised, scenario-tested clinical triage logic
- Privacy-protected, consented anonymized data generation
- End-to-end integration in a reproducible test environment
- Ready-for-pilot status for the funded 12-month implementation

---

## How to run it locally

Requires Python 3.9+. No package installation needed, the engine has zero external dependencies.

```bash
git clone https://github.com/Biobuild-africa/cocci-alert.git
cd cocci-alert

# Run the 31-scenario validation
python3 validation/cocci_scenarios.py

# Run the single-farmer integration demo
python3 integration/integration_demo.py

# Generate a 50-record synthetic dataset
python3 integration/integration_demo.py --batch 50

# Open the interactive bilingual adaptive-triage demo
open prototype/coccialert_live_demo.html        # macOS
xdg-open prototype/coccialert_live_demo.html    # Linux
start prototype/coccialert_live_demo.html       # Windows
```

---

## Editing the interactive demo

The bundled `prototype/coccialert_live_demo.html` is built from modular source files in `prototype/src/`. To change any wording, color, or behaviour, edit a source file and rerun the build.

| What you want to change | Edit only this file |
|---|---|
| An English question, answer label, helper note, button label, result message, or backend-preview label | `prototype/src/i18n.en.js` |
| Any Yorùbá string | `prototype/src/i18n.yo.js` |
| Which pre-canned scenario a demo button replays | `prototype/src/demo_scenarios.js` |
| The order in which the controller asks questions | `prototype/src/flow_controller.js` |
| A clinical rule, threshold, or sign list (must also update the Python engine) | `prototype/src/engine.js` and `engine/cocci_engine.py` |
| Colors, fonts, layout, card styling | `prototype/src/styles.css` |
| Page skeleton (header markup, panel containers) | `prototype/template.html` |

After editing, run:

```bash
# Rebuild the bundled HTML
python prototype/build.py

# Confirm the 6 adaptive scenarios still pass
node prototype/src/test_adaptive_demo.js

# Regenerate Emmanuel's Yorùbá review file from i18n.yo.js
python prototype/generate_yoruba_review.py
```

Then open the rebuilt demo:

```bash
open prototype/coccialert_live_demo.html        # macOS
xdg-open prototype/coccialert_live_demo.html    # Linux
start prototype/coccialert_live_demo.html       # Windows
```

The bundled HTML is self-contained, no internet or server required.

---

## Audio support (Pass 2)

The interactive demo includes browser-native audio support: each question can be read aloud, and each triage outcome plays a short distinctive tone before the result message is spoken.

**Audio is off by default.** The reviewer must click the **Sound: off → Sound: on** toggle in the top bar to enable speech and tones. This is required because browsers block automatic audio playback until a user gesture.

**What audio fires:**

| Outcome | Tone | Then spoken |
|---|---|---|
| Emergency | Two descending notes (E5 → C5, around 450ms total), serious | Emergency message in the selected language |
| Act Now | Single warm chime (D5, around 300ms) | Act Now message in the selected language |
| Keep Monitoring | Soft confirmation (G5, around 200ms) | Keep Monitoring message in the selected language |

**Questions:** when Sound is on, each question is read aloud as it appears. A **Replay Question** button lets the reviewer hear the current question again on demand.

**Yorùbá voice availability:** browser-native text-to-speech does not ship with Yorùbá on most desktops (Chrome, Edge, Safari typically include English, Spanish, French, German, Mandarin, Hindi, but not Yorùbá). When Yorùbá is selected and no Yorùbá voice is present, the demo:

- displays a clear amber banner under the top bar: *"Yorùbá text is displayed; audio support depends on device or browser voice support"*
- continues to show all Yorùbá text correctly
- does NOT fall back to an English voice reading Yorùbá words (which would mispronounce everything)
- continues to play the three outcome tones, since those are language-independent

**Technical implementation:** `prototype/src/audio.js` uses only `window.speechSynthesis` (TTS) and `window.AudioContext` (synthesized tones). No external audio files, no CDN, no Google Cloud TTS, no ElevenLabs, no paid APIs. The bundled HTML works fully offline.

**Audio is additive only.** The engine logic, the flow controller, the question counts, and the adaptive early-stopping behaviour are exactly the same with audio off as with audio on. Toggling Sound does not change clinical decisions in any way.

---

## Project trajectory (FCI4Africa-aligned)

| Phase | Months | TRL transition | Payment |
|---|---|---|---|
| Pre-submission (this repo) | June 2026 | TRL 3-4 established | n/a |
| Phase 1, Design | Nov 2026 – Jan 2027 | TRL 4 confirmation | 20% |
| Phase 2, Development | Feb – Jul 2027 | TRL 4 → 5 | 50% |
| Phase 3, Validation | Aug – Oct 2027 | TRL 5 → 6 | 30% |

---

## Team

**Dr. Emmanuel Alagbe Oluwabukunmi**, Science Lead. PhD, animal science (poultry-specialised). Clinical decision logic and Phase-2 pilot oversight.

**Johnson Adetooto**, Engineering Lead. ML and civil engineering background. Rule engine implementation, integration architecture, and dataset infrastructure.

**BioBuild Africa Ltd**, RC 9604822 · Incorporated 10 June 2026 · Ibadan, Oyo State, Nigeria.

---

## Citation

If referencing this evidence pack in submission materials or reviews:

> BioBuild Africa Ltd (2026). *CocciAlert: TRL 3-4 evidence pack for FCI4Africa Open Call 1 submission.* GitHub repository: `https://github.com/Biobuild-africa/cocci-alert`. Version `v1.0.0-fci4africa-submission`.

---

## License

This repository is licensed under a **two-layer model**, see [`NOTICE.md`](NOTICE.md) for the full breakdown.

- **Software code and schema** (the contents of `engine/`, `validation/`, `integration/`, `prototype/`, and the schema CSV in `data/`), licensed under the [MIT License](LICENSE).
- **Clinical decision logic** (the decision tree in `docs/decision_tree.md` and the clinical thresholds it embeds), © 2026 Dr. Emmanuel Alagbe Oluwabukunmi and BioBuild Africa Ltd, all rights reserved. May be read and cited; clinical re-use requires written permission.

The synthetic dataset in `data/sample_event_log_50.csv` contains no real farmer data and is provided for demonstration only.
