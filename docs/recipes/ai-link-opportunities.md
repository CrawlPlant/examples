# Prepare a source-backed link research shortlist

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py ai-link-opportunities --dry-run
python run.py ai-link-opportunities
```

Starts up to **2 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/ai-link-opportunities/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## AI workflow

Select candidate referring domains for manual relevance review. Explain that a link gap does not guarantee outreach suitability or ranking gains. Do not contact anyone.

With only `APIFY_TOKEN`, the example writes `evidence.json`, `prompt.md` and a deterministic preview. Attach the first two files to your own assistant. No AI model is called by default.

For the optional model step, set `OPENAI_API_KEY` and `OPENAI_MODEL`, then run:

```sh
python run.py ai-link-opportunities --reuse --ai
```

This sends the evidence packet to OpenAI and incurs separate model charges. The model selects known evidence IDs (or a validated filter plan); Python supplies factual content. It does not autonomously execute generated code.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [commoncrawl-domain-metrics](https://apify.com/crawlplant/commoncrawl-domain-metrics)

```json
{
  "maxItems": 20,
  "domains": [
    "${DOMAIN}",
    "${COMPETITOR}"
  ],
  "mode": "profiles"
}
```

### [link-gap-finder](https://apify.com/crawlplant/link-gap-finder)

```json
{
  "maxItems": 20,
  "yourDomain": "${YOUR_DOMAIN}",
  "domains": [
    "${DOMAIN}",
    "${COMPETITOR}"
  ],
  "maxReferrersPerDomain": 30
}
```

