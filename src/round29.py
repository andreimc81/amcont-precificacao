# ===== rodada 29 (versão 2026.8.15): R26-03 premissas alinhadas, com as explicações em balões de ajuda =====
s=sub1(s,"""body:not(.modo-compra) .grade{display:none}""","""body:not(.modo-compra) .grade{display:none}
#prem-grid .campo{position:relative;margin-bottom:12px}
#prem-grid .campo > label:not(.chk){display:flex;align-items:flex-end;gap:6px;line-height:1.3;min-height:2.6em;margin-bottom:5px}
#prem-grid #ncm-desc:empty{display:none}
#b-base .bloco-tit{display:none}
#prem-topo{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px;margin-bottom:16px}
#prem-topo .seg{grid-column:span 2;display:grid;grid-template-columns:1fr 1fr;gap:22px;margin:0;max-width:none!important}
#prem-topo .seg button{box-sizing:border-box;height:48px;min-height:0;padding:0 10px;margin:0;font-size:14px;line-height:1.2;display:flex;align-items:center;justify-content:center;text-align:center}
#prem.fechado #prem-topo{display:none}
@media(max-width:1000px){#prem-topo{grid-template-columns:repeat(2,minmax(0,1fr))}#prem-topo .seg{gap:10px}}
@media(max-width:640px){#prem-topo{grid-template-columns:1fr}#prem-topo .seg{grid-column:auto}}
header{padding:12px 0 0}
.hd{align-items:center;gap:18px;flex-wrap:nowrap}
.hd .sub{display:flex;flex-direction:column;gap:2px;min-width:0}
.hd .sub .hd-t{font:600 15.5px/1.25 "IBM Plex Sans",Arial,sans-serif;color:#fff}
.hd .sub .hd-s{font:400 12px/1.3 "IBM Plex Sans",Arial,sans-serif;color:var(--petroleo-3)}
.hd .lei{white-space:nowrap}
.faixa-ano{border-top:0;padding:12px 0 13px}
@media(max-width:700px){.hd .sub{display:flex}.hd .sub .hd-s{display:none}.hd .sub .hd-t{font-size:13px}}
#prem-grid .dupla{grid-template-columns:1fr;gap:0}
#prem-grid label.chk{display:flex;align-items:flex-start;gap:7px;margin:6px 0 8px;line-height:1.3}
#prem-grid label.chk .aj{margin-left:auto}
#prem-grid .bloco{margin-bottom:6px}
.barra{padding-bottom:12px}
#prem-grid .campo > label .lt{flex:1}
#prem-grid .bloco-tit{min-height:0}
#prem-grid select,#prem-grid input[type=number],#prem-grid input[type=text],#prem-grid input:not([type]){width:100%}
.aj{flex:0 0 auto;width:19px;height:19px;border-radius:50%;border:1px solid var(--petroleo-2);background:#fff;color:var(--petroleo);font:600 12px/17px "IBM Plex Sans",Arial,sans-serif;text-align:center;cursor:pointer;padding:0;margin-left:6px;vertical-align:middle}
.aj:hover,.aj[aria-expanded=true]{background:var(--petroleo);color:#fff;border-color:var(--petroleo)}
#prem-grid .dica.balao{display:none;position:absolute;left:0;right:0;top:100%;z-index:35;margin:2px 0 0;background:#fff;border:1px solid var(--petroleo-2);border-radius:4px;box-shadow:0 6px 18px rgba(16,36,42,.18);padding:10px 12px;font-size:13px;line-height:1.45;color:var(--tinta)}
#prem-grid .dica.balao.aberto{display:block}
@media print{.aj{display:none}#prem-grid .dica.balao{display:block;position:static;border:0;box-shadow:none;padding:0;background:transparent}}""")
s=sub1(s,"""        <div class="bloco-tit">Base do ICMS e do ISS, de 2027 em diante</div>
        <div class="campo" id="c-base">
          <label for="base-sem">A CBS e o IBS entram na base do ICMS e do ISS?</label>
          <select id="base-sem">
            <option value="0">Sim: ICMS e ISS sobre o total da nota</option>
            <option value="1">Não: ICMS e ISS sobre o valor sem CBS e IBS</option>
          </select>""","""        <div class="bloco-tit">Base do ICMS e do ISS em 2027</div>
        <div class="campo" id="c-base">
          <label for="base-sem">CBS e IBS na base do ICMS e do ISS?</label>
          <select id="base-sem">
            <option value="0">Sim, sobre o total da nota</option>
            <option value="1">Não, sobre o valor sem CBS e IBS</option>
          </select>""")
