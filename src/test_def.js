const { chromium } = require('playwright');
(async()=>{ const b=await chromium.launch(); const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file:///home/claude/work/amcont-produto.html'); await p.evaluate(()=>localStorage.clear()); await p.reload();
 await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(400);
 // prova por definicao legal das bases, em 4 cenarios
 const r=await p.evaluate(()=>{ const out=[];
  for (const [cod,ano,icms,reg] of [['22084000',2032,25,'presumido'],['22030000',2027,25,'real'],['18063110',2029,17,'presumido'],['87032100',2033,12,'real']]){
   $("#regime").value=reg; $("#icms-venda").value=icms; ANO=ano; selecionarCodigo(cod); if(cod==='87032100') $("#is").value=7.6;
   const o=opcoes(), H=hoje(o), A=noAno(o,H.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn), t=tAno(ano);
   const bCbs=A.nf-A.icms-A.cbs-A.ibs, bIs=bCbs-A.impSel;
   out.push([cod,ano,+A.nf.toFixed(2),'cbs/base='+(A.cbs/bCbs).toFixed(5)+' lei='+(t.cbs*(1-o.trat)).toFixed(5),'ibs/base='+(A.ibs/bCbs).toFixed(5)+' lei='+(t.ibs*(1-o.trat)).toFixed(5),
     'is/base='+(bIs?A.impSel/bIs:0).toFixed(5)+' lei='+o.is,'icms/nf='+(A.icms/A.nf).toFixed(5)+' lei='+(o.icmsVenda*t.fatorIcmsIss).toFixed(5),'mc-dif='+(A.mc-H.mc).toExponential(1)]); }
  return out; });
 r.forEach(x=>console.log(x.join(' | ')));
 const q=await b.newPage(); q.on('pageerror',e=>errs.push(String(e)));
 await q.goto('file:///home/claude/work/amcont-precificacao.html'); await q.evaluate(()=>localStorage.clear()); await q.reload();
 await q.fill('#senha','amcont2027'); await q.keyboard.press('Enter'); await q.waitForTimeout(500);
 console.log(JSON.stringify(await q.evaluate(()=>{ MODO="custo"; $("#regime").value="real"; $("#setor").value="comercio"; $("#custo").value=499.128; $("#desp").value=10; $("#lucro").value=10; $("#imposto").value=12; $("#reducao").value="0";
   const out={padrao:$("#premissa").value}; for (const a of [2026,2027,2033]){ ANO=a; out[a]=["prof","lc","plp"].map(pr=>+rodar(pr).r.NF.toFixed(2)); } return out; })), errs);
 await b.close(); })();
