# ===== rodada 20 (versão 2026.8.8): R22-01 a R22-04 =====
# R22-01: a lista de atividades acompanha o tipo (produto ou serviço)
s=sub1(s,"""function definirTipo(t, limpar){
  TIPO = t;""","""const SETORES_TIPO = {produto:["comercio","industria","combustivel"], servico:["servicos","hospitalar","carga","passageiros"]};
function preencherSetores(){
  const lista = SETORES_TIPO[TIPO] || SETORES_TIPO.produto, atual = $("#setor").value;
  $("#setor").innerHTML = P.atividades.filter(a=>lista.includes(a.id)).map(a=>`<option value="${a.id}">${a.nome}</option>`).join("");
  $("#setor").value = lista.includes(atual) ? atual : lista[0];
}
function definirTipo(t, limpar){
  TIPO = t;
  preencherSetores();""")
s=sub1(s,"""  $("#setor").innerHTML = P.atividades.map(a=>`<option value="${a.id}">${a.nome}</option>`).join("");""","""  preencherSetores();""")
s=sub1(s,"""      if (o.entradas.ano){ ANO=+o.entradas.ano;""","""      preencherSetores(); sincReaj();
      if (o.entradas.ano){ ANO=+o.entradas.ano;""")
# R22-02: PIS e COFINS de hoje em serviço não oferece monofásico nem alíquota zero
s=sub1(s,"""  const sv = TIPO === "servico";
  $("#c-is").hidden = sv; $("#c-icms-compra").hidden = sv;""","""  const sv = TIPO === "servico";
  const ph = $("#pc-hoje"), semServ = ["mono","monofab","zero"];
  [...ph.options].forEach(op=>{ const b = sv && semServ.includes(op.value); op.hidden = b; op.disabled = b;
    if (op.value === "auto") op.textContent = sv ? "Automático: tributação normal" : "Automático, pela base do NCM"; });
  if (sv && semServ.includes(ph.value)) ph.value = "auto";
  $("#c-is").hidden = sv; $("#c-icms-compra").hidden = sv;""")
s=sub1(s,"""  $("#dica-pc").textContent = (o.regime === "simples\"""","""  $("#dica-pc").textContent = o.servico
    ? (o.regime === "simples"
        ? "No Simples, o PIS e a COFINS de hoje fazem parte do DAS. Monofásico e alíquota zero não existem para serviço."
        : "Em serviço, o PIS e a COFINS de hoje incidem sobre a receita e seguem o regime da empresa (cumulativo no Presumido, não cumulativo no Real). Monofásico e alíquota zero não existem para serviço.")
    : (o.regime === "simples\"""")
# R22-03: reajuste do fornecedor em percentual no lugar do segundo preço de compra
s=sub1(s,"""        <div class="campo">
          <label for="pc-ano">Preço de compra no ano de referência</label>
          <input id="pc-ano" type="number" step="0.01" value="600">
          <p class="dica">Mantenha igual ao de hoje para ver o teto de impacto. Se o fornecedor já sinalizou reajuste, informe aqui.</p>
        </div>""","""        <div class="campo">
          <label for="reaj-forn" id="lb-reaj">Reajuste esperado do fornecedor, no ano simulado (%)</label>
          <input id="reaj-forn" type="number" step="0.01" value="0">
          <p class="dica" id="dica-reaj"></p>
          <input id="pc-ano" type="number" step="0.01" value="600" hidden>
        </div>""")
s=sub1(s,"""function calcular(){
  const o = opcoes();""","""function aplicarReaj(){ const r = parseFloat($("#reaj-forn").value); $("#pc-ano").value = (num("pc")*(1+(isNaN(r)?0:r)/100)).toFixed(2); }
function sincReaj(){ const pc = num("pc"), pa = num("pc-ano"); $("#reaj-forn").value = pc > 0 ? +((pa/pc-1)*100).toFixed(2) : 0; }
function mostrarPcAno(){
  const el = $("#dica-reaj"); if (!el) return;
  el.textContent = "0% significa que o fornecedor mantém o preço de hoje. Preço de compra no ano simulado: "+BRL.format(num("pc-ano"))
    +" (hoje "+BRL.format(num("pc"))+"). Informe só o reajuste que o fornecedor sinalizou. O regime dele muda o crédito que você toma, mesmo com preço igual.";
}
document.addEventListener("input", e=>{ const id = e.target && e.target.id; if (id === "reaj-forn" || id === "pc") aplicarReaj(); }, true);
function calcular(){
  mostrarPcAno();
  const o = opcoes();""")
s=sub1(s,"""$("#pc-ano").value = best.preco; $("#forn").value = best.reg;""","""$("#pc-ano").value = best.preco; $("#forn").value = best.reg; sincReaj();""")
s=sub1(s,"""  $("#lb-pc").textContent = sv ? "Insumos e serviços tomados por unidade vendida, valor total das notas" : "Preço de compra por unidade, valor total da nota";""","""  $("#lb-pc").textContent = sv ? "Insumos e serviços tomados por unidade vendida, valor total das notas" : "Preço de compra por unidade, valor total da nota";
  $("#lb-reaj").textContent = sv ? "Reajuste esperado nos insumos e serviços tomados, no ano simulado (%)" : "Reajuste esperado do fornecedor, no ano simulado (%)";""")
# R22-04: a opção integral do serviço só aparece quando a tabela oficial a lista ou quando não há benefício
s=sub1(s,"""  if (!tem("000001")) f.opcoes.push(INTEGRAL);
  const beneficio""","""  if (!tem("000001") && (!idx || !f.opcoes.some(o=>o.red > 0))) f.opcoes.push(INTEGRAL);
  const beneficio""")
s=sub1(s,"""  } else {
    f.cor = "amarelo"; f.selo = "Conferir";
    const iInt = f.opcoes.findIndex(o=>o.ccl==="000001" && o !== INTEGRAL);""","""  } else if (f.opcoes.length === 1 && !f.opcoes[0].semRed){
    f.cor = "verde"; f.selo = "Benefício"; f.sel = 0;
    f.msg = "Redução de "+Math.round(f.opcoes[0].red*100)+"% prevista na lei para este serviço"+(f.opcoes[0].rot ? " ("+f.opcoes[0].rot+")" : "")
      +". A tabela oficial de correlação da NFS-e não traz outra classificação para este código, por isso não há opção integral. A redução vale se o serviço prestado for o descrito no anexo.";
  } else {
    f.cor = "amarelo"; f.selo = "Conferir";
    const iInt = f.opcoes.findIndex(o=>o.ccl==="000001" && o !== INTEGRAL);""")
