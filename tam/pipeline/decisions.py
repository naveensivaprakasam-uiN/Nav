# Manual ICP review of the original (Apollo-built) TAM rows. name -> (bucket, reason)
# buckets: REMOVE, DOUBT (needs revenue/fit check), DUP (duplicate of another row), ZOCKET (already with Zocket: account list / pipeline / group)
R = {}
def put(bucket, reason, names):
    for n in names.split(';'):
        n = n.strip()
        if n: R[n] = (bucket, reason)

# ---------- REMOVE ----------
put('REMOVE', 'Not B2C – auto components / industrial supplier',
    "CUMI Abrasives India;Lumax Auto Technologies Ltd;Uno Minda;Pricol Limited;Suprajit Engineering Limited;Sona Comstar;Motherson Group;Fiem Industries Limited;TATA AutoComp Systems Ltd;Bosch Limited;Sandhar Technologies Limited;Hero Motors;myTVS (Ki Mobility Solutions Pvt Ltd)")
put('REMOVE', 'Not B2C – electronics contract manufacturer (EMS)',
    "Syrma SGS Technology Limited;Avalon Technologies Limited;Amber Enterprises India Limited;Tata Electronics;Kaynes Technology India Limited;Cyient DLM Limited;Dixon Technologies India Limited;EPACK Durable Limited;PG Electroplast")
put('REMOVE', 'Not B2C – solar manufacturer / power equipment',
    "ReGen Powertech;Rayzon Solar Limited;Gautam Solar Pvt Ltd;Waaree Group;Emmvee Group;RenewSys India Pvt. Ltd.;Goldi Solar Pvt. Ltd.;Tata Power Renewable Energy Limited;Adani Solar;Premier Energies Limited;Vikram Solar;Transrail Lighting Limited;Bharat Bijlee Ltd;Voltamp Transformers Limited;APAR Industries Limited;Genus Power Infrastructures Ltd;TD Power Systems;CG Power and Industrial Solutions Limited;Universal Cables Ltd;Shakti Pumps (I) Ltd.;KOEL Fluid Dynamics;ACE (Action Construction Equipment);OSWAL PUMPS LIMITED")
put('REMOVE', 'Not B2C – steel / metals (excluded)',
    "Gallantt Group;Usha Martin Limited;Pennar Industries Limited;Electrotherm (India) Limited;Bansal Wire Industries;SG Mart;APL Apollo Tubes Ltd.;Jsw Steel Limited.Mumbai;Electrosteel Castings Ltd. - India")
put('REMOVE', 'Not B2C – telecom equipment',
    "HFCL Limited;Tejas Networks;STL - Sterlite Technologies Limited;Vindhya Telelinks Limited;Pace Digitek Limited")
put('REMOVE', 'Not B2C – chemicals / glass / packaging',
    "Shriram Fertilisers & Chemicals;Rain Industries;Asahi India Glass Limited;PGP Glass Ltd.;AGI Greenpac;Hindusthan National Glass & Industries Limited;Godavari Biorefineries Limited")
put('REMOVE', 'Not B2C – ingredients, sugar, commodity or export business',
    "AOV Group;Allana Group;WayCool Foods;Drytech Processes (India) Private Limited;Keva - Fragrances, Flavours & Aroma Ingredients;Oriental Aromatics;Plant Lipids Private Limited;Symega Food Ingredients Ltd.;Synthite Industries Pvt. Ltd;Gujarat Ambuja Exports Limited;Shree Renuka Sugars Limited;Dhampur Bio Organics Ltd.;Dwarikesh Sugar Industries Ltd;DCM Shriram Industries Limited;Uttam Sugar Mills Ltd;BCL Industries Limited;EID Parry India Ltd;Kanan Devan Hills Plantations Company (P) Ltd.;HyFun Foods;Hindustan Foods Limited;SLMG Beverages Pvt Ltd")
put('REMOVE', 'Not B2C – commercial vehicles / tractors / B2B tyres',
    "Ashok Leyland;Isuzu Motors India Pvt Ltd;Solis Yanmar Tractors India;CNH Industrial (India) Private Limitedï¿½;Escorts Kubota Limited;Balkrishna Industries (BKT Tyres)")
put('REMOVE', 'Not B2C – market infrastructure / B2B services',
    "Bombay Stock Exchange Limited;Multi Commodity Exchange of India Ltd.;CDSL (Central Depository Services);Shankara Building Products Ltd;IndiQube;SILA;Tribeca Developers;Star Estate;Wipro Lighting;Sarita Handa")
put('REMOVE', 'Not B2C – prescription (Rx) pharma',
    "Dr. Reddy's Laboratories;Sun Pharmaceuticals;Lupin India;Ipca Laboratories Limited;Adalbert Life Plus Pharma;Charak Pharma")
put('REMOVE', 'Government / PSU',
    "Central Bank of India;Union Bank of India;Bank of Baroda;Bank of India;Canara Bank;Indian Bank;LIC;BOBCARD")
put('REMOVE', 'Excluded by rule (Zepto / Zomato-Blinkit / malls)',
    "Zepto;Zomato;The Phoenix Mills Ltd.")
