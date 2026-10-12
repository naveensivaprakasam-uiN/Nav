"""Merge agent research, dedupe, exclude, qualify, score. Writes merged.json + review files."""
import sys, json, glob, re, collections
sys.path.insert(0, '.')
from load import nm, dom, li
from groups_excluded import GROUPS
from rapidfuzz import fuzz

USD_RATE = 85.0
GENERIC_DOMAINS = {'', 'linkedin.com', 'facebook.com', 'not found', 'google.com', 'wikipedia.org'}

seen = json.load(open('seen_index.json'))
HARD = {'CLIENT_META', 'PIPELINE', 'ACCOUNT_LIST', 'ACTIVE_CONN', 'WIKI_CUSTOMER', 'WIKI_ACTIVE_PROSPECT', 'WIKI_EXPLORING'}
by_dom = collections.defaultdict(list); by_li = collections.defaultdict(list); by_nm = collections.defaultdict(list)
for s in seen:
    if s['domain'] not in GENERIC_DOMAINS: by_dom[s['domain']].append(s)
    if s['li']: by_li[s['li']].append(s)
    if s['norm']: by_nm[s['norm']].append(s)
GENERIC = set('industries industry holidays hospitals hospital medicare healthcare foods food products product enterprises enterprise retail ventures technologies technology solutions services service international global holdings holding consumer care lifestyle lifestyles brands brand estates estate realty developers developer properties property infra infrastructure housing finance financial motors motor auto automobiles hotels hotel resorts resort labs laboratories pharma pharmaceuticals and of ltd limited pvt private india co company corporation corp group the stores store mart jewellers jewellery jewels diamonds gold silks textiles fashions fashion apparels apparel works mills agro dairy beverages spirits breweries cements cement paints ceramics tiles electricals electric electronics appliances projects constructions construction builders buildcon buildtech homes realtors shelters promoters spaces land lands'.split())
def core(n):
    t=[w for w in n.split() if w not in GENERIC]
    return ' '.join(t)
seen_norms = [(s['norm'], s) for s in seen if len(s['norm']) >= 4]
by_core = collections.defaultdict(list)
for s in seen:
    c = core(s['norm'])
    if len(c) >= 5: by_core[c].append(s)
GROUP_RX = [(g, t, re.compile(r'(?i)(?<![a-z0-9])(?:' + p + r')(?![a-z0-9])')) for g, t, p in GROUPS if p != '$^']

def regdom(d):
    parts = d.split('.')
    if len(parts) >= 3 and parts[-2] in ('co', 'com', 'net', 'org', 'gov', 'ac') and parts[-1] == 'in':
        return '.'.join(parts[-3:])
    return '.'.join(parts[-2:]) if len(parts) >= 2 else d

def seen_match(r):
    d = dom(r.get('website')); l = li(r.get('linkedin_url')); n = nm(r.get('company_name')); b = nm(r.get('brand_name'))
    hits = []
    if d and d not in GENERIC_DOMAINS:
        hits += [('domain', s) for s in by_dom.get(d, [])]
        if not hits:
            rd = regdom(d)
            hits += [('domain', s) for k, v in by_dom.items() if regdom(k) == rd for s in v]
    if l: hits += [('linkedin', s) for s in by_li.get(l, [])]
    for x in {n, b}:
        if x: hits += [('name', s) for s in by_nm.get(x, [])]
    if hits: return 'strong', hits
    soft = []
    for x in {n, b}:
        c = core(x)
        if len(c) >= 5:
            for s in by_core.get(c, []):
                (hits if ' ' in c else soft).append(('core', s))
    if hits: return 'strong', hits
    if soft: return 'fuzzy', [('core-1word', soft[0][1])]
    # fuzzy name: high token-sort ratio, or multi-token containment
    best = None
    for x in {n, b}:
        if len(x) < 4: continue
        for sn, s in seen_norms:
            sc = fuzz.token_sort_ratio(x, sn)
            if sc >= 93 or (len(x.split()) >= 2 and len(sn.split()) >= 2 and (x.startswith(sn + ' ') or sn.startswith(x + ' '))):
                if not best or sc > best[0]: best = (sc, s)
    if best: return 'fuzzy', [('fuzzy%d' % best[0], best[1])]
    return None, []

