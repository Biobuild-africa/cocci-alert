"""
CocciAlert — Integration Demo
TRL 4 evidence: rule engine + farmer-facing flow + anonymized event log

This script demonstrates the end-to-end controlled-prototype flow:

  Farmer answers questions  →  Rule engine produces triage
  → Anonymized event-log record written to CSV
  → Aggregated for FCI4Africa Food Systems Dashboard upload

Run from CLI:
    python3 integration_demo.py            # demo on one synthetic farmer
    python3 integration_demo.py --batch 50 # generate 50 synthetic records
"""

import argparse
import csv
import hashlib
import json
import os
import random
import sys
import uuid
from dataclasses import asdict
from datetime import datetime, timezone, timedelta

# Allow running from repo root or from the integration/ folder
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "..", "engine"))

from cocci_engine import (
    FlockObservation, Droppings, HunchedPosture, FeedDeviation,
    WaterChange, AgeBand, Vaccination, Mortality, Litter,
    Triage, triage,
)


# ----------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------

ENGINE_VERSION = "0.1.0"
SCHEMA_VERSION = "0.1.0"

# Nigerian state + LGA codes (aggregated, no farmer-level geocoding ever)
NIGERIAN_LGAS = [
    ("NG-OY", "NG-OY-IBN", "Ibadan North"),
    ("NG-OY", "NG-OY-ASW", "Akinyele"),
    ("NG-OY", "NG-OY-MNY", "Moniya"),
    ("NG-OY", "NG-OY-SAK", "Saki East"),
    ("NG-OY", "NG-OY-ISY", "Iseyin"),
    ("NG-OG", "NG-OG-ABE", "Abeokuta North"),
    ("NG-OG", "NG-OG-IJB", "Ijebu Ode"),
    ("NG-KW", "NG-KW-ILR", "Ilorin South"),
    ("NG-OS", "NG-OS-OSG", "Osogbo"),
    ("NG-LA", "NG-LA-EPE", "Epe"),
    ("NG-OY", "NG-OY-EGB", "Egbeda"),
    ("NG-OY", "NG-OY-LGV", "Lagelu"),
]

CHANNELS = ["ussd", "whatsapp"]
LANGUAGES = ["yo", "en"]   # Yoruba, English (Hausa/Igbo for later cohorts)


# ----------------------------------------------------------------------
# Privacy-preserving identifier handling
# ----------------------------------------------------------------------

def hash_user_identifier(raw_identifier: str, salt: str) -> str:
    """Generate an anonymized user ID from a raw identifier (phone number, etc).

    Uses SHA-256 with a per-deployment salt. The salt is rotated periodically
    so the hash cannot be used to track a farmer across long time spans.
    The raw_identifier is NEVER stored anywhere — only the hash leaves this
    function. The salt is held server-side, never exposed in logs.
    """
    digest = hashlib.sha256((raw_identifier + salt).encode()).hexdigest()
    return str(uuid.UUID(digest[:32]))


# ----------------------------------------------------------------------
# Map observation + result → schema-compliant log row
# ----------------------------------------------------------------------

# Map UI codes to engine enums (lowercase, snake_case for storage)
SIGN_CODES = {
    "Birds hunched with ruffled feathers (widespread)": "hunched_wide",
    "Birds huddling despite adequate ambient temperature": "huddling",
    "Noticeable paleness or depigmentation": "paleness",
    "Feed intake below expected growth curve": "feed_drop",
    "Water consumption dropped below normal": "water_drop",
    "Flock is < 3 weeks old (immune naivety)": "age_under_3wk",
    "Coccidiosis vaccination absent / unknown": "vacc_absent",
    "Not on dietary coccidiostat program": "no_coccidiostat",
    "Daily mortality gradually rising above baseline": "mort_gradual",
    "Litter damp or heavily caked and wet": "litter_wet",
    "Misaligned / leaking drinkers creating wet spots": "drinkers_leak",
    "Predominant droppings are loose": "droppings_loose_sign",
}

EMERGENCY_CODES = {
    "Fresh blood visible in droppings": "fresh_blood",
    "Orange mucus or sloughed intestinal tissue": "orange_mucus",
    "Sudden mortality spike": "sudden_spike",
}


def flock_size_band(n: int) -> str:
    if n < 50:    return "tiny"
    if n <= 200:  return "small"
    if n <= 500:  return "medium"
    return "large"


def bird_age_to_band(age: AgeBand) -> str:
    return {
        AgeBand.UNDER_3W: "under_3wk",
        AgeBand.THREE_TO_8W: "3_to_8wk",
        AgeBand.OVER_8W: "over_8wk",
    }[age]


