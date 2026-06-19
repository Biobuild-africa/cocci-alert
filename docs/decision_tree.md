# Deterministic Decision Tree for Suspected Coccidiosis Screening

**Author:** Dr. Emmanuel Alagbe Oluwabukunmi (PhD, animal science / poultry-specialised)
**Project:** BioBuild Africa Ltd · CocciAlert · FCI4Africa Open Call 1
**Status:** Formalised clinical logic, ready for rule-engine encoding (TRL 3)

This document is the authoritative source for the clinical logic encoded in
[`engine/cocci_engine.py`](../engine/cocci_engine.py). All triage decisions
made by the engine map one-to-one onto the rules described below.

---

## Decision rule

Follow the steps in order. Stop at the first branch that matches the flock condition.

### 1. Emergency

- Fresh blood is visible in the droppings → **Emergency, contact a veterinarian.**
- Orange mucus or sloughed intestinal tissue is present → **Emergency, contact a veterinarian.**
- Mortality has shown a sudden spike → **Emergency, contact a veterinarian.**
- Severe diarrhea is present AND any of the following are also present: widespread hunched posture / ruffled feathers, significant drop in feed intake, significant drop in water consumption, noticeable paleness, or widespread huddling → **Emergency, contact a veterinarian.**

### 2. Act now

If none of the emergency conditions are met, use the signs below. Count the number of positive supporting signs.

- Predominant droppings are loose.
- Birds are hunched with ruffled feathers (especially if widespread).
- Birds are huddling together despite adequate ambient temperatures.
- There is noticeable paleness or depigmentation in the skin, shanks, or combs.
- Daily feed intake has dropped below the expected growth curve.
- Daily water consumption has dropped below normal.
- The flock is less than 3 weeks old.
- The flock was not vaccinated for coccidiosis at the hatchery, or the vaccination status is unknown.
- The flock is not on a dietary coccidiostat program.
- Daily mortality has shown a gradual increase above baseline.
- The litter is damp or heavily caked and wet.
- Misaligned or leaking drinkers are creating localized wet spots.

**Decision after counting supporting signs:**

- Severe diarrhea + 1 or more supporting signs → **Act now.**
- Loose droppings + 2 or more supporting signs → **Act now.**
- Normal droppings + 3 or more supporting signs, especially when age is under 3 weeks or vaccination status is absent/unknown → **Act now.**

### 3. Keep monitoring, no coccidiosis

- No blood, no orange mucus, no sloughed tissue, and no sudden mortality spike.
- Droppings are normal or only mildly changed.
- Supporting signs are absent or too few to meet the Act-now thresholds.

---

## Decision summary

| Outcome | Trigger |
|---|---|
| Emergency, contact a veterinarian | Fresh blood, orange mucus / sloughed tissue, sudden mortality spike, or severe diarrhea with major systemic signs. |
| Act now | No emergency signs, but the flock has enough supporting signs to suggest active disease pressure. |
| Keep monitoring, no coccidiosis | No red flags and too few supporting signs to justify intervention. |

---

## Questions presented to the farmer

The bounded question schema below is the input layer for the rule engine. Every question has a closed answer set; no free text is captured.

**Q1.** Are there visible signs of fresh blood in the droppings?
> Yes / No

**Q2.** Is there orange mucus or sloughed intestinal tissue present?
> Yes / No

**Q3.** What is the predominant consistency of the droppings?
> Normal (Firm) / Loose / Severe Diarrhea

**Q4.** Are birds exhibiting a hunched posture with ruffled feathers?
> Widespread (>10%) / Isolated (<10%) / None

**Q5.** Are birds huddling together despite adequate ambient temperatures?
> Yes / No

**Q6.** Is there noticeable paleness or depigmentation in the skin, shanks, or combs?
> Yes / No

**Q7.** How has daily feed intake deviated from the expected growth curve over the last 48 hours?
> At/Above Target / Slight Drop (<10%) / Significant Drop (>10%)

**Q8.** How has daily water consumption changed?
> Normal / Slight Drop / Significant Drop

**Q9.** What is the current age of the flock?
> < 3 weeks / 3–8 weeks / > 8 weeks

**Q10.** Was the flock vaccinated for coccidiosis at the hatchery?
> Yes / No / Unknown

**Q11.** Is the flock currently on a dietary coccidiostat program (e.g., ionophores or chemicals)?
> Yes / No

**Q12.** Has daily mortality exceeded the expected baseline for this age?
> No / Gradual Increase / Sudden Spike

**Q13.** What is the overall physical condition of the litter?
> Dry & Friable / Damp / Heavily Caked & Wet

**Q14.** Are there misaligned or leaking drinkers creating localized wet spots?
> Yes / No

---

> **Clinical scope note.** This decision tree is intended for field screening and triage of suspected coccidiosis. It is not a diagnostic instrument and does not replace veterinary examination or laboratory confirmation. The Emergency and Act-now classifications direct the farmer to seek veterinary support; the tool does not recommend any specific drug, dose, or treatment protocol. Implementation must be adapted to local flock health programmes and registered veterinary guidance.

---
*This document is the source-of-truth for the clinical logic encoded in the CocciAlert rule engine. See [`docs/CLINICAL_REVIEW_for_Emmanuel.md`](CLINICAL_REVIEW_for_Emmanuel.md) for the engine-to-tree mapping audit and Emmanuel's sign-off pack.*
