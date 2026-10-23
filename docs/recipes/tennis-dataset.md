# Export winner/loser rows to JSON, CSV and SQLite

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py tennis-dataset --dry-run
python run.py tennis-dataset
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/tennis-dataset/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [tennis-match-dataset](https://apify.com/crawlplant/tennis-match-dataset)

```json
{
  "maxItems": 200,
  "years": [],
  "dateFrom": "${DATE_FROM}",
  "dateTo": "${DATE_TO}",
  "tours": [
    "atp",
    "wta"
  ]
}
```

