# Four Actors, one match investigation

![Four Actors, one match investigation](../assets/14-workflow-report.png)

## Run

From the repository root, after installing `tennis/requirements.txt`:

```sh
python tennis/render.py
```

The shared renderer rebuilds all tennis charts and reports in one run.

Output: [PNG](../assets/14-workflow-report.png) / [SVG](../assets/14-workflow-report.svg).

Inspect the [result](../reports/workflow.md).

Actors used in the live workflow: [tennis-match-dataset](https://apify.com/crawlplant/tennis-match-dataset), [tennis-match-history](https://apify.com/crawlplant/tennis-match-history), [flashscore-tennis](https://apify.com/crawlplant/flashscore-tennis), [tennis-point-by-point](https://apify.com/crawlplant/tennis-point-by-point).

[Full tutorial and live input examples](https://crawlplant.com/guides/season-to-single-point/).

The default run uses dated saved data and makes no network calls. AI selections are editorial demonstrations; no model response is claimed. See [data provenance and limitations](../README.md).
