const {chromium}=require('playwright');const fs=require('fs');
const B=process.argv[2];const ids=process.argv.slice(3);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720},deviceScaleFactor:2});
p.on('pageerror',e=>console.log('ERR',e.message));p.on('console',m=>{if(m.type()==='error')console.log('CERR',m.text())});
const hits=fs.existsSync(B+'/hits.json')?JSON.parse(fs.readFileSync(B+'/hits.json')):{};
fs.mkdirSync(B+'/png',{recursive:true});
for(const id of ids){await p.goto('file://'+B+'/screens.html?s='+id);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
 hits[id]=await p.evaluate(()=>HITS());await p.screenshot({path:`${B}/png/${id}.png`});}
fs.writeFileSync(B+'/hits.json',JSON.stringify(hits,null,1));await b.close();})();
