"""
CocciAlert — Synthetic Scenario Validation Pack

Generates 32 synthetic flock observations spanning the decision space,
runs the rule engine, and produces a clinical-review-ready report
for Emmanuel's sign-off.

Scenario design covers:
  - Emergency triggers (each individually, plus the severe-diarrhea + systemic combo)
  - Act-now via Severe-diarrhea+1 (without emergency systemic signs)
  - Act-now via Loose+2
  - Act-now via Normal+3 (with and without age/vacc gate)
  - Keep-monitoring (below threshold)
  - Edge cases (right at threshold; right under threshold)
  - Sensitivity to the two parameterised clinical ambiguities

Each scenario is labeled with the EXPECTED outcome based on Emmanuel's
decision tree; the engine's actual outcome is compared and discrepancies
are flagged for review.
"""

import json
import os
import sys
from dataclasses import asdict

# Allow running from repo root or from the validation/ folder
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "engine"))

from cocci_engine import (
    FlockObservation, Droppings, HunchedPosture, FeedDeviation,
    WaterChange, AgeBand, Vaccination, Mortality, Litter,
    Triage, triage, format_result,
)


def obs(**overrides) -> FlockObservation:
    """Build a FlockObservation with sensible 'healthy' defaults, then apply overrides."""
    base = dict(
        fresh_blood_in_droppings=False,
        orange_mucus_or_sloughed_tissue=False,
        droppings_consistency=Droppings.NORMAL,
        hunched_posture=HunchedPosture.NONE,
        huddling_despite_temperature=False,
        paleness_or_depigmentation=False,
        feed_intake_deviation=FeedDeviation.AT_OR_ABOVE,
        water_consumption_change=WaterChange.NORMAL,
        flock_age=AgeBand.THREE_TO_8W,
        coccidiosis_vaccinated_at_hatchery=Vaccination.YES,
        on_coccidiostat_program=True,
        mortality_trend=Mortality.NONE,
        litter_condition=Litter.DRY,
        leaking_or_misaligned_drinkers=False,
    )
    base.update(overrides)
    return FlockObservation(**base)


