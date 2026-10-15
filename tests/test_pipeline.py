import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.simulate_trial_data import simulate
from src.endpoint_derivation import derive_all_endpoints
from src.validation import validate_endpoint_accuracy


def test_cohort_has_340_patients():
    df = simulate()
    assert len(df) == 340


def test_missingness_is_realistic():
    df = simulate()
    missing_frac = df["week12_score"].isna().mean()
    assert 0.0 < missing_frac < 0.10


def test_derived_endpoints_present():
    df = simulate()
    derived = derive_all_endpoints(df)
    for col in ["chg_from_baseline", "responder", "serious_ae"]:
        assert col in derived.columns


def test_endpoint_validation_overall_accuracy_high():
    df = simulate()
    derived = derive_all_endpoints(df)
    result = validate_endpoint_accuracy(derived)
    assert result["overall_accuracy_pct"] >= 99.0


def test_safety_endpoint_matches_grade_rule():
    df = simulate()
    derived = derive_all_endpoints(df)
    assert (derived.loc[derived["ae_grade"] >= 3, "serious_ae"] == 1).all()
    assert (derived.loc[derived["ae_grade"] < 3, "serious_ae"] == 0).all()
