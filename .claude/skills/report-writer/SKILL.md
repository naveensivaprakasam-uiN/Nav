---
name: report-writer
description: Write clear, skimmable work reports and documents (weekly/monthly status updates, client performance reports, campaign recaps and post-mortems, executive summaries, meeting notes with action items, and one-pagers) from rough notes, data, or bullet dumps. Use this whenever the user asks to "write up", "summarize for my manager/client/team", "draft the weekly update", "turn these notes into…", "recap the campaign", or pastes messy notes and wants something shareable.
---

# Report Writer

Turn raw inputs (notes, numbers, Slack threads, transcripts) into a document the reader can understand in 30 seconds and act on in 2 minutes.

## 1. Identify reader and type

Infer these. Ask only if it genuinely changes the output.

| Type | Reader | Length | Leads with |
|---|---|---|---|
| Weekly / status update | manager, team | ≤1 page | Progress vs plan, blockers |
| Client performance report | client | 1–2 pages | Results vs goals, next steps |
| Campaign recap / post-mortem | team, leadership | 1–2 pages | Outcome, what worked, what we'll change |
| Executive summary | leadership | ≤½ page | Decision or ask |
| Meeting notes | attendees | short | Decisions + action items |
| One-pager / proposal | stakeholders | 1 page | Problem → proposal → ask |

## 2. Structure: bottom line up front

Every report opens with a **TL;DR** of 2–3 lines: the outcome, the key number, and the ask or next step. Then use the matching template from `references/templates.md`.

## 3. Writing rules

- **Numbers with context**: "CPA ₹380 (target ₹400, −12% WoW)", never a bare "CPA ₹380".
- **Status signals**: 🟢 on track / 🟡 at risk / 🔴 off track, and only for things that have a target.
- **Action items** always have an owner and a date: "- [ ] Refresh Meta creatives (Priya, Oct 15)".
- **Plain language** for clients and executives: no unexplained acronyms beyond CTR, CPA and ROAS, no internal jargon.
- **Bad news early and owned**: say what happened, its impact, and what you're doing about it. Don't bury it on page 2.
- Keep sentences short, and use bullets for lists of three or more. Bold only the key phrase in each bullet.
- Don't pad. If a section has nothing to say this week, write "No change" or drop it.
- Never invent numbers, names or dates. Use `[TBD]` where the input is missing and list the gaps at the end.

## 4. Data in reports

If the user gives raw data rather than finished numbers, compute them first (with the `data-insights` or `ad-performance` skill) and then write. If the report is for sharing, offer to make it a doc (the `docs` skill) or a deck.

## 5. Final check before handing over

- Could the reader stop after the TL;DR and still know the outcome and the ask?
- Does every metric have a comparison (target, prior period or benchmark)?
- Does every action item have an owner and a date?
- Is anything confidential, like client names or spend, going to the wrong audience?
