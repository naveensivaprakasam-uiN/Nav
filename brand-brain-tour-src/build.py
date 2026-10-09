import json, base64, os, shutil, zipfile
from PIL import Image

B = os.path.dirname(os.path.abspath(__file__))
NAME = 'brand-brain-tour'
OUT = os.path.join(B, 'out', NAME)
H = json.load(open(os.path.join(B, 'hits.json')))

def hit(scr, name):
    return H[scr][name]

def ctr(r):
    return [round(r[0] + r[2] / 2, 2), round(r[1] + r[3] / 2, 2)]

def U(*rs):
    x = min(r[0] for r in rs); y = min(r[1] for r in rs)
    return [round(x, 2), round(y, 2), round(max(r[0] + r[2] for r in rs) - x, 2), round(max(r[1] + r[3] for r in rs) - y, 2)]

def tick_on(r, inset=2.2):
    """green tick near the top-right corner of a frame-% rect"""
    return [round(r[0] + r[2] - inset, 2), round(r[1] + inset * 16 / 9, 2)]

# (chapter, screen, title, on-screen text, area, click point, zoom cap, next hit, next label, narration)
SPEC = [
 ("Brand Brain", "home", "Welcome to Brand Brain",
  "Zocket keeps one shared memory of your brand: its products, customers and category. Open Brand Brain from the sidebar.",
  lambda s: U(hit(s,'prompt'), hit(s,'cards')), lambda s: ctr(hit(s,'prompt')), 1.3, 'nav-bb', 'Brand Brain',
  "Everything begins on this home screen. Brand Brain is where Zocket keeps one shared memory of your brand: your products, your customers, and your category. Let's open it from the sidebar."),
 ("Brand Brain", "bb_sources", "Everything that feeds your brand",
  "Ad accounts, social channels, CRM and your own documents, all in one place. Click Connect source to add another.",
  lambda s: U(hit(s,'connect'), [hit(s,'srclist')[0], hit(s,'connect')[1], hit(s,'srclist')[2], 30]), lambda s: ctr(hit(s,'connect')), 1.7, None, None,
  "This is the Sources page. Here you can see everything that feeds Brand Brain: your ad accounts, your social channels, your CRM, and the documents your team has shared. To add something new, we simply click Connect source."),
 ("Brand Brain", "bb_connect", "Add any source in a minute",
  "Pick a source type. Website URL crawls your site, and competitor sites, for brand and market signals.",
  lambda s: hit(s,'dialog'), lambda s: ctr(hit(s,'opt-website')), 1.6, None, None,
  "Connecting a new source takes about a minute. You simply choose the type of data. For example, with Website URL, Brand Brain reads your own website, and your competitors' websites, to pick up brand and market signals."),
 ("Brand Brain", "bb_graph", "One brain every agent shares",
  "Every source feeds a live knowledge graph. The creative, moderation, insight and ads agents all read from it.",
  lambda s: hit(s,'graph'), lambda s: ctr(hit(s,'graph')), 1.3, 'nav-ad', 'AI Designer',
  "All of these sources come together in one live knowledge graph. Reviews, social conversations, news and ad performance are all linked to each other. And every Zocket agent reads from this same graph, so they all understand your brand in the same way. Now, let's see how the creative agent uses it."),
 ("Creative AI", "ad_prompt", "Brief it in plain words",
  "Describe the ad you want. AI Designer pulls product shots, logos and brand rules from Brand Brain.",
  lambda s: hit(s,'promptbox'), lambda s: ctr(hit(s,'send')), 1.6, None, None,
  "This is AI Designer. Your team writes the brief in plain language, exactly the way they would brief an agency. When we send it, the agent goes to Brand Brain for the right product images, the logo, and your brand guidelines."),
 ("Creative AI", "ad_assets", "Your brand assets, ready",
  "It finds the right product images and logo marks, and asks you to confirm them before it designs.",
  lambda s: hit(s,'assets'), lambda s: ctr(hit(s,'submit')), 1.5, None, None,
  "Before it designs anything, the agent shows you the assets it has picked: the product shots and the logo marks. So your team always stays in control. Once these look right, we click Submit assets."),
 ("Creative AI", "ad_resize", "Every size in one click",
  "Resize a finished creative for Stories, Reels or any placement. Pick 9:16 and the layout reflows to fit.",
  lambda s: U(hit(s,'canvas'), hit(s,'resize-menu'), hit(s,'resize-btn')), lambda s: ctr(hit(s,'r916')), 1.6, None, None,
  "Every creative can be resized for any placement, in a single click. Here, we are choosing nine by sixteen, for Stories and Reels, and the layout adjusts on its own, without anyone redoing the design."),
 ("Creative AI", "ad_generated", "On-brand creatives, approved",
  "Three finished concepts, built from your brief and your brand assets, and approved. Next: keeping every conversation on brand.",
  lambda s: U(hit(s,'gen'), [hit(s,'gen')[0], 50, hit(s,'gen')[2], 13]), lambda s: ctr(hit(s,'cr2')), 1.5, 'rail-bm', 'Brand Moderator',
  "And here are the finished creatives, ready in minutes, and fully on brand. Your team reviews them, and once they are approved, they are ready to go live in your campaigns. Next, let's see how Brand Brain keeps your customer conversations on brand as well."),
 ("Brand Moderator", "bm_queue", "Every comment in one queue",
  "Comments, reviews and DMs from every platform land in one queue, flagged by topic and priority. Filter by platform any time.",
  lambda s: [hit(s,'queue')[0], 4.5, hit(s,'queue')[2], 93], lambda s: ctr(hit(s,'filters')), 1.15, None, None,
  "This is Brand Moderator. Every comment, every review, and every direct message, from every platform, comes into one single queue. The agent flags the complaints and marks their priority, so the important ones are always on top. And you can filter by platform, whenever you need to."),
 ("Brand Moderator", "bm_reply", "Replies in your brand voice",
  "The agent drafts a calm, on-brand reply to each complaint. Approve it and it posts under the customer's comment.",
  lambda s: hit(s,'draft'), lambda s: ctr(hit(s,'approve')), 1.6, None, None,
  "For each complaint, the agent drafts a reply in your brand's voice. It is calm, it takes ownership, and it moves the conversation to a private message. Your team reviews it, clicks Approve, and the reply is posted right under the customer's comment."),
 ("Brand Moderator", "bm_rule", "Automate the routine",
  "Turn a pattern into a rule. When a low rating lands on these channels, the agent replies in your brand voice and alerts the team.",
  lambda s: U(hit(s,'rule'), hit(s,'summary')), lambda s: ctr(hit(s,'auto')), 1.3, 'nav-ci', 'Consumer Insights',
  "For routine cases, you can automate the entire process with a rule. Here, whenever a low rating comes in on these channels, the agent replies automatically in your brand voice, and alerts your team. The rule is now active, and the job is done. Next, let's see what customers are saying about you across the market."),
 ("Consumer Insights", "ci_sov", "Know where you stand",
  "See your share of the category conversation, your rank against competitors and how it moved this period.",
  lambda s: hit(s,'sov'), lambda s: ctr(hit(s,'rank2')), 1.5, None, None,
  "This is Consumer Insights. It shows your share of the conversation in your category, where you rank against your competitors, and how that has moved this month. Here, your brand is at number two, and gaining ground."),
 ("Consumer Insights", "ci_sent", "Sentiment by channel",
  "How people feel about you on each platform, and which way it's moving. Next: turning this into paid media results.",
  lambda s: hit(s,'bychannel'), lambda s: ctr(hit(s,'bychannel')), 1.6, 'nav-pm', 'AI Paid Media',
  "You can also see how people feel about your brand on each platform, and whether that sentiment is improving or slipping. Now, let's connect all of this to your paid media."),
 ("AI Paid Media", "pm_conn_before", "Connect your ad platforms",
  "AI Paid Media reads your ad accounts, analytics and attribution tools. Meta Ads isn't connected yet, so connect it.",
  lambda s: hit(s,'meta'), lambda s: ctr(hit(s,'meta-btn')), 1.9, None, None,
  "AI Paid Media reads your ad accounts, your analytics, and your attribution tools, together. Google Ads is already connected. Meta Ads is not connected yet, so let's connect it."),
 ("AI Paid Media", "pm_conn_after", "Meta Ads connected",
  "Meta now syncs alongside Google Ads, GA4 and AppsFlyer. Open the Overview to see what it all adds up to.",
  lambda s: hit(s,'meta'), lambda s: ctr(hit(s,'meta')), 1.9, 'sub-pm-overview', 'Overview',
  "Meta Ads is now connected, and it syncs alongside Google Ads, Google Analytics, and AppsFlyer. Let's open the overview, to see the complete picture."),
 ("AI Paid Media", "pm_overview", "Performance, explained",
  "Headline metrics against the last period, with plain-language highlights on wins, risks and pacing.",
  lambda s: hit(s,'snapshot'), lambda s: ctr(hit(s,'snapshot')), 1.4, 'nav-rep', 'Reporting',
  "The overview gives you your headline numbers: spend, return on ad spend, leads, and cost per lead, compared with the previous period. Alongside, the agent explains the wins, the risks, and how you are pacing against your goals, in plain language."),
 ("AI Paid Media", "pm_dash", "Dashboards from a sentence",
  "Describe the dashboard you need in a sentence. It's built from your connected sources and stays live.",
  lambda s: hit(s,'newdash'), lambda s: ctr(hit(s,'create-dash')), 1.6, None, None,
  "Your team does not need to wait for an analyst to build a report. Just describe the dashboard you need, in one sentence, and it is created from your connected sources, and stays live."),
 ("AI Paid Media", "pm_signals", "Act on what matters",
  "Signals rank what changed by its impact on spend and results. Analyse any one to see the cause and the fix.",
  lambda s: hit(s,'sig1'), lambda s: ctr(hit(s,'analyse1')), 1.6, None, None,
  "And finally, Signals. The agent ranks what has changed, by its impact on your spend and your results. Click Analyse on any signal, to see the reason behind it, and the recommended fix."),
]

