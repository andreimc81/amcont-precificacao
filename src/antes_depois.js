const { chromium } = require('playwright');
const arqs={antes:'/home/claude/work/historico/v2026.7-pre-auditoria-externa/amcont-produto.html', depois:'/home/claude/work/amcont-produto.html'};
(async()=>{ const b=await chromium.launch(); const R={};
 for (const [k,f] of Object.entries(arqs)){ const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('file://'+f); await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
  R[k]=await p.evaluate(()=>{
   const out={};
   // 1. credito PIS/COFINS de fornecedor Simples com ICMS fora do DAS (sublimite), comprador Lucro Real, 2026
   definirModo('compra'); definirTipo('produto',true); selecionarCodigo('84713012'); $("#regime").value='real'; $("#destino").value='revenda'; ANO=2026; sincronizar();
   const o=opcoes();
   out.pc_sublimite=creditoComprador({reg:'sn_sublimite',preco:100,icms:0.12*100,das:7.3,anexo:'I',fora:false},o).pc;
   out.pc_regular=creditoComprador({reg:'regular',preco:100,icms:12,das:0,anexo:'I',fora:false},o).pc;
   // 2. classificacoes com cClassTrib composto (mais de um codigo no campo principal)
   let comp=0, tot=0, ex=null;
   for (const c of Object.keys(DB.ncm||{}).slice(0,99999)){ let f; try{ f=classificarNcm(c);}catch(e){continue;} (f.opcoes||[f]).forEach(x=>{ tot++; if (/\d{6}\D+\d{6}/.test(String(x.ccl||''))){ comp++; if(!ex) ex=c+': '+x.ccl; } }); }
   out.composto={comp,tot,ex};
   return out; });
  R[k].errs=errs; await p.close(); }
 console.log(JSON.stringify(R,null,1)); await b.close(); })();
