# Price Factors and Coefficients

The numbers used by the valuation model.

> ⚠️ **STATUS: almost everything here is `expert_prior` — informed estimates, not
> measured values. Treat every number as a HYPOTHESIS PENDING VALIDATION.**
>
> They are probably within ±40% of the correct value, which is good enough to
> start and not good enough to trust. Phase 4-5 replaces them with values measured
> from collected data. Record every change in `05-calibration-log.md`.

**Source values:** `expert_prior` (estimate) · `market_data` (measured from our
data) · `external` (public statistics) · `backtested` (validated against sales)

---

## 1. Three families of adjustment

Mixing them produces absurd results. A parking space is not worth "10%" — it is
worth ~18,000 € whether the flat costs 80,000 € or 800,000 €.

| Family | Applied how | Examples |
|---|---|---|
| **Size** | Power law `m²^α` | Surface |
| **Multiplicative** | Quality index, multiplies value | Condition, floor, orientation |
| **Additive** | Fixed € amount | Garage, storage, renovation cost |

Correct order: strip additive components from the observed price, homogenise the
remainder multiplicatively, then add them back.

```
P̂ = exp(β₀ + α·ln(m²) + Σ βₖ·xₖ) + Σ Vⱼ − renovation_cost
```

---

## 2. Size elasticity

| Market | α | Source | Confidence |
|---|---|---|---|
| Sale | 0.82 | expert_prior | medium |
| Rent | 0.60 | expert_prior | medium |

α = 1 would mean constant €/m². Rent's much lower α is why **large flats yield
worse than small ones** — the single most reliable structural fact in this file.

---

## 3. Sale — multiplicative index

Baseline = 1.00 means "average flat, good condition, 2nd-4th floor with lift,
exterior".

| Factor | Index | Source | Conf. |
|---|---|---|---|
| **Condition** — renovated | 1.15 | expert_prior | medium |
| **Condition** — good / move-in ready | 1.00 | — | high |
| **Condition** — needs renovation | 0.82 | expert_prior | low |
| **Floor** — 2nd-4th with lift | 1.00 | — | high |
| **Floor** — 1st with lift | 0.97 | expert_prior | medium |
| **Floor** — 5th+ with lift | 1.03 | expert_prior | low |
| **Floor** — ground floor (bajo) | 0.90 | expert_prior | medium |
| **No lift** | `1 − 0.05 × max(0, floor−1)`, floor ≥ 0, cap **0.72** | expert_prior | medium |
| **Interior** (patio) | 0.90 | expert_prior | medium |
| **Terrace** | 1.06 (1.10 if top floor) | expert_prior | low |
| **Balcony** | 1.02 | expert_prior | low |
| **2nd bathroom** | 1.06 | expert_prior | medium |
| **3rd+ bathroom** | 1.00 | expert_prior | low |
| **Air conditioning** | 1.02 | expert_prior | low |
| **Orientation** — south | 1.025 | expert_prior | **very low** |
| **Orientation** — north | 0.975 | expert_prior | **very low** |
| **Built before 1960, unrenovated** | 0.95 | expert_prior | low |

**Notes**

- *No lift* is deliberately **non-linear**: a ground or first floor is unaffected,
  a 5th floor is severely penalised. This is one of the few coefficients we are
  fairly confident about.
- *Condition* has the largest magnitude of any factor (±30% range) and is the
  **worst-documented field in listings**. "A reformar" can mean paint or a gut job.
  Expect this to be the largest single source of model error.
- **Orientation is near noise.** Do not let a model overfit on it. If data ever
  contradicts these values, delete the factor rather than tune it.

## 4. Sale — additive components (EUR)

| Component | Value | Source | Conf. |
|---|---|---|---|
| Parking space | 15,000-30,000 (city-dependent) | expert_prior | medium |
| Storage room (trastero) | 5,000-12,000 | expert_prior | medium |
| Renovation — cosmetic | −250 €/m² | expert_prior | low |
| Renovation — standard | −500 €/m² | expert_prior | low |
| Renovation — full (integral) | −800 €/m² | expert_prior | low |

