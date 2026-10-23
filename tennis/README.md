# CrawlPlant tennis guides: offline companion

Run `python -m pip install -r requirements.txt`, then `python render.py`.
No API token, Actor call or model call is needed. Outputs are written to assets/ and reports/.
The chart source is render.py and ai_assets.py; reports.py produces the finished reports.
examples.py and ai_examples.py contain the same calculations used in the tutorials.

Data: saved 233-row match export, 116 point streams, 20 enriched matches and five history
records retrieved in October 2026, plus the recorded 2024 Wimbledon final point feed.
worked-followups.json contains additional read-only CrawlPlant database records retrieved
23 October 2026 for the same-match workflow, the Machac follow-up and the rivalry.
Those supplementary records are cached source data, not new Apify Actor runs.
Retrieval timestamps, source URLs and match IDs are preserved. No credentials are included.

The 17-match rivalry excludes retirements and exhibitions; the earlier aggregate's 18
included a retirement. The 233-row sample is not a season, and the 116-row overlap is not
overall product coverage. Historical ratings and odds were retrieved after the events.
AI examples use editorial selections, not a recorded paid-model response.
The package reproduces these dated examples; live Actor requests can return different results.
