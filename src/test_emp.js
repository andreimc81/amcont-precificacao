const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{ const X=JSON.parse(fs.readFileSync('motor_xlsx.json')); const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1300,height:1400}}); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file:///home/claude/work/amcont-precificacao.html'); await p.evaluate(()=>localStorage.clear()); await p.reload();
 await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(500);
 for (const ano of [2027,2029,2033]){
  const r=await p.evaluate((ano)=>{ MODO="reajuste"; $("#regime").value="presumido"; $("#setor").value="comercio"; sincronizar&&sincronizar();
    const set=(k,v)=>$("#"+k).value=v; set("receita",3100000); set("g-integral",150000); set("g-red30",0); set("g-red60",1390000); set("g-red70",120000); set("g-sem",720000); set("g-bimp",1200000); set("imposto",12); set("reducao","0"); set("p-irpj",8); set("p-csll",12);
    ANO=ano; const x=rodar("lc").r; return [x.NF, x.liqApos-x.liqAntes, x.cred, x.icms]; },ano);
  const x=X[ano]; console.log(ano,'html NF',r[0].toFixed(2),'prova',r[1].toExponential(1),'cred',r[2].toFixed(2),'| xlsx NF',x[0].toFixed(2),'cred',x[2].toFixed(2),'| dif NF',(r[0]/x[0]-1).toExponential(2)); }
 // Simples e LC 224
 console.log(JSON.stringify(await p.evaluate(()=>{ $("#receita").value=8000000; const f=fatorLC224(); $("#receita").value=3100000; $("#regime").value="simples"; sincronizar(); const s=rodar("lc"); return [f, s.tipo, +s.r.NF.toFixed(2), $("#c-bimp").hidden, $("#lb-imposto").textContent]; })), errs);
 // produto: SC e consulta
 const q=await b.newPage({viewport:{width:1300,height:1500}}); q.on('pageerror',e=>errs.push(String(e)));
 await q.goto('file:///home/claude/work/amcont-produto.html'); await q.evaluate(()=>localStorage.clear()); await q.reload();
 await q.fill('#senha','amcont2027'); await q.keyboard.press('Enter'); await q.waitForTimeout(400);
 await q.fill('#ncm','1006.30.21'); await q.waitForTimeout(200);
 console.log(JSON.stringify(await q.evaluate(()=>FICHA.sc.ops.map(o=>[o.aliq,o.rot.slice(0,50)]))));
 await q.click('#ficha input[name=scq-c7][value="sim"]'); await q.waitForTimeout(100);
 await q.click('#ficha input[name=scq-dest][value="rev"]'); await q.waitForTimeout(100);  // perguntas de ICMS de SC (rodada 17): cesta básica a contribuinte, 7%
 console.log('icms-venda', await q.inputValue('#icms-venda'));
 await q.click('#b-consulta'); await q.fill('#cq','1006.30.21\n2203.00.00, 3004.90.99; 62052000\n1.2301.22.00 123 0401.20.10 8703.21.00'); await q.click('#b-consultar'); await q.waitForTimeout(200);
 console.log('linhas', await q.evaluate(()=>document.querySelectorAll('#cq-res tbody tr').length));
 await q.screenshot({path:'/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/consulta.png'});
 await q.click('#cq-res button[data-sim="22030000"]'); await q.waitForTimeout(200);
 console.log('simular', await q.evaluate(()=>[FICHA.cod, $("#tela-consulta").hidden, $("#is").value, FICHA.sc.ops[0].aliq]), errs);
 await b.close(); })();
