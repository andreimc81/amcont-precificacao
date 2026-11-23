const { chromium } = require('playwright');
(async()=>{
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1280,height:1500}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e))); p.on('console',m=>{if(m.type()==='error'&&!/net::|Failed to load/.test(m.text()))errs.push(m.text())});
  await p.goto('file:///home/claude/work/amcont-produto.html');
  await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
  const R = async (tipo,cod)=> await p.evaluate(([tipo,cod])=>{ if(TIPO!==tipo) definirTipo(tipo,true); selecionarCodigo(cod);
     const A=noAno(opcoes(),hoje(opcoes()).mc,opcoes().pcAno,opcoes().forn,opcoes().aliqForn,"I");
     return {selo:FICHA.selo, cor:FICHA.cor, sel:FICHA.sel, ops:FICHA.opcoes.map(o=>[o.red,o.cst,o.ccl,o.rot.slice(0,40)]), trat:$("#trat").value, is:$("#is").value, isNota:(FICHA.isNota||'').slice(0,50), nf:A.nf&&+A.nf.toFixed(2), extra:FICHA.extra.map(x=>x[0]+': '+x[1].slice(0,70))}; },[tipo,cod]);
  for (const c of ['10063021','22021000','22030000','87032100','18063110','30049099','06011000','08051000','99999999','07129010','24022000','27101259','04012010','62052000'])
    console.log(c, JSON.stringify(await R('produto',c)));
  for (const c of ['123012200','115021000','122012000','101011100','999999999','117011000'])
    console.log(c, JSON.stringify(await R('servico',c)));
  console.log(JSON.stringify(await p.evaluate(()=>[buscarNbs('04.01'),buscarNbs('consultoria').slice(0,4),buscarNbs('1.2301').slice(0,3),buscarNbs('advoca').slice(0,3),buscarNbs('17.14').slice(0,3)])));
  // UI flow
  await p.evaluate(()=>definirTipo('produto',true));
  await p.fill('#ncm','0601.10.00'); await p.waitForTimeout(200);
  await p.click('#ficha input[value="1"]'); await p.waitForTimeout(100);
  console.log('ui', await p.evaluate(()=>[FICHA.sel,$("#trat").value,document.querySelector('#p-ano .val').textContent]));
  await p.selectOption('#trat','0'); await p.waitForTimeout(100);
  console.log('manual', await p.evaluate(()=>[...document.querySelectorAll('#ficha .f-al')].map(x=>x.textContent.slice(0,80))));
  await p.fill('#ncm','choco'); await p.waitForTimeout(150);
  console.log('lista', await p.evaluate(()=>document.querySelectorAll('#ncm-lista div').length));
  await p.fill('#ncm','10063021'); await p.waitForTimeout(200);
  await p.screenshot({path:'/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/prod.png',fullPage:false});
  await p.evaluate(()=>{definirTipo('servico',true); selecionarCodigo('123012200');});
  await p.screenshot({path:'/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/serv.png',fullPage:false});
  console.log('ERRS',errs);
  await b.close();
})();
