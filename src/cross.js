const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
  const X=JSON.parse(fs.readFileSync('cross_xlsx.json'));
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file:///home/claude/work/amcont-produto.html');
  await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
  let ok=0;
  for (let i=0;i<X.sc.length;i++){
    const [tipo,cod,reg,ax,ah,aliq,ano,forn]=X.sc[i]; const pcx=({monofasico_fab:'monofab',monofasico:'mono'})[X.sc[i][8]]||X.sc[i][8]||'auto';
    const h=await p.evaluate(([tipo,cod,reg,ah,aliq,ano,forn,pcx])=>{
      definirTipo(tipo,true); $("#regime").value=reg; $("#setor").value=ah; $("#icms-venda").value=aliq*100; $("#forn").value=forn; $("#anexo").value="I"; $("#pc-hoje").value=pcx; ANO=ano;
      selecionarCodigo(cod); const o=opcoes(), H=hoje(o), A=noAno(o,H.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn);
      return {mc:H.mc, nf:A.tipo==="geral"?A.nf:A.trad.nf, red:o.trat, is:o.is, selo:FICHA.selo};
    },[tipo,cod,reg,ah,aliq,ano,forn,pcx]);
    const x=X.res[i]; const d=Math.abs(h.nf-x.nf), dm=Math.abs(h.mc-x.mc);
    const pass=d<0.005&&dm<0.005&&Math.abs(h.red-x.red)<1e-9&&Math.abs(h.is-(x.is||0))<1e-9&&Math.abs(x.prova)<1e-6;
    if(pass)ok++;
    console.log(pass?'OK ':'DIF',tipo,cod,reg,ano,forn,'| html',h.nf.toFixed(2),h.mc.toFixed(2),h.red,h.is,'| xlsx',x.nf.toFixed(2),x.mc.toFixed(2),x.red,x.is,x.sit);
  }
  console.log(ok+'/'+X.sc.length);
  await b.close();
})();