def triage_outcome_code(t: Triage) -> str:
    return {
        Triage.EMERGENCY: "emergency",
        Triage.ACT_NOW: "act_now",
        Triage.KEEP_MONITORING: "keep_monitoring",
    }[t]


def triage_rationale_code(t: Triage, obs: FlockObservation, n_signs: int) -> str:
    """Auditable rule-fire code so we can reconstruct WHY the engine decided."""
    if t == Triage.EMERGENCY:
        return "emergency_trigger_matched"
    if t == Triage.KEEP_MONITORING:
        return "below_threshold"
    if obs.droppings_consistency == Droppings.SEVERE_DIARRHEA:
        return "severe_diarrhea_plus_1_sign"
    if obs.droppings_consistency == Droppings.LOOSE:
        return "loose_plus_2_signs"
    return "normal_plus_3_signs"


def build_log_row(
    obs: FlockObservation,
    flock_size_n: int,
    bird_type: str,
    state_code: str,
    lga_code: str,
    channel: str,
    language: str,
    consent_data_sharing: bool,
    consent_method: str,
    anonymized_user_id: str,
    session_id: str,
    timestamp_utc: str,
    consent_timestamp_utc: str,
    loose_double_count: bool = False,
    age_vacc_hard_gate: bool = False,
) -> dict:
    """Run engine + emit a schema-compliant row."""
    result = triage(obs,
                    loose_double_count=loose_double_count,
                    age_vacc_hard_gate=age_vacc_hard_gate)

    emergency_codes = [
        EMERGENCY_CODES.get(t.split(" WITH")[0], "compound_severe_diarrhea")
        for t in result.triggers_matched
    ]
    sign_codes = [
        SIGN_CODES.get(s, "unknown_sign") for s in result.supporting_signs_present
    ]

    return {
        "event_id": str(uuid.uuid4()),
        "session_id": session_id,
        "timestamp_utc": timestamp_utc,
        "anonymized_user_id": anonymized_user_id,
        "consent_data_sharing": str(consent_data_sharing).lower(),
        "consent_method": consent_method,
        "consent_timestamp_utc": consent_timestamp_utc,
        "state_code": state_code,
        "lga_code": lga_code,
        "channel": channel,
        "language": language,
        "flock_size_band": flock_size_band(flock_size_n),
        "bird_type": bird_type,
        "bird_age_band": bird_age_to_band(obs.flock_age),
        "vaccination_coccidiosis": obs.coccidiosis_vaccinated_at_hatchery.value.lower(),
        "on_coccidiostat_program": str(obs.on_coccidiostat_program).lower(),
        "droppings_consistency": obs.droppings_consistency.name.lower(),
        "emergency_signs_present": "|".join(emergency_codes),
        "supporting_signs_count": result.supporting_signs_count,
        "supporting_signs_codes": "|".join(sign_codes),
        "litter_condition": obs.litter_condition.name.lower(),
        "mortality_trend": obs.mortality_trend.name.lower(),
        "triage_outcome": triage_outcome_code(result.outcome),
        "triage_rationale_code": triage_rationale_code(
            result.outcome, obs, result.supporting_signs_count
        ),
        "referral_made": str(result.outcome != Triage.KEEP_MONITORING).lower(),
        "engine_version": ENGINE_VERSION,
        "schema_version": SCHEMA_VERSION,
        "loose_double_count_param": str(loose_double_count).lower(),
        "age_vacc_hard_gate_param": str(age_vacc_hard_gate).lower(),
    }


# ----------------------------------------------------------------------
# Synthetic batch generator (for the 50-row sample dataset)
# ----------------------------------------------------------------------

