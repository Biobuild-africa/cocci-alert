# CocciAlert Rule Engine — Clinical Review Pack
**For sign-off by Dr. Emmanuel Alagbe Oluwabukunmi (PhD, animal science / poultry)**
BioBuild Africa Ltd · RC 9604822
Prepared in support of the FCI4Africa Open Call 1 proposal — CocciAlert, Option B / Challenge 5

---

## 1. What this document is

This is the clinical-review artefact that completes the **TRL 3 evidence chain** for the CocciAlert proposal. Emmanuel's decision tree (`Coccidiosis_decision_tree.docx`) has been encoded one-to-one into a deterministic Python rule engine and validated against 31 synthetic scenarios. This document asks Emmanuel to:

1. Confirm the rule encoding is faithful to his clinical intent
2. Resolve two parameterised clinical ambiguities
3. Sign off on the 31 scenario outcomes as clinically acceptable

Once signed, this completes Artefact #3 (expert validation) in the TRL 3 evidence pack.

## 2. Mapping from decision tree to engine

The engine implements **exactly** the three-step logic from the decision tree:

| Decision-tree section | Engine implementation |
|---|---|
| §1 Emergency triggers | `emergency_check()` — short-circuits before counting signs |
| §2 Supporting-sign tally | `collect_supporting_signs()` — returns positive signs list |
| §2 Decision after counting | `triage()` — applies gating + threshold logic |
| §3 Keep monitoring | Default fallthrough when no rule matches |

The 14 questions are encoded as bounded enumerations matching the answer choices verbatim:

| Q | Variable name | Choices |
|---|---|---|
| 1 | fresh_blood_in_droppings | Yes / No |
| 2 | orange_mucus_or_sloughed_tissue | Yes / No |
| 3 | droppings_consistency | Normal (Firm) / Loose / Severe Diarrhea |
| 4 | hunched_posture | Widespread (>10%) / Isolated (<10%) / None |
| 5 | huddling_despite_temperature | Yes / No |
| 6 | paleness_or_depigmentation | Yes / No |
| 7 | feed_intake_deviation | At/Above Target / Slight Drop (<10%) / Significant Drop (>10%) |
| 8 | water_consumption_change | Normal / Slight Drop / Significant Drop |
| 9 | flock_age | < 3 weeks / 3–8 weeks / > 8 weeks |
| 10 | coccidiosis_vaccinated_at_hatchery | Yes / No / Unknown |
| 11 | on_coccidiostat_program | Yes / No |
| 12 | mortality_trend | No / Gradual Increase / Sudden Spike |
| 13 | litter_condition | Dry & Friable / Damp / Heavily Caked & Wet |
| 14 | leaking_or_misaligned_drinkers | Yes / No |

## 3. Two clinical clarifications that need Emmanuel's decision

These were noted in earlier conversations with Damilola as unresolved. Both are parameterised in code so they can be flipped without re-engineering. **Emmanuel should mark which interpretation he intends.**

### 3.1 The "loose droppings" double-counting question

Your supporting-signs list (§2 of the decision tree) includes "Predominant droppings are loose" as one of the 12 supporting signs. But the same variable (Q3) is **also** the gating condition for the Act-now thresholds (Severe diarrhea + 1 / Loose + 2 / Normal + 3).

**The question:** When Q3 = Loose, should "Predominant droppings are loose" be counted as one of the supporting signs *toward* the +2 threshold, or excluded to avoid double-counting?

- [ ] **Option A (default in engine, recommended):** Do NOT double-count. When Q3 = Loose, the "loose droppings" sign is treated as the gating variable only; the +2 threshold must be met by signs *other than* loose droppings. (Engine parameter: `loose_double_count=False`)
- [ ] **Option B:** DO count it. When Q3 = Loose, "loose droppings" is one positive sign automatically, so only 1 additional sign is needed to reach the +2 threshold. (Engine parameter: `loose_double_count=True`)

**Emmanuel's decision:** ____________________________

### 3.2 The age/vaccination clause for Normal droppings

Your decision tree text says:

> *"Normal droppings + 3 or more supporting signs, **especially when age is under 3 weeks or vaccination status is absent/unknown** → Act now."*

**The question:** Is the "especially when" clause a hard gate (must be satisfied) or emphasis only (highlighting the strongest cases)?

- [ ] **Option A (default in engine, recommended):** Emphasis only. Normal droppings + ≥3 supporting signs always triggers Act-now; the age/vaccination clause just signals the strongest sub-population. (Engine parameter: `age_vacc_hard_gate=False`)
- [ ] **Option B:** Hard gate. Normal droppings + ≥3 signs triggers Act-now ONLY IF age <3 weeks OR vaccination is absent/unknown. Otherwise stays in Keep Monitoring. (Engine parameter: `age_vacc_hard_gate=True`)

**Emmanuel's decision:** ____________________________

## 4. The 31 synthetic scenarios for clinical sign-off

Each scenario below was run through the rule engine with the default parameters (loose_double_count=False, age_vacc_hard_gate=False). All 31 produce outcomes matching the expected interpretation of the decision tree.

**Emmanuel: review each scenario's expected outcome. Mark ✓ if clinically acceptable, or note a concern.**

### Emergency triggers (9 scenarios)

