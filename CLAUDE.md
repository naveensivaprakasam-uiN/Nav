# Nav

## Marketing skills — use them extensively

This repo ships 50 marketing skills in `.claude/skills/` (from
[coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills),
MIT, snapshot of commit `1efedbc`). Claude Code loads them automatically.

For **any** marketing, growth, sales, or go-to-market task, invoke the
matching skill(s) with the Skill tool before doing the work, and combine
several when a task spans areas (e.g. a launch → `launch` + `copywriting` +
`emails` + `social`). Do not answer from general knowledge when a skill covers
the topic.

Quick map:

| Area | Skills |
|---|---|
| Strategy & planning | `marketing-plan`, `marketing-ideas`, `marketing-loops`, `marketing-council`, `marketing-psychology`, `product-marketing`, `content-strategy`, `launch`, `offers`, `pricing` |
| Research | `customer-research`, `competitor-profiling`, `competitors`, `analytics`, `attribution` |
| Copy & content | `copywriting`, `copy-editing`, `emails`, `cold-email`, `sms`, `social`, `video`, `image`, `lead-magnets`, `free-tools` |
| Conversion (CRO) | `cro`, `ab-testing`, `signup`, `onboarding`, `paywalls`, `popups`, `churn-prevention` |
| SEO & discovery | `seo-audit`, `ai-seo`, `programmatic-seo`, `schema`, `site-architecture`, `aso`, `directory-submissions` |
| Paid & creative | `ads`, `ad-creative` |
| Distribution & partnerships | `community-marketing`, `influencer-marketing`, `co-marketing`, `referrals`, `public-relations`, `events` |
| Sales & RevOps | `prospecting`, `sales-enablement`, `revops` |

Shared product context: many skills read `.claude/product-marketing.md` (or
`.agents/product-marketing.md`) first. If it does not exist, create it with the
`product-marketing` skill so every other skill can reuse it.

To update the skills, re-copy `skills/` from the upstream repo into
`.claude/skills/`.
