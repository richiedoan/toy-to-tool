// Handler evidence only: this minimal DOM adapter is not a browser or AT test.
const fs = require('node:fs');
const vm = require('node:vm');
const {performance} = require('node:perf_hooks');
const phase = process.argv[2];
const source = fs.readFileSync('dashboard/app.js', 'utf8');
class Element {
  constructor() { this.children = []; this.listeners = {}; this.value = ''; this.textContent = ''; this.disabled = false; }
  append(...nodes) { this.children.push(...nodes); }
  replaceChildren(...nodes) { this.children = nodes; }
  addEventListener(name, fn) { (this.listeners[name] ??= []).push(fn); }
}
const elements = Object.fromEntries(['status','filter','refresh','metrics'].map(k => ['#'+k,new Element()]));
const data = [{title:'Revenue',value:'$24,500'},{title:'Orders',value:'182'},{title:'Customers',value:'96'},{title:'Conversion',value:'4.2%'}];
let mode = 'success', calls = 0, release;
const context = vm.createContext({performance, document:{querySelector:s=>elements[s],createElement:()=>new Element()},fetch:async()=>{
  calls++;
  if(mode === 'delay') await new Promise(r=>release=r);
  if(mode === 'offline') throw new TypeError('Controlled offline rejection');
  return {ok:mode!=='503',json:async()=>structuredClone(data)};
}});
const settle = () => new Promise(r=>setImmediate(r));
const snapshot = () => ({status:elements['#status'].textContent,disabled:elements['#refresh'].disabled,rows:elements['#metrics'].children.map(a=>a.children.map(n=>n.textContent))});
const filter = value => {elements['#filter'].value=value; const t=performance.now(); elements['#filter'].listeners.input[0](); return performance.now()-t;};
(async()=>{
  vm.runInContext(source,context); await settle();
  const result={captured_at:new Date().toISOString(),runtime:process.version,scope:'Real app.js executed in Node VM with minimal DOM and controlled fetch; no rendering, browser input-to-frame timing, keyboard, AT or leak proof.',initial:snapshot()};
  const beforeCalls=calls;
  result.filters=[];
  for(const q of ['REVen','orders','zzz','']) {filter(q); result.filters.push({query:q,...snapshot()});}
  result.filterRequests=calls-beforeCalls;
  filter('');
  result.synchronousHandlerSamplesMs=['r','o','c','x',''].map(filter);
  result.timingLimit='Five handler durations after warmup, diagnostic only. No requestAnimationFrame or Chrome; cannot establish README p95 budget.';
  result.faults=[];
  for(const fault of ['503','offline']){
    mode=fault; await elements['#refresh'].listeners.click[0](); result.faults.push({fault,...snapshot()});
    mode='success'; await elements['#refresh'].listeners.click[0](); result.faults.push({fault:'retry',...snapshot()});
  }
  mode='delay'; const pending=elements['#refresh'].listeners.click[0](); await settle(); result.loading=snapshot(); release(); await pending; result.delayedSuccess=snapshot();
  result.cycles=[];
  mode='success';
  for(let n=1;n<=15;n++){filter('orders');filter('');await elements['#refresh'].listeners.click[0]();if([1,5,15].includes(n))result.cycles.push({n,calls,nodes:elements['#metrics'].children.length,listeners:Object.fromEntries(Object.entries(elements).map(([k,e])=>[k,Object.fromEntries(Object.entries(e.listeners).map(([key,v])=>[key,v.length]))]))});}
  // A final failed refresh after successful cycles.
  elements['#metrics'].replaceChildren(); mode='503'; await elements['#refresh'].listeners.click[0](); result.finalFailure=snapshot();
  if (phase === 'after') {
    result.initialFailureComparison = [];
    for (const [build,path] of [['before','audits/before/source/app.js'],['after','dashboard/app.js']]) {
      const fresh = Object.fromEntries(['status','filter','refresh','metrics'].map(k=>['#'+k,new Element()]));
      const realm = vm.createContext({performance,document:{querySelector:s=>fresh[s],createElement:()=>new Element()},fetch:async()=>({ok:false})});
      vm.runInContext(fs.readFileSync(path,'utf8'),realm); await settle();
      const failed={status:fresh['#status'].textContent,disabled:fresh['#refresh'].disabled,rows:fresh['#metrics'].children.length};
      realm.fetch=async()=>({ok:true,json:async()=>structuredClone(data)});
      await fresh['#refresh'].listeners.click[0]();
      result.initialFailureComparison.push({build,failed,retryRows:fresh['#metrics'].children.map(a=>a.children.map(n=>n.textContent))});
    }
  }
  fs.writeFileSync(`audits/${phase}/handlers.json`,JSON.stringify(result,null,2)+'\n');
  console.log(JSON.stringify({phase,initial:result.initial,faults:result.faults,samples:result.synchronousHandlerSamplesMs}));
})().catch(e=>{console.error(e);process.exitCode=1});
