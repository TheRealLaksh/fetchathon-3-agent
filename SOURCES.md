# Assumptions and sources (Mandi Net-Price Desk)

Prices and distances are live data. The three numbers below are assumptions, set from public sources on
24 Oct 2026. Each is shown in every answer and can be overridden in chat (for example "my truck costs
Rs 4 per tonne-km" or "my agent charges 6% commission").

| Assumption | Default | Source and how it was derived | Confidence |
|---|---|---|---|
| Freight | Rs 3.0 per tonne-km | Business Standard, using CMIE data (Apr 2024): Delhi-Kolkata Rs 42.9 per km and Delhi-Bengaluru Rs 42.3 per km for a 15 t truck, about Rs 2.8 per tonne-km. FR8 route quotes (15 t, 32 ft): Delhi-Bangalore Rs 103,900 for 2,189 km (about Rs 3.2) and Delhi-Kolkata Rs 84,500 for 1,524 km (about Rs 3.7). Median of these four is about Rs 3.0. | Medium for long hauls. Short hauls (under 300 km, our use case) usually cost more per tonne-km, so this may flatter far mandis. |
| Market fee | 2% | Tribune, Gurugram, 10 Feb 2024: Haryana collects 1% market fee plus 1% Rural Development Fund on fruits and vegetables, paid by commission agents. Other Tribune reports conflict (some say the fee was raised to 2% or 4%). | Medium. Check the current HSAMB notification. |
| Agent (arhtiya) commission | 0% (not included) | No reliable single rate found. A national feature gives 6 to 10% depending on place and product, and it is unclear who pays. Left out on purpose and shown as "not included"; the user can state their own. | Low, hence excluded by default. |
| Transit loss | 0.25% (tomato), 0.15% (onion), 0.2% (other) of value per drive hour | A Lok Sabha answer citing the NABCONS 2022 study gives vegetable transport losses of roughly 0.1 to 1.6% per trip, about 0.2% per hour over a 5 hour trip. Tomato and onion are scaled by their market-stage losses in NABCONS 2022 (3.25% and 1.96%, as reported by Global Agriculture). Potato has no crop figure, so it uses the default. | Low to medium. The per-hour scaling is our own derivation. |

## Sensitivity (tomato from Gurugram, 24 Oct 2026, real data)

The top-4 order (Sohna, Gohana, Narnaul, Patiala) did not change when freight went to Rs 3.7 or Rs 5.0, when
transit loss went to 0.5% per hour, or when fees plus commission went to 8%. Fees move every net figure down by a
similar share but do not reorder the mandis. Freight and transit loss only matter at long distances.

## Links

- Business Standard, truck freight rates (CMIE): https://www.business-standard.com/industry/news/truck-freight-rates-dip-for-smaller-cities-remain-flat-for-bigger-ones-124050500187_1.html
- FR8 truck rates: https://www.fr8.in/truck-rates
- Tribune, Gurugram market fee and RDF: https://www.tribuneindia.com/news/haryana/arhtiyas-in-gurugram-fruit-and-vegetable-market-on-strike-589500
- NABCONS 2022 tomato and onion losses (as reported): https://www.global-agriculture.com/india-region/indias-highest-post-harvest-losses-guava-and-tomato-among-the-worst-hit/
- Lok Sabha answers citing the loss studies: https://eparlib.sansad.in/bitstream/123456789/2984698/1/AU1773_tyKJYF.pdf and https://eparlib.sansad.in/bitstream/123456789/3017416/1/AU1976_37fxUw.pdf

Not yet verified at the primary source: the exact NABCONS 2022 crop-by-stage tables, and the current Haryana
commission schedule. Treat the transit-loss and fee figures as estimates until checked.
