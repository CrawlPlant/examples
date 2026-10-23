# Search Woolworths products with prices

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py woolworths-search --dry-run
python run.py woolworths-search
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/woolworths-search/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [woolworths-au](https://apify.com/crawlplant/woolworths-au)

```json
{
  "maxItems": 20,
  "mode": "search",
  "queries": [
    "${QUERY}"
  ],
  "postcodes": [
    "${POSTCODE}"
  ]
}
```

