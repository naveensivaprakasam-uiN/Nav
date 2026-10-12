# Nav — Claude skills

Custom Claude Code skills for ad/marketing work, reports and data analysis. They live in `.claude/skills/` and load automatically when Claude Code runs in this repo. Each one triggers on its own when a request matches, or you can call it by name (e.g. `/ad-copy`).

| Skill | Use it for |
|---|---|
| `ad-copy` | Platform-sized ad copy variants (Meta, Google RSA, LinkedIn, TikTok) with char counts and a test plan |
| `campaign-brief` | Turning a launch idea into a brief: objective, audience, channel/budget split, creative asks, KPIs, timeline |
| `ad-performance` | Analysing Ads Manager / Google Ads exports: CTR, CPC, CPM, CPA, ROAS, plus scale/cut verdicts and budget moves |
| `data-insights` | Any CSV, sheet or SQL result: profile → findings → recommendations, plus SQL writing |
| `report-writer` | Weekly updates, client reports, recaps, exec summaries, meeting notes |

## Using them everywhere (not just this repo)

Copy the folders into your personal skills directory:

```bash
cp -r .claude/skills/* ~/.claude/skills/
```

On claude.ai, zip a skill folder and upload it under **Settings → Capabilities → Skills**.

## ad-performance script

```bash
python3 .claude/skills/ad-performance/scripts/analyze_ads.py export.csv \
  --by "Ad set name" --target-roas 3 --min-spend 500
```

Stdlib-only Python 3. It auto-detects Meta, Google, LinkedIn and TikTok column names; use `--map spend="Your header"` if detection misses one.
