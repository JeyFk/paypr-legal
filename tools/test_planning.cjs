const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const {wages,fica2026,booking,shift} = require('../docs/sage/pay-math.js');
let count=0;
function near(actual,expected){assert.ok(Math.abs(actual-expected)<1e-7,`${actual} != ${expected}`);count++;}
function rejects(fn){assert.throws(fn);count++;}
near(booking(20,4,30,1,0,3).booking,90);
near(booking(20,4,30,1,0,3).weekly,270);
near(booking(20,4,0,2,2,1).booking,88);
near(booking(20,4,0,2,0,1).booking,80);
near(booking(23.75,0,1,1,0,1).booking,23.75/60);
near(booking(0,1,0,1,0,1).booking,0);
for(const args of [['',4,0,1,0,1],[-1,4,0,1,0,1],[20,4.5,0,1,0,1],[20,4,60,1,0,1],[20,24,1,1,0,1],[20,0,0,1,0,1],[20,4,0,0,0,1],[20,4,0,1.5,0,1],[20,4,0,1,0,0],[20,24,0,1,0,8],[Infinity,4,0,1,0,1]])rejects(()=>booking(...args));
near(shift('09:00','17:30',30,false),480);
near(shift('22:00','02:30',0,true),270);
near(shift('09:00','09:00',0,true),1440);
near(shift('','',0,false),0);
for(const args of [['09:00','',0,false],['22:00','02:00',0,false],['09:00','17:00',480,false],['09:00','17:00',-1,false],['09:00','17:00',.5,false],['','',30,false],['','',0,true],['25:00','17:00',0,false],['09:00','10:00',0,true]])rejects(()=>shift(...args));
near(wages(25,46,52).weekly,1225);near(wages(25,46,52).annual,63700);
near(wages(25,46,52).monthly,63700/12);near(wages(20,40.5,1).weekly,815);
near(wages(20,5*shift('09:00','17:30',30,false)/60,1).weekly,800);
near(wages(20,(5*480+30)/60,1).weekly,815);
for(const args of [[' ',40,52],[25,-1,52],[25,169,52],[25,40,53]])rejects(()=>wages(...args));
near(fica2026(2999.99).employerFica,0);near(fica2026(3000).employerFica,229.5);near(fica2026(200000).socialSecurity,11439);
// Exports contain actual user-selected values and valid CSV escaping, without network calls.
const blobs=[];let downloaded;
const ctx={window:{},Blob,URL:{createObjectURL:b=>{blobs.push(b);return 'blob:test';},revokeObjectURL:()=>{}},document:{createElement:()=>({click(){downloaded=this.download},remove(){}}),body:{appendChild(){}}},setTimeout:fn=>fn()};
vm.runInNewContext(fs.readFileSync(__dirname+'/../docs/sage/tool-export.js','utf8'),ctx);
(async()=>{ctx.window.PayprExport.csv('summary.csv',[['Item','Value'],['A "quote", comma','123.45']]);assert.equal(downloaded,'summary.csv');assert.equal(await blobs[0].text(),'"Item","Value"\r\n"A ""quote"", comma","123.45"\r\n');count++; console.log(`Planning checks passed: ${count} calculation, validation, regression and CSV checks.`);})().catch(e=>{console.error(e);process.exitCode=1;});
