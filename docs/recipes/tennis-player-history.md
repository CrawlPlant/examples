# Export recent completed player matches

[Setup](../../docs/LIVE-QUICKSTART.md) · [All recipes](../CATALOG.md)

```sh
python run.py tennis-player-history --dry-run
python run.py tennis-player-history
```

Starts up to **1 Actor run(s)**. Each run uses `APIFY_MAX_CHARGE_USD`; this is not a per-recipe budget. `--reuse` reuses matching saved exports and can be stale.

Results: `output/tennis-player-history/`. Each source has JSON, JSONL, CSV, SQLite and `run.json` with IDs, inputs, retrieval time and cap information.

## Actor inputs

Edit the recipe JSON to change filters or sample size. `${NAME}` values come from `.env`.

### [tennis-match-history](https://apify.com/crawlplant/tennis-match-history)

```json
{
  "maxItems": 50,
  "playerUrls": [
    "${PLAYER}"
  ],
  "status": "finished"
}
```

