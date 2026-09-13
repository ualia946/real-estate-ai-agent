# How Property Valuation Actually Works

The domain knowledge behind the evaluator. Read before touching valuation code.

---

## 1. Value is not asking price

```
Asking price ──(negotiation, −5% to −10%)──> Closing price ≈ Market value
```

We scrape **asking prices**. Real value sits ~5-10% below. Therefore a listing
"6% below market" is not a bargain — it is a seller who already priced realistically.

Only large deviations are detectable above model noise. See ROADMAP §1.

## 2. The three classical methods

| Method | Question it answers | Used for |
|---|---|---|
| **Comparison** | What do similar properties sell for? | Housing. 95% of cases |
| **Cost** | What would it cost to rebuild? | New builds, unique buildings |
| **Income capitalisation** | How much money does it produce? | Investment property |

This project uses **comparison** (primary) and **income capitalisation**
(secondary, via the rental market). They are two independent opinions on the same
asset — when they agree, confidence is high; when they diverge, that divergence
is itself information.

---

## 3. The comparison method: homogenisation

The naive approach — "average similar listings" — always fails, because no two
properties are identical.

> **Homogenisation: take each comparable and ask "what would THIS property cost
> if it had exactly the target's characteristics?"**

Nothing is discarded. Every comparable is **transformed** until it is equivalent
to the target, then compared.

**This is also the answer to the asymmetric-opportunity blind spot.** If you
filter comparables to "only 3-bedroom flats", you never learn that the target
costs the same as a 2-bedroom nearby. Homogenisation never filters — it converts.

### Worked example

**Target:** 80 m², 3 bed, 3rd floor **with lift**, exterior, **terrace**,
**needs renovation**. Asking **180,000 €** → 2,250 €/m²

| # | m² | Floor | Condition | Ext. | Terrace | Price | €/m² |
|---|---|---|---|---|---|---|---|
| A | 75 | 2nd, lift | Renovated | Yes | No | 210,000 | 2,800 |
| B | 90 | 4th, lift | Good | Yes | No | 243,000 | 2,700 |
| C | 70 | 3rd, **no lift** | Needs reno. | Yes | No | 154,000 | 2,200 |
| D | 85 | 1st, lift | Good | **Interior** | No | 212,500 | 2,500 |
| E | 82 | 5th, lift | Renovated | Yes | **Yes** | 254,200 | 3,100 |

#### ⚠️ The trap

Median comparable = 2,700 €/m². Target = 2,250 €/m² → **"17% below market, bargain!"**

**False.** Watch.

#### Step 1 — quality index per property

Multiply the coefficients from `02-price-factors.md`:

**Target:** `0.82 (needs reno) × 1.00 (3rd+lift) × 1.00 (exterior) × 1.06 (terrace) = 0.869`

| # | Calculation | Index |
|---|---|---|
| A | 1.15 × 1.00 × 1.00 × 1.00 | 1.150 |
| B | 1.00 × 1.00 × 1.00 × 1.00 | 1.000 |
| C | 0.82 × **0.85** × 1.00 × 1.00 | 0.697 |
| D | 1.00 × 0.97 × **0.90** × 1.00 | 0.873 |
| E | 1.15 × 1.03 × 1.00 × **1.06** | 1.256 |

#### Step 2 — homogenise

```
homogenised €/m² = actual €/m² × (target_index / comparable_index)
```

| # | Actual | Factor | **Homogenised** |
|---|---|---|---|
| A | 2,800 | 0.756 | **2,116** |
| B | 2,700 | 0.869 | **2,346** |
| C | 2,200 | **1.247** | **2,743** |
| D | 2,500 | 0.995 | **2,488** |
| E | 3,100 | 0.692 | **2,145** |

Note comparable **C**: cheapest on paper (2,200 €/m²), but it is a 3rd floor
**without a lift**. Once mentally given a lift, it becomes the **most expensive**
of the set. That is homogenisation earning its keep.

#### Step 3 — the value

Median of homogenised values: `2,116 | 2,145 | **2,346** | 2,488 | 2,743`

```
Estimated value = 2,346 €/m² × 80 m² = 187,700 €
Asking price    = 180,000 €
Deviation       = −4%   →  fairly priced, NOT a bargain
```

Naive comparison said −17%. Homogenisation says −4%. The gap was the renovation
cost the buyer would pay themselves.

> **Lesson 1: raw €/m² manufactures fake bargains constantly.** The cheap flat is
> almost always cheap for a reason that is in the small print.

At 150,000 € the same flat would be −20% — a real anomaly worth a call.

### Step 4 — dispersion is confidence

Use **MAD (median absolute deviation), not standard deviation** — the market has
fat tails, and a single genuine bargain would inflate σ and hide the next ones.

