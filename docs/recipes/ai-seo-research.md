# Connect metrics, referrers and similar sites into a research packet

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py ai-seo-research --dry-run
python run.py ai-seo-research
```

Starts up to **3 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/ai-seo-research/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## AI workflow

Select evidence for a domain research brief. Distinguish authority metrics, sampled link data and hypotheses about related sites. Do not equate similarity with commercial competition.

With only `APIFY_TOKEN`, the example writes `evidence.json`, `prompt.md` and a deterministic preview. Attach the first two files to your own assistant. No AI model is called by default.

For the optional model step, set `OPENAI_API_KEY` and `OPENAI_MODEL`, then run:

```sh
python run.py ai-seo-research --reuse --ai
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

### [referring-domains-checker](https://apify.com/crawlplant/referring-domains-checker)

```json
{
  "maxItems": 20,
  "domains": [
    "${DOMAIN}"
  ],
  "maxReferrersPerDomain": 20
}
```

### [similar-sites-finder](https://apify.com/crawlplant/similar-sites-finder)

```json
{
  "maxItems": 20,
  "domains": [
    "${DOMAIN}"
  ],
  "maxReferrersPerDomain": 20
}
```

