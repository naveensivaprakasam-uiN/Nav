import openpyxl, re
from urllib.parse import urlparse
def dom(u):
    if not u: return ''
    u=str(u).strip().lower()
    if not u.startswith('http'): u='http://'+u
    h=urlparse(u).netloc
    return h[4:] if h.startswith('www.') else h
def li(u):
    if not u: return ''
    m=re.search(r'linkedin\.com/(company|school|showcase)/([^/?#]+)',str(u).lower())
    return m.group(2).strip('.') if m else ''
SUFFIX=r'\b(private|pvt|limited|ltd|llp|inc|india|co|company|corporation|corp|group|of companies|the)\b'
def nm(s):
    s=str(s or '').lower()
    s=re.sub(r'\(.*?\)','',s); s=s.replace('&',' and ')
    s=re.sub(r'[^a-z0-9 ]',' ',s); s=re.sub(SUFFIX,' ',s)
    return re.sub(r'\s+',' ',s).strip()
def load_tabs(path):
    wb=openpyxl.load_workbook(path,read_only=True,data_only=True)
    out={}
    for ws in wb.worksheets:
        rows=list(ws.iter_rows(values_only=True))
        hdr=[str(h).strip() if h else '' for h in rows[0]]
        recs=[]
        for r in rows[1:]:
            if not any(c not in (None,'') for c in r): continue
            d={hdr[i]:r[i] for i in range(len(hdr)) if hdr[i]}
            recs.append(d)
        out[ws.title]=(hdr,recs)
    return out
