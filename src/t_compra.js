const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage({acceptDownloads:true, viewport:{width:1300,height:1700}}); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 const SP='/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/';
 const go=async()=>{ await p.goto('file:///home/claude/work/amcont-produto.html'); await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(400); };
 await go(); await p.evaluate(()=>localStorage.clear());
 // venda: nota fiscal
 await p.fill('#ncm','1806.31.10'); await p.waitForTimeout(200);
 await p.screenshot({path:SP+'venda_nota.png'});
 console.log('nota venda', await p.evaluate(()=>[...document.querySelectorAll('#p-nota tr')].map(r=>r.innerText.replace(/\s+/g,' ')).join(' | ')));
 console.log('visiveis venda', await p.evaluate(()=>['#p-cot','#p-compra','#p-nota','#p-hoje','#c-snop'].map(s=>s+':'+(getComputedStyle(document.querySelector(s)).display!=='none'))));
 // compra
 await p.click('#modo button[data-m=compra]'); await p.waitForTimeout(200);
 console.log('visiveis compra', await p.evaluate(()=>['#p-cot','#p-compra','#p-nota','#p-hoje','#p-ano','#c-snop','#pv'].map(s=>s+':'+(getComputedStyle(document.querySelector(s)).display!=='none' && document.querySelector(s).offsetParent!==null))));
 const linhas=async()=>p.evaluate(()=>[...document.querySelectorAll('#p-compra tbody tr')].map(r=>r.innerText.replace(/\s+/g,' ')));
 console.log('2027 presumido revenda', await linhas());
 await p.screenshot({path:SP+'compra.png', fullPage:false});
 // cotacoes com precos diferentes
 await p.evaluate(()=>{ const tr=[...document.querySelectorAll('#cot tbody tr')]; tr[0].querySelector('[data-k=preco]').value=105; tr[2].querySelector('[data-k=preco]').value=92; tr[3].querySelector('[data-k=preco]').value=90; tr[3].dispatchEvent(new Event('input',{bubbles:true})); });
 await p.waitForTimeout(100);
 console.log('cotacoes', await linhas(), await p.evaluate(()=>document.querySelector('#p-compra .destaque').innerText.replace(/\s+/g,' ')));
 console.log('alerta', await p.evaluate(()=>(document.querySelector('#p-compra p.dica')||{}).innerText));
 await p.click('#p-compra tbody tr[data-i="2"]'); 
 console.log('nota compra', await p.evaluate(()=>[...document.querySelectorAll('#p-nota-compra tr')].map(r=>r.innerText.replace(/\s+/g,' ')).join(' | ')));
 await p.screenshot({path:SP+'compra2.png', fullPage:true});
 // simples das
 await p.selectOption('#regime','simples'); await p.waitForTimeout(100);
 console.log('simples das', (await linhas()).slice(0,3), await p.evaluate(()=>getComputedStyle(document.querySelector('#c-snop')).display));
 await p.selectOption('#sn-opcao','regular'); await p.waitForTimeout(100);
 console.log('simples regular', (await linhas()).slice(0,3));
 await p.selectOption('#regime','real'); await p.selectOption('#destino','uso'); await p.click('#anos button[data-a="2026"]'); await p.waitForTimeout(100);
 console.log('real uso 2026', (await linhas()).slice(0,3));
 await p.selectOption('#destino','revenda'); await p.waitForTimeout(100);
 console.log('real revenda 2026', (await linhas()).slice(0,3), await p.evaluate(()=>[...document.querySelectorAll('#p-compra thead th')].map(x=>x.innerText).join('/')));
 // salvar e reabrir
 const [dl]=await Promise.all([p.waitForEvent('download'),p.click('#b-salvar')]); await dl.saveAs(SP+'compra.json');
 await go(); await p.setInputFiles('#arquivo',SP+'compra.json'); await p.waitForTimeout(300);
 console.log('reaberto', await p.evaluate(()=>[MODO, document.body.classList.contains('modo-compra'), lerCot().map(c=>c.preco).join(','), $("#regime").value, $("#destino").value, ANO]));
 // levar para venda
 await p.click('#b-cot-usar'); await p.waitForTimeout(150);
 console.log('levado', await p.evaluate(()=>[MODO, $("#pc-ano").value, $("#forn").value, $("#aliqsn-forn").value]));
 // servico
 await p.click('#modo button[data-m=compra]'); await p.click('#tipo button[data-t=servico]'); await p.fill('#ncm','040101'); await p.waitForTimeout(200); await p.click('#ncm-lista div[data-lc]'); await p.click('#anos button[data-a="2033"]'); await p.waitForTimeout(150);
 console.log('servico 2033', (await linhas()), await p.evaluate(()=>[...document.querySelectorAll('#cot .cot-icms')].every(x=>x.style.display==='none')));
 await p.click('#modo button[data-m=venda]'); await p.waitForTimeout(100);
 console.log('nota servico', await p.evaluate(()=>[...document.querySelectorAll('#p-nota tr')].map(r=>r.innerText.replace(/\s+/g,' ')).join(' | ')));
 console.log(errs); await b.close(); })();