| ID | Scenario | Engine outcome | Emmanuel ✓ / concern |
|---|---|---|---|
| E1 | Fresh blood visible in droppings, otherwise healthy-looking | EMERGENCY | |
| E2 | Orange mucus / sloughed intestinal tissue observed | EMERGENCY | |
| E3 | Sudden mortality spike with no other major signs | EMERGENCY | |
| E4 | Severe diarrhea + widespread hunched posture | EMERGENCY | |
| E5 | Severe diarrhea + significant feed drop | EMERGENCY | |
| E6 | Severe diarrhea + paleness | EMERGENCY | |
| E7 | Severe diarrhea + widespread huddling | EMERGENCY | |
| E8 | Severe diarrhea + significant water drop | EMERGENCY | |
| E9 | Multiple emergency signs (blood + spike + severe diarrhea + paleness) | EMERGENCY | |

### Act-now via Severe diarrhea + ≥1 supporting (no emergency systemic) (3 scenarios)

| ID | Scenario | Engine outcome | Emmanuel ✓ / concern |
|---|---|---|---|
| A1 | Severe diarrhea + leaking drinkers | ACT NOW | |
| A2 | Severe diarrhea + damp litter only | ACT NOW | |
| A3 | Severe diarrhea + slight (not significant) feed drop | ACT NOW | |

### Act-now via Loose droppings + ≥2 supporting (4 scenarios)

| ID | Scenario | Engine outcome | Emmanuel ✓ / concern |
|---|---|---|---|
| A4 | Loose droppings + damp litter + leaking drinkers | ACT NOW | |
| A5 | Loose droppings + gradual mortality + slight feed drop | ACT NOW | |
| A6 | Loose droppings + widespread hunched + huddling | ACT NOW | |
| A7 | Loose droppings + <3wk + unvaccinated | ACT NOW | |

### Act-now via Normal droppings + ≥3 supporting (3 scenarios)

| ID | Scenario | Engine outcome | Emmanuel ✓ / concern |
|---|---|---|---|
| A8 | Normal droppings + wet litter + leaking drinkers + <3wk | ACT NOW | |
| A9 | Normal droppings + unknown vaccine + no coccidiostat + damp litter | ACT NOW | |
| A10 | Normal droppings + gradual mortality + <3wk + no coccidiostat + damp litter | ACT NOW | |

### Keep monitoring (5 scenarios)

| ID | Scenario | Engine outcome | Emmanuel ✓ / concern |
|---|---|---|---|
| K1 | Completely healthy flock | KEEP MONITORING | |
| K2 | Loose droppings + only 1 supporting sign | KEEP MONITORING | |
| K3 | Normal droppings + 2 supporting signs | KEEP MONITORING | |
| K4 | Isolated hunched posture only (doesn't count as widespread) | KEEP MONITORING | |
| K5 | Slight water drop only — single sign | KEEP MONITORING | |

### Edge cases at threshold (3 scenarios)

| ID | Scenario | Engine outcome | Emmanuel ✓ / concern |
|---|---|---|---|
| EDGE1 | Loose + exactly 2 signs (at threshold) | ACT NOW | |
| EDGE2 | Normal + exactly 3 signs (at threshold) | ACT NOW | |
| EDGE3 | Severe diarrhea alone, zero other signs, no emergency systemic | KEEP MONITORING | ⚠ check |

> **EDGE3 note:** With zero supporting signs and no emergency systemic signs, severe diarrhea alone defaults to Keep Monitoring under the literal reading of the tree. Emmanuel should confirm: is severe diarrhea on its own clinically sufficient to escalate, even without other signs? If yes, we should add a fourth threshold: "Severe diarrhea + 0 signs → Act now anyway." If no, the current behaviour is correct.

### Routine background + parameter sensitivity (7 scenarios)

| ID | Scenario | Engine outcome | Emmanuel ✓ / concern |
|---|---|---|---|
| R1 | Older vaccinated flock + paleness only | KEEP MONITORING | |
| R2 | Young unvaccinated chicks, otherwise dry/managed | ACT NOW | |
| P1 | Loose + 1 other sign — default param behaviour | KEEP MONITORING | |
| P2 | Older vaccinated + 3 management signs — default param behaviour | ACT NOW | |

## 5. Clinical sign-off

I, **Dr. Emmanuel Alagbe Oluwabukunmi** (PhD, animal science / poultry), confirm that:

- [ ] The Python rule engine faithfully encodes the clinical logic of my decision tree dated [DATE].
- [ ] The 31 scenarios above produce clinically acceptable triage outcomes (with noted concerns, if any, addressed).
- [ ] I have resolved the two parameterised ambiguities in §3 above.
- [ ] This engine is appropriate for use in the CocciAlert proposal's TRL 3 claim.

Signature: ____________________________      Date: ____________________________

## 6. Notes for the proposal narrative

The validation results support the following defensible statement in Annex 5 Section 5 (Technology Impact / TRL):

> *"The CocciAlert clinical decision logic has been formalised by Dr. Emmanuel Alagbe (poultry-specialised PhD, animal science) and encoded as a deterministic Python rule engine. The engine has been validated against 31 synthetic flock scenarios spanning the decision space, with 100% consistency between expected and actual triage outcomes under the literal interpretation of the decision tree. Clinical sign-off documented in BioBuild Africa Ltd internal review package, available on request. Two clinical ambiguities have been identified and parameterised for resolution in Phase 1 of the project. This work establishes the clinical-logic component at TRL 3."*

---
*Prepared by BioBuild Africa Ltd internal R&D for FCI4Africa Open Call 1 submission.*
