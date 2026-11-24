# ===== rodada 23 (versão 2026.8.10): R23-01 a R23-03 =====
# R23-01: o destaque do preço passa a mostrar o valor do produto/serviço a cadastrar, com CBS e IBS separados e o total da nota abaixo
# R23-02: cenário "mesmo desembolso do cliente": o total da nota fica no preço de hoje e a ferramenta mostra a margem que sobra
# R23-03: a nota fiscal usa o mesmo nome, "valor a cadastrar", para o primeiro item
s=sub1(s,"""function desenharNotaVenda(o, A){""","""/* R23-02: o cliente continua desembolsando o preço de hoje (produto mais CBS e IBS por fora). Usa as mesmas fórmulas de noAno,
   com o total da nota fixado em o.pv, e devolve o valor a cadastrar e a margem que sobra. Antes de 2027 não há efeito. */
function mesmoDesembolso(o, A){
  if (o.ano < 2027) return null;
  const pv = o.pv;
  if (A.tipo === "geral"){
    const i = A.i, c = A.c, b = A.b, s = o.is, k = (1-i)*(c+b)/(1+c+b), sg = s*(1-i-k)/(1+s);
    const icms = pv*i, bc = pv*(1-i)/(1+c+b), cbs = bc*c, ibs = bc*b, impSel = pv*sg, lucro = o.r*pv*(1-k-sg);
    const trib = icms + cbs + ibs + impSel + lucro - A.cred.total;
    return {tipo:"geral", nf:pv, cad:pv - cbs - ibs, cbs, ibs, mc:pv - o.pcAno - trib};
  }
  const t = tAno(o.ano), an = P.simplesAnexos[o.anexo] || P.simplesAnexos.I;
  const aliqT = o.aliqSN;
  const Th = o.aliqSN * (1 - an.pis - an.cofins - (an.icms+an.iss)*(1-t.fatorIcmsIss));
  const Kb = 1 - o.aliqSN * (an.cpp + an.ipi + (an.icms+an.iss)*t.fatorIcmsIss);
  const pH = pv/(1 + Kb*(A.c + A.b)), cbsH = pH*Kb*A.c, ibsH = pH*Kb*A.b;
  return {tipo:"simples", trad:{nf:pv, mc:pv*(1-aliqT) - o.pcAno},
          hib:{nf:pv, cad:pH, cbs:cbsH, ibs:ibsH, mc:pH - o.pcAno - pH*Th + A.cred.cbsIbs}};
}
function blocoMesmoDesembolso(o, A, H){
  const M = mesmoDesembolso(o, A); if (!M) return "";
  const un = o.servico ? "serviço" : "produto";
  const alvo = M.tipo === "geral" ? A.mc : H.mc;
  const par = (x, rot) => {
    const perda = alvo - x.mc, pc = alvo > 0.005 ? perda/alvo : 0;
    return {perda, pc, txt: perda > 0.005
      ? `Sem repassar o aumento da carga tributária, a margem de contribuição cai de <b>${BRL.format(alvo)}</b> para <b>${BRL.format(x.mc)}</b>: redução de <b class="neg">${BRL.format(perda)}</b> por unidade (<b class="neg">${PCT(pc)}</b> da margem).`
      : `Nesta combinação a carga tributária não aumenta: o cliente paga o mesmo e a margem se mantém em <b>${BRL.format(x.mc)}</b>, sem perda.`};
  };
  const cab = `<div class="destaque" style="margin-top:20px;padding-top:16px;border-top:1px dashed var(--linha)">`;
  if (M.tipo === "geral"){
    const r = par(M);
    return cab + `<div class="rot">Mantendo o mesmo desembolso do cliente</div>`
      + `<div class="val">${BRL.format(M.cad)}</div>`
      + `<div class="cmp">Valor do ${un} a cadastrar para que o valor do ${un} mais CBS e IBS (<b>${BRL.format(M.cbs + M.ibs)}</b>) somem os mesmos <b>${BRL.format(o.pv)}</b> que o cliente paga hoje. ${r.txt}</div></div>`
      + li("Valor do "+un+" a cadastrar", M.cad, "g")
      + li("CBS e IBS, somados por fora", M.cbs + M.ibs, "g")
      + li("Total da nota, igual ao de hoje", M.nf, "sum")
      + li("Margem de contribuição preservada", alvo, "g")
      + li("Margem de contribuição neste cenário", M.mc, "sum")
      + li(r.perda > 0.005 ? "Redução da margem por unidade" : "Variação da margem por unidade", -r.perda, "trib")
      + `<p class="dica" style="margin-top:9px">Compare com o painel acima: para manter a margem, o valor a cadastrar é de <b>${BRL.format(A.nf - A.cbs - A.ibs)}</b>
         e o cliente paga <b>${BRL.format(A.nf)}</b>. Repassar ou absorver a diferença de <b>${BRL.format(A.nf - o.pv)}</b> na nota é uma decisão comercial.</p>`;
  }
  const rt = par(M.trad), rh = par(M.hib);
  return cab + `<div class="rot">Mantendo o mesmo desembolso do cliente</div>`
    + `<div class="cmp">O total da nota fica em <b>${BRL.format(o.pv)}</b>, o preço de hoje.</div></div>`
    + `<table class="cmp"><thead><tr><th></th><th>Simples tradicional</th><th>Optante do regime regular</th></tr></thead><tbody>`
    + `<tr><td>Valor do ${un} a cadastrar</td><td>${BRL.format(M.trad.nf)}</td><td>${BRL.format(M.hib.cad)}</td></tr>`
    + `<tr><td>CBS e IBS, somados por fora</td><td>${BRL.format(0)}</td><td>${BRL.format(M.hib.cbs + M.hib.ibs)}</td></tr>`
    + `<tr><td>Margem de contribuição neste cenário</td><td>${BRL.format(M.trad.mc)}</td><td>${BRL.format(M.hib.mc)}</td></tr>`
    + `<tr><td>Margem preservada</td><td>${BRL.format(alvo)}</td><td>${BRL.format(alvo)}</td></tr>`
    + `<tr><td>Redução da margem</td><td class="${rt.perda>0.005?"neg":""}">${BRL.format(rt.perda)}</td><td class="${rh.perda>0.005?"neg":""}">${BRL.format(rh.perda)}</td></tr>`
    + `</tbody></table>`
    + `<p class="dica" style="margin-top:9px">${rh.txt.replace("a margem de contribuição cai","no regime regular a margem de contribuição cai")}</p>`;
}
function desenharNotaVenda(o, A){""")
# destaque do preço: valor a cadastrar em evidência, CBS e IBS separados, total da nota logo abaixo (a partir de 2027)
s=sub1(s,"""      + `<div class="destaque"><div class="rot">Preço de venda por unidade</div>`
      + `<div class="val">${BRL.format(A.nf)}</div>`
      + `<div class="cmp">Contra <b>${BRL.format(o.pv)}</b> hoje, variação de `
      + `<b class="${dif>=0?"neg":"pos"}">${dif>=0?"+":""}${PCT(dif)}</b>. `
      + `Margem de contribuição preservada em <b>${BRL.format(A.mc)}</b>.</div></div>`""","""      + (ANO >= 2027
        ? `<div class="destaque"><div class="rot">Valor do ${o.servico?"serviço":"produto"} a cadastrar no emissor</div>`
          + `<div class="val">${BRL.format(A.nf - A.cbs - A.ibs)}</div>`
          + `<div class="cmp">Mais CBS e IBS por fora, <b>${BRL.format(A.cbs + A.ibs)}</b>. Total da nota, o que o cliente paga: <b>${BRL.format(A.nf)}</b>, `
          + `contra <b>${BRL.format(o.pv)}</b> hoje (<b class="${dif>=0?"neg":"pos"}">${dif>=0?"+":""}${PCT(dif)}</b>). `
          + `Com este valor a margem de contribuição fica preservada em <b>${BRL.format(A.mc)}</b>.</div></div>`
        : `<div class="destaque"><div class="rot">Preço de venda por unidade</div>`
          + `<div class="val">${BRL.format(A.nf)}</div>`
          + `<div class="cmp">Contra <b>${BRL.format(o.pv)}</b> hoje, variação de `
          + `<b class="${dif>=0?"neg":"pos"}">${dif>=0?"+":""}${PCT(dif)}</b>. `
          + `Margem de contribuição preservada em <b>${BRL.format(A.mc)}</b>.</div></div>`)""")
