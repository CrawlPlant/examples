# Build a source-linked scouting packet from three Actor calls

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py ai-tennis-scout --dry-run
python run.py ai-tennis-scout
```

Starts up to **3 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/ai-tennis-scout/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## AI workflow

Prepare a concise tennis scout using only eligible pre-match ratings and completed prior matches. State history gaps. Do not use the target result.

With only `APIFY_TOKEN`, the example writes `evidence.json`, `prompt.md` and a deterministic preview. Attach the first two files to your own assistant. No AI model is called by default.

For the optional model step, set `OPENAI_API_KEY` and `OPENAI_MODEL`, then run:

```sh
python run.py ai-tennis-scout --reuse --ai
```

This sends the evidence packet to OpenAI and incurs separate model charges. The model selects known evidence IDs (or a validated filter plan); Python supplies factual content. It does not autonomously execute generated code.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [flashscore-tennis](https://apify.com/crawlplant/flashscore-tennis)

```json
{
  "maxItems": 20,
  "mode": "matches",
  "includeOdds": false,
  "includeH2H": false,
  "dateFrom": "${SCOUT_DATE}",
  "dateTo": "${SCOUT_DATE}",
  "players": [
    "${SCOUT_PLAYER}"
  ],
  "tournaments": [
    "${SCOUT_TOURNAMENT}"
  ],
  "tours": [
    "wta"
  ]
}
```


## Find the match by name

Search by surname, tournament and date, then require exactly one match for both players. maxItems caps candidate matches, not games or points. Inspect saved candidates if selection fails. The default is Karolina Muchova vs Diana Shnaider, Wuhan, 15 October 2026 (a retrospective scout).

Edit `SCOUT_PLAYER`, `SCOUT_OPPONENT`, `SCOUT_DATE` and `SCOUT_TOURNAMENT` in `.env`. Use surnames because match labels can be abbreviated. The runner saves all candidates, validates the pair/date/tournament, and writes `selected-match.json` with the returned source identifiers. Never invent an ID or silently select the first match.