INTRO = ("Welcome. In the next few minutes, I'll walk you through Brand Brain by Zocket, and show you how one shared brain "
         "powers your creative, your customer conversations, your consumer insights, and your paid media.")

# Overlays drawn on top of the frame (positions in % of the frame, size s in % of frame width, d = delay in ms)
def overlays(scr):
    if scr == 'ad_generated':
        o = [{"k": "tick", "c": tick_on(hit(scr, f'cr{n}'), 0.25), "s": 2.6, "d": 700 + 350 * (n - 1)} for n in (1, 2, 3)]
        g = hit(scr, 'gen')
        o.append({"k": "pill", "c": [round(g[0] + g[2] / 2, 2), round(g[1] + g[3] + 4.2, 2)], "s": 1.25, "d": 1900, "t": "3 creatives approved"})
        return o
    if scr == 'bm_rule':
        a = hit(scr, 'auto'); sv = hit(scr, 'save')
        return [{"k": "tick", "c": [round(a[0] + a[2] - 1.6, 2), round(a[1] + a[3] / 2, 2)], "s": 2.2, "d": 800},
                {"k": "pill", "c": ctr(sv), "s": 1.2, "d": 1500, "t": "Rule active"}]
    return []

steps = []
for c, scr, t, d, fa, fp, z, nh, nl, v in SPEC:
    st = {"c": c, "img": scr, "t": t, "d": d, "a": fa(scr), "p": fp(scr), "z": z, "v": v}
    if nh:
        st["h"] = hit(scr, nh); st["hp"] = ctr(st["h"]); st["next"] = nl
    o = overlays(scr)
    if o: st["o"] = o
    steps.append(st)

