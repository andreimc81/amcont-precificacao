const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch();
 for (const f of ['amcont-precificacao.html','amcont-cliente.html']){
  const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('file:///home/claude/work/'+f);
  await p.evaluate(()=>localStorage.setItem('amcont_precificacao_parametros',JSON.stringify({versaoDados:'2026.1',transicao:[{ano:2026,cbs:0,ibs:0,fatorIcmsIss:1},{ano:2027,cbs:0.092,ibs:0.001,fatorIcmsIss:1}]})));
  await p.reload();
  const s=await p.$('#senha'); if(s){ await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(400); }
  console.log(f, await p.evaluate(()=>[PARAM.versaoDados, PARAM.transicao.map(t=>t.cbs).join(','), PARAM.atividades.find(a=>a.id==='passageiros').redSaida, localStorage.getItem('amcont_precificacao_parametros')]), errs);
  await p.close(); }
 await b.close(); })();
