const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file:///home/claude/work/amcont-produto.html'); await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(400);
 for (const trat of ["1","0.6","0"]){
 const r = await p.evaluate((trat)=>{ definirModo("compra"); $("#trat").value=trat; ANO=2027;
   escreverCot([{reg:"regular",preco:100,icms:7,das:9.403,anexo:"I"},{reg:"sn_regular",preco:100,icms:7,das:9.40,anexo:"II"},{reg:"sn_tradicional",preco:100,icms:0,das:2.5,anexo:"I"},{reg:"sn_sublimite",preco:100,icms:7,das:9.40,anexo:"I"},{reg:"mei",preco:100,icms:0,das:9.403,anexo:"I"}]);
   calcular(); const o=opcoes(); return lerCot().map(c=>{const k=creditoComprador(c,o); return c.reg+' cbs '+k.cbsIbs.toFixed(2)+' icms '+k.icms.toFixed(2)+' custo '+k.custo.toFixed(2);}); }, trat);
 console.log('trat',trat, r); }
 console.log(errs); await b.close(); })();
