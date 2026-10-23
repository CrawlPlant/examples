# Resolve advertisers for a domain

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py ads-advertisers --dry-run
python run.py ads-advertisers
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/ads-advertisers/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [google-ads-transparency](https://apify.com/crawlplant/google-ads-transparency)

```json
{
  "maxItems": 20,
  "mode": "advertisers",
  "targets": [
    "${ADVERTISER}"
  ],
  "maxScanPages": 2
}
```

