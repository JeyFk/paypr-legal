/* Exercise emitted goals, including localization and untrusted metadata. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const code = fs.readFileSync(path.join(__dirname, '../docs/sage/conversions.js'), 'utf8');
function app(hostname, pathname) {
  const emitted = [], handlers = {};
  const context = {window:{datafast:(...args)=>emitted.push(args)},
    location:{hostname,pathname,origin:'https://'+hostname,href:'https://'+hostname+pathname},
    document:{addEventListener:(event,fn)=>handlers[event]=fn},URL};
  vm.runInNewContext(code, context);
  return {context,emitted,handlers};
}
let checks = 0;
for (const lang of ['es','fr','de','ar']) {
  const state = app('usepaypr.com','/'+lang+'/nanny-timesheet-template');
  state.context.window.payprGoal('template_download',{asset:'timesheet',name:'PRIVATE',amount:789,language:'spoofed'});
  assert.deepEqual(JSON.parse(JSON.stringify(state.emitted[0])),['template_download',{
    page:'/'+lang+'/nanny-timesheet-template',language:lang,content_market:'global',asset:'timesheet'}]);checks++;
  const link = {href:'https://usepaypr.com/downloads/'+lang+'/nanny-timesheet.csv',hasAttribute:()=>true,closest:()=>null};
  state.handlers.click({target:{closest:()=>link}});
  assert.equal(state.emitted[1][0],'template_download');assert.equal(state.emitted[1][1].asset,'timesheet');checks++;
}
for (const [segment,market] of [['espana','ES'],['mexico','MX']]) {
  const state=app('usepaypr.com','/es/'+segment+'/horas-y-pagos-en-casa');
  const link={href:'https://apps.apple.com/app/id6778970494',closest:()=>null};
  state.handlers.click({target:{closest:()=>link}});
  assert.equal(state.emitted[0][0],'app_store_click');assert.equal(state.emitted[0][1].content_market,market);checks++;
}
for (const pathname of ['/es/private/person-name','/es/mexico/private','/de/../../private']) {
  const state=app('usepaypr.com',pathname);state.context.window.payprGoal('app_store_click',{});
  assert.equal(state.emitted[0][1].page,'other_resource');checks++;
}
const old=app('usepaypr.com','/nanny-pay-calculator');old.context.window.payprGoal('calculator_completed',{tool:'wages'});
assert.equal(old.emitted[0][1].page,'/nanny-pay-calculator');assert.equal(old.emitted[0][1].tool,'wages');checks++;
old.context.window.payprGoal('unknown_event',{});assert.equal(old.emitted.length,1);checks++;
old.context.window.datafast=undefined;assert.doesNotThrow(()=>old.context.window.payprGoal('app_store_click',{}));checks++;
old.context.window.datafast=()=>{throw Error('blocked');};assert.doesNotThrow(()=>old.context.window.payprGoal('app_store_click',{}));checks++;
for (const host of ['localhost','127.0.0.1','preview.example.com']) {
  const state=app(host,'/es/');assert.equal(state.context.window.payprGoal,undefined);checks++;
}
console.log(`International goal tests passed: ${checks} scenarios.`);
