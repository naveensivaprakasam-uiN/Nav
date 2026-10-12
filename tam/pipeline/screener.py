"""Verify revenue of listed Indian companies via screener.in (no search engine)."""
import subprocess, json, re, os, time, hashlib, sys
from bs4 import BeautifulSoup
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
C='cache/screener'
def get(url):
    f=os.path.join(C,hashlib.md5(url.encode()).hexdigest())
    if os.path.exists(f): return open(f,encoding='utf-8',errors='ignore').read()
    for i in range(3):
        r=subprocess.run(['curl','-sS','-L','-m','30','-A',UA,url],capture_output=True)
        t=r.stdout.decode('utf-8','ignore')
        if r.returncode==0 and t and 'Too Many Requests' not in t[:500]: break
        time.sleep(4*(i+1))
    open(f,'w').write(t); time.sleep(0.8); return t
def search(q):
    t=get('https://www.screener.in/api/company/search/?q='+re.sub(r'\s+','+',q.strip()))
    try: return json.loads(t)
    except Exception: return []
def parse(url):
    h=get('https://www.screener.in'+url)
    s=BeautifulSoup(h,'html.parser'); sec=s.select_one('section#profit-loss')
    if not sec or not sec.select_one('table'): return None
    t=sec.select_one('table'); hdr=[th.get_text(strip=True) for th in t.select('thead th')]
    row=None
    for tr in t.select('tbody tr'):
        lab=tr.select_one('td').get_text(strip=True).rstrip('+').strip() if tr.select_one('td') else ''
        if lab in ('Sales','Revenue','Revenue from operations','Total Income'):
            row=[td.get_text(strip=True) for td in tr.select('td')]; break
    if not row: return None
    vals=list(zip(hdr[1:],row[1:]))
    vals=[(p,v) for p,v in vals if p!='TTM' and re.match(r'[A-Z][a-z]{2} \d{4}',p)]
    if not vals: return None
    p,v=vals[-1]
    try: v=float(v.replace(',',''))
    except: return None
    mon,yr=p.split(); yr=int(yr)
    fy=f"FY{str(yr if mon in ('Mar','Apr','May','Jun') else yr+1)[-2:]}" if mon!='Dec' else f"CY{yr}"
    name=(s.select_one('h1') or s.select_one('title')).get_text(strip=True)
    about=(s.select_one('.company-profile .about') or s.select_one('.about'))
    peers=s.select_one('#peers')
    sector=' > '.join(a.get_text(strip=True) for a in (peers.select('a[href*="/market/"]') if peers else []))
    return {'screener_name':name,'revenue_inr_cr':v,'period':p,'revenue_fy':fy,'url':'https://www.screener.in'+url,
            'about':about.get_text(' ',strip=True)[:400] if about else '','sector':sector,
            'basis':'consolidated' if 'consolidated' in url else 'standalone'}
def verify(name,symbol=''):
    hits=[]
    if symbol: hits=[{'url':f'/company/{symbol}/consolidated/','name':symbol}]
    if not hits or not parse(hits[0]['url']): hits=search(name)
    for hit in hits[:2]:
        u=hit['url']
        cu=u if 'consolidated' in u else u.rstrip('/')+'/consolidated/'
        r=parse(cu) or parse(u.replace('consolidated/',''))
        if r: r['match_query']=name; return r
    return None
if __name__=='__main__':
    print(json.dumps(verify(sys.argv[1], sys.argv[2] if len(sys.argv)>2 else ''),indent=1))
