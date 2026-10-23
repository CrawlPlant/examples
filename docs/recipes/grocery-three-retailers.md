# Collect comparable search results from three retailers

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py grocery-three-retailers --dry-run
python run.py grocery-three-retailers
```

Starts up to **3 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/grocery-three-retailers/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Interpretation

Products are not automatically matched. Compare pack sizes, unit labels, store context and dates before comparing prices.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [woolworths-au](https://apify.com/crawlplant/woolworths-au)

```json
{
  "maxItems": 10,
  "mode": "search",
  "queries": [
    "${QUERY}"
  ],
  "postcodes": [
    "${POSTCODE}"
  ]
}
```

### [coles-au](https://apify.com/crawlplant/coles-au)

```json
{
  "maxItems": 10,
  "mode": "search",
  "queries": [
    "${QUERY}"
  ],
  "postcodes": [
    "${POSTCODE}"
  ]
}
```

### [aldi-au](https://apify.com/crawlplant/aldi-au)

```json
{
  "maxItems": 10,
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
