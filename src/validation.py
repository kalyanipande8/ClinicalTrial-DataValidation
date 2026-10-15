"""Independent-recomputation validation: re-derives each endpoint from
raw fields using a second, independently-written implementation and
checks agreement against the primary derivation -- the real test of
whether an endpoint-validation framework actually catches derivation
errors rather than trivially agreeing with itself."""
from __future__ import annotations

import pandas as pd


def independent_primary(df: pd.DataFrame) -> pd.Series:
    chg = []
    for _, row in df.iterrows():
        if pd.isna(row["week12_score"]):
            chg.append(float("nan"))
        else:
            chg.append(round(row["baseline_score"] - row["week12_score"], 6))
    return pd.Series(chg, index=df.index)


def independent_responder(chg: pd.Series, threshold: float = 10.0) -> pd.Series:
    out = []
    for v in chg:
        if pd.isna(v):
            out.append(pd.NA)
        else:
            out.append(1 if v >= threshold else 0)
    return pd.Series(out, index=chg.index, dtype="Int64")


def independent_serious_ae(df: pd.DataFrame) -> pd.Series:
    return pd.Series([1 if g >= 3 else 0 for g in df["ae_grade"]], index=df.index)


def validate_endpoint_accuracy(derived: pd.DataFrame) -> dict:
    """Compare the primary derivation against an independently-coded
    recomputation for each of the 3 endpoints, field by field."""
    indep_chg = independent_primary(derived)
    indep_resp = independent_responder(indep_chg)
    indep_ae = independent_serious_ae(derived)

    def match_rate(a: pd.Series, b: pd.Series) -> float:
        both_na = a.isna() & b.isna()
        eq = (a == b) | both_na
        return float(eq.mean())

    chg_match = match_rate(derived["chg_from_baseline"].round(6), indep_chg)
    resp_match = match_rate(derived["responder"], indep_resp)
    ae_match = match_rate(derived["serious_ae"], indep_ae)

    n_endpoints = 3
    overall = (chg_match + resp_match + ae_match) / n_endpoints

    return {
        "primary_endpoint_match_pct": round(chg_match * 100, 4),
        "secondary_endpoint_match_pct": round(resp_match * 100, 4),
        "safety_endpoint_match_pct": round(ae_match * 100, 4),
        "overall_accuracy_pct": round(overall * 100, 4),
        "n_patients": len(derived),
    }