# Each scenario: (id, narrative, observation, expected_outcome)
SCENARIOS = [
    # ===== EMERGENCY TRIGGERS =====
    ("E1", "Fresh blood visible in droppings, otherwise healthy-looking flock",
     obs(fresh_blood_in_droppings=True), Triage.EMERGENCY),

    ("E2", "Orange mucus / sloughed intestinal tissue observed",
     obs(orange_mucus_or_sloughed_tissue=True), Triage.EMERGENCY),

    ("E3", "Sudden mortality spike with no other major signs",
     obs(mortality_trend=Mortality.SUDDEN_SPIKE), Triage.EMERGENCY),

    ("E4", "Severe diarrhea + widespread hunched posture",
     obs(droppings_consistency=Droppings.SEVERE_DIARRHEA,
         hunched_posture=HunchedPosture.WIDESPREAD), Triage.EMERGENCY),

    ("E5", "Severe diarrhea + significant feed drop",
     obs(droppings_consistency=Droppings.SEVERE_DIARRHEA,
         feed_intake_deviation=FeedDeviation.SIGNIFICANT_DROP), Triage.EMERGENCY),

    ("E6", "Severe diarrhea + paleness",
     obs(droppings_consistency=Droppings.SEVERE_DIARRHEA,
         paleness_or_depigmentation=True), Triage.EMERGENCY),

    ("E7", "Severe diarrhea + widespread huddling",
     obs(droppings_consistency=Droppings.SEVERE_DIARRHEA,
         huddling_despite_temperature=True), Triage.EMERGENCY),

    ("E8", "Severe diarrhea + significant water drop",
     obs(droppings_consistency=Droppings.SEVERE_DIARRHEA,
         water_consumption_change=WaterChange.SIGNIFICANT), Triage.EMERGENCY),

    ("E9", "Multiple emergency signs (blood + spike + severe diarrhea)",
     obs(fresh_blood_in_droppings=True,
         mortality_trend=Mortality.SUDDEN_SPIKE,
         droppings_consistency=Droppings.SEVERE_DIARRHEA,
         paleness_or_depigmentation=True), Triage.EMERGENCY),

    # ===== ACT NOW: SEVERE DIARRHEA + ≥1 SUPPORTING SIGN (NO MAJOR SYSTEMIC) =====
    ("A1", "Severe diarrhea + leaking drinkers (no emergency systemic signs)",
     obs(droppings_consistency=Droppings.SEVERE_DIARRHEA,
         leaking_or_misaligned_drinkers=True), Triage.ACT_NOW),

    ("A2", "Severe diarrhea + damp litter only",
     obs(droppings_consistency=Droppings.SEVERE_DIARRHEA,
         litter_condition=Litter.DAMP), Triage.ACT_NOW),

    ("A3", "Severe diarrhea + slight (not significant) feed drop",
     obs(droppings_consistency=Droppings.SEVERE_DIARRHEA,
         feed_intake_deviation=FeedDeviation.SLIGHT_DROP), Triage.ACT_NOW),

    # ===== ACT NOW: LOOSE DROPPINGS + ≥2 SUPPORTING SIGNS =====
    ("A4", "Loose droppings + damp litter + leaking drinkers",
     obs(droppings_consistency=Droppings.LOOSE,
         litter_condition=Litter.DAMP,
         leaking_or_misaligned_drinkers=True), Triage.ACT_NOW),

    ("A5", "Loose droppings + gradual mortality + feed drop",
     obs(droppings_consistency=Droppings.LOOSE,
         mortality_trend=Mortality.GRADUAL,
         feed_intake_deviation=FeedDeviation.SLIGHT_DROP), Triage.ACT_NOW),

    ("A6", "Loose droppings + widespread hunched + huddling",
     obs(droppings_consistency=Droppings.LOOSE,
         hunched_posture=HunchedPosture.WIDESPREAD,
         huddling_despite_temperature=True), Triage.ACT_NOW),

    ("A7", "Loose droppings + young chicks unvaccinated (immune-naive risk)",
     obs(droppings_consistency=Droppings.LOOSE,
         flock_age=AgeBand.UNDER_3W,
         coccidiosis_vaccinated_at_hatchery=Vaccination.NO), Triage.ACT_NOW),

    # ===== ACT NOW: NORMAL DROPPINGS + ≥3 SUPPORTING SIGNS =====
    ("A8", "Normal droppings + 3 wet-environment signs",
     obs(litter_condition=Litter.HEAVILY_CAKED_WET,
         leaking_or_misaligned_drinkers=True,
         flock_age=AgeBand.UNDER_3W), Triage.ACT_NOW),

    ("A9", "Normal droppings + 3 management gaps",
     obs(coccidiosis_vaccinated_at_hatchery=Vaccination.UNKNOWN,
         on_coccidiostat_program=False,
         litter_condition=Litter.DAMP), Triage.ACT_NOW),

    ("A10", "Normal droppings + 4 signs incl. gradual mortality",
     obs(mortality_trend=Mortality.GRADUAL,
         flock_age=AgeBand.UNDER_3W,
         on_coccidiostat_program=False,
         litter_condition=Litter.DAMP), Triage.ACT_NOW),

    # ===== KEEP MONITORING: BELOW THRESHOLD =====
    ("K1", "Completely healthy flock",
     obs(), Triage.KEEP_MONITORING),

    ("K2", "Loose droppings + only 1 supporting sign (below threshold of 2)",
     obs(droppings_consistency=Droppings.LOOSE,
         litter_condition=Litter.DAMP), Triage.KEEP_MONITORING),

    ("K3", "Normal droppings + 2 supporting signs (below threshold of 3)",
     obs(on_coccidiostat_program=False,
         litter_condition=Litter.DAMP), Triage.KEEP_MONITORING),

    ("K4", "Isolated hunched posture only (doesn't count as widespread sign)",
     obs(hunched_posture=HunchedPosture.ISOLATED), Triage.KEEP_MONITORING),

    ("K5", "Slight water drop only — single sign, not enough",
     obs(water_consumption_change=WaterChange.SLIGHT), Triage.KEEP_MONITORING),

    # ===== EDGE: AT-THRESHOLD CASES =====
    ("EDGE1", "Loose + exactly 2 signs (at threshold)",
     obs(droppings_consistency=Droppings.LOOSE,
         litter_condition=Litter.DAMP,
         on_coccidiostat_program=False), Triage.ACT_NOW),

    ("EDGE2", "Normal + exactly 3 signs (at threshold)",
     obs(on_coccidiostat_program=False,
         coccidiosis_vaccinated_at_hatchery=Vaccination.NO,
         litter_condition=Litter.DAMP), Triage.ACT_NOW),

    ("EDGE3", "Severe diarrhea + zero other signs — should NOT escalate to Emergency,"
              " but should still Act Now (severe diarrhea + 1 supporting sign needs 1)",
     obs(droppings_consistency=Droppings.SEVERE_DIARRHEA), Triage.KEEP_MONITORING),
     # NOTE: This is a clinical question for Emmanuel. The tree says "+1 supporting
     # sign" for severe diarrhea to trigger Act Now. With zero signs and no emergency
     # systemic signs, default falls to Keep Monitoring. Is this the intended behaviour?

    # ===== ROUTINE-MANAGEMENT BACKGROUND CASES =====
    ("R1", "Older flock, vaccinated, healthy environment, mild paleness only",
     obs(flock_age=AgeBand.OVER_8W, paleness_or_depigmentation=True),
     Triage.KEEP_MONITORING),

    ("R2", "Young chicks, unvaccinated, dry well-managed environment",
     obs(flock_age=AgeBand.UNDER_3W,
         coccidiosis_vaccinated_at_hatchery=Vaccination.NO,
         on_coccidiostat_program=False), Triage.ACT_NOW),
     # NOTE: 3 supporting signs (under_3w + unvacc + no coccidiostat) + Normal droppings.
     # This tests the age/vacc gate clarification. Default (gate=False): Act Now.

    # ===== PARAMETER SENSITIVITY TESTS =====
    ("P1", "Loose droppings + 1 other sign — depends on loose_double_count",
     obs(droppings_consistency=Droppings.LOOSE,
         litter_condition=Litter.DAMP), Triage.KEEP_MONITORING),
     # With loose_double_count=False (default): 1 sign, below threshold. Keep Monitoring.
     # With loose_double_count=True: 2 signs, at threshold. Act Now.
     # Default behaviour expected here.

    ("P2", "Older vaccinated flock with 3 management-only signs — tests age/vacc gate",
     obs(flock_age=AgeBand.OVER_8W,
         coccidiosis_vaccinated_at_hatchery=Vaccination.YES,
         on_coccidiostat_program=False,
         litter_condition=Litter.DAMP,
         leaking_or_misaligned_drinkers=True), Triage.ACT_NOW),
     # With age_vacc_hard_gate=False (default): 3 signs, Act Now.
     # With age_vacc_hard_gate=True: hard-gated to Keep Monitoring.
     # Default behaviour expected here.
]


