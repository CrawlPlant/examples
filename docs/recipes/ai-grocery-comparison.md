# Prepare evidence for a three-retailer shopping comparison

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py ai-grocery-comparison --dry-run
python run.py ai-grocery-comparison
```

Starts up to **3 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/ai-grocery-comparison/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## AI workflow

Select comparable products for a shopping comparison. Compare only matching quantities and unit-price units. Retain retailer, postcode and retrieval context; do not invent a cheapest basket.

With only `APIFY_TOKEN`, the example writes `evidence.json`, `prompt.md` and a deterministic preview. Attach the first two files to your own assistant. No AI model is called by default.

For the optional model step, set `OPENAI_API_KEY` and `OPENAI_MODEL`, then run:

```sh
python run.py ai-grocery-comparison --reuse --ai
```

This sends the evidence packet to OpenAI and incurs separate model charges. The model selects known evidence IDs (or a validated filter plan); Python supplies factual content. It does not autonomously execute generated code.

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
