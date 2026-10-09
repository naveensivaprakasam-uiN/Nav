Zocket Brand Brain: interactive product tour
============================================

What's in this folder
  index.html   the tour (Figtree font, logo and all code embedded; no external requests)
  img/         19 screens, 2560x1440 WebP (quality 92)
  audio/       19 narration clips, MP3 (00 = intro, 01-18 = steps)
  README.txt   this file

Open index.html in a browser to try it. Keep img/ next to index.html.


1. Embed on the landing page (hero)
-----------------------------------
Upload the folder (for example to /tour/brand-brain/) and add:

  <div style="position:relative;width:100%;max-width:1280px;margin:0 auto;aspect-ratio:16/10.4">
    <iframe src="/tour/brand-brain/index.html"
            title="Brand Brain interactive product tour"
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
- Steps 8 and 11 end with green ticks: the three creatives are approved, then the auto-respond
  rule goes live.
- Transition steps (1, 4, 8, 11, 13, 15, 16) have two beats: first the screen zooms into what
  the step explains; after 2.6s it zooms out, outlines the next product in the sidebar in blue,
  moves the cursor there and shows a "Next: <product> →" chip.
- End screen: "That's Brand Brain" with a Replay button. No voiceover, no call to action.


3. Settings (top of the <script> in index.html)
-----------------------------------------------
  CONFIG.voice      "files"    recorded narration in audio/00.mp3 … audio/18.mp3 (default; included)
                    "browser"  device text-to-speech instead of the recordings
                    "off"      no sound, and the sound button is hidden
  (used only in "browser" mode)
  CONFIG.voiceLang  "en-IN"    Indian English first. Voice order: the device's first en-IN voice,
                               then Google UK English Female, Samantha, Google US English, any en-GB, any en-US.
  CONFIG.voiceRate  1.0        natural speed
  CONFIG.voicePitch 1.0        natural pitch (shifting rate or pitch makes device voices sound robotic)
  CONFIG.beatDelay  2600       ms before a transition step zooms out to the next product
  CONFIG.intro      the line spoken before step 1 in "browser" mode

The captions (t = title, d = on-screen text, v = the narration, which explains each screen
in more detail than the caption) are in the STEPS array just below.
Each step also carries p (click point), a (highlighted area), h (next product's sidebar item)
and z (zoom limit), all in % of the frame. These were measured from the rendered screens,
so don't edit them by hand unless a screen changes.


4. Voiceover
------------
The narration in audio/ is the approved Brand Brain voice, recorded from the demo and cleaned:
only the voice is kept (pauses are true silence, background noise removed under the speech),
loudness-normalised to -16 LUFS. About 4.5 minutes in total. Every visitor hears this same voice.
To use a different recording, replace the files keeping the same names (00 = intro before step 1,
01-18 = steps, nothing for the end screen).

Script, one line per file. Record it with a warm, clear Indian English female voice, at an
unhurried pace, as if walking a senior client through the product:

  00  Welcome. In the next few minutes, I'll walk you through Brand Brain by Zocket, and show you how one shared brain powers your creative, your customer conversations, your consumer insights, and your paid media.
  01  Everything begins on this home screen. Brand Brain is where Zocket keeps one shared memory of your brand: your products, your customers, and your category. Let's open it from the sidebar.
  02  This is the Sources page. Here you can see everything that feeds Brand Brain: your ad accounts, your social channels, your CRM, and the documents your team has shared. To add something new, we simply click Connect source.
  03  Connecting a new source takes about a minute. You simply choose the type of data. For example, with Website URL, Brand Brain reads your own website, and your competitors' websites, to pick up brand and market signals.
  04  All of these sources come together in one live knowledge graph. Reviews, social conversations, news and ad performance are all linked to each other. And every Zocket agent reads from this same graph, so they all understand your brand in the same way. Now, let's see how the creative agent uses it.
  05  This is AI Designer. Your team writes the brief in plain language, exactly the way they would brief an agency. When we send it, the agent goes to Brand Brain for the right product images, the logo, and your brand guidelines.
  06  Before it designs anything, the agent shows you the assets it has picked: the product shots and the logo marks. So your team always stays in control. Once these look right, we click Submit assets.
  07  Every creative can be resized for any placement, in a single click. Here, we are choosing nine by sixteen, for Stories and Reels, and the layout adjusts on its own, without anyone redoing the design.
  08  And here are the finished creatives, ready in minutes, and fully on brand. Your team reviews them, and once they are approved, they are ready to go live in your campaigns. Next, let's see how Brand Brain keeps your customer conversations on brand as well.
  09  This is Brand Moderator. Every comment, every review, and every direct message, from every platform, comes into one single queue. The agent flags the complaints and marks their priority, so the important ones are always on top. And you can filter by platform, whenever you need to.
  10  For each complaint, the agent drafts a reply in your brand's voice. It is calm, it takes ownership, and it moves the conversation to a private message. Your team reviews it, clicks Approve, and the reply is posted right under the customer's comment.
  11  For routine cases, you can automate the entire process with a rule. Here, whenever a low rating comes in on these channels, the agent replies automatically in your brand voice, and alerts your team. The rule is now active, and the job is done. Next, let's see what customers are saying about you across the market.
  12  This is Consumer Insights. It shows your share of the conversation in your category, where you rank against your competitors, and how that has moved this month. Here, your brand is at number two, and gaining ground.
  13  You can also see how people feel about your brand on each platform, and whether that sentiment is improving or slipping. Now, let's connect all of this to your paid media.
  14  AI Paid Media reads your ad accounts, your analytics, and your attribution tools, together. Google Ads is already connected. Meta Ads is not connected yet, so let's connect it.
  15  Meta Ads is now connected, and it syncs alongside Google Ads, Google Analytics, and AppsFlyer. Let's open the overview, to see the complete picture.
  16  The overview gives you your headline numbers: spend, return on ad spend, leads, and cost per lead, compared with the previous period. Alongside, the agent explains the wins, the risks, and how you are pacing against your goals, in plain language.
  17  Your team does not need to wait for an analyst to build a report. Just describe the dashboard you need, in one sentence, and it is created from your connected sources, and stays live.
  18  And finally, Signals. The agent ranks what has changed, by its impact on your spend and your results. Click Analyse on any signal, to see the reason behind it, and the recommended fix.

Clips run about 10-20 seconds. The tour doesn't auto-advance, so length isn't critical.
