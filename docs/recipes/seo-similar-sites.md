# Discover sites with related linking patterns

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py seo-similar-sites --dry-run
python run.py seo-similar-sites
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/seo-similar-sites/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [similar-sites-finder](https://apify.com/crawlplant/similar-sites-finder)

```json
{
  "maxItems": 20,
  "domains": [
    "${DOMAIN}"
  ],
  "maxReferrersPerDomain": 20
}
```

