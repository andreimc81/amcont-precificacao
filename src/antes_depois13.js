const { chromium } = require('playwright');
const arqs={antes:'/home/claude/work/historico/v2026.8-candidata-pre-rodada13/amcont-produto.html', depois:'/home/claude/work/amcont-produto.html'};
(async()=>{ const b=await chromium.launch(); const R={};
 for (const [k,f] of Object.entries(arqs)){ const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('file://'+f); await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
  R[k]=await p.evaluate(()=>{ const out={};
   for (const cod of ['84131100','73201000','89031200']){
     definirModo('venda'); definirTipo('produto',true); selecionarCodigo(cod); $("#regime").value='presumido'; $("#setor").value='comercio';
     $("#pv").value=1000; $("#pc").value=600; $("#pc-ano").value=600; $("#icms-venda").value=17; $("#icms-compra").value=12; $("#forn").value='regular'; $("#pc-hoje").value='auto';
     ANO=2027; sincronizar(); calcular(); const o=opcoes(), H=hoje(o), A=noAno(o,H.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn);
     out[cod]={pcReg:o.pcReg, mcHoje:+H.mc.toFixed(2), nf2027:+A.nf.toFixed(2), is:o.is}; }
   return out; });
  R[k].errs=errs; await p.close(); }
 console.log(JSON.stringify(R)); await b.close(); })();