s=sub1(s,"""      + `<p class="dica" style="margin-top:9px">Se o seu comprador for contribuinte do regime regular,""","""      + blocoMesmoDesembolso(o, A, H)
      + `<p class="dica" style="margin-top:9px">Se o seu comprador for contribuinte do regime regular,""")
# Simples: opção pelo regime regular também mostra o valor a cadastrar
s=sub1(s,"""      + `<div class="val">${BRL.format(A.hib.nf)}</div>`
      + `<div class="cmp">Variação de <b class="${d2>=0?"neg":"pos"}">${d2>=0?"+":""}${PCT(d2)}</b>
         contra hoje. Aproveita""","""      + `<div class="val">${BRL.format(A.hib.preco)}</div>`
      + `<div class="cmp">Valor a cadastrar no emissor, mais CBS e IBS por fora de <b>${BRL.format(A.hib.cbs + A.hib.ibs)}</b>.
         Total da nota <b>${BRL.format(A.hib.nf)}</b>, variação de <b class="${d2>=0?"neg":"pos"}">${d2>=0?"+":""}${PCT(d2)}</b>
         contra hoje. Aproveita""")
s=sub1(s,"""      + `<p class="dica" style="margin-top:9px">A margem é a mesma nas duas.
         A decisão está no painel de comparação abaixo.</p>`;""","""      + blocoMesmoDesembolso(o, A, H)
      + `<p class="dica" style="margin-top:9px">A margem é a mesma nas duas.
         A decisão está no painel de comparação abaixo.</p>`;""")
# R23-03: nota fiscal
s=sub1(s,"""R = [["Valor do "+(o.servico?"serviço":"produto")+" (com "+imp+(A.impSel>0.005?" e Imposto Seletivo embutidos)":" embutido)"), A.nf - A.cbs - A.ibs],""","""R = [["Valor do "+(o.servico?"serviço":"produto")+" a cadastrar (com "+imp+(A.impSel>0.005?" e Imposto Seletivo embutidos)":" embutido)"), A.nf - A.cbs - A.ibs],""")
