import csv, json, sys, re, collections
sys.path.insert(0, '.')
from load import nm
import merge
from govt import is_govt
T = list(csv.DictReader(open('inputs/tensai.csv', encoding='utf-8-sig')))
E = list(csv.DictReader(open('inputs/expansion_484.csv', encoding='utf-8-sig')))
M = json.load(open('merged.json'))
def keys(n):
    n = re.sub(r'\(.*?\)', ' ', n or ''); n = n.replace('ABC - ', '').replace('ABC -', '')
    k = nm(n); return {k, merge.core(k)} - {''}
EK = {}
for e in E:
    for k in keys(e['Company Name']) | keys(e['Company Name For Emails']): EK[k] = e['Company Name']
MK = {}
for r in M:
    for k in keys(r['company_name']) | keys(r.get('brand_name')): MK.setdefault(k, r)
out = []
for t in T:
    n = t['Account list'].strip(); ks = keys(n)
    r = {'name': n, 'tq': t['Qualification'], 'trev': t['Est. Annual Revenue (₹ Cr)'], 'tnote': t['Reason / Notes'], 'tsrc': t['Source'], 'vert': t['Industry vertical'], 'parent': t['Parent industry']}
    hit = next((EK[k] for k in ks if k in EK and len(k) >= 4), None)
    if hit: r['status'] = 'In expansion 484'; r['match'] = hit; out.append(r); continue
    st, h = merge.seen_match({'company_name': n})
    if st == 'strong': r['status'] = 'Known: ' + h[0][1]['source']; r['match'] = h[0][1].get('name', ''); out.append(r); continue
    g = merge.group_match({'company_name': n, 'parent_group': t['Reason / Notes'][:200]})
    g0 = merge.group_match({'company_name': n})
    if g0: r['status'] = 'Group excluded'; r['match'] = g0[0]; out.append(r); continue
    if is_govt({'company_name': n, 'ownership': '', 'parent_group': '', 'b2c_rationale': t['Reason / Notes']}):
        r['status'] = 'Govt/NGO'; out.append(r); continue
    m = next((MK[k] for k in ks if k in MK and len(k) >= 5), None)
    if m: r['status'] = 'Examined by us: ' + m['final_status']; r['match'] = m['company_name'] + ' | ' + (m.get('final_reason') or ''); out.append(r); continue
    if st == 'fuzzy': r['fuzzy'] = h[0][1].get('name', '') + ' (' + h[0][1]['source'] + ')'
    if g: r['group_hint'] = g[0]
    r['status'] = 'NEW'; out.append(r)
json.dump(out, open('tensai/triage.json', 'w'), indent=1)
c = collections.Counter((r['status'] if not r['status'].startswith('Known') else 'Known', r['tq']) for r in out)
for k, v in sorted(c.items()): print(k, v)
