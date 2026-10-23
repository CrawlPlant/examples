# Export ad creatives and their source records

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py ads-creatives --dry-run
python run.py ads-creatives
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/ads-creatives/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [google-ads-transparency](https://apify.com/crawlplant/google-ads-transparency)

```json
{
  "maxItems": 10,
  "mode": "ads",
  "targets": [
    "${ADVERTISER}"
  ],
  "includeAdContent": true,
  "maxScanPages": 2
}
```

