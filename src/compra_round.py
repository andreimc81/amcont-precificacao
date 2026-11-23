# ===== rodada 7: modo Compra (custo real por fornecedor) e nota fiscal da venda =====
# --- correcao: fornecedor do Simples optante do regime regular de CBS e IBS continua com o ICMS no DAS
s=sub1(s,"""  // ICMS: MEI e pessoa fisica nao transferem credito. O Simples tradicional transfere so o ICMS
  // efetivamente pago no DAS (LC 123/2006, art. 23, paragrafos 1 e 2): DAS x parcela de ICMS do anexo.
  let icms = 0;
  if (forn === "sn_tradicional"){""","""  // ICMS: MEI e pessoa fisica nao transferem credito. O Simples, tradicional ou optante do regime
  // regular de CBS e IBS, transfere so o ICMS efetivamente pago no DAS (LC 123/2006, art. 23):
  // DAS x parcela de ICMS do anexo. A opcao pelo regime regular tira do DAS so a CBS e o IBS.
  let icms = 0;
  if (forn === "sn_tradicional" || forn === "sn_regular"){""")
s=sub1(s,"""  $("#c-aliqforn").hidden = $("#forn").value!=="sn_tradicional";""","""  $("#c-aliqforn").hidden = !["sn_tradicional","sn_regular"].includes($("#forn").value);""")
s=sub1(s,"""<li>O crédito transferido por fornecedor do Simples tradicional é limitado ao que ele paga dentro do DAS: a parcela de CBS e IBS e, no ICMS,""","""<li>O crédito transferido por fornecedor do Simples é limitado ao que ele paga dentro do DAS. No Simples tradicional vale para a CBS, o IBS e o ICMS; no optante do regime regular de CBS e IBS, só para o ICMS, que continua no DAS. No ICMS,""")

# --- CSS
s=sub1(s,"""\n[hidden]{display:none!important}""","""\n[hidden]{display:none!important}
body:not(.modo-compra) .so-compra{display:none!important}
body.modo-compra .so-venda{display:none!important}
#modo{margin-bottom:18px}
table.cot input,table.cot select{width:100%;padding:5px 6px;font-size:12.5px;min-width:0}
table.cot td{padding:4px 0 4px 6px;vertical-align:middle}
table.cot td:first-child{padding-left:0}
table.cot input:disabled,table.cot select:disabled{opacity:.35}
table.cot button{padding:4px 8px}
table.nf td{padding:5px 0 5px 10px}
table.nf tr.tot td{font-weight:700;border-top:2px solid var(--tinta);border-bottom:none}
table.nf tr.cr td{color:var(--saldo)}
table.nf tr.sub td{color:#5C6E72;font-size:12px}
table.nf tr.sep td{padding-top:14px;font:600 10px "IBM Plex Mono";letter-spacing:.1em;text-transform:uppercase;color:var(--petroleo-2);border-bottom:1px solid var(--linha)}
#p-compra tr[data-i]{cursor:pointer}
#p-compra tr.ver td{box-shadow:inset 0 -2px 0 var(--petroleo)}""")

# --- HTML: seletor de modo, campos da compra e paineis
s=sub1(s,"""      <div class="bloco">
        <div class="bloco-tit" id="tit-item">""","""      <div class="seg" id="modo" role="group" aria-label="O que simular">
        <button type="button" data-m="venda" aria-pressed="true">Simular uma venda: preço necessário</button>
        <button type="button" data-m="compra" aria-pressed="false">Simular uma compra: custo real</button>
      </div>
      <div class="bloco">
        <div class="bloco-tit" id="tit-item">""")
