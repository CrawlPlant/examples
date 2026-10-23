# Create a factual recap evidence ledger

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py ai-match-recap --dry-run
python run.py ai-match-recap
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/ai-match-recap/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## AI workflow

Explain the result and up to three supported pressure moments in the selected match. Use player names, set and game numbers for readers; retain source URLs and event IDs as receipts. Say when fewer than three moments are supported. Do not infer emotions or causes.

With only `APIFY_TOKEN`, the example writes `evidence.json`, `prompt.md` and a deterministic preview. Attach the first two files to your own assistant. No AI model is called by default.

For the optional model step, set `OPENAI_API_KEY` and `OPENAI_MODEL`, then run:

```sh
python run.py ai-match-recap --reuse --ai
```

This sends the evidence packet to OpenAI and incurs separate model charges. The model selects known evidence IDs (or a validated filter plan); Python supplies factual content. It does not autonomously execute generated code.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [tennis-point-by-point](https://apify.com/crawlplant/tennis-point-by-point)

```json
{
  "maxItems": 20,
  "mode": "matches",
  "pointByPointFormat": "games",
  "dateFrom": "${MATCH_DATE}",
  "dateTo": "${MATCH_DATE}",
  "players": [
    "${MATCH_PLAYER}"
  ],
  "tournaments": [
    "${MATCH_TOURNAMENT}"
  ],
  "tours": [
    "atp"
  ]
}
```


## Find the match by name

Search by surname, tournament and date, then require exactly one match for both players. maxItems caps candidate matches, not games or points. Inspect saved candidates if selection fails. The default is Carlos Alcaraz vs Novak Djokovic, Wimbledon final, 14 July 2024.

Edit `MATCH_PLAYER`, `MATCH_OPPONENT`, `MATCH_DATE` and `MATCH_TOURNAMENT` in `.env`. Use surnames because match labels can be abbreviated. The runner saves all candidates, validates the pair/date/tournament, and writes `selected-match.json` with the returned source identifiers. Never invent an ID or silently select the first match.
