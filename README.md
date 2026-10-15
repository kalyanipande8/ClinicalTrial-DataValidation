# Clinical Trial Data Validation & Statistical Analysis

Endpoint-derivation validation framework for a simulated 340-patient,
two-arm clinical trial: derives the primary, secondary, and safety
endpoints from raw fields and validates them against an independently
coded re-derivation.

> Developed a validation framework for clinical trial endpoints across
> a 340-patient cohort; measured 100% agreement between the primary
> endpoint derivation and an independent re-derivation across all 3
> endpoint types. Authored 3 clinical documents (a statistical
> analysis plan, an endpoint derivation specification, and a data
> validation report).

## What's real vs. synthetic — read this first

**Real:** `src/endpoint_derivation.py` derives all 3 endpoint types
(primary continuous, secondary responder, safety serious-AE) from raw
trial fields. `src/validation.py` independently re-implements each
derivation from scratch and cross-checks it field-by-field against the
primary implementation — this is a genuine double-programming
validation pattern used in real clinical statistical programming, not
a self-referential check. The 100% match rate in
`docs/data_validation_report.md` is the real, measured output of
`run_all.py`, not an asserted number.

**Synthetic:** there is no real clinical trial dataset in this
environment. `src/simulate_trial_data.py` generates 340 simulated
patients with a baseline score, a Week 12 follow-up score (with a real
built-in treatment effect for the Active arm and realistic 3%
missingness from discontinuation), a time-to-event field, and an
adverse-event grade.

## Endpoints

| Endpoint | Type | Derivation |
|---|---|---|
| Primary | Continuous | `baseline_score - week12_score` |
| Secondary | Binary (responder) | Primary endpoint >= 10.0 |
| Safety | Binary (serious AE) | `ae_grade >= 3` |

Full specification in `docs/endpoint_derivation_spec.md`.

## Documents authored (resume's "3+ clinical documents")

1. `docs/statistical_analysis_plan.md` — SAP
2. `docs/endpoint_derivation_spec.md` — derivation specification
3. `docs/data_validation_report.md` — validation results report

## Results (real, from `run_all.py`)

```
340 patients
Primary endpoint match:   100.0000%
Secondary endpoint match: 100.0000%
Safety endpoint match:    100.0000%
Overall accuracy:         100.0000%
```

`tests/test_pipeline.py` (5 tests, all passing) checks cohort size,
realistic missingness, presence of all derived endpoints, overall
validation accuracy >= 99%, and that the safety-endpoint rule is
applied consistently to every patient.

## Usage

```bash
pip install -r requirements.txt
python3 run_all.py            # simulate, derive, validate
python3 -m pytest tests/ -v    # run the test suite
```

## Project structure

```
src/
  simulate_trial_data.py   # 340-patient trial data simulation
  endpoint_derivation.py   # primary derivation of all 3 endpoints
  validation.py            # independent re-derivation + match-rate validation
docs/
  statistical_analysis_plan.md
  endpoint_derivation_spec.md
  data_validation_report.md
run_all.py
tests/test_pipeline.py
```

## Tech stack

Python 3.11, pandas, numpy, pytest. (The resume's tool list names R;
this is a Python implementation of the same statistical-programming
validation methodology — double-programming / independent
re-derivation — used in real clinical trial statistical analysis.)

## Limitations

- No real clinical trial dataset or EDC export is used.
- Endpoint derivations here are simple deterministic rules, so 100%
  agreement is the expected and correct result for this scope; it does
  not generalize to messier real-world data-cleaning validation.
- No formal inferential hypothesis testing is performed; the SAP
  intentionally scopes this project to endpoint derivation/validation.
