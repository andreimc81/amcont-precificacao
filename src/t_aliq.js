const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1280,height:900}});
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file:///home/claude/work/amcont-produto.html');
 await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
 const r=await p.evaluate(()=>{ const f=[]; 
  const prova=(rot)=>{ for(const tipo of ['produto','servico']) for(const reg of ['presumido','real','simples']){ definirTipo(tipo,true); try{$("#regime").value=reg}catch(e){}
    for(const ano of [2027,2029,2031,2033]){ ANO=ano; calcular(); const o=opcoes(),H=hoje(o);
      const L=linhaAno(o,H,ano); const A=noAno(o,H.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn);
      const nf=A.tipo==='geral'?A.nf:A.hib.nf; if(Math.abs(L.nf-nf)>0.005) f.push([rot,'nf',tipo,reg,ano].join(' '));
      if(L.M && A.tipo==='geral'){ const R=noAno(o,L.M.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn); if(Math.abs(R.nf-o.pv)>0.005) f.push([rot,'prova',tipo,reg,ano,R.nf].join(' ')); } } } };
  prova('previsto');
  document.querySelector('#al-dcbs').value=2; document.querySelector('#al-dibs').value=3; document.querySelector('#al-aplicar').click();
  const alt=aliqAlterada(); if(!alt) f.push('nao detectou alteracao'); if(document.querySelector('#aviso-aliq').hidden) f.push('aviso oculto');
  const c27=P.transicao.find(t=>t.ano===2027).cbs; if(Math.abs(c27-(TRANS0[1].cbs+0.02))>1e-9) f.push('cbs +2pp errado '+c27);
  const i33=P.transicao.find(t=>t.ano===2033).ibs; if(Math.abs(i33-(TRANS0[7].ibs+0.03))>1e-9) f.push('ibs 33 errado '+i33);
  prova('editado');
  document.querySelector('#al-reset').click(); if(aliqAlterada()) f.push('reset falhou'); if(!document.querySelector('#aviso-aliq').hidden) f.push('aviso nao sumiu');
  return f; });
 console.log(JSON.stringify({falhas:r,errs})); await b.close(); process.exit(r.length||errs.length?1:0);
})();
