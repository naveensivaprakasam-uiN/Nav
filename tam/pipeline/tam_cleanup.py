import sys, json, re, collections; sys.path.insert(0,'.')
from load import *
import importlib, merge
tabs=load_tabs('inputs/tam_723.xlsx')
recs=[(t,d) for t,(h,r) in tabs.items() if t!='Summary' for d in r]
KEEP={  # domain -> (keep industry tab, sub-industry, why)
 'himalayawellness.com':('Retail, Electronics & Beauty','Beauty, Personal Care & Wellness','Same company listed under two names (Himalaya Wellness / Himalaya Drug Co); largest line is personal care'),
 'casio.com':('Retail, Electronics & Beauty','Consumer Electronics','Watches & calculators sold retail'),
 'gonoise.com':('Retail, Electronics & Beauty','Consumer Electronics','Wearables/audio D2C'),
 'sony.co.in':('Retail, Electronics & Beauty','Consumer Electronics','TVs/audio/cameras'),
 'tecno-mobile.in':('Retail, Electronics & Beauty','Consumer Electronics','Smartphones'),
 'zebronics.com':('Retail, Electronics & Beauty','Consumer Electronics','Consumer electronics/peripherals'),
 'boat-lifestyle.com':('Retail, Electronics & Beauty','Consumer Electronics','Audio/wearables D2C'),
 'aachigroup.com':('Food, FMCG & QSR','Staples, Edible Oils & Spices','Spices & masalas'),
 'licious.in':('Food, FMCG & QSR','Meat, Fresh Food & Online Grocery','D2C meat & seafood'),
 'marico.com':('Food, FMCG & QSR','FMCG – Personal & Home Care','Parachute/Saffola — FMCG'),
 'wiproconsumercare.com':('Food, FMCG & QSR','FMCG – Personal & Home Care','Santoor/Yardley — FMCG personal care (one company, two rows)'),
 'crompton.co.in':('Home improvement','Electricals & Lighting','Fans, lighting, pumps'),
 'gmmodular.com':('Home improvement','Electricals & Lighting','Switches & wiring devices'),
 'goldmedalindia.com':('Home improvement','Electricals & Lighting','Switches & electricals'),
 'haier.com':('Home improvement','Home Appliances (AC, Washing Machine, Dishwasher, Kitchen)','Large appliances'),
 'orientelectric.com':('Home improvement','Electricals & Lighting','Fans & lighting (also conflicts: CK Birla group)'),
 'preethi.in':('Retail, Electronics & Beauty','Home, Kitchen & Furnishing','Small kitchen appliances'),
 'vguard.in':('Home improvement','Electricals & Lighting','Stabilisers, fans, wires, water heaters'),
 'voltas.com':('Home improvement','Home Appliances (AC, Washing Machine, Dishwasher, Kitchen)','ACs (also conflicts: Tata group)'),
 'voltasbeko.com':('Home improvement','Home Appliances (AC, Washing Machine, Dishwasher, Kitchen)','Large appliances (also conflicts: Tata group)'),
 'celloworld.com':('Retail, Electronics & Beauty','Home, Kitchen & Furnishing','Houseware & kitchenware'),
 'duroflexworld.com':('Home improvement','Furniture, Mattresses & Interiors','Mattresses (also conflicts: Duroflex is in pipeline)'),
 'hindware.com':('Home improvement','Tiles, Sanitaryware & Bath Fittings','Sanitaryware & bath'),
 'kurlon.com':('Home improvement','Furniture, Mattresses & Interiors','Mattresses'),
 'sheelafoam.com':('Home improvement','Furniture, Mattresses & Interiors','Sleepwell mattresses'),
 'stovekraft.com':('Retail, Electronics & Beauty','Home, Kitchen & Furnishing','Pigeon/Gilma kitchen appliances'),
 'wakefit.co':('Home improvement','Furniture, Mattresses & Interiors','D2C mattresses & furniture'),
 '1mg.com':('Healthcare','Pharmacy Retail','E-pharmacy (also conflicts: Tata group)'),
 'apollopharmacy.in':('Healthcare','Pharmacy Retail','Pharmacy chain (also conflicts: Apollo Hospitals is in account list)'),
 'countrydelight.in':('Food, FMCG & QSR','Dairy & Ice Cream','D2C milk & dairy'),
 'olaelectric.com':('Automotive','Electric Vehicles','EV two-wheelers'),
 'sobha.com':('Real Estate','Developers (Residential & Mixed-use)','Residential developer'),
 'casagrand.co.in':('Real Estate','Developers (Residential & Mixed-use)','Residential developer'),
 'kalpataruproject.com':('Real Estate','Developers (Residential & Mixed-use)','Residential developer'),
 'anantrajlimited.com':('Real Estate','Developers (Residential & Mixed-use)','Developer'),
 'signatureglobal.in':('Real Estate','Developers (Residential & Mixed-use)','Residential developer'),
}
H=['Company Name','Current TAM tab','Current sub-industry','Issue','Detail','Recommended action']
rows=[]
where=collections.defaultdict(list)
for t,d in recs:
    k=dom(d.get('Website'))
    if k and k!='not found': where[k].append((t,d))
