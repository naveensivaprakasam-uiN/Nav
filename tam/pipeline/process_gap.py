import sys, json, glob, re, collections; sys.path.insert(0,'.')
from known import known, excluded_group
from load import nm, dom
def strip(n): return re.sub(r'\s*\(.*?\)\s*',' ',n or '').strip()
ap={nm(e['company_name']) for e in json.load(open('cand_apollo.json'))}
apdom={dom(e.get('website')) for e in json.load(open('cand_apollo.json')) if e.get('website')}
r1={nm(r['company_name']) for r in json.load(open('merged.json'))}
r1dom={dom(r.get('website')) for r in json.load(open('merged.json')) if r.get('website')}
scr={nm(c['name']) for c in json.load(open('cand_screener.json'))}
out={}; st=collections.Counter()
for f in sorted(glob.glob('triage/gap_*.jsonl')+glob.glob('triage/gap2_*.jsonl')):
    for l in open(f):
        try: r=json.loads(l)
        except: continue
        c=strip(r.get('company_name')); k=dom(r.get('website')) or nm(c)
        if k in out: continue
        kn,s=known(c,r.get('website',''),'',(r.get('brand_name') or '',))
        g=excluded_group(' | '.join([c,r.get('brand_name') or '',r.get('parent_group') or '']))
        n=nm(c); d=dom(r.get('website'))
        if kn=='strong': r['status']='known:'+s['source']+':'+s['name']
        elif g: r['status']='group:'+g[0]
        elif n in r1 or (d and d in r1dom): r['status']='round1'
        elif n in ap or (d and d in apdom): r['status']='in_apollo_cands'
        elif n in scr: r['status']='in_screener_cands'
        else: r['status']='open'
        r['company_name']=c; out[k]=r; st[r['status'].split(':')[0]]+=1
json.dump(list(out.values()),open('cand_gap.json','w'),ensure_ascii=False)
print(len(out),dict(st))
op=[r for r in out.values() if r['status']=='open']
print('open listed',sum(r.get('listed')=='Yes' for r in op),'private',sum(r.get('listed')!='Yes' for r in op))
