import json, base64, os, shutil, sys
from PIL import Image

B = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(B, 'out', 'brandos-tour')
H = json.load(open(os.path.join(B, 'hits.json')))

def hit(scr, name):
    return H[scr][name]

def ctr(r):
    return [round(r[0] + r[2] / 2, 2), round(r[1] + r[3] / 2, 2)]

def U(*rs):
    x = min(r[0] for r in rs); y = min(r[1] for r in rs)
    return [round(x, 2), round(y, 2), round(max(r[0] + r[2] for r in rs) - x, 2), round(max(r[1] + r[3] for r in rs) - y, 2)]

# (chapter, screen, title, text, area, click-point, zoom cap, next-hit, next-label)
SPEC = [
 ("Brand Brain", "home", "Welcome to Brand Brain",
  "Brand OS starts with one shared memory of your brand. Open Brand Brain from the sidebar.",
  lambda s: U(hit(s,'prompt'), hit(s,'cards')), lambda s: ctr(hit(s,'prompt')), 1.3, 'nav-bb', 'Brand Brain'),
 ("Brand Brain", "bb_sources", "Everything that feeds your brand",
  "Ad accounts, social channels, CRM and your own documents, all in one place. Click Connect source to add another.",
  lambda s: U(hit(s,'connect'), [hit(s,'srclist')[0], hit(s,'connect')[1], hit(s,'srclist')[2], 30]), lambda s: ctr(hit(s,'connect')), 1.7, None, None),
 ("Brand Brain", "bb_connect", "Add any source in a minute",
  "Pick a source type. Website URL crawls your site, and competitor sites, for brand and market signals.",
  lambda s: hit(s,'dialog'), lambda s: ctr(hit(s,'opt-website')), 1.6, None, None),
 ("Brand Brain", "bb_graph", "One brain every agent shares",
  "Every source feeds a live knowledge graph. The creative, moderation, insight and ads agents all read from it.",
  lambda s: hit(s,'graph'), lambda s: ctr(hit(s,'graph')), 1.3, 'nav-ad', 'AI Designer'),
 ("Creative AI", "ad_prompt", "Brief it in plain words",
  "Describe the ad you want. AI Designer pulls product shots, logos and brand rules from Brand Brain.",
  lambda s: hit(s,'promptbox'), lambda s: ctr(hit(s,'send')), 1.6, None, None),
 ("Creative AI", "ad_assets", "Your brand assets, ready",
  "It finds the right product images and logo marks, and asks you to confirm them before it designs.",
  lambda s: hit(s,'assets'), lambda s: ctr(hit(s,'submit')), 1.5, None, None),
 ("Creative AI", "ad_resize", "Every size in one click",
  "Resize a finished creative for Stories, Reels or any placement. Pick 9:16 and the layout reflows to fit.",
  lambda s: U(hit(s,'canvas'), hit(s,'resize-menu'), hit(s,'resize-btn')), lambda s: ctr(hit(s,'r916')), 1.6, None, None),
 ("Creative AI", "ad_generated", "On-brand creatives in minutes",
  "Three finished concepts, each built from your brief and your brand assets. Next: keeping every conversation on brand.",
  lambda s: hit(s,'gen'), lambda s: ctr(hit(s,'gen')), 1.5, 'rail-bm', 'Brand Moderator'),
 ("Brand Moderator", "bm_queue", "Every comment in one queue",
  "Comments, reviews and DMs from every platform land in one queue, flagged by topic and priority. Filter by platform in a click.",
  lambda s: U(hit(s,'filters'), hit(s,'filtermenu')), lambda s: ctr(hit(s,'opt-instagram')), 1.7, None, None),
 ("Brand Moderator", "bm_reply", "Replies in your brand voice",
  "The agent drafts a calm, on-brand reply to each complaint. Approve it and it posts under the customer's comment.",
  lambda s: hit(s,'draft'), lambda s: ctr(hit(s,'approve')), 1.6, None, None),
 ("Brand Moderator", "bm_rule", "Automate the routine",
  "Turn a pattern into a rule. When a low rating lands on these channels, reply in your brand voice and alert the team.",
  lambda s: hit(s,'rule'), lambda s: ctr(hit(s,'rule')), 1.4, 'nav-ci', 'Consumer Insights'),
 ("Consumer Insights", "ci_sov", "Know where you stand",
  "See your share of the category conversation, your rank against competitors and how it moved this period.",
  lambda s: hit(s,'sov'), lambda s: ctr(hit(s,'rank2')), 1.5, None, None),
 ("Consumer Insights", "ci_sent", "Sentiment by channel",
  "How people feel about you on each platform, and which way it's moving. Next: turning this into paid media results.",
  lambda s: hit(s,'bychannel'), lambda s: ctr(hit(s,'bychannel')), 1.6, 'nav-pm', 'AI Paid Media'),
 ("AI Paid Media", "pm_conn_before", "Connect your ad platforms",
  "AI Paid Media reads your ad accounts, analytics and attribution tools. Meta Ads isn't connected yet, so connect it.",
  lambda s: hit(s,'meta'), lambda s: ctr(hit(s,'meta-btn')), 1.9, None, None),
 ("AI Paid Media", "pm_conn_after", "Meta Ads connected",
  "Meta now syncs alongside Google Ads, GA4 and AppsFlyer. Open the Overview to see what it all adds up to.",
  lambda s: hit(s,'meta'), lambda s: ctr(hit(s,'meta')), 1.9, 'sub-pm-overview', 'Overview'),
 ("AI Paid Media", "pm_overview", "Performance, explained",
  "Headline metrics against the last period, with plain-language highlights on wins, risks and pacing.",
  lambda s: hit(s,'snapshot'), lambda s: ctr(hit(s,'snapshot')), 1.4, 'nav-rep', 'Reporting'),
 ("AI Paid Media", "pm_dash", "Dashboards from a sentence",
  "Describe the dashboard you need in a sentence. It's built from your connected sources and stays live.",
  lambda s: hit(s,'newdash'), lambda s: ctr(hit(s,'create-dash')), 1.6, None, None),
 ("AI Paid Media", "pm_signals", "Act on what matters",
  "Signals rank what changed by its impact on spend and results. Analyse any one to see the cause and the fix.",
  lambda s: hit(s,'sig1'), lambda s: ctr(hit(s,'analyse1')), 1.6, None, None),
]

