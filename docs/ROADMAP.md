# Project Roadmap & Current State

> **READ THIS FIRST.** This file is the entry point for any human or AI agent
> joining this project. It answers: what are we building, where are we now,
> and what is the next thing to do.
>
> **Last updated:** 2026-09-09

---

## 1. What this project is

An autonomous agent that scrapes Spanish real estate portals, estimates whether
a listing is priced below its market value, and alerts the user about the ones
worth a phone call.

**Realistic goal — read carefully, this shapes every design decision:**

This is a **screener**, not an oracle. Best-in-class commercial AVMs achieve
5-10% median error using *closed transaction* data. We only have *asking prices*,
a noisier signal, so 10-15% error is the realistic ceiling.

- ❌ Not achievable: "this flat is worth exactly 187,700 EUR"
- ✅ Achievable and valuable: "of these 500 listings, these 10 deserve a call"

Consequence: discounts below ~15% are indistinguishable from model noise. Do not
design for precision we cannot have. Design for **ranking quality**.

---

## 2. Current state (2026-09-09)

| Layer | Status | Notes |
|---|---|---|
| Domain (entity + value objects) | ✅ Done | 7 files, solid. Missing some fields — see Phase 0 |
| Ports (interfaces) | 🟡 Signatures only | 5 ports defined, no bodies |
| Use cases | ❌ Empty | `src/core/use_cases/` has no files |
| Adapters | ❌ Empty | `src/adapters/` has no files |
| Entrypoint | ❌ Empty | `src/main.py` is 0 bytes |
| Tests | ❌ None | `src/tests/` empty. Note: `pyproject.toml` points pytest at `tests/`, path mismatch |

**Nothing executes yet.** Running `python src/main.py` does nothing.

The vocabulary (what things are) and the contracts (what each piece promises)
exist. No piece performs real work.

### Current phase: **Phase 0**

---

## 3. The next action

**Phase 0 — add the missing domain fields.** ~2-3 hours. Nothing else.

Do not think about valuation algorithms, hedonic coefficients, or LLM prompts
while doing this. See §4.

---

## 4. Phases

Each phase has an **exit criterion**. Do not move on until it is met.
Do not start a later phase early — the ordering is deliberate (see §5).

### Phase 0 — Close the domain model · ~2-3 h · **CURRENT**

Add what is missing so listings can be stored faithfully.

| Where | Add |
|---|---|
| `Property` | `operation_type` (SALE/RENT), `description: str`, `first_seen_at: datetime` |
| `PhysicalDimensions` | `surface_type` (BUILT/USABLE/UNKNOWN); fix `square_meters <= 0` (currently allows 0 → `ZeroDivisionError` in `price_per_m2`) |
| `BuildingDetails` | `condition` (NEEDS_RENOVATION/GOOD/RENOVATED/UNKNOWN), `year_built: int \| None` |
| `Amenities` | `has_storage_room` |

`operation_type` is the most important: without it, sale and rental listings mix
in the same comparable pool and every downstream number becomes meaningless.

`surface_type` matters because Spanish portals mix *superficie construida* and
*superficie útil*, a 15-20% difference. See `domain/03-red-flags.md`.

**Exit criterion:** mypy passes; you can hand-construct a `Property` that
faithfully represents a real listing from a portal.

---

### Phase 1 — Persistence with price history · ~1 day · ⏰ TIME-CRITICAL

SQLite adapter for `IPropertyRepositoryPort`. Two tables:

```
property           (id, url, attributes..., first_seen_at)
price_observation  (property_id, price, seen_at, is_active)   -- one row per day
```

**Never overwrite a price. Always insert a new observation.**

Why this is time-critical: historical data cannot be scraped retroactively. Every
week without collection is a week of data permanently lost. See
`domain/04-data-strategy.md` for the full rationale.

**Exit criterion:** save a `Property`, read it back, objects are equal.

---

### Phase 2 — Scraper adapter · ~2-4 days

Implement `IScraperPort` for one portal, one city, one search. The most tedious
phase (blocks, captchas, DOM changes). Do not generalize prematurely.

**Exit criterion:** a command downloads 50 real listings and stores them.

---

### Phase 3 — End-to-end pipeline with a *deliberately naive* evaluator · ~1 day

Wire the use case: search → extract → store → evaluate → print top 10.
No Telegram yet; print to console.

**The evaluator in this phase is intentionally stupid:**

```python
# Deliberately naive. Placeholder until real data exists.
median_ppm2 = median(c.price_per_m2 for c in market_comparables)
discount = 1 - (target.price_per_m2 / median_ppm2)
score = max(0.0, min(10.0, discount * 40))
```

This is wrong in every way described in `domain/01-valuation-method.md`. That is
fine. Its job is not to be accurate — its job is to **close the circuit so data
collection can start**.

Keep it permanently as `NaiveEvaluator`: it is the **baseline**. If the real
hedonic model in Phase 5 cannot beat three lines of code, something is broken.

**Exit criterion:** `python src/main.py` does something useful end to end.

