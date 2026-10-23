# Validation coverage

Checked 23 October 2026 on Windows with Python 3.13 and Node 22.

## Automated checks

- 48 recipe input definitions validated against the public schemas of the 15 deployed Actors.
  Build IDs and public schema URLs are recorded in `tests/schemas/manifest.json`.
- 11 unit tests cover input schemas, charge/timeout arguments, dataset iteration,
  JSON/CSV/SQLite exports, CSV formula escaping, reuse identity, failed runs,
  invalid budgets, `.env` precedence, match identity, AI evidence validation,
  scouting and offline report generation.
- The original offline gallery's identity, cutoff and output checks also pass.
- JavaScript syntax and dry-run behavior checked with Node.
- Public files scanned for known local credentials and private local paths.

## Live Actor smoke tests

Small calls (usually `maxItems=2`, requested charge limit USD 0.05 per run):

| Actor | Tested operation |
|---|---|
| flashscore-tennis | Match lookup and player profile |
| tennis-match-history | Player history |
| tennis-match-dataset | Date-window export |
| tennis-point-by-point | Game-format point data |
| woolworths-au | Product search |
| coles-au | Product search |
| aldi-au | Product search |
| commoncrawl-domain-metrics | Domain profiles |
| referring-domains-checker | Referring domains |
| link-gap-finder | Link gap |
| similar-sites-finder | Similar sites |
| google-ads-transparency | Advertiser resolution |
| bilibili-trending-history | Technology ranking |
| au-bank-rates | Term-deposit records |
| au-energy-plans | Electricity estimates |

The ALDI test initially returned no store for postcode 2000. The shared grocery
examples were checked again at 2010, which returned ALDI data but no Coles store.
The final defaults therefore use `POSTCODE=2000` and `ALDI_POSTCODE=2010`, retaining
each retailer's store context instead of implying identical locations.
Some grocery Actors return store-specific rows, so the output row count can exceed
the product cap. The wrapper preserves all returned rows and labels bounded exports.

End-to-end `ai-tennis-scout` and `ai-match-recap` were run with live Apify data,
without calling a model. The standalone JavaScript match lookup also completed live.

## Limits

Not every mode/filter combination in all 48 recipes was run live. Schema validation
checks accepted inputs, not guaranteed source availability. External data, Actor
versions, pricing, rankings and store coverage can change.

No paid OpenAI model call was made during validation. The optional model path reuses
the evidence-first helpers and validates model selections, but model availability,
quota and structured-output support depend on the user's account.

The default AI output is explicitly a deterministic evidence preview. It is not
presented as an actual model response. Historical scouting may have missing eligible
history; dated snapshots are not archived pre-match predictions.
