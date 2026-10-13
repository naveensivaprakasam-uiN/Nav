"""Zocket verdict for every row of the Tensai lookalike list (1,816 rows)."""
import csv, json, re, sys, collections
sys.path.insert(0, '.')
from load import nm
import merge
from govt import is_govt
sys.path.insert(0, 'tensai')
from blank_codes_ao import load as load_ao

T = list(csv.DictReader(open('inputs/tensai.csv', encoding='utf-8-sig')))
TAM = list(csv.DictReader(open('inputs/tam_all.csv', encoding='utf-8-sig')))
seen = [s for s in json.load(open('seen_index.json')) if s['source'] != 'APOLLO']

# ---------- verdict vocabulary ----------
V_NEW = 'Qualified – added to Zocket TAM'
V_TAM = 'Qualified – already in Zocket TAM'
V_CLIENT = 'Excluded – existing Zocket client'
V_PIPE = 'Excluded – in Zocket pipeline / in talks'
V_ACCT = 'Excluded – already in Zocket account list'
V_GROUP = 'Excluded – group company already with Zocket'
V_NO = 'Not qualified'
CAT = {  # code -> (verdict, reason)
    'A': (V_NO, 'Foreign company – no India-led marketing (back office, franchise or HQ-run)'),
    'B': (V_NO, 'Not B2C – B2B fintech / software / services'),
    'C': (V_NO, 'Below ₹500 Cr – small broker, insurance broker, DSA or advisory'),
    'D': (V_NO, 'Below ₹500 Cr – small lender, bank, AMC, insurer or finance app'),
    'E': (V_NO, 'Below ₹500 Cr – small consumer brand or store'),
    'F': (V_NO, 'Not B2C – manufacturer, exporter, wholesaler or distributor'),
    'K': (V_NO, 'Not B2C – prescription pharma or medical devices (sold via doctors/hospitals)'),
    'G': (V_NO, 'Government, PSU, trust/non-profit, merged or defunct'),
    'H': (V_NO, 'Name too generic – could not identify one company'),
    'J': (V_NO, 'Revenue below ₹500 Cr or not verifiable'),
    'I': (V_GROUP, 'Same company or group already in Zocket TAM / lists'),
    'Q': (V_NEW, 'Qualified – ₹500 Cr+, consumer-facing, India-led'),
    'HNI': (V_NO, 'Not mass-market B2C – serves only HNI / institutional clients'),
    'MSME': (V_NO, 'Not B2C – lends mainly to businesses / MSMEs'),
    'DEAD': (V_NO, 'Defunct, merged, exited India or insolvent'),
    'GOV': (V_NO, 'Government, PSU, co-operative society or non-profit'),
    'LOW': (V_NO, 'Revenue below ₹500 Cr'),
    'NOREV': (V_NO, 'Revenue not verifiable – no public filed figure'),
    'B2B': (V_NO, 'Not B2C – B2B / manufacturer / exporter / captive'),
    'DEALER': (V_NO, 'Car dealer – brand advertising is run by the carmaker'),
    'LOWFIT': (V_NO, 'Low fit for Zocket – limited consumer marketing need'),
    'FOR': (V_NO, 'Foreign company – no India-led marketing (back office, franchise or HQ-run)'),
}

# ---------- manual verdicts (Zocket research) ----------
MAN = {}
for n, (v, why) in json.load(open('tensai/man_qualified.json')).items():
    MAN[n] = {'CAN ADD': ('Q', why), 'Duplicate': ('TAM', why), 'Already known': ('ACCT', why),
              'Group excluded': ('I', why), 'Not confirmed': ('NOREV', why)}[v]
