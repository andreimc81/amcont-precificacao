# ===== rodada 12: integracao da auditoria independente (10/11/2026) =====
# F02: cClassTrib composto vira codigo principal + alternativas a confirmar
s=sub1(s,"""/* ---------- simulacao de compra: custo real por fornecedor ---------- */""",r"""/* ---------- cClassTrib composto: codigo principal e alternativas (auditoria F02) ---------- */
function normCcl(f){
  if (!f || !f.opcoes) return f;
  let alt = null;
  for (const o of f.opcoes){
    if (o.ccl && !/^\d{6}$/.test(o.ccl)){
      const m = String(o.ccl).match(/\d{6}/g);
      o.cclTexto = o.ccl; o.ccl = m ? m[0] : o.ccl; o.cclConfirmar = true;
      o.cond = (o.cond ? o.cond + " " : "") + "cClassTrib a confirmar: " + o.cclTexto + ".";
      if (!alt) alt = o;
    }
  }
  if (alt) f.avisos.push("Há mais de um cClassTrib possível para esta classificação (" + alt.cclTexto + "). A ferramenta usa o principal, " + alt.ccl + ", só para simular. Confirme o código com a Amcont antes de emitir a nota.");
  return f;
}
/* ---------- simulacao de compra: custo real por fornecedor ---------- */""")
s=sub1(s,"""function classifTexto(o){
  const x = FICHA && FICHA.opcoes[FICHA.sel];
  if (x && Math.abs(x.red - o.trat) < 1e-9) return "CST "+x.cst+" · cClassTrib "+x.ccl;""","""function classifTexto(o){
  const x = FICHA && FICHA.opcoes[FICHA.sel];
  if (x && Math.abs(x.red - o.trat) < 1e-9) return "CST "+x.cst+" · cClassTrib "+x.ccl+(x.cclConfirmar ? " (confirmar)" : "");""")
s=sub1(s,"""function iniciar(){""","""{ const _cN = classificarNcm, _cB = classificarNbs;
  classificarNcm = function(c){ return normCcl(_cN(c)); };
  classificarNbs = function(c, it){ return normCcl(_cB(c, it)); }; }
function iniciar(){""")

# F01 e C5: credito estimado x prudencial; PIS/COFINS sem ICMS na base quando o ICMS e destacado (regular e sublimite)
s=sub1(s,"""    ? pc * (1 - (forn === "regular" ? o.icmsCompra : 0)) * (o.pis + o.cofins) : 0;""","""    ? pc * (1 - ((forn === "regular" || forn === "sn_sublimite") ? o.icmsCompra : 0)) * (o.pis + o.cofins) : 0;""")
s=sub1(s,"""<button type="button" class="btn" id="b-cot-5">Comparar todos os regimes pelo preço da 1ª linha</button>
        </div>""","""<button type="button" class="btn" id="b-cot-5">Comparar todos os regimes pelo preço da 1ª linha</button>
        </div>
        <label style="margin-top:10px"><input type="checkbox" id="cred-prud" style="width:auto;margin-right:7px">
          Cenário prudencial: comparar sem crédito (nota sem destaque válido ou débito do fornecedor não pago)</label>""")
s=sub1(s,"""  const L = lerCot().map((c,i)=>Object.assign({i}, c, creditoComprador(c, o))).filter(x=>x.preco > 0);
  if (!L.length){""","""  const prud = $("#cred-prud").checked;
  const L = lerCot().map((c,i)=>{ const k = creditoComprador(c, o), semCred = c.preco + k.difal;
      return Object.assign({i}, c, k, {semCred}, prud ? {custo:semCred, taxa:c.preco > 0 ? -k.difal/c.preco : 0} : {}); })
    .filter(x=>x.preco > 0);
  if (!L.length){""")
s=sub1(s,"""    + `<th>Custo real</th><th>Preço máximo para empatar</th><th>A mais</th></tr></thead><tbody>`""","""    + `<th>${prud ? "Custo sem crédito" : "Custo real"}</th>${prud ? "" : "<th>Sem crédito</th>"}<th>Preço máximo para empatar</th><th>A mais</th></tr></thead><tbody>`""")
s=sub1(s,"""          + `<td><b>${BRL.format(x.custo)}</b></td><td>${m ? "" : BRL.format(eq)}</td>`""","""          + `<td><b>${BRL.format(x.custo)}</b></td>${prud ? "" : `<td>${BRL.format(x.semCred)}</td>`}<td>${m ? "" : BRL.format(eq)}</td>`""")
s=sub1(s,"""  notas.push("Preço máximo para empatar: o valor de nota""","""  notas.push(prud ? "Cenário prudencial: os créditos não são considerados, e a comparação usa o valor da nota mais o DIFAL."
    : "Os créditos são estimativas: só podem ser apropriados com documento fiscal idôneo e depois que o débito do fornecedor for extinto (LC 214/2025, art. 47, caput, § 1º, II, e § 2º, I). A coluna Sem crédito mostra o custo se o crédito não vier.");
  notas.push("Preço máximo para empatar: o valor de nota""")
