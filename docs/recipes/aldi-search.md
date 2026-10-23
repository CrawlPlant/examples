# Search Aldi products with prices

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py aldi-search --dry-run
python run.py aldi-search
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/aldi-search/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [aldi-au](https://apify.com/crawlplant/aldi-au)

```json
{
  "maxItems": 20,
  "mode": "search",
  "queries": [
    "${QUERY}"
  ],
  "postcodes": [
    "${ALDI_POSTCODE}"
  ]
}
```


The default ALDI postcode is 2010; other retailer defaults use 2000. Keep these different store locations visible in comparisons.
