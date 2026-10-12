# Product Marketing Context

**Document version:** v1
**Last updated:** 2026-10-12

> Sources: zocket.com, zocket.com/brand-brain, and the Zocket internal wiki (v0.4, read 2026-10-12).
> Internal-only facts (pipeline names, product gaps, model stack) are marked **[internal]**. Never put them in public copy.

## Positioning hierarchy (read this first)

**Brand Brain is the hero. Everything else is an agent that runs on it.**

- **Master brand / category:** Zocket BrandOS, the AI-native brand operating system for enterprise brands.
- **Core product (the hero):** **Brand Brain**, one context layer that holds everything the brand knows (guidelines, voice, products, claims, disclaimers, competitors, customer and market signals) and that every team, agency and AI agent reads from.
- **Agents that run on Brand Brain:**
  - **Creative AI Agent** (in-app: *AI Designer*). On-brand image, video, UGC, localisation and marketplace creative.
  - **Paid Media AI Agent** (in-app: *AI Paid Media*; homepage: *Performance AI*). Ask your campaigns in plain English, get a ranked action plus the evidence.
  - **Consumer AI Agent** (in-app: *Consumer Insights* for listening + *Brand Moderator* for replies; homepage: *ORM* / *AI Consumer Research*). Share of category voice, sentiment, emotion, and governed replies.
  - Supporting surfaces: **Content AI**, **Competitor Intelligence**, **Reporting**, **Tasks**, **Custom agents**.
- **The architecture argument:** "Generic AI starts from zero. Brand Brain is the context layer underneath." Encode the brand once and every agent inherits it, so on-brand comes from the architecture, not from prompting.
- **The commercial argument:** buying any one agent still builds the Brand Brain, so the second agent is cheaper to land and better on day one.

**Naming is inconsistent across surfaces. Pick one set before writing anything public.** See *Open questions* at the bottom.

## Product Overview
**One-liner:** One Brand Brain. Every channel, on brand.
**Alt one-liner (homepage):** The AI-native brand operating system for enterprise brands.
**What it does:** Zocket builds a live knowledge graph of your brand and your whole category, called Brand Brain. It connects guidelines, assets, content, performance data, and customer and market signals from 90+ sources. AI agents for creative, paid media and consumer/reputation run on top of it. Every asset, reply and budget move is checked against your rules before it ships, with a full audit trail.
**Product category:** AI brand operating system / AI marketing workspace for enterprise brands. Buyers also file it under "AI creative tool", "social listening/ORM" and "marketing analytics". The job of positioning is to pull it out of those shelves.
**Product type:** Enterprise SaaS (app.zocket.com). Self-serve or managed service, often a hybrid.
**Business model:** Three components: **subscription + scraping + credits**.
- *Subscription*: platform access and seats. The licence buys the customised Brand Brain.
- *Scraping*: public data feeding Brand Brain and Consumer Insights, priced from the brand's real data volume (mentions, reviews, filings), the platforms, the cadence and the competitor set.
- *Credits*: metered AI usage. Only consumed credits are charged, and modules a customer never uses cost nothing.
- Creative pilots are scoped in **masters + adaptations** (e.g. 25 masters + 100 adaptations/month), and iterations don't count against the cap.
- Motion: NDA, then a paid POC with written KPIs (sell a quarter, not a month), then conversion. No public price list.

