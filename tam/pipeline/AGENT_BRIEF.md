# Zocket TAM expansion — research brief (read fully before starting)

You are expanding the Total Addressable Market list for Zocket (an AI brand operating system sold to
enterprise consumer brands). Find NEW companies that fit the ICP, verify them, and write them to a file.

## ICP (all must be true to be "Qualified")
1. Revenue >= ₹500 crore for the latest reported fiscal year: FY26 (Apr-2025–Mar-2026) if published, else FY25
   (Apr-2024–Mar-2025). FY24 only if nothing newer exists, and then mark confidence Low.
   Use consolidated revenue from operations (for banks/NBFCs: total income; insurers: gross written premium;
   cooperatives: turnover). Every revenue figure MUST have a source URL (annual report, BSE/NSE filing,
   screener.in, moneycontrol, tofler, ET/BS/Mint/Inc42/Entrackr/Fortune India, company press release).
   Never guess. If you cannot find a figure, do not mark it Qualified.
2. Consumer-facing (B2C) brand. NO manufacturers-only, contract manufacturers, EPC/infra, industrial B2B,
   commodity exporters, IT services. A B2B company qualifies ONLY if it has a large, branded B2C business.
3. Headquartered in India. Indian arm of a multinational qualifies ONLY if the Indian entity alone does
   >= ₹500 cr AND marketing decisions are made in India (India MD/CEO + India marketing head, India-specific
   campaigns/agencies) — like Bata India. Mark these ownership = "MNC – India-led".
4. NOT already known (see exclusion files) and NOT part of an excluded business group.

## Exclusion files (CHECK EVERY CANDIDATE before you spend time verifying it)
- /tmp/claude-0/-home-user-Nav/e42decda-81be-573e-bfd6-4280a147ac06/scratchpad/tam/agent_seen_all.txt
  "name | domain" for ~3,700 companies already in the TAM, the Apollo export, customers, pipeline,
  account list and connections. Use grep -i on distinctive name fragments AND the domain.
  Watch for name variants (e.g. "Kalyan Jewellers India Ltd" vs "Kalyan Jewellers").
- /tmp/claude-0/-home-user-Nav/e42decda-81be-573e-bfd6-4280a147ac06/scratchpad/tam/agent_groups_excluded.md
  Business groups that are fully excluded (parent, subsidiary, sister company, JV, franchisee).
  e.g. anything Tata, Reliance, Aditya Birla, Mahindra, Kotak, Bajaj, Godrej, HDFC, ICICI, SBI, Axis,
  Adani, Murugappa, Hinduja, Piramal, Jindal/JSW, ITC, HUL, Flipkart/PhonePe, Zomato, Nykaa...
  If a candidate's parent/promoter group is in that file, skip it.
- One company = one row. Brands owned by the same company go in one row (key_brands field), never
  separate rows. Do not list a subsidiary separately from its parent.

## Output — write JSON Lines (one JSON object per line) to the output file given in your task.
Append as you go (so work is not lost). Fields (all strings except revenue_inr_cr which is a number):
{
 "company_name": "Legal/common name, e.g. 'Senco Gold Ltd'",
 "brand_name": "Name used for emails/marketing, e.g. 'Senco Gold & Diamonds'",
 "key_brands": "comma-separated consumer brands",
 "parent_group": "promoter/business group or parent company ('Independent' if none)",
 "industry": "one of the 10 industries below",
 "sub_industry": "one sub-industry (use the list; propose a new one only if nothing fits)",
 "website": "https://...",
 "linkedin_url": "https://www.linkedin.com/company/... (best effort, '' if not found)",
 "hq_city": "", "hq_state": "",
 "ownership": "Indian listed | Indian private | Cooperative | PSU/Govt | MNC – India-led",
 "revenue_inr_cr": 1234.5,
 "revenue_fy": "FY25 | FY26 | FY24",
 "revenue_basis": "consolidated revenue from ops | standalone | total income | GWP | turnover",
 "revenue_source_url": "https://...",
 "b2c_rationale": "one line: why this is consumer-facing",
 "consumer_signals": "short: e.g. '350 stores in 4 states; app; heavy Meta/YouTube ads; D2C site'",
 "verdict": "Qualified | Rejected",
 "reject_reason": "'' or e.g. 'Revenue ₹310 cr FY25' / 'B2B manufacturer' / 'Group excluded: Tata'",
 "confidence": "High | Medium | Low  (High = audited/filed figure; Medium = credible press; Low = estimate/old)"
}
Also log notable Rejected candidates (revenue just under the bar, group-excluded, B2B) — useful for audit,
but focus effort on Qualified ones.