def group_match(r):
    text = ' | '.join(str(r.get(k, '')) for k in ('company_name', 'brand_name', 'key_brands', 'parent_group'))
    for g, t, rx in GROUP_RX:
        m = rx.search(text)
        if m: return g, t, m.group(0)
    return None

LEAD = [  # (industry, sub-industry regex, lead module, secondary, priority weight 0-2)
 ('BFSI', r'NBFC|Housing|Gold|Micro', 'Creative AI (AI Designer) + Brand Brain', 'Paid Media AI', 2),
 ('BFSI', r'Broking|Asset|Fintech', 'Creative AI (content/SEO) + Consumer AI', 'Reporting', 2),
 ('BFSI', r'Bank|Insurance', 'Consumer AI (Brand Moderator) + Creative AI', 'Reporting', 2),
 ('Retail, Electronics & Beauty', r'.', 'Consumer AI (Brand Moderator + Insights)', 'Creative AI (store & marketplace)', 2),
 ('Food, FMCG & QSR', r'QSR|Caf|Delivery|Meat', 'Consumer AI (reviews & ORM)', 'Paid Media AI', 2),
 ('Food, FMCG & QSR', r'.', 'Paid Media AI', 'Creative AI (per-SKU governance)', 2),
 ('Health & Wellness', r'.', 'Paid Media AI + Creative AI', 'Consumer AI', 2),
 ('Healthcare', r'.', 'Consumer AI (reviews & ORM)', 'Paid Media AI', 1),
 ('Real Estate', r'.', 'Paid Media AI + Reporting (lead funnel)', 'Creative AI', 1),
 ('Automotive', r'.', 'Paid Media AI + Creative AI (dealer localisation)', 'Consumer AI', 1),
 ('Hospitality', r'.', 'Consumer AI (reviews & ORM)', 'Paid Media AI', 1),
 ('Airlines & Aviation', r'.', 'Consumer AI (Brand Moderator)', 'Creative AI', 1),
 ('Home improvement', r'.', 'Creative AI (dealer & retail creative)', 'Paid Media AI', 1),
]

def lead(ind, sub):
    for i, rx, a, b, w in LEAD:
        if i == ind and re.search(rx, sub or ''): return a, b, w
    return 'Brand Brain + Paid Media AI', 'Creative AI', 1

def score(r):
    rev = r['revenue_inr_cr'] or 0
    s = 2 if rev < 1000 else 3 if rev < 2500 else 4 if rev < 10000 else 5
    _, _, w = lead(r['industry'], r['sub_industry']); s += w
    sig = (r.get('consumer_signals') or '').lower()
    s += min(2, sum(k in sig for k in ('store', 'outlet', 'app', 'd2c', 'ads', 'meta', 'youtube', 'ecommerce', 'e-commerce', 'online', 'marketplace', 'campaign', 'showroom', 'branch', 'dealer')))
    s += {'High': 1, 'Medium': 0, 'Low': -1}.get(r.get('confidence'), 0)
    if r.get('ownership', '').startswith('MNC'): s -= 1
    return max(1, min(10, s))

def num(x):
    try: return float(str(x).replace(',', '').replace('₹', '').strip())
    except: return None

