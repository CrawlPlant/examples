# An AI scout with sources

![An AI scout with sources](../assets/07-ai-scout-card.png)

## Run

From the repository root, after installing `tennis/requirements.txt`:

```sh
python tennis/render.py
```

The shared renderer rebuilds all tennis charts and reports in one run.

Output: [PNG](../assets/07-ai-scout-card.png) / [SVG](../assets/07-ai-scout-card.svg).

Inspect the [result](../reports/scout.md).

Actors used in the live workflow: [flashscore-tennis](https://apify.com/crawlplant/flashscore-tennis), [tennis-match-history](https://apify.com/crawlplant/tennis-match-history).

[Full tutorial and live input examples](https://crawlplant.com/guides/ai-tennis-scout/).

The default run uses dated saved data and makes no network calls. AI selections are editorial demonstrations; no model response is claimed. See [data provenance and limitations](../README.md).