---

## 5. Rental — multiplicative index

| Factor | Index | Source | Conf. |
|---|---|---|---|
| Furnished | 1.08 | expert_prior | medium |
| Renovated | 1.10 | expert_prior | low |
| Needs renovation | 0.88 | expert_prior | low |
| Air conditioning | 1.04 | expert_prior | low |
| Terrace | 1.05 | expert_prior | low |
| No lift (per floor above 1st) | −0.04, cap 0.80 | expert_prior | low |
| Interior | 0.93 | expert_prior | low |

Additive: parking **+60-100 €/month**.

Rental coefficients are generally **weaker** than sale coefficients — tenants are
less sensitive to quality than buyers, because they are not making a capital
commitment. Only condition and furnishing move the needle much.

---

## 6. Yield calculation constants

| Constant | Value | Source | Conf. |
|---|---|---|---|
| Gross-to-net income factor | 0.65-0.70 | expert_prior | medium |
| Purchase costs (resale) | +8-12% of price | external | **high** |
| ITP (transfer tax) | 6-10%, by autonomous community | external | **high** |
| Notary + registry + admin | ~1-1.5% | external | high |
| Vacancy allowance | 4-8% of annual rent | expert_prior | medium |
| Annual maintenance | ~1% of property value | expert_prior | medium |
| Typical neighbourhood cap rate | 4-7% | expert_prior | low |
| Spanish average PER | 20-25 years | external | medium |

Recurring costs to subtract from gross rent: IBI (300-600 €/yr), comunidad
(600-1,500 €/yr), insurance (200-400 €/yr), maintenance, vacancy, plus any
*derrama*.

---

## 7. Market drift (for time-adjusting old comparables)

| Constant | Value | Source | Conf. |
|---|---|---|---|
| Spanish price drift | ~5-8% / year (~0.5%/month) | external | medium |

| Comparable age | Accumulated drift | Usable? |
|---|---|---|
| 3 months | ~1.5% | Yes, uncorrected |
| 6 months | ~3% | Yes, below model noise |
| 12 months | ~6% | Correct it |
| 3 years | ~20% | **Unusable uncorrected** |

Two corrections:

```
recency weight   = 0.5 ^ (age_months / 12)
index correction = price × (index_today / index_then)
```

Once we have history, compute that index **from our own data per neighbourhood**
rather than from national statistics.

---

## 8. Model tiers by sample size

Never fit more parameters than the data supports.

| Tier | Comparables | Approach |
|---|---|---|
| **0** | < 15 | 100% expert priors. β₀ from robust neighbourhood median, α fixed at 0.82 |
| **1** | 15-49 | Estimate β₀ and α from the neighbourhood (2 params, stable). βₖ stay expert priors |
| **2** | ≥ 50 | Ridge regression on `ln(P)` shrinking **towards the expert priors**, not towards zero: `argmin Σ wᵢ(ln Pᵢ − Xᵢβ)² + λ‖β − β_prior‖²`, with λ decreasing as n grows |

**Start at Tier 0 (Phase 5). Do not build Tier 2 until data justifies it** —
on small samples, expert priors beat any regression.

---

## 9. Scoring

```
r     = ln(P_target_normalised) − ln(P̂)     # negative = cheap
σ     = 1.4826 × MAD(comparable residuals)   # robust, NOT std deviation
z     = r / σ
score = 10 / (1 + exp(1.5 × (z + 1.0)))
```

| z | score | Reading |
|---|---|---|
| 0 | 1.8 | At market |
| −1 | 5.0 | Cheap-ish |
| −2 | 8.2 | Strong candidate |
| −3 | 9.5 | Anomaly — usually a red flag, verify |

**Confidence:**

```
confidence = min(1, n/30) × dispersion_weight × (known_attributes / total_attributes)
```

**Decision:** `is_opportunity = score ≥ 7.5 AND confidence ≥ 0.6 AND no red flags`

All three conditions are required. A high score with low confidence is noise; a
high score with a red flag is a trap.
