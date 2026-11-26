# R27-04: barra de abas sem rolagem; alíquotas simuladas vira botão da barra de ações; visão do comprador por último
s=sub1(s,"""const ABAS = [["hoje","Como é hoje"],["ano","Preço necessário"],["comp","Visão do comprador"],["md","Mesmo desembolso"],["nota","Nota fiscal"],["todos","Todos os anos"],["forn","Compra e fornecedores"],["aliq","Alíquotas simuladas"]];""","""const ABAS = [["hoje","Como é hoje"],["ano","Preço necessário"],["md","Mesmo desembolso"],["nota","Nota fiscal"],["todos","Todos os anos"],["forn","Compra e fornecedores"],["comp","Visão do comprador"]];
let ABA_ANT = "hoje";""")
s=sub1(s,"""  ABA = a;
""","""  if (a === "aliq"){ if (ABA !== "aliq") ABA_ANT = ABA; } 
  ABA = a;
  { const ba = $("#b-aliq"); if (ba) ba.classList.toggle("forte", a === "aliq"); }
""")
s=sub1(s,"""  const i = ABAS.findIndex(x=>x[0] === a), nav = $("#aba-nav"); if (!nav) return;
""","""  const i = ABAS.findIndex(x=>x[0] === a), nav = $("#aba-nav"); if (!nav) return;
  if (i < 0){ const v = ABAS.find(x=>x[0] === ABA_ANT) || ABAS[0]; nav.innerHTML = `<button type="button" class="btn forte" data-aba="${v[0]}">Voltar: ${v[1]}</button>`; return; }
""")
s=sub1(s,"""  const nav = document.createElement("div"); nav.id = "aba-nav"; main.insertBefore(nav, ref.nextSibling);""","""  { const c = document.createElement("div"); c.className = "aba-c"; c.id = "aba-aliq"; main.insertBefore(c, ref.nextSibling); ref = c; cont.aliq = c; }
  const nav = document.createElement("div"); nav.id = "aba-nav"; main.insertBefore(nav, ref.nextSibling);
  { const bc = $("#b-consulta"); if (bc){ const ba = document.createElement("button"); ba.type = "button"; ba.className = "btn"; ba.id = "b-aliq"; ba.dataset.aba = "aliq"; ba.textContent = "Alíquotas simuladas"; const bp = [...bc.parentNode.querySelectorAll("button")].find(x=>/Imprimir/.test(x.textContent)); bc.parentNode.insertBefore(ba, bp ? bp.nextSibling : null); } }""")
s=sub1(s,"""if (y < 0 || b.closest("#aba-nav")) $("#prem").scrollIntoView(); return; }""","""if (b.id === "b-aliq") $("#abas").scrollIntoView(); else if (y < 0 || b.closest("#aba-nav")) $("#prem").scrollIntoView(); return; }""")
s=sub1(s,"""#abas{display:flex;gap:2px;border-bottom:2px solid var(--petroleo);margin-bottom:14px;position:sticky;top:var(--hh,120px);background:var(--via);z-index:30;padding-top:6px;overflow-x:auto}
#abas button{border:0;background:transparent;padding:10px 15px;font:500 13.5px "IBM Plex Sans";color:var(--petroleo-2);cursor:pointer;border-radius:4px 4px 0 0;white-space:nowrap}""","""#abas{display:flex;gap:2px;border-bottom:2px solid var(--petroleo);margin-bottom:14px;position:sticky;top:var(--hh,120px);background:var(--via);z-index:30;padding-top:6px;overflow:hidden}
#abas button{flex:1 1 auto;min-width:0;border:0;background:transparent;padding:10px 6px;font:500 13.5px "IBM Plex Sans";color:var(--petroleo-2);cursor:pointer;border-radius:4px 4px 0 0;white-space:nowrap;text-align:center}
body.modo-compra #b-aliq,body.em-consulta #b-aliq{display:none}
@media(max-width:1180px){#abas button{white-space:normal;line-height:1.2;font-size:12.5px}#abas button .n{display:none}}""")
# R27-05: no quadro Todos os anos, a perda de margem aparece com sinal negativo
s=sub1(s,"""    + lin("Redução da margem, R$ por unidade", l=>l.M ? BRL.format(l.perda) : sem, l=>cls(l.perda))
    + lin("Redução da margem, % da margem preservada", l=>l.M ? sg(l.pperda) : sem, l=>cls(l.pperda))
    + (simp ? lin("Redução da margem, Simples tradicional, R$", l=>l.perdaT == null ? sem : BRL.format(l.perdaT), l=>cls(l.perdaT||0)) : "")""","""    + lin("Variação da margem, R$ por unidade", l=>l.M ? sgR(-l.perda) : sem, l=>cls(l.perda))
    + lin("Variação da margem, % da margem preservada", l=>l.M ? sg0(-l.pperda) : sem, l=>cls(l.pperda))
    + (simp ? lin("Variação da margem, Simples tradicional, R$", l=>l.perdaT == null ? sem : sgR(-l.perdaT), l=>cls(l.perdaT||0)) : "")""")