## Target Audience
**Target companies:** Mid-to-large and enterprise consumer brands, mostly India-headquartered and growing internationally (SE Asia, Middle East, US). The brands are big enough that creative volume, inbox volume and fragmented reporting are real operational problems, and often regulated enough that "just ship it fast" isn't allowed. Secondary segments: B2B/industrial brands with long CRM funnels, and agencies/OEM partners wanting multi-client or white-label use.
**Priority verticals and the agent that leads in each:**
| Vertical | Leading agent | Why |
|---|---|---|
| BFSI · Lending (IIFL, ICICI HF, Grihum, NeoGrowth) | Creative AI + Brand Brain | Branch- and language-scale creative under locked RBI/SEBI disclaimers |
| BFSI · Broking & Neobank (5paisa, Kotak Neo, Revolut India, Paytm) | Creative (content/SEO) · Consumer AI | Content volume for SEO; ORM and the weekly report |
| Retail & Durables (Bata, Lenovo, Croma, Duroflex, Whirlpool) | Consumer AI (Brand Moderator) | Inbox on fire; reviews across marketplaces |
| FMCG & D2C (Dabur, CavinKare, Mamaearth) | Paid Media AI | Portfolio scale, per-SKU claims governance |
| B2B & Industrial (Numeric UPS, Tata Motors CV, Saint-Gobain) | Paid Media AI + Reporting | Funnel leakage across systems, CRM-joined reporting |
| Consumer Internet & Media (Bharat Matrimony, Cure.fit, Zee) | Paid Media AI | Buying back analyst time |
| Agencies & OEM (Pivotroots, Amber, Langoor) | Creative AI or the whole platform | Multi-client, maybe white-label |
| Emerging: healthcare, travel, logistics | Varies | Narayana Health, Sterling Holiday Resorts, Blue Dart |

**Decision-makers:** CMO / VP Brand, Brand Manager, Head of Performance/Digital Marketing, Creative Lead, Social/Community lead, Head of CX (when ORM sits in customer service), Compliance head (BFSI), Procurement and InfoSec.
**Primary use case:** Replace a fragmented marketing stack (agencies, point tools, listening tool, native ad managers, a weekly hand-built deck) with one system, where every output is grounded in the same brand truth and governed before it ships.
**Jobs to be done:**
- "Give me forty on-brand size, language and placement variants of this hero asset by Friday, without breaking a disclaimer."
- "Tell me where my ad money is leaking and what to do about it, without me pulling five dashboards."
- "Tell me how the brand is doing against the category, and answer every comment safely within SLA."
- "Stop someone rebuilding the same report every Monday."
**Use cases:**
- Festive or seasonal campaigns across regions and languages (Diwali, Akshaya Tritiya)
- Branch/dealer-level localisation from HQ-approved masters
- Marketplace content (A+, Amazon Brand Store) and print/OOH
- Product photoshoots without a physical shoot
- Moderating comments, DMs and reviews, with ≤2★ reviews escalated to CRM
- Share of category voice and competitor benchmarks for board packs
- Paid media diagnosis: creative fatigue, audience saturation, search-term waste, offline conversions on 7–45 day cycles
- Prompt-built dashboards and scheduled exec reports

## Personas
| Persona | Cares about | Challenge | Value we promise |
|---------|-------------|-----------|------------------|
| CMO / VP Brand (decision maker) | Brand consistency across markets, speed, consolidating spend, a defensible "how is the brand doing" number | Silos ship apart; waste is found at the QBR; agencies and tools don't share a brain | One system, one brand truth, governed autonomy they can sign off on; share of category voice they can take to the board |
| Brand Manager (champion) | Output that is on-brand without re-briefing; visibility into what the brand "knows" | Re-briefs, review rounds, off-brand drafts; brand rules are tribal knowledge | Brand Brain: encode it once, every agent inherits it; Skills make category rules durable |
| Performance Marketer (user) | Time back, finding waste early, hitting CPA/ROAS goals | Half the week is spent pulling reports from 5+ dashboards; data is stale when it arrives | Plain-English questions, ranked actions with evidence, goals that say "breached" and become tasks |
| Creative Lead (user) | Volume without losing quality; approvals that flow | Can't hire to 400 assets a month; agencies price per adaptation | 25 specialist creative agents, AI judge/Compliance Checker, gate-by-gate approvals |
| Social / CX lead (user) | 30-min response SLA, never saying the wrong thing | Fire-hose inbox across platforms, WhatsApp-thread escalations, no audit trail | AI-drafted, human-approved replies (nothing auto-posts), Rules Engine, Action History |
| Compliance / Legal (technical influencer, BFSI) | Disclaimers, prohibited claims, audit trail | Fear of AI saying something wrong under their logo | Rules enforced before output; approval flows; exportable audit trail |
| IT / InfoSec / Procurement (technical influencer, financial buyer) | Security, data location, predictable cost | Vendor risk; unpredictable credit bills | SOC 2 Type II, ISO 27001, GDPR, SSO/SAML, RBAC; three-part pricing in writing |