put('REMOVE', 'Below ₹500 Cr revenue',
    "Clove Dental;Nazeer Foods;Snitch;Bombay Shaving Company;Healthians;Sharp Sight Eye Hospitals;Fernandez Hospital;Desai Brothers Ltd.;Kaff India;Fam;lendingplate;Ambak;NSDL Payments Bank;River;Aditya Birla Real Estate Limited (Formerly Century Textiles);Ashiana Housing Limited;Stanza Living;Housiey;The Golkonda Hotel;The Postcard Hotels;The Umrao Hotels and Resorts;Fariyas Hotels & Resorts;Avadh Utopia Surat;Ananta Spa & Resort;RK Business Group;Lohono Stays;The Hosteller;Abad Group of Hotels")
put('REMOVE', 'Not mass-market B2C – loan DSA / HNI / MSME lender',
    "my money mantra;Finova Capital;Lendingkart Finance Limited;Maybright Ventures")
put('REMOVE', 'Insolvent / distressed',
    "Ansal Properties & Infrastructure Ltd.;Religare Diagnostics")
put('REMOVE', 'Below ₹500 Cr – small regional developer',
    "32ND;KHB;Kumar Properties;Ark Group;Northernsky Properties Pvt Ltd;DASNAC;Akshaya Homes;Express Infrastructure Private Ltd;BBG - BUILDING BLOCKS GROUP;Suncity Projects Pvt. Ltd.;Unishire;Ubber Group;Peram Group;Vistara Group;Dharmadev Infrastructure Limited;Isha Homes (India) Private Limited;Renaatus;Quarkcity India Pvt Limited;ABIL Group;The SHRI Group;Mapsko Group;Tulip Infratech;DRA Homes;Synergy Property Development Services Pvt Ltd;Arun Excello;Appaswamy Real Estates Limited;Krisumi Corporation;Assotech Realty Pvt. Ltd.;VGN Developers;Raheja Developers Ltd.;Kanodia Group;Isprava;Puranik Builders")

# ---------- DUPLICATES ----------
put('DUP', 'Duplicate – same as Go Fashion (India)', "Go Colors - Go Fashion India Ltd.")
put('DUP', 'Duplicate – same company as Credo Brands (Mufti)', "MUFTI;MUFTI Credo Brand Mrkt Pvt Ltd.")
put('DUP', 'Duplicate – brand of Aditya Birla Lifestyle Brands', "Vanheusen")
put('DUP', 'Duplicate – brand of Arvind Fashions', "US Polo Assn India")
put('DUP', 'Duplicate – brand of Sheela Foam', "Sleepwell;Kurlon Enterprise Limited")
put('DUP', 'Duplicate – same as Chitale Group', "Chitale Foods")
put('DUP', 'Duplicate – same as Shree Baidyanath', "Baidyanath Group")
put('DUP', 'Duplicate – same as Capri Global Capital', "Capri Global Housing Finance Ltd.")
put('DUP', 'Duplicate – Reliance General is now IndusInd General', "Reliance General Insurance")
put('DUP', 'Duplicate – SRL is now Agilus Diagnostics', "SRL Diagnostics")
put('DUP', 'Duplicate – same as P N Gadgil Jewellers', "PNG Jewellers")
put('DUP', 'Duplicate – Rajnigandha is DS Group (account list)', "Dharampal Premchand Limited(DPPCL)")
put('DUP', 'Duplicate – Transsion (itel/TECNO) already in TAM', "TECNO Mobile India")

# ---------- ALREADY WITH ZOCKET (account list / pipeline / active / group of those) ----------
put('ZOCKET', 'Group already with Zocket (Aditya Birla – ABFRL in account list)', "Aditya Birla Lifestyle Brands Limited;TMRW House of Brands;W for Woman (TCNS);Reebok Fitness India;Novel Jewels (Aditya Birla Group);Aditya Birla Health Insurance Company Limited;UltraTech Cement;The India Cements Ltd")
put('ZOCKET', 'Already with Zocket – Emami in account list / pipeline', "Emami Limited")
put('ZOCKET', 'Group already with Zocket – Godrej in account list / active', "Godrej Consumer Products Limited;Godrej Enterprises Group;Godrej Properties")
put('ZOCKET', 'Already with Zocket – Duroflex is an active prospect', "Duroflex")
put('ZOCKET', 'Group already with Zocket – Tata in account list', "Tata Motors Limited;Tata Passenger Electric Mobility Ltd;Tata Motors Commercial Vehicles;1mg Technologies;VoltasBeko;Voltas Limited - A TATA Enterprise")
put('ZOCKET', 'Group already with Zocket – Mahindra in account list', "Mahindra Holidays & Resorts (Club Mahindra);Mahindra Lifespace Developers Ltd.;Mahindra Last Mile Mobility;Jawa | Yezdi | BSA Motorcycles")
put('ZOCKET', 'Group already with Zocket – Piramal in account list', "Piramal Realty")
put('ZOCKET', 'Group already with Zocket – Shriram in account list', "Shriram Properties;SHRIRAM GENERAL INSURANCE CO. LTD.;Shree Ram Life Insurance")
put('ZOCKET', 'Group already with Zocket – Landmark (active connection)', "EasyBuy")
put('ZOCKET', 'Group already with Zocket – DS Group in account list', "Catch Spices (DS Group)")
put('ZOCKET', 'Group already with Zocket – HDFC in lists', "HDB Financial Service Limited")
put('ZOCKET', 'Group already with Zocket – Bajaj in account list', "NIRLEP Appliances Limited")
put('ZOCKET', 'Group already with Zocket – JSW / Jindal in lists', "JSW Paints;JSW MG Motor India Pvt Ltd")
put('ZOCKET', 'Group already with Zocket – Hinduja (IndusInd) in lists', "Hinduja Leyland Finance;IndusInd General Insurance")