steps = []
for c, scr, t, d, fa, fp, z, nh, nl in SPEC:
    st = {"c": c, "img": scr, "t": t, "d": d, "a": fa(scr), "p": fp(scr), "z": z}
    if nh:
        st["h"] = hit(scr, nh); st["hp"] = ctr(st["h"]); st["next"] = nl
        st["p"] = fp(scr)
    st["v"] = t + ". " + d
    steps.append(st)

gap = H['home']['gap']; start_at = ctr(gap)

shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT + '/img')
ids = ['home'] + [s['img'] for s in steps]
ids = list(dict.fromkeys(ids))
for k in ids:
    im = Image.open(f'{B}/png/{k}.png').convert('RGB')
    assert im.size == (2560, 1440), im.size
    im.save(f'{OUT}/img/{k}.webp', 'WEBP', quality=92, method=6)

src = open(f'{B}/index.src.html').read()
font = base64.b64encode(open(f'{B}/assets/figtree.woff2', 'rb').read()).decode()
logo = ('<svg viewBox="0 0 44 44" width="100%" height="100%"><defs><linearGradient id="lg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4f8cff"/><stop offset="1" stop-color="#1d4ed8"/></linearGradient></defs>'
        '<circle cx="22" cy="22" r="22" fill="url(#lg)"/><g transform="translate(6 6) scale(1.333)">'
        '<path d="M13.6 5.3c2.4-1.6 4.6-2 6.4-1.8.2 1.8-.2 4-1.8 6.4l-4.6 4.6-4.6-4.6z" fill="#fff"/><path d="M9.6 9.3l-3.2-.2-2.2 2.4 3.6.8z M14.7 14.4l.2 3.2-2.4 2.2-.8-3.6z" fill="#fff"/>'
        '<path d="M7.3 15.2c-1.6.3-2.7 1.6-3 3.8 2.2-.3 3.5-1.4 3.8-3z" fill="#fff"/></g></svg>')
base = (src.replace('/*FONT*/', font).replace('/*LOGO*/', logo)
           .replace('/*STEPS*/', json.dumps(steps, ensure_ascii=False))
           .replace('/*STARTAT*/', json.dumps(start_at)))
open(f'{OUT}/index.html', 'w').write(base.replace('/*IMG*/', json.dumps({k: f'img/{k}.webp' for k in ids})))
data = {k: 'data:image/webp;base64,' + base64.b64encode(open(f'{OUT}/img/{k}.webp', 'rb').read()).decode() for k in ids}
open(os.path.join(B, 'out', 'brandos-tour-preview.html'), 'w').write(base.replace('/*IMG*/', json.dumps(data)))
json.dump(steps, open(os.path.join(B, 'steps.json'), 'w'), indent=1)
print('steps', len(steps), 'start', start_at)
