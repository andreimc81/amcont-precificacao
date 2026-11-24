# ===== rodada 24 (versão 2026.8.11): R24-01 a R24-03 =====
# R24-01: barra de anos fixa no topo; R24-02: alíquotas de CBS, IBS e transição editáveis; R24-03: painel "Todos os anos" com tabela e gráfico
s=sub1(s,""".anos{display:flex;gap:4px;flex-wrap:wrap}""",""".anos{display:flex;gap:4px;flex-wrap:wrap}
.faixa-ano{position:sticky;top:0;z-index:40;background:var(--nota);border-bottom:1px solid var(--linha);box-shadow:0 2px 0 rgba(16,36,42,.05);padding:9px 0 7px;margin-bottom:12px}
.faixa-ano .fa-in{display:flex;align-items:center;gap:12px}
.faixa-ano .fa-rot{font:500 10.5px "IBM Plex Mono";letter-spacing:.16em;text-transform:uppercase;color:var(--petroleo-2);white-space:nowrap}
.faixa-ano .anos{flex:1;flex-wrap:nowrap;overflow-x:auto}
.faixa-ano .dica{margin-top:5px}
#aviso-aliq{margin-top:6px;padding:7px 10px;background:#FBEDE7;border-left:3px solid var(--carimbo);font-size:12.5px;color:var(--tinta);line-height:1.4}
#aviso-aliq[hidden]{display:none}
.rolar{overflow-x:auto}
table.todos{border-collapse:collapse;width:100%;min-width:640px;font-size:13px}
table.todos th,table.todos td{padding:6px 8px;text-align:right;border-bottom:1px solid var(--linha);white-space:nowrap}
table.todos th:first-child,table.todos td:first-child{text-align:left;white-space:normal;min-width:190px;position:sticky;left:0;background:var(--nota)}
table.todos th[data-a]{cursor:pointer;font:500 12px "IBM Plex Mono";color:var(--petroleo)}
table.todos tr.grp td{font:500 10.5px "IBM Plex Mono";letter-spacing:.14em;text-transform:uppercase;color:var(--petroleo-2);background:var(--via-2);text-align:left}
table.todos .sel{background:#EAF2F4}
table.todos td.neg{color:var(--carimbo)}table.todos td.pos{color:var(--saldo)}
.graf{position:relative;margin:14px 0 6px}
.graf svg{width:100%;height:auto;display:block}
.graf .tip{position:absolute;pointer-events:none;background:#fff;border:1px solid var(--linha);padding:7px 9px;font-size:12px;box-shadow:0 2px 8px rgba(16,36,42,.12);display:none;min-width:190px;z-index:5}
.graf .tip b{font:600 12.5px "IBM Plex Mono";color:var(--tinta)}
.graf .tip .k{display:inline-block;width:14px;height:0;border-top:3px solid;vertical-align:middle;margin-right:6px}
.leg{display:flex;gap:18px;flex-wrap:wrap;font-size:12.5px;color:#4E6165;margin-top:4px}
.leg .k{display:inline-block;width:18px;height:0;border-top:3px solid;vertical-align:middle;margin-right:6px}
#p-aliq summary{cursor:pointer;font:500 11px "IBM Plex Mono";letter-spacing:.16em;text-transform:uppercase;color:var(--petroleo-2)}
#p-aliq table{border-collapse:collapse;margin:12px 0}
#p-aliq th,#p-aliq td{padding:5px 8px;border-bottom:1px solid var(--linha);font-size:13px;text-align:right}
#p-aliq th:first-child,#p-aliq td:first-child{text-align:left}
#p-aliq input[type=number]{width:96px;padding:5px 7px;font-size:13px}
#p-aliq .atalhos{display:flex;gap:12px;flex-wrap:wrap;align-items:flex-end;margin:8px 0}
#p-aliq .atalhos .campo{margin:0}
@media print{.faixa-ano{position:static}}
header{position:sticky;top:0;z-index:45}
.faixa-ano{top:var(--hh,66px)}
@media(max-width:700px){header{position:static}.faixa-ano{top:0}}
@media print{header{position:static}}""")
# faixa de anos fixa no topo no lugar do bloco "Ano de referência"
s=sub1(s,"""      <div class="bloco">
        <div class="bloco-tit">Ano de referência</div>
        <div class="anos" id="anos"></div>
        <p class="dica" id="dica-ano"></p>
      </div>
""","")
s=sub1(s,"""<main class="wrap">
  <div class="barra">""","""<main class="wrap">
  <div class="faixa-ano" id="faixa-ano">
    <div class="fa-in"><span class="fa-rot">Ano simulado</span><div class="anos" id="anos"></div></div>
    <p class="dica" id="dica-ano"></p>
    <div id="aviso-aliq" role="status" hidden></div>
  </div>
  <div class="barra">""")