# ---------- DOUBTFUL (consumer brand, but ₹500 Cr+ not confirmed) ----------
put('DOUBT', 'Consumer brand – revenue may be below ₹500 Cr (Apollo figure unreliable)',
    "BIBA Fashion;Blackberrys Menswear;Modenik Lifestyle;The House of Rare;Colorbar Cosmetics Pvt. Ltd.;Forest Essentials;Lotus Herbals;Medimix (Cholayil);Plix Life;Casio India Co, Pvt Ltd;Intex Technologies (India) Ltd.;Noise India (Wearables);Nobel Hygiene Pvt. Ltd.;Aqualite India;Asian Footwears Pvt Ltd;Crocs India;India's VKC;Lifelong Online;Preethi Kitchen Appliances;D'DECOR HOME FABRICS;ORRA Fine Jewellery;Vummidi Bangaru Jewellers (VBJ);Kisna Diamond Jewellery;Avon Cycles;Steelbird Hi-Tech India Ltd.;BGS Gleneagles;DDRC Agilus Diagnostics;Lifecell International;MediBuddy;Motherhood Hospitals;Paras Health;Vasan Eye Care;Jaypee Hospital;Indira IVF;Sahyadri Hospitals;SBM Bank (India);Bandhan AMC;Augmont | Gold For All;Clix Capital Services Pvt Ltd;CoinDCX (Primestack Pvt Ltd);Edelweiss Broking;MARGADARSI CHIT FUND PRIVATE LIMITED;Navi Mutual Fund;Nirmal Bang;Stashfin (Akara Capital);Truhome Finance Limited;Raheja QBE General Insurance;Anand Rathi Wealth Limited;Halonix Technologies Pvt. Limited;HPL Electric & Power Ltd;SPACEWOOD Furnishers Pvt Ltd;Onida;Elica PB Whirlpool Kitchen Appliances Private Limited;Kamdhenu Limited;Sheenlac Paints Limited;TOTO India Industries Pvt. Ltd.;Beetel;Fenesta Windows;KALS Group of Companies;Paper Boat (Hector Beverages);Dairy Day;GRB Dairy Foods PVT. LTD.,;Keventer;Nova Dairy;Sunfresh Agro Industries P. Ltd. (Prabhat Dairy);VRS Foods Limited;Ghodawat Consumer;Danone India;Del Monte Foods Private Limited;Tirupati Group;Impresario Handmade Restaurants;Lite Bite Foods Pvt Ltd;Sagar Ratna Restaurants Pvt. Ltd;Unibic Foods India Pvt Ltd;Goldiee Group;JK Masale;Modi Naturals;Agro Tech Foods Limited;Roseate Hotels & Resorts;Sarovar Hotels;GreenPark Hotels and Resorts;Treebo Hotels;FabHotels;BGauss Electric Vehicles (RR Kabel);Lahori Zeera;Simpolo Tiles and Bathware;Varmora Tiles Bathware;Cafe Coffee Day;Sathya Agencies - India;Kohinoor Group Pune;Chandak Group;Bhumika Realty;Hindva;Ashwin Sheth Group;Bhartiya Urban;Merlin Group;Geras Developments;DB Realty;Gaurs Group;Dynamix Group;Kanakia Paris;Rohan Builders India;JP Infra;Ozone Group;Raheja Group Mumbai;Ambience Group;ELAN GROUP;Marathon Realty;Omkar Realtors & Developers Pvt Ltd.;PS Group;Eros Group;Chaithanya Projects Pvt Ltd;Century Real Estate;Alliance Group;Dosti Realty;Embassy Group;Embassy Developments Limited (formerly Equinox India Developments Limited);Square Yards;NoBroker.com;Housing.com;Smartworld Developers;Experion Developers;BPTP Ltd.;The Wadhwa Group;Moneyview;Ramco Industries Ltd.;Wonder Cement Ltd.")
put('DUP', 'Duplicate – Conrad is a Hilton brand (Hilton India already in TAM)', "Conrad (Hilton)")
put('REMOVE', 'Foreign chain with negligible India presence', "Anantara (Minor Hotels)")
put('DUP', 'Duplicate – same group as JK Tyre & Industries', "JK Organisation")
