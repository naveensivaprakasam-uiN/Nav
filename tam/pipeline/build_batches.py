"""Final verified status for every account in Tensai batches 1-3."""
import json, glob, collections, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
M = json.load(open('batches/map.json'))
SCR = json.load(open('batches/scr_results.json'))
BAD_SCR = {'vivo India', 'Hilton (India)', 'Merino Group', 'Lotte India', 'Bharat Hotels (The Lalit)'}
EXP = json.load(open('batches/exp_src.json'))
RES = {}
for f in glob.glob('batches/res_*.jsonl'):
    for l in open(f):
        try: x = json.loads(l); RES[x['company']] = x
        except Exception: pass
EXC = {'Clove Dental': ('KEEP', 450, 'FY26', '', 'Yes – dental clinic chain (600+ clinics)',
                        'Exception approved by Zocket: ₹450 Cr FY26, projected ₹600 Cr, ~200 live ads')}
TODAY = datetime.date.today().strftime('%d-%b-%Y')
rows = []
for x in M:
    b, d = x['b'], x['d']
    n = b['Company Name']
    st = rev = fy = src = b2c = why = ''
    if n in EXC:
        st, rev, fy, src, b2c, why = EXC[n]
    elif n in RES:
        r = RES[n]
        st = r['verdict']; rev = r.get('revenue_inr_cr') or ''; fy = r.get('revenue_fy') or ''
        src = r.get('source_url') or ''; b2c = r.get('b2c') or ''; why = r.get('reason') or ''
    elif n in SCR and SCR[n] and n not in BAD_SCR:
        s = SCR[n]; st = 'KEEP' if s['revenue_inr_cr'] >= 500 else 'REMOVE'
        rev, fy, src = s['revenue_inr_cr'], s['revenue_fy'], s['url']; b2c = 'Yes'
        why = f"Listed – {s['screener_name']} revenue ₹{s['revenue_inr_cr']:,.0f} Cr {s['revenue_fy']} (screener)"
    elif d:
        stt = d['Status']
        if stt.startswith('Keep'):
            st = 'KEEP'; rev = d.get('Revenue (₹ Cr)') or ''; src = d.get('Revenue source') or ''; b2c = 'Yes'
            why = d.get('Reason') or ''
            if not src and n in EXP:
                e = EXP[n]; rev, fy, src, b2c = e['rev'], e['fy'], e['src'], e['b2c']
                why = f"Verified in expansion research – ₹{float(e['rev']):,.0f} Cr {e['fy']}"
            if not src: st, why = 'CHECK', 'No revenue source yet – pending verification'
        elif 'already with Zocket' in stt: st, why = 'ZOCKET', d.get('Reason') or ''
        elif 'duplicate' in stt: st, why = 'DUP', d.get('Reason') or ''
        else: st, why = 'REMOVE', d.get('Reason') or ''
        if st in ('REMOVE',) and d.get('Revenue (₹ Cr)'): rev, src = d['Revenue (₹ Cr)'], d.get('Revenue source') or ''
    else:
        st, why = 'CHECK', 'Not in TAM – pending verification'
    rows.append(dict(batch=b['Batch'], name=n, email_name=b.get('Company Name for Emails', ''), industry=b.get('Industry', ''),
                     website=b.get('Website', ''), li=b.get('Company LinkedIn URL', ''), city=b.get('Company City', ''),
                     st=st, rev=rev, fy=fy, src=src, b2c=b2c, why=why))
LBL = {'KEEP': 'Verified – ICP (OK to call)', 'REMOVE': 'Remove – not ICP', 'ZOCKET': "Remove – already with Zocket (don't call)",
       'DUP': 'Remove – duplicate', 'CHECK': 'Pending check'}
