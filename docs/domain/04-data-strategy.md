# Data Strategy — Why History Matters

> **The single most time-critical decision in this project: start storing daily
> price snapshots as early as possible. Historical data cannot be scraped
> retroactively.**

---

## 1. Two different kinds of "history"

These are constantly confused. They have different uses and different risks.

| | **Cross-sectional history** | **Longitudinal history** |
|---|---|---|
| What | Old listings used as comparables | The **life story of each individual listing** |
| Example | "A flat sold in March for 190k" | "This listing: 265k → 245k → 210k → 199k" |
| Vulnerable to market drift? | ✅ Yes — must be time-corrected | ❌ No |
| Importance | Low | **Very high** |

The common objection — *"old prices mislead because the market moves"* — applies
only to the left column, and is handled by the corrections in
`02-price-factors.md` §7.

**The value is almost entirely in the right column**, which is immune to drift
because it tracks the *same property* over time rather than comparing different
properties across time.

Note the self-referential elegance: you can only know the market has moved by
having history. History is what lets you measure and correct the very drift that
makes history risky.

---

## 2. What longitudinal history gives you

### a) Ground truth labels — the decisive reason

This is a predictive model. **Without knowing what happened, you can never learn
whether it works.**

- Listing disappears after 12 days → it was underpriced
- Listing still up after 8 months → it was overpriced

**The market labels the data for you, for free.** No manual annotation.

After ~6 months you can ask measurable questions:

- *"Of listings I scored 8+, what fraction sold within 30 days?"*
- *"What is the neighbourhood base rate?"*
- *"If I raise the terrace coefficient to 1.10, does that metric improve?"*

Without this, the agent is **frozen at v1 quality forever** — there is no signal
telling you which direction to correct in.

> This is also the shortcut around the developer's lack of appraisal expertise.
> You do not need to know what a terrace is worth. You need to measure which
> coefficient best predicts fast sales.

### b) Price drops — arguably the strongest single signal

Three listings, all 80 m², all asking 199,000 € today. A snapshot cannot tell them
apart. History can:

| | History | Reading |
|---|---|---|
| **X** | Listed 12 days ago at 199k, no changes | Initial price. If cheap, it is genuinely cheap — and it will be gone in two weeks |
| **Y** | 14 months: 265k → 245k → 225k → 210k → 199k | Seller has conceded 25% and still has not sold. Either desperate, or there is a defect buyers see |
| **Z** | Listed 12 days ago at 199k, but was listed 8 months ago at 189k | Seller **raised** the price. Not an opportunity |

None of this is derivable from today's snapshot, and none of it is affected by
market drift.

For **Y**, be honest about the interpretation: history gives you the right
*question*, not the answer. But moving from "I know nothing" to "I know what to
ask" is exactly what a screener is for.

### c) Time on market as a reality check

If the model says a flat is 20% underpriced but it has sat unsold for 200 days,
**the market disagrees with the model**. Every day it does not sell is evidence
against the estimate. Free validation.

### d) Neighbourhood liquidity and price index

Aggregating time-on-market per neighbourhood gives both a risk measure (how hard
is it to resell here?) and the local price index used to time-correct comparables.

---

## 3. Which data serves which question

Separate the uses and the drift objection dissolves.

| Question | Data used |
|---|---|
| **What is it worth today?** (level) | **Currently active listings**, plus those that disappeared < 6-9 months ago, recency-weighted |
| **Is the market rising or falling?** (trend) | Full neighbourhood history |
| **Is this seller motivated?** | History of **that specific listing** |
| **Does my model work?** | Full history with time-on-market |

> **Price level comes from the present. Dynamics and validation come from the
> past.** Different questions, different sources — they never conflict.

---

## 4. Storage design

```
property           (id, url, attributes..., operation_type, first_seen_at)
price_observation  (property_id, price, seen_at, is_active)
```

Rules:

1. **Never overwrite a price.** Always insert a new `price_observation`.
2. **Never hard-delete a disappeared listing.** Mark `is_active = false` and keep
   the row — a disappearance is a label, and deleting it destroys the signal.
3. Record `first_seen_at` and derive time-on-market from observations.
4. Store the **raw listing text** — red-flag detection and future re-parsing both
   depend on prose you did not know you needed.
5. Store sale and rental listings in the same schema, separated by
   `operation_type`. The cross-market yield calculation needs both.

**Cost:** ~3,000 listings with daily observations for a year is a few MB in
SQLite. There is no storage argument against this.

**Asymmetry:** storing and never using it wastes 4 MB. Not storing and later
needing it loses information that **cannot be recovered by any means**.

---

## 5. Calibration loop

```
collect → predict → observe outcome → adjust coefficients → repeat
```

1. **Phase 4** — collect ≥1,000 listings, some already disappeared
2. **Phase 5** — Tier 0 model with expert priors, benchmarked against `NaiveEvaluator`
3. **Phase 6** — shadow mode: review the top 10 daily, record *why each is not a
   bargain*. Each entry becomes a coefficient correction or a new red flag
4. Record every change in `05-calibration-log.md` with the evidence

The metric to optimise is **ranking quality**, not price accuracy: of the listings
scored highest, what fraction sold quickly compared to the base rate?

---

## 6. External data sources (free)

Anchor the coefficients in verifiable data rather than estimates.

| Source | Provides | Notes |
|---|---|---|
| **Sede Electrónica del Catastro** (public API) | Real surface, year built, use | **Ground truth** against listing claims. Fixes the built-vs-usable error — likely the cheapest accuracy win available |
| **Ministerio de Vivienda** — quarterly price series | Real price level by municipality | Appraised values |
| **INE** — Housing Price Index | Temporal trend | For time-correcting comparables |
| **Idealista / Fotocasa neighbourhood reports** | €/m² sale **and rent** by neighbourhood, monthly | Directly comparable to our own aggregates |
| **Colegio de Registradores** | **Closed transaction** prices | Closer to true value than asking prices |
