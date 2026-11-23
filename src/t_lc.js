const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage({acceptDownloads:true, viewport:{width:1300,height:1500}}); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const SP='/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/';
 const go=async()=>{ await p.goto('file:///home/claude/work/amcont-produto.html'); await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(400); };
 await go(); await p.evaluate(()=>localStorage.clear()); await p.click('#tipo button[data-t=servico]');
 const tipo=async q=>{ await p.fill('#ncm',''); await p.type('#ncm',q); await p.waitForTimeout(150); };
 for (const q of ['04.01','4.01','0401','040101','04.01.01','401','7.02','medicina','17','1.2301','99.03.02']){
   await tipo(q); console.log(q, await p.evaluate(()=>[...document.querySelectorAll('#ncm-lista div[data-lc]')].map(x=>x.dataset.lc).join(','))+' | nbs '+await p.evaluate(()=>document.querySelectorAll('#ncm-lista div[data-c]').length)); }
 await tipo('040101'); await p.click('#ncm-lista div[data-lc]');
 console.log('04.01 ->', await p.evaluate(()=>[FICHA.fmt,FICHA.lc,FICHA.opcoes[FICHA.sel].ccl,$("#trat").value,FICHA.opcoes.map(o=>o.ccl).join("/")]));
 await tipo('16.02'); await p.click('#ncm-lista div[data-lc]');
 console.log('painel', await p.evaluate(()=>[document.querySelectorAll('#ficha .lcp label').length, $("#ncm").value]));
 await p.fill('#lcp-f','escolar'); console.log('filtro', await p.evaluate(()=>[...document.querySelectorAll('#ficha .lcp label')].filter(l=>l.style.display!=="none").length));
 await p.fill('#lcp-f',''); await p.screenshot({path:SP+'lc_painel.png'});
 await p.click('#ficha .lcp label >> nth=3');
 console.log('escolhido', await p.evaluate(()=>[FICHA.fmt,FICHA.lc,FICHA.lcQtd,FICHA.opcoes.map(o=>o.ccl).join("/"),!!document.querySelector('button[data-lcp]')]));
 await p.screenshot({path:SP+'lc_ficha.png'});
 const [dl]=await Promise.all([p.waitForEvent('download'),p.click('#b-salvar')]); await dl.saveAs(SP+'lc.json');
 await p.click('button[data-lcp]'); console.log('trocar', await p.evaluate(()=>document.querySelectorAll('#ficha .lcp label').length));
 // NBS com mais de um item
 await tipo('115021000'); console.log('multi', await p.evaluate(()=>[FICHA.lcItens, FICHA.opcoes.map(o=>o.ccl).join("/")]));
 await p.click('button[data-lcr="01.03"]').catch(()=>{}); await p.click('button[data-lcr]').catch(()=>{});
 console.log('restrito', await p.evaluate(()=>[FICHA.lc, FICHA.opcoes.map(o=>o.ccl).join("/")]));
 await go(); await p.setInputFiles('#arquivo',SP+'lc.json'); await p.waitForTimeout(300);
 console.log('reaberto', await p.evaluate(()=>[TIPO,FICHA.fmt,FICHA.lc,FICHA.sel]));
 await p.click('#b-consulta'); await p.fill('#cq','07.02\n1006.30.21\n040101\n99.03.02\n12345'); await p.click('#b-consultar');
 console.log('lote', await p.evaluate(()=>document.querySelectorAll('#cq-res tbody tr').length));
 await p.click('#cq-res button[data-lc="07.02"] >> nth=0'); console.log('simular', await p.evaluate(()=>[TIPO,FICHA.fmt,FICHA.lc]));
 console.log(errs); await b.close(); })();
