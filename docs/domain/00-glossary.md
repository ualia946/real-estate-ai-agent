# Glossary — Spanish Real Estate Terms

Spanish terms are kept **verbatim** because the scraper matches them literally in
listing text and the LLM judge must recognise them. This file is the bridge
between the Spanish market, the English codebase, and the LLM prompts.

🚩 = red flag. See `03-red-flags.md`.

---

## Surface and measurement

| Term | Meaning | Impact |
|---|---|---|
| **Superficie construida** | Built area, includes interior walls | The number portals usually show |
| **Superficie útil** | Usable floor area | Typically **15-20% smaller** than construida |
| **Superficie construida con elementos comunes** | Built area + share of common areas | Largest of the three. Inflates listings |
| **Superficie computable** | Legally computable area used in official appraisal | Terraces often count at 50% |

⚠️ Mixing these across comparables silently corrupts every €/m² calculation.
Model as `surface_type` on `PhysicalDimensions`.

## Floor and position

| Term | Meaning |
|---|---|
| **Bajo** | Ground floor. Discount: less light, security, street noise |
| **Entresuelo** | Mezzanine, between ground and first |
| **Principal** | Traditional "main" floor, above entresuelo |
| **Ático** | Top floor, usually with terrace. Premium |
| **Sobreático** | Above the ático, set back further |
| **Exterior** | Windows face the street |
| **Interior** | Windows face an interior courtyard (*patio de luces*). Discount ~10% |

## Condition

| Term | Meaning | Approx. effect |
|---|---|---|
| **A reformar** | Needs renovation. Range is huge: paint vs. gut job | −18% |
| **Para entrar a vivir** | Move-in ready | Baseline |
| **Reformado** | Recently renovated | +15% |
| **Reforma integral** | Full gut renovation | 600-900 €/m² |
| **Obra nueva** | New build | Different market segment |
| **Sobre plano** 🚩 | Off-plan, not yet built | Not comparable to existing stock |

## Ownership and legal status — mostly red flags

| Term | Meaning | Why it matters |
|---|---|---|
| **Nuda propiedad** 🚩 | Bare ownership; a *usufructuario* lives there for life | Price is 30-60% below market **for a reason**. Not a bargain |
| **Usufructo** | Life interest held by another person | You cannot occupy or rent the property |
| **Proindiviso** 🚩 | Undivided co-ownership share | You buy a % of the property, not the property |
| **Okupas / ocupada** 🚩 | Squatters in occupation | Eviction takes years. Price reflects this |
| **Alquilada / renta antigua** 🚩 | Tenanted, possibly under an old rent-controlled lease | You inherit the tenant and their rent |
| **Subasta** 🚩 | Auction / bank repossession | Special process, possible hidden charges |
| **Multipropiedad** 🚩 | Timeshare | Not a dwelling purchase at all |
| **VPO / VPP** 🚩 | Subsidised housing | Legal caps on resale price and buyer eligibility |
| **Tanteo y retracto** | Public administration's right of first refusal | Can block the sale |
| **Cargas** | Encumbrances, mortgages, liens on the property | Must be checked in the Registro |
| **Arras** | Deposit contract preceding the deed | Standard, not a flag |

## Building and community

| Term | Meaning |
|---|---|
| **Comunidad de propietarios** | Homeowners' association |
| **Gastos de comunidad** | Monthly HOA fees. 50-150 €/month typical |
| **Derrama** 🚩 | Special assessment levy for major works. Can be 10-30k € and is rarely disclosed in listings |
| **ITE / IEE** | Mandatory periodic building inspection. An unfavourable one implies future *derramas* |
| **Aluminosis** 🚩 | Structural concrete degradation (1950s-70s buildings). Can be catastrophic |
| **Cédula de habitabilidad** | Occupancy certificate. Required to rent or sell |
| **Certificado energético** | Energy rating A-G. Increasing price impact |
| **Finca** | The building / estate as a whole |

## Extras

| Term | Meaning | Valuation treatment |
|---|---|---|
| **Plaza de garaje** | Parking space | **Additive**: 15-30k € (sale), 60-100 €/mo (rent) |
| **Trastero** | Storage room | **Additive**: 5-12k € |
| **Terraza** | Terrace | Multiplicative: ~+6% |
| **Balcón** | Balcony (smaller than a terrace) | ~+2% |
| **Amueblado** | Furnished | +3% sale, +8% rent |

## Rental market

| Term | Meaning |
|---|---|
| **Zona tensionada** 🚩 | Officially designated stressed rental area with legal rent caps. Limits future yield |
| **Índice de precios de alquiler** | Government reference rent index used to enforce caps |
| **Alquiler con opción a compra** 🚩 | Rent-to-own. Different asset, not comparable |
| **Alquiler por habitaciones** | Room-by-room letting. Higher yield, different (sometimes restricted) business |
| **Fianza** | Legal deposit (1 month for residential) |
| **Vacancy / desocupación** | Months empty between tenants. 4-8% of annual rent |

## Taxes and purchase costs

| Term | Meaning | Amount |
|---|---|---|
| **ITP** | Transfer tax on resale property | 6-10%, varies by autonomous community |
| **IVA + AJD** | VAT + stamp duty, on new builds only | 10% + 0.5-1.5% |
| **IBI** | Annual property tax | 300-600 €/yr typical flat |
| **Notaría, registro, gestoría** | Deed, land registry, admin | ~1-1.5% |
| **Total purchase costs** | | **~8-12% on top of the price** |

## Market slang

| Term | Meaning |
|---|---|
| **Chollo** | Bargain. What this project hunts |
| **Oportunidad** | Used by agents on *anything*, including overpriced stock. Not a signal |
| **Precio a consultar** 🚩 | Price on request. Unusable, exclude from comparables |
| **Se vende por traslado / herencia** | Motivated seller. Weak but real positive signal |
