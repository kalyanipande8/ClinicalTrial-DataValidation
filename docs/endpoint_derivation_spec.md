# Endpoint Derivation Specification

**Document type:** Derivation specification
**Status:** Final

## Primary endpoint — Change from baseline

```
chg_from_baseline = baseline_score - week12_score
```

Set to missing if `week12_score` is missing (patient discontinued
before the Week 12 visit).

## Secondary endpoint — Responder

```
responder = 1 if chg_from_baseline >= 10.0 else 0
responder = missing if chg_from_baseline is missing
```

The 10.0-point threshold is a pre-specified minimal clinically
important difference (MCID) for this simulated efficacy scale.

## Safety endpoint — Serious adverse event

```
serious_ae = 1 if ae_grade >= 3 else 0
```

Grades follow the standard 0–4 CTCAE-style severity scale (0 = none,
4 = life-threatening). Grade >= 3 is the conventional "serious AE"
cutoff.

## Traceability

| Field | Source | Derivation function |
|---|---|---|
| `chg_from_baseline` | `baseline_score`, `week12_score` | `derive_primary_endpoint` |
| `responder` | `chg_from_baseline` | `derive_secondary_endpoint` |
| `serious_ae` | `ae_grade` | `derive_safety_endpoint` |

Each function is implemented once in `src/endpoint_derivation.py` and
independently re-implemented in `src/validation.py` for cross-checking.
