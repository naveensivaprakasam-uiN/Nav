import sys, csv, json; sys.path.insert(0,'.')
from load import *
rows=[]
def add(src,name,web=None,lnk=None,extra=''):
    if not name or str(name).strip() in ('','None'): return
    rows.append(dict(source=src,name=str(name).strip(),norm=nm(name),domain=dom(web),li=li(lnk),extra=extra))
tam=load_tabs('inputs/tam_723.xlsx')
for t,(h,r) in tam.items():
    if t=='Summary': continue
    for d in r: add('TAM723',d.get('Company Name'),d.get('Website'),d.get('Company Linkedin Url') or d.get('Company LinkedIn URL'),t+' / '+str(d.get('Industry')))
ap=load_tabs('inputs/apollo_all.xlsx')
for t,(h,r) in ap.items():
    for d in r: add('APOLLO',d.get('Company Name'),d.get('Website'),d.get('Company Linkedin Url'),t)
ex=load_tabs('inputs/exclusions.xlsx')
for d in ex['Meta Ad Accounts'][1]: add('CLIENT_META',d.get('Brand'))
for d in ex['Pipeline_Draft'][1]: add('PIPELINE',d.get('Brand'),extra=str(d.get('Status')))
for d in ex['Account List'][1]: add('ACCOUNT_LIST',d.get('Account Name'))
for d in load_tabs('inputs/active_connections.xlsx')['Sheet1'][1]: add('ACTIVE_CONN',d.get('Institution'))
for line in open('wiki_prospects.txt'):
    st,name,ind=[x.strip() for x in line.split('|')]
    add('WIKI_'+st.upper().replace(' ','_'),name,extra=ind)
json.dump(rows,open('seen_index.json','w'))
import collections
print(collections.Counter(r['source'] for r in rows))
# agent-facing compact list
ex_names=sorted(set(r['name'] for r in rows if not r['source'] in('APOLLO','TAM723')))
seen=sorted(set(f"{r['name']} | {r['domain']}" for r in rows))
open('agent_exclusions.txt','w').write('\n'.join(ex_names))
open('agent_seen_all.txt','w').write('\n'.join(seen))
print(len(ex_names),len(seen))
