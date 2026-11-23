const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage({acceptDownloads:true}); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const go=async()=>{ await p.goto('file:///home/claude/work/amcont-produto.html'); await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(400); };
 await go(); await p.evaluate(()=>localStorage.clear());
 await p.click('#b-consulta'); await p.fill('#cq','1006.30.21\n3004.90.99\n1.2301.22.00'); await p.click('#b-consultar');
 const [dl]=await Promise.all([p.waitForEvent('download'),p.click('#b-cq-salvar')]); const f='/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/cq.json'; await dl.saveAs(f);
 await go(); await p.setInputFiles('#arquivo',f); await p.waitForTimeout(300);
 console.log(await p.evaluate(()=>[$("#cq").value.split("\n").length, document.querySelectorAll('#cq-res tbody tr').length]), errs);
 await b.close(); })();
