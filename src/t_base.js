const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file:///home/claude/work/amcont-produto.html');
 await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
 const r=await p.evaluate(()=>{ const f=[]; let n=0; const ap=(a,b)=>Math.abs(a-b)<0.005; const amostra={};
  for (const [tipo,cod] of [['produto','61091000'],['produto','22030000'],['servico',null]]) for (const reg of ['presumido','real']) for (const ano of [2027,2029,2031,2033]){
    definirTipo(tipo,true); if (cod) selecionarCodigo(cod); document.querySelector('#regime').value=reg; ANO=ano;
    const res={};
    for (const fl of ['0','1']){ document.querySelector('#base-sem').value=fl; sincronizar(); calcular();
      const o=opcoes(), H=hoje(o), A=noAno(o,H.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn), id=[tipo,cod,reg,ano,'base-sem='+fl].join(' '); n++;
      if (A.tipo!=='geral'){ f.push('tipo '+id); continue; }
      const baseI = fl==='1' ? A.nf-A.cbs-A.ibs : A.nf;
      if (!ap(A.icms, A.i*baseI)) f.push('icms '+id+' '+A.icms+' x '+A.i*baseI);
      const bc = A.nf-A.icms-A.cbs-A.ibs;
      if (!ap(A.cbs, A.c*bc) || !ap(A.ibs, A.b*bc)) f.push('cbs ibs '+id);
      if (o.is>0 && !ap(A.impSel, o.is*(bc-A.impSel))) f.push('IS '+id);
      if (!ap(A.mc, H.mc)) f.push('margem '+id+' '+A.mc+' x '+H.mc);
      const M=mesmoDesembolso(o,A); if (M){ const R=noAno(o,M.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn); if(!ap(R.nf,o.pv)) f.push('mesmo desembolso '+id+' '+R.nf);
        if (!ap(M.cad+M.cbs+M.ibs, o.pv)) f.push('md soma '+id); }
      res[fl]=A.nf; if (tipo==='produto'&&cod==='61091000'&&reg==='presumido'&&ano===2033) amostra[fl]={nf:+A.nf.toFixed(2),cad:+(A.nf-A.cbs-A.ibs).toFixed(2),icms:+A.icms.toFixed(2)};
    }
    if (!(res['1'] < res['0'] + 1e-9)) f.push('sem base deveria custar menos ou igual: '+[tipo,cod,reg,ano,res['0'],res['1']].join(' '));
  }
  document.querySelector('#base-sem').value='0'; calcular();
  return {f,n,amostra}; });
 console.log(JSON.stringify({falhas:r.f,casos:r.n,amostra:r.amostra,errs})); await b.close(); process.exit(r.f.length||errs.length?1:0);
})();
