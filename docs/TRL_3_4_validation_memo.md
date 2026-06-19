# CocciAlert — TRL 3-4 Validation Memo
**FCI4Africa Open Call 1 · Option B · Challenge 5**
BioBuild Africa Ltd · RC 9604822
Prepared: June 2026

---

## 1. Purpose of this memo

This memo documents the TRL 3-4 evidence assembled for **CocciAlert**, the USSD/WhatsApp poultry-health triage and informal-sector data system proposed under FCI4Africa Open Call 1, Option B (Challenge 5: *Limited transparency and data obstructing the integration of the informal sector*).

The memo establishes — honestly and within tightly-bounded claims — what has been built, what has been tested, and what remains to advance the solution from TRL 3-4 toward TRL 6 over the 12-month implementation period.

## 2. What has been built (and tested)

### 2.1 Clinical decision logic — TRL 3
A bounded deterministic decision tree for suspected coccidiosis screening in smallholder poultry, comprising:
- 14 closed-form questions with bounded multiple-choice answer sets
- Three triage outputs: **Emergency**, **Act now**, **Keep monitoring**
- 12 supporting signs aggregated under a tiered gating logic (severe diarrhea +1, loose +2, normal +3)
- Pathophysiologically grounded weighting (e.g. the <3 weeks age sub-cohort reflects underdeveloped intestinal immunity)
- Triage-not-diagnosis register throughout — the tool refers high-risk cases to veterinary support and never recommends a specific drug or dose

**Source artefact:** `Coccidiosis_decision_tree.docx`, authored by Dr. Emmanuel Alagbe Oluwabukunmi (PhD, animal science, poultry-specialised). Iterated over six weeks of team meetings (24 May – 18 June 2026, weekly cadence).

### 2.2 Rule engine implementation — TRL 3
A deterministic Python implementation of the decision tree, 280 lines, no external dependencies:
- One-to-one mapping from decision tree clauses to engine functions
- Two clinical ambiguities parameterised (`loose_double_count`, `age_vacc_hard_gate`) so the convention can be flipped without code change
- Auditable rule-fire codes attached to every decision (for downstream traceability)
- Reproducibility metadata (engine version, schema version, parameter settings) emitted with every result

**Source artefact:** `cocci_engine.py`. Validation harness: `cocci_scenarios.py`.

### 2.3 Scenario-based validation — TRL 3
31 synthetic test scenarios spanning the decision space:
- 9 emergency triggers (each emergency rule fired individually + a compound case)
- 14 act-now cases across all three threshold pathways
- 5 keep-monitoring cases below threshold
- 3 edge-at-threshold cases
- Sensitivity tests for both parameterised ambiguities

**Result:** 31 / 31 scenarios match expected outcomes under the literal interpretation of the decision tree. Outcome distribution across the synthetic set: 29% Emergency, 45% Act-now, 26% Keep-monitoring — consistent with a realistic stress-test distribution where most decisions cluster in the actionable region.

### 2.4 Controlled prototype integration — TRL 4
An end-to-end pipeline demonstrating the full informal-sector data flow on synthetic input:
- Farmer-facing question flow (USSD shortcode + WhatsApp Business API mocks)
- Engine integration with consent capture, language selection, and channel detection
- Privacy-preserving anonymized user identification (SHA-256 hash with rotating per-cooperative salt; raw phone number never persisted)
- Schema-compliant event-log row generation
- LGA-level geographic aggregation (no farm-level coordinates ever)
- Sample dataset: 50 synthetic anonymized records spanning 12 LGAs across 5 Nigerian states, 92% consent rate, mixed USSD/WhatsApp + Yoruba/English

**Source artefacts:** `coccialert_demo.html` (visual prototype), `integration_demo.py` (functional integration), `event_log_schema.csv` (schema), `sample_event_log_50.csv` (synthetic dataset).

### 2.5 Privacy and ethics design — TRL 3-4
The privacy architecture is consent-by-default and aligned with GDPR / Nigerian Data Protection Act 2023:
- Explicit consent captured at session start with method-of-capture audit (`consent_method`, `consent_timestamp_utc`)
- Anonymized user IDs derived from phone numbers via salted SHA-256, salt rotated periodically per cooperative
- Geographic resolution capped at Local Government Area; no farm-level GPS
- Sensitive raw inputs (PII) never persisted beyond the active session
- Schema versioning + engine versioning embedded in every record for full reproducibility

## 3. TRL position — honest statement