# ----------------------------------------------------------------------
# Run validation
# ----------------------------------------------------------------------

def run_validation():
    print("=" * 78)
    print("CocciAlert Rule Engine — Synthetic Scenario Validation")
    print("32 scenarios spanning the decision space")
    print("=" * 78)

    results = []
    matches = 0

    for sid, narrative, observation, expected in SCENARIOS:
        actual = triage(observation)
        match = actual.outcome == expected
        if match:
            matches += 1
            marker = "✓"
        else:
            marker = "✗ MISMATCH"

        results.append({
            "scenario_id": sid,
            "narrative": narrative,
            "expected": expected.value,
            "actual": actual.outcome.value,
            "match": match,
            "supporting_signs_count": actual.supporting_signs_count,
            "supporting_signs": actual.supporting_signs_present,
            "triggers": actual.triggers_matched,
            "rationale": actual.rationale,
        })

        print(f"{marker}  [{sid}] {narrative[:60]}")
        print(f"     Expected: {expected.value:30s}  Actual: {actual.outcome.value}")
        if not match:
            print(f"     >>> {actual.rationale}")

    print()
    print("=" * 78)
    print(f"Summary: {matches}/{len(SCENARIOS)} scenarios match expected outcomes.")
    print("=" * 78)

    # Output distribution
    from collections import Counter
    outcomes = Counter(r["actual"] for r in results)
    print("\nOutcome distribution across the synthetic scenario set:")
    for outcome, count in outcomes.most_common():
        pct = 100 * count / len(results)
        print(f"  {outcome:35s} {count:3d}  ({pct:.1f}%)")

    # Persist for Emmanuel's review
    with open("cocci_validation_run.json", "w") as f:
        json.dump({
            "total_scenarios": len(SCENARIOS),
            "matches": matches,
            "outcome_distribution": dict(outcomes),
            "results": results,
        }, f, indent=2)
    print("\nFull results written to cocci_validation_run.json")


if __name__ == "__main__":
    run_validation()
