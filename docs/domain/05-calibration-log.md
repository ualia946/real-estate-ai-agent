# Calibration Log

Append-only record of changes to the valuation model and the evidence behind them.

**Why this file exists:** in six months nobody will remember why a coefficient has
the value it has, and without that context nobody will dare change it. This is the
file that keeps the model editable.

## How to write an entry

One entry per change. Never edit or delete past entries — supersede them.

```
## YYYY-MM-DD — <what changed>

**Change:** <parameter>: <old> → <new>
**Evidence:** <what data or observation motivated this; sample size>
**Confidence:** low | medium | high
**Source:** expert_prior | market_data | external | backtested
**Effect:** <what happened to ranking quality, if measured>
```

Also log:

- Red flags discovered during shadow mode (and added to `03-red-flags.md`)
- Coefficients **removed** for being noise — deleting a factor is a real result
- Model tier changes (Tier 0 → 1 → 2) and the sample size that justified it
- Scoring or threshold changes

---

## 2026-09-09 — Initial coefficient set

**Change:** Established the baseline model in `02-price-factors.md`.
**Evidence:** None. Every value is an informed estimate.
**Confidence:** low across the board.
**Source:** `expert_prior` for all multiplicative and additive factors;
`external` only for purchase costs, taxes and market drift.
**Effect:** Not measurable — no data collected yet.

Open questions to resolve once data exists:

- Is the `needs renovation` index really 0.82? Highest-magnitude and
  worst-documented factor; expect it to dominate model error.
- Is orientation signal or noise? Flagged **very low** confidence. If data does
  not support it, **delete the factor** rather than tune it.
- Is the sale size elasticity α = 0.82 right for the target city?
- Do the additive values for parking and storage hold locally?

---

<!-- New entries below, newest last -->
