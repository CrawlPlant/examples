# Compare electricity estimates for an explicit usage scenario

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py energy-plan-estimates --dry-run
python run.py energy-plan-estimates
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/energy-plan-estimates/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Interpretation

4,000 kWh/year scenario; estimates depend on tariff assumptions and are not a bill guarantee.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [au-energy-plans](https://apify.com/crawlplant/au-energy-plans)

```json
{
  "maxItems": 10,
  "mode": "cheapest",
  "postcodes": [
    "${POSTCODE}"
  ],
  "fuelTypes": [
    "ELECTRICITY"
  ],
  "annualKwh": 4000
}
```

