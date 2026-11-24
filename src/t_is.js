const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage();
 const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file:///home/claude/work/amcont-produto.html');
 await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
 const r=await p.evaluate(()=>{ const out={}; const f=[];
  const txt=()=>document.querySelector('#dica-is').textContent;
  calcular(); out.vazio=txt(); if(!/Busque o NCM/.test(out.vazio)) f.push('sem ncm');
  const sel=c=>{ definirTipo('produto',true); const cod=c; try{ selecionarCodigo(cod) }catch(e){ f.push('selecionarCodigo '+e.message) } };
  for (const [c,re,rot] of [['22021000',/sujeito ao Imposto Seletivo: al[ií]quota de 2,60%/,'refri'],['22084000',/20,00%/,'destilado'],['87032100',/modelo/,'carro'],['24022000',/modelo|regra pr[óo]pria/,'cigarro'],['18063210',/n[ãa]o consta/,'chocolate']]){ sel(c); calcular(); const t=txt(); out[rot]=t; if(!re.test(t)) f.push(rot+': '+t); }
  sel('22021000'); document.querySelector('#is').value=5; calcular(); if(!/alterado manualmente/.test(txt())) f.push('manual');
  return {f,out}; });
 console.log(JSON.stringify(r,null,1), JSON.stringify(errs)); await b.close(); process.exit(r.f.length||errs.length?1:0);
})();
