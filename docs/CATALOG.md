# 48 live recipes

Every command runs independently from the repository root after [setup](LIVE-QUICKSTART.md).
Empty results are valid when a source has no matching data. Caps produce samples, not exhaustive exports.

| Recipe | Result | Type | Max Actor runs |
|---|---|---|---|
| [tennis-daily-matches](recipes/tennis-daily-matches.md) | Export yesterday’s completed tennis matches | Code | 1 |
| [tennis-live-scoreboard](recipes/tennis-live-scoreboard.md) | Capture the current live scoreboard | Code | 1 |
| [tennis-upcoming](recipes/tennis-upcoming.md) | Fetch the scheduled match list | Code | 1 |
| [tennis-match-details](recipes/tennis-match-details.md) | Find a match by player names, tournament and date | Code | 1 |
| [tennis-player-profile](recipes/tennis-player-profile.md) | Find a player profile by name | Code | 1 |
| [tennis-player-history](recipes/tennis-player-history.md) | Export recent completed player matches | Code | 1 |
| [tennis-surface-stats](recipes/tennis-surface-stats.md) | Compare a player’s statistics by surface | Code | 1 |
| [tennis-opponent-bands](recipes/tennis-opponent-bands.md) | Inspect statistics by opponent rank band | Code | 1 |
| [tennis-rankings](recipes/tennis-rankings.md) | Export a bounded ATP/WTA ranking snapshot | Code | 1 |
| [tennis-historical-rankings](recipes/tennis-historical-rankings.md) | Retrieve a dated ranking list | Code | 1 |
| [tennis-surface-elo](recipes/tennis-surface-elo.md) | Retrieve grass-court Elo ratings | Code | 1 |
| [tennis-dataset](recipes/tennis-dataset.md) | Export winner/loser rows to JSON, CSV and SQLite | Code | 1 |
| [tennis-cohort-summary](recipes/tennis-cohort-summary.md) | Count tours, surfaces and missing ranks | Code | 1 |
| [tennis-refresh-dataset](recipes/tennis-refresh-dataset.md) | Keep a results dataset up to date without duplicates | Code | 1 |
| [tennis-point-games](recipes/tennis-point-games.md) | Download game-format point data | Code | 1 |
| [tennis-point-stream](recipes/tennis-point-stream.md) | Download a Sackmann-format point stream | Code | 1 |
| [tennis-pressure-games](recipes/tennis-pressure-games.md) | Compute break-point pressure games | Code | 1 |
| [tennis-join-dataset-points](recipes/tennis-join-dataset-points.md) | Join two Actors by match identity | Code | 2 |
| [tennis-rivalry-surfaces](recipes/tennis-rivalry-surfaces.md) | Resolve identity and aggregate a rivalry by surface | Code | 2 |
| [tennis-elo-market](recipes/tennis-elo-market.md) | Compute Elo-versus-market probability differences | Code | 1 |
| [woolworths-search](recipes/woolworths-search.md) | Search Woolworths products with prices | Code | 1 |
| [coles-search](recipes/coles-search.md) | Search Coles products with prices | Code | 1 |
| [aldi-search](recipes/aldi-search.md) | Search Aldi products with prices | Code | 1 |
| [grocery-specials](recipes/grocery-specials.md) | Fetch Coles specials and discounts | Code | 1 |
| [grocery-price-history](recipes/grocery-price-history.md) | Fetch Woolworths products with price history | Code | 1 |
| [grocery-three-retailers](recipes/grocery-three-retailers.md) | Collect comparable search results from three retailers | Code | 3 |
| [seo-domain-metrics](recipes/seo-domain-metrics.md) | Compare domain metrics from public data sources | Code | 1 |
| [seo-domain-history](recipes/seo-domain-history.md) | Export domain metrics across releases | Code | 1 |
| [seo-referring-domains](recipes/seo-referring-domains.md) | Inspect a sample of referring domains | Code | 1 |
| [seo-link-gap](recipes/seo-link-gap.md) | Find referring domains shared by competitors | Code | 1 |
| [seo-similar-sites](recipes/seo-similar-sites.md) | Discover sites with related linking patterns | Code | 1 |
| [ads-creatives](recipes/ads-creatives.md) | Export ad creatives and their source records | Code | 1 |
| [ads-advertisers](recipes/ads-advertisers.md) | Resolve advertisers for a domain | Code | 1 |
| [ads-timeline](recipes/ads-timeline.md) | Retrieve an advertiser activity timeline | Code | 1 |
| [bilibili-tech-ranking](recipes/bilibili-tech-ranking.md) | Collect a technology video ranking snapshot | Code | 1 |
| [bilibili-hot-searches](recipes/bilibili-hot-searches.md) | Collect current hot search terms | Code | 1 |
| [bank-term-deposits](recipes/bank-term-deposits.md) | Export 12-month term-deposit rate records | Code | 1 |
| [energy-plan-estimates](recipes/energy-plan-estimates.md) | Compare electricity estimates for an explicit usage scenario | Code | 1 |
| [ai-tennis-scout](recipes/ai-tennis-scout.md) | Build a source-linked scouting packet from three Actor calls | AI + data | 3 |
| [ai-match-recap](recipes/ai-match-recap.md) | Create a factual recap evidence ledger | AI + data | 1 |
| [ai-tennis-question](recipes/ai-tennis-question.md) | Translate a tennis question into validated Python filters | AI + data | 1 |
| [ai-grocery-comparison](recipes/ai-grocery-comparison.md) | Prepare evidence for a three-retailer shopping comparison | AI + data | 3 |
| [ai-seo-research](recipes/ai-seo-research.md) | Connect metrics, referrers and similar sites into a research packet | AI + data | 3 |
| [ai-link-opportunities](recipes/ai-link-opportunities.md) | Prepare a source-backed link research shortlist | AI + data | 2 |
| [ai-ad-creative-review](recipes/ai-ad-creative-review.md) | Prepare evidence for an ad messaging review | AI + data | 1 |
| [ai-content-research](recipes/ai-content-research.md) | Prepare a video-topic research packet | AI + data | 1 |
| [ai-rate-brief](recipes/ai-rate-brief.md) | Prepare a cited rate-comparison evidence packet | AI + data | 1 |
| [ai-energy-explainer](recipes/ai-energy-explainer.md) | Prepare evidence to explain electricity plan estimates | AI + data | 1 |
