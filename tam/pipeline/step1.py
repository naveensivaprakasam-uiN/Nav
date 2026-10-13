import csv, json, re, sys
sys.path.insert(0, '.')
from load import nm, dom
import merge
from rapidfuzz import fuzz, process
T = list(csv.DictReader(open('inputs/tam_all.csv', encoding='utf-8-sig')))
E = {r['Company Name'] for r in csv.DictReader(open('inputs/expansion_484.csv', encoding='utf-8-sig'))}
O = [t for t in T if t['Company Name'] not in E]
print('original rows', len(O))
VL = json.load(open('verified_listed.json'))
SC = json.load(open('screener_sector_cos.json'))
M = json.load(open('merged.json'))
def clean(n): return nm(re.sub(r'\(.*?\)', ' ', n or ''))
vl = {clean(v['screener_name']): v for v in VL.values() if v and v.get('screener_name')}
sc = {}
for s in SC:
    sc.setdefault(clean(s['name']), s)
mm = {}
for r in M:
    if r.get('revenue_inr_cr'):
        for k in (clean(r['company_name']), clean(r.get('brand_name'))):
            if k: mm.setdefault(k, r)
mdom = {dom(r.get('website')): r for r in M if r.get('revenue_inr_cr') and r.get('website')}
out = []
for t in O:
    keys = {clean(t['Company Name']), clean(t['Company Name For Emails'])}
    ev = None
    for k in keys:
        if k in vl: v = vl[k]; ev = ('screener', v['revenue_inr_cr'], v['revenue_fy'], v['url']); break
    if not ev:
        for k in keys:
            if k in sc: s = sc[k]; ev = ('screener-qtr', round(s['sales_qtr'] * 4), 'FY26 run-rate', 'https://www.screener.in' + s['url']); break
    if not ev:
        for k in keys:
            if not k: continue
            m = process.extractOne(k, list(sc.keys()), scorer=fuzz.token_sort_ratio)
            if m and m[1] >= 92: s = sc[m[0]]; ev = ('screener-qtr~', round(s['sales_qtr'] * 4), 'FY26 run-rate', 'https://www.screener.in' + s['url']); break
    if not ev:
        r = mdom.get(dom(t['Website'])) if t['Website'] else None
        if not r:
            for k in keys:
                if k in mm: r = mm[k]; break
        if r: ev = ('our-research', r['revenue_inr_cr'], r.get('revenue_fy'), r.get('revenue_source_url'))
    out.append(dict(row=t, ev=ev))
json.dump(out, open('reclean/step1.json', 'w'), default=str, indent=0)
import collections
print(collections.Counter(o['ev'][0] if o['ev'] else 'none' for o in out))
print('below500 among evidenced', sum(1 for o in out if o['ev'] and o['ev'][1] and float(o['ev'][1]) < 500))
