const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const S='/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/';
 for (const [f,n] of [['amcont-produto.html','lp'],['amcont-cliente.html','lc']]){ const p=await b.newPage({viewport:{width:1100,height:520}}); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('file:///home/claude/work/'+f); await p.evaluate(()=>localStorage.clear()); await p.reload(); await p.screenshot({path:S+n+'1.png'});
  await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(500); await p.screenshot({path:S+n+'2.png'}); console.log(f,errs); }
 await b.close(); })();