## Problems & Pain Points
**Core problem:** Fragmentation. Agencies, in-house teams, sub-brands and a dozen point tools all ship in silos. Those look like four or five problems (slow creative, unanswered inbox, blind paid spend, undiagnosed brand, hand-built reports), but they are one problem: **there's no shared brain.** Every tool starts from zero and every output drifts.
**Why alternatives fall short:**
- Generic AI tools (Jasper, Copy.ai, Pencil, Pebblely, Higgsfield) start from zero context. "Staying on-brand" comes down to prompt engineering and hope.
- Agencies don't scale to 10x content across surfaces and languages, and they price per adaptation.
- Listening tools report your own mention count, not your rank against the category, and they send a summary once a month.
- Native ad managers and BI tools show charts but not decisions, and the data is days old.
- Point tools don't talk to each other, so creative isn't informed by performance or consumer signal.
**What it costs them:** 6 weeks to ship one campaign; 5+ dashboards to find what's working ("by then the budget's gone"); 90 days between research reports; manual reply hours; waste discovered only at the QBR; a person rebuilding the same deck every week.
**Emotional tension:** Fear of AI going off-brand or non-compliant in public. Distrust after trying generic AI tools. Anxiety about unpredictable credit bills. Embarrassment when the CMO asks "how is the brand doing?" and nobody can answer against the category.

## Competitive Landscape
**Direct (AI creative / AI marketing platforms):** Jasper, Copy.ai, Pencil, Pebblely, Higgsfield, Freepik AI. They fall short because they generate without brand context, so output drifts and nothing is governed or audited.
**Secondary (specialist point tools):** Listening/ORM such as Brandwatch, Sprout Social and Connect Insights; attribution tools such as Triple Whale; BI such as Tableau, BigQuery and in-house warehouses. They fall short because each owns one slice and none shares a brand memory. (We coexist with dedicated attribution and warehouses rather than replace them.)
**Indirect:** Creative and media agencies, in-house design hires, horizontal enterprise AI (Microsoft Copilot), and primary research firms (Kantar, Ipsos). They fall short because agencies don't scale and price per adaptation, and Copilot is horizontal productivity, not brand operations. We use secondary data, not recruited panels, so we complement Kantar rather than replace it.

## Differentiation
**Key differentiators:**
- **Brand Brain as a visible, auditable knowledge graph.** It's a screen you can point at: live signal counter, sources with freshness, the graph by layer, and Signals you can read row by row. It is category-wide, because every competitor is built from the same sources, which makes share of voice computable rather than estimated.
- **Governed autonomy.** Approvals and gates, a rules engine, and an exportable audit trail (SIEM / CSV / API). Nothing ships past a gate you didn't open. Brand Moderator never auto-posts.
- **Loop engineering.** Every agent run reads the graph, plans, acts, clears gates, then writes the outcome back, so every run starts smarter than the last.
- **Specialists, not one generator.** 25 creative agents; a video pipeline that directs (concept → storyboard → preview → export) with human gates; an AI judge QAs every asset.
- **End-to-end loop.** The same platform makes the creative, measures it in paid media, and moderates the comments it gets.
- **Skills.** Per-brand, per-agent instructions inside Brand Brain turn category rules into a durable configured asset.
- **Model-agnostic routing.** The Brand Brain is the moat, not the model. **[internal: do not name models in writing]**
**How we do it differently:** Brain first, agents second. We build the brand and category graph (48–72 hours once inputs arrive), then agents run on it.
**Why that's better:** On-brand by construction rather than by prompting. The second agent lands on a brain that's already built. Every action traces to a rule, a playbook and an owner.
**Why customers choose us:** One system instead of five fires, proven references in their own category, a paid POC on real data, and enterprise-grade governance.

