const { chromium } = require('playwright');
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file:///home/claude/work/amcont-produto.html');
 await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
 const f=await p.evaluate(()=>{const f=[]; const av=c=>{ definirTipo('produto',true); selecionarCodigo(c); return FICHA.avisos.join(' || '); };
  const tem=(c,re,rot)=>{ if(!re.test(av(c))) f.push('faltou '+rot+' em '+c); }, nao=(c,re,rot)=>{ if(re.test(av(c))) f.push('sobrou '+rot+' em '+c); };
  tem('03044300',/trata a subposição inteira como excluída/,'peixe'); nao('03043100',/subposição inteira/,'peixe'); nao('03044100',/subposição inteira/,'peixe (salmão já integral)');
  tem('90183211',/art\. 144, II/,'Anexo IV'); tem('85171100',/art\. 145, II/,'Anexo V'); tem('28273931',/art\. 146, § 2º/,'Anexo VI');
  tem('07020000',/cClassTrib 200038/,'Anexo IX'); nao('10063021',/Receita Federal/,'arroz'); nao('22030000',/administração pública/,'cerveja');
  if (DB.ccl['220001']||DB.ccl['220002']||DB.ccl['220003']) f.push('cClassTrib encerrado presente');
  for (const k of ['221002','221003','221004','200054','200055','000006']) if(!DB.ccl[k]) f.push('cClassTrib faltando '+k);
  if (!/CBS é reduzida a zero/.test(DB.ccl['200025'][3])) f.push('aviso Prouni');
  return f; });
 console.log(JSON.stringify({falhas:f,errs})); await b.close(); process.exit(f.length||errs.length?1:0);
})();
