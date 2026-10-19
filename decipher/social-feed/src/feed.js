(function(){
'use strict';
document.body.classList.add('cf-page');
if(document.querySelector('#comment_Initialize')){
 const start=document.querySelector('#btn_continue');
 if(start && !start.disabled)start.click();
 return;
}
const root=document.querySelector('.question.cf-feed');
if(!root)return;
const native=root.querySelector('.answers'),form=root.closest('form'),next=form&&form.querySelector('#btn_continue');
const config=document.querySelector('.cf-config');
if(!native||!next||!config)return;
const groups=new Map();
native.querySelectorAll('input[type=radio]').forEach(i=>{if(!groups.has(i.name))groups.set(i.name,[]);groups.get(i.name).push(i)});
const rows=Array.from(groups.values()).map(inputs=>{const tr=inputs[0].closest('tr');const legend=tr&&tr.querySelector('.row-legend');const codes={};inputs.forEach(input=>{const headers=input.closest('td')?.getAttribute('headers')||'';['c1','c2','c3'].forEach(code=>{if(headers.split(/\s+/).some(h=>h.endsWith('_'+code)))codes[code]=input})});return {inputs,legend,codes,card:null,since:null,last:0,touch:null};});
if(!rows.length||rows.some(r=>!r.legend||Object.keys(r.codes).length!==3))return;
const feed=Number(config.dataset.feed),count=Number(config.dataset.feeds),version=config.dataset.version;
const storageKey='commonplace-v1:'+location.pathname+':'+config.dataset.session+':'+feed+':'+version;
let restored=null;try{restored=JSON.parse(sessionStorage.getItem(storageKey)||'null')}catch(e){}
let submitting=false;
function selected(r){return ['c1','c2','c3'].find(c=>r.codes[c].checked)||'c1'}
function choose(r,c){if(!r.codes[c].checked)r.codes[c].click();render(r);save()}
function save(){try{sessionStorage.setItem(storageKey,JSON.stringify(rows.map(r=>selected(r))))}catch(e){}}
function render(r){if(!r.card)return;const yes=selected(r)==='c3';const b=r.card.querySelector('.cf-like');b.setAttribute('aria-pressed',String(yes));b.innerHTML=(yes?'♥':'♡')+' &nbsp;'+(yes?'Liked':'Like');const total=rows.filter(r=>selected(r)==='c3').length;ui.querySelector('.cf-count').textContent=total+' liked in this feed';}
const ui=document.createElement('section');ui.className='cf-layout';ui.innerHTML='<div class="cf-instructions"><div class="cf-round">Feed '+feed+' of '+count+'</div><h2>Which posts stand out to you?</h2><p>Scroll and like any posts that stand out. Double-tap an image to like it; tap Like again to undo. You may continue without liking any posts.</p><div class="cf-count cf-sr" aria-live="polite"></div></div><div class="cf-stream"></div>';
root.appendChild(ui);const stream=ui.querySelector('.cf-stream');
rows.forEach((r,i)=>{const card=document.createElement('article');r.card=card;card.className='cf-card';card.dataset.item=String(i+1);card.innerHTML=r.legend.innerHTML+'<div class="cf-actions"><button type="button" class="cf-like" aria-label="Like post '+(i+1)+'" aria-pressed="false">♡ Like</button><span class="cf-post-id">'+String(i+1).padStart(2,'0')+' / '+rows.length+'</span></div>';stream.appendChild(card);if(restored&&['c1','c2','c3'].includes(restored[i]))r.codes[restored[i]].click();else if(!r.inputs.some(x=>x.checked))r.codes.c1.click();
function toggle(){const now=performance.now();if(submitting||now-r.last<420)return;r.last=now;choose(r,selected(r)==='c3'?'c2':'c3')}
card.querySelector('.cf-like').addEventListener('click',e=>{if(e.detail>1)return;toggle()});
const art=card.querySelector('.cf-art');if(art){art.addEventListener('dblclick',e=>{e.preventDefault();toggle()});art.addEventListener('pointerup',e=>{if(e.pointerType!=='touch')return;const now=performance.now();const t=r.touch;if(t&&now-t.time<340&&Math.hypot(e.clientX-t.x,e.clientY-t.y)<25){toggle();r.touch=null}else r.touch={time:now,x:e.clientX,y:e.clientY}});art.addEventListener('pointercancel',()=>r.touch=null)}render(r);
});
const end=document.createElement('div');end.className='cf-end';end.innerHTML='<button type="button" class="cf-next">Continue</button><p class="cf-status" role="status"></p>';stream.appendChild(end);
const button=end.querySelector('button');
function submit(){if(submitting)return;submitting=true;save();button.disabled=true;end.querySelector('.cf-status').textContent='Saving…';next.click()}
button.addEventListener('click',submit);
form.addEventListener('submit',()=>{submitting=true;save();button.disabled=true});
window.addEventListener('pagehide',save);window.addEventListener('pageshow',e=>{if(e.persisted){submitting=false;button.disabled=false;end.querySelector('.cf-status').textContent='Your selections are restored.'}});
// Exposure is conservative and is NOT attention: full image loaded, >=50% card
// visible continuously for >=1000 ms in a visible document. Explicit Like also counts.
setInterval(()=>{const now=performance.now();rows.forEach(r=>{if(selected(r)!=='c1'||document.visibilityState!=='visible'){r.since=null;return}const rect=r.card.getBoundingClientRect();const visible=Math.max(0,Math.min(rect.bottom,innerHeight)-Math.max(rect.top,0));const horizontal=Math.max(0,Math.min(rect.right,innerWidth)-Math.max(rect.left,0));const ratio=visible*horizontal/(rect.width*rect.height);if(ratio>=.5){if(r.since===null)r.since=now;if(now-r.since>=1000)choose(r,'c2')}else r.since=null})},100);
native.classList.add('cf-native-hidden');root.querySelector('.question-text')?.classList.add('cf-native-hidden');root.querySelector('.comment')?.classList.add('cf-native-hidden');next.classList.add('cf-native-hidden');save();
})();