## Objections
| Objection | Response |
|-----------|----------|
| "We don't trust AI with our brand." | Brand Brain plus the Compliance Checker plus approval gates. Show the Sources and Signals screens. Brand Moderator never auto-posts. |
| "We tried Jasper/Pencil and it didn't work." | Those start from zero context. We build the graph of your brand and category first; on-brand is the architecture. |
| "Our agency already does this." | We replace the manual execution layer (resize, localisation, the 3am comment, the Monday report), not the strategy or the agency relationship. |
| "Pricing is inconsistent / credits are unpredictable." | One model, three parts: subscription, scraping, credits. Firm written quote from real volumes. Iterations don't count against the creative cap. |
| "What's the ROI?" | Bharat Matrimony saves 3–4 hours a day; root-cause diagnosis dropped from 15–20 days to under one; about 80% less reporting time. Then make them price their status quo. |
| "We're regulated (BFSI)." | Disclaimers and prohibited claims enforced, approval flows, provenance on failures, audit trail. We shorten the compliance loop, we don't replace the reviewer. |
| "Half your modules don't apply to us (B2B)." | Subtract honestly. Lead with Paid Media + Reporting and the CRM-joined funnel. |

**Anti-persona:** Small brands with low creative and inbox volume; buyers who need primary research panels; buyers who need fully autonomous ad execution today (paid media is insight-first, with a human approving the push); quick-commerce-first brands needing native Blinkit/Zepto APIs; anyone wanting a one-month pilot judged on output.

## Switching Dynamics
**Push:** 6-week campaigns, agency per-adaptation costs, five dashboards, unanswered inboxes, waste found at the QBR, decks rebuilt by hand, generic AI that drifted off-brand.
**Pull:** One brand truth under every agent; 48 hours from brief to live; share of category voice they can defend; governed autonomy with an audit trail; time back.
**Habit:** Agency retainers and relationships, existing listening and BI tools, monthly decks, "the way we brief".
**Anxiety:** AI saying something wrong in public; non-compliance; IP and copyright exposure; pack shots being redrawn; data location; unpredictable bills; implementation effort (answer: OAuth plug-and-play, no engineering on their side).

## Customer Language
**How they describe the problem:**
- "The resize-and-adapt work is the manual part of my business." (Amber, agency)
- "Consolidating multiple marketing tools into one unified, AI-driven system." (the line that landed at Kotak)
- "AI OS for Marketing." (PN Rao deck title)
- "We've bought analytics tools before. Nobody looks at them."
- "We want smarter and more relevant, not just cheaper and faster."
- "How do you keep the AI on-brand?" (the first hard question on every call)
**How they describe us:** "BrandOS platform setup" (Numeric UPS).
**Words to use:** Brand Brain, operating system, one brand truth, context layer, on-brand by construction, governed, gates, approvals, audit trail, share of category voice, category rank, ranked action with the evidence, masters and adaptations, subscription/scraping/credits, "AI agents with human approval where it matters", "the manual execution layer".
**Words to avoid:** "replace your agency/team", "fully autonomous", "it takes the action for you" (paid media), "best-in-class" / "industry-leading" / "cutting-edge", "you only pay for what works", "your data stays in India", "never touches your asset", "AI Researcher" / "Storyboard Creator" / "Feed" (removed surfaces), any model name in writing, and signal counts borrowed from another account.
**Glossary:**
| Term | Meaning |
|------|---------|
| BrandOS | The master product/category name: the AI brand operating system |
| Brand Brain | The live knowledge graph of the brand and its category that every agent reads before acting |
| Layers | Groupings in the graph (Ratings & Reviews, Owned Social, Paid Ads, Filings…). Agent-built; more sources means more layers |
| Signals | Individual extracted facts in the graph, tagged by layer and source |
| Skills | Per-brand, per-agent instructions stored in Brand Brain |
| Gates | Human approval checkpoints (concept → character → image → voice) |
| Masters / adaptations | The unit creative work is scoped in |
| Share of category voice | Your share of conversation and rank against every tracked competitor, with auditable sources |

