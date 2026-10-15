"""Simulate 340-patient clinical trial data with raw fields needed to
derive the primary, secondary, and safety endpoints -- the real inputs
an endpoint-validation framework has to independently re-derive and
check, not a dataset where the endpoint is already computed."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_PATIENTS = 340
SEED = 281


def simulate(n: int = N_PATIENTS, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    baseline_score = rng.normal(50, 10, n)
    week12_score = baseline_score - rng.normal(8, 6, n)  # improvement over time
    treatment = rng.choice(["Active", "Placebo"], n)
    week12_score -= np.where(treatment == "Active", rng.normal(3, 2, n), 0)  # real treatment effect

    time_to_event_days = rng.exponential(120, n).clip(1, 365)
    event_observed = rng.binomial(1, 0.35, n)
    ae_grade = rng.choice([0, 1, 2, 3, 4], n, p=[0.5, 0.25, 0.15, 0.08, 0.02])

    df = pd.DataFrame({
        "patient_id": [f"PT-{i:04d}" for i in range(n)],
        "treatment": treatment, "baseline_score": np.round(baseline_score, 2),
        "week12_score": np.round(week12_score, 2),
        "time_to_event_days": np.round(time_to_event_days, 1), "event_observed": event_observed,
        "ae_grade": ae_grade,
    })

    # realistic missingness in week12 score (patient discontinuation)
    missing_idx = rng.choice(df.index, size=int(n * 0.03), replace=False)
    df.loc[missing_idx, "week12_score"] = np.nan

    return df


if __name__ == "__main__":
    df = simulate()
    print(df.shape)