s=sub1(s,"""  <div class="rod">
    <h3>Antes de usar este número</h3>""","""  <div class="painel" id="p-todos"></div>
  <details class="painel" id="p-aliq">
    <summary>Alíquotas simuladas: CBS, IBS e transição do ICMS e do ISS (editáveis)</summary>
    <p class="dica" style="margin-top:8px;max-width:90ch">As alíquotas de 2027 em diante ainda não estão definidas em lei: vêm preenchidas com as estimativas atuais e podem ser alteradas para simular cenários. Tudo recalcula na hora, inclusive o quadro Todos os anos. Alterar estes valores não muda a lei: o resultado deixa de ser o cenário previsto, e a faixa no topo avisa enquanto houver alteração.</p>
    <div id="aliq-tabela"></div>
    <div class="atalhos">
      <div class="campo"><label for="al-dcbs">Somar à CBS, de 2027 a 2033 (pontos percentuais)</label><input id="al-dcbs" type="number" step="0.1" value="0"></div>
      <div class="campo"><label for="al-dibs">Somar ao IBS pleno de 2033 (pontos percentuais), com a transição proporcional</label><input id="al-dibs" type="number" step="0.1" value="0"></div>
      <button type="button" class="btn" id="al-aplicar">Aplicar a partir dos valores previstos</button>
      <button type="button" class="btn" id="al-reset">Voltar aos valores previstos</button>
    </div>
    <p class="dica" id="al-ref"></p>
  </details>

  <div class="rod">
    <h3>Antes de usar este número</h3>""")
