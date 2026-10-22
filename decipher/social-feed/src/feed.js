(function(){
'use strict';
if(window.QuestraTheme&&!window.QuestraTheme.canEnhance())return;
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
 return {inputs,legend,codes,ms:timeInputs.find(i=>column(i,'ms')),state:timeInputs.find(i=>column(i,'state')),anyms:timeInputs.find(i=>column(i,'anyms')),halfms:timeInputs.find(i=>column(i,'halfms')),exposurestate:timeInputs.find(i=>column(i,'exposurestate')),card:null,touch:null,lastGesture:-Infinity,lastButton:-Infinity};
});
if(!rows.length||rows.some(r=>!r.legend||Object.keys(r.codes).length!==3||!r.ms||!r.state||!r.anyms||!r.halfms||!r.exposurestate))return;

const feed=Number(config.dataset.feed),count=Number(config.dataset.feeds),version=config.dataset.version;
const storageKey='adfeed-exposure-v1:'+location.pathname+':'+config.dataset.session+':'+feed+':'+version;
const clock=window.SocialFeedTiming,supported=!!(clock&&window.performance&&typeof performance.now==='function'&&typeof document.hasFocus==='function'&&'visibilityState' in document&&typeof IntersectionObserver==='function');
let restored=null,storageOK=true;
try{const value=JSON.parse(sessionStorage.getItem(storageKey)||'null');if(value&&value.schema===6&&value.items.length===rows.length)restored=value.items}catch(e){storageOK=false}
const navigation=window.performance?.getEntriesByType?.('navigation')[0]?.type;
const gestureNow=()=>window.performance?.now?performance.now():Date.now();
const lostCache=!restored&&(navigation==='reload'||navigation==='back_forward');
let submitting=false,paused=false,lastSave=0;
function selected(r){return ['c1','c2','c3'].find(c=>r.codes[c].checked)||'c1'}
function choose(r,c){if(!r.codes[c].checked)r.codes[c].click();render(r);save()}
function sync(){ui.dataset.pageVisible=document.visibilityState;ui.dataset.pageFocused=String(typeof document.hasFocus==='function'&&document.hasFocus());rows.forEach(r=>{r.ms.value=supported?String(Math.floor(r.meter.total)):'-1';r.state.value=supported?String(r.meter.state()):'4';r.anyms.value=supported?String(Math.floor(r.anyMeter.total)):'-1';r.halfms.value=supported?String(Math.floor(r.halfMeter.total)):'-1';r.exposurestate.value=supported?String(r.anyMeter.partial||r.halfMeter.partial?3:(r.anyMeter.total>=1?2:1)):'4'})}
function save(){
 sync();
 try{sessionStorage.setItem(storageKey,JSON.stringify({schema:6,items:rows.map(r=>({like:selected(r),ms:r.meter.total,partial:r.meter.partial,anyms:r.anyMeter.total,halfms:r.halfMeter.total,exposurepartial:r.anyMeter.partial||r.halfMeter.partial}))}))}
 catch(e){storageOK=false;rows.forEach(r=>{r.meter.partial=true;r.anyMeter.partial=true;r.halfMeter.partial=true});sync()}
}
const thumb='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7.5 10.5v10H4a1 1 0 0 1-1-1v-8a1 1 0 0 1 1-1h3.5Zm0 0L12 3c.4-.7 1.4-.7 1.8 0 .7 1.3.5 3.2-.1 5H19a2 2 0 0 1 2 2.4l-1.5 8.5a2 2 0 0 1-2 1.6h-10" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>';
function render(r){if(!r.card)return;const yes=selected(r)==='c3',b=r.card.querySelector('.cf-like');b.setAttribute('aria-pressed',String(yes));b.innerHTML=thumb+'<span>'+(yes?'Liked':'Like')+'</span>'}
const ui=document.createElement('section');ui.className='cf-layout';ui.innerHTML='<div class="cf-stream"></div>';
root.appendChild(ui);const stream=ui.querySelector('.cf-stream');
rows.forEach((r,i)=>{
 const cached=restored?.[i],nativeMs=Number(r.ms.value);
 const total=cached&&Number.isFinite(cached.ms)&&cached.ms>=0?cached.ms:Math.max(0,nativeMs||0);
 r.meter=clock.meter(total,!!cached?.partial||!storageOK||lostCache||Number(r.state.value)===3);
 const restoredTotal=key=>Math.max(0,Number(r[key].value)||0,Number(cached?.[key])||0);
 const partial=!!cached?.exposurepartial||!storageOK||lostCache||Number(r.exposurestate.value)===3;
 r.anyMeter=clock.meter(restoredTotal('anyms'),partial);r.halfMeter=clock.meter(restoredTotal('halfms'),partial);
 const card=document.createElement('article');r.card=card;card.className='cf-card';card.dataset.item=String(i+1);
 card.innerHTML=r.legend.innerHTML+'<div class="cf-actions"><button type="button" class="cf-like" aria-label="Like post '+(i+1)+'" aria-pressed="false">♡ Like</button></div>';stream.appendChild(card);
 card.querySelectorAll('img[data-src]').forEach(photo=>{photo.loading=i<2?'eager':'lazy';photo.decoding='async';if(i===0)photo.fetchPriority='high';photo.src=photo.dataset.src;});
 if(cached&&['c1','c2','c3'].includes(cached.like))r.codes[cached.like].click();else if(!r.inputs.some(x=>x.checked))r.codes.c1.click();
 function toggle(){if(submitting)return;choose(r,selected(r)==='c3'?(r.meter.total>=1?'c2':'c1'):'c3')}
 // A button click toggles immediately; subsequent click events in the same multi-click gesture do not.
 card.querySelector('.cf-like').addEventListener('click',e=>{const now=gestureNow();if(e.detail>1&&now-r.lastButton<420)return;r.lastButton=now;toggle()});
 function imageGesture(){const now=gestureNow();if(now-r.lastGesture<420)return;r.lastGesture=now;toggle();if(selected(r)==='c3'){art.classList.remove('cf-liked-flash');void art.offsetWidth;art.classList.add('cf-liked-flash')}}
 const art=card.querySelector('.cf-art');if(art){const flash=document.createElement('span');flash.className='cf-like-flash';flash.setAttribute('aria-hidden','true');flash.innerHTML=thumb;art.appendChild(flash);const photo=art.querySelector('img');art.dataset.loading='true';const loaded=()=>{delete art.dataset.loading;r.rendered=!!(photo.complete&&photo.naturalWidth>0)};photo?.addEventListener('load',loaded);if(photo?.complete&&photo.naturalWidth>0)loaded();photo?.addEventListener('error',()=>{delete art.dataset.loading;art.dataset.failed='true';r.rendered=false;r.meter.partial=true;r.anyMeter.partial=true;r.halfMeter.partial=true;save()});art.addEventListener('dblclick',e=>{e.preventDefault();imageGesture()});art.addEventListener('pointerup',e=>{if(e.pointerType!=='touch')return;const now=gestureNow(),t=r.touch;if(t&&now-t.time<340&&Math.hypot(e.clientX-t.x,e.clientY-t.y)<25){imageGesture();r.touch=null}else r.touch={time:now,x:e.clientX,y:e.clientY}});art.addEventListener('pointercancel',()=>r.touch=null)}
 render(r);
});
const observed=new Map(rows.map(r=>[r.card,r]));
const observer=supported?new IntersectionObserver(entries=>{entries.forEach(entry=>{const r=observed.get(entry.target);if(r)r.intersects=entry.isIntersecting})},{threshold:0}):null;
if(observer)rows.forEach(r=>observer.observe(r.card));
function fullVisibleFraction(card){
 const vv=window.visualViewport;
 const clips=[{left:vv?vv.offsetLeft:0,top:vv?vv.offsetTop:0,right:vv?vv.offsetLeft+vv.width:innerWidth,bottom:vv?vv.offsetTop+vv.height:innerHeight}];
 for(let el=card.parentElement;el;el=el.parentElement){
  const style=getComputedStyle(el),rect=el.getBoundingClientRect();
  const x=/(auto|scroll|hidden|clip)/.test(style.overflowX),y=/(auto|scroll|hidden|clip)/.test(style.overflowY);
  if(x||y)clips.push({left:x?rect.left+el.clientLeft:-Infinity,right:x?rect.left+el.clientLeft+el.clientWidth:Infinity,top:y?rect.top+el.clientTop:-Infinity,bottom:y?rect.top+el.clientTop+el.clientHeight:Infinity});
 }
 return clock.fullFraction(card.getBoundingClientRect(),clips);
}
function active(){return supported&&!submitting&&!paused&&document.visibilityState==='visible'&&document.hasFocus()}
function sample(now){
 const enabled=active();
 rows.forEach(r=>{const photo=r.card.querySelector('.cf-art img');const ready=photo&&photo.complete&&photo.naturalWidth>0;const eligible=enabled&&root.dataset.enhanced==='true'&&r.rendered&&ready&&r.intersects===true&&clock.fraction(r.card.getBoundingClientRect(),innerWidth,innerHeight)>=.5;
  r.meter.sample(now,eligible);
  const fraction=enabled&&root.dataset.enhanced==='true'&&r.rendered&&ready?fullVisibleFraction(r.card):0;
  r.anyMeter.sample(now,fraction>=.01);r.halfMeter.sample(now,fraction>=.5);
  if(r.meter.total>=1&&selected(r)==='c1'){r.codes.c2.click();render(r)}
 });
}
function flush(){if(supported)sample(performance.now());save()}
function pause(){flush();paused=true;rows.forEach(r=>{r.meter.pause();r.anyMeter.pause();r.halfMeter.pause()})}
function resume(){paused=false;rows.forEach(r=>{r.meter.pause();r.anyMeter.pause();r.halfMeter.pause()});if(supported)sample(performance.now())}
// Keep native navigation and validation intact. Save before native handlers read fields.
next.addEventListener('click',flush,true);
form.addEventListener('submit',flush,true);
window.addEventListener('blur',pause);window.addEventListener('focus',resume);
document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')pause();else resume()});
window.addEventListener('pagehide',()=>{pause();submitting=true});window.addEventListener('beforeunload',flush);
window.addEventListener('pageshow',e=>{if(e.persisted){submitting=false;resume()}});
function frame(now){if(!submitting){sample(now);if(now-lastSave>=250){save();lastSave=now}}requestAnimationFrame(frame)}
root.dataset.enhanced='true';
native.classList.add('cf-native-hidden');timing.classList.add('cf-native-hidden');
save();if(supported)requestAnimationFrame(frame);
})();

if(window.QuestraTheme)window.QuestraTheme.ready();