> 🎉 At this point you have a live product. Bad, but alive — and the data clock
> is running.

---

### Phase 4 — Collect and document · ~3-4 weeks · **no new code**

Run a daily cron. While it collects, write the domain docs with real listings in
front of you:

- `domain/00-glossary.md` — terms you actually see in listings
- `domain/03-red-flags.md` — every anomaly you encounter
- `domain/02-price-factors.md` — refine coefficients, record sources

**Exit criterion:** >1,000 listings stored, some already disappeared (= sold).

---

### Phase 5 — The real evaluator · ~2-3 days

`HedonicValuator` as a pure domain service: homogenisation of comparables,
size elasticity, robust median (MAD), confidence score.
See `domain/01-valuation-method.md` for the method and
`domain/02-price-factors.md` for the coefficients.

**Exit criterion:** on real collected data, the hedonic model ranks better than
`NaiveEvaluator`, measured against which listings sold fastest.

---

### Phase 6 — Shadow mode · ~3-4 weeks

Still no notifications. Every morning, spend 15 minutes reviewing the top 10
scored listings and write down **why each one is NOT a bargain**.

That third column is the fastest path to domain expertise, and each entry becomes
either a new coefficient or a new red flag.

**Exit criterion:** at least 3 of every 10 alerts look worth a phone call.

---

### Phase 7 — LLM judge · ~2-3 days

Narrow port (`ILlmJudgePort`), not a full evaluator. Its only jobs:
detect red flags from listing prose, apply a **bounded** qualitative adjustment
(±1.5 points), and write the alert text. It must never compute the score.

**Exit criterion:** it filters out the false positives you were catching by hand
in Phase 6.

---

### Phase 8 — Telegram notifier · ~0.5 day

Last. Bad alerts are worse than no alerts — three useless pings and the user
stops looking at their phone.

---

## 5. Decisions already made (do not re-litigate)

| Decision | Rationale |
|---|---|
| **Valuation logic lives in the domain, not in an adapter** | It is pure, deterministic business knowledge with no I/O. Putting it in `adapters/` would make business rules untestable without mocking a paid API |
| **The LLM does not compute the score** | Non-reproducible, poor at arithmetic over many rows, expensive. It judges prose and vetoes; the maths is deterministic |
| **`IEvaluatorPort` should be narrowed or replaced** | The only real boundary crossing is the LLM call. Prefer a narrow `ILlmJudgePort` and a plain domain service for the maths. `EvaluationResult` mixing `score` (formula) and `reasoning` (LLM prose) is the smell that revealed this |
| **Value objects carry behaviour** | Entity vs VO is decided by *identity*, not by presence of logic. `Property` is an Entity (persists through price changes); `Money`, `Appraisal`, `HedonicCoefficients` are VOs |
| **Track both SALE and RENT markets** | They are independent markets and give two independent valuations. Their divergence is itself signal. See `domain/01-valuation-method.md` §4 |
| **Naive evaluator first, real one later** | The real model cannot be calibrated without data, and data cannot be collected without a working pipeline |
| **Store daily price snapshots, never overwrite** | Price drops and time-on-market are the strongest opportunity signals and the only source of training labels. Unrecoverable if not collected |

## 6. Explicitly deferred — do NOT build these yet

These were considered and consciously postponed. They are not oversights.

- **Ridge regression / learned coefficients (Tier 2).** Needs >50 comparables per
  neighbourhood. Expert priors beat any regression on small samples.
- **Geographic expansion beyond one city.** Scraper fragility first.
- **Catastro API integration** for surface verification. High value (fixes the
  built-vs-usable error) but not on the critical path yet.
- **Multiple portals.** One working scraper before two broken ones.
- **The abstraction to non-real-estate markets** mentioned in the README.

---

## 7. Where the knowledge lives

| File | Contains |
|---|---|
| `docs/domain/00-glossary.md` | Spanish market terms → domain concepts. Also feeds LLM prompts |
| `docs/domain/01-valuation-method.md` | How appraisal actually works: the three methods, homogenisation, rental yield |
| `docs/domain/02-price-factors.md` | The coefficient tables, each with source and confidence |
| `docs/domain/03-red-flags.md` | What makes a discount fake. Source material for the LLM system prompt |
| `docs/domain/04-data-strategy.md` | Why price history matters and how it calibrates the model |
| `docs/domain/05-calibration-log.md` | Append-only log of coefficient changes and why |

---

## 8. Maintaining this file

- Update §2 (current state) and §3 (next action) **whenever a phase completes**.
  A roadmap claiming Phase 2 while the code is at Phase 5 is worse than no roadmap.
- Add to §5 when a non-obvious decision is made, **with its rationale**.
- Add to §6 when something is deliberately postponed, so nobody thinks it was forgotten.
- Keep the "Last updated" date honest.

### Rule for getting unstuck

> **Ask: does this decision require data I do not have yet?**
>
> - **Yes** → wrong time. Put a placeholder in and move on.
> - **No** → decide in 10 minutes and move on.

Most valuation-design questions fall in the first group until Phase 4 completes.
