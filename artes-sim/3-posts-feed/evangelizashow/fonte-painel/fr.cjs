const { chromium } = require('playwright');(async()=>{
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(2500);await p.evaluate(()=>window.ready);
const n=Math.round(await p.evaluate(()=>TEND)*30);const el=await p.$('canvas');
for(let i=0;i<n;i++){await p.evaluate(t=>render(t),i/30);await el.screenshot({path:`${process.argv[3]}/f_${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close();})();
