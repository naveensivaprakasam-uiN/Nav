Zocket Brand OS: interactive product tour
=========================================

What's in this folder
  index.html   the tour (Figtree font, logo and all code embedded; no external requests)
  img/         19 screens, 2560x1440 WebP (quality 92)
  README.txt   this file

Open index.html in a browser to try it. Keep img/ next to index.html.


1. Embed on the landing page (hero)
-----------------------------------
Upload the folder (for example to /tour/brand-os/) and add:

  <div style="position:relative;width:100%;max-width:1280px;margin:0 auto;aspect-ratio:16/10.4">
    <iframe src="/tour/brand-os/index.html"
            title="Brand OS interactive product tour"
            style="position:absolute;inset:0;width:100%;height:100%;border:0"
            allow="autoplay" loading="lazy"></iframe>
  </div>

The tour sizes itself to the iframe: the 16:9 screen, the product tabs above it and the
Back/Next bar below it always fit. Below 720px of stage width the caption moves under the
screen and the start/end screens simplify, so the same embed works on phones. For a phone,
a taller box reads better, e.g. aspect-ratio: 4/5 under a 720px media query.


2. How it behaves
-----------------
- Start screen: the home screen with a "Take an interactive Tour" button. Nothing plays,
  and no sound starts, until it's clicked.
- 18 steps in 5 chapters: Brand Brain (1-4), Creative AI (5-8), Brand Moderator (9-11),
  Consumer Insights (12-13), AI Paid Media (14-18).
- Click the pulsing ring (or Next, or the right-arrow key) to go on. Back / left-arrow goes back.
  The product tabs at the top jump to the start of each chapter.
- Transition steps (1, 4, 8, 11, 13, 15, 16) have two beats: first the screen zooms into what
  the step explains; after 2.6s it zooms out, outlines the next product in the sidebar in blue,
  moves the cursor there and shows a "Next: <product> →" chip.
- End screen: "That's Brand OS" with a Replay button. No voiceover, no call to action.


3. Settings (top of the <script> in index.html)
-----------------------------------------------
  CONFIG.voice      "browser"  device text-to-speech (placeholder, default)
                    "files"    recorded voiceover from audio/ (see 4)
                    "off"      no sound
  CONFIG.voiceLang  "en-US"
  CONFIG.voiceRate  1.0
  CONFIG.beatDelay  2600       ms before a transition step zooms out to the next product
  CONFIG.intro      the line spoken before step 1 in "browser" mode

The captions (t = title, d = text, v = what the voice says) are in the STEPS array just below.
Each step also carries p (click point), a (highlighted area), h (next product's sidebar item)
and z (zoom limit), all in % of the frame. These were measured from the rendered screens,
so don't edit them by hand unless a screen changes.


4. Voiceover files
------------------
Set CONFIG.voice = "files" and add a folder audio/ next to index.html:

  audio/00.mp3   intro (plays after the Tour button, before step 1)
  audio/01.mp3   step 1
  ...
  audio/18.mp3   step 18
  (nothing for the end screen)

Script, one line per file:
  00  Here's a quick tour of Brand OS: five AI products that share one brain about your brand.
  01  Welcome to Brand Brain. Brand OS starts with one shared memory of your brand. Open Brand Brain from the sidebar.
  02  Everything that feeds your brand. Ad accounts, social channels, CRM and your own documents, all in one place. Click Connect source to add another.
  03  Add any source in a minute. Pick a source type. Website URL crawls your site, and competitor sites, for brand and market signals.
  04  One brain every agent shares. Every source feeds a live knowledge graph. The creative, moderation, insight and ads agents all read from it.
  05  Brief it in plain words. Describe the ad you want. AI Designer pulls product shots, logos and brand rules from Brand Brain.
  06  Your brand assets, ready. It finds the right product images and logo marks, and asks you to confirm them before it designs.
  07  Every size in one click. Resize a finished creative for Stories, Reels or any placement. Pick 9:16 and the layout reflows to fit.
  08  On-brand creatives in minutes. Three finished concepts, each built from your brief and your brand assets. Next: keeping every conversation on brand.
  09  Every comment in one queue. Comments, reviews and DMs from every platform land in one queue, flagged by topic and priority. Filter by platform in a click.
  10  Replies in your brand voice. The agent drafts a calm, on-brand reply to each complaint. Approve it and it posts under the customer's comment.
  11  Automate the routine. Turn a pattern into a rule. When a low rating lands on these channels, reply in your brand voice and alert the team.
  12  Know where you stand. See your share of the category conversation, your rank against competitors and how it moved this period.
  13  Sentiment by channel. How people feel about you on each platform, and which way it's moving. Next: turning this into paid media results.
  14  Connect your ad platforms. AI Paid Media reads your ad accounts, analytics and attribution tools. Meta Ads isn't connected yet, so connect it.
  15  Meta Ads connected. Meta now syncs alongside Google Ads, GA4 and AppsFlyer. Open the Overview to see what it all adds up to.
  16  Performance, explained. Headline metrics against the last period, with plain-language highlights on wins, risks and pacing.
  17  Dashboards from a sentence. Describe the dashboard you need in a sentence. It's built from your connected sources and stays live.
  18  Act on what matters. Signals rank what changed by its impact on spend and results. Analyse any one to see the cause and the fix.

Keep each clip roughly 5-8 seconds. The tour doesn't auto-advance, so length isn't critical.
