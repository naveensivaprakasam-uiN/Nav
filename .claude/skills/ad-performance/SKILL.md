---
name: ad-performance
description: Analyze ad campaign performance from Meta Ads Manager, Google Ads, LinkedIn or TikTok exports (CSV/XLSX) by computing CTR, CPC, CPM, CPA, ROAS and CVR, ranking campaigns/ad sets/ads/creatives, spotting winners, losers and fatigue, and recommending budget shifts. Use this whenever the user shares an ads export or report, asks "how are my ads doing", "which creative is winning", "where should I move budget", "why did CPA go up", or wants a performance summary for a client or manager.
---

# Ad Performance Analysis

Turn a raw ads export into decisions: what to scale, what to pause, what to test next.

## 1. Load and compute metrics with the script

Never do the metric maths in your head. Run the bundled script, which normalises column names across platforms and computes every KPI:

```bash
python3 .claude/skills/ad-performance/scripts/analyze_ads.py <file.csv> \
    [--by "Ad set name"] [--target-cpa 400] [--target-roas 3] [--min-spend 500]
```

- `--by`: dimension to group on (campaign / ad set / ad / creative / date / placement). Defaults to the first one found.
- `--target-cpa` / `--target-roas`: if given, each row is labelled SCALE / WATCH / CUT against them.
- `--min-spend`: rows below this spend are marked "low data" and not judged.
- `--json`: machine-readable output if you want to build charts.

For `.xlsx`, convert it to CSV first (the `xlsx` skill, or pandas if installed). If the script can't map a column, it prints what it found. Pass the right header with `--map spend="Amount spent (INR)"` and re-run.

## 2. Read the numbers like a media buyer

Look at these, in this order:

1. **Totals vs. target**: are we on track for the period's goal?
2. **Concentration**: what share of spend went to the top 20% of rows, and are they also the best on CPA/ROAS?
3. **Winners**: CPA below target (or ROAS above it) on meaningful spend. These are candidates to scale by 20–30% per step, not 2×, so you don't reset learning.
4. **Losers**: CPA more than 1.5× target after spending at least 2× target CPA. Pause them or rework the creative.
5. **Funnel diagnosis** when CPA is bad:
   - Low CTR (< ~0.8% on Meta feed) means a creative or hook problem
   - Good CTR but low CVR means a landing page, offer or audience-mismatch problem
   - High CPM means the audience is too narrow or competitive, or there's a seasonality spike
6. **Fatigue** (if there's a date column): frequency above ~3 together with CTR falling week on week means creative refresh is due.

Benchmarks vary a lot by industry and country, so present them as rough guides and prefer the account's own averages as the baseline.

## 3. Output

```markdown
## Summary
3 bullets: headline result vs goal, biggest win, biggest problem.

## Key numbers
| Metric | Value | vs target / prior |

## Top & bottom performers
Table from the script (top 5 / bottom 5 by CPA or ROAS, with spend).

## Diagnosis
Short paragraphs on *why*, tied to the funnel metrics.

## Recommendations
Numbered, each with action + expected impact + confidence. E.g.
1. Shift ₹20k/day from Ad set B → Ad set A (CPA ₹310 vs ₹720). Expect around 25 more conversions a week. High confidence.
```

If the user wants it visual, build charts with the `dataviz` skill (spend vs CPA scatter, daily CPA trend). If it's going to a client, keep the language plain and lead with outcomes, not jargon.

## Caveats to state when relevant

- Attribution windows differ between platforms (Meta defaults to 7-day click / 1-day view), so platform-reported conversions won't match GA4 or CRM.
- Small samples (<30 conversions) are noisy. Say so instead of crowning a winner.
