// R27-06: no Simples (venda) os campos de ICMS, base e destino somem e não alteram o resultado
const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch(); const p=await b.newPage({viewport:{width:1348,height:900}}); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file://'+process.cwd()+'/amcont-produto.html'); await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
 const r = await p.evaluate(()=>{ const f=[]; let casos=0; const vis=id=>{const e=document.querySelector(id); return !!e && e.offsetHeight>0;};
  const set=(id,v)=>{const e=document.querySelector(id); e.value=v; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true}));};
  const snap=()=>{const o=opcoes(), H=hoje(o); return JSON.stringify(P.transicao.map(t=>{const oo=Object.assign({},o,{ano:t.ano}); const A=noAno(oo,H.mc,oo.pcAno,oo.forn,oo.aliqForn,oo.anexoForn); const M=mesmoDesembolso(oo,A); return [H.mc,A.trad&&A.trad.nf,A.hib&&A.hib.nf,M&&M.hib&&M.hib.mc,M&&M.trad&&M.trad.mc].map(x=>x==null?null:Math.round(x*100)/100);}));};
  for (const tipo of ['produto','servico']){ definirTipo(tipo,true); if(tipo==='produto') selecionarCodigo('61091000');
   set('#regime','simples'); calcular(); casos++;
   for (const id of ['#icms-venda','#c-dest','#c-dupla']) if (vis(id)) f.push(tipo+' visivel '+id);
   if (/ICMS em Santa Catarina/.test(document.querySelector('#ficha').textContent)) f.push(tipo+' ficha mostra ICMS SC');
   if (/ICMS \d|ISS \d/.test(document.querySelector('#prem-res').textContent)) f.push(tipo+' resumo mostra ICMS');
   const a=snap(); set('#icms-venda','7'); const b1=snap(); if(a!==b1) f.push(tipo+' aliquota altera resultado do Simples');
   if (tipo==='produto'){ set('#uf-dest','SP'); const c=snap(); if(a!==c) f.push('destino altera resultado do Simples '+a+' '+c); set('#uf-dest','SC'); }
   set('#icms-venda','18');
   for (const reg of ['presumido','real']){ set('#regime',reg); calcular(); casos++;
     if (!vis('#icms-venda')) f.push(tipo+' '+reg+' sem campo de aliquota'); 
     if (tipo==='produto' && !vis('#c-dest')) f.push(reg+' sem destino');
     if (tipo==='produto' && !/ICMS em Santa Catarina/.test(document.querySelector('#ficha').textContent)) f.push(reg+' ficha sem ICMS SC'); }
  }
  definirTipo('produto',true); set('#regime','simples'); const bc=[...document.querySelectorAll('#modo button')].find(x=>/compra/i.test(x.textContent)); bc.click(); calcular(); casos++;
  if (!vis('#icms-venda')) f.push('compra no Simples perdeu a aliquota interna do DIFAL');
  return {falhas:f, casos}; });
 r.errs=errs; console.log(JSON.stringify(r)); await b.close(); process.exit(r.falhas.length||errs.length?1:0);})();
