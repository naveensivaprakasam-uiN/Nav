---
name: campaign-brief
description: Turn a rough idea, product launch, or client request into a structured marketing campaign brief covering objective, audience, key message, channels, budget split, creative asks, KPIs and timeline. Use this whenever the user mentions a campaign, launch plan, media plan, creative brief, GTM plan, promo, or says something like "plan a campaign for…", "we're launching X next month", or "brief the design team".
---

# Campaign Brief

Produce a one-page brief that a designer, media buyer and stakeholder can all act on without a follow-up meeting.

## Workflow

1. **Extract** everything you can from the user's input: product, offer, dates, budget, audience, past results.
2. **Ask at most 3 questions**, and only if the answer changes the plan. The usual blockers are budget, launch date and primary goal. For anything else, assume, then list it under *Assumptions*.
3. **Draft** using the template below. Be concrete: numbers, dates, named channels, not "leverage social media".
4. **Sanity-check** the numbers. The budget split must add up to 100%, KPI targets must be consistent with budget (for example, budget ÷ target CPA = expected conversions), and the timeline must fit before launch.

## Template

```markdown
# [Campaign name] — Brief
**Owner:** … · **Dates:** start → end · **Budget:** total (currency)

## Objective
One sentence. One primary goal (e.g. "Drive 1,200 trial sign-ups at ≤₹400 CPA").
Secondary goals, if any.

## Audience
- Primary: who, where, what they care about, what stops them buying
- Secondary / exclusions
- Targeting notes (interests, lookalikes, retargeting pools, keywords)

## Key message
- Single-minded proposition (one line)
- 3 proof points / reasons to believe
- Offer & CTA

## Channels & budget
| Channel | Role (prospecting / retargeting / search) | % | Amount | KPI |
|---|---|---|---|---|

## Creative asks
| Asset | Format / size | Qty | Angle | Due |
|---|---|---|---|---|
(e.g. Meta 1:1 + 9:16 static ×4, 15s video ×2, RSA set ×1)

## Measurement
- Primary KPI + target, secondary KPIs
- Tracking: pixel/CAPI events, UTMs, conversion definitions
- Test plan: what we're A/B testing first

## Timeline
| Date | Milestone |
|---|---|

## Risks & assumptions
- …
```

## Defaults when the user doesn't say

- Budget split for a performance campaign: ~70% prospecting, ~20% retargeting, ~10% testing.
- Creative volume: at least 3 distinct angles × 2 formats per channel, so there's something to test.
- Learning phase: on Meta, an ad set needs ~50 conversions a week to exit learning. Flag it if the budget can't get there.

Hand off to the `ad-copy` skill if the user wants the actual copy written next.