> CocciAlert is currently at **TRL 3-4**. The clinical decision logic has been formalised by the Science Lead (Dr. Emmanuel Alagbe, PhD animal science) and encoded as a deterministic Python rule engine, validated against 31 synthetic flock scenarios with 100% consistency between expected and actual triage outcomes. A controlled prototype connects the triage engine to a farmer-facing USSD/WhatsApp-style interaction, captures explicit consent, and generates anonymized event-log records suitable for cooperative- and LGA-level analysis. The 12-month FCI4Africa project will advance the tool toward TRL 6 through field pilot validation with smallholder poultry farmers, usability testing in Yorùbá and English, expert clinical review of pilot triage outcomes, and privacy-protected anonymized dataset contribution to the FCI4Africa Food Systems Dashboard.

## 4. What this memo does NOT claim

For honesty and to protect the proposal's eligibility status, the following claims are explicitly NOT made:
- ❌ Clinical field validation has occurred
- ❌ CocciAlert has been deployed with actual farmers
- ❌ The tool diagnoses coccidiosis (it screens and triages, then refers)
- ❌ The tool replaces veterinary services
- ❌ TRL 4 has been demonstrated through field testing
- ❌ The validation dataset reflects real farmer responses

What IS claimed:
- ✓ Clinical logic is scenario-tested against expert-defined cases
- ✓ The engine is expert-reviewed (Dr. Emmanuel Alagbe; sign-off package included)
- ✓ Rule-based deterministic triage produces consistent, traceable outputs
- ✓ A controlled prototype demonstrates end-to-end integration including privacy-protected logging
- ✓ The solution is ready for pilot validation under the funded 12-month implementation

## 5. What remains to reach TRL 6 (mapped to FCI4Africa phases)

| Phase | TRL transition | Key activities |
|---|---|---|
| Phase 1 — Design (Nov 2026 – Jan 2027, 3 months, 20% payment) | TRL 4 confirmation | Africa's Talking USSD procurement, WhatsApp Business API setup, FitCrown Agro cooperative MoU, ethics approval, Yorùbá UX validation with native-speaker cooperative members, final clinical sign-off on production parameters |
| Phase 2 — Development (Feb – Jul 2027, 6 months, 50% payment) | TRL 4 → 5 | Live USSD + WhatsApp deployment, controlled pilot with 80-100 smallholder poultry keepers in 3-4 LGAs, mid-pilot clinical case-review with Emmanuel, adjustments to thresholds based on observed signal patterns |
| Phase 3 — Validation (Aug – Oct 2027, 3 months, 30% payment) | TRL 5 → 6 | 6-month pilot data analysis, methodology paper, openly published anonymized dataset (Zenodo + FCI4Africa Food Systems Dashboard), Ibadan dissemination event, lessons-learnt report |

## 6. Proposal language that the evidence supports

Direct quote-ready for Annex 5 §5 (Technology Impact):

> *"The CocciAlert clinical triage logic has been formalised by Dr. Emmanuel Alagbe (PhD, animal science / poultry) and encoded as a deterministic Python rule engine of 280 lines. The engine has been validated against 31 representative synthetic flock scenarios spanning the decision space (emergency, act-now, and keep-monitoring outcomes), with 100% consistency between expected and actual triage outputs. A controlled prototype integrates the engine with a farmer-facing USSD/WhatsApp interaction layer and a privacy-protected event-logging pipeline, producing schema-compliant anonymized records aligned with FCI4Africa's Food Systems Dashboard requirements. A sample synthetic dataset of 50 records spanning 12 Nigerian LGAs demonstrates the data-contribution pathway. Two clinical parameter ambiguities have been identified and exposed as engine parameters, to be resolved during Phase 1 of the project. CocciAlert begins the project at TRL 3-4 and will advance to TRL 6 through field pilot validation with 80-100 smallholder poultry keepers."*

## 7. Evidence pack inventory

| # | Artefact | Purpose |
|---|---|---|
| 1 | `Coccidiosis_decision_tree.docx` | Source decision logic (Emmanuel) |
| 2 | `cocci_engine.py` | Rule-engine encoding |
| 3 | `cocci_scenarios.py` | 31-scenario validation harness |
| 4 | `cocci_validation_run.json` | Validation output log |
| 5 | `CLINICAL_REVIEW_for_Emmanuel.md` | Expert sign-off pack |
| 6 | `event_log_schema.csv` | Data layer schema definition |
| 7 | `integration_demo.py` | Controlled prototype integration |
| 8 | `sample_event_log_50.csv` | 50-record synthetic dataset |
| 9 | `coccialert_demo.html` | Farmer-facing flow visual prototype |
| 10 | `TRL_3_4_validation_memo.md` | This memo |

---
*Prepared by BioBuild Africa Ltd internal R&D for FCI4Africa Open Call 1 submission. All artefacts are original work by BioBuild Africa Ltd and contain no third-party IP. Synthetic datasets are clearly labeled as such and do not represent real farmer data.*
