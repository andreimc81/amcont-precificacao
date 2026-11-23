const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file:///home/claude/work/amcont-cliente.html'); await p.evaluate(()=>localStorage.clear()); await p.reload();
 await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(500);
 console.log(JSON.stringify(await p.evaluate(()=>{ MODO="reajuste"; ANO=2027; const out=[]; for (const sh of [0,40,100]){ $("#sem-pc").value=sh; const x=rodar("lc").r; out.push([sh,+x.NF.toFixed(2),+(x.variacao*100).toFixed(2),(x.liqApos-x.liqAntes).toExponential(1)]); } return out; })), errs);
 await b.close(); })();
