# Collect current hot search terms

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py bilibili-hot-searches --dry-run
python run.py bilibili-hot-searches
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/bilibili-hot-searches/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [bilibili-trending-history](https://apify.com/crawlplant/bilibili-trending-history)

```json
{
  "maxItems": 20,
  "mode": "hotSearches",
  "trackHistory": false
}
```

