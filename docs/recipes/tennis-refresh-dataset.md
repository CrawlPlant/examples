# Keep a results dataset up to date without duplicates

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py tennis-refresh-dataset --dry-run
python run.py tennis-refresh-dataset
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/tennis-refresh-dataset/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Interpretation

Run again with an overlapping date window. merged.json is updated atomically; new records replace matching IDs.

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