## Brand Voice
**Tone:** Confident, precise, enterprise-calm. Numbers over adjectives.
**Style:** Direct, short declaratives, before/after contrasts ("6 weeks → 48 hrs"). Show the mechanism (read → plan → act → gate → write back). Honest about limits.
**Personality:** Intelligent, governed, fast, accountable, grounded.

## Proof Points
**Public metrics (website):** 48 hrs brief-to-live (vs 6 weeks); 3.5x ROAS (up from 2.1x); 98% brand-voice match; 41% lower production cost; 10-second response across 2.18M daily signals; 78% autonomous ORM with 11s average response; 4-day campaign production; 90+ sources; "Trusted by 200+ enterprise brands across 25+ countries".
**Sales metrics:** about $120M monthly media spend managed across 250+ brand accounts; Bharat Matrimony (₹2–2.5 crore/month spend, 3–4 hours a day saved, diagnosis cut from 15–20 days to under one); about 80% less time on data compilation and reporting.
**Customers (per wiki):** Bata, Bharat Matrimony, Cloudnine, Dabur, IIFL, IndiGo, Lenovo India, Montra Electric, Numeric UPS, Yokohama India. **[internal: confirm logo and case-study permission before public use]**
**Named public references:** Bharat Matrimony (paid media), Bata (ORM in production), IndiGo (production case study), Chola (BFSI).
**Trust:** SOC 2 Type II, ISO 27001, GDPR-ready, SSO/SAML (Entra, Google Workspace), RBAC per sub-brand, exportable audit trail.
**Value themes:**
| Theme | Proof |
|-------|-------|
| Speed | 48 hrs brief-to-live; statics in minutes; bulk adaptation inside a day |
| On-brand at scale | 98% voice match; 8-dimension compliance scoring; AI judge |
| Money | 3.5x ROAS; 41% lower production cost; waste found in-quarter |
| Time back | 3–4 hrs/day (Bharat Matrimony); about 80% less reporting time |
| Governance | Gates, rules engine, audit trail; zero auto-posted replies |

## Goals
**Business goal:** Win enterprise brands onto BrandOS, landing with one agent (Brand Brain gets built either way) and expanding to more agents.
**Conversion action:** Book a demo, a 30-minute call where they "bring your brand guidelines and leave with your first on-brand ads, generated live". Secondary: the interactive tour.
**Current metrics:** 11 customers, 81 active prospects and 31 exploring (wiki pipeline, Oct 2026). **[internal]**

## Open questions (resolve before external copy)
1. **Agent names.** The Brand Brain page says Creative AI Agent / Paid Media AI Agent / Consumer Expert AI Agent (and later "Consumer AI Agent"). The homepage says AI Designer / AI Consumer Research / AI Paid Media plus six "modules" (Brand Brain, Creative AI, Content AI, Performance AI, ORM, Competitor Intelligence). The footer says Brand IQ / Creative Designer / Consumer Research / Paid Media. The app says AI Designer / Brand Moderator / Consumer Insights / AI Paid Media. Which set is canonical?
2. **Brand Brain as hero vs. BrandOS as master brand.** The new direction is "Brand Brain is main". The wiki currently says Brand Brain is "never sold alone" and BrandOS is the category name. Is the hierarchy BrandOS > Brand Brain > agents, or does Brand Brain replace BrandOS publicly?
3. **Conflicting numbers.** 44 vs 90+ sources; 200+ brands vs 250+ accounts; 96% vs 98% voice match; 1.48M signals vs 2.18M daily signals. Which are approved?

## Changelog
*Newest first. One line per revision: what changed and why.*
- v1 (2026-10-12) — Initial context, drafted from zocket.com, the Brand Brain page and the internal wiki; Brand Brain positioned as the core with agents running on it.