for k,v in where.items():
    if len(v)>1:
        keep=KEEP.get(k)
        for t,d in v:
            if keep:
                act = 'KEEP here' if t==keep[0] else f'DELETE (keep in {keep[0]} › {keep[1]})'
                rows.append([d.get('Company Name'),t,d.get('Industry'),'Duplicate across tabs',keep[2],act])
            else:
                rows.append([d.get('Company Name'),t,d.get('Industry'),'Same website as another row','Check: may be two different companies sharing a domain (e.g. Raheja Developers vs Raheja Group Mumbai)','Verify; if same company keep one row'])
importlib.reload(sys.modules['groups_excluded']); importlib.reload(merge)
HARD={'CLIENT_META','PIPELINE','ACCOUNT_LIST','ACTIVE_CONN','WIKI_CUSTOMER','WIKI_ACTIVE_PROSPECT','WIKI_EXPLORING'}
seen=json.load(open('seen_index.json')); hard_norm={s['norm']:s for s in seen if s['source'] in HARD and s['norm']}
for t,d in recs:
    name=d.get('Company Name'); g=merge.group_match({'company_name':name}); hit=hard_norm.get(nm(name))
    if hit: rows.append([name,t,d.get('Industry'),'Conflicts with exclusions',f'Listed in {hit["source"].replace("_"," ").title()} as "{hit["name"]}"','Remove from TAM (already owned by sales)'])
    elif g: rows.append([name,t,d.get('Industry'),'Conflicts with exclusions (group rule)',f'{g[0]} — trigger in exclusion lists: {g[1]}','Remove from TAM (group already engaged)'])
B2B={'Auto Components (B2B)','Electronics Manufacturing (EMS)','Solar Manufacturing','Steel & Metals','Telecom Equipment','Glass Packaging','Pumps & Machinery','Chemicals','Abrasives & Industrial Products','Power & Electrical Equipment','Glass & Mirrors'}
for t,d in recs:
    if d.get('Industry') in B2B: rows.append([d.get('Company Name'),t,d.get('Industry'),'ICP violation: B2B / manufacturer','Sub-industry is B2B; ICP requires consumer-facing brands','Remove unless it runs a large B2C brand'])
for t,d in recs:
    if t=='Automotive': pass
rows.append(['','','','','',''])
rows.append(['Note','Automotive tab','automotive / oil & energy / internet / consumer services','Sub-industries are raw Apollo labels','Suggested: Passenger Vehicles, Two & Three Wheelers, Electric Vehicles, Commercial Vehicles, Tyres, Lubricants & Batteries, Auto Dealerships, Used Cars & Auto-tech, Mobility','Re-tag (new list in this file uses these)'])
json.dump({'header':H,'rows':rows},open('tam_cleanup.json','w'),ensure_ascii=False)
c=collections.Counter(r[3] for r in rows); print(c)