## Industries and sub-industries (company goes in exactly ONE — the best fit by its largest revenue line)
- Retail, Electronics & Beauty: Apparel & Fashion | Jewellery & Watches | Retail & E-commerce |
  Home Appliances & Electricals | Home, Kitchen & Furnishing | Beauty, Personal Care & Wellness | Footwear |
  Consumer Electronics | Lifestyle & Accessories
- Food, FMCG & QSR: Staples, Edible Oils & Spices | Dairy & Ice Cream | Snacks, Biscuits & Confectionery |
  QSR & Restaurants | Alcoholic Beverages | Packaged & Ready-to-eat Foods | Beverages (non-alcoholic) |
  FMCG – Personal & Home Care | Meat, Fresh Food & Online Grocery | Tea & Coffee | Nutrition & Health Foods |
  Cafés, Bakery & Desserts | Food Delivery & Quick Commerce
- Healthcare: Hospitals & Health Systems | Eye Care | Fertility & Mother-Child | Diagnostics |
  Pharmacy Retail | Pharmaceuticals (consumer/OTC-led) | Dental & Specialty Clinics
- Health & Wellness: Ayurveda & Herbal | Nutrition & Supplements | Fitness & Gyms | Salons & Personal Grooming |
  Optical & Eyewear | Wellness D2C
- BFSI: Banking | Small Finance & Payments Banks | Cooperative Banks | NBFC & Consumer Lending |
  Housing Finance | Gold Loans & Microfinance | Life Insurance | General & Health Insurance |
  Asset Management | Broking & Wealth | Fintech & Payments
- Real Estate: Developers (Residential & Mixed-use) | Real Estate Marketplaces & Brokerage |
  Co-living & Flex Workspaces | Malls & Retail Real Estate
- Automotive: Passenger Vehicles | Two & Three Wheelers | Electric Vehicles | Commercial Vehicles |
  Tyres | Lubricants & Batteries | Auto Dealerships | Used Cars & Auto-tech | Mobility & Ride-hailing
- Hospitality: Hotels & Resorts | Global Hotel Chains (India) | Budget & Alternate Stays | Holiday & Leisure |
  Travel & OTAs | Entertainment, Cinemas & Theme Parks
- Airlines & Aviation: Airlines | Airports
- Home improvement: Paints & Waterproofing | Tiles, Sanitaryware & Bath Fittings | Plywood, Laminates &
  Building Products | Pipes & Plumbing | Electricals & Lighting | Wires & Cables | Cement (branded retail) |
  Furniture, Mattresses & Interiors | Home Appliances (AC, Washing Machine, Dishwasher, Kitchen) |
  Windows, Doors & Hardware | Water Purifiers & Water Heaters | Consumer Electronics | Batteries & Inverters
  (Only consumer-facing, retail-branded businesses. Do NOT add B2B manufacturers.)

## How to search (be thorough — the user explicitly wants brands Apollo missed)
Use many angles: "top X companies in India by revenue", "largest regional X chains", listed-company sector
lists (screener.in screens, NSE sector indices), Fortune India 500 / ET 500 / BT 500 lists, cooperative
federations, state-wise leaders (South, West, East, North, NE), private companies via Tofler/Entrackr/Inc42
revenue stories, "crosses ₹500 crore revenue", "₹1,000 crore turnover", D2C brands "FY25 revenue".
Regional champions (e.g. Kerala jewellers, Tamil Nadu textile retailers, Gujarat dairies, Hyderabad
developers) are exactly what Apollo misses.

Work steadily and completely: target as many Qualified rows as genuinely exist in your scope (often
80–200). Quality over padding — every Qualified row must have a real revenue source.
When finished, reply with: counts (Qualified / Rejected), sub-industry breakdown, and any doubts.
