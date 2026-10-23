# A prediction model versus Elo

![A prediction model versus Elo](../assets/12-ml-baselines.png)

## Run

From the repository root, after installing `tennis/requirements.txt`:

```sh
python tennis/render.py
```

The shared renderer rebuilds all tennis charts and reports in one run.

Output: [PNG](../assets/12-ml-baselines.png) / [SVG](../assets/12-ml-baselines.svg).

Inspect the [result](../reports/model-evaluation.json).

Actors used in the live workflow: [tennis-match-dataset](https://apify.com/crawlplant/tennis-match-dataset).

[Full tutorial and live input examples](https://crawlplant.com/guides/first-tennis-model/).

The default run uses dated saved data and makes no network calls. AI selections are editorial demonstrations; no model response is claimed. See [data provenance and limitations](../README.md).