s=sub1(s,"""        <div class="campo">
          <label for="icms-venda" id="lb-icms-venda">""","""        <div class="campo so-compra" id="c-snop">
          <label for="sn-opcao">No Simples, como você recolhe a CBS e o IBS</label>
          <select id="sn-opcao">
            <option value="das">Dentro do DAS (Simples tradicional)</option>
            <option value="regular">Pelo regime regular, fora do DAS</option>
          </select>
          <p class="dica">Dentro do DAS, você não toma crédito de CBS e IBS nas compras (LC 214/2025, art. 47, § 9º, I). Pelo regime regular, toma. O ICMS continua no DAS nos dois casos e não gera crédito.</p>
        </div>
        <div class="campo so-compra">
          <label for="destino">Destinação da compra</label>
          <select id="destino">
            <option value="revenda">Revenda ou insumo de produção</option>
            <option value="uso">Uso e consumo do estabelecimento</option>
            <option value="imob">Ativo imobilizado</option>
          </select>
          <p class="dica" id="dica-destino"></p>
        </div>
        <div class="campo">
          <label for="icms-venda" id="lb-icms-venda">""")
s=sub1(s,"""      <div class="painel" id="p-ano"></div>""","""      <div class="painel so-compra" id="p-cot">
        <h3>Cotações de compra <em>valor total da nota</em></h3>
        <div style="overflow-x:auto"><table class="cmp cot" id="cot"><thead><tr>
          <th style="width:24%">Fornecedor</th><th style="width:27%">Regime</th><th>Valor da nota</th>
          <th class="cot-icms">ICMS %</th><th>DAS %</th><th>Anexo</th><th></th></tr></thead><tbody></tbody></table></div>
        <div class="barra" style="padding-top:10px">
          <button type="button" class="btn" id="b-cot-add">Adicionar cotação</button>
          <button type="button" class="btn" id="b-cot-5">Comparar os 5 regimes pelo preço da 1ª linha</button>
        </div>
        <p class="dica">Informe o valor total de cada nota, como o fornecedor cobra. O ICMS é o destacado na nota (para Simples, deixe o percentual da mercadoria: o crédito é limitado ao DAS). O DAS e o anexo só valem para fornecedor do Simples.</p>
      </div>
      <div class="painel so-compra" id="p-compra"></div>
      <div class="painel so-compra" id="p-nota-compra"></div>
      <div class="painel" id="p-ano"></div>
      <div class="painel so-venda" id="p-nota"></div>""")

# --- opcoes(): destino e opcao do Simples para a compra
s=sub1(s,"""    forn:$("#forn").value, aliqForn:num("aliqsn-forn")/100, anexoForn:"I",""","""    destino:$("#destino").value, snReg:$("#sn-opcao").value === "regular",
    forn:$("#forn").value, aliqForn:num("aliqsn-forn")/100, anexoForn:"I",""")

