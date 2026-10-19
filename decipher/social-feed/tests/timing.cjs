const assert=require('node:assert/strict');const {fraction,meter}=require('../src/timing.js');
let count=0;function test(name,fn){fn();console.log('PASS',name);count++}
const rect=(left,top,width,height)=>({left,top,width,height,right:left+width,bottom:top+height});
test('short card full and partial visibility',()=>{assert.equal(fraction(rect(0,0,600,400),600,800),1);assert.equal(fraction(rect(0,-201,600,400),600,800),199/400)});
test('tall card uses achievable viewport area',()=>{assert.equal(fraction(rect(0,-200,390,1200),390,600),1);assert.equal(fraction(rect(0,301,390,1200),390,600),299/600)});
test('horizontal clipping is included',()=>assert.equal(fraction(rect(-301,0,600,400),600,800),299/600));
test('zero size and offscreen do not qualify',()=>{assert.equal(fraction(rect(0,0,0,0),600,800),0);assert.equal(fraction(rect(0,900,600,400),600,800),0)});
test('accumulates disjoint visits without double counting',()=>{let m=meter();m.sample(0,true);m.sample(100,true);m.sample(100,true);m.sample(200,false);m.sample(1000,false);m.sample(1100,true);m.sample(1200,true);assert.equal(m.total,200)});
test('hidden and focus pauses drop elapsed gap',()=>{let m=meter();m.sample(0,true);m.sample(100,true);m.pause();m.sample(10000,true);m.sample(10100,true);assert.equal(m.total,200)});
test('reload starts a new monotonic baseline',()=>{let old=meter();old.sample(0,true);old.sample(100,true);let resumed=meter(old.total,old.partial);resumed.sample(0,true);resumed.sample(125,true);assert.equal(resumed.total,225)});
test('long stalls excluded and flagged lower-bound',()=>{let m=meter();m.sample(0,true);m.sample(900,true);assert.equal(m.total,0);assert.equal(m.state(),3);m.sample(1000,true);assert.equal(m.total,100)});
test('negative clock steps never subtract or add',()=>{let m=meter();m.sample(100,true);m.sample(90,true);assert.equal(m.total,0)});
test('availability distinguishes observed zero and positive',()=>{let m=meter();assert.equal(m.state(),1);m.sample(0,true);m.sample(10,true);assert.equal(m.state(),2);assert.equal(meter(0,true).state(),3)});
console.log(count+' timing tests passed');
