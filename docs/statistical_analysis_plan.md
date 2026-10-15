# Statistical Analysis Plan (SAP)

**Study:** Simulated 340-patient two-arm trial (Active vs. Placebo)
**Document type:** Statistical Analysis Plan
**Status:** Final

## 1. Objectives

- Primary: estimate the treatment effect on change from baseline in a
  continuous efficacy score at Week 12.
- Secondary: estimate the proportion of responders (patients achieving
  a clinically meaningful improvement) in each arm.
- Safety: characterize the incidence of serious (Grade >= 3) adverse
  events by treatment arm.

## 2. Population

All 340 randomized patients (intent-to-treat). Patients with missing
Week 12 assessments (approximately 3% of the cohort, due to early
discontinuation) are excluded from primary-endpoint analyses on a
per-endpoint basis (observed-cases analysis); their safety data remain
included through the day of last contact.

## 3. Endpoint definitions

| Endpoint | Type | Derivation |
|---|---|---|
| Primary | Continuous | `baseline_score - week12_score` |
| Secondary | Binary (responder) | Primary endpoint >= 10.0 points |
| Safety | Binary (serious AE) | `ae_grade >= 3` |

Full derivation logic is specified in `endpoint_derivation_spec.md` and
implemented in `src/endpoint_derivation.py`.

## 4. Statistical methods

- Primary and secondary endpoints are summarized descriptively by arm
  (mean/SD for the continuous endpoint, proportion for the responder
  endpoint).
- No formal hypothesis test is pre-specified in this simulated SAP;
  this project's focus is endpoint **derivation and validation**
  correctness, not inferential trial analysis.

## 5. Validation requirement

Every derived endpoint value must agree with an independently coded
re-derivation (`src/validation.py`) computed directly from raw fields.
Discrepancies are reported, not hidden, and the overall match rate is
the project's primary quality metric (see `data_validation_report.md`
for the real, measured result).
