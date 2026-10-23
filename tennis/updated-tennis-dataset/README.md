# Updating a tennis dataset

![Updating a tennis dataset](../assets/01-rank-upsets.png)

## Run

From the repository root, after installing `tennis/requirements.txt`:

```sh
python tennis/render.py
```

The shared renderer rebuilds all tennis charts and reports in one run.

Output: [PNG](../assets/01-rank-upsets.png) / [SVG](../assets/01-rank-upsets.svg).

Inspect the [result](../reports/update-demo.json).

Actors used in the live workflow: [tennis-match-dataset](https://apify.com/crawlplant/tennis-match-dataset).

[Full tutorial and live input examples](https://crawlplant.com/guides/updated-tennis-dataset/).

The default run uses dated saved data and makes no network calls. AI selections are editorial demonstrations; no model response is claimed. See [data provenance and limitations](../README.md).