def main():
    rows = []
    for f in sorted(glob.glob('raw/*.jsonl')):
        for i, line in enumerate(open(f, encoding='utf-8', errors='ignore')):
            line = line.strip().rstrip(',')
            if not line.startswith('{'): continue
            try: r = json.loads(line)
            except Exception: continue
            r['_file'] = f.split('/')[-1]; r['revenue_inr_cr'] = num(r.get('revenue_inr_cr'))
            rows.append(r)
    out = []; dedupe = {}
    for r in rows:
        r['final_status'] = None; r['final_reason'] = ''
        if (r.get('verdict') or '').lower() != 'qualified':
            r['final_status'] = 'Rejected'; r['final_reason'] = r.get('reject_reason') or 'Rejected by researcher'
        elif r['revenue_inr_cr'] is None or r['revenue_inr_cr'] < 500:
            r['final_status'] = 'Rejected'; r['final_reason'] = 'Revenue below ₹500 cr or unverified'
        elif not re.search(r'FY ?2[4-7]|20(24|25|26)', str(r.get('revenue_fy') or '')):
            r['final_status'] = 'Rejected'; r['final_reason'] = f"Unverified: revenue figure not dated FY24 or later ({r.get('revenue_fy') or 'no year'})"
        elif not (r.get('revenue_source_url') or '').startswith('http'):
            r['final_status'] = 'Rejected'; r['final_reason'] = 'No revenue source URL'
        if not r['final_status']:
            g = group_match(r)
            if g:
                r['final_status'] = 'Rejected'; r['final_reason'] = f'Group excluded: {g[0]} (trigger: {g[1]}; matched "{g[2]}")'
        if not r['final_status']:
            kind, hits = seen_match(r)
            if kind == 'strong':
                srcs = sorted({h[1]['source'] for h in hits}); names = sorted({h[1]['name'] for h in hits})[:3]
                r['final_status'] = 'Rejected'; r['final_reason'] = f'Already known ({", ".join(srcs)}): {"; ".join(names)}'
            elif kind == 'fuzzy':
                r['_fuzzy'] = f'{hits[0][0]}: {hits[0][1]["name"]} ({hits[0][1]["source"]})'
        # cross-agent dedupe (keep higher confidence / larger revenue source)
        if not r['final_status']:
            k = dom(r.get('website')) or nm(r.get('company_name'))
            k2 = nm(r.get('company_name'))
            prev = dedupe.get(k) or dedupe.get(k2)
            if prev:
                rank = {'High': 3, 'Medium': 2, 'Low': 1}
                if rank.get(r.get('confidence'), 0) > rank.get(prev.get('confidence'), 0):
                    prev['final_status'] = 'Rejected'; prev['final_reason'] = f'Duplicate of {r["company_name"]} (kept one row)'
                    dedupe[k] = dedupe[k2] = r
                else:
                    r['final_status'] = 'Rejected'; r['final_reason'] = f'Duplicate of {prev["company_name"]} (kept one row)'
            else:
                dedupe[k] = dedupe[k2] = r
        out.append(r)
    ov = json.load(open('overrides.json')) if __import__('os').path.exists('overrides.json') else {}
    ovn = {nm(k): v for k, v in ov.items()}
    for r in out:
        if not r['final_status'] and (r.get('company_name') in ov or nm(r.get('company_name')) in ovn):
            r['final_status'] = 'Rejected'; r['final_reason'] = ov.get(r.get('company_name')) or ovn[nm(r.get('company_name'))]
    for r in out:
        if not r['final_status']:
            r['final_status'] = 'Qualified'
            a, b, _ = lead(r.get('industry'), r.get('sub_industry'))
            r['lead_module'] = a; r['expansion_module'] = b; r['fit_score'] = score(r)
            r['revenue_usd'] = round(r['revenue_inr_cr'] * 1e7 / USD_RATE)
    json.dump(out, open('merged.json', 'w'), ensure_ascii=False, indent=0)
    c = collections.Counter(r['final_status'] for r in out)
    print('rows', len(out), dict(c))
    q = [r for r in out if r['final_status'] == 'Qualified']
    print(collections.Counter(r.get('industry') for r in q).most_common())
    fz = [r for r in q if r.get('_fuzzy')]
    print('fuzzy to review', len(fz))
    with open('review_fuzzy.txt', 'w') as fh:
        for r in fz: fh.write(f"{r['company_name']} | {r.get('website')} || {r['_fuzzy']}\n")
    rc = collections.Counter(re.sub(r'[:(].*', '', r['final_reason']).strip() for r in out if r['final_status'] == 'Rejected')
    print(rc.most_common(12))

if __name__ == '__main__':
    main()
