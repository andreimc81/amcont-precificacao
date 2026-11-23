const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
  const X=JSON.parse(fs.readFileSync('cross_amplo.json'));
  const b = await chromium.launch(); const p = await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('file:///home/claude/work/amcont-produto.html');
  await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
  let ok=0, falhas=[];
  for (let i=0;i<X.sc.length;i++){
    const s=X.sc[i], x=X.res[i]; const pcx=({monofasico_fab:'monofab',monofasico:'mono'})[s.pcx]||s.pcx;
    const h=await p.evaluate(([s,pcx])=>{
      definirModo("venda"); definirTipo(s.tipo,true); $("#regime").value=s.reg; $("#setor").value=s.ah; $("#icms-venda").value=s.aliq*100;
      $("#forn").value=s.forn; $("#aliqsn-forn").value=s.das*100; $("#anexo").value="I"; $("#pc-hoje").value=pcx; ANO=s.ano;
      $("#uf-dest").value=s.uf; $("#dest-tipo").value={contribuinte:"contrib",contribuinte_uso:"contrib_uso",final:"final"}[s.dt];
      $("#importado").checked=s.imp==="S"; $("#difal-dupla").checked=s.dup==="S";
      selecionarCodigo(s.cod); sincronizar(); const o=opcoes(), H=hoje(o), A=noAno(o,H.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn);
      return {mc:H.mc, nf:A.tipo==="geral"?A.nf:A.trad.nf, hib:A.tipo==="geral"?null:A.hib.nf, red:o.trat, is:o.is, i:o.icmsVenda};
    },[s,pcx]);
    const pass=Math.abs(h.nf-x.nf)<0.005&&Math.abs(h.mc-x.mc)<0.005&&Math.abs(h.red-x.red)<1e-9&&Math.abs(h.is-(x.is||0))<1e-9&&Math.abs(x.prova)<1e-6
      &&(h.hib===null||Math.abs(h.hib-x.hib)<0.005)&&Math.abs(h.i-x.i17)<1e-9&&Math.abs(x.nfprova||0)<1e-6;
    if(pass)ok++; else falhas.push([i,s,h,x]);
  }
  console.log(ok+'/'+X.sc.length); falhas.slice(0,6).forEach(f=>console.log(JSON.stringify(f)));
  console.log(errs); await b.close();
})();
