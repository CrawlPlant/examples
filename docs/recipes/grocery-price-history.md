# Fetch Woolworths products with price history

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py grocery-price-history --dry-run
python run.py grocery-price-history
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/grocery-price-history/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

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
  ],
  "priceHistoryDays": 14
}
```

