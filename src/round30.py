# ===== rodada 30 (versão 2026.8.18): R27-01 relatório em PDF no padrão de documentos da Amcont =====
_logo_rel = open('fontes/logo_relatorio.svg.b64').read().strip()
_cab_rel = open('fontes/cab_relatorio.svg.b64').read().strip()
s=sub1(s,""".reg-oculto{display:none!important}""",""".reg-oculto{display:none!important}
#relatorio{display:none}
@page{size:A4;margin:34mm 20mm 26mm 30mm;
  @top-left{content:url("data:image/svg+xml;base64,"""+_logo_rel+"""");vertical-align:bottom;padding-bottom:3mm;margin-bottom:5mm;border-bottom:.6pt solid #2A5F6B}
  @top-center{content:"";margin-bottom:5mm;border-bottom:.6pt solid #2A5F6B}
  @top-right{content:url("data:image/svg+xml;base64,"""+_cab_rel+"""");text-align:right;vertical-align:bottom;padding-bottom:3mm;margin-bottom:5mm;border-bottom:.6pt solid #2A5F6B}
  @bottom-center{content:"AMCONT ASSESSORIA & CONTABILIDADE | CRC/SC 011862/O | 46.592.477/0001-04\\A (48) 3997-0969 | (48) 99826-6207 | amcont@amcontassessoria.com.br | Criciúma, Santa Catarina\\A Página " counter(page) " de " counter(pages);white-space:pre;text-align:center;font:7pt/1.5 Arial,sans-serif;color:#2A5F6B;vertical-align:top;padding-top:2.5mm;border-top:.6pt solid #2A5F6B}
  @bottom-left{content:"";border-top:.6pt solid #2A5F6B}
  @bottom-right{content:"";border-top:.6pt solid #2A5F6B}
}
@media print{
  html,body{background:#fff!important}
  body > *:not(#relatorio){display:none!important}
  body{padding:0!important;margin:0!important}
  #relatorio{display:block;font:11pt/1.4 Arial,Helvetica,sans-serif;color:#000}
  #relatorio *{font-family:Arial,Helvetica,sans-serif!important;letter-spacing:0!important;text-transform:none!important;box-shadow:none!important}
  #relatorio .r-tit{font-size:14pt;font-weight:700;color:#2A5F6B;margin:0 0 3pt}
  #relatorio .r-sub{font-size:11pt;margin:0 0 2pt}
  #relatorio .r-data{font-size:9pt;margin:0 0 12pt}
  #relatorio .r-alerta{border:.7pt solid #A63D1B;padding:5pt 7pt;font-size:10pt;margin:0 0 10pt}
  #relatorio h2{font-size:13pt;font-weight:700;color:#2A5F6B;margin:14pt 0 6pt;break-after:avoid}
  #relatorio p{margin:0 0 6pt;text-align:justify;font-size:10.5pt}
  #relatorio p.dica,#relatorio .dica{font-size:9.5pt;color:#222}
  #relatorio table{width:100%;border-collapse:collapse;table-layout:auto;font-size:10pt;margin:0 0 8pt;border:.7pt solid #2A5F6B;break-inside:auto;min-width:0}
  #relatorio th{background:#2A5F6B!important;color:#fff!important;font-weight:700;text-align:center;vertical-align:middle;padding:3.5pt 5pt;border:.4pt solid #2A5F6B;position:static!important;white-space:normal;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  #relatorio td{padding:3.5pt 5pt;border:.4pt solid #9DB2B7;vertical-align:middle;background:#fff!important;position:static!important;white-space:normal;color:#000}
  #relatorio td:first-child{text-align:left}
  #relatorio tr{break-inside:avoid}
  #relatorio table.r-prem td:first-child{width:46%;color:#2A5F6B;font-weight:700}
  #relatorio table.r-prem td:last-child{text-align:left}
  #relatorio tr.grp td{background:#D6E8EB!important;color:#2A5F6B;font-weight:700;text-align:left;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  #relatorio td.neg,#relatorio .neg{color:#A63D1B}#relatorio td.pos,#relatorio .pos{color:#1F6B4A}
  #relatorio .li{display:flex;align-items:baseline;gap:6pt;padding:2.5pt 0;border-bottom:.4pt solid #C9D6D9;font-size:10.5pt;break-inside:avoid}
  #relatorio .li .n{flex:0 1 auto}#relatorio .li .p{flex:1;border:0}#relatorio .li .v{flex:0 0 auto;font-variant-numeric:tabular-nums;text-align:right}
  #relatorio .li.trib .n,#relatorio .li.trib .v{color:#A63D1B}#relatorio .li.cr .n,#relatorio .li.cr .v{color:#1F6B4A}
  #relatorio .li.sum,#relatorio .li.tot,#relatorio .li.res{font-weight:700;border-top:.8pt solid #000;border-bottom:0;margin-top:3pt;padding-top:4pt}
  #relatorio .destaque{border:.7pt solid #2A5F6B;background:#D6E8EB!important;padding:7pt 9pt;margin:0 0 8pt;break-inside:avoid;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  #relatorio .destaque .rot{font-size:10pt;color:#2A5F6B;font-weight:700}
  #relatorio .destaque .val{font-size:17pt;font-weight:700;color:#2A5F6B;margin:2pt 0}
  #relatorio .destaque .cmp{font-size:10pt;line-height:1.45}
  #relatorio ol{margin:0 0 6pt 16pt;padding:0;font-size:9.5pt}#relatorio ol li{margin:0 0 3pt;text-align:justify}
  #relatorio svg{max-width:100%;height:auto}
  #relatorio .graf{margin:6pt 0;break-inside:avoid}#relatorio .leg{font-size:9pt;display:flex;gap:14pt;flex-wrap:wrap;margin-bottom:6pt}
  #relatorio .leg .k{display:inline-block;width:16pt;border-top:2pt solid;vertical-align:middle;margin-right:4pt}
  #relatorio .r-sec{break-inside:auto}
  #relatorio .r-kpis{display:flex;gap:6pt;margin:0 0 8pt;break-inside:avoid}
  #relatorio .r-kpis > div{flex:1;border:.7pt solid #2A5F6B;padding:6pt 7pt;background:#fff!important}
  #relatorio .r-kpis > div.pri{background:#2A5F6B!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  #relatorio .r-kpis span{display:block;font-size:8.5pt;color:#2A5F6B;font-weight:700;line-height:1.25;min-height:2.5em}
  #relatorio .r-kpis b{display:block;font-size:15pt;color:#2A5F6B;margin-top:2pt;white-space:nowrap}
  #relatorio .r-kpis small{display:block;font-size:8.5pt;color:#333;margin-top:1pt}
  #relatorio .r-kpis > div.pri span,#relatorio .r-kpis > div.pri b,#relatorio .r-kpis > div.pri small{color:#fff}
  #relatorio .rolar{overflow:visible!important}
  #relatorio table.todos{font-size:7.5pt;table-layout:fixed}
  #relatorio table.todos th,#relatorio table.todos td{padding:3pt 2pt;text-align:right;white-space:nowrap}
  #relatorio table.todos td:first-child{white-space:normal}
  #relatorio .r-sec:last-of-type p{font-size:8.5pt}
  #relatorio fieldset{border:0!important;padding:0!important}#relatorio legend{padding:0!important}
  #relatorio table.todos th:first-child,#relatorio table.todos td:first-child{width:25%;text-align:left}
  #relatorio table:not(.todos):not(.r-prem){break-inside:avoid}
  #relatorio fieldset{border:.5pt solid #9DB2B7;margin:0 0 6pt;padding:5pt 7pt;break-inside:avoid}
  #relatorio legend{font-size:9.5pt;font-weight:700;color:#2A5F6B;padding:0 4pt}
  #relatorio fieldset label{display:block;font-size:10pt;margin:2pt 0}
  #relatorio dl{margin:0 0 6pt;font-size:10pt}#relatorio dt{font-weight:700;color:#2A5F6B;float:left;margin-right:6pt}#relatorio dd{margin:0 0 2pt}
  #relatorio .f-top{font-size:11pt;font-weight:700;margin-bottom:2pt}
  #relatorio .f-top > *:first-child{display:inline-block;border:.6pt solid #2A5F6B;color:#2A5F6B;padding:0 5pt;margin-right:6pt;font-size:9pt;background:#fff!important}
  #relatorio .f-al{border-left:2pt solid #A63D1B;padding:3pt 7pt;margin:0 0 6pt;font-size:10pt;background:#fff!important;break-inside:avoid}
  #relatorio .r-det{font-size:9.5pt;margin:0 0 6pt}
  #relatorio .r-junto{break-inside:avoid}
  #relatorio h3,#relatorio h4{font-size:11pt;color:#2A5F6B;margin:8pt 0 4pt}
  #relatorio .r-ass{margin-top:16pt;font-size:11pt}
  #relatorio .r-fonte{margin-top:10pt;font-size:8pt;text-align:left}
  #relatorio a{color:inherit;text-decoration:none}
}""")
s=sub1(s,"""function ajustarAbas(){""","""/* R27-01: relatório para impressão ou PDF, no padrão de documentos da Amcont */
function montarRelatorio(){
  let r = document.getElementById("relatorio"); if (!r){ r = document.createElement("div"); r.id = "relatorio"; document.body.appendChild(r); }
  const prem = $("#prem"), fechado = prem.classList.contains("fechado"); prem.classList.remove("fechado");
  const o = opcoes(), compra = MODO === "compra", sv = TIPO === "servico";
  const txt = el => (el.querySelector(".lt") || el).textContent.replace(/\\s+/g, " ").replace(/\\?\\s*$/, "").trim();
  const P1 = [["Tipo de simulação", compra ? "Compra: custo real" : "Venda: preço necessário"], ["Objeto", sv ? "Serviço" : "Produto"], ["Ano simulado", String(ANO)]];
  document.querySelectorAll("#prem-grid label").forEach(l=>{
    if (l.offsetHeight === 0) return;
    const cx = l.querySelector("input[type=checkbox]");
    if (cx){ P1.push([l.textContent.replace(/\\s+/g, " ").replace(/\\?\\s*$/, "").trim(), cx.checked ? "Sim" : "Não"]); return; }
    const c = l.htmlFor ? document.getElementById(l.htmlFor) : null; if (!c || c.offsetHeight === 0) return;
    let v = c.tagName === "SELECT" ? (c.selectedOptions[0] ? c.selectedOptions[0].textContent.trim() : "") : String(c.value).trim();
    if (c.id === "ncm"){ const d = (typeof FICHA !== "undefined" && FICHA && FICHA.desc) ? String(FICHA.desc) : ""; v = v ? v + (d ? ", " + d : "") : "Não informado"; }
    else if (c.type === "number" && v !== ""){ const n = parseFloat(v), rot = txt(l); v = /\\(%\\)/.test(rot) ? String(n).replace(".", ",") + "%" : (/Preço|Insumos|valor/i.test(rot) ? BRL.format(n) : String(n).replace(".", ",")); }
    P1.push([txt(l).replace(/\\s*\\(%\\)/, ""), v]);
  });
  if (fechado) prem.classList.add("fechado");
  const limpo = (el, tiraDica) => { if (!el || (el.hidden) ) return ""; const c = el.cloneNode(true);
    c.querySelectorAll("h3:first-child,button,.aj,.tip,.ghit,#gcruz,script").forEach(x=>x.remove());
    if (tiraDica){ const d = c.querySelector("p.dica"); if (d) d.remove(); }
    c.querySelectorAll(".rod details, details.reg").forEach(x=>x.remove());
    if (c.matches && c.matches(".rod")) c.querySelectorAll("details").forEach(x=>x.remove());
    c.querySelectorAll("details").forEach(x=>{ const d = document.createElement("div"); d.className = "r-det"; const sm = x.querySelector("summary"); if (sm){ const b = document.createElement("b"); b.textContent = sm.textContent.trim() + ": "; sm.replaceWith(b); } while (x.firstChild) d.appendChild(x.firstChild); x.replaceWith(d); });
    c.querySelectorAll("fieldset").forEach(fs=>{ const ins = [...fs.querySelectorAll("input[type=radio],input[type=checkbox]")];
      if (!ins.length) return; ins.forEach(i=>{ if (!i.checked){ const l = i.closest("label"); if (l) l.remove(); } });
      if (!fs.querySelector("label")) fs.remove(); else fs.querySelectorAll("input").forEach(i=>i.remove()); });
    c.querySelectorAll(".f-al").forEach(x=>{ if (/^Responda/.test(x.textContent.trim())) x.remove(); });
    c.querySelectorAll("input,select").forEach(x=>{ const sp = document.createElement("span"); sp.textContent = x.tagName === "SELECT" ? (x.selectedOptions[0] ? x.selectedOptions[0].textContent : "") : (x.type === "checkbox" ? (x.checked ? "Sim" : "Não") : x.value); x.replaceWith(sp); });
    c.querySelectorAll("[id]").forEach(x=>x.removeAttribute("id")); c.querySelectorAll("[style]").forEach(x=>{ if (!x.closest("svg") && !x.classList.contains("k")) x.removeAttribute("style"); });
    return c.innerHTML.trim(); };
  const aliq = `<table><thead><tr><th>Ano</th><th>CBS</th><th>IBS</th><th>ICMS e ISS que permanecem</th></tr></thead><tbody>`
    + P.transicao.map(t=>`<tr><td>${t.ano}</td><td>${t.ano === 2026 ? "teste" : PCT(t.cbs)}</td><td>${t.ano === 2026 ? "teste" : PCT(t.ibs)}</td><td>${PCT(t.fatorIcmsIss)}</td></tr>`).join("") + `</tbody></table>`
    + `<p class="dica">${aliqAlterada() ? "Alíquotas alteradas nesta simulação: o resultado não é o cenário previsto." : "Alíquotas previstas na data desta simulação. As de 2027 em diante são estimativas e dependem de ato do Senado e do Comitê Gestor do IBS."} ${baseSem() ? "ICMS e ISS calculados sobre o valor sem CBS e IBS (opção da simulação)." : "ICMS e ISS calculados sobre o total da nota, com CBS e IBS na base."}</p>`;
  const H = hoje(o), LA = compra ? null : linhaAno(o, H, ANO), un = sv ? "serviço" : "produto";
  const kpi = (rot, val, obs, pri) => `<div${pri ? ' class="pri"' : ""}><span>${rot}</span><b>${val}</b>${obs ? `<small>${obs}</small>` : ""}</div>`;
  const sgn = x => (x >= 0 ? "+" : "") + PCT(x), semDest = h => { const d = document.createElement("div"); d.innerHTML = h; const x = d.querySelector(".destaque"); if (x) x.remove(); return d.innerHTML; };
  let kAno = "", kMd = "";
  if (LA){
    const rr = LA.g ? "" : ", no regime regular";
    kAno = `<div class="r-kpis">` + kpi("Valor do " + un + " a cadastrar" + rr, BRL.format(LA.cad), "preserva a margem de hoje", true)
      + kpi("CBS e IBS, somados por fora", BRL.format(LA.nf - LA.cad), "")
      + kpi("Total da nota: o que o cliente paga", BRL.format(LA.nf), sgn(LA.var) + " contra " + BRL.format(o.pv) + " hoje", true)
      + kpi("Margem de contribuição preservada", BRL.format(H.mc), "por unidade") + `</div>`
      + (LA.g ? "" : `<div class="r-kpis">` + kpi("Total da nota no Simples tradicional", BRL.format(LA.nfT), "CBS e IBS dentro do DAS") + `</div>`);
    if (LA.M) kMd = `<div class="r-kpis">` + kpi("Valor do " + un + " a cadastrar" + rr, BRL.format(LA.cad2), "para o cliente pagar o mesmo de hoje", true)
      + kpi("Total da nota: o que o cliente paga", BRL.format(o.pv), "igual ao de hoje", true)
      + kpi("Margem de contribuição neste cenário", BRL.format(LA.mc2), "hoje: " + BRL.format(H.mc))
      + kpi("Redução da margem por unidade", BRL.format(LA.perda), PCT(LA.pperda) + " da margem") + `</div>`;
  }
  const S = [];
  S.push(["Premissas", `<table class="r-prem"><tbody>` + P1.map(x=>`<tr><td>${esc(x[0])}</td><td>${esc(x[1])}</td></tr>`).join("") + `</tbody></table>`]);
  const fi = limpo($("#ficha")); if (fi && $("#ficha").offsetHeight > 0) S.push(["Classificação do código", fi]);
  if (compra){
    S.push(["Cotações informadas", limpo($("#p-cot"))]); S.push(["Custo real da compra em " + ANO, limpo($("#p-compra"))]); S.push(["Nota fiscal da compra", limpo($("#p-nota-compra"))]);
  } else {
    S.push(["Como é hoje", limpo($("#p-hoje"))]);
    S.push(["Preço necessário em " + ANO, kAno + (kAno ? semDest(limpo($("#p-ano"))) : limpo($("#p-ano"))) + ($("#p-simples") && $("#p-simples").innerHTML.trim() && !$("#p-simples").hidden ? limpo($("#p-simples")) : "")]);
    S.push(["Mantendo o mesmo desembolso do cliente em " + ANO, kMd ? kMd + semDest(limpo($("#p-md"))) : limpo($("#p-md"))]);
    S.push(["Nota fiscal da venda em " + ANO, limpo($("#p-nota"))]);
    S.push(["Todos os anos, de 2026 a 2033", `<p class="dica">Valores em reais, por unidade.</p>` + limpo($("#p-todos"), true).replace(/(<td[^>]*>)R[$](?:\s|&nbsp;|\u00a0)?/g, "$1").replace(/(<td[^>]*>)-R[$](?:\s|&nbsp;|\u00a0)?/g, "$1-")]);
    S.push(["Compra e fornecedores em " + ANO, limpo($("#p-forn"))]);
  }
  S.push(["Alíquotas usadas", aliq]);
  S.push(["Antes de usar estes números", limpo(document.querySelector(".rod"))]);
  const cod = $("#ncm").value.trim(), reg = $("#regime").selectedOptions[0].textContent.trim();
  const dataHoje = new Date().toLocaleDateString("pt-BR", {day:"numeric", month:"long", year:"numeric"});
  let h = `<p class="r-tit">Simulação de ${compra ? "custo de compra" : "preço de venda"} na Reforma Tributária</p>`
    + `<p class="r-sub">${sv ? "Serviço" : "Produto"}${cod ? " " + esc(cod) : ""}, ${esc(reg)}, ano simulado ${ANO}</p>`
    + `<p class="r-data">${dataHoje}</p>`
    + (aliqAlterada() ? `<div class="r-alerta"><b>Simulação com alíquotas alteradas.</b> Este resultado não é o cenário previsto.</div>` : "");
  let n = 0;
  S.forEach(x=>{ if (!x[1]) return; n++; h += `<div class="r-sec"><h2>${n}. ${x[0]}</h2>${x[1]}</div>`; });
  h += `<p class="r-ass">Amcont Assessoria Contábil</p>`
    + `<p class="r-fonte">Simulação com base na Lei Complementar 214/2025 e na legislação conferida pela Amcont. Não é apuração de imposto devido. Ferramenta de precificação, versão ${window.AMCONT_VERSAO || ""}.</p>`;
  r.innerHTML = h;
}
window.addEventListener("beforeprint", montarRelatorio);
function ajustarAbas(){""")
