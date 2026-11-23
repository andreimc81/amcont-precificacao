const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file:///home/claude/work/amcont-produto.html'); await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
 const r=await p.evaluate(()=>{ definirModo('compra'); definirTipo('produto',true); selecionarCodigo('18063110'); $("#regime").value='real'; $("#destino").value='revenda'; ANO=2027; sincronizar(); calcular();
   const ler=()=>[...document.querySelectorAll("#p-compra table.cmp tbody tr")].map(tr=>[...tr.cells].map(c=>c.textContent.trim()).join(' | ')).slice(0,3);
   const a=ler(); $("#cred-prud").checked=true; $("#cred-prud").dispatchEvent(new Event('change')); const b2=ler();
   const cab2=[...document.querySelectorAll('table.cmp thead th')].map(t=>t.textContent).join('/'); return {antes:a, prudente:b2, cab2, aviso:[...document.querySelectorAll('p.dica')].map(x=>x.textContent).filter(t=>/art. 47|prudente/i.test(t)).map(t=>t.slice(0,160))}; });
 console.log(JSON.stringify(r,null,1), errs); await b.close(); })();
