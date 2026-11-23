// Coleta casos aleatorios da calculadora (entradas, parametros e resultados) para a verificacao independente em Python
const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{
  const b=await chromium.launch(); const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('file:///home/claude/work/amcont-produto.html'); await p.fill('#senha','amcont2027'); await p.click('#form-gate button'); await p.waitForSelector('#app:not([hidden])');
  const out = await p.evaluate(()=>{
    let seed=7; const rnd=()=>{ seed=(seed*16807)%2147483647; return seed/2147483647; }, pick=a=>a[Math.floor(rnd()*a.length)];
    const venda=[], compra=[];
    const cods=['18063110','10063021','22030000','30049099','02013000','84713012','61091000','22021000','08119000'];
    for (let k=0;k<160;k++){
      const tipo = rnd()<0.8 ? 'produto':'servico';
      definirModo('venda'); definirTipo(tipo,true);
      if (tipo==='produto') selecionarCodigo(pick(cods)); else selecionarCodigo(pick(['123012200','115021000','101011100']));
      $("#regime").value=pick(['presumido','real','simples']); $("#setor").value= tipo==='produto' ? pick(['comercio','industria']) : pick(['servicos','hospitalar']);
      $("#pv").value=(200+Math.floor(rnd()*1800)); $("#pc").value=(50+Math.floor(rnd()*900)); $("#pc-ano").value=(50+Math.floor(rnd()*900));
      $("#icms-venda").value=pick(tipo==='produto'?[7,12,17,25]:[2,3,5]); $("#icms-compra").value=pick([0,4,7,12,17]);
      $("#forn").value=pick(['regular','sn_regular','sn_tradicional','sn_sublimite','mei','pf']); $("#aliqsn-forn").value=pick([4,7.3,9.5,12]);
      $("#pc-hoje").value=pick(['auto','normal','mono','zero']); $("#inc-lucro").checked=rnd()<0.6; $("#lc224").checked=false;
      $("#uf-dest").value='SC'; if (tipo==='produto' && rnd()<0.3){ $("#uf-dest").value=pick(['RS','BA','RJ','SP','PE']); $("#dest-tipo").value=pick(['contrib','final']); $("#difal-dupla").checked=rnd()<0.5; }
      ANO=pick([2026,2027,2028,2029,2030,2031,2032,2033]); sincronizar(); calcular();
      const o=opcoes(), H=hoje(o), A=noAno(o,H.mc,o.pcAno,o.forn,o.aliqForn,o.anexoForn), t=tAno(o.ano);
      venda.push({o:{regime:o.regime,servico:o.servico,ano:o.ano,pv:o.pv,pc:o.pc,pcAno:o.pcAno,icmsVenda:o.icmsVenda,icmsCompra:o.icmsCompra,
        forn:o.forn,aliqForn:o.aliqForn,trat:o.trat,is:o.is||0,r:o.r,pis:o.pis,cofins:o.cofins,pcReg:o.pcReg,pcConc:o.pcConc,aliqSN:o.aliqSN,anexo:o.anexo},
        t, anexos:P.simplesAnexos, H:{mc:H.mc}, A:{tipo:A.tipo, nf:A.tipo==='geral'?A.nf:null, trad:A.tipo==='geral'?null:A.trad.nf, mc:A.mc}});
    }
    definirModo('compra');
    for (let k=0;k<160;k++){
      const tipo = rnd()<0.8 ? 'produto':'servico'; definirTipo(tipo,true); selecionarCodigo(tipo==='produto'?pick(cods):'115021000');
      $("#regime").value=pick(['presumido','real','simples']); $("#sn-opcao").value=pick(['das','regular']); $("#destino").value=pick(['revenda','uso','imob']);
      $("#icms-venda").value=pick([12,17,25]); $("#difal-dupla").checked=rnd()<0.5; $("#pc-hoje").value=pick(['auto','normal','mono']); ANO=pick([2026,2027,2029,2031,2033]);
      sincronizar();
      const c={reg:pick(['regular','sn_regular','sn_tradicional','sn_sublimite','mei','pf']), preco:50+Math.floor(rnd()*950), icms:pick([0,4,7,12,17,18]), das:pick([4,7.3,9.5,12]), anexo:pick(['I','II','III']), fora:rnd()<0.3};
      const o=opcoes(), k2=creditoComprador(c,o);
      compra.push({o:{regime:o.regime,snReg:o.snReg,destino:o.destino,servico:o.servico,ano:o.ano,trat:o.trat,icmsSC:o.icmsSC,difalDupla:o.difalDupla,pis:o.pis,cofins:o.cofins,pcReg:o.pcReg},
        t:tAno(o.ano), anexos:P.simplesAnexos, c, k:{cbsIbs:k2.cbsIbs,icms:k2.icms,pc:k2.pc,difal:k2.difal,custo:k2.custo}});
    }
    return {venda, compra};
  });
  fs.writeFileSync('ref_casos.json', JSON.stringify(out)); console.log(out.venda.length, out.compra.length, errs); await b.close();
})();