s=sub1(s,"""  ["#uf-dest","#dest-tipo","#importado","#difal-dupla"].forEach(""","""  $("#cred-prud").addEventListener("change", calcular);
  ["#uf-dest","#dest-tipo","#importado","#difal-dupla"].forEach(""")
s=sub1(s,"""         ["Crédito de CBS e IBS do comprador do regime regular", A.cbs + A.ibs, "cr"],""","""         ["Crédito estimado de CBS e IBS do comprador do regime regular", A.cbs + A.ibs, "cr"],""")

# F04 e F10 e F01 na venda: projecao, sensibilidade, cenario sem credito e alcance da margem
s=sub1(s,"""  desenharNotaVenda(o, A);
  /* --- comparador de fornecedores --- */""","""  if (A.tipo === "geral" && ANO >= 2027){
    const T = P.transicao, ex = [];
    P.transicao = T.map(x=>x.ano === ANO ? Object.assign({}, x, {cbs:x.cbs + 0.005, ibs:x.ibs + 0.005}) : x);
    let S1; try { S1 = noAno(o, H.mc, o.pcAno, o.forn, o.aliqForn, o.anexoForn); } finally { P.transicao = T; }
    const S2 = noAno(o, H.mc, o.pcAno, "pf", o.aliqForn, o.anexoForn);
    const tA = tAno(ANO);
    ex.push(`<b>Projeção.</b> ${ANO} usa CBS de ${PCT(tA.cbs)} e IBS de ${PCT(tA.ibs)}, alíquotas de referência ainda provisórias: o resultado é simulação, não o imposto devido.`);
    ex.push(`Se a alíquota de referência (CBS mais IBS) for 1 ponto maior, o preço necessário passa a <b>${BRL.format(S1.nf)}</b> (${BRL.format(S1.nf - A.nf)} a mais).`);
    if (A.cred.total > 0.005) ex.push(`Se o crédito da compra não for aproveitado, o preço necessário passa a <b>${BRL.format(S2.nf)}</b>.`);
    ex.push("O preço mantém a margem de contribuição por unidade de hoje. Despesas fixas, volume, comissões e frete não entram: para o resultado da empresa, use a calculadora de empresa.");
    $("#p-ano").insertAdjacentHTML("beforeend", `<p class="dica" style="margin-top:9px">${ex.join(" ")}</p>`);
  }
  /* F06: beneficio de ICMS de SC com fim em 31/12/2026 aplicado em ano posterior */
  if (FICHA && FICHA.sc && TIPO === "produto" && vendaICMS().fora === false){
    const cur = num("icms-venda")/100, sel = FICHA.sc.ops.find(x=>Math.abs(x.aliq - cur) < 1e-9);
    if (sel && sel.fim && ANO > sel.fim && !FICHA.sc.ops.some(x=>!x.fim && Math.abs(x.aliq - cur) < 1e-9)){
      const alt = FICHA.sc.ops.find(x=>!x.fim);
      $("#p-ano").insertAdjacentHTML("beforeend", `<p class="dica" style="margin-top:9px;color:var(--carimbo)"><b>Benefício vencido.</b> A alíquota de ICMS de ${PCT(cur)} vem de benefício que vale até 31/12/${sel.fim}. Sem prorrogação, em ${ANO} a alíquota é ${alt ? PCT(alt.aliq) : "a geral"}.`
        + (alt ? ` <button type="button" class="btn" data-icms-alt="${alt.aliq*100}">Usar ${PCT(alt.aliq)}</button>` : "") + `</p>`);
    }
  }
  desenharNotaVenda(o, A);
  /* --- comparador de fornecedores --- */""")
s=sub1(s,"""  $("#cred-prud").addEventListener("change", calcular);""","""  $("#cred-prud").addEventListener("change", calcular);
  $("#p-ano").addEventListener("click", e=>{ const b = e.target.closest("[data-icms-alt]"); if (b){ $("#icms-venda").value = b.dataset.icmsAlt; calcular(); } });""")
# F09: Imposto Seletivo
s=sub1(s,"""    f.isNota = is ? is[2] : "Bem do Anexo XVII, sujeito ao Imposto Seletivo. Informe a alíquota.";""","""    f.isNota = (is ? is[2] : "Bem do Anexo XVII, sujeito ao Imposto Seletivo. Informe a alíquota.")
      + " Referência de fonte secundária: a MP 1.399/2026 (art. 3º) apura a alíquota de 2027 multiplicando a alíquota da TIPI do produto pelo fator de conversão dos seus Anexos IV e V, com efeitos a partir de 02/02/2027. Confira a alíquota do produto antes de precificar.";""")
# F03: Anexo VIII
s=sub1(s,"""O Anexo VIII da NFS-e Nacional admite ${it.n.length} códigos NBS para este item.""","""O Anexo VIII da NFS-e Nacional (versão 1.01.00, correlação preliminar; a 1.02.00 de 26/10/2026 ainda não foi incorporada) admite ${it.n.length} códigos NBS para este item.""")
