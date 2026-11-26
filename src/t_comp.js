const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file:///home/claude/work/amcont-produto.html');
 await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
 const r=await p.evaluate(()=>{ const f=[]; const ap=(a,b)=>Math.abs(a-b)<0.005; let n=0, amostra=null;
  for (const tipo of ['produto','servico']) for (const reg of ['presumido','real']) for (const ano of [2027,2030,2033]){
    definirTipo(tipo,true); if(tipo==='produto') selecionarCodigo('61091000'); document.querySelector('#regime').value=reg; ANO=ano; sincronizar(); calcular();
    const o=opcoes(), H=hoje(o), A=noAno(o,H.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn), V=visaoComprador(o,H,A), id=[tipo,reg,ano].join(' '); n++;
    if(!V){ f.push('sem visão '+id); continue; }
    const sv=tipo==='servico', icmsH=sv?0:o.pv*o.icmsVenda, pc=o.pcReg==='normal'?0.0925*(o.pv-(sv?0:o.pv*o.icmsVenda)):0;
    const [R,Pz,S]=V.perfis;
    if(!ap(R.liqH,o.pv-icmsH-pc)) f.push('real hoje '+id); if(!ap(Pz.liqH,o.pv-icmsH)) f.push('pres hoje '+id); if(!ap(S.liqH,o.pv)||!ap(S.liqA,A.nf)) f.push('simples '+id);
    const esperado=A.nf-A.cbs-A.ibs-(sv?0:A.icms); if(!ap(R.liqA,esperado)||!ap(Pz.liqA,esperado)) f.push('ano '+id+' '+R.liqA+' x '+esperado);
    if(!ap(R.dif,R.liqA-R.liqH)) f.push('dif '+id);
    if(!document.querySelector('#p-comp table')) f.push('painel '+id);
    if(tipo==='produto'&&reg==='presumido'&&ano===2027) amostra=V.perfis.map(x=>[x.nome.slice(0,22),+x.liqH.toFixed(2),+x.liqA.toFixed(2),+x.dif.toFixed(2)]);
  }
  ANO=2026; calcular(); if(document.querySelector('#p-comp table')) f.push('2026 deveria não ter tabela');
  document.querySelector('#regime').value='simples'; ANO=2027; sincronizar(); calcular(); if(document.querySelector('#p-comp table')) f.push('simples deveria não ter tabela');
  return {f,n,amostra}; });
 console.log(JSON.stringify({falhas:r.f,casos:r.n,amostra:r.amostra,errs})); await b.close(); process.exit(r.f.length||errs.length?1:0);
})();