COL = {'KEEP': 'DCFCE7', 'REMOVE': 'FEE2E2', 'ZOCKET': 'FEF3C7', 'DUP': 'FEE2E2', 'CHECK': 'E0E7FF'}
HDR = PatternFill('solid', fgColor='1F2937')
def head(ws, h):
    ws.append(h)
    for c in ws[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = HDR; c.alignment = Alignment(wrap_text=True)
wb = Workbook(); s = wb.active; s.title = 'Summary'
H = ['Batch', 'Company Name', 'Company Name for Emails', 'Industry', 'Website', 'Company LinkedIn URL', 'City', 'Status', 'Revenue (₹ Cr)',
     'Revenue FY', 'Revenue source (link)', 'Sells to consumers?', 'Reason']
order = ['KEEP', 'CHECK', 'ZOCKET', 'REMOVE', 'DUP']
def put(ws, sel, verified_col=False):
    head(ws, H + (['Verified on'] if verified_col else []))
    for r in sorted(sel, key=lambda r: (r['batch'], order.index(r['st']), r['industry'], r['name'].lower())):
        ws.append([r['batch'], r['name'], r['email_name'], r['industry'], r['website'], r['li'], r['city'], LBL[r['st']], r['rev'], r['fy'],
                   r['src'], r['b2c'], r['why']] + ([TODAY] if verified_col else []))
        ws.cell(ws.max_row, 8).fill = PatternFill('solid', fgColor=COL[r['st']])
        if str(r['src']).startswith('http'): ws.cell(ws.max_row, 11).hyperlink = str(r['src'])
    for i, w in enumerate([9, 38, 30, 26, 30, 34, 14, 30, 12, 9, 44, 34, 60, 13], 1):
        ws.column_dimensions[chr(64 + i)].width = w
    ws.freeze_panes = 'C2'; ws.auto_filter.ref = ws.dimensions
put(wb.create_sheet('Verified list – OK to call'), [r for r in rows if r['st'] == 'KEEP'], True)
for bn in ('Batch 1', 'Batch 2', 'Batch 3'):
    put(wb.create_sheet(f'{bn} – all accounts'), [r for r in rows if r['batch'] == bn])
c = collections.Counter((r['batch'], r['st']) for r in rows)
s.append(['Tensai batches 1–3 – re-verification']); s['A1'].font = Font(bold=True, size=14)
s.append([f'Checked on {TODAY}. Every "Verified" account has a revenue figure ≥ ₹500 Cr with a source link and a consumer-facing check.']); s.append([])
s.append(['Status', 'Batch 1', 'Batch 2', 'Batch 3', 'Total']); [setattr(x, 'font', Font(bold=True)) for x in s[s.max_row]]
for st in order:
    v = [c[(b, st)] for b in ('Batch 1', 'Batch 2', 'Batch 3')]
    s.append([LBL[st]] + v + [sum(v)])
v = [sum(c[(b, st)] for st in order) for b in ('Batch 1', 'Batch 2', 'Batch 3')]
s.append(['Total'] + v + [sum(v)])
s.append([]); s.append(['Removal reasons', 'Accounts']); [setattr(x, 'font', Font(bold=True)) for x in s[s.max_row]]
import re
def bucket(r):
    w = r['why'] or ''
    if r['st'] == 'DUP': return 'Duplicate of another account'
    if r['st'] == 'ZOCKET': return 'Already with Zocket (client / pipeline / account list / group)'
    if w.startswith('Car dealer'): return 'Car dealer'
    if w.startswith('Government'): return 'Government / PSU'
    if re.search(r'(?i)no verifiable', w): return 'No verifiable revenue figure'
    if re.search(r'(?i)not b2c|b2b|manufactur|rx|foreign|industrial|insolvent|distress|dsa|hni|msme|excluded by rule', w): return 'Not B2C / outside ICP'
    return 'Revenue below ₹500 Cr'
for k, v in collections.Counter(bucket(r) for r in rows if r['st'] in ('REMOVE', 'DUP', 'ZOCKET')).most_common(): s.append([k, v])
s.column_dimensions['A'].width = 70
for col in 'BCDE': s.column_dimensions[col].width = 11
wb.save('/home/user/Nav/tam/Tensai_Batches_1-3_Reverified.xlsx')
print(c); print('CHECK left:', [r['name'] for r in rows if r['st'] == 'CHECK'])
