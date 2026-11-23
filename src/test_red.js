const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file:///home/claude/work/amcont-cliente.html'); await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(500);
 for (const modo of ['custo','reajuste']) for (const v of ['0','0.6','1','isento']){
   const r=await p.evaluate(([modo,v])=>{ MODO=modo; $("#reducao").value=v; const x=rodar(PARAM.premissaPadrao||"prof"); const r=x.r;
     return [x.tipo, x.o.redSaida, (r.NF??r.nf??r.preco), r.cred, r.cbs, $("#dica-reducao").textContent.slice(0,40)]; },[modo,v]);
   console.log(modo,v,JSON.stringify(r)); }
 await p.selectOption('#setor','passageiros'); console.log('passageiros ->',await p.evaluate(()=>$("#reducao").value), await p.evaluate(()=>document.querySelector('#cta-link')?.href), errs);
 await b.close(); })();
