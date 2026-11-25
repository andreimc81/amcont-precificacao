# ===== rodada 26 (versão 2026.8.13): R25-02 avisos da conferência com a base oficial da Receita Federal =====
s=sub1(s,"""    f.tipos = e.t;
    if (cod.startsWith("30")){""","""    f.tipos = e.t;
    avisosRFB(f, cod, e);
    if (cod.startsWith("30")){""")
s=sub1(s,"""function dicaIS(){""","""/* R25-02: divergências e complementos apurados na conferência com a base oficial da Receita (24/11/2026) */
function avisosRFB(f, cod, e){
  const cls = [e.ccl || ""].concat((e.o || []).map(o=>o[4])).join(" "), ax = [e.ax || ""].concat((e.o || []).map(o=>o[0])).join(" | ");
  if (/^0304[45789]/.test(cod) && /200003/.test(cls))
    f.avisos.push("Atenção: a lei exclui da cesta básica os salmonídeos, atuns, bacalhaus, hadoque e saithe das subposições 0304.4, 0304.5, 0304.7, 0304.8 e 0304.9 (Anexo I, item 20, c). Esta ferramenta lê a exclusão por espécie, e por isso mantém a alíquota zero para os demais peixes. A calculadora oficial da Receita Federal trata a subposição inteira como excluída (tributação integral). Na dúvida, adote a leitura da Receita ou confirme com a Amcont.");
  if (/Anexo IV(?![A-Z])/.test(ax) && !/200005/.test(cls))
    f.avisos.push("Venda a órgão da administração pública ou a entidade de saúde imune: alíquota zero de CBS e IBS (LC 214/2025, art. 144, II, cClassTrib 200005), em vez da redução de 60%.");
  if (/Anexo V(?![A-Z])/.test(ax) && !/200008/.test(cls))
    f.avisos.push("Venda a órgão da administração pública: alíquota zero de CBS e IBS (LC 214/2025, art. 145, II, cClassTrib 200008), em vez da redução de 60%.");
  if (/Anexo VI(?![A-Z])/.test(ax) && !/200011/.test(cls))
    f.avisos.push("Composição para nutrição enteral ou parenteral adquirida por órgão da administração pública: alíquota zero de CBS e IBS (LC 214/2025, art. 146, § 2º, cClassTrib 200011), em vez da redução de 60%.");
  if (/^(07|15|0210|0602)/.test(cod) && !/200038/.test(cls))
    f.avisos.push("A base oficial da Receita Federal também admite para este código a redução de 60% dos insumos agropecuários (Anexo IX, cClassTrib 200038), quando o produto for semente, muda ou insumo destinado à fabricação de ração ou à alimentação animal, nos termos dos itens 10, 11 e 21 do Anexo IX.");
}
function dicaIS(){""")
