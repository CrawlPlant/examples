# Find referring domains shared by competitors

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py seo-link-gap --dry-run
python run.py seo-link-gap
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/seo-link-gap/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [link-gap-finder](https://apify.com/crawlplant/link-gap-finder)

```json
{
  "maxItems": 20,
  "yourDomain": "${YOUR_DOMAIN}",
  "domains": [
    "${DOMAIN}",
    "${COMPETITOR}"
  ],
  "maxReferrersPerDomain": 30
}
```

