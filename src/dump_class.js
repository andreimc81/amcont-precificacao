// Exporta a classificacao de todos os codigos pelo mesmo codigo JS da calculadora (fonte unica).
const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file:///home/claude/work/amcont-produto.html');
  await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
  const out = await p.evaluate(()=>{
    const pack = f => ({cod:f.cod, desc:f.desc, selo:f.selo, sel:f.sel, msg:f.msg, is:f.is===undefined?null:f.is, isNota:f.isNota||"",
      temIs:f.isNota!==undefined, avisos:f.avisos, extra:f.extra, sc:(f.tipo==='produto'&&f.cor!=='cinza')?icmsSC(f.cod):null, pc:(f.tipo==='produto'&&f.cor!=='cinza')?pcHoje(f.cod):null, ops:f.opcoes.map(o=>({rot:o.rot,red:o.red,cst:o.cst,ccl:o.ccl,base:o.base,cond:o.cond,semRed:!!o.semRed}))});
    const ncm=[]; const cods=new Set(NCM.itens.map(x=>x[0])); Object.keys(DB.ncm).forEach(c=>cods.add(c));
    [...cods].sort().forEach(c=>ncm.push(pack(classificarNcm(c))));
    const nbs=[]; [...NBSIDX.keys()].sort().forEach(c=>nbs.push(pack(classificarNbs(c))));
    const pares=[]; for (const it of DB.lc){ if (!it.n.length) pares.push({item:it.i, vazio:true});
      for (const [cod] of it.n){ const q = pack(classificarNbs(cod, it.i)); q.item = it.i; pares.push(q); } }
    return {pares,ncm,nbs,meta:DB.meta,ccl:DB.ccl,regras:DB.regras,is:DB.is,lc:DB.lc,sc:DB.sc,nbsDesc:DB.nbsDesc,P:P};
  });
  fs.writeFileSync('class_dump.json',JSON.stringify(out));
  console.log(out.ncm.length,out.nbs.length);
  await b.close();
})();
