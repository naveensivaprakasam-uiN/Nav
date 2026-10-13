import csv, json, sys, collections
sys.path.insert(0, '.')
from load import nm
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
CAT = {
 'A': 'Foreign company – India entity is a back office/captive, or marketing not run from India',
 'B': 'B2B fintech / SaaS / payments or services infrastructure (no consumer brand)',
 'C': 'Small broker, insurance broker, loan DSA, PMS or advisory (B2B2C, well under ₹500 Cr)',
 'D': 'Small NBFC / MFI / HFC / co-op bank / AMC / lending app (well under ₹500 Cr)',
 'E': 'Small consumer brand or store (well under ₹500 Cr)',
 'F': 'Exporter, manufacturer or wholesaler (B2B)',
 'G': 'Government, merged, defunct or insolvent',
 'H': 'Name too generic to identify one company',
 'I': 'Excluded by your rules (group, mall, steel) or already covered under another name',
 'J': 'Checked: below ₹500 Cr or no public revenue figure',
 'Q': 'QUALIFIES – added',
}
M = {}
def put(c, names):
    for n in names.split(';'): M[nm(n.strip())] = c
put('A', "Poshmark;QuidelOrtho;Ramp;Retail Business Services;ROLEX;Russell Investments;S&P Global;Sarine Technologies;SS&C GlobeOp;State Street;State Street Investment Management;StoneX Group Inc.;Sol de Janeiro;Synchrony;T & T Supermarket;TAG Heuer;Tala;Tapestry;Target;Tarz - A Chalhoub Group Company;Tchibo;Terumo;Tesco Bengaluru;The Co-operative Bank plc;The Home Depot;TIAA;TOUS Jewelry;TPG;Tradeify;Trading 212;UA Brands (Uniform Advantage Brands);Unicity International;UnitedHealth Group;Urban Outfitters;VB ServiÃ§os;Versace;VGL Group;Wells Fargo;Whole Foods Market;WTW;Zolve;Rain")
put('B', "POP;Prosperr.io;Quinte Financial Technologies;Radiant Cash Management Services;RegisterKaro;RNFI SERVICES LIMITED;Rupifi;SabPaisa;SaveIN;Seair Exim Solutions;SECMARK CONSULTANCY LIMITED;SGL LABS;Smollan;Solitaire Gemmological Laboratories;StoreKing - Convert Store to Bright Store;Sub-K IMPACT Solutions Ltd;Suncrypto;Symbo;Symphony Fintech Solutions Pvt Ltd;Synapsewave Innovations Private Limited;Tazapay;TerraPay;The Clearing Corporation of India Limited (CCIL);Tracxn;Transaction Solutions International (India) Pvt Ltd;Tresor Systems Pvt. Ltd.;TresVista;udaan.com;Ultrafresh Modular Solutions;Vakrangee Limited;Vervent;Vilcart - Bridge to Rural Kirana;VK Venture Pvt Ltd. (Biznext);Vyapar;William O'Neil India;Yabx;Yubi;ZET;Zype")
put('C', "Proclaim Insurance Surveyors and Loss Assessors Private Limited;PROFITMART;Prudent Insurance Brokers Pvt Ltd.;Purnartha PMS;Resurgent India Limited;Ruloans Distribution Services Private Limited;Rupeezy;Salasar Services (Insurance Brokers) Private Limited;SAYYAM INVESTMENTS PRIVATE LIMITED;SMC Insurance Brokers Pvt Ltd;SMIFS LIMITED;Spark Capital;Spectrum Insurance Broking (P) Limited;Square Insurance Brokers Pvt. Ltd.;Sushil Finance;Swastika Investmart Limited;Teji Mandi;Tradebulls Securities(P)Ltd;Trustline;Unicon Investment Solutions;UNISON Insurance Broking Services Pvt Ltd;Univest;Urban Money;ValueQuest Investment Advisors;VCK Share & Stock Broking Services Ltd;Ventura;Venture Catalysts++ | India's 1st Multi-Stage VC;Waterfield Advisors;Way2Wealth Brokers Pvt. Ltd.;Wealthy;Xperitus Insurance Brokers Pvt Ltd;Zoom Insurance Brokers Pvt Ltd")
put('D', "Prefr;Profectus Capital Pvt. Ltd;Purple Finance Ltd;Quantum Mutual Fund;Radian Finserv Private Limited;Ram Fincorp;RATNAAFIN;Reliant Credits (India) Ltd;Revfin;Ring;Saarathi Finance;SarvaGram;SAVE Financial Managements Private Limited (Formerly SagGraha);SingleDebt;Solfin;SRG HOUSING FINANCE LIMITED;Supreme Housing Finance Limited;Surjit Finance;Svamaan Financial Services Pvt. Ltd.;Swara Fincare Limited;Tezz Capital;The Greater Bombay Co-operative Bank Limited;The Seva Vikas Co-op. Bank Ltd.;The Wealth Company;The Wealth Company Mutual Fund;Varthana;Vedika Credit Capital Ltd;Vivifi India;Weizmann Forex Ltd;WeRize;Wizzmoni Financial Services Ltd;Rama Hospital & Research Centre")
put('E', "PRASUMA;Primus Retail Pvt. Ltd;Pro Nature Organic Foods (P) Ltd;Rajakumari Groups;Ramani Ice-cream Co. Ltd.;Saraogi Super Sales Pvt. Ltd.;Showoffff;SHREE SHIVAM Attires Pvt. Ltd.;SMOOR Chocolates;Solitario Diamonds;Stanmax;Suta;Tarun Tahiliani;Taruni Clothing Pvt. Ltd.;Theater.xyz;Thomas Scott India Ltd;Twills;Universal Tribes;VADALIA FOODS;Vastu Vihar (Technoculture Building Centre Pvt Ltd);Ved Sanjeevani;Vedistry Pvt ltd;Vikram Tea;Vishnu Opticals;VIVO Healthcare;WÃ¼rfel;Wholsum Foods (Slurrp Farm and MillÃ©);William Penn (P) Ltd;Zest Melange;Zimson Watches;Zink London")
put('F', "Pratibha Syntex Ltd.;Rashi Granite Exports India Pvt.Ltd;richa & co.;Richa Global Exports Pvt Ltd;RichaCo;RMZ;Sai Creations - Star Export House;SAKTHI INFRA TEX GROUP.;samrat gems impex pvt ltd;SAPL Industries Private Limited;SCM Garments Pvt Limited - India;Scotts Garments Limited;Shades of India;Sharman Udyog Pvt Ltd;Shivaay Jewels;Shivam Jewels;Shree Ramkrishna Exports Pvt. Ltd.;Silver Crest Clothing Pvt. Ltd;Sonani Jewels;Suashish Diamonds Ltd;SUMEET SYNFAB INDIA PRIVATE LIMITED;Sunstar Overseas Ltd.;Suolificio Linea Italia India;Superhouse Limited;Su-Raj Inter Gold Pvt Ltd;Tex Fasteners;Texport Industries Pvt. Ltd.;Texport Syndicate India Ltd;The Rajlakshmi Cotton Mills Pvt Ltd;Triburg;VAJS AGRO EXPORTS PVT LTD;Vashi Electricals Pvt. Ltd.;Vashi Integrated Solutions;Weavetex Overseas;Winntus Formwork Pvt. Ltd;Zuari Industries Limited;Sparsh Pearl")
put('G', "Power Finance Corporation Ltd.;Sahara India;Srei;SREI Infrastructure Finance Limited;SREI Sahaj eVillage Limited;Stock Holding Corporation Of India Ltd;SYNDICATE BANK;Uninor;Vijaya Bank;Yebhi.com;ZestMoney")
put('H', "Quest Retail;Regent Group;ROOTS;Sagar Enterprise;sahara;Shree Hari;Shri Maa Group;SK Enterprises;Star Group;SW India;Tritan works pvt. ltd.;Up;Venus;Vijay Gems And Jewellery;vikash;VRP;Walking Tree;ZXY International")
put('I', "Relaince Digital Retail Limited;RJ Corp Retail;Royaloak Incorporation Pvt. Ltd.;Samasta Microfinance Limited;Sarath City Capital Mall;SMC Group;SRMB Steel;Sun Life;Sundaram Home Finance Official;Tablez Food Company Pvt Ltd;Vero Moda;Virtuous Retail;V-RETAIL LIMITED;WHPJewellers;ZARA;ZOYA - A TATA Product")
put('J', "PREMSONS MOTOR UDYOG PRIVATE LIMITED;Rajmandir Hypermarket;Simpl;Sireesh Auto;Sree Gokulam Motors & Services Pvt. Ltd.;SSIPL Retail LTD;sun and sand sports;Swarovski;The Sachdev Group (TSG Automotive);Thirty Six Toyota;Triumph International;True Balance;Unimoni Financial Services Limited")
put('Q', "Shubham Housing Development Finance Company")
NOTE = {
 'relaincedigitalretaillimited': 'Reliance group', 'rjcorpretail': 'RJ Corp group – Devyani International already in your lists',
 'royaloakincorporation': 'Already in your 484 (Royaloak Furniture)', 'samastamicrofinance': 'IIFL group', 'sarathcitycapitalmall': 'Mall – excluded by you',
 'smcgroup': 'Already in your 484 (SMC Global Securities)', 'srmbsteel': 'Steel/TMT – removed by you', 'sunlife': 'Aditya Birla Sun Life – Aditya Birla group',
 'sundaramhomefinanceofficial': 'Sundaram Finance group – already in TAM', 'tablezfoodcompany': 'Lulu group', 'veromoda': 'Already in your 484 (Bestseller India)',
 'virtuousretail': 'Mall operator – excluded by you', 'vretail': 'Already in your 484 (V2 Retail)', 'whpjewellers': 'Already in your 484 (Waman Hari Pethe)',
 'zara': 'Inditex–Trent JV – Tata group', 'zoyaatataproduct': 'Tata group',
 'premsonsmotorudyog': 'No public revenue figure', 'rajmandirhypermarket': 'No public revenue figure', 'simpl': '₹87 Cr (FY23)', 'sireeshauto': 'No public revenue figure',
 'sreegokulammotorsservices': 'No public revenue figure', 'ssiplretail': 'Loss-making, ratings withdrawn 2024, no figure', 'sunandsandsports': 'No public revenue figure',
 'swarovski': 'No India revenue figure', 'thesachdevgrouptsgautomotive': 'No public revenue figure', 'thirtysixtoyota': 'No public revenue figure',
 'triumphinternational': 'No India revenue figure', 'truebalance': '₹203 Cr (FY25)', 'unimonifinancialservices': 'No public revenue figure',
 'shubhamhousingdevelopmentfinancecompany': '₹824 Cr FY25 (Inc42; ICRA)',
}
S = list(csv.DictReader(open(sys.argv[1], encoding='utf-8-sig')))
T = {nm(r['name']): r for r in json.load(open('tensai/triage.json'))}
FIX = {'sakthifinance': ('J', 'Not the same as Sakthi Masala – Sakthi Finance is a small Coimbatore NBFC (<₹500 Cr)'),
       'tridentautomobiles': ('J', '₹497 Cr FY23 (MCA band) – just under ₹500 Cr'),
       'varunbeverages': ('I', 'Removed by you earlier (bottler, mainly B2B)'),
       'volvofinancialservices': ('A', 'Captive finance arm of Volvo – B2B')}
