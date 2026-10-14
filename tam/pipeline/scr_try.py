import json, sys, re
sys.path.insert(0, '.')
import screener
from rapidfuzz import fuzz
M = json.load(open('batches/map.json'))
todo = []
for x in M:
    d = x['d']
    if not d: todo.append(x['b']['Company Name'])
    elif d['Status'] == 'Keep – ICP' and not d.get('Revenue source') and d.get('Part of list') != 'Expansion (verified)':
        todo.append(x['b']['Company Name'])
todo = list(dict.fromkeys(todo))
out = {}
for n in todo:
    q = re.sub(r'\(.*?\)|Pvt\.?|Ltd\.?|Limited|Private|India|Group|- India', ' ', n).strip()
    hits = screener.search(q)[:3]
    best = None
    for h in hits:
        sc = fuzz.token_set_ratio(q.lower(), h['name'].lower())
        if sc >= 85:
            r = screener.parse(h['url'] if 'consolidated' in h['url'] else h['url'].rstrip('/') + '/consolidated/') or screener.parse(h['url'])
            if r: best = dict(r, score=sc, hit=h['name']); break
    out[n] = best
    print(n, '->', (best['hit'], best['revenue_inr_cr'], best['revenue_fy']) if best else None, flush=True)
json.dump(out, open('batches/scr_results.json', 'w'), indent=0)
