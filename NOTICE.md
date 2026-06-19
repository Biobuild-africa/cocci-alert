# NOTICE — License scope and clinical IP carve-out

This repository contains two categories of work with **different licensing**.

---

## 1. Software code and non-clinical schema — MIT License

The following content is licensed under the [MIT License](LICENSE):

- All Python source code (`engine/`, `validation/`, `integration/`)
- The event-log schema definition (`data/event_log_schema.csv`)
- The synthetic dataset (`data/sample_event_log_50.csv`) — provided for demonstration only; contains no real farmer data
- The visual prototype (`prototype/coccialert_demo.html`)
- The `README.md` and the build/setup documentation

You may use, copy, modify, and redistribute these items under MIT terms.

## 2. Clinical decision logic and triage content — All rights reserved

The clinical content of this repository is **copyrighted material**, NOT under MIT, and may not be reused for any clinical deployment, screening service, advisory product, or training resource without express written permission. This includes:

- `docs/decision_tree.md` — the deterministic coccidiosis screening decision tree, its 14 bounded questions, its 12 supporting signs, its threshold logic, and the triage classifications it produces
- `docs/CLINICAL_REVIEW_for_Emmanuel.md` — the expert-review scenarios and clinical interpretation guidance
- The clinical thresholds, sign weightings, and pathophysiological reasoning embedded in the code (the *logic* expressed in `cocci_engine.py`, separate from the code structure that expresses it)

**Copyright © 2026 Dr. Emmanuel Alagbe Oluwabukunmi (PhD, animal science) and BioBuild Africa Ltd. All rights reserved.**

You may:
- ✅ Read this content for understanding the project
- ✅ Reference it in academic citation with attribution
- ✅ Audit it for the purposes of FCI4Africa evaluation or comparable peer review

You may NOT, without prior written permission:
- ❌ Deploy this logic in a poultry-health screening service, application, or platform
- ❌ Sell training, advisory, or extension services based on this decision logic
- ❌ Republish or redistribute the decision tree in modified or derivative form
- ❌ Use this content to train machine learning models for poultry-health triage or diagnosis

To request permission for clinical or commercial use, contact BioBuild Africa Ltd.

## 3. Why this carve-out exists

The MIT License is intentionally permissive for the software layer because openness strengthens the proposal's technical credibility — evaluators can reproduce every result, audit every line of the engine, and inspect the schema.

The clinical layer is treated differently because the decision tree represents months of original work by a domain-credentialed scientist (Emmanuel) and is the basis on which BioBuild Africa intends to build its commercial poultry-health product line beyond the FCI4Africa grant. Open-sourcing the *code* protects no one; open-sourcing the *clinical logic* would risk dilution by unsafe re-implementations and would weaken Emmanuel's standing as the originator.

This separation is consistent with how the broader open-source ecosystem treats medical and veterinary content (e.g. clinical guidelines are typically copyrighted even when implementation code is open).

## 4. Synthetic data disclaimer

The dataset at `data/sample_event_log_50.csv` is **entirely synthetic**. It was generated programmatically by `integration/integration_demo.py` for demonstration. It does NOT represent any real farmer, any real flock, or any real triage decision. The anonymized user IDs are hashes of fake phone numbers and cannot be reversed to any real person.

---

*BioBuild Africa Ltd · RC 9604822 · Ibadan, Oyo State, Nigeria · June 2026.*
