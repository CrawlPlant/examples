# Join two Actors by match identity

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py tennis-join-dataset-points --dry-run
python run.py tennis-join-dataset-points
```

Starts up to **2 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/tennis-join-dataset-points/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

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

### [tennis-point-by-point](https://apify.com/crawlplant/tennis-point-by-point)

```json
{
  "maxItems": 200,
  "mode": "matches",
  "dateFrom": "${DATE_FROM}",
  "dateTo": "${DATE_TO}",
  "tours": [
    "atp",
    "wta"
  ],
  "pointByPointFormat": "sackmann"
}
```

