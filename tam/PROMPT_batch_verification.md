# Prompt: verify a Tensai calling batch (zero-error standard)

Copy everything below the line into a new Claude chat. Attach:
1. the batch file (one batch at a time),
2. Zocket's exclusion lists: client list, pipeline, account list, active connections,
3. (optional) last verified file `Tensai_Batches_1-3_Reverified.xlsx` – re-use its sourced figures, but re-check any row with no link.

---

You are verifying a list of Indian companies before an external cold-calling team (Tensai) calls them. Tensai is paid per demo booked, so every wrong account costs us money and trust. **Zero errors. Never answer from memory. Every revenue number must come from a web search or page you actually opened in this chat, with the link.**

## Who Zocket sells to (the ICP)
Zocket sells an AI brand-marketing platform (Brand Brain + creative, paid-media and consumer-insight agents) to consumer brands. A company is ICP only if ALL of these are true:
1. **Consumer-facing (B2C):** it sells its own branded products/services to consumers – retail chains, D2C brands, FMCG, jewellery, apparel, electronics, consumer finance/insurance/broking, hospitals/diagnostics, real-estate developers selling homes, hotels, QSR, consumer apps, etc.
2. **Revenue ≥ ₹500 Cr** in the latest reported year (FY26 or FY25; FY24 acceptable; FY22–FY23 only if nothing newer exists – mark it "older"). Use the Indian operating entity.
   - Banks/NBFCs: total income. Insurers: gross written / gross direct premium. Real estate: revenue from operations – **never sales bookings**.
3. **India-led:** Indian HQ, or an Indian arm of a foreign brand that runs its own India marketing (India marketing head, India campaigns). Pure management-fee entities, back offices, captive centres and franchise-only presence are NOT ICP.

## Always REMOVE (even if revenue is huge)
- B2B / manufacturers / exporters / contract manufacturers / ingredient, sugar, commodity, chemicals, glass, packaging / auto components / EMS / solar & power equipment / telecom equipment / steel & TMT / cement-industrial / tractors & commercial vehicles / B2B tyres / market infrastructure (exchanges, depositories) / B2B services / distributors.
- Prescription (Rx) pharma and medical devices (OTC/consumer-health brands are fine).
- Government, PSU, PSU-controlled JVs (e.g. IndiaFirst Life = Bank of Baroda majority; Star Union Dai-ichi = Bank of India/Union Bank), co-operative societies run by government, trusts, NGOs.
- Flipkart group (Myntra, Cleartrip, Shopsy, PhonePe, super.money), Amazon, Zepto, Blinkit/Zomato.
- Malls / mall operators, airports, car dealers (the carmaker runs the advertising).
- Insolvent or defunct companies.
- HNI-only wealth managers, MSME/business lenders, loan DSAs.

## Already with Zocket → mark "Don't call" (not ICP-wrong, but must not be cold-called)
Check every company against the attached client list, pipeline, account list and active connections:
- match on name variants, short names (e.g. "IDFC" = IDFC FIRST Bank), brand names, and website domain;
- **group rule:** if the parent company or a subsidiary is on those lists → "Don't call". **Sister companies are allowed** (e.g. CEAT is fine even though Raychem RPG is listed).
- Watch for false matches: Indigo Paints ≠ IndiGo airline, Nippon Paint ≠ Nippon India MF, Shalimar Paints ≠ Shalimar Group (food), Landmark Cars ≠ Landmark Group, Y-Axis ≠ Axis Bank.

## Duplicates
One company = one row. Same company under two names (Go Colors / Go Fashion), a brand of another listed company (Sleepwell → Sheela Foam, Vanheusen → Aditya Birla Lifestyle), or a rename (Reliance General → IndusInd General) → keep one, mark the rest "Duplicate of X".

## How to verify revenue (in this order)
1. Listed company → screener.in company page (consolidated), or annual report.
2. Rating rationale: CRISIL, ICRA, CARE, Acuité, India Ratings, Infomerics, Brickwork.
3. Filings data: Tofler / thecompanycheck / Inc42 Datalabs / Entrackr (state if it is a revenue band – use the lower bound).
4. Reputable news quoting filings (ET, Business Standard, Mint, Moneycontrol, PTI, Reuters).
**Never use:** Apollo, ZoomInfo, LinkedIn, Owler, Tracxn-only estimates, company "targets" or "aims".
If no figure can be found with a link → do NOT guess. Mark **"Needs Zocket's call – no public figure"** (for clearly large brands) or **Remove – "No verifiable revenue figure"** (for everything else).
**Removals need proof too:** "below ₹500 Cr" must have a sourced figure. (Lesson: Snitch was wrongly removed from memory – its FY25 was ₹498–520 Cr and FY26 ~₹900 Cr.)

## How to verify B2C
Open the company's own website. Confirm it sells consumer products/services under its own brand. One line of evidence, e.g. "Yes – 150 retail stores + D2C site" or "No – exports meat & medical devices to businesses".
(Lessons: AOV Group looked like a food brand in Apollo but is a B2B exporter; Nazeer Foods showed $169M in Apollo but is a ~₹10 Cr restaurant chain.)

## Zocket-approved exceptions
- Clove Dental: KEEP (₹450 Cr FY26, projected ₹600 Cr, ~200 live ads).
- Near-threshold rule (only if Zocket approves case by case): ₹400–500 Cr latest revenue + clear growth + heavy live advertising → mark "Needs Zocket's call", never auto-keep.

## Process (do it batch by batch, row by row)
1. List every row of the batch. Do not skip any.
2. For each row run: Don't-call check → duplicate check → hard-remove rules → B2C website check → revenue search.
3. Work in chunks of ~25 rows. After each chunk, show the results table and continue.
4. At the end run a self-audit and fix anything that fails:
   - every KEEP has a clickable source link and revenue ≥ ₹500 Cr (FY22 or later);
   - no KEEP is B2B, government, dealer, mall, excluded group or on Zocket's lists;
   - every REMOVE for revenue has a sourced figure (or says "No verifiable revenue figure" after a real search);
   - no duplicates by name or website domain.

## Output (Excel-ready table, one row per company, same order as the batch)
| Batch | Company | Website | Status | Revenue (₹ Cr) | Revenue year | Source link | B2C evidence | Reason |

Status must be exactly one of:
- **Verified – OK to call**
- **Don't call – already with Zocket** (say which list/group)
- **Remove – not ICP** (exact reason: not B2C / below ₹500 Cr with figure / government / dealer / mall / excluded group / no verifiable revenue)
- **Remove – duplicate of X**
- **Needs Zocket's call** (say exactly what is missing)

Finish with a summary: counts per status, the list of "Needs Zocket's call" rows, and any row you are less than certain about.
