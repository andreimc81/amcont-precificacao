const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage();
 await p.goto('file:///home/claude/work/amcont-produto.html'); await p.evaluate(()=>localStorage.clear()); await p.reload();
 await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(400);
 console.log(await p.evaluate(()=>{ ANO=2026; const o=opcoes(),H=hoje(o),A=noAno(o,H.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn); return [o.pv,A.nf,H.mc,A.mc]; }));
 await b.close(); })();
