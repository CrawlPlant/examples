# Find a match by player names, tournament and date

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py tennis-match-details --dry-run
python run.py tennis-match-details
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/tennis-match-details/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [flashscore-tennis](https://apify.com/crawlplant/flashscore-tennis)

```json
{
  "maxItems": 20,
  "mode": "matches",
  "includeOdds": false,
  "includeH2H": false,
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
