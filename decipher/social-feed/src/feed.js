(function(){
'use strict';
document.body.classList.add('cf-page');
if(document.querySelector('#comment_Initialize')){
 const start=document.querySelector('#btn_continue');if(start&&!start.disabled)start.click();return;
}
const root=document.querySelector('.question.cf-feed');
if(!root||root.dataset.enhanced)return;
const native=root.querySelector('.answers'),form=root.closest('form'),next=form&&form.querySelector('#btn_continue');
const config=document.querySelector('.cf-config'),timing=document.querySelector('.question.cf-timing');
if(!native||!next||!config||!timing)return;
const groups=new Map();
native.querySelectorAll('input[type=radio]').forEach(i=>{if(!groups.has(i.name))groups.set(i.name,[]);groups.get(i.name).push(i)});
function column(input,code){return (input.closest('td')?.getAttribute('headers')||'').split(/\s+/).some(h=>h.endsWith('_'+code))}
const timeRows=Array.from(timing.querySelectorAll('tr')).filter(tr=>tr.querySelector('input[type=text],input[type=number]'));
const rows=Array.from(groups.values()).map((inputs,index)=>{
 const tr=inputs[0].closest('tr'),legend=tr&&tr.querySelector('.row-legend'),codes={};
 inputs.forEach(input=>['c1','c2','c3'].forEach(code=>{if(column(input,code))codes[code]=input}));
 const timeInputs=Array.from(timeRows[index]?.querySelectorAll('input')||[]);
 return {inputs,legend,codes,ms:timeInputs.find(i=>column(i,'ms')),state:timeInputs.find(i=>column(i,'state')),card:null,touch:null,lastGesture:-Infinity};
});
if(!rows.length||rows.some(r=>!r.legend||Object.keys(r.codes).length!==3||!r.ms||!r.state))return;
root.dataset.enhanced='true';
const feed=Number(config.dataset.feed),count=Number(config.dataset.feeds),version=config.dataset.version;
const storageKey='adfeed-v2:'+location.pathname+':'+config.dataset.session+':'+feed+':'+version;
const clock=window.SocialFeedTiming,supported=!!(clock&&window.performance&&typeof performance.now==='function'&&typeof document.hasFocus==='function'&&'visibilityState' in document&&typeof IntersectionObserver==='function');
let restored=null,storageOK=true;
try{const value=JSON.parse(sessionStorage.getItem(storageKey)||'null');if(value&&value.schema===2&&value.items.length===rows.length)restored=value.items}catch(e){storageOK=false}
const navigation=window.performance?.getEntriesByType?.('navigation')[0]?.type;
const gestureNow=()=>window.performance?.now?performance.now():Date.now();
const lostCache=!restored&&(navigation==='reload'||navigation==='back_forward');
let submitting=false,paused=false,lastSave=0;
function selected(r){return ['c1','c2','c3'].find(c=>r.codes[c].checked)||'c1'}
function choose(r,c){if(!r.codes[c].checked)r.codes[c].click();render(r);save()}
function sync(){ui.dataset.pageVisible=document.visibilityState;ui.dataset.pageFocused=String(typeof document.hasFocus==='function'&&document.hasFocus());rows.forEach(r=>{r.ms.value=supported?String(Math.floor(r.meter.total)):'-1';r.state.value=supported?String(r.meter.state()):'4'})}
function save(){
 sync();
 try{sessionStorage.setItem(storageKey,JSON.stringify({schema:2,items:rows.map(r=>({like:selected(r),ms:r.meter.total,partial:r.meter.partial}))}))}
 catch(e){storageOK=false;rows.forEach(r=>r.meter.partial=true);sync()}
}
function render(r){if(!r.card)return;const yes=selected(r)==='c3',b=r.card.querySelector('.cf-like');b.setAttribute('aria-pressed',String(yes));b.innerHTML=(yes?'♥':'♡')+' &nbsp;'+(yes?'Liked':'Like')}
const ui=document.createElement('section');ui.className='cf-layout';ui.innerHTML='<div class="cf-instructions"><div class="cf-round">Feed '+feed+' of '+count+'</div><h2>Which posts stand out to you?</h2><p>Scroll and like any posts that stand out. Double-tap an image to like it; tap Like again to undo. You may continue without liking any posts.</p></div><div class="cf-stream"></div>';
root.appendChild(ui);const stream=ui.querySelector('.cf-stream');
rows.forEach((r,i)=>{
 const cached=restored?.[i],nativeMs=Number(r.ms.value);
 const total=cached&&Number.isFinite(cached.ms)&&cached.ms>=0?cached.ms:Math.max(0,nativeMs||0);
 r.meter=clock.meter(total,!!cached?.partial||!storageOK||lostCache||Number(r.state.value)===3);
 const card=document.createElement('article');r.card=card;card.className='cf-card';card.dataset.item=String(i+1);
 card.innerHTML=r.legend.innerHTML+'<div class="cf-actions"><button type="button" class="cf-like" aria-label="Like post '+(i+1)+'" aria-pressed="false">♡ Like</button></div>';stream.appendChild(card);
 if(cached&&['c1','c2','c3'].includes(cached.like))r.codes[cached.like].click();else if(!r.inputs.some(x=>x.checked))r.codes.c1.click();
 function toggle(){if(submitting)return;choose(r,selected(r)==='c3'?(r.meter.total>=1?'c2':'c1'):'c3')}
 // A button click toggles immediately; subsequent click events in the same multi-click gesture do not.
 card.querySelector('.cf-like').addEventListener('click',e=>{if(e.detail<=1)toggle()});
 function imageGesture(){const now=gestureNow();if(now-r.lastGesture<420)return;r.lastGesture=now;toggle()}
 const art=card.querySelector('.cf-art');if(art){art.addEventListener('dblclick',e=>{e.preventDefault();imageGesture()});art.addEventListener('pointerup',e=>{if(e.pointerType!=='touch')return;const now=gestureNow(),t=r.touch;if(t&&now-t.time<340&&Math.hypot(e.clientX-t.x,e.clientY-t.y)<25){imageGesture();r.touch=null}else r.touch={time:now,x:e.clientX,y:e.clientY}});art.addEventListener('pointercancel',()=>r.touch=null)}
 render(r);
});
const observed=new Map(rows.map(r=>[r.card,r]));
const observer=supported?new IntersectionObserver(entries=>{entries.forEach(entry=>{const r=observed.get(entry.target);if(r)r.intersects=entry.isIntersecting})},{threshold:0}):null;
if(observer)rows.forEach(r=>observer.observe(r.card));
const end=document.createElement('div');end.className='cf-end';end.innerHTML='<button type="button" class="cf-next">Continue</button><p class="cf-status" role="status"></p>';stream.appendChild(end);const button=end.querySelector('button');
function active(){return supported&&!submitting&&!paused&&document.visibilityState==='visible'&&document.hasFocus()}
function sample(now){
 const enabled=active();
 rows.forEach(r=>{const eligible=enabled&&r.intersects===true&&clock.fraction(r.card.getBoundingClientRect(),innerWidth,innerHeight)>=.5;
  r.meter.sample(now,eligible);
  if(r.meter.total>=1&&selected(r)==='c1'){r.codes.c2.click();render(r)}
 });
}
function flush(){if(supported)sample(performance.now());save()}
function pause(){flush();paused=true;rows.forEach(r=>r.meter.pause())}
function resume(){paused=false;rows.forEach(r=>r.meter.pause());if(supported)sample(performance.now())}
function submit(){if(submitting)return;flush();submitting=true;rows.forEach(r=>r.meter.pause());button.disabled=true;end.querySelector('.cf-status').textContent='Saving…';next.click()}
button.addEventListener('click',submit);
form.addEventListener('submit',()=>{if(!submitting)flush();submitting=true;button.disabled=true});
window.addEventListener('blur',pause);window.addEventListener('focus',resume);
document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')pause();else resume()});
window.addEventListener('pagehide',pause);window.addEventListener('beforeunload',flush);
window.addEventListener('pageshow',e=>{if(e.persisted){submitting=false;button.disabled=false;end.querySelector('.cf-status').textContent='';resume()}});
function frame(now){if(!submitting){sample(now);if(now-lastSave>=250){save();lastSave=now}}requestAnimationFrame(frame)}
native.classList.add('cf-native-hidden');timing.classList.add('cf-native-hidden');root.querySelector('.question-text')?.classList.add('cf-native-hidden');root.querySelector('.comment')?.classList.add('cf-native-hidden');next.classList.add('cf-native-hidden');
save();if(supported)requestAnimationFrame(frame);
})();
