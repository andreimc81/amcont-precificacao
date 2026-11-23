const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage();
 await p.goto('file:///home/claude/work/amcont-precificacao.html'); await p.evaluate(()=>localStorage.clear()); await p.reload();
 await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(500);
 console.log(JSON.stringify(await p.evaluate(()=>{ const out={};
   MODO="custo"; $("#regime").value="presumido"; $("#setor").value="comercio"; sincronizar(); $("#custo").value=500; $("#desp").value=9.86; $("#lucro").value=10; $("#imposto").value=12; $("#reducao").value="0";
   out.custo={}; for (const a of [2026,2027,2029,2031,2033]){ ANO=a; out.custo[a]=["prof","lc","plp"].map(pr=>+rodar(pr).r.NF.toFixed(2)); }
   $("#regime").value="simples"; sincronizar(); $("#receita").value=1000000; $("#anexo").value="I"; $("#aliqsn").value=9.403; ANO=2027; $("#g-bimp").value=0;
   const s=rodar("lc").r; out.simples={baseEq:s.baseEq, credEq:s.credEq, keys:Object.keys(s).join(',')};
   return out; })));
 const q=await b.newPage(); await q.goto('file:///home/claude/work/amcont-produto.html'); await q.evaluate(()=>localStorage.clear()); await q.reload();
 await q.fill('#senha','amcont2027'); await q.keyboard.press('Enter'); await q.waitForTimeout(400);
 console.log(JSON.stringify(await q.evaluate(()=>{ const out={}; for (const a of [2027,2029,2033]){ ANO=a; calcular(); out[a]=[...document.querySelectorAll('#p-forn tbody tr')].map(r=>r.innerText.replace(/\s+/g,' ')); } return out; })));
 await b.close(); })();