s=sub1(s,"""function ajustarAbas(){""","""function montarBaloes(){
  let n = 0;
  document.querySelectorAll("#prem-grid p.dica").forEach(d=>{
    if (d.closest("#ficha") || d.classList.contains("balao")) return;
    const pai = d.parentNode; let rot = d.previousElementSibling;
    while (rot && rot.tagName !== "LABEL") rot = rot.previousElementSibling;
    if (!rot) return;
    if (!d.id) d.id = "aj-" + (++n);
    const marca = rot.querySelector("input[type=checkbox],input[type=radio]");
    if (!marca && !rot.querySelector(".lt")){ const sp = document.createElement("span"); sp.className = "lt"; while (rot.firstChild) sp.appendChild(rot.firstChild); rot.appendChild(sp); }
    if (marca) rot.classList.add("chk");
    const b = document.createElement("button"); b.type = "button"; b.className = "aj"; b.textContent = "?";
    b.setAttribute("aria-label", "Explicação deste campo"); b.setAttribute("aria-expanded", "false"); b.setAttribute("aria-controls", d.id);
    rot.appendChild(b); d.classList.add("balao");
    if (getComputedStyle(pai).position === "static") pai.style.position = "relative";
  });
  document.addEventListener("click", e=>{
    const b = e.target.closest(".aj");
    document.querySelectorAll("#prem-grid .dica.balao.aberto").forEach(d=>{
      if (b && b.getAttribute("aria-controls") === d.id) return;
      if (!b && d.contains(e.target)) return;
      d.classList.remove("aberto"); const bt = document.querySelector('.aj[aria-controls="'+d.id+'"]'); if (bt) bt.setAttribute("aria-expanded", "false");
    });
    if (!b) return;
    e.preventDefault(); e.stopPropagation();
    const d = document.getElementById(b.getAttribute("aria-controls")); if (!d) return;
    const ab = d.classList.toggle("aberto"); b.setAttribute("aria-expanded", ab ? "true" : "false");
  }, true);
  document.addEventListener("keydown", e=>{ if (e.key === "Escape") document.querySelectorAll("#prem-grid .dica.balao.aberto").forEach(d=>{ d.classList.remove("aberto"); const bt = document.querySelector('.aj[aria-controls="'+d.id+'"]'); if (bt) bt.setAttribute("aria-expanded", "false"); }); });
}
function ajustarAbas(){""")
s=sub1(s,"""  window.addEventListener("resize", ajustarAbas); ajustarAbas(); irAba("hoje");""","""  montarBaloes();
  window.addEventListener("resize", ajustarAbas); ajustarAbas(); irAba("hoje");""")
# revisão de frontend (R26-03): selo de versão no cabeçalho, ficha do código em largura total, rolagem sem esconder o topo
s=sub1(s,"""#prem-grid .campo{position:relative;margin-bottom:12px}""","""#prem-grid .campo{position:relative;margin-bottom:12px}
#prem,#abas{scroll-margin-top:calc(var(--hh,140px) + 10px)}
#selo-versao.no-topo{position:static!important;background:transparent!important;opacity:1!important;padding:0!important;margin-left:16px;font:500 11.5px "IBM Plex Sans",Arial,sans-serif!important;color:var(--petroleo-3)!important;white-space:nowrap}
#prem-ficha{margin:0 0 12px}
#prem-ficha:empty{display:none}
#prem.fechado #prem-ficha{display:none}
@media(min-width:1001px){#prem-ficha #ficha{max-width:none}}
@media(max-width:700px){#selo-versao.no-topo{margin-left:auto;font-size:10.5px!important}}
@media print{#selo-versao.no-topo{color:#2A5F6B!important}#prem.fechado #prem-ficha{display:block}}""")
s=sub1(s,"""  col.forEach(c=>grid.appendChild(c)); prem.appendChild(grid);""","""  col.forEach(c=>grid.appendChild(c)); prem.appendChild(grid);
  const pf = document.createElement("div"); pf.id = "prem-ficha"; prem.appendChild(pf);
  const fi = prem.querySelector("#ficha"); if (fi) pf.appendChild(fi);""")
s=sub1(s,"""  const pmd = $("#p-md"); if (!pmd) return;""","""  const sv = $("#selo-versao"), hd = document.querySelector("header .hd");
  if (sv && hd && !sv.classList.contains("no-topo")){ sv.classList.add("no-topo"); sv.textContent = sv.textContent.replace(/, de .*$/, ""); hd.appendChild(sv); }
  const pmd = $("#p-md"); if (!pmd) return;""")
# cabeçalho com o lema institucional e escolha de tipo e de simulação em uma linha de quatro botões
s=sub1(s,"""  <span class="sub">Preço por produto ou serviço na reforma tributária</span>""","""  <span class="sub"><span class="hd-t">Preço por produto ou serviço na reforma tributária</span><span class="hd-s">Pessoas, processos e tecnologia a favor do seu negócio</span></span>""")
s=sub1(s,"""  prem.appendChild($("#modo"));""","""  const topo = document.createElement("div"); topo.id = "prem-topo";
  topo.appendChild($("#tipo")); topo.appendChild($("#modo")); prem.appendChild(topo);""")
