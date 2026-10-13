"""Build the single-sheet final list: merged Qualified rows + re-check updates."""
import sys, json, glob, re
sys.path.insert(0, '.')
from load import nm
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
OUT = sys.argv[1]
M = json.load(open('merged.json'))
Q = [r for r in M if r['final_status'] == 'Qualified']
# optional: argv[2] = existing list xlsx -> output only rows from round 10 not already in it
if len(sys.argv) > 2:
    import csv
    from merge import core
    from load import dom
    B = list(csv.DictReader(open(sys.argv[2], encoding='utf-8-sig')))
    base = {k for b in B for k in (nm(b['Company Name']), core(nm(b['Company Name'])), nm(b['Company Name For Emails'])) if len(k) >= 5}
    bdom = {dom(b['Website']) for b in B if b['Website']}
    Q = [r for r in Q if r['_file'].startswith('r10_') and not ({nm(r['company_name']), core(nm(r['company_name'])), nm(r.get('brand_name') or '')} & base)
         and dom(r.get('website')) not in bdom]
RC = {}
for f in glob.glob('round9/recheck_out_*.jsonl'):
    for l in open(f):
        try: x = json.loads(l); RC[nm(x['company_name'])] = x
        except Exception: pass
final, dropped = [], []
for r in Q:
    x = RC.get(nm(r['company_name']))
    if x:
        st = (x.get('recheck_status') or '').upper()
        if st == 'DROP': dropped.append((r['company_name'], x.get('recheck_note'))); continue
        if st == 'UPDATED' and x.get('revenue_inr_cr'):
            try: rv = float(str(x['revenue_inr_cr']).replace(',', ''))
            except Exception: rv = None
            if rv and rv >= 500:
                r.update({'revenue_inr_cr': rv, 'revenue_fy': x.get('revenue_fy'), 'revenue_basis': x.get('revenue_basis'),
                          'revenue_source_url': x.get('revenue_source_url'), 'confidence': x.get('confidence') or 'Medium'})
            elif rv and rv < 500:
                dropped.append((r['company_name'], f"Latest revenue ₹{rv} Cr {x.get('revenue_fy')}")); continue
    final.append(r)
# de-dupe by normalised name / domain one last time
seen, F = set(), []
for r in final:
    k = nm(r['company_name'])
    if k in seen: continue
    seen.add(k); F.append(r)
IND = ['Retail, Electronics & Beauty', 'Food, FMCG & QSR', 'Healthcare', 'Health & Wellness', 'BFSI', 'Home improvement',
       'Real Estate', 'Automotive', 'Hospitality', 'Airlines & Aviation', 'Media, Entertainment & Consumer Internet', 'Education']
F.sort(key=lambda r: (IND.index(r['industry']) if r['industry'] in IND else 99, r.get('sub_industry') or '', -(r['revenue_inr_cr'] or 0)))
H = ['#', 'Company Name', 'Company Name for Emails', 'Industry', 'Sub-industry', 'Website', 'Company Linkedin Url', 'Company City',
     'Company State', 'Company Country', 'Annual Revenue (₹ Cr)', 'Annual Revenue (USD)', 'Revenue Year', 'Revenue Source', 'Data Confidence',
     'Ownership', 'Parent Group', 'Key Brands', 'Why Consumer-facing', 'Zocket Fit Score (1-10)', 'Priority Tier', 'Lead Zocket Agent', 'Source']
wb = Workbook(); ws = wb.active; ws.title = 'Expansion List' if len(sys.argv) > 2 else 'Final ICP List'
ws.append(H)
for c in ws[1]:
    c.fill = PatternFill('solid', fgColor='1F2937'); c.font = Font(bold=True, color='FFFFFF'); c.alignment = Alignment(wrap_text=True, vertical='center')
for i, r in enumerate(F, 1):
    s = r.get('fit_score') or 0
    ws.append([i, r['company_name'], r.get('brand_name') or r['company_name'], r.get('industry'), r.get('sub_industry'), r.get('website'),
               r.get('linkedin_url'), r.get('hq_city'), r.get('hq_state'), 'India', round(r['revenue_inr_cr'], 1),
               round(r['revenue_inr_cr'] * 1e7 / 85), r.get('revenue_fy'), r.get('revenue_source_url'), r.get('confidence'),
               r.get('ownership'), r.get('parent_group'), r.get('key_brands'), r.get('b2c_rationale'), s,
               'A' if s >= 8 else 'B' if s >= 6 else 'C', r.get('lead_module'), r.get('source_tag')])
W = {'#': 5, 'Company Name': 38, 'Company Name for Emails': 30, 'Industry': 28, 'Sub-industry': 32, 'Website': 30, 'Company Linkedin Url': 36,
     'Revenue Source': 40, 'Key Brands': 36, 'Why Consumer-facing': 44, 'Parent Group': 26, 'Lead Zocket Agent': 38, 'Source': 34}
for i, h in enumerate(H, 1): ws.column_dimensions[get_column_letter(i)].width = W.get(h, 14)
for row in ws.iter_rows(min_row=2):
    c = row[H.index('Revenue Source')]
    if c.value and str(c.value).startswith('http'): c.hyperlink = str(c.value); c.font = Font(color='1D4ED8', underline='single')
    c = row[H.index('Website')]
    if c.value and str(c.value).startswith('http'): c.hyperlink = str(c.value)
ws.freeze_panes = 'C2'; ws.auto_filter.ref = ws.dimensions
wb.save(OUT)
print('FINAL', len(F), 'dropped', len(dropped)); [print('  drop:', d) for d in dropped]
