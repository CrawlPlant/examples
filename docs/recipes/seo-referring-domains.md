# Inspect a sample of referring domains

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py seo-referring-domains --dry-run
python run.py seo-referring-domains
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/seo-referring-domains/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [referring-domains-checker](https://apify.com/crawlplant/referring-domains-checker)

```json
{
  "maxItems": 20,
  "domains": [
    "${DOMAIN}"
  ],
  "maxReferrersPerDomain": 20
}
```

