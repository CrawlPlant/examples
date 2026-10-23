# Search Coles products with prices

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py coles-search --dry-run
python run.py coles-search
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/coles-search/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [coles-au](https://apify.com/crawlplant/coles-au)

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

