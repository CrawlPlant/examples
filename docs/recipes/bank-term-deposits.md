# Export 12-month term-deposit rate records

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py bank-term-deposits --dry-run
python run.py bank-term-deposits
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/bank-term-deposits/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Interpretation

Source rates and conditions, not personal financial advice; inspect eligibility and dates.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [au-bank-rates](https://apify.com/crawlplant/au-bank-rates)

```json
{
  "maxItems": 10,
  "mode": "best",
  "categories": [
    "TERM_DEPOSITS"
  ],
  "termMonths": [
    12
  ],
  "amount": 10000
}
```