s=sub1(s,"""  const c = (l, f, extra) => `<td class="${l.ano===ANO?"sel ":""}${extra||""}">${f}</td>`;""","""  const sgR = x => Math.abs(x) < 0.005 ? BRL.format(0) : (x > 0 ? "+" : "-") + BRL.format(Math.abs(x));
  const sg0 = x => Math.abs(x) < 0.00005 ? PCT(0) : (x > 0 ? "+" : "-") + PCT(Math.abs(x));
  const c = (l, f, extra) => `<td class="${l.ano===ANO?"sel ":""}${extra||""}">${f}</td>`;""")
# R27-06: vendedor do Simples Nacional não vê campos nem consultas de ICMS, ISS, DIFAL e base, que só valem para Lucro Presumido e Lucro Real
s=sub1(s,"""    oc($("#c-snop"), reg !== "simples");""","""    oc($("#c-snop"), reg !== "simples");
    { const snv = reg === "simples" && !compra;
      oc($("#icms-venda").closest(".campo"), snv); oc($("#c-dest"), snv); oc($("#c-dupla"), snv); }""")
s=sub1(s,"""    document.querySelectorAll("#prem-grid .bloco").forEach(bl=>{ bl.classList.remove("reg-oculto"); oc(bl,""","""    document.querySelectorAll("#prem-grid .bloco").forEach(bl=>{ bl.classList.remove("reg-oculto"); oc(bl,""")
s=sub1(s,"""  if (f.pc){
    const q = f.pc;""","""  const snVenda = $("#regime").value === "simples" && MODO !== "compra";
  if (f.pc && !(snVenda && !f.pc.st && f.pc.reg === "normal")){
    const q = f.pc;""")
s=sub1(s,"""  if (f.sc && f.scQ && MODO !== "compra"){""","""  if (snVenda){
    if (f.sc) h += `<p class="dica" style="margin-top:10px">Simples Nacional: o ICMS${TIPO === "servico" ? " e o ISS" : ""} desta venda ${TIPO === "servico" ? "estão" : "está"} dentro do DAS. A consulta de alíquota de ICMS de Santa Catarina não se aplica a esta simulação. Substituição tributária e sublimite não são simulados.</p>`;
  } else if (f.sc && f.scQ && MODO !== "compra"){""")
s=sub1(s,"""             (o.servico ? "ISS " : "ICMS ") + PCT(o.icmsVenda),""","""             ...(o.regime === "simples" && MODO !== "compra" ? ["DAS " + PCT(o.aliqSN)] : [(o.servico ? "ISS " : "ICMS ") + PCT(o.icmsVenda)]),""")
s=sub1(s,"""  $("#regime").addEventListener("change", sincronizar);""","""  $("#regime").addEventListener("change", sincronizar);
  $("#regime").addEventListener("change", ()=>{ try{ if (FICHA) desenharFicha(); }catch(e){} });""")
s=sub1(s,"""      oc($("#icms-venda").closest(".campo"), snv);""","""      { const lb = document.querySelector('label[for="base-sem"]'); if (lb) (lb.querySelector(".lt") || lb).textContent = snv ? "CBS e IBS na base do ICMS da compra?" : "CBS e IBS na base do ICMS e do ISS?"; }
      oc($("#icms-venda").closest(".campo"), snv);""")
