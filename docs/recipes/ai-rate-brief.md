# Prepare a cited rate-comparison evidence packet

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py ai-rate-brief --dry-run
python run.py ai-rate-brief
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/ai-rate-brief/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## AI workflow

Select rate records for a factual term-deposit brief. Preserve term, amount, conditions and date. Do not recommend a personal investment or imply eligibility.

With only `APIFY_TOKEN`, the example writes `evidence.json`, `prompt.md` and a deterministic preview. Attach the first two files to your own assistant. No AI model is called by default.

For the optional model step, set `OPENAI_API_KEY` and `OPENAI_MODEL`, then run:

```sh
python run.py ai-rate-brief --reuse --ai
```

This sends the evidence packet to OpenAI and incurs separate model charges. The model selects known evidence IDs (or a validated filter plan); Python supplies factual content. It does not autonomously execute generated code.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [au-bank-rates](https://apify.com/crawlplant/au-bank-rates)

```json
{
  "maxItems": 10,
  "mode": "best",
  "categories": [
    "TERM_DEPOSITS"
  ],
  "termMonths": [
    12
  ],
  "amount": 10000
}
```

