# Resolve identity and aggregate a rivalry by surface

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py tennis-rivalry-surfaces --dry-run
python run.py tennis-rivalry-surfaces
```

Starts up to **2 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/tennis-rivalry-surfaces/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [flashscore-tennis](https://apify.com/crawlplant/flashscore-tennis)

```json
{
  "maxItems": 2,
  "mode": "playerProfiles",
  "playerUrls": [
    "${PLAYER}"
  ]
}
```

### [tennis-match-history](https://apify.com/crawlplant/tennis-match-history)

```json
{
  "maxItems": 100,
  "playerUrls": [
    "${PLAYER}"
  ],
  "players": [
    "${OPPONENT}"
  ],
  "status": "finished"
}
```

