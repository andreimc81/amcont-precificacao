const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const ctx=await b.newContext();
 for (const f of ['amcont-produto.html','amcont-cliente.html']){
  const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  const U='file:///home/claude/work/'+f; const log=[];
  const entrar=async s=>{ await p.fill('#senha',s); await p.keyboard.press('Enter'); await p.waitForTimeout(400); return await p.evaluate(()=>!document.getElementById('gate')); };
  await p.goto(U); await p.evaluate(()=>localStorage.clear()); await p.reload();
  log.push('padrao entra:'+await entrar('amcont2027'));
  await p.click('#b-senha'); await p.fill('#ns1','minhasenha9'); await p.fill('#ns2','minhasenha9'); await p.click('#troca-senha button[type=submit]'); await p.waitForTimeout(300);
  await p.reload(); log.push('padrao bloqueada:'+!(await entrar('amcont2027')));
  log.push('nova entra:'+await entrar('minhasenha9'));
  await p.reload(); await p.click('#b-esqueci'); log.push('redefine com original:'+await entrar('amcont2027'));
  await p.reload(); log.push('voltou ao padrao:'+await entrar('amcont2027'));
  console.log(f, log.join(' | '), errs); await p.close(); }
 // tela do usuario: produto aliquota zero, compra 100, ICMS 12
 const p=await ctx.newPage(); await p.goto('file:///home/claude/work/amcont-produto.html'); await p.evaluate(()=>localStorage.clear()); await p.reload();
 await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(400);
 console.log(JSON.stringify(await p.evaluate(()=>{ $("#pc").value=100; $("#pc-ano").value=100; $("#pv").value=150; $("#icms-compra").value=12; $("#icms-venda").value=12; $("#trat").value="1"; calcular();
   return [...document.querySelectorAll('#p-forn tbody tr')].map(r=>r.innerText.replace(/\s+/g,' ')); })));
 await b.close(); })();