MAN.update({
    'Kalyani motors': ('Q', '₹2,474 Cr FY24 (CARE) – Maruti dealer group, 39 showrooms in Karnataka/Telangana'),
    'BHANDARI AUTOMOBILES PVT. LTD.': ('Q', '₹1,979 Cr FY22 (CRISIL) – Maruti & Tata dealer group, West Bengal'),
    'Kataria Automobiles Private Limited': ('Q', '₹3,600 Cr+ FY24 (CRISIL) – Maruti dealer group, Gujarat'),
    'AMP Motors': ('Q', '₹750–1,000 Cr FY25 band (MCA via Tofler) – JLR dealer'),
    'Galaxy Toyota': ('Q', '₹2,111 Cr (MCA via thecompanycheck) – Toyota dealer, Delhi NCR'),
    'BNew Mobiles Pvt.Ltd': ('Q', '₹1,250–1,500 Cr FY25 band (MCA via Tofler) – mobile retail, ~150 stores AP/TS'),
    'Branch International': ('Q', '₹832 Cr FY25 (Tracxn) – personal-loan app, 5 Cr+ users'),
    'Galderma': ('Q', '₹1,250–1,500 Cr FY25 band (MCA via Tofler) – Cetaphil, India-run marketing'),
    'OTTO Clothing Pvt Ltd': ('Q', '₹750–1,000 Cr FY25 band (MCA via Tofler) – menswear brand'),
    'Dhanlaxmi Bank Limited': ('LOWFIT', '₹1,601 Cr FY26 – conservative regional bank with limited brand/creative marketing'),
    'Shubham Housing Development Finance Company': ('Q', '₹824 Cr FY25 (Inc42; ICRA) – affordable home loans'),
    'Kuttukaran Group': ('TAM', 'Popular Vehicles & Services is in Zocket TAM'),
    'India Garage - VST Group': ('I', 'VST group – V.S.T. Motors added to Zocket TAM'),
    "Pernia's Pop-Up Shop": ('TAM', 'Purple Style Labs is in Zocket TAM'),
    'Bimbo Bakeries India': ('TAM', 'Grupo Bimbo India is in Zocket TAM'),
    'Avenue E-Commerce Limited': ('I', 'DMart (Avenue Supermarts) is in Zocket TAM'),
    'Hari Krishna Exports Pvt. Ltd.': ('I', 'KISNA (Hari Krishna group) is in Zocket TAM'),
    'Oxygen The Digital Expert': ('NOREV', 'Only a company-claimed ~₹1,000 Cr; no filed figure'),
    'Harsha Toyota AP & Telangana': ('NOREV', 'No filed revenue figure found'),
    'Arvind Motors Pvt Ltd - TATA Dealers': ('NOREV', 'No filed revenue figure (CRISIL B+ rated)'),
    'Apra Auto (I) Pvt Ltd': ('NOREV', 'Only an unverified estimate'),
    'MyCar (Pune) Pvt. Ltd.': ('NOREV', 'No filed revenue figure found'),
    'Anaamalais Toyota': ('NOREV', 'Sources conflict (₹250–620 Cr)'),
    'Amrit Cement Limited': ('B2B', '₹540 Cr cement maker – sold to builders/dealers, not a consumer brand'),
    'Fangs Technology Pvt Ltd (vivo-TN)': ('B2B', 'vivo distributor – brand marketing run by vivo India'),
    'CASHe': ('LOW', '₹607 Cr FY24 fell to ~₹325 Cr FY25'),
    'Aviva': ('I', 'Burman family (Dabur/Religare) group'),
    'Cocoblu Retail': ('F', 'Marketplace seller of other brands (RattanIndia) – not a consumer brand'),
    'Coinbase': ('FOR', 'Global crypto exchange – no India revenue/marketing team confirmed'),
    'Crypto.com': ('FOR', 'Global crypto exchange – no India entity confirmed'),
    'Gap Inc.': ('FOR', 'Sold in India by Reliance Retail (franchise)'),
    'India1 Payments Limited': ('B2B', 'White-label ATM operator – income is bank interchange fees'),
    'Khimji Jewellers': ('LOW', 'Below ₹500 Cr (targets ₹500 Cr by 2028)'),
    'Kiwi General Insurance Limited': ('NOREV', 'New insurer (licensed Mar 2026) – no revenue yet'),
    'Kshema General Insurance Limited': ('B2B', '₹771 Cr GWP, but mostly government crop-insurance schemes – little consumer marketing'),
    'Nainital Bank Limited': ('GOV', 'Bank of Baroda subsidiary (PSU)'),
    'Purple Style Labs (PSL)': ('TAM', "Purple Style Labs (Pernia's) is in Zocket TAM"),
    'WHPJewellers': ('TAM', 'Waman Hari Pethe Jewellers is in Zocket TAM'),
    'Ajanta Pharma': ('K', 'Prescription pharma maker'),
    'Kerovit - A Kajaria Company': ('I', 'Kajaria Ceramics is in Zocket TAM'),
    'PINKCITY JEWELHOUSE P. LTD.': ('B2B', 'Jewellery export manufacturer – below ₹500 Cr, no Indian consumer brand'),
    'Ethos': ('FOR', 'US online life insurer – India office is engineering only'),
    'National Life': ('H', 'Generic name – no Indian company identified'),
    'Life Pharmacy': ('FOR', 'UAE pharmacy chain – India presence only announced'),
    'Apex Group Ltd': ('B2B', 'Fund administration for asset managers – B2B'),
    'EXPRESS': ('FOR', 'US apparel chain – no India operations'),
    'Hindustan Gold Company': ('LOW', 'Small gold-buying chain – far below ₹500 Cr'),
    'Sakthi Finance Limited': ('D', 'Small Coimbatore NBFC (not Sakthi Masala)'),
    'Trident Automobiles': ('J', '₹497 Cr FY23 (MCA band) – just under ₹500 Cr'),
    'VARUN BEVERAGES LIMITED': ('B2B', 'PepsiCo bottler – mainly B2B (removed from TAM earlier)'),
    'Volvo Financial Services': ('B2B', 'Captive truck/bus finance arm – B2B'),
    'Bajaj Finance Limited': ('I', 'Bajaj group'),
    'Bath & Body Works': ('I', 'Run in India by Apparel Group – in Zocket TAM'),
})
for n, (c, d) in load_ao().items(): MAN.setdefault(n, (c, d))
for n, (c, d) in json.load(open('tensai/sheet2_codes.json')).items():
    if c == 'I' and d.startswith('Already in '): continue  # recomputed below
    MAN.setdefault(n, (c, d))

