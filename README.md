# CrawlPlant examples

**48 live recipes · 15 Actors · 10 AI workflows · Python + JavaScript**

Paste your Apify token into `.env`, choose an example and run it.
Examples cover tennis, grocery prices, SEO, advertising, video trends, bank rates and energy plans.

- [Start here: live setup](docs/LIVE-QUICKSTART.md)
- [Browse all 48 recipes](docs/CATALOG.md)
- [Python and JavaScript examples](code/README.md)
- [Use the examples with an AI agent](docs/AI-AGENTS.md)
- [What was tested](docs/VALIDATION.md)

```sh
python -m pip install -r requirements.txt
# Copy .env.example to .env and paste your APIFY_TOKEN.
python run.py tennis-match-details
python run.py grocery-three-retailers
python run.py ai-tennis-scout
```

AI recipes work with an Apify token alone to generate evidence and prompts for your own
assistant. Optional `--ai` adds a real model call and requires a separate OpenAI key/model.
Live Actor runs can incur charges; each recipe documents how many runs it starts.

Runnable data and AI projects built with [CrawlPlant Actors](https://apify.com/crawlplant).
Start with a finished result, reproduce it locally, then follow the guide to connect live data.

![Four Actors, one investigation](tennis/assets/14-workflow-report.png)

## Original offline gallery: nine tennis projects

Python 3.11 or newer. Run from the repository root:

```sh
python -m venv .venv
# Windows: .venv/Scripts/activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r tennis/requirements.txt
python tennis/render.py
python tennis/render_recap.py
python tests/check_examples.py
```

The default examples run offline: no account, API token, Actor charges or model charges.
Generated figures are in `tennis/assets/`; readable reports and machine-readable results are in `tennis/reports/`.
The shared renderer builds the collection; the illustrated recap also has its own renderer.

## Pick a project

| Example | Actors working together |
|---|---|
| [Updating a tennis dataset](tennis/updated-tennis-dataset/) | tennis-match-dataset |
| [A rivalry across three surfaces](tennis/rivalry-on-three-surfaces/) | tennis-match-history |
| [The pressure behind the scoreline](tennis/wimbledon-pressure-map/) | tennis-point-by-point |
| [Elo versus market expectations](tennis/elo-versus-market/) | flashscore-tennis + tennis-match-history |
| [Four Actors, one match investigation](tennis/season-to-single-point/) | tennis-match-dataset + tennis-match-history + flashscore-tennis + tennis-point-by-point |
| [An AI scout with sources](tennis/ai-tennis-scout/) | flashscore-tennis + tennis-match-history |
| [Ask a question; Python counts](tennis/chat-with-tennis-data/) | tennis-match-dataset |
| [An illustrated match recap](tennis/ai-match-recap/) | tennis-point-by-point |
| [A prediction model versus Elo](tennis/first-tennis-model/) | tennis-match-dataset |

## Find data using names

Live tennis examples start with player surnames, a tournament and a date, such as Alcaraz vs Djokovic at Wimbledon on 14 July 2024. No match ID is required. They verify both opponents and stop on ambiguous results. See [AI agent instructions](docs/AI-AGENTS.md) and [name/date settings](docs/LIVE-QUICKSTART.md). IDs in the offline snapshots remain fixed provenance references; they are not inputs users need to discover.

## How the Actors connect

Match Dataset selects a cohort → Match History supplies prior player context →
Flashscore Tennis adds match details, Elo and odds → Point-by-Point reveals pressure games.
Join by match/player IDs, check player orientation and retain timestamps. Individual projects
only use the Actors they need.

## Live data and optional AI

Follow the linked tutorial for the exact Actor inputs. Install `apify-client` separately and
set `APIFY_TOKEN` in your environment. `tennis/examples.py` provides `call_actor`.
Live calls can incur Apify charges: start small and configure a spending limit in Apify.
Never commit tokens or `.env` files. Live outputs can differ from these snapshots.

`tennis/ai_examples.py` contains optional model functions. They require `OPENAI_API_KEY`
and `OPENAI_MODEL` and can incur separate model charges. The default renderers do not call them.
The examples use explicit editorial selections, compute numbers in Python and preserve source IDs.
The recap artwork is drawn with Matplotlib; it is not an image-model-generated reconstruction.

## Data and scope

See [provenance and limitations](tennis/README.md). The snapshots are dated teaching examples,
not a complete season, an official record, a live prediction service or evidence of betting profit.
We build the Actors linked here. No affiliation with Flashscore, ATP, WTA or Jeff Sackmann.

[More guides](https://crawlplant.com/guides/) · [CrawlPlant](https://crawlplant.com)

## Reuse

No blanket open-source or data license is asserted in this initial publication.
Third-party source data retains applicable rights and terms; contact CrawlPlant before redistribution.
