const { chromium } = require('playwright'); const fs=require('fs');
const C=JSON.parse(fs.readFileSync('cross_scq.json'));
(async()=>{ const b=await chromium.launch(); const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file:///home/claude/work/amcont-produto.html'); await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
 const r=await p.evaluate(C=>{ const D={contribuinte:'rev',contribuinte_uso:'uso',final:'final',orgao_sc:'orgao'}, O={sc:'sc',outro_estado:'fora',importacao:'imp'}, A={comercio:'com',fabricante:'ind'}, SN={S:'sim',N:'nao'};
   return C.map(k=>{ const b=benSC(k.cod), oi='ABCDE'.indexOf(k.ben), ben=b&&b.q&&b.ops[oi]?b.ops[oi][0]:'(nenhum)'; const z=resolverSC(k.cod,{dest:D[k.dest],desc:SN[k.desc],c7:SN[k.c7],orig:O[k.orig],ativ:A[k.ativ],ben}); return [k.cod,k.dest,k.ben,k.desc,k.c7,k.orig,k.ativ,z.carga,k.xlsx,k.i17]; }); }, C);
 let ok=0; for (const x of r){ const g=Math.abs(x[7]-x[8])<1e-9 && Math.abs(x[8]-x[9])<1e-9; ok+=g; console.log(g?'OK ':'DIF',x.join(' | ')); }
 console.log(ok+' de '+r.length, errs); await b.close(); })();