# user decisions (latest)
DEALERS = ['Kalyani motors', 'BHANDARI AUTOMOBILES PVT. LTD.', 'Kataria Automobiles Private Limited', 'AMP Motors', 'Galaxy Toyota',
           'Harsha Toyota AP & Telangana', 'Arvind Motors Pvt Ltd - TATA Dealers', 'Apra Auto (I) Pvt Ltd', 'MyCar (Pune) Pvt. Ltd.',
           'Anaamalais Toyota', 'DD Motors Official', 'India Garage - VST Group', 'PREMSONS MOTOR UDYOG PRIVATE LIMITED', 'Sireesh Auto',
           'Thirty Six Toyota', 'The Sachdev Group (TSG Automotive)', 'Sree Gokulam Motors & Services Pvt. Ltd.', 'Trident Automobiles',
           'GlobeToyota', 'Kuttukaran Group']
for d in DEALERS:
    MAN[d] = ('DEALER', MAN.get(d, (None, ''))[1] if MAN.get(d, (None, ''))[0] == 'Q' else '')
MAN['Indel Money'] = ('LOWFIT', '₹606 Cr FY26 – branch-led gold-loan lender with limited digital/brand marketing')
MAN['Marwadi Shares and Finance Ltd.'] = ('LOWFIT', '₹891 Cr FY25 – regional broker, limited brand marketing need')
MAN['BNew Mobiles Pvt.Ltd'] = ('LOWFIT', '₹1,250–1,500 Cr band – regional mobile retailer, limited marketing need')

# ---------- list matching ----------
def clean(n): return re.sub(r'\(.*?\)', ' ', n or '').replace('ABC - ', '')
def keys(n):
    k = nm(clean(n)); return {x for x in (k, merge.core(k)) if len(x) >= 4}
IDX = collections.defaultdict(set)
for s in seen:
    for k in keys(s['name']): IDX[k].add(s['source'])
for t in TAM:
    for k in keys(t['Company Name']) | keys(t['Company Name For Emails']): IDX[k].add('TAM')
PRI = [('CLIENT_META', V_CLIENT), ('WIKI_CUSTOMER', V_CLIENT), ('PIPELINE', V_PIPE), ('WIKI_ACTIVE_PROSPECT', V_PIPE),
       ('WIKI_EXPLORING', V_PIPE), ('ACTIVE_CONN', V_PIPE), ('ACCOUNT_LIST', V_ACCT), ('TAM', V_TAM), ('TAM723', V_TAM)]
WHY = {V_CLIENT: 'Existing Zocket client', V_PIPE: 'In Zocket pipeline / active conversation', V_ACCT: 'Already in Zocket account list',
       V_TAM: 'Already in Zocket TAM'}
def known(n):
    src = set()
    for k in keys(n): src |= IDX.get(k, set())
    for s, v in PRI:
        if s in src: return v
    return None

