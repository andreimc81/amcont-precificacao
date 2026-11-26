# ===== rodada 31 (versão 2026.8.19): R27-03 visão do comprador (custo líquido de quem compra, hoje e no ano simulado) =====
s=sub1(s,"""const ABAS = [["hoje","Como é hoje"],["ano","Preço necessário"],["md","Mesmo desembolso"],""","""const ABAS = [["hoje","Como é hoje"],["ano","Preço necessário"],["comp","Visão do comprador"],["md","Mesmo desembolso"],""")
s=sub1(s,"""body.modo-compra #aba-md,""","""body.modo-compra #aba-md,body.modo-compra #aba-comp,""")
s=sub1(s,"""  cont.hoje.appendChild($("#p-hoje"));""","""  const pcp = document.createElement("div"); pcp.className = "painel so-venda"; pcp.id = "p-comp"; cont.comp.appendChild(pcp);
  cont.hoje.appendChild($("#p-hoje"));""")
s=sub1(s,"""function montarNav(){""","""/* R27-03: custo líquido do comprador. Premissa: o comprador usa o item na atividade e tem direito aos créditos do regime dele.
   Hoje: crédito de ICMS (produto) para contribuinte do regime normal; crédito de PIS e COFINS de 9,25% só no Lucro Real e só se a venda é tributada.
   No ano simulado: crédito de CBS e IBS destacados (regime regular, que inclui Lucro Real e Presumido) e do ICMS que ainda existir. */
function visaoComprador(o, H, A){
  if (!A || A.tipo !== "geral" || o.ano < 2027) return null;
  // venda para outro estado: o comprador contribuinte só se credita do ICMS interestadual; o DIFAL não gera crédito
  const sv = !!o.servico, txI = o.fora ? o.icmsInter : o.icmsVenda, icmsH = sv ? 0 : o.pv * txI, pcOn = o.pcReg === "normal";
  const pcReal = pcOn ? 0.0925 * (sv ? o.pv : o.pv - o.pv * o.icmsVenda) : 0;
  const icmsA = sv ? 0 : (o.icmsVenda > 0 ? A.icms * txI / o.icmsVenda : 0), ci = A.cbs + A.ibs;
  const perfil = (nome, crH, crA) => ({nome, pagaH:o.pv, crH, liqH:o.pv - crH, pagaA:A.nf, crA, liqA:A.nf - crA, dif:(A.nf - crA) - (o.pv - crH), pdif:((A.nf - crA) - (o.pv - crH)) / (o.pv - crH)});
  return {icmsH, pcReal, icmsA, ci, perfis:[
    perfil("Comprador do Lucro Real", icmsH + pcReal, icmsA + ci),
    perfil("Comprador do Lucro Presumido", icmsH, icmsA + ci),
    perfil("Comprador do Simples Nacional (tudo no DAS) ou consumidor final", 0, 0)]};
}
function htmlComprador(o, H, A){
  const V = visaoComprador(o, H, A), un = o.servico ? "serviço" : "produto";
  if (!V) return `<h3>Visão do comprador <em>${ANO}</em></h3><p class="dica">` + (o.ano < 2027 ? "Em 2026 a CBS e o IBS não alteram o preço nem o custo de quem compra. Escolha um ano de 2027 em diante na barra do topo."
    : "Este quadro vale para o vendedor do Lucro Presumido ou do Lucro Real. No Simples Nacional, o crédito que o comprador toma depende de como a sua empresa recolhe a CBS e o IBS: veja a comparação na aba Preço necessário.") + `</p>`;
  const sg = x => (x >= 0 ? "+" : "-") + BRL.format(Math.abs(x)), cl = x => x > 0.005 ? "neg" : (x < -0.005 ? "pos" : "");
  const P0 = V.perfis[0], P1 = V.perfis[1];
  let h = `<h3>Visão do comprador <em>${ANO}</em></h3>`
    + `<div class="destaque"><div class="rot">Custo líquido de quem compra de você, no preço que preserva a sua margem</div>`
    + `<div class="cmp">O cliente paga <b>${BRL.format(A.nf)}</b> na nota, contra <b>${BRL.format(o.pv)}</b> hoje. Mas a CBS e o IBS destacados (<b>${BRL.format(V.ci)}</b>) viram crédito para o comprador do regime regular. `
    + `Para um comprador do Lucro Presumido, o custo líquido ${P1.dif < 0 ? "cai" : "sobe"} de <b>${BRL.format(P1.liqH)}</b> para <b>${BRL.format(P1.liqA)}</b> (<b class="${cl(P1.dif)}">${sg(P1.dif)}</b> por unidade). `
    + `Para um comprador do Lucro Real, vai de <b>${BRL.format(P0.liqH)}</b> para <b>${BRL.format(P0.liqA)}</b> (<b class="${cl(P0.dif)}">${sg(P0.dif)}</b>).</div></div>`
    + `<div class="rolar"><table class="todos" id="tb-comp"><thead><tr><th>Quem compra</th><th>Paga hoje</th><th>Créditos hoje</th><th>Custo líquido hoje</th><th>Paga em ${ANO}</th><th>Créditos em ${ANO}</th><th>Custo líquido em ${ANO}</th><th>Diferença</th></tr></thead><tbody>`
    + V.perfis.map(p=>`<tr><td>${p.nome}</td><td>${BRL.format(p.pagaH)}</td><td>${BRL.format(p.crH)}</td><td>${BRL.format(p.liqH)}</td><td>${BRL.format(p.pagaA)}</td><td>${BRL.format(p.crA)}</td><td><b>${BRL.format(p.liqA)}</b></td><td class="${cl(p.dif)}">${sg(p.dif)} (${(p.pdif >= 0 ? "+" : "") + PCT(p.pdif)})</td></tr>`).join("")
    + `</tbody></table></div>`
    + `<p class="dica" style="margin-top:8px"><b>Créditos considerados.</b> Hoje: ${o.servico ? "" : "ICMS de " + BRL.format(V.icmsH) + " para o comprador contribuinte do regime normal; "}PIS e COFINS de ${BRL.format(V.pcReal)} (9,25%) só para o comprador do Lucro Real${o.pcReg === "normal" ? "" : ", zerados porque esta venda não é tributada normalmente por PIS e COFINS"}. `
    + `Em ${ANO}: CBS e IBS de ${BRL.format(V.ci)}${o.servico ? "" : " e ICMS de " + BRL.format(V.icmsA)}. O PIS e a COFINS deixam de existir em 2027.</p>`
    + `<p class="dica"><b>Condições.</b> O quadro supõe que o comprador usa o ${un} na atividade dele e tem direito ao crédito. O crédito de CBS e IBS depende do documento fiscal e do pagamento do tributo (LC 214/2025, art. 47). `
    + `O comprador desembolsa o total da nota e recupera o crédito na apuração, o que pesa no caixa dele até lá. Comprador do Simples Nacional que recolhe tudo no DAS e consumidor final não tomam crédito: para eles, o custo é o total da nota. `
    + `Se o comprador for do Simples e optar por recolher a CBS e o IBS fora do DAS, passa a tomar esse crédito.</p>`;
  return h;
}
function montarNav(){""")
s=sub1(s,"""  const pmd = $("#p-md"); if (!pmd) return;""","""  { const pcp = $("#p-comp"); if (pcp){ const Hc = hoje(o); pcp.innerHTML = htmlComprador(o, Hc, noAno(o, Hc.mc, o.pcAno, o.forn, o.aliqForn, o.anexoForn)); } }
  const pmd = $("#p-md"); if (!pmd) return;""")
