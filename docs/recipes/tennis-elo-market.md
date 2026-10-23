# Compute Elo-versus-market probability differences

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py tennis-elo-market --dry-run
python run.py tennis-elo-market
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/tennis-elo-market/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Interpretation

Retrieved odds are not an archived pre-match betting signal. No profit or predictive advantage is claimed.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [flashscore-tennis](https://apify.com/crawlplant/flashscore-tennis)

```json
{
  "maxItems": 20,
  "mode": "matches",
  "dateFrom": "${DATE_FROM}",
  "dateTo": "${DATE_TO}",
  "includeOdds": true,
  "tours": [
    "atp",
    "wta"
  ]
}
```