# ---------- reason from our team's earlier notes ----------
def from_notes(note, trev):
    t = note.lower()
    if re.search(r'too generic|cannot identify|could not (identify|pin)|unidentif|ambiguous|not a specific|generic term|no identifiable|name is ambiguous', t): return 'H'
    if re.search(r'no longer|amalgamated|merged into|defunct|shut down|closed all|ceased|insolven|cirp|liquidat|wound up|bankrupt|deadpool|exited india|out of business|crunchbase lists it as closed', t): return 'DEAD'
    if re.search(r'government|\bpsu\b|state-owned|public.sector|gov-owned|govt|co-?operative society|trust-run|not-for-profit|non-profit|\bngo\b|section.?8|society', t): return 'GOV'
    if re.search(r'\bhnis?\b|uhni|ultra-?hni|wealthy clients|family office|private bank|private wealth', t): return 'HNI'
    if re.search(r'msme|sme lend|business-borrower|business loans|corporate lending|venture-debt', t): return 'MSME'
    if re.search(r'car.dealer|dealer with|nexa|dealership|dealers (are )?rejected|dealer group|(maruti|suzuki|toyota|tata motors|hyundai|mahindra|jlr|honda|kia) (suzuki )?dealer', t): return 'DEALER'
    if re.search(r'prescription|\brx\b|hcp|medical.device|doctor-prescribed|hospitals? (and|&) labs', t): return 'K'
    if re.search(r'no india\b|not present in india|geography rule|no indian (operations|entity|retail|stores|team|presence)|exited|decision-?makers (are )?(in|outside|abroad)|marketing is (run|set|controlled) (globally|from)|no own india', t): return 'FOR'
    if re.search(r'b2b|manufactur|exporter|export|wholesale|distribut|saas|software|infrastructure|platform for|institutional|contract|oem|industrial|merchant|payment gateway|agency|services provider|consult|sourcing|trading|outsourc|supplier|refin|captive|capability (centre|center|hub)|back-?office|gcc|technology cent', t): return 'B2B'
    if re.search(r'india entity|only in |licen[cs]ee|franchise|global', t): return 'FOR'
    if re.search(r'single .*store|no evidence of scale|below|far below|well below|under ₹500|<\s?₹?\s?500|less than|small|tiny|sub-₹500|short of|near the|only ~|only ₹', t): return 'LOW'
    if re.search(r'unverif|no official|not verifiable|only from data sites|conflicting|no (public|filed|recent)|undisclosed|not disclosed|n/a', t): return 'NOREV'
    v = [float(x) for x in re.findall(r'\d+(?:\.\d+)?', trev.replace(',', '')) if float(x) < 1e6]
    if v and max(v) < 500: return 'LOW'
    return None

rows, unres = [], []
for t in T:
    n = t['Account list'].strip()
    code = detail = None
    if n in MAN: code, detail = MAN[n]
    if code in (None, 'TAM', 'ACCT', 'I') or code is None:
        k = known(n)
        if k and code not in ('Q',):
            verdict, reason = k, WHY[k]
            if code in ('TAM', 'ACCT', 'I') and detail: reason = WHY[k]
            rows.append((t, verdict, reason, detail or '')); continue
    if code == 'TAM': rows.append((t, V_TAM, 'Already in Zocket TAM', detail)); continue
    if code == 'ACCT': rows.append((t, V_ACCT, 'Already in Zocket account list', detail)); continue
    if code is None:
        g = merge.group_match({'company_name': clean(n)})
        PSU = r'(?i)punjab national|bank of baroda|canara bank|union bank of india|^bank of india|indian bank|central bank of india|uco bank|indian overseas|bank of maharashtra|punjab (&|and) sind|state bank|\\blic\\b|life insurance corporation|new india assurance|oriental insurance|united india insurance|national insurance|\\bgic\\b|idbi|gramin|india post|nabard|sidbi|exim bank'
        if re.search(PSU, n) or is_govt({'company_name': n, 'ownership': '', 'parent_group': '', 'b2c_rationale': t['Reason / Notes']}):
            code = 'GOV'
        elif g: rows.append((t, V_GROUP, 'Same company or group already in Zocket TAM / lists', g[0])); continue
        elif t['Reason / Notes']:
            code = from_notes(t['Reason / Notes'], t['Est. Annual Revenue (₹ Cr)'])
            detail = t['Reason / Notes'][:220]
    if code is None:
        unres.append(t); rows.append((t, '?', '?', t['Reason / Notes'][:200])); continue
    verdict, reason = CAT[code]
    rows.append((t, verdict, reason, detail or ''))

json.dump([(r[0]['Account list'], r[1], r[2], r[3]) for r in rows], open('tensai/final_rows.json', 'w'), indent=0)
print('unresolved', len(unres))
for t in unres[:80]: print(' ?', t['Account list'], '|', t['Qualification'], '|', t['Est. Annual Revenue (₹ Cr)'][:25], '|', t['Reason / Notes'][:130])
c = collections.Counter(r[1] for r in rows); print(c, sum(c.values()))
print(collections.Counter(r[2] for r in rows if r[1] == V_NO))