def random_observation(rng: random.Random) -> tuple:
    """Generate one synthetic flock observation with realistic distributions.
    Returns (observation, flock_size_n, bird_type)."""
    # 15% high-risk cluster, 50% medium, 35% low (mirror PFSI distribution)
    cluster = rng.random()

    if cluster < 0.15:  # high-risk
        obs = FlockObservation(
            fresh_blood_in_droppings=rng.random() < 0.3,
            orange_mucus_or_sloughed_tissue=rng.random() < 0.1,
            droppings_consistency=rng.choice([Droppings.LOOSE, Droppings.SEVERE_DIARRHEA, Droppings.SEVERE_DIARRHEA]),
            hunched_posture=rng.choice([HunchedPosture.WIDESPREAD, HunchedPosture.WIDESPREAD, HunchedPosture.ISOLATED]),
            huddling_despite_temperature=rng.random() < 0.5,
            paleness_or_depigmentation=rng.random() < 0.5,
            feed_intake_deviation=rng.choice([FeedDeviation.SIGNIFICANT_DROP, FeedDeviation.SLIGHT_DROP]),
            water_consumption_change=rng.choice([WaterChange.SIGNIFICANT, WaterChange.SLIGHT]),
            flock_age=rng.choice([AgeBand.UNDER_3W, AgeBand.THREE_TO_8W]),
            coccidiosis_vaccinated_at_hatchery=rng.choice([Vaccination.NO, Vaccination.UNKNOWN]),
            on_coccidiostat_program=False,
            mortality_trend=rng.choice([Mortality.SUDDEN_SPIKE, Mortality.GRADUAL, Mortality.GRADUAL]),
            litter_condition=rng.choice([Litter.HEAVILY_CAKED_WET, Litter.DAMP]),
            leaking_or_misaligned_drinkers=rng.random() < 0.7,
        )
    elif cluster < 0.65:  # medium-risk
        obs = FlockObservation(
            fresh_blood_in_droppings=False,
            orange_mucus_or_sloughed_tissue=False,
            droppings_consistency=rng.choice([Droppings.LOOSE, Droppings.LOOSE, Droppings.NORMAL]),
            hunched_posture=rng.choice([HunchedPosture.NONE, HunchedPosture.ISOLATED, HunchedPosture.WIDESPREAD]),
            huddling_despite_temperature=rng.random() < 0.2,
            paleness_or_depigmentation=rng.random() < 0.15,
            feed_intake_deviation=rng.choice([FeedDeviation.SLIGHT_DROP, FeedDeviation.AT_OR_ABOVE]),
            water_consumption_change=rng.choice([WaterChange.NORMAL, WaterChange.SLIGHT]),
            flock_age=rng.choice([AgeBand.THREE_TO_8W, AgeBand.OVER_8W, AgeBand.UNDER_3W]),
            coccidiosis_vaccinated_at_hatchery=rng.choice([Vaccination.YES, Vaccination.UNKNOWN, Vaccination.NO]),
            on_coccidiostat_program=rng.random() < 0.4,
            mortality_trend=rng.choice([Mortality.NONE, Mortality.GRADUAL]),
            litter_condition=rng.choice([Litter.DAMP, Litter.DRY, Litter.DAMP]),
            leaking_or_misaligned_drinkers=rng.random() < 0.3,
        )
    else:  # low-risk / well-managed
        obs = FlockObservation(
            fresh_blood_in_droppings=False,
            orange_mucus_or_sloughed_tissue=False,
            droppings_consistency=Droppings.NORMAL,
            hunched_posture=HunchedPosture.NONE,
            huddling_despite_temperature=False,
            paleness_or_depigmentation=False,
            feed_intake_deviation=FeedDeviation.AT_OR_ABOVE,
            water_consumption_change=WaterChange.NORMAL,
            flock_age=rng.choice([AgeBand.THREE_TO_8W, AgeBand.OVER_8W]),
            coccidiosis_vaccinated_at_hatchery=Vaccination.YES,
            on_coccidiostat_program=True,
            mortality_trend=Mortality.NONE,
            litter_condition=Litter.DRY,
            leaking_or_misaligned_drinkers=False,
        )

    flock_size = rng.choice([
        rng.randint(15, 49),
        rng.randint(50, 200),
        rng.randint(50, 200),
        rng.randint(201, 500),
        rng.randint(501, 1200),
    ])
    bird_type = rng.choice(["layer", "broiler", "broiler", "dual_purpose", "indigenous"])
    return obs, flock_size, bird_type