# --- motor da compra e da nota
s=sub1(s,"""/* ---------- busca de NCM ---------- */""",r"""/* ---------- simulacao de compra: custo real por fornecedor ---------- */
let MODO = "venda", NOTA_I = null;
const REG_FORN = [["regular","Lucro Real ou Presumido"],["sn_regular","Simples optante pelo regime regular"],
                  ["sn_tradicional","Simples tradicional"],["mei","MEI"],["pf","Pessoa física ou produtor rural"]];
const nomeReg = id => (REG_FORN.find(x=>x[0]===id) || ["", id])[1];
const ehSN = r => r === "sn_tradicional" || r === "sn_regular";
const numTxt = v => parseFloat(String(v).replace(",", ".")) || 0;
function linhaCot(c){
  const sn = ehSN(c.reg);
  return `<tr><td><input data-k="nome" type="text" value="${esc(c.nome||"")}" placeholder="Fornecedor"></td>`
    + `<td><select data-k="reg">${REG_FORN.map(([v,n])=>`<option value="${v}"${v===c.reg?" selected":""}>${n}</option>`).join("")}</select></td>`
    + `<td><input data-k="preco" type="number" step="0.01" min="0" value="${c.preco}"></td>`
    + `<td class="cot-icms"><input data-k="icms" type="number" step="0.01" min="0" value="${c.icms}"></td>`
    + `<td><input data-k="das" type="number" step="0.001" min="0" value="${c.das}"${sn?"":" disabled"}></td>`
    + `<td><select data-k="anexo"${sn?"":" disabled"}>${["I","II","III","IV","V"].map(a=>`<option${a===(c.anexo||"I")?" selected":""}>${a}</option>`).join("")}</select></td>`
    + `<td><button type="button" class="btn" data-rm title="Remover cotação">×</button></td></tr>`;
}
function lerCot(){
  return $$("#cot tbody tr").map(tr=>{ const g = k=>tr.querySelector(`[data-k=${k}]`);
    return {nome:g("nome").value, reg:g("reg").value, preco:numTxt(g("preco").value), icms:numTxt(g("icms").value),
            das:numTxt(g("das").value), anexo:g("anexo").value}; });
}
function escreverCot(l){ $("#cot tbody").innerHTML = l.map(linhaCot).join(""); NOTA_I = null; }
function cotPadrao(preco, icms, das){
  return REG_FORN.map(([v,n])=>({nome:n, reg:v, preco, icms:(v==="mei"||v==="pf") ? 0 : icms, das:das||9.403, anexo:"I"}));
}
/* credito que o comprador aproveita, conforme o regime dele e a destinacao */
function creditoComprador(c, o){
  const icmsC = o.servico ? 0 : c.icms/100;
  const base = creditoCompra(c.preco, c.reg, o.ano, icmsC, c.das/100, c.anexo || "I", o.trat);
  const simplesDAS = o.regime === "simples" && !o.snReg;
  const cbsIbs = simplesDAS ? 0 : base.cbsIbs;                       // LC 214/2025, art. 47, par. 9, I
  const icms = (o.regime === "simples" || o.servico || o.destino === "uso") ? 0 : base.icms;   // LC 87/1996, art. 33, I
  const pc = (o.ano < 2027 && o.destino === "revenda") ? pcCredito(Object.assign({}, o, {icmsCompra:icmsC}), c.preco, c.reg) : 0;
  const total = cbsIbs + icms + pc;
  return {cbsIbs, icms, pc, total, custo:c.preco - total, taxa:c.preco > 0 ? total/c.preco : 0, base};
}
function linhasNf(rows){
  return `<table class="cmp nf"><tbody>` + rows.filter(Boolean).map(([k,v,cls])=>
    `<tr class="${cls||""}"><td>${k}</td><td>${typeof v === "number" ? BRL.format(v) : (v||"")}</td></tr>`).join("") + `</tbody></table>`;
}
function classifTexto(o){
  const x = FICHA && FICHA.opcoes[FICHA.sel];
  if (x && Math.abs(x.red - o.trat) < 1e-9) return "CST "+x.cst+" · cClassTrib "+x.ccl;
  return o.trat > 0 ? "CST 200 · confira o cClassTrib" : "CST 000 · cClassTrib 000001";
}
function calcCompra(o){
  const sv = o.servico, t = tAno(o.ano);
  $$("#cot .cot-icms").forEach(x=>x.style.display = sv ? "none" : "");
  $("#dica-destino").textContent = o.destino === "uso"
    ? "Uso e consumo: sem crédito de ICMS até 2032 (LC 87/1996, art. 33, I). A CBS e o IBS dão crédito, salvo bens de uso ou consumo pessoal."
    : (o.destino === "imob"
      ? "Imobilizado: o crédito de ICMS entra em 48 parcelas mensais; a tabela mostra o total. Em 2026, o crédito de PIS e COFINS do Lucro Real segue a depreciação e não é simulado."
      : "Revenda ou insumo: crédito integral conforme o regime do fornecedor.");
  const L = lerCot().map((c,i)=>Object.assign({i}, c, creditoComprador(c, o))).filter(x=>x.preco > 0);
  if (!L.length){
    $("#p-compra").innerHTML = `<h3>Custo real da compra <em>${o.ano}</em></h3><p class="dica">Informe ao menos uma cotação com valor.</p>`;
    $("#p-nota-compra").innerHTML = ""; return;
  }
  const min = Math.min(...L.map(x=>x.custo)), best = L.find(x=>Math.abs(x.custo - min) < 1e-9);
  const minNF = Math.min(...L.map(x=>x.preco)), barata = L.find(x=>x.preco === minNF);
  const colPc = o.ano < 2027 && o.regime === "real" && o.destino === "revenda";
  const colIcms = !sv && o.regime !== "simples" && o.destino !== "uso";
  const nome = x => esc(x.nome || nomeReg(x.reg));
  if (NOTA_I === null || !L.some(x=>x.i === NOTA_I)) NOTA_I = best.i;
  let h = `<h3>Custo real da compra <em>${o.ano}</em></h3>`
    + `<div class="destaque"><div class="rot">Menor custo real</div><div class="val">${BRL.format(best.custo)}</div>`
    + `<div class="cmp"><b>${nome(best)}</b> (${esc(nomeReg(best.reg))}): nota de ${BRL.format(best.preco)}, `
    + `com ${BRL.format(best.total)} de crédito.</div></div>`;
  if (barata.custo - min > 0.005)
    h += `<p class="dica" style="color:var(--carimbo);margin:10px 0 0"><b>A nota mais barata não é a compra mais barata.</b> `
      + `${nome(barata)} cobra ${BRL.format(barata.preco)}, mas depois dos créditos custa ${BRL.format(barata.custo)}, `
      + `${BRL.format(barata.custo - min)} a mais por unidade.</p>`;
  h += `<table class="cmp" style="margin-top:14px"><thead><tr><th>Fornecedor</th><th>Nota</th><th>Crédito CBS e IBS</th>`
    + (colIcms ? `<th>Crédito ICMS</th>` : "") + (colPc ? `<th>Crédito PIS e COFINS</th>` : "")
    + `<th>Custo real</th><th>Preço máximo para empatar</th><th>A mais</th></tr></thead><tbody>`
    + L.map(x=>{ const eq = x.taxa < 1 ? min/(1 - x.taxa) : 0, m = Math.abs(x.custo - min) < 0.005;
        return `<tr data-i="${x.i}" class="${m?"melhor":""}${x.i===NOTA_I?" ver":""}"><td>${nome(x)}<br><small style="color:#5C6E72">${esc(nomeReg(x.reg))}</small></td>`
          + `<td>${BRL.format(x.preco)}</td><td>${BRL.format(x.cbsIbs)}</td>`
          + (colIcms ? `<td>${BRL.format(x.icms)}</td>` : "") + (colPc ? `<td>${BRL.format(x.pc)}</td>` : "")
          + `<td><b>${BRL.format(x.custo)}</b></td><td>${m ? "" : BRL.format(eq)}</td>`
          + `<td class="${m?"":"neg"}">${m ? "" : BRL.format(x.custo - min)}</td></tr>`; }).join("")
    + `</tbody></table>`;
  const notas = [];
  if (o.regime === "simples" && !o.snReg)
    notas.push("Você está no Simples recolhendo a CBS e o IBS no DAS: não toma crédito de CBS, IBS nem ICMS. O custo real é o valor da nota, e o regime do fornecedor não muda o seu custo.");
  else if (o.regime === "simples")
    notas.push("Optante do regime regular de CBS e IBS: você toma crédito de CBS e IBS, mas não de ICMS, que continua no DAS.");
  if (o.ano < 2027) notas.push("Em 2026, a CBS e o IBS de teste não geram custo nem crédito: valem o ICMS e, no Lucro Real, o PIS e a COFINS.");
  if (L.some(x=>ehSN(x.reg))) notas.push("Fornecedor do Simples transfere crédito limitado ao que paga no DAS: no tradicional, CBS, IBS e ICMS; no optante do regime regular, só o ICMS fica limitado (LC 214/2025, art. 47, § 9º, II; LC 123/2006, art. 23).");
  if (L.some(x=>x.reg === "pf")) notas.push("Compra de produtor rural pessoa física ou não contribuinte pode gerar crédito presumido de CBS e IBS, que não é simulado aqui.");
  notas.push("Preço máximo para empatar: o valor de nota que cada fornecedor teria de cobrar para ter o mesmo custo real da melhor opção. Clique em uma linha para ver a nota.");
  h += `<p class="dica" style="margin-top:10px">${notas.map(esc).join(" ")}</p>`
    + `<div class="barra" style="padding-top:8px"><button type="button" class="btn forte" id="b-cot-usar">Levar a melhor cotação para a simulação de venda</button></div>`;
  $("#p-compra").innerHTML = h;
  $("#p-nota-compra").innerHTML = notaCompra(L.find(x=>x.i === NOTA_I), o);
}
function notaCompra(x, o){
  const t = tAno(o.ano), c = t.cbs*(1-o.trat), b = t.ibs*(1-o.trat), f = t.fatorIcmsIss, icC = o.servico ? 0 : x.icms/100;
  const imp = o.servico ? "ISS" : "ICMS", R = [];
  if (x.reg === "regular" || x.reg === "sn_regular"){
    const icmsN = x.reg === "regular" ? x.preco*icC*f : 0;
    let base = 0, cbs = 0, ibs = 0;
    if (o.ano >= 2027 && c + b > 0){ base = x.preco*(1 - icC*f)/(1 + c + b); cbs = base*c; ibs = base*b; }
    R.push(["Valor do "+(o.servico?"serviço":"produto")+(o.servico?"":" (com ICMS embutido)"), x.preco - cbs - ibs]);
    if (!o.servico) R.push(x.reg === "regular" ? ["ICMS destacado, "+PCT(icC*f), icmsN, "sub"] : ["ICMS dentro do DAS do fornecedor", "não destacado", "sub"]);
    if (o.ano >= 2027){
      R.push(["Base da CBS e do IBS", base, "sub"]);
      R.push(["CBS "+PCT(c)+" · "+classifTexto(o), cbs]); R.push(["IBS "+PCT(b), ibs]);
    } else R.push(["PIS e COFINS do fornecedor", "embutidos no preço", "sub"]);
  } else if (x.reg === "sn_tradicional"){
    R.push(["Valor da nota", x.preco]);
    R.push(["DAS do fornecedor dentro do preço, "+PCT(x.das/100), x.preco*x.das/100, "sub"]);
    if (o.ano >= 2027) R.push(["Parte do DAS que corresponde a CBS e IBS", x.base.cbsIbs, "sub"]);
    if (!o.servico) R.push(["Parte do DAS que corresponde a ICMS", x.base.icms, "sub"]);
  } else {
    R.push(["Valor da nota", x.preco]);
    R.push([x.reg === "mei" ? "MEI: tributos fixos, sem destaque que gere crédito" : "Pessoa física: sem destaque que gere crédito", "", "sub"]);
  }
  R.push(["Total da nota", x.preco, "tot"]);
  R.push(["O que você recupera", "", "sep"]);
  R.push(["Crédito de CBS e IBS", x.cbsIbs, "cr"]);
  if (!o.servico) R.push(["Crédito de ICMS"+(o.destino === "imob" && x.icms > 0 ? ", em 48 parcelas" : ""), x.icms, "cr"]);
  if (x.pc > 0.005) R.push(["Crédito de PIS e COFINS", x.pc, "cr"]);
  R.push(["Custo real", x.custo, "tot"]);
  return `<h3>A nota de ${esc(x.nome || nomeReg(x.reg))} <em>${o.ano}</em></h3>` + linhasNf(R)
    + `<p class="dica" style="margin-top:10px">Leiaute ilustrativo. A CBS e o IBS são calculados por fora, sobre o valor sem ${imp}, e somados ao total da nota. `
    + `Confira com a nota real do fornecedor: o crédito só vale para o que estiver destacado e, no Simples, para o que ele informar como pago no DAS.</p>`;
}
function desenharNotaVenda(o, A){
  const el = $("#p-nota"), imp = o.servico ? "ISS" : "ICMS", doc = o.servico ? "NFS-e" : "NF-e";
  let R = [], nota = "";
  if (A.tipo === "geral" && o.ano >= 2027){
    const base = A.nf - A.icms - A.cbs - A.ibs;
    R = [["Valor do "+(o.servico?"serviço":"produto")+" (com "+imp+(A.impSel>0.005?" e Imposto Seletivo":"")+" embutidos)", A.nf - A.cbs - A.ibs],
         ["Base do "+imp+": total da nota", A.nf, "sub"], [imp+" "+PCT(A.i), A.icms],
         A.impSel > 0.005 ? ["Base do Imposto Seletivo", base - A.impSel, "sub"] : null,
         A.impSel > 0.005 ? ["Imposto Seletivo "+PCT(o.is), A.impSel] : null,
         ["Base da CBS e do IBS: valor sem "+imp+", CBS e IBS", base, "sub"],
         ["CBS "+PCT(A.c)+" · "+classifTexto(o), A.cbs], ["IBS "+PCT(A.b), A.ibs],
         ["Total da nota: o que o cliente paga", A.nf, "tot"],
         ["Para quem compra de você", "", "sep"],
         ["Crédito de CBS e IBS do comprador do regime regular", A.cbs + A.ibs, "cr"],
         ["Custo do comprador sem o crédito de "+imp, A.nf - A.cbs - A.ibs, "sub"]];
    nota = `Total = valor do ${o.servico?"serviço":"produto"} + CBS + IBS. O preço de etiqueta ao consumidor é o total da nota. `
      + `Se o sistema emissor soma a CBS e o IBS por fora, o preço a cadastrar é ${BRL.format(A.nf - A.cbs - A.ibs)}. Confirme com o fornecedor do sistema.`;
  } else if (A.tipo === "geral"){
    R = [["Valor do "+(o.servico?"serviço":"produto"), A.nf], [imp+" "+PCT(A.i), A.icms],
         A.pisCof > 0.005 ? ["PIS e COFINS embutidos no preço", A.pisCof, "sub"] : null,
         ["Total da nota", A.nf, "tot"]];
    nota = "Em 2026 a nota destaca a CBS e o IBS de teste só para informação; eles não mudam o preço nem a margem.";
  } else {
    const t = tAno(o.ano), crT = creditoCompra(A.trad.nf, "sn_tradicional", o.ano, o.servico ? 0 : o.icmsVenda, o.aliqSN, o.anexo, o.trat);
    R = [["Simples tradicional", "", "sep"], ["Total da nota", A.trad.nf, "tot"], ["DAS dentro do preço", A.trad.das, "sub"],
         o.ano >= 2027 ? ["Crédito de CBS e IBS para o comprador do regime regular", crT.cbsIbs, "cr"] : null];
    if (o.ano >= 2027) R.push(["Optante do regime regular de CBS e IBS", "", "sep"],
         ["Valor do "+(o.servico?"serviço":"produto"), A.hib.preco], ["Base da CBS e do IBS", A.c > 0 ? A.hib.cbs/A.c : 0, "sub"],
         ["CBS "+PCT(A.c)+" · "+classifTexto(o), A.hib.cbs], ["IBS "+PCT(A.b), A.hib.ibs],
         ["Total da nota", A.hib.nf, "tot"], ["Crédito de CBS e IBS para o comprador do regime regular", A.hib.cbs + A.hib.ibs, "cr"]);
    nota = "No Simples tradicional a nota não destaca CBS e IBS para crédito pleno: o comprador do regime regular credita só o que corresponde ao DAS (LC 214/2025, art. 47, § 9º, II). O "+imp+" segue no DAS nas duas opções.";
  }
  el.innerHTML = `<h3>Nota fiscal desta venda, ${doc} <em>${o.ano}</em></h3>` + linhasNf(R)
    + `<p class="dica" style="margin-top:10px">${esc(nota)} Leiaute ilustrativo, com os valores de uma unidade; os campos e a ordem seguem a nota técnica vigente do documento fiscal.</p>`;
}
function definirModo(m){
  MODO = m === "compra" ? "compra" : "venda";
  document.body.classList.toggle("modo-compra", MODO === "compra");
  $$("#modo button").forEach(b=>b.setAttribute("aria-pressed", b.dataset.m === MODO));
  $('label[for="trat"]').textContent = MODO === "compra" ? "Tratamento de CBS e IBS do item comprado" : "Tratamento de CBS e IBS na venda";
  calcular();
}
function prepararCompra(){
  [$("#tit-compra").closest(".bloco"), $("#pv").closest(".campo"), $("#c-is"), $("#c-setor"), $("#c-simples"),
   $("#icms-venda").closest(".campo"), $("#inc-lucro").closest("label"), $("#inc-lucro").closest("label").nextElementSibling,
   $("#lc224").closest("label"), $("#lc224").closest("label").nextElementSibling, $("#p-hoje"), $("#p-forn"), $("#p-simples")]
    .forEach(el=>el && el.classList.add("so-venda"));
  escreverCot(cotPadrao(100, 18));
  $("#modo").addEventListener("click", e=>{ const b = e.target.closest("button"); if (b && b.dataset.m !== MODO) definirModo(b.dataset.m); });
  const cot = $("#cot");
  cot.addEventListener("input", calcular);
  cot.addEventListener("change", e=>{
    if (e.target.dataset.k === "reg"){ const tr = e.target.closest("tr"), sn = ehSN(e.target.value);
      tr.querySelector('[data-k=das]').disabled = !sn; tr.querySelector('[data-k=anexo]').disabled = !sn; }
    calcular();
  });
  cot.addEventListener("click", e=>{ if (e.target.closest("[data-rm]")){ e.target.closest("tr").remove(); NOTA_I = null; calcular(); } });
  $("#b-cot-add").addEventListener("click", ()=>{ const l = lerCot();
    l.push({nome:"", reg:"regular", preco:l.length ? l[l.length-1].preco : 100, icms:num("icms-compra"), das:9.403, anexo:"I"}); escreverCot(l); calcular(); });
  $("#b-cot-5").addEventListener("click", ()=>{ const p = lerCot()[0] || {preco:100, icms:18, das:9.403};
    escreverCot(cotPadrao(p.preco || 100, p.icms || (p.reg==="mei"||p.reg==="pf" ? 18 : p.icms), p.das)); calcular(); });
  $("#p-compra").addEventListener("click", e=>{
    if (e.target.closest("#b-cot-usar")){
      const o = opcoes(), L = lerCot().map(c=>Object.assign({}, c, creditoComprador(c, o))).filter(x=>x.preco > 0);
      if (!L.length) return;
      const best = L.reduce((m,x)=>x.custo < m.custo ? x : m);
      $("#pc-ano").value = best.preco; $("#forn").value = best.reg;
      if (!o.servico) $("#icms-compra").value = best.icms;
      if (ehSN(best.reg)) $("#aliqsn-forn").value = best.das;
      sincronizar(); definirModo("venda");
      avisar("Melhor cotação levada para a simulação de venda, como preço de compra no ano de referência.", "ok");
      return;
    }
    const tr = e.target.closest("tr[data-i]"); if (tr){ NOTA_I = +tr.dataset.i; calcular(); }
  });
}
/* ---------- busca de NCM ---------- */""")

