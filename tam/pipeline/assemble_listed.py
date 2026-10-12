"""Build raw/r2_listed.jsonl from screener-verified listed candidates + consumer triage."""
import sys, json, glob; sys.path.insert(0,'.')
from screener import verify, parse
V=json.load(open('verified_listed.json'))
def tri(files):
    d={}
    for f in files:
        for l in open(f):
            try: r=json.loads(l); d[r['name']]=r
            except: pass
    return d
T=tri(glob.glob('triage/scr_out_*.jsonl'))
rows=[]
def row(name,ind,sub,r,t,src):
    keep=(t or {}).get('keep','Yes')
    v=r or {}
    ok=keep in ('Yes','Maybe') and v.get('revenue_inr_cr') and v['revenue_inr_cr']>=500 and v.get('revenue_fy','').startswith(('FY24','FY25','FY26','FY27','CY2025','CY2026','CY2024'))
    fy=v.get('revenue_fy','')
    if fy.startswith('CY'): fy='FY'+str(int(fy[2:])+1)[-2:]
    reason='' if ok else ('Not consumer-facing / B2B: '+(t or {}).get('reason','') if keep not in ('Yes','Maybe') else ('Revenue ₹%s cr %s'%(v.get('revenue_inr_cr'),v.get('revenue_fy')) if v.get('revenue_inr_cr') else 'Screener figure not found'))
    return {'company_name':(t or {}).get('canonical_company') or v.get('screener_name') or name,'brand_name':(t or {}).get('canonical_company') or name,
      'key_brands':'','parent_group':(t or {}).get('parent_group') or 'Independent','industry':(t or {}).get('industry') or ind,'sub_industry':(t or {}).get('sub_industry') or sub,
      'website':'','linkedin_url':'','hq_city':'','hq_state':'','ownership':'Indian listed','revenue_inr_cr':v.get('revenue_inr_cr'),'revenue_fy':fy,
      'revenue_basis':v.get('basis','')+' revenue (screener.in)','revenue_source_url':v.get('url',''),'b2c_rationale':(t or {}).get('reason',''),
      'consumer_signals':v.get('about','')[:200],'verdict':'Qualified' if ok else 'Rejected','reject_reason':reason,'confidence':'High','_from_apollo':src=='apollo'}
C={c['url']:c for c in json.load(open('cand_screener.json'))}
for k,v in V.items():
    if k.startswith('S:'):
        c=C.get(k[2:]); 
        if not c: continue
        rows.append(row(c['name'],c['industry'],c['sub_industry'],v,T.get(c['name']),'screener'))
A={e['company_name']:e for e in json.load(open('cand_apollo.json'))}
for k,v in V.items():
    if k.startswith('A:'):
        e=A.get(k[2:])
        if not e: continue
        t={'keep':'Yes' if e['keep']=='Yes' else 'Maybe','canonical_company':e['company_name'],'parent_group':e.get('parent_group'),'industry':e['industry'],'sub_industry':e['sub_industry'],'reason':e.get('reason','')}
        if e['keep']=='Maybe': t['keep']='Yes'   # listed + verified revenue: accept Maybe if revenue clears; B2B ones were already No
        rr=row(e['company_name'],e['industry'],e['sub_industry'],v,t,'apollo'); rr['website']=e.get('website') or ''; rr['linkedin_url']=e.get('linkedin') or ''; rr['hq_city']=e.get('city') or ''; rr['hq_state']=e.get('state') or ''
        rows.append(rr)
with open('raw/r2_listed.jsonl','w') as f:
    for r in rows: f.write(json.dumps(r,ensure_ascii=False)+'\n')
import collections; print(len(rows),collections.Counter(r['verdict'] for r in rows))
