# ===== rodada 28 (versão 2026.8.14): R26-02 navegação: premissas no topo e resultados em abas =====
s=sub1(s,""".rolar{overflow-x:auto}""",""".rolar{overflow-x:auto}
/* R26-02: premissas em faixa e resultados em abas */
.grade{display:block}
#prem{background:var(--nota);border:1px solid var(--linha);padding:14px 18px 4px;margin-bottom:14px}
#prem-cab{display:flex;align-items:center;gap:14px;margin-bottom:10px}
#prem-cab h3{font:500 11px "IBM Plex Mono";letter-spacing:.16em;text-transform:uppercase;color:var(--petroleo);margin:0;flex:1}
#prem-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px;align-items:start}
#prem-grid .bloco{margin:0 0 12px}
#prem #modo{max-width:520px;margin-bottom:14px}
#prem-res{display:none;flex:1;font-size:14px;line-height:1.45}
#prem.fechado #prem-grid{display:none}
#prem.fechado #prem-res{display:block}
#prem.fechado #prem-cab h3{flex:0 0 auto}
#prem.fechado #prem-cab{margin-bottom:8px}
#abas{display:flex;gap:2px;border-bottom:2px solid var(--petroleo);margin-bottom:14px;position:sticky;top:var(--hh,120px);background:var(--via);z-index:30;padding-top:6px;overflow-x:auto}
#abas button{border:0;background:transparent;padding:10px 15px;font:500 13.5px "IBM Plex Sans";color:var(--petroleo-2);cursor:pointer;border-radius:4px 4px 0 0;white-space:nowrap}
#abas button:hover{color:var(--petroleo)}
#abas button.on{background:var(--petroleo);color:#fff}
#abas button .n{font:500 11px "IBM Plex Mono";opacity:.7;margin-right:6px}
.aba-c{display:none}.aba-c.on{display:block}
#aba-nav{display:flex;justify-content:space-between;gap:10px;margin:0 0 26px}
#aba-nav .btn.forte{padding:9px 16px}
body.modo-compra #abas,body.modo-compra #aba-nav,body.modo-compra #aba-hoje,body.modo-compra #aba-ano,body.modo-compra #aba-md,body.modo-compra #aba-nota,body.modo-compra #aba-forn{display:none}
body.modo-compra #aba-todos,body.modo-compra #aba-aliq{display:block}
body:not(.modo-compra) .grade{display:none}
body.em-consulta #prem,body.em-consulta #abas,body.em-consulta .aba-c,body.em-consulta #aba-nav{display:none!important}
body.em-consulta .grade{display:none!important}
@media(max-width:1000px){#prem-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:640px){#prem-grid{grid-template-columns:1fr}#prem-cab{flex-wrap:wrap}}
@media print{#abas,#aba-nav,#prem-tg{display:none!important}.aba-c{display:block!important}#prem.fechado #prem-grid{display:grid}#prem.fechado #prem-res{display:none}}""")
x="""      + blocoMesmoDesembolso(o, A, H)"""
assert s.count(x)==2, s.count(x)
s=s.replace(x,"""      + (MD_HTML = blocoMesmoDesembolso(o, A, H), "")""")
s=sub1(s,"""function calcular(){""","""let MD_HTML = "", ABA = "hoje";
const ABAS = [["hoje","Como é hoje"],["ano","Preço necessário"],["md","Mesmo desembolso"],["nota","Nota fiscal"],["todos","Todos os anos"],["forn","Compra e fornecedores"],["aliq","Alíquotas simuladas"]];
function irAba(a){
  ABA = a;
  document.querySelectorAll("#abas button").forEach(b=>b.classList.toggle("on", b.dataset.aba === a));
  document.querySelectorAll(".aba-c").forEach(c=>c.classList.toggle("on", c.id === "aba-"+a));
  const i = ABAS.findIndex(x=>x[0] === a), nav = $("#aba-nav"); if (!nav) return;
  nav.innerHTML = (i > 0 ? `<button type="button" class="btn" data-aba="${ABAS[i-1][0]}">Voltar: ${ABAS[i-1][1]}</button>` : "<span></span>")
    + (i < ABAS.length-1 ? `<button type="button" class="btn forte" data-aba="${ABAS[i+1][0]}">Avançar: ${ABAS[i+1][1]}</button>` : "");
}
function montarNav(){
  const g = document.querySelector(".grade"), L = g.children[0], main = g.parentNode;
  const prem = document.createElement("div"); prem.id = "prem";
  prem.innerHTML = `<div id="prem-cab"><h3>Premissas</h3><div id="prem-res"></div><button type="button" class="btn" id="prem-tg">Recolher premissas</button></div>`;
  prem.appendChild($("#modo"));
  const grid = document.createElement("div"); grid.id = "prem-grid";
  const blocos = [...L.querySelectorAll(":scope > .bloco")];
  // quatro colunas: produto ou serviço | sua empresa e base | compra | venda
  const col = [document.createElement("div"), document.createElement("div"), document.createElement("div"), document.createElement("div")];
  blocos.forEach(bl=>{
    const venda = !!bl.querySelector("#tit-venda"), compra = !!bl.querySelector("#tit-compra"), base = bl.id === "b-base", prod = !!bl.querySelector("#ncm");
    (prod ? col[0] : venda ? col[3] : compra ? col[2] : col[1]).appendChild(bl);
    if (base) col[1].appendChild(bl);
  });
  col.forEach(c=>grid.appendChild(c)); prem.appendChild(grid);
  main.insertBefore(prem, g);
  const abas = document.createElement("div"); abas.id = "abas"; abas.setAttribute("role", "tablist");
  abas.innerHTML = ABAS.map((d,i)=>`<button type="button" role="tab" data-aba="${d[0]}"><span class="n">${i+1}</span><span class="t">${d[1]}</span></button>`).join("");
  main.insertBefore(abas, g.nextSibling);
  let ref = abas; const cont = {};
  ABAS.forEach(d=>{ const c = document.createElement("div"); c.className = "aba-c"; c.id = "aba-"+d[0]; main.insertBefore(c, ref.nextSibling); ref = c; cont[d[0]] = c; });
  const nav = document.createElement("div"); nav.id = "aba-nav"; main.insertBefore(nav, ref.nextSibling);
  const pmd = document.createElement("div"); pmd.className = "painel so-venda"; pmd.id = "p-md";
  cont.hoje.appendChild($("#p-hoje")); cont.ano.appendChild($("#p-ano")); cont.ano.appendChild($("#p-simples")); cont.md.appendChild(pmd);
  cont.nota.appendChild($("#p-nota")); cont.todos.appendChild($("#p-todos")); cont.forn.appendChild($("#p-forn")); cont.aliq.appendChild($("#p-aliq"));
  $("#p-aliq").open = true;
  document.addEventListener("click", e=>{
    const b = e.target.closest("[data-aba]");
    if (b){ irAba(b.dataset.aba); const y = $("#abas").getBoundingClientRect().top; if (y < 0 || b.closest("#aba-nav")) $("#prem").scrollIntoView(); return; }
    if (e.target.id === "prem-tg"){ const f = $("#prem").classList.toggle("fechado"); e.target.textContent = f ? "Editar premissas" : "Recolher premissas"; ajustarAbas(); }
  });
  window.addEventListener("resize", ajustarAbas); ajustarAbas(); irAba("hoje");
}
function ajustarAbas(){ const h = document.querySelector("header"); if (h) document.documentElement.style.setProperty("--hh", h.offsetHeight + "px"); }
function navPos(o){
  const pmd = $("#p-md"); if (!pmd) return;
  pmd.innerHTML = MD_HTML ? `<h3>Mesmo desembolso <em>${ANO}</em></h3>` + MD_HTML.replace('style="margin-top:20px;padding-top:16px;border-top:1px dashed var(--linha)"', "")
    : `<h3>Mesmo desembolso <em>${ANO}</em></h3><p class="dica">Em 2026 a CBS e o IBS não alteram o preço: o cliente paga o mesmo e a margem não muda. Escolha um ano de 2027 em diante na barra do topo.</p>`;
  const t = document.querySelector('#abas button[data-aba="ano"] .t'); if (t) t.textContent = "Preço necessário em " + ANO;
  const sel = id => { const e = $(id); return e && e.selectedOptions && e.selectedOptions[0] ? e.selectedOptions[0].textContent.trim() : ""; };
  const cod = $("#ncm").value.trim(), desc = (typeof FICHA !== "undefined" && FICHA && FICHA.desc) ? String(FICHA.desc) : "";
  const p = [`<b>${o.servico ? "Serviço" : "Produto"}</b>` + (cod ? " · " + esc(cod) + (desc ? ", " + esc(desc.slice(0, 48)) : "") : " · código não informado"),
             `<b>${esc(sel("#regime"))}</b>` + (sel("#setor") ? ", " + esc(sel("#setor").toLowerCase()) : ""),
             (o.servico ? "ISS " : "ICMS ") + PCT(o.icmsVenda),
             (o.servico ? "insumos " : "compra ") + BRL.format(o.pc), `<b>venda ${BRL.format(o.pv)}</b>`];
  if (baseSem()) p.push("ICMS e ISS sem CBS e IBS na base");
  $("#prem-res").innerHTML = p.join(" · ");
}
function calcular(){
  MD_HTML = "";""")
s=sub1(s,"""  atualizarTodos(o, H); sinalAliq(); dicaIS();""","""  atualizarTodos(o, H); sinalAliq(); dicaIS(); navPos(o);""")
s=sub1(s,"""  montarAliq(); lerAliq();
  $("#base-sem").addEventListener("change", calcular);""","""  montarAliq(); lerAliq(); montarNav();
  $("#base-sem").addEventListener("change", calcular);""")
s=sub1(s,"""  $("#tela-consulta").hidden = !abrir; document.querySelector(".grade").hidden = abrir;""","""  $("#tela-consulta").hidden = !abrir; document.querySelector(".grade").hidden = abrir; document.body.classList.toggle("em-consulta", !!abrir);""")