s=sub1(s,"""function iniciar(){""","""function iniciar(){
  prepararCompra();""")
s=sub1(s,"""  /* --- comparador de fornecedores --- */""","""  desenharNotaVenda(o, A);
  /* --- comparador de fornecedores --- */""")
s=sub1(s,"""  desenharFicha();
  $("#dica-ano").textContent = ANO === 2026""","""  desenharFicha();
  if (MODO === "compra") calcCompra(o);
  $("#dica-ano").textContent = ANO === 2026""")
# salvar e abrir
s=sub1(s,"""baseFiscal:DB.meta.versao, consulta:$("#cq").value,""","""baseFiscal:DB.meta.versao, consulta:$("#cq").value, modo:MODO, cotacoes:lerCot(),""")
s=sub1(s,"""      if (o.consulta){ consultarLote(); } else { $("#cq-res").innerHTML = ""; }""","""      if (o.consulta){ consultarLote(); } else { $("#cq-res").innerHTML = ""; }
      if (Array.isArray(o.cotacoes) && o.cotacoes.length) escreverCot(o.cotacoes);
      MODO = o.modo === "compra" ? "compra" : "venda"; document.body.classList.toggle("modo-compra", MODO === "compra");
      $$("#modo button").forEach(b=>b.setAttribute("aria-pressed", b.dataset.m === MODO));""")
s=sub1(s,"""    if (el.id==="senha" || el.id==="ncm" || el.id==="cq" || el.id==="lcp-f") return;""","""    if (el.id==="senha" || el.id==="ncm" || el.id==="cq" || el.id==="lcp-f" || el.closest("#cot")) return;""")
