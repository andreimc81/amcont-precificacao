const { chromium } = require('playwright'); const fs=require('fs');
const SP='/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/';
const X=JSON.parse(fs.readFileSync(SP+'cross_uf.json'));
(async()=>{ const b=await chromium.launch(); const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file:///home/claude/work/amcont-produto.html'); await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(400);
 let ok=0;
 for (let s=0;s<X.sc.length;s++){
   const [reg,ano,uf,dt,imp,dup]=X.sc[s], R=X.res[s];
   const h = await p.evaluate(([reg,ano,uf,dt,imp,dup])=>{ definirModo("venda"); definirTipo("produto", true); selecionarCodigo("18063110");
     $("#regime").value=reg; $("#icms-venda").value=18; $("#icms-compra").value=18; $("#pc").value=600; $("#pc-ano").value=600; $("#pv").value=1000; $("#forn").value="regular";
     $("#uf-dest").value=uf; $("#dest-tipo").value={contribuinte:"contrib",contribuinte_uso:"contrib_uso",final:"final"}[dt]; $("#importado").checked=imp==="S"; $("#difal-dupla").checked=dup==="S";
     $("#inc-lucro").checked=true; $("#lc224").checked=false; $("#pc-hoje").value="auto"; ANO=ano; sincronizar(); calcular();
     const o=opcoes(), H=hoje(o), A=noAno(o,H.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn);
     return {nf: A.tipo==="geral" ? A.nf : A.trad.nf, hib: A.tipo==="geral" ? null : A.hib.nf, mc:H.mc, i:o.icmsVenda}; }, [reg,ano,uf,dt,imp,dup]);
   const okk = Math.abs(h.nf-R.nf)<0.005 && Math.abs(h.mc-R.mc)<0.005 && Math.abs(h.i-R.i17)<1e-9 && Math.abs(R.prova)<1e-6;
   if (okk) ok++;
   console.log(okk?'OK ':'ERRO', X.sc[s].join(' '), '| html', h.nf.toFixed(2), h.i.toFixed(4), '| xlsx', R.nf.toFixed(2), R.i17.toFixed(4), '| prova', R.prova, '|', R.f12);
 }
 console.log(ok+'/'+X.sc.length, errs); await b.close(); })();
