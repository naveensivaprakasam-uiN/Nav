---
name: data-insights
description: Analyze a spreadsheet, CSV, SQL result or pasted table and return decision-ready insights covering what changed, why, and what to do, backed by computed numbers rather than eyeballed ones. Use this whenever the user shares data and asks to analyze, summarize, find trends, compare periods, break down metrics, explain a drop/spike, segment, or "tell me what's interesting here", or asks for a SQL query to answer a business question. For ad-platform exports specifically, prefer the ad-performance skill.
---

# Data Insights

Turn data into a short list of findings someone can act on. Every number you quote must come from code you ran, not from reading the table by eye.

## Workflow

### 1. Profile first (always)
Load the data with Python (pandas if available, otherwise `csv`) and print:
- row and column count, column names and dtypes
- date range, if there's a date column
- nulls, duplicates, obviously bad values (negative spend, future dates, totals rows)
- cardinality of categorical columns

Tell the user about any data-quality issue that would change conclusions *before* you analyse. Don't silently drop rows: say what you excluded and why.

### 2. Pin down the question
If the user's ask is vague ("analyze this"), pick the 2–3 questions that matter most for this kind of data and say which ones you chose. Typical ones:
- **Trend**: how is the key metric moving over time? Use week-over-week or month-over-month, not day-level noise.
- **Comparison**: this period vs last, or segment A vs B
- **Drivers**: which segment explains most of the change? (Contribution = segment Δ ÷ total Δ.)
- **Distribution**: is it concentrated? What do the top 10% contribute?

### 3. Compute
- Use ratios of sums, not averages of ratios. Overall CTR is Σclicks / Σimpressions, not the mean of the per-row CTRs.
- Report absolute **and** relative change: "+₹42k (+18%)".
- When a change is small or n is small, say whether it's likely noise.
- Look for Simpson's paradox when segments have very different sizes.

### 4. Present

```markdown
## TL;DR
1–3 sentences with the single most important finding and the recommended action.

## Findings
1. **Headline finding.** Supporting number(s). Why it matters.
2. …

## Supporting table
Compact table (≤10 rows) with the numbers behind the findings.

## Caveats & next steps
Data gaps, assumptions, what to check next.
```

Lead with the insight, not the method. "Repeat customers drove 70% of the revenue drop" beats "I grouped by customer type and computed deltas".

If a chart would make a finding clearer (a trend, comparison or distribution), use the `dataviz` skill. If the user wants a cleaned or enriched spreadsheet back, use the `xlsx` skill.

## SQL requests
When asked for a query: ask for or infer the dialect (BigQuery, Postgres, MySQL, Snowflake), write readable CTEs, comment any non-obvious join or filter, and guard against divide-by-zero (`SAFE_DIVIDE` / `NULLIF`). If `bq` is available and the user has granted access, offer to run it.
