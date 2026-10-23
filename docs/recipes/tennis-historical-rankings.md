# Retrieve a dated ranking list

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py tennis-historical-rankings --dry-run
python run.py tennis-historical-rankings
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/tennis-historical-rankings/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [flashscore-tennis](https://apify.com/crawlplant/flashscore-tennis)

```json
{
  "maxItems": 20,
  "mode": "rankings",
  "rankingLists": [
    "atp"
  ],
  "rankingDate": "2024-07-15"
}
```

