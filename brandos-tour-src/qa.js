const {chromium}=require('playwright');const fs=require('fs');
const [file,out]=process.argv.slice(2);
(async()=>{const b=await chromium.launch();const errs=[];
 async function pg(w,h){const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
  p.on('console',m=>{if(m.type()==='error'||m.type()==='warning')errs.push(w+' '+m.text())});p.on('pageerror',e=>errs.push(w+' PAGEERR '+e.message));
  p.on('requestfailed',r=>errs.push('REQFAIL '+r.url().slice(0,80)));p.on('request',r=>{if(!r.url().startsWith('file:')&&!r.url().startsWith('data:'))errs.push('EXTERNAL '+r.url())});
  await p.goto('file://'+file);await p.waitForTimeout(800);return p;}
 const curPos=p=>p.evaluate(()=>{const s=document.getElementById('stage').getBoundingClientRect();const c=document.getElementById('cur');return [s.x+parseFloat(c.style.left),s.y+parseFloat(c.style.top)]});
 const p=await pg(1500,900);
 await p.screenshot({path:`${out}/1500_start.png`});
 const steps=await p.evaluate(()=>STEPS.length);const cur=[];
 await p.click('#startBtn');
 for(let n=0;n<steps;n++){
  await p.evaluate(n=>BrandOSTour.go(n),n);await p.waitForTimeout(1300);
  const tag=String(n+1).padStart(2,'0');
  const hasH=await p.evaluate(n=>!!STEPS[n].h,n);
  await p.screenshot({path:`${out}/1500_${tag}${hasH?'a':''}.png`});
  cur.push({n:tag,beat:1,xy:await curPos(p)});
  if(hasH){await p.waitForTimeout(3000);await p.screenshot({path:`${out}/1500_${tag}b.png`});cur.push({n:tag,beat:2,xy:await curPos(p)});}
 }
 await p.click('#next');await p.waitForTimeout(1000);await p.screenshot({path:`${out}/1500_end.png`});
 for(const [w,h] of [[400,760],[768,900]]){const q=await pg(w,h);await q.screenshot({path:`${out}/${w}_start.png`});
  await q.click('#startBtn');await q.waitForTimeout(1300);await q.screenshot({path:`${out}/${w}_01.png`});
  await q.evaluate(()=>BrandOSTour.go(9));await q.waitForTimeout(1300);await q.screenshot({path:`${out}/${w}_10.png`});
  await q.evaluate(()=>BrandOSTour.go(STEPS.length));await q.waitForTimeout(900);await q.screenshot({path:`${out}/${w}_end.png`});
  const sw=await q.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]);if(sw[0]>sw[1])errs.push(w+' HSCROLL '+sw);}
 fs.writeFileSync(`${out}/cursor.json`,JSON.stringify(cur));fs.writeFileSync(`${out}/errors.txt`,errs.join('\n'));
 console.log('errors:',errs.length);errs.slice(0,20).forEach(e=>console.log(e));await b.close();})();