start_at = ctr(H['home']['gap'])

shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT + '/img')
ids = list(dict.fromkeys(['home'] + [s['img'] for s in steps]))
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
AUD = os.path.join(B, 'audio')
clips = sorted(f for f in os.listdir(AUD) if f.endswith('.mp3')) if os.path.isdir(AUD) else []
have_audio = len(clips) == len(steps) + 1
voice = '"files"' if have_audio else '"browser"'
base = (src.replace('/*FONT*/', font).replace('/*VOICE*/', voice).replace('/*LOGO*/', logo)
           .replace('/*STEPS*/', json.dumps(steps, ensure_ascii=False))
           .replace('/*INTRO*/', json.dumps(INTRO))
           .replace('/*STARTAT*/', json.dumps(start_at)))
open(f'{OUT}/index.html', 'w').write(base.replace('/*IMG*/', json.dumps({k: f'img/{k}.webp' for k in ids})).replace('/*AUDIO*/', '{}'))
if have_audio:
    shutil.copytree(AUD, f'{OUT}/audio')
audio_data = {int(f[:2]): 'data:audio/mpeg;base64,' + base64.b64encode(open(os.path.join(AUD, f), 'rb').read()).decode() for f in clips} if have_audio else {}
shutil.copy(f'{B}/README.txt', f'{OUT}/README.txt')
data = {k: 'data:image/webp;base64,' + base64.b64encode(open(f'{OUT}/img/{k}.webp', 'rb').read()).decode() for k in ids}
open(os.path.join(B, 'out', 'brand-brain-tour-preview.html'), 'w').write(base.replace('/*IMG*/', json.dumps(data)).replace('/*AUDIO*/', json.dumps(audio_data)))
with zipfile.ZipFile(os.path.join(B, 'out', 'Brand-Brain-Interactive-Tour.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
    for r, _, fs in os.walk(OUT):
        for f in sorted(fs):
            p = os.path.join(r, f); z.write(p, os.path.relpath(p, os.path.join(B, 'out')))
json.dump({"intro": INTRO, "steps": steps}, open(os.path.join(B, 'steps.json'), 'w'), indent=1, ensure_ascii=False)
print('steps', len(steps), 'start', start_at, 'voice', voice, 'clips', len(clips))
