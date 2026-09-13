# Red Flags — Why a Discount Is Usually Fake

> **Core principle: an unexplained discount is an alarm, not an opportunity.**
>
> The deeper the discount, the more likely it has a reason. Extreme residuals are
> almost never bargains — they are legal encumbrances, data errors, or a different
> asset entirely.

This file is the **source material for the LLM judge's system prompt** (Phase 7).
The deterministic model cannot read prose; this is the only thing the LLM is
uniquely good at. Keep this file and the prompt in sync.

Add a new entry every time shadow mode (Phase 6) surfaces one.

---

## A. Hard vetoes — different asset, not a discount

If any of these appear, `is_opportunity = false` regardless of score.

| Flag | Spanish keywords | Why |
|---|---|---|
| **Bare ownership** | `nuda propiedad`, `usufructo`, `usufructuario` | 30-60% below market by definition. You cannot occupy it, possibly for decades |
| **Undivided share** | `proindiviso`, `50% de la vivienda`, `participación` | You buy a fraction, not the property |
| **Occupied** | `okupas`, `ocupada`, `ocupada ilegalmente`, `sin posesión` | Eviction takes years and costs money |
| **Tenanted** | `alquilada`, `inquilino`, `renta antigua`, `con inquilinos` | You inherit the tenant, sometimes at a frozen rent |
| **Auction / bank asset** | `subasta`, `procedimiento judicial`, `adjudicación` | Different process, possible hidden charges |
| **Timeshare** | `multipropiedad`, `aprovechamiento por turnos` | Not a dwelling purchase |
| **Subsidised housing** | `VPO`, `VPP`, `protección oficial`, `precio tasado` | Legal caps on resale price and on who may buy |
| **Off-plan** | `sobre plano`, `entrega en 2027`, `en construcción` | Not comparable to existing stock; delivery risk |
| **Rent-to-own** | `alquiler con opción a compra` | Different financial instrument |
| **Non-residential** | `local`, `nave`, `oficina`, `solar`, `terreno` | Wrong asset class; scraper filter failure |
| **Price on request** | `precio a consultar`, `consultar precio`, `0 €` | No usable price. Exclude from comparables too |

## B. Real costs hidden from the price

Not vetoes, but they explain the discount and must be subtracted before calling
anything cheap.

| Flag | Keywords | Typical cost |
|---|---|---|
| **Pending levy** | `derrama`, `derrama pendiente`, `obras aprobadas` | 10,000-30,000 € |
| **Unfavourable building inspection** | `ITE desfavorable`, `IEE pendiente` | Implies future derramas |
| **Structural degradation** | `aluminosis`, `patologías estructurales` | Potentially catastrophic |
| **No occupancy certificate** | `sin cédula de habitabilidad` | Cannot legally rent or sometimes sell |
| **Full renovation needed** | `reforma integral`, `para reformar entera`, `a reformar` | 500-900 €/m² |
| **No lift, high floor** | `sin ascensor` + `4º`, `5º` | Already in the coefficients, but verify |
| **Bad energy rating** | `certificado energético G` | Rising impact, renovation obligations coming |

## C. Data and scraping errors

Frequently the "best bargains" are simply bugs. Check these first.

| Error | How it shows | Detection |
|---|---|---|
| **Surface type mismatch** | Comparing *construida* against *útil* | 15-20% systematic bias. Verify against Catastro |
| **Order-of-magnitude price** | 18,000 € for an 80 m² flat in a city | Sanity bounds on €/m² |
| **Garage price on a flat listing** | Very low price, small surface | Cross-check surface and price jointly |
| **Plot vs. built area** | Huge surface, rural | Property type filter |
| **Rent listed as sale** | 1,100 € "price" | `operation_type` must be explicit, never inferred |
| **Duplicate listing** | Same flat via several agencies | Fuzzy hash on (coords, m², price) |
| **Building total price** | Whole block sold as one unit | Room/surface ratio implausible |

> Rule: **before believing an outlier, assume it is a bug.** In practice most
> extreme residuals in early phases are parsing errors, not opportunities.

## D. Timing signals

These come from **price history**, not from the listing itself. See
`04-data-strategy.md`.

| Signal | Reading |
|---|---|
| **Repeated price cuts** (e.g. 265k → 245k → 210k → 199k) | Either a motivated seller **or** a defect buyers can see and we cannot. Investigate — it is a question, not an answer |
| **Long time on market, no cuts** (8+ months, same price) | Overpriced, not a bargain. The market has already voted |
| **Relisted higher** | Withdrawn and re-published above the previous price. Seller testing the market |
| **Just listed, priced low** | The strongest positive signal. These sell in days — act fast |
| **Sold in under 2-3 weeks** | Retrospective evidence it was underpriced. Use as a training label |

## E. Location subtleties the model cannot see

| Issue | Why it matters |
|---|---|
| **"Neighbourhood" is too coarse** | Two streets 400 m apart can differ 30%. A railway line, a motorway or a park boundary splits a neighbourhood into distinct markets |
| **Noisy avenue vs. pedestrian street** | Significant discount, never in the structured fields |
| **Ground floor onto a busy street** | Compounded penalty beyond the standard *bajo* coefficient |
| **Views / blocked views** | Only in the prose and the photos |

Mitigation: prefer coordinate-radius comparables over administrative neighbourhood
boundaries once coordinates are reliably captured.

## F. Rental-specific

| Flag | Why |
|---|---|
| **Zona tensionada** | Legal rent caps limit future yield |
| **Room-by-room letting** | Not comparable to whole-unit rent; sometimes locally restricted |
| **Seasonal / temporada** | `alquiler de temporada`, `11 meses` — different market, higher headline rent |
| **Tourist licence** | Different regime entirely, do not mix into residential comparables |
| **Utilities included** | `gastos incluidos` inflates the headline rent by 80-150 €/month |

---

## Using this file for the LLM prompt

The judge should receive: the target's raw listing text, the computed numbers, the
iso-price cohort and the twin comparables — and return **only**:

```json
{"red_flags": ["..."], "qualitative_adjustment": -0.5,
 "confidence_in_data": "high", "reasoning": "..."}
```

Constraints to enforce in the prompt:

- The adjustment is bounded to **[−1.5, +1.5]**. The LLM never sets the score.
- Any **Section A** flag forces `is_opportunity = false`.
- It must not perform arithmetic on the comparables — the model already did.
- Absence of data is not a defect (unknown orientation is not a penalty).
- Reasoning in Spanish, for the Telegram alert; never invent a figure.
