"""
CocciAlert — Coccidiosis Screening Rule Engine
TRL 3 Prototype v0.1

Direct encoding of Emmanuel's clinical decision tree (Coccidiosis_decision_tree.docx).
This engine produces deterministic triage outputs from 14 bounded inputs.

Outputs: EMERGENCY | ACT_NOW | KEEP_MONITORING
Register: triage-only. Never recommends a specific drug or dose. Emergency
escalations always say "contact a veterinarian."

Two clinical clarifications are parameterised so Emmanuel can flip the
convention without code change:

  loose_double_count : whether "Predominant droppings are loose" is counted
    as a supporting sign when Q3 = Loose (default: False, to avoid
    double-counting the gating variable).

  age_vacc_hard_gate : whether the "especially when age < 3 weeks or
    vaccination absent/unknown" clause for the Normal-droppings pathway
    is a hard gate (must be true) or emphasis only (default: False,
    treated as emphasis).

Author: BioBuild Africa Ltd (RC 9604822)
Clinical logic: Dr. Emmanuel Alagbe Oluwabukunmi (animal science, poultry)
Engine implementation: Damilola / BioBuild Africa engineering
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


# ----------------------------------------------------------------------
# 1. Enumerated answer choices — match the question schema exactly
# ----------------------------------------------------------------------

class Droppings(Enum):
    NORMAL = "Normal (Firm)"
    LOOSE = "Loose"
    SEVERE_DIARRHEA = "Severe Diarrhea"

class HunchedPosture(Enum):
    WIDESPREAD = "Widespread (>10%)"
    ISOLATED = "Isolated (<10%)"
    NONE = "None"

class FeedDeviation(Enum):
    AT_OR_ABOVE = "At/Above Target"
    SLIGHT_DROP = "Slight Drop (<10%)"
    SIGNIFICANT_DROP = "Significant Drop (>10%)"

class WaterChange(Enum):
    NORMAL = "Normal"
    SLIGHT = "Slight Drop"
    SIGNIFICANT = "Significant Drop"

class AgeBand(Enum):
    UNDER_3W = "< 3 weeks"
    THREE_TO_8W = "3–8 weeks"
    OVER_8W = "> 8 weeks"

class Vaccination(Enum):
    YES = "Yes"
    NO = "No"
    UNKNOWN = "Unknown"

class Mortality(Enum):
    NONE = "No"
    GRADUAL = "Gradual Increase"
    SUDDEN_SPIKE = "Sudden Spike"

class Litter(Enum):
    DRY = "Dry & Friable"
    DAMP = "Damp"
    HEAVILY_CAKED_WET = "Heavily Caked & Wet"


# ----------------------------------------------------------------------
# 2. Input schema — one structure for all 14 questions
# ----------------------------------------------------------------------

@dataclass
class FlockObservation:
    # Emergency-only questions
    fresh_blood_in_droppings: bool          # Q1
    orange_mucus_or_sloughed_tissue: bool   # Q2

    # Gating + supporting variables
    droppings_consistency: Droppings        # Q3
    hunched_posture: HunchedPosture         # Q4
    huddling_despite_temperature: bool      # Q5
    paleness_or_depigmentation: bool        # Q6
    feed_intake_deviation: FeedDeviation    # Q7
    water_consumption_change: WaterChange   # Q8
    flock_age: AgeBand                      # Q9
    coccidiosis_vaccinated_at_hatchery: Vaccination  # Q10
    on_coccidiostat_program: bool           # Q11 (Yes = True)
    mortality_trend: Mortality              # Q12
    litter_condition: Litter                # Q13
    leaking_or_misaligned_drinkers: bool    # Q14


# ----------------------------------------------------------------------
# 3. Output schema
# ----------------------------------------------------------------------

class Triage(Enum):
    EMERGENCY = "Emergency"
    ACT_NOW = "Act now"
    KEEP_MONITORING = "Keep monitoring, no coccidiosis"


@dataclass
class TriageResult:
    outcome: Triage
    rationale: str
    triggers_matched: List[str] = field(default_factory=list)
    supporting_signs_present: List[str] = field(default_factory=list)
    supporting_signs_count: int = 0
    action_message: str = ""


# ----------------------------------------------------------------------
# 4. Emergency check — Section 1 of decision tree
# ----------------------------------------------------------------------

def emergency_check(obs: FlockObservation) -> Optional[TriageResult]:
    """Return Emergency triage if any emergency trigger is met, else None."""
    triggers = []

    if obs.fresh_blood_in_droppings:
        triggers.append("Fresh blood visible in droppings")
    if obs.orange_mucus_or_sloughed_tissue:
        triggers.append("Orange mucus or sloughed intestinal tissue")
    if obs.mortality_trend == Mortality.SUDDEN_SPIKE:
        triggers.append("Sudden mortality spike")

    # Severe diarrhea + any major systemic sign
    if obs.droppings_consistency == Droppings.SEVERE_DIARRHEA:
        major_systemic = []
        if obs.hunched_posture == HunchedPosture.WIDESPREAD:
            major_systemic.append("widespread hunched posture / ruffled feathers")
        if obs.feed_intake_deviation == FeedDeviation.SIGNIFICANT_DROP:
            major_systemic.append("significant drop in feed intake")
        if obs.water_consumption_change == WaterChange.SIGNIFICANT:
            major_systemic.append("significant drop in water consumption")
        if obs.paleness_or_depigmentation:
            major_systemic.append("noticeable paleness")
        if obs.huddling_despite_temperature:
            major_systemic.append("widespread huddling")
        if major_systemic:
            triggers.append(
                "Severe diarrhea WITH " + " + ".join(major_systemic)
            )

    if triggers:
        return TriageResult(
            outcome=Triage.EMERGENCY,
            rationale="One or more emergency triggers matched.",
            triggers_matched=triggers,
            action_message=(
                "EMERGENCY: contact a veterinary officer or approved agro-vet "
                "immediately. Remove wet litter, isolate severely affected birds, "
                "and ensure clean water is available. Do not self-medicate; "
                "wait for veterinary guidance on appropriate anticoccidial."
            ),
        )
    return None


# ----------------------------------------------------------------------
# 5. Supporting-sign tally — Section 2 of decision tree
# ----------------------------------------------------------------------

def collect_supporting_signs(
    obs: FlockObservation,
    loose_double_count: bool = False,
) -> List[str]:
    """Return the list of supporting signs that are POSITIVE for this flock.

    The 12 supporting signs from the decision tree. The 'Predominant droppings
    are loose' sign is treated as the gating variable by default and not
    counted again unless loose_double_count=True.
    """
    signs = []

    # 1. Predominant droppings are loose
    if obs.droppings_consistency == Droppings.LOOSE and loose_double_count:
        signs.append("Predominant droppings are loose")

    # 2. Hunched / ruffled (widespread weighted full; isolated NOT counted by default)
    if obs.hunched_posture == HunchedPosture.WIDESPREAD:
        signs.append("Birds hunched with ruffled feathers (widespread)")

    # 3. Huddling despite adequate temperature
    if obs.huddling_despite_temperature:
        signs.append("Birds huddling despite adequate ambient temperature")

    # 4. Paleness / depigmentation
    if obs.paleness_or_depigmentation:
        signs.append("Noticeable paleness or depigmentation")

    # 5. Feed intake drop below growth curve (any drop counts; significant counts strongly)
    if obs.feed_intake_deviation in (FeedDeviation.SLIGHT_DROP,
                                      FeedDeviation.SIGNIFICANT_DROP):
        signs.append("Feed intake below expected growth curve")

    # 6. Water consumption drop
    if obs.water_consumption_change in (WaterChange.SLIGHT,
                                          WaterChange.SIGNIFICANT):
        signs.append("Water consumption dropped below normal")

    # 7. Flock < 3 weeks old
    if obs.flock_age == AgeBand.UNDER_3W:
        signs.append("Flock is < 3 weeks old (immune naivety)")

    # 8. Not vaccinated for coccidiosis at hatchery (or unknown)
    if obs.coccidiosis_vaccinated_at_hatchery in (Vaccination.NO,
                                                    Vaccination.UNKNOWN):
        signs.append("Coccidiosis vaccination absent / unknown")

    # 9. Not on dietary coccidiostat program
    if not obs.on_coccidiostat_program:
        signs.append("Not on dietary coccidiostat program")

    # 10. Gradual mortality increase above baseline
    if obs.mortality_trend == Mortality.GRADUAL:
        signs.append("Daily mortality gradually rising above baseline")

    # 11. Litter damp or heavily caked
    if obs.litter_condition in (Litter.DAMP, Litter.HEAVILY_CAKED_WET):
        signs.append("Litter damp or heavily caked and wet")

    # 12. Leaking / misaligned drinkers creating wet spots
    if obs.leaking_or_misaligned_drinkers:
        signs.append("Misaligned / leaking drinkers creating wet spots")

    return signs


# ----------------------------------------------------------------------
# 6. Main triage routine
# ----------------------------------------------------------------------

def triage(
    obs: FlockObservation,
    loose_double_count: bool = False,
    age_vacc_hard_gate: bool = False,
) -> TriageResult:
    """Run the full decision tree on a single flock observation."""

    # Step 1: emergency short-circuit
    emergency = emergency_check(obs)
    if emergency is not None:
        # Even on emergency, collect supporting signs for dataset completeness
        emergency.supporting_signs_present = collect_supporting_signs(
            obs, loose_double_count=loose_double_count
        )
        emergency.supporting_signs_count = len(emergency.supporting_signs_present)
        return emergency

    # Step 2: tally supporting signs
    signs = collect_supporting_signs(obs, loose_double_count=loose_double_count)
    n = len(signs)

    # Step 3: gated thresholds against droppings consistency
    gating = obs.droppings_consistency

    if gating == Droppings.SEVERE_DIARRHEA:
        # Should have been caught as Emergency unless no major systemic signs;
        # tree text: "Severe diarrhea + 1 or more supporting signs → Act now"
        threshold = 1
        rule_used = "Severe diarrhea + ≥1 supporting sign"
    elif gating == Droppings.LOOSE:
        threshold = 2
        rule_used = "Loose droppings + ≥2 supporting signs"
    else:  # NORMAL
        threshold = 3
        rule_used = "Normal droppings + ≥3 supporting signs"
        # Optional hard gate on age/vaccination for the Normal pathway
        if age_vacc_hard_gate:
            young_or_unvacc = (
                obs.flock_age == AgeBand.UNDER_3W
                or obs.coccidiosis_vaccinated_at_hatchery in (
                    Vaccination.NO, Vaccination.UNKNOWN
                )
            )
            if not young_or_unvacc:
                # Hard-gate mode: even if ≥3 signs, do not escalate
                return TriageResult(
                    outcome=Triage.KEEP_MONITORING,
                    rationale=(
                        f"Normal droppings with {n} supporting signs, but age "
                        f"≥3 weeks AND vaccination present (hard-gate mode). "
                        f"Below the Act-now threshold."
                    ),
                    supporting_signs_present=signs,
                    supporting_signs_count=n,
                    action_message=(
                        "No coccidiosis triage indicated. Maintain biosecurity, "
                        "keep litter dry, monitor next 48 hours, and recheck "
                        "feed/water consumption daily."
                    ),
                )

    if n >= threshold:
        return TriageResult(
            outcome=Triage.ACT_NOW,
            rationale=f"Rule matched: {rule_used} ({n} signs present, threshold {threshold}).",
            supporting_signs_present=signs,
            supporting_signs_count=n,
            action_message=(
                "ACT NOW: high-risk pattern consistent with coccidiosis pressure. "
                "Immediate steps: remove and replace wet/caked litter, isolate "
                "severely affected birds, ensure clean water and shaded ventilation, "
                "and contact a veterinary officer or approved agro-vet for "
                "anticoccidial guidance consistent with national protocols. "
                "Do not self-prescribe drugs."
            ),
        )

    return TriageResult(
        outcome=Triage.KEEP_MONITORING,
        rationale=(
            f"Below Act-now threshold: {n} supporting signs vs threshold {threshold} "
            f"({rule_used.split(' + ')[0]} pathway)."
        ),
        supporting_signs_present=signs,
        supporting_signs_count=n,
        action_message=(
            "Keep monitoring. No coccidiosis triage indicated at this time. "
            "Maintain dry litter, biosecurity, and recheck droppings, feed and "
            "water consumption daily for the next 48 hours."
        ),
    )


# ----------------------------------------------------------------------
# 7. Convenience: pretty-printing a result
# ----------------------------------------------------------------------

def format_result(r: TriageResult) -> str:
    lines = [f"OUTCOME: {r.outcome.value}", f"Rationale: {r.rationale}"]
    if r.triggers_matched:
        lines.append("Emergency triggers:")
        for t in r.triggers_matched:
            lines.append(f"  • {t}")
    if r.supporting_signs_present:
        lines.append(f"Supporting signs present ({r.supporting_signs_count}):")
        for s in r.supporting_signs_present:
            lines.append(f"  • {s}")
    lines.append(f"Action: {r.action_message}")
    return "\n".join(lines)
