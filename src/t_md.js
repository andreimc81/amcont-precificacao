const { chromium } = require('playwright');
(async()=>{
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1280,height:1800}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('file:///home/claude/work/amcont-produto.html');
  await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
  const out = await p.evaluate(()=>{
    const res=[]; let falhas=0;
    for (const tipo of ['produto','servico']) for (const reg of ['presumido','real','simples']) for (const ano of [2026,2027,2029,2033]) {
      definirTipo(tipo,true);
      try{ $("#regime").value=reg; }catch(e){}
      ANO=ano; calcular();
      const o=opcoes(), H=hoje(o), A=noAno(o,H.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn), M=mesmoDesembolso(o,A);
      if (ano<2027){ if(M!==null){falhas++;res.push('2026 deveria ser null');} continue; }
      if (!M){falhas++;res.push('null '+tipo+reg+ano);continue;}
      // prova: refazendo noAno com mcAlvo = mc do cenario deve devolver nf = pv
      const alvo = M.tipo==='geral'?M.mc:null;
      if (M.tipo==='geral'){ const R=noAno(o,M.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn); if (Math.abs(R.nf-o.pv)>0.005){falhas++;res.push(['prova geral',tipo,reg,ano,R.nf,o.pv].join(' '));}
        if (Math.abs(M.cad+M.cbs+M.ibs-o.pv)>0.005){falhas++;res.push('soma');} }
      else { const Rt=noAno(o,M.trad.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn), Rh=noAno(o,M.hib.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn);
        if (Math.abs(Rt.trad.nf-o.pv)>0.005||Math.abs(Rh.hib.nf-o.pv)>0.005){falhas++;res.push(['prova simples',tipo,ano,Rt.trad.nf,Rh.hib.nf,o.pv].join(' '));} }
      res.push([tipo,reg,ano,M.tipo==='geral'?[A.nf,M.cad,M.cbs+M.ibs,A.mc,M.mc].map(x=>x.toFixed(2)).join('|'):[M.hib.cad,M.hib.mc,M.trad.mc,H.mc].map(x=>x.toFixed(2)).join('|')].join(' '));
    }
    return {falhas,res};
  });
  console.log(out.res.join('\n')); console.log('FALHAS',out.falhas,'ERRS',errs); if(out.falhas||errs.length) process.exitCode=1;
  await p.evaluate(()=>{definirTipo('produto',true);$('#regime').value='presumido';ANO=2027;calcular();});
  console.log(await p.evaluate(()=>document.querySelector('#p-ano').innerText.replace(/\n+/g,' | ').slice(0,1800)));
  await b.close();
})();
