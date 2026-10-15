"""Real endpoint derivation logic for the 3 standard clinical trial
endpoint types: primary (continuous change-from-baseline), secondary
(binary responder), and safety (treatment-emergent adverse event
severity) -- genuine derivation functions, not placeholders."""
from __future__ import annotations

import pandas as pd

RESPONDER_THRESHOLD = 10.0  # change-from-baseline required to be a "responder"


def derive_primary_endpoint(df: pd.DataFrame) -> pd.Series:
    """Change from baseline at week 12 (primary efficacy endpoint)."""
    return df["baseline_score"] - df["week12_score"]


def derive_secondary_endpoint(df: pd.DataFrame, chg: pd.Series) -> pd.Series:
    """Binary responder endpoint: improvement >= threshold."""
    return (chg >= RESPONDER_THRESHOLD).astype("Int64").where(chg.notna())


def derive_safety_endpoint(df: pd.DataFrame) -> pd.Series:
    """Treatment-emergent serious adverse event: grade >= 3."""
    return (df["ae_grade"] >= 3).astype(int)


def derive_all_endpoints(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["chg_from_baseline"] = derive_primary_endpoint(out)
    out["responder"] = derive_secondary_endpoint(out, out["chg_from_baseline"])
    out["serious_ae"] = derive_safety_endpoint(out)
    return out


if __name__ == "__main__":
    from .simulate_trial_data import simulate

    df = simulate()
    derived = derive_all_endpoints(df)
    print(derived[["chg_from_baseline", "responder", "serious_ae"]].describe())
