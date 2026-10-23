# Download game-format point data

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py tennis-point-games --dry-run
python run.py tennis-point-games
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/tennis-point-games/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [tennis-point-by-point](https://apify.com/crawlplant/tennis-point-by-point)

```json
{
  "maxItems": 2,
  "mode": "matchIds",
  "matchIds": [
    "${MATCH_ID}"
  ],
  "pointByPointFormat": "games"
}
```

