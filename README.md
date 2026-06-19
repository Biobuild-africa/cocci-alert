# CocciAlert

**A privacy-protected USSD/WhatsApp poultry-health triage and informal-sector data system for Nigerian smallholders.**

CocciAlert converts smallholder poultry health events into anonymized, consented, LGA-aggregated food-system resilience data — addressing the lack of formal disease records in Nigeria's informal poultry sector.

This repository contains the **TRL 3-4 evidence pack** prepared in support of the [FCI4Africa Open Call 1](https://opencalls.fci4africa.eu) proposal (Horizon Europe HORIZON-CL6-2024-FARM2FORK-01-11), submitted under **Option B · Challenge 5: Limited transparency and data obstructing the integration of the informal sector**.

---

## Why this exists

The Nigerian smallholder poultry sector — estimated at over 80% of national poultry production — operates almost entirely outside formal disease-recording systems. Coccidiosis is the single largest preventable cause of flock mortality, yet:

- No structured event-level data exists at LGA scale
- Farmers default to inappropriate over-the-counter antibiotic use, contributing to AMR
- Buyers cannot distinguish risk-managed from unmanaged sources
- The FCI4Africa Food Systems Dashboard has no informal-sector poultry-health layer

CocciAlert is a **triage tool, not a diagnostic tool**. It helps a farmer decide whether a flock needs no action, immediate management changes, or a veterinarian — and in doing so, generates the first structured, anonymized, LGA-aggregated dataset of smallholder poultry health events in Nigeria.

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
| `prototype/` | Farmer-facing visual prototype (USSD + WhatsApp mocks) |

### TRL 3 — Clinical logic formalised and encoded

- **`docs/decision_tree.md`** — The bounded decision tree authored by Dr. Emmanuel Alagbe Oluwabukunmi (PhD, animal science / poultry-specialised). 14 closed-form questions, 12 supporting signs, three triage outputs (Emergency / Act now / Keep monitoring).
- **`engine/cocci_engine.py`** — One-to-one Python encoding. 280 lines, no external dependencies. Two clinical ambiguities parameterised for clean Phase-1 resolution.
- **`validation/cocci_scenarios.py`** — 31 synthetic scenarios spanning the decision space. **Result: 31/31 match expected outcomes.**

### TRL 4 — Controlled prototype integration

- **`integration/integration_demo.py`** — End-to-end pipeline including consent capture, salted SHA-256 user-ID anonymization, and schema-compliant event-log emission.
- **`data/event_log_schema.csv`** — 29-field schema with privacy classifications, geographic resolution capped at LGA level.
- **`data/sample_event_log_50.csv`** — 50 synthetic anonymized records across 12 LGAs in 5 Nigerian states, 92% consent rate, mixed USSD/WhatsApp and Yoruba/English.
- **`prototype/coccialert_demo.html`** — Self-contained farmer-facing visual mock (open directly in any browser).

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

Requires Python 3.9+. No package installation needed — the engine has zero external dependencies.

```bash
git clone https://github.com/<your-org>/cocci-alert.git
cd cocci-alert

# Run the 31-scenario validation
python3 engine/cocci_scenarios.py

# Run the single-farmer integration demo
python3 integration/integration_demo.py

# Generate a 50-record synthetic dataset
python3 integration/integration_demo.py --batch 50

# Open the visual prototype in your browser
open prototype/coccialert_demo.html        # macOS
xdg-open prototype/coccialert_demo.html    # Linux
start prototype/coccialert_demo.html       # Windows
```

---

## Project trajectory (FCI4Africa-aligned)

| Phase | Months | TRL transition | Payment |
|---|---|---|---|
| Pre-submission (this repo) | June 2026 | TRL 3-4 established | — |
| Phase 1 — Design | Nov 2026 – Jan 2027 | TRL 4 confirmation | 20% |
| Phase 2 — Development | Feb – Jul 2027 | TRL 4 → 5 | 50% |
| Phase 3 — Validation | Aug – Oct 2027 | TRL 5 → 6 | 30% |

---

## Team

**Dr. Emmanuel Alagbe Oluwabukunmi** — Science Lead. PhD, animal science (poultry-specialised). Clinical decision logic and Phase-2 pilot oversight.

**Damilola "Johnson"** — Engineering Lead. ML and civil engineering background. Rule engine implementation, integration architecture, and dataset infrastructure.

**BioBuild Africa Ltd** — RC 9604822 · Incorporated 10 June 2026 · Ibadan, Oyo State, Nigeria.

---

## Citation

If referencing this evidence pack in submission materials or reviews:

> BioBuild Africa Ltd (2026). *CocciAlert: TRL 3-4 evidence pack for FCI4Africa Open Call 1 submission.* GitHub repository: `<your-url-here>`. Version `v1.0.0-fci4africa-submission`.

---

## License

This repository is licensed under a **two-layer model** — see [`NOTICE.md`](NOTICE.md) for the full breakdown.

- **Software code and schema** (the contents of `engine/`, `validation/`, `integration/`, `prototype/`, and the schema CSV in `data/`) — licensed under the [MIT License](LICENSE).
- **Clinical decision logic** (the decision tree in `docs/decision_tree.md` and the clinical thresholds it embeds) — © 2026 Dr. Emmanuel Alagbe Oluwabukunmi and BioBuild Africa Ltd, all rights reserved. May be read and cited; clinical re-use requires written permission.

The synthetic dataset in `data/sample_event_log_50.csv` contains no real farmer data and is provided for demonstration only.