# relatório: seção da visão do comprador e conceito de markup
s=sub1(s,"""    S.push(["Mantendo o mesmo desembolso do cliente em " + ANO,""","""    S.push(["Visão do comprador em " + ANO, limpo($("#p-comp"))]);
    S.push(["Mantendo o mesmo desembolso do cliente em " + ANO,""")
s=sub1(s,"""        + `<p><b>Por que ela é a referência.</b>""","""        + `<p><b>Não confunda com markup nem com margem de lucro.</b> Markup é o multiplicador aplicado sobre o custo para formar o preço: preço dividido pelo custo${o.pc > 0 ? " (neste estudo, " + String((o.pv / o.pc).toFixed(2)).replace(".", ",") + ")" : ""}. Margem de lucro é o que sobra do preço depois de todos os custos e despesas, inclusive as fixas. A margem de contribuição é calculada sobre o preço de venda, antes das despesas fixas. São três medidas diferentes, e esta simulação trabalha só com a margem de contribuição.</p>`
        + `<p><b>Por que ela é a referência.</b>""")
s=sub1(s,"""<table class="todos" id="tb-comp">""","""<table class="todos comp" id="tb-comp">""")
s=sub1(s,"""  #relatorio table.todos td:first-child{white-space:normal}""","""  #relatorio table.todos td:first-child{white-space:normal}
  #relatorio table.comp{font-size:7.5pt}
  #relatorio table.comp th{white-space:normal;text-align:center;line-height:1.25}
  #relatorio table.comp th:first-child,#relatorio table.comp td:first-child{width:21%;text-align:left}
  #relatorio table.comp th:last-child,#relatorio table.comp td:last-child{width:17%}""")
