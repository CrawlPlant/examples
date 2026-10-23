# Live examples: paste your Apify token and run

The live catalog covers 15 CrawlPlant Actors. Each recipe is independent;
you do not need to run the earlier tennis tutorials first.

## 1. Install

Python 3.11+:

```sh
git clone https://github.com/CrawlPlant/examples.git
cd examples
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or macOS/Linux:

```sh
source .venv/bin/activate
```

If activation is unavailable, use `.venv/Scripts/python.exe` (Windows) or
`.venv/bin/python` (macOS/Linux) instead of `python` in every command.

```sh
python -m pip install -r requirements.txt
python -c "from pathlib import Path; p=Path('.env'); p.exists() or p.write_text(Path('.env.example').read_text())"
```

## 2. Edit .env

Get your token from [Apify Console → API & Integrations](https://console.apify.com/settings/integrations).
Paste it into the local `.env`:

```dotenv
APIFY_TOKEN=your_actual_token
APIFY_MAX_CHARGE_USD=0.50
```

Only `APIFY_TOKEN` is required. All filters have usable defaults.
Environment variables already set in your terminal take precedence over `.env`.
The loader always reads the `.env` beside `run.py`, regardless of working directory.
The token and local output folder are ignored by Git.

## 3. Choose an example

```sh
python run.py --list
python run.py tennis-match-details --dry-run
python run.py tennis-match-details
python run.py grocery-three-retailers
python run.py seo-link-gap
python run.py ai-tennis-scout
```

See the [full catalog](CATALOG.md) for every command, its input and number of Actor runs.
`--dry-run` prints the resolved inputs without contacting Apify or a model.
There is deliberately no run-all command: selecting one recipe keeps costs predictable.

## Outputs and costs

`output/<recipe>/<source>/` contains `data.json`, `data.jsonl`, `data.csv`,
`data.sqlite` and `run.json`. SQLite stores each raw object in a `records` table;
nested CSV objects are JSON strings. Formula-like CSV text is escaped for spreadsheet safety.

`run.json` records the Actor input, run/dataset IDs, retrieval time, status,
requested charge limit and row count. Analytical recipes also produce derived reports.
An empty export can be legitimate; a source may have no live matches, no eligible history,
no point coverage or no results for your filters. Missing evidence is not fabricated.

The default charge limit is **USD 0.50 per Actor run**, not per command.
For example, the three-retailer comparison makes three runs (up to USD 1.50 in
requested Actor charge limits), and the scout can make three runs too.
Apify billing and the Actor's charging model determine the final charge; check your
account limits. A low budget can stop a run or reduce its results. Model charges are separate.

`APIFY_TIMEOUT_SECONDS=180` is the requested Actor runtime limit. Dataset downloads
and network waits can take additional time. If a network error leaves a run uncertain,
inspect Apify Console before rerunning; it may already have started.

```sh
python run.py ai-tennis-scout --reuse
```

`--reuse` reads a successful local export only when its Actor and input match.
It avoids a fresh call but can return stale prices, rankings or scores. Omit it to refresh.
Each source folder is replaced on refresh; copy outputs elsewhere if you need a historical archive.
`tennis-refresh-dataset` additionally maintains `merged.json`, updating matching match IDs.

## Change filters

Edit `.env`, for example:

```dotenv
PLAYER=Iga Swiatek
OPPONENT=Sabalenka
MATCH_ID=Sf0bExdB
SCOUT_MATCH_ID=Q3fQfAg2
QUERY=coffee
POSTCODE=2000
ALDI_POSTCODE=2010
DOMAIN=apify.com
YOUR_DOMAIN=scrapy.org
COMPETITOR=zyte.com
DATE_FROM=2026-10-12
DATE_TO=2026-10-18
```

Change `recipes/<name>.json` for other modes, maximum rows or advanced options.
`years: []` in date-window dataset examples is intentional: it overrides the Actor's default season.
For an exact player identity, use a Flashscore player URL instead of an ambiguous name.
Grocery postcodes select stores in that postcode, not automatically the nearest store.
The worked Sydney defaults use 2000 for Woolworths/Coles and nearby 2010 for ALDI:
there is no ALDI in 2000 and the tested Coles lookup found none in 2010. These are
different store catchments, not a same-store or identical-location price comparison.
Choose postcodes with stores for each retailer, or edit a recipe to supply explicit
`storeIds`. Keep store context attached to comparisons.
Historical scouting uses only eligible earlier history from the bounded export; it may be sparse.
The scout has its own `SCOUT_MATCH_ID` (a recorded Muchova–Shnaider match); the recap uses
`MATCH_ID` (the recorded Wimbledon final). Set the scout ID to an upcoming match for prospective use.

## AI with just an Apify token

AI recipes first fetch data and write `evidence.json`, `prompt.md` and a deterministic
preview. Attach the evidence and prompt to your preferred assistant. This path needs
only an Apify token in this repository; your assistant has its own account and usage terms.

## Optional AI directly from Python

Add your own key and a Responses API model available to your OpenAI account:

```dotenv
OPENAI_API_KEY=your_actual_key
OPENAI_MODEL=your_supported_model_id
```

```sh
python run.py ai-match-recap --reuse --ai
python run.py ai-tennis-question --reuse --ai
python run.py ai-ad-creative-review --reuse --ai
```

This sends the evidence to OpenAI and can incur model charges. The model selects
known evidence IDs; Python renders the original facts. The question example lets
the model select a validated filter plan, then Python computes the ranking-upset rates.
No model-generated Python or SQL is executed. Without `--ai`, no model is called.

The recap recipe produces evidence and text. The existing
`python tennis/render_recap.py` separately renders the fixed saved Wimbledon card;
it is not a general image generator for arbitrary live matches.

## Troubleshooting

| Symptom | Action |
|---|---|
| Missing APIFY_TOKEN | Save `.env` beside `run.py`; do not leave the field blank. |
| Authentication failure | Verify the token and Actor permissions in Apify Console. |
| Insufficient credit or failed run | Check billing and the run ID in `run.json`; do not blindly retry. |
| Item cap reached | Treat output as a sample or deliberately increase `maxItems` and budget. |
| No eligible scout history | Inspect the cutoff and history exports; widen the history cap if appropriate. |
| Empty AI evidence | Broaden filters or use a date with known records; don't invent an answer. |
| Model error | Check model availability and structured-output support; use the prompt packet instead. |

## Validation

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -p "test_*.py"
```

Tests use fake clients and recorded public input schemas, so they make no paid calls.
Read [validation coverage](VALIDATION.md) for which live calls were actually checked.
