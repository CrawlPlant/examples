# Prepare evidence to explain electricity plan estimates

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py ai-energy-explainer --dry-run
python run.py ai-energy-explainer
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/ai-energy-explainer/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## AI workflow

Select plan records to explain a 4,000 kWh/year electricity estimate. Preserve supply charges, usage assumptions and conditions. Do not promise savings.

With only `APIFY_TOKEN`, the example writes `evidence.json`, `prompt.md` and a deterministic preview. Attach the first two files to your own assistant. No AI model is called by default.

For the optional model step, set `OPENAI_API_KEY` and `OPENAI_MODEL`, then run:

```sh
python run.py ai-energy-explainer --reuse --ai
```

This sends the evidence packet to OpenAI and incurs separate model charges. The model selects known evidence IDs (or a validated filter plan); Python supplies factual content. It does not autonomously execute generated code.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [au-energy-plans](https://apify.com/crawlplant/au-energy-plans)

```json
{
  "maxItems": 10,
  "mode": "cheapest",
  "postcodes": [
    "${POSTCODE}"
  ],
  "fuelTypes": [
    "ELECTRICITY"
  ],
  "annualKwh": 4000
}
```

