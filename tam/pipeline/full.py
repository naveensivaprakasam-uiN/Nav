import csv, json, re, sys, collections
sys.path.insert(0, '.')
from load import nm
import merge
from govt import is_govt
T = list(csv.DictReader(open('inputs/tensai.csv', encoding='utf-8-sig')))
TAM = list(csv.DictReader(open('inputs/tam_all.csv', encoding='utf-8-sig')))
seen = [s for s in json.load(open('seen_index.json')) if s['source'] != 'APOLLO']
def clean(n): return re.sub(r'\(.*?\)', ' ', n or '').replace('ABC - ', '').replace(' - Fedfina', '')
def keys(n):
    k = nm(clean(n)); return {x for x in (k, merge.core(k)) if len(x) >= 5 or (x == k and len(x) >= 4)}
IDX = collections.defaultdict(set)
for s in seen:
    for k in keys(s['name']): IDX[k].add(s['source'])
for t in TAM:
    for k in keys(t['Company Name']) | keys(t['Company Name For Emails']): IDX[k].add('TAM')
PRI = [('CLIENT_META', 'Existing Zocket client'), ('WIKI_CUSTOMER', 'Existing Zocket client'),
       ('PIPELINE', 'In Zocket sales pipeline / in talks'), ('WIKI_ACTIVE_PROSPECT', 'In Zocket sales pipeline / in talks'),
       ('WIKI_EXPLORING', 'In Zocket sales pipeline / in talks'), ('ACTIVE_CONN', 'Active conversation with Zocket'),
       ('ACCOUNT_LIST', 'Already in Zocket target account list'), ('TAM', 'Already in Zocket TAM'), ('TAM723', 'Already in Zocket TAM')]
def known(n):
    src = set()
    for k in keys(n): src |= IDX.get(k, set())
    for s, label in PRI:
        if s in src: return label
    return None
out = []
for t in T:
    n = t['Account list'].strip()
    r = dict(name=n, tq=t['Qualification'], trev=t['Est. Annual Revenue (₹ Cr)'], tnote=t['Reason / Notes'], vert=t['Industry vertical'], parent=t['Parent industry'])
    k = known(n)
    g = merge.group_match({'company_name': clean(n)})
    if k: r['layer'] = k
    elif g: r['layer'] = 'GROUP'; r['group'] = g[0]
    elif is_govt({'company_name': n, 'ownership': '', 'parent_group': '', 'b2c_rationale': t['Reason / Notes']}): r['layer'] = 'GOVT'
    else: r['layer'] = 'REST'
    out.append(r)
json.dump(out, open('tensai/full_layers.json', 'w'), indent=1)
print(collections.Counter(r['layer'] for r in out))
print(collections.Counter((r['layer'] == 'REST', r['tq']) for r in out))
