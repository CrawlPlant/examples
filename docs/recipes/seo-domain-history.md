# Export domain metrics across releases

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py seo-domain-history --dry-run
python run.py seo-domain-history
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/seo-domain-history/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [commoncrawl-domain-metrics](https://apify.com/crawlplant/commoncrawl-domain-metrics)

```json
{
  "maxItems": 20,
  "mode": "history",
  "domains": [
    "${DOMAIN}"
  ],
  "historyReleases": 3
}
```

