# Collect a technology video ranking snapshot

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py bilibili-tech-ranking --dry-run
python run.py bilibili-tech-ranking
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/bilibili-tech-ranking/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [bilibili-trending-history](https://apify.com/crawlplant/bilibili-trending-history)

```json
{
  "maxItems": 10,
  "mode": "ranking",
  "rankingCategories": [
    "tech"
  ],
  "trackHistory": false
}
```

