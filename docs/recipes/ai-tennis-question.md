# Translate a tennis question into validated Python filters

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py ai-tennis-question --dry-run
python run.py ai-tennis-question
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/ai-tennis-question/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## AI workflow

Which WTA players on hard courts have the highest ranking-upset rate, with at least two eligible underdog appearances?

With only `APIFY_TOKEN`, the example writes `evidence.json`, `prompt.md` and a deterministic preview. Attach the first two files to your own assistant. No AI model is called by default.

For the optional model step, set `OPENAI_API_KEY` and `OPENAI_MODEL`, then run:

```sh
python run.py ai-tennis-question --reuse --ai
```

This sends the evidence packet to OpenAI and incurs separate model charges. The model selects known evidence IDs (or a validated filter plan); Python supplies factual content. It does not autonomously execute generated code.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [tennis-match-dataset](https://apify.com/crawlplant/tennis-match-dataset)

```json
{
  "maxItems": 200,
  "years": [],
  "dateFrom": "${DATE_FROM}",
  "dateTo": "${DATE_TO}",
  "tours": [
    "atp",
    "wta"
  ]
}
```

