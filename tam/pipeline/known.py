"""'Known' = existing 723 TAM + hard exclusion lists (customers, pipeline, account list, connections, wiki). Apollo is NOT a blocker anymore."""
import json, collections, sys
sys.path.insert(0,'.')
from load import nm, dom, li
from rapidfuzz import fuzz
import merge
seen=[s for s in json.load(open('seen_index.json')) if s['source']!='APOLLO']
G=merge.GENERIC_DOMAINS
bd=collections.defaultdict(list); bl=collections.defaultdict(list); bn=collections.defaultdict(list); bc=collections.defaultdict(list)
for s in seen:
    if s['domain'] and s['domain'] not in G: bd[s['domain']].append(s)
    if s['li']: bl[s['li']].append(s)
    if s['norm']: bn[s['norm']].append(s)
    c=merge.core(s['norm'])
    if len(c)>=5: bc[c].append(s)
def known(name, website='', linkedin='', extra_names=()):
    d=dom(website); l=li(linkedin)
    if d and d not in G and d in bd: return 'strong', bd[d][0]
    if l and l in bl: return 'strong', bl[l][0]
    for x in (name,)+tuple(extra_names):
        n=nm(x)
        if n in bn: return 'strong', bn[n][0]
        c=merge.core(n)
        if len(c)>=5 and c in bc: return ('strong' if ' ' in c else 'soft'), bc[c][0]
    return None, None
def excluded_group(text):
    return merge.group_match({'company_name':text})
