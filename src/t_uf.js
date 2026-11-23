const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1300,height:1700}}); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const SP='/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/';
 await p.goto('file:///home/claude/work/amcont-produto.html'); await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(400);
 await p.fill('#ncm','1806.31.10'); await p.waitForTimeout(150);
 for (const [uf,tipo,imp,dupla] of [["SC","contrib",false,true],["RS","contrib",false,true],["BA","contrib",false,true],["RJ","final",false,true],["RJ","final",false,false],["BA","final",true,true],["SP","contrib_uso",false,true]]){
   const r = await p.evaluate(([uf,tipo,imp,dupla])=>{ $("#uf-dest").value=uf; $("#dest-tipo").value=tipo; $("#importado").checked=imp; $("#difal-dupla").checked=dupla; sincronizar(); calcular();
     const o=opcoes(); const H=hoje(o); const A=noAno(o,H.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn);
     return [o.icmsVenda.toFixed(4), o.icmsInter, o.difal.toFixed(4), A.nf.toFixed(2), (A.mc-H.mc).toFixed(6), $("#icms-venda").disabled, [...document.querySelectorAll('#p-nota tr')].slice(0,5).map(x=>x.innerText.replace(/\s+/g,' ')).join(' | '), $("#dica-dest").textContent.slice(0,140)]; }, [uf,tipo,imp,dupla]);
   console.log(uf,tipo,imp,dupla, r);
 }
 await p.screenshot({path:SP+'uf.png'});
 // compra com fornecedor de fora
 const r2 = await p.evaluate(()=>{ $("#uf-dest").value="SC"; definirModo("compra"); $("#regime").value="presumido"; $("#destino").value="uso"; $("#icms-venda").value=17; ANO=2027;
   escreverCot([{reg:"regular",preco:100,icms:12,das:9.4,anexo:"I",fora:true},{reg:"regular",preco:100,icms:17,das:9.4,anexo:"I",fora:false},{reg:"regular",preco:100,icms:4,das:9.4,anexo:"I",fora:true}]);
   $("#difal-dupla").checked=true; calcular(); const o=opcoes();
   return [getComputedStyle($("#c-dupla")).display, getComputedStyle($("#icms-venda").closest('.campo')).display, $("#lb-icms-venda").textContent, lerCot().map(c=>{const k=creditoComprador(c,o); return k.difal.toFixed(2)+'/'+k.custo.toFixed(2);}), [...document.querySelectorAll('#p-compra thead th')].map(x=>x.innerText).join('/')]; });
 console.log('compra', r2);
 await p.screenshot({path:SP+'uf_compra.png', fullPage:true});
 console.log(errs); await b.close(); })();
