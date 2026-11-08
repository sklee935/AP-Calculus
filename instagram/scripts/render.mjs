import {chromium} from 'playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createHash} from 'node:crypto';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const args=process.argv.slice(2);const checkOnly=args.includes('--check-only');
const selection=args.includes('--lessons')?args[args.indexOf('--lessons')+1]:'all';
const out=path.join(root,'instagram','exports');
const names=(await fs.readdir(out)).filter(n=>/^L\d{2}$/.test(n)).sort().filter(n=>selection==='all'||selection.split(',').includes(n));
if(selection!=='all'&&[...new Set(selection.split(','))].some(id=>!names.includes(id)))throw new Error('Unknown lesson selection: '+selection);
if(!names.length)throw new Error('No generated lessons. Run python instagram/scripts/build.py first.');
const browser=await chromium.launch({headless:true});const page=await browser.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
const reports=[];
const sha=b=>createHash('sha256').update(b).digest('hex');
const cssHash=sha(await fs.readFile(path.join(root,'instagram/templates/card.css')));
try{
for(const id of names){
 await page.goto(pathToFileURL(path.join(out,id,'lesson.html')).href,{waitUntil:'load'});
 await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(im=>im.decode()));});
 const sourceHash=sha(await fs.readFile(path.join(root,'instagram/lessons',id+'.json')));
 if(await page.locator('meta[name="lesson-source-sha256"]').getAttribute('content')!==sourceHash)throw new Error(id+': stale HTML; rebuild before rendering');
 const problems=await page.evaluate(()=>{
  const bad=[];const cards=[...document.querySelectorAll('.card')];
  if(cards.length!==8)bad.push('Expected 8 cards');
  if(![...document.fonts].some(f=>f.family==='TeachingNoto'&&f.status==='loaded'))bad.push('CJK font did not load');
  for(const [i,card] of cards.entries()){
   const c=card.getBoundingClientRect();const content=card.querySelector('.card-content').getBoundingClientRect();
   if(c.width!==1080||c.height!==1350)bad.push(`card ${i+1}: wrong dimensions`);
   for(const el of card.querySelectorAll('h1,h2,.explanation p,.formula,.graph,.values-table')){
    const r=el.getBoundingClientRect();
    if(r.left<c.left+79||r.right>c.right-79)bad.push(`card ${i+1}: horizontal bounds ${el.tagName}`);
    if(r.top<content.top-.5||r.bottom>content.bottom+.5)bad.push(`card ${i+1}: vertical overflow ${el.className||el.tagName}`);
    if(el.matches('.explanation p,.values-table')&&parseFloat(getComputedStyle(el).fontSize)<40)bad.push(`card ${i+1}: prose/table too small`);
    if(el.matches('.formula,.graph')&&Math.min(r.width/Number(el.dataset.naturalWidth),r.height/Number(el.dataset.naturalHeight))*Number(el.dataset.baseFont)<40)bad.push(`card ${i+1}: formula/graph labels too small`);
   }
   if(card.querySelectorAll('.explanation [lang]').length!==2)bad.push(`card ${i+1}: missing language`);
  }return bad;
 });
 if(problems.length)throw new Error(id+'\n'+problems.join('\n'));
 if(!checkOnly){for(let i=0;i<8;i++)await page.locator('.card').nth(i).screenshot({path:path.join(out,id,`${String(i+1).padStart(2,'0')}.png`),animations:'disabled'});}
 const manifest={id,cards:8,dimensions:[1080,1350],languages:['en','ko'],overflow:false,minimumProsePx:44,source_sha256:sourceHash,css_sha256:cssHash};
 if(!checkOnly){manifest.png_sha256={};for(let i=1;i<=8;i++){const name=String(i).padStart(2,'0')+'.png';manifest.png_sha256[name]=sha(await fs.readFile(path.join(out,id,name)));}await fs.writeFile(path.join(out,id,'manifest.json'),JSON.stringify(manifest,null,2)+'\n');}
 reports.push(manifest);
 console.log(id,checkOnly?'layout verified':'8 PNGs rendered and layout verified');
}
}finally{await browser.close();}
if(!checkOnly)await fs.writeFile(path.join(out,'render-report.json'),JSON.stringify({renderer:'Playwright Chromium',lessons:reports},null,2)+'\n');
