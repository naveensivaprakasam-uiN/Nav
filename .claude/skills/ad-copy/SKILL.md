---
name: ad-copy
description: Write ad copy variants (headlines, primary text, descriptions, CTAs) for Meta/Facebook/Instagram, Google Search & Display, LinkedIn and TikTok, sized to each platform's character limits. Use this whenever the user asks for ad copy, ad text, headlines, hooks, taglines, creative variants, A/B test copy, or "write ads for X" — even if they only paste a product description or landing page and say "make some ads".
---

# Ad Copy

Produce on-brief, platform-ready ad copy that can be pasted straight into an ads manager. The goal is a set of meaningfully *different* variants a marketer can A/B test, not ten rewordings of one idea.

## 1. Gather the brief

Pull these from what the user gave you (product page, notes, previous ads). Ask only for what is missing and actually blocks you; otherwise state a sensible assumption and go.

- **Product / offer**: what it is, price or discount, any deadline
- **Audience**: who, and the pain or desire that matters most to them
- **Platform(s) & placement**: default to Meta feed if unstated
- **Goal**: awareness, traffic, leads, sales/conversions, app installs
- **Brand voice**: e.g. playful, premium, direct. Mirror any copy the user pasted.
- **Must-say / must-avoid**: legal claims, competitor names, banned words

## 2. Pick distinct angles

Write each variant from a different angle so the test teaches something. Choose 3–5 that fit:

| Angle | Hook pattern |
|---|---|
| Pain → relief | "Tired of X? …" |
| Outcome / benefit | "Get X in Y days" |
| Social proof | "Join 10,000+ …", review quote |
| Urgency / scarcity | "Ends Sunday", "Only 50 left" |
| Curiosity | "The one thing … gets wrong" |
| Offer-led | "50% off your first month" |
| Objection-handling | "No credit card. Cancel anytime." |
| Founder / UGC voice | first-person, casual |

Only use social proof numbers, prices, discounts or claims the user supplied. Never invent stats or testimonials. Put a `[placeholder]` in instead so it's obvious what to fill in.

## 3. Respect platform limits

Read `references/platform-specs.md` for the full table. The short version:

- **Meta**: primary text ≤125 chars before "See more" (front-load the hook), headline ≤40, description ≤30
- **Google RSA**: headlines ≤30 (give 10–15), descriptions ≤90 (give 4), paths ≤15
- **LinkedIn**: intro ≤150, headline ≤70
- **TikTok**: ad text ≤100, no emojis-heavy clickbait

Count characters for every line that has a limit and show the count. If a line is over, rewrite it. Don't just flag it.

## 4. Output format

Use one block per variant, laid out so it can be copied straight into an ads manager:

```
### Variant A — Pain → relief
Primary text (118): …
Headline (34): …
Description (27): …
CTA: Shop Now
Why it might win: one line on the hypothesis being tested
```

For Google RSA, output one table of headlines (with char counts, flag 2–3 to pin) and one table of descriptions instead of variants.

End with:
- **Test plan**: which 2–3 variants to launch first and what each tests
- **Assumptions**: anything you guessed (audience, offer, voice)

## Quality bar

- Hook in the first ~5 words. On mobile feed that's all most people read.
- One idea per ad. Specific beats clever ("Ships in 24h" > "Lightning fast").
- Use "you" more than "we".
- CTA must match the goal: "Learn More" for awareness, "Shop Now" or "Get Offer" for sales.
- Avoid Meta-policy red flags: personal attributes ("Are you overweight?"), before/after claims, exaggerated income promises.