# lógica
s=sub1(s,"""function desenharNotaVenda(o, A){""","""/* R24-02: alíquotas editáveis */
const TRANS0 = JSON.parse(JSON.stringify(P.transicao));
const fmtP = x => String(+(x*100).toFixed(4)).replace(".", ",");
function aliqAlterada(){
  return P.transicao.some((t,i)=> Math.abs(t.cbs-TRANS0[i].cbs)>1e-9 || Math.abs(t.ibs-TRANS0[i].ibs)>1e-9 || Math.abs(t.fatorIcmsIss-TRANS0[i].fatorIcmsIss)>1e-9);
}
function montarAliq(){
  $("#aliq-tabela").innerHTML = `<div class="rolar"><table><thead><tr><th>Ano</th><th>CBS (%)</th><th>IBS (%)</th><th>ICMS e ISS que permanecem (%)</th><th>CBS mais IBS</th></tr></thead><tbody>`
    + P.transicao.map(t=>{ const d = t.ano === 2026;
      return `<tr><td>${t.ano}</td>`
      + `<td><input type="number" step="0.01" min="0" max="100" id="al-${t.ano}-cbs" value="${+(t.cbs*100).toFixed(4)}" ${d?"disabled":""}></td>`
      + `<td><input type="number" step="0.01" min="0" max="100" id="al-${t.ano}-ibs" value="${+(t.ibs*100).toFixed(4)}" ${d?"disabled":""}></td>`
      + `<td><input type="number" step="1" min="0" max="100" id="al-${t.ano}-fat" value="${+(t.fatorIcmsIss*100).toFixed(4)}" ${d?"disabled":""}></td>`
      + `<td id="al-${t.ano}-soma">${d?"teste, sem efeito no preço":""}</td></tr>`; }).join("")
    + `</tbody></table></div>`;
}
function lerAliq(){
  P.transicao.forEach(t=>{
    if (t.ano === 2026) return;
    const f = (k, atual)=>{ const el = document.getElementById("al-"+t.ano+"-"+k); if (!el) return atual;
      const v = parseFloat(el.value); if (!isFinite(v) || v < 0 || v > 100) return atual; return Math.round(v*1e4)/1e6; };
    t.cbs = f("cbs", t.cbs); t.ibs = f("ibs", t.ibs); t.fatorIcmsIss = f("fat", t.fatorIcmsIss);
    const sm = document.getElementById("al-"+t.ano+"-soma"); if (sm) sm.textContent = fmtP(t.cbs + t.ibs) + "%";
  });
}
function escreverAliq(){
  P.transicao.forEach(t=>{ if (t.ano === 2026) return;
    $("#al-"+t.ano+"-cbs").value = +(t.cbs*100).toFixed(4); $("#al-"+t.ano+"-ibs").value = +(t.ibs*100).toFixed(4); $("#al-"+t.ano+"-fat").value = +(t.fatorIcmsIss*100).toFixed(4); });
  lerAliq();
}
function sinalAliq(){
  const el = $("#aviso-aliq"); if (!el) return;
  const alt = aliqAlterada(); el.hidden = !alt;
  if (alt){
    const ref = P.transicao.find(t=>t.ano===2033), r0 = TRANS0.find(t=>t.ano===2033);
    el.innerHTML = `<b>Simulação com alíquotas alteradas.</b> Este resultado não é o cenário previsto. Em 2033, CBS mais IBS: <b>${PCT(ref.cbs+ref.ibs)}</b> contra <b>${PCT(r0.cbs+r0.ibs)}</b> previstos. `
      + `<a href="#p-aliq" id="al-ver">Ver ou restaurar</a>`;
  }
  const r = $("#al-ref"); if (r){ const t33 = P.transicao.find(t=>t.ano===2033); r.textContent = "Alíquota combinada de CBS e IBS em 2033, nesta simulação: "+PCT(t33.cbs+t33.ibs)+". Previsto: "+PCT(TRANS0.find(t=>t.ano===2033).cbs+TRANS0.find(t=>t.ano===2033).ibs)+"."; }
}
function ajustarTopo(){ const h = document.querySelector("header"); if (h) document.documentElement.style.setProperty("--hh", h.offsetHeight + "px"); }
function iniciarAliq(){
  ajustarTopo(); window.addEventListener("resize", ajustarTopo);
  montarAliq(); lerAliq();
  $("#aliq-tabela").addEventListener("input", ()=>{ lerAliq(); calcular(); });
  $("#al-aplicar").addEventListener("click", ()=>{
    const dc = (parseFloat($("#al-dcbs").value)||0)/100, di = (parseFloat($("#al-dibs").value)||0)/100;
    const ib33 = TRANS0.find(t=>t.ano===2033).ibs;
    TRANS0.forEach((b,i)=>{ const t = P.transicao[i]; if (b.ano < 2027) return;
      t.cbs = Math.max(0, b.cbs + dc);
      t.ibs = b.ano >= 2029 ? Math.max(0, b.ibs * (ib33 + di) / ib33) : b.ibs;
      t.fatorIcmsIss = b.fatorIcmsIss; });
    escreverAliq(); calcular();
  });
  $("#al-reset").addEventListener("click", ()=>{
    TRANS0.forEach((b,i)=>{ Object.assign(P.transicao[i], {cbs:b.cbs, ibs:b.ibs, fatorIcmsIss:b.fatorIcmsIss}); });
    $("#al-dcbs").value = 0; $("#al-dibs").value = 0; escreverAliq(); calcular();
  });
  document.addEventListener("click", e=>{ if (e.target && e.target.id === "al-ver"){ e.preventDefault(); const d = $("#p-aliq"); d.open = true; d.scrollIntoView({behavior:"smooth"}); } });
}

/* R24-03: quadro Todos os anos, independente do ano selecionado */
function linhaAno(o, H, ano){
  const o2 = Object.assign({}, o, {ano});
  const A = noAno(o2, H.mc, o.pcAno, o.forn, o.aliqForn, o.anexoForn);
  const M = mesmoDesembolso(o2, A);
  const g = A.tipo === "geral";
  const nf = g ? A.nf : A.hib.nf, cad = g ? (ano >= 2027 ? A.nf - A.cbs - A.ibs : A.nf) : A.hib.preco;
  const mc2 = M ? (g ? M.mc : M.hib.mc) : H.mc, alvo = g ? A.mc : H.mc;
  return {ano, A, M, g, nf, cad, var: nf/o.pv - 1, cad2: M ? (g ? M.cad : M.hib.cad) : null, mc2, perda: alvo - mc2, pperda: alvo > 0.005 ? (alvo - mc2)/alvo : 0,
          nfT: g ? null : A.trad.nf, mc2T: (M && !g) ? M.trad.mc : null, perdaT: (M && !g) ? H.mc - M.trad.mc : null};
}
function atualizarTodos(o, H){
  const el = $("#p-todos"); if (!el) return;
  const L = P.transicao.map(t=>linhaAno(o, H, t.ano));
  const un = o.servico ? "serviço" : "produto", simp = !L[0].g;
  const sg = x => (x>=0?"+":"") + PCT(x), cls = x => x > 0.00005 ? "neg" : (x < -0.00005 ? "pos" : "");
  const c = (l, f, extra) => `<td class="${l.ano===ANO?"sel ":""}${extra||""}">${f}</td>`;
  const lin = (rot, fn, ex) => `<tr><td>${rot}</td>` + L.map(l=>c(l, fn(l), ex ? ex(l) : "")).join("") + `</tr>`;
  const grp = t => `<tr class="grp"><td colspan="${L.length+1}">${t}</td></tr>`;
  const sem = "sem efeito";
  let h = `<h3>Todos os anos <em>2026 a 2033</em></h3>`
    + `<p class="dica" style="margin-bottom:8px">Este quadro não muda com o ano escolhido na barra do topo: ele reage aos dados da ficha e às alíquotas simuladas. O ano escolhido aparece destacado. Clique em um ano para selecioná-lo.</p>`
    + `<div class="rolar"><table class="todos" id="tb-todos"><thead><tr><th></th>` + L.map(l=>`<th data-a="${l.ano}" class="${l.ano===ANO?"sel":""}">${l.ano}</th>`).join("") + `</tr></thead><tbody>`
    + grp("Preço que preserva a margem")
    + lin("Valor do "+un+" a cadastrar" + (simp ? ", regime regular" : ""), l=>BRL.format(l.cad))
    + lin("Total da nota, o que o cliente paga" + (simp ? ", regime regular" : ""), l=>BRL.format(l.nf))
    + lin("Variação do total contra hoje", l=>sg(l.var), l=>cls(l.var))
    + (simp ? lin("Total da nota, Simples tradicional", l=>BRL.format(l.nfT)) : "")
    + grp("Mesmo desembolso do cliente (total da nota igual ao de hoje, " + BRL.format(o.pv) + ")")
    + lin("Valor do "+un+" a cadastrar" + (simp ? ", regime regular" : ""), l=>l.cad2 == null ? sem : BRL.format(l.cad2))
    + lin("Margem de contribuição" + (simp ? ", regime regular" : ""), l=>BRL.format(l.mc2))
    + lin("Redução da margem, R$ por unidade", l=>l.M ? BRL.format(l.perda) : sem, l=>cls(l.perda))
    + lin("Redução da margem, % da margem preservada", l=>l.M ? sg(l.pperda) : sem, l=>cls(l.pperda))
    + (simp ? lin("Redução da margem, Simples tradicional, R$", l=>l.perdaT == null ? sem : BRL.format(l.perdaT), l=>cls(l.perdaT||0)) : "")
    + `</tbody></table></div>`;
  h += `<div class="graf" id="graf"></div>`
    + `<div class="leg"><span><i class="k" style="border-color:#0A7FA0"></i>Preço necessário: variação do total da nota contra hoje</span>`
    + `<span><i class="k" style="border-color:#A63D1B;border-top-style:dashed"></i>Mesmo desembolso: redução da margem, % da margem preservada</span></div>`
    + `<p class="dica" style="margin-top:8px">Valores acima de zero na linha tracejada significam margem menor se o aumento de carga não for repassado; abaixo de zero, margem maior. `
    + `2026 não tem efeito de CBS e IBS no preço. De 2027 em diante, as alíquotas são estimativas${aliqAlterada() ? ", alteradas nesta simulação" : ""}.</p>`;
  el.innerHTML = h;
  el.querySelector("thead").addEventListener("click", e=>{ const th = e.target.closest("th[data-a]"); if (th){ const b = $('#anos button[data-a="'+th.dataset.a+'"]'); if (b) b.click(); } });
  desenharGraf(L);
}
function desenharGraf(L){
  const W = 720, Hh = 270, ml = 54, mr = 90, mt = 16, mb = 30, cinza = "#9DB2B7";
  const s1 = L.map(l=>l.var), s2 = L.map(l=>l.pperda);
  let lo = Math.min(0, ...s1, ...s2), hi = Math.max(0, ...s1, ...s2);
  if (hi - lo < 0.01){ hi += 0.005; lo -= 0.005; }
  const pad = (hi - lo)*0.12; lo -= pad; hi += pad;
  const X = i => ml + i*(W-ml-mr)/(L.length-1), Y = v => mt + (hi - v)*(Hh-mt-mb)/(hi-lo);
  const passo = (()=>{ const r = hi-lo, bruto = r/4, mag = Math.pow(10, Math.floor(Math.log10(bruto))), n = bruto/mag; return (n<1.5?1:n<3.5?2:n<7.5?5:10)*mag; })();
  let svg = `<svg viewBox="0 0 ${W} ${Hh}" role="img" aria-label="Variação do preço e redução da margem, de 2026 a 2033">`;
  for (let v = Math.ceil(lo/passo)*passo; v <= hi; v += passo){
    const y = Y(v), zero = Math.abs(v) < passo/1000;
    svg += `<line x1="${ml}" x2="${W-mr}" y1="${y}" y2="${y}" stroke="${zero?"#5C6E72":"#DDE6E8"}" stroke-width="${zero?1.4:1}"/>`
        + `<text x="${ml-8}" y="${y+4}" text-anchor="end" font-size="11" fill="#5C6E72" font-family="IBM Plex Mono">${(v*100).toFixed(Math.abs(passo)<0.01?1:0).replace(".", ",")}%</text>`;
  }
  L.forEach((l,i)=>{ const sel = l.ano === ANO;
    if (sel) svg += `<rect x="${X(i)-((W-ml-mr)/(L.length-1))/2}" y="${mt}" width="${(W-ml-mr)/(L.length-1)}" height="${Hh-mt-mb}" fill="#EAF2F4"/>`;
    svg += `<text x="${X(i)}" y="${Hh-9}" text-anchor="middle" font-size="11.5" ${sel?'font-weight="700"':''} fill="#10242A" font-family="IBM Plex Mono">${l.ano}</text>`; });
  const linha = (vals, cor, dash, forma)=>{
    let d = vals.map((v,i)=>(i?"L":"M")+X(i)+" "+Y(v)).join(" ");
    let t = `<path d="${d}" fill="none" stroke="${cor}" stroke-width="2" ${dash?'stroke-dasharray="6 4"':""}/>`;
    vals.forEach((v,i)=>{ t += forma === "q" ? `<rect x="${X(i)-4}" y="${Y(v)-4}" width="8" height="8" fill="${cor}" stroke="#fff" stroke-width="2"/>` : `<circle cx="${X(i)}" cy="${Y(v)}" r="4.5" fill="${cor}" stroke="#fff" stroke-width="2"/>`; });
    return t; };
  svg += linha(s1, "#0A7FA0", false, "q") + linha(s2, "#A63D1B", true, "c");
  const ult = L.length-1; let y1 = Y(s1[ult]), y2 = Y(s2[ult]); if (Math.abs(y1-y2) < 15){ if (y1 <= y2){ y1 -= 8; y2 += 8; } else { y1 += 8; y2 -= 8; } }
  svg += `<text x="${X(ult)+9}" y="${y1+4}" font-size="11.5" fill="#10242A" font-family="IBM Plex Sans">Preço</text><text x="${X(ult)+9}" y="${y2+4}" font-size="11.5" fill="#10242A" font-family="IBM Plex Sans">Margem</text>`;
  svg += `<line id="gcruz" x1="0" x2="0" y1="${mt}" y2="${Hh-mb}" stroke="#5C6E72" stroke-width="1" style="display:none"/>`;
  L.forEach((l,i)=>{ const w = (W-ml-mr)/(L.length-1); svg += `<rect class="ghit" data-i="${i}" x="${X(i)-w/2}" y="${mt}" width="${w}" height="${Hh-mt-mb}" fill="transparent" tabindex="0"/>`; });
  svg += `</svg><div class="tip" id="gtip"></div>`;
  const g = $("#graf"); g.innerHTML = svg;
  const tip = $("#gtip"), cruz = g.querySelector("#gcruz");
  const mostrar = i=>{
    const l = L[i]; tip.replaceChildren();
    const t = document.createElement("div"); t.style.cssText = "font:600 12px IBM Plex Mono;margin-bottom:4px"; t.textContent = String(l.ano); tip.appendChild(t);
    [["#0A7FA0","", "Total da nota", BRL.format(l.nf)+" ("+(l.var>=0?"+":"")+PCT(l.var)+")", false],
     ["#A63D1B","dashed", "Margem no mesmo desembolso", BRL.format(l.mc2)+" ("+(l.pperda>=0?"-":"+")+PCT(Math.abs(l.pperda))+")", true]].forEach(([cor,est,nome,val])=>{
      const r = document.createElement("div"); const k = document.createElement("i"); k.className = "k"; k.style.borderColor = cor; if (est) k.style.borderTopStyle = est;
      const b = document.createElement("b"); b.textContent = val; const n = document.createElement("span"); n.textContent = "  " + nome; n.style.color = "#5C6E72";
      r.append(k, b, n); tip.appendChild(r); });
    tip.style.display = "block";
    const gx = (X(i)/W)*g.clientWidth; tip.style.left = Math.min(g.clientWidth - tip.offsetWidth - 4, Math.max(0, gx + 12)) + "px"; tip.style.top = "8px";
    cruz.setAttribute("x1", X(i)); cruz.setAttribute("x2", X(i)); cruz.style.display = "";
  };
  const ocultar = ()=>{ tip.style.display = "none"; cruz.style.display = "none"; };
  g.querySelectorAll(".ghit").forEach(r=>{ const i = +r.dataset.i;
    r.addEventListener("pointermove", ()=>mostrar(i)); r.addEventListener("focus", ()=>mostrar(i)); r.addEventListener("pointerleave", ocultar); r.addEventListener("blur", ocultar);
    r.addEventListener("click", ()=>{ const b = $('#anos button[data-a="'+L[i].ano+'"]'); if (b) b.click(); }); });
}
function desenharNotaVenda(o, A){""")
s=sub1(s,"""  if (MODO === "compra") calcCompra(o);
  $("#dica-ano").textContent""","""  atualizarTodos(o, H); sinalAliq();
  if (MODO === "compra") calcCompra(o);
  $("#dica-ano").textContent""")
s=sub1(s,"""  prepararCompra();
  preencherSetores();""","""  prepararCompra();
  iniciarAliq();
  preencherSetores();""")
s=sub1(s,"""      sincronizar(); calcular();
      const va = window.AMCONT_VERSAO""","""      lerAliq(); sincronizar(); calcular();
      const va = window.AMCONT_VERSAO""")