```
σ = 1.4826 × MAD(residuals)
z = residual / σ
```

A −20% deviation on 8 comparables in a highly dispersed neighbourhood is noise.
The same deviation on 60 tight comparables is a signal. **Never emit an alert
without a confidence measure.**

---

## 4. The rental lens

Everything above answers *"what is it worth?"*. Rent answers *"what does it produce?"*

> **Sale and rental are two different markets with different buyers and different
> drivers.** Sales follow interest rates, expectations and credit. Rents follow
> the actual disposable income of people who live there. **They desynchronise —
> and that gap is where opportunity lives.**

### Gross yield

```
gross yield = (monthly rent × 12) / purchase price × 100
```

Example flat at 180,000 € renting for 1,100 €/mo → `13,200 / 180,000` = **7.33%**

### Net yield — the one that matters

Gross yield lies on both sides of the fraction.

**Numerator:** costs eat 30-35% of rent (IBI, comunidad, insurance, maintenance,
vacancy, management). Rule of thumb: `net income ≈ gross rent × 0.65-0.70`

**Denominator:** buying costs 8-12% more than the price (ITP, notary, registry),
plus renovation if needed.

```
Net income      = 13,200 × 0.68                    =   8,976 €
Total invested  = 180,000 × 1.10 + 40,000 reno     = 238,000 €
Net yield       = 8,976 / 238,000                  =    3.77%
```

**7.33% → 3.77%.** Roughly half. This is why forum gross-yield figures are noise.

### PER (years of rent to repay the property)

```
PER = price / annual rent = 180,000 / 13,200 = 13.6 years
```

Spanish average is ~20-25 years. Lower is better yield.

### Valuation by capitalisation

You can value the property purely from rent, ignoring sale comparables entirely:

```
value = net annual income / neighbourhood cap rate
```

At a 5% cap rate: `8,976 / 0.05` = **179,500 €**

| Method | Value |
|---|---|
| Comparison (sale market) | 187,700 € |
| Capitalisation (rental market) | 179,500 € |

Two independent estimates. Agreement → confidence. Divergence → signal.

### Two kinds of bargain — they are not the same

| | **Arbitrage bargain** | **Yield bargain** |
|---|---|---|
| Buyer | Flipper / reseller | Landlord |
| Definition | Price < comparison value | Yield > threshold (e.g. 6% net) |
| You earn | Once, on resale | Every month |
| Method | Comparison | Capitalisation |
| Found in | Expensive districts, inheritances, urgency | Working-class areas, mid-size cities |

**They rarely coincide.** A penthouse in a prime district at −15% is a huge
arbitrage bargain and a terrible 2.5% yield. A flat in a working-class area at
exactly market price can yield 8% net.

> **When both signals fire on the same property, that is a genuine anomaly** —
> usually a seller in a hurry or one who does not know what they have. That is the
> case worth waking someone up for.

### Consequence for data collection

Rent is **not in the sale listing**. Both markets must be scraped separately and
cross-referenced **by characteristics**, not by identity: "what does an 80 m²,
3-bed, renovated flat rent for in this neighbourhood?"

> **Key fact: rent does not scale with size the way price does.** Doubling the
> area nearly doubles sale price but not rent — tenants pay for *somewhere to
> live*, not for square metres. **Large flats therefore have systematically worse
> yield.** Studios and 1-2 bedroom units are where the yield is.

---

## 5. Size elasticity — why raw €/m² is biased

Price is **not linear** in surface. A 40 m² studio has a structurally higher €/m²
than a 120 m² flat on the same street (fixed cost of kitchen and bathroom, higher
liquidity of small units).

```
ln(P) = β₀ + α·ln(m²) + Σ βₖ·xₖ
```

with **α ≈ 0.82** for sale (α = 1 would mean constant €/m²) and **α ≈ 0.55-0.65**
for rent.

Using a flat neighbourhood median €/m² flags every large flat as a bargain and
every small flat as overpriced. Always apply the elasticity.

Note also that `rooms` and `square_meters` are strongly collinear. Conditional on
m², an extra bedroom adds only ~2-3%. Rooms are mostly a *proxy* for size — give
them a heavily shrunk coefficient.

---

## 6. Summary — valuation answers three questions

| | Question | Method | Output |
|---|---|---|---|
| 1 | What is it worth? | Homogenised comparison | Estimated value, % deviation |
| 2 | What does it yield? | Income capitalisation | Net yield, PER |
| 3 | Do I believe it? | Sample size and dispersion | Confidence score |

Three principles:

1. **Never compare raw prices. Homogenise first.**
2. **Sale and rent are independent markets.** Two opinions validate each other.
3. **An unexplained discount is an alarm, not an opportunity.** The agent's job is
   not only to find the discount but to find *why it exists*.
