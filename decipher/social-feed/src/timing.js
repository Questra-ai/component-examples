/* Shared by the native component and deterministic timing tests. */
(function(scope){
'use strict';
function fraction(rect,width,height){
 const area=Math.min(rect.width,width)*Math.min(rect.height,height);
 if(!(area>0))return 0;
 const w=Math.max(0,Math.min(rect.right,width)-Math.max(rect.left,0));
 const h=Math.max(0,Math.min(rect.bottom,height)-Math.max(rect.top,0));
 return Math.min(1,w*h/area);
}
function meter(total=0,partial=false){
 return {total:Math.max(0,total),partial,last:null,eligible:false,
  sample(now,eligible){
   if(this.last!==null){const dt=now-this.last;
    if(this.eligible&&eligible&&dt>=0&&dt<=250)this.total+=dt;
    else if(this.eligible&&eligible&&dt>250)this.partial=true;
   }
   this.last=now;this.eligible=eligible;return Math.floor(this.total);
  },
  pause(){this.last=null;this.eligible=false;},
  state(){return this.partial?3:(this.total>=1?2:1)}
 };
}
const api={fraction,meter};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
else scope.SocialFeedTiming=api;
})(typeof window==='undefined'?globalThis:window);