def generate_batch(n: int, seed: int = 42) -> list:
    """Generate n synthetic records using a small pool of recurring farmers."""
    rng = random.Random(seed)
    salt = "DEMO_SALT_2026_OY"  # in production, rotated per cooperative
    # 18 distinct farmers across the LGAs — some repeat across sessions
    farmer_phones = [f"+23480{rng.randint(10000000, 99999999)}" for _ in range(18)]
    base_time = datetime(2026, 6, 1, 7, 0, 0, tzinfo=timezone.utc)

    rows = []
    for i in range(n):
        obs, flock_size, bird_type = random_observation(rng)
        phone = rng.choice(farmer_phones)
        state, lga, _ = rng.choice(NIGERIAN_LGAS)

        # 92% consent rate; non-consenting events are still logged for engine QA
        # but the dataset published to FCI4Africa filters consent_data_sharing=true
        consent = rng.random() < 0.92

        ts = base_time + timedelta(hours=i * 3 + rng.randint(0, 5))
        consent_ts = ts - timedelta(seconds=rng.randint(20, 90))

        row = build_log_row(
            obs=obs,
            flock_size_n=flock_size,
            bird_type=bird_type,
            state_code=state,
            lga_code=lga,
            channel=rng.choice(CHANNELS),
            language=rng.choice(LANGUAGES),
            consent_data_sharing=consent,
            consent_method=rng.choice(["ussd_opt_in", "whatsapp_button", "voice_confirm"]),
            anonymized_user_id=hash_user_identifier(phone, salt),
            session_id=str(uuid.uuid4()),
            timestamp_utc=ts.isoformat().replace("+00:00", "Z"),
            consent_timestamp_utc=consent_ts.isoformat().replace("+00:00", "Z"),
        )
        rows.append(row)
    return rows


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def write_csv(rows: list, path: str):
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def demo_one():
    """Single-farmer interaction demo: input → engine → log row."""
    print("=" * 72)
    print("CocciAlert Integration Demo — Single Farmer Session")
    print("=" * 72)

    # Simulated farmer in Moniya, Oyo State, calling USSD
    obs = FlockObservation(
        fresh_blood_in_droppings=False,
        orange_mucus_or_sloughed_tissue=False,
        droppings_consistency=Droppings.LOOSE,
        hunched_posture=HunchedPosture.WIDESPREAD,
        huddling_despite_temperature=True,
        paleness_or_depigmentation=False,
        feed_intake_deviation=FeedDeviation.SLIGHT_DROP,
        water_consumption_change=WaterChange.NORMAL,
        flock_age=AgeBand.UNDER_3W,
        coccidiosis_vaccinated_at_hatchery=Vaccination.NO,
        on_coccidiostat_program=False,
        mortality_trend=Mortality.NONE,
        litter_condition=Litter.DAMP,
        leaking_or_misaligned_drinkers=True,
    )

    result = triage(obs)
    print(f"\nFarmer reports: 120 broiler chicks, 2 weeks old, in Moniya LGA")
    print(f"USSD interaction, Yoruba language")
    print(f"\nEngine triage decision: {result.outcome.value}")
    print(f"Rationale: {result.rationale}")
    print(f"Supporting signs detected: {result.supporting_signs_count}")
    for s in result.supporting_signs_present:
        print(f"  • {s}")
    print(f"\nAction message to farmer (paraphrased): {result.action_message}")

    # Build the log row that this event generates
    now = datetime.now(timezone.utc)
    row = build_log_row(
        obs=obs,
        flock_size_n=120,
        bird_type="broiler",
        state_code="NG-OY",
        lga_code="NG-OY-MNY",
        channel="ussd",
        language="yo",
        consent_data_sharing=True,
        consent_method="ussd_opt_in",
        anonymized_user_id=hash_user_identifier("+2348012345678", "DEMO_SALT_2026_OY"),
        session_id=str(uuid.uuid4()),
        timestamp_utc=now.isoformat().replace("+00:00", "Z"),
        consent_timestamp_utc=(now - timedelta(seconds=45)).isoformat().replace("+00:00", "Z"),
    )
    print("\nEvent-log row written to FCI4Africa-aligned schema:")
    print(json.dumps(row, indent=2))
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, default=0,
                    help="Generate N synthetic records into sample_event_log_N.csv")
    args = ap.parse_args()

    if args.batch > 0:
        rows = generate_batch(args.batch)
        path = f"sample_event_log_{args.batch}.csv"
        write_csv(rows, path)
        print(f"Wrote {len(rows)} synthetic anonymized records to {path}")
        print()
        # Quick summary
        from collections import Counter
        outcomes = Counter(r["triage_outcome"] for r in rows)
        lgas = Counter(r["lga_code"] for r in rows)
        channels = Counter(r["channel"] for r in rows)
        langs = Counter(r["language"] for r in rows)
        consents = Counter(r["consent_data_sharing"] for r in rows)

        print("Triage outcomes:")
        for k, v in outcomes.most_common():
            print(f"  {k:25s} {v:3d}  ({100*v/len(rows):.1f}%)")
        print(f"\nGeographic coverage: {len(lgas)} LGAs across {len({l.split('-')[1] for l in lgas})} states")
        print(f"Channels: {dict(channels)}")
        print(f"Languages: {dict(langs)}")
        print(f"Consent rate: {100 * consents['true'] / len(rows):.1f}%")
    else:
        demo_one()


if __name__ == "__main__":
    main()
