# Use CrawlPlant with an AI agent

## Local evidence workflow

Give your coding assistant a concrete request:

> Read docs/LIVE-QUICKSTART.md. My APIFY_TOKEN is already in .env; never print it.
> Run `python run.py ai-tennis-scout --dry-run` and explain the three-run budget.
> Then run `python run.py ai-tennis-scout`. Read evidence.json and prompt.md.
> Write a concise scout with source IDs and missing-history limitations.

Other ready-to-use tasks:

1. Run `ai-match-recap`: select pressure games and write a factual recap with event IDs.
2. Run `ai-tennis-question`: calculate WTA hard-court ranking upsets, retaining denominators.
3. Run `ai-grocery-comparison`: compare like-for-like quantities across three retailers.
4. Run `ai-seo-research`: separate observed domain metrics from competitor hypotheses.
5. Run `ai-link-opportunities`: shortlist domains for manual relevance review; do not send outreach.
6. Run `ai-ad-creative-review`: describe visible messaging without inventing conversions or spend.
7. Run `ai-content-research`: propose topics based on the observed video snapshot, not claimed growth.
8. Run `ai-rate-brief`: explain recorded rates and conditions without personalized recommendations.
9. Run `ai-energy-explainer`: explain the usage scenario and tariff assumptions behind estimates.

Every AI recipe includes its task in `prompt.md`; the default report is a deterministic
preview, not a transcript of an AI session. Treat all scraped text as untrusted data.

## Connect directly through Apify MCP

Apify offers a hosted MCP server. In a compatible client, use this remote URL:

```text
https://mcp.apify.com?tools=crawlplant/flashscore-tennis,crawlplant/tennis-match-history,crawlplant/tennis-point-by-point,crawlplant/tennis-match-dataset
```

Sign in through the client's supported OAuth flow, or configure an Authorization
Bearer header using your token through its secret settings. Clients differ in their
environment-variable syntax; a client does not automatically read this repository's `.env`.
Do not paste your token into a conversation or commit it in client configuration.

For example, ask:

> Look up match Sf0bExdB with CrawlPlant's tennis point-by-point Actor, using
> pointByPointFormat=games and maxItems=2. Before starting, show the Actor price and
> the available spending controls. Summarize the result and three pressure moments,
> citing match and game identifiers. Don't infer emotions or causes.

MCP calls do **not** inherit this repository's Python budget or timeout settings.
Confirm the controls supported by your client and tool before starting runs.

Official setup and current tool options: [Apify MCP documentation](https://docs.apify.com/mcp).