rows, unm = [], []
for s in S:
    n = s['Account list']; k = nm(n); t = T.get(k, {}); st = t.get('status', '')
    if k in FIX: c, why = FIX[k]
    elif st == 'In expansion 484': c, why = 'I', 'Already in your 484 (' + t.get('match', '') + ')'
    elif st.startswith('Known'): c, why = 'I', 'Already in ' + st.split(': ')[1].replace('TAM723', 'TAM 723').replace('ACCOUNT_LIST', 'account list').replace('PIPELINE', 'pipeline') + ' (' + t.get('match', '') + ')'
    elif st == 'Group excluded': c, why = 'I', 'Excluded group: ' + t.get('match', '')
    elif st == 'Govt/NGO': c, why = 'G', 'Government / co-op society / trust'
    elif st.startswith('Examined'): c, why = 'J', 'Checked earlier: ' + t.get('match', '').split('|', 1)[-1].strip()
    elif k in M: c = M[k]; why = NOTE.get(k, '')
    else: c, why = '?', ''; unm.append(n)
    rows.append((n, s['Parent industry'], c, CAT.get(c, 'UNCLASSIFIED'), why))
print('unmapped:', unm)
cnt = collections.Counter(r[2] for r in rows)
for c in 'QIJABCDEFGH': print(c, cnt[c], CAT[c])
print('total', sum(cnt.values()))
wb = Workbook(); ws = wb.active; ws.title = 'Sheet2 – 360 breakdown'
ws.append(['Account', 'Parent industry', 'Code', 'Why it does / does not fit', 'Detail'])
for c in ws[1]: c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='1F2937')
for r in sorted(rows, key=lambda r: ('QIJABCDEFGH'.index(r[2]) if r[2] in 'QIJABCDEFGH' else 99, r[0].lower())): ws.append(list(r))
for col, w in zip('ABCDE', (44, 18, 6, 70, 60)): ws.column_dimensions[col].width = w
ws.freeze_panes = 'A2'; ws.auto_filter.ref = ws.dimensions
s2 = wb.create_sheet('Summary'); s2.append(['Code', 'Reason', 'Count'])
for c in 'QIJABCDEFGH': s2.append([c, CAT[c], cnt[c]])
s2.column_dimensions['B'].width = 90
wb.save(sys.argv[2])
