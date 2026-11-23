# ===== rodada 17: perguntas de enquadramento do ICMS de SC antes da alíquota (R17-01) =====
# Regras conferidas no texto da SEF/SC em 11/11/2026: Lei 10.297/1996, art. 19, III, d, e, n, e § 3º;
# RICMS/SC, Anexo 2, art. 1º, XXXVI; art. 11-A; art. 12-A; art. 12-B.
s=sub1(s,"""function garantirOpcaoTrat(r){""","""/* ---------- ICMS de SC: perguntas antes da alíquota ---------- */
const SC_BOV = ["0201","0202","02061","02062"];               // art. 12-B: carne bovina e bufalina e miudezas, frescas, resfriadas ou congeladas
const SC_CARNE_INTER = ["0201","0202","0203","0204","02061","02062","02063","02064","0207","020810","02101","021020"]; // art. 12-A
const SC_TEXTIL = () => DB.sc.textil || [];
function scHoje(){ return new Date().getFullYear(); }
function benSC(cod){ const hit = l => l.some(p=>cod.startsWith(p)); return (DB.sc.ben || []).find(b=>hit(b.pref) && !hit(b.excl)); }
function perguntasSC(cod){
  const S = DB.sc, hit = l => l.some(p=>cod.startsWith(p)), q = [];
  const b = benSC(cod);
  if (b && b.q) q.push({id:"ben", txt:b.q, ops:b.ops.map(o=>[o[0],o[1]])});
  const m = S.r12.find(x=>hit(x[0])), exato = m && (m[3] || hit(S.r12nc || []));
  const vale26 = scHoje() <= 2026;
  const c7 = vale26 ? S.c7.find(x=>hit(x[0])) : null;
  const ise = vale26 ? S.isento.find(x=>x[0].includes(cod)) : null;
  if (m && !exato) q.push({id:"desc", txt:"O produto corresponde à descrição da lei de SC: "+m[1]+"?", ops:[["sim","Sim"],["nao","Não"]]});
  if (c7) q.push({id:"c7", txt:"O produto é: "+c7[1]+"? (carga de 7% até 31/12/2026)", ops:[["sim","Sim"],["nao","Não"]], se:r=>!m || exato || r.desc==="sim"});
  q.push({id:"dest", txt:"Para quem é a venda?", ops:[["rev","Contribuinte de SC, para revenda ou industrialização"],["uso","Contribuinte de SC, para uso, consumo, ativo ou uso em serviço do ISS"],["final","Consumidor final ou não contribuinte"],["orgao","Órgão da administração direta do Estado de SC, fundação ou autarquia estadual"]]});
  if (hit(SC_BOV)) q.push({id:"orig", txt:"Como a carne entrou na sua empresa?", ops:[["fora","Comprada de outro estado"],["sc","Abatida ou comprada em SC"],["imp","Importação própria"]]});
  if ((c7 && cod.startsWith("1101")) || hit(SC_TEXTIL())) q.push({id:"ativ", txt:"Quem vende?", ops:[["ind","Sou o fabricante (estabelecimento industrial)"],["com","Comércio (atacado ou varejo)"]]});
  // pergunta só aparece se mudar o resultado
  // a pergunta só aparece se, em alguma combinação das demais respostas, mudar o resultado
  const combos = q.reduce((acc,y)=>acc.flatMap(c=>y.ops.map(o=>Object.assign({}, c, {[y.id]:o[0]}))), [{}]);
  const chave = r => { const z = resolverSC(cod, r); return z.carga+"|"+z.base+"|"+(z.notas||[]).length; };
  return q.filter(x=>combos.some(c=>new Set(x.ops.map(o=>chave(Object.assign({}, c, {[x.id]:o[0]})))).size > 1));
}
function resolverSC(cod, r){
  const S = DB.sc, hit = l => l.some(p=>cod.startsWith(p)), notas = [];
  if (r.dest === "orgao") return {aliq:0, carga:0, base:"RICMS/SC, Anexo 2, art. 1º, XI (isenção na venda a órgão da administração direta, fundação ou autarquia do Estado)", rot:"Venda a órgão do Estado de SC", notas:["Confira as condições do § 5º do art. 1º (entre elas, o desconto do imposto no preço e a indicação na nota)."]};
  const b = benSC(cod);
  if (b){
    const op = b.q ? b.ops.find(o=>o[0] === r.ben) : b.ops[0];
    if (op && op[2] !== null && (!op[4] || scHoje() <= op[4]) && (!op[5] || op[5].includes(r.dest)))
      return {aliq:op[2], carga:op[2], base:op[3], rot:op[1] === "Sim" ? (b.q.replace(/[?]$/,"")) : op[1], fim:op[4] || undefined, notas: op[2] === 0 ? ["Isenção: confira a exigência de estorno do crédito de ICMS da entrada."] : []};
  }
  const s25 = S.r25.find(x=>cod.startsWith(x[0]));
  if (s25) return {aliq:0.25, carga:0.25, base:"Lei 10.297/1996, art. 19, II, b, e Anexo I, Seção I", rot:"Produto supérfluo ("+s25[1]+")", notas};
  const m = S.r12.find(x=>hit(x[0])), exato = m && (m[3] || hit(S.r12nc || []));
  const vale26 = scHoje() <= 2026;
  const naLista = m && (exato || r.desc === "sim");
  if (vale26 && r.dest === "final"){
    const ise = S.isento.find(x=>x[0].includes(cod));
    if (ise && naLista !== false) return {aliq:0, carga:0, base:ise[2], rot:"Isento: "+ise[1], fim:2026, notas:["A isenção exige o estorno do crédito de ICMS da entrada."]};
  }
  if (naLista){
    let carga = 0.12, base = "Lei 10.297/1996, art. 19, III, "+(/Seção III/.test(m[2]) ? "e" : "d")+", e Anexo I, "+m[2], rot = m[1], fim;
    const c7 = vale26 ? S.c7.find(x=>hit(x[0])) : null;
    if (c7 && r.c7 === "sim" && !(cod.startsWith("1101") && r.ativ === "ind")){
      carga = 0.07; base = "RICMS/SC, Anexo 2, art. 11-A (base reduzida em 41,667%)"; rot = "Cesta básica: "+c7[1]; fim = 2026;
    }
    if (hit(SC_BOV) && r.orig === "fora" && (r.dest === "rev" || r.dest === "uso")){
      carga = 0.07; base = "RICMS/SC, Anexo 2, art. 12-B (base reduzida em 41,66% na venda interna a contribuinte inscrito; crédito integral mantido)"; rot = "Carne bovina ou bufalina recebida de outro estado";
    }
    if (hit(SC_BOV) && r.orig === "imp") notas.push("Importação própria: o art. 12-B alcança só a carne recebida de outro estado. Se a empresa tem TTD de importação, a carga sai do regime especial, que a ferramenta não simula: informe a alíquota à mão.");
    return {aliq:0.12, carga, base, rot, fim, notas};
  }
  // regra geral: 17% ou 12% para contribuinte (alínea n e § 3º)
  if (r.dest === "rev"){
    if (hit(SC_TEXTIL()) && r.ativ === "ind") return {aliq:0.17, carga:0.17, base:"Lei 10.297/1996, art. 19, I, e § 3º, III (saída do próprio fabricante de têxteis, vestuário e couro)", rot:"Fabricante de têxtil, vestuário ou couro", notas};
    return {aliq:0.12, carga:0.12, base:"Lei 10.297/1996, art. 19, III, n", rot:"Contribuinte de SC, para revenda ou industrialização", notas:["Se o comprador usar a mercadoria em uso, consumo, ativo ou em serviço do ISS, ele responde pela diferença até 17% (art. 19, § 4º)."]};
  }
  return {aliq:0.17, carga:0.17, base:"Lei 10.297/1996, art. 19, I"+(r.dest === "uso" ? ", e § 3º, II" : ""), rot: r.dest === "uso" ? "Contribuinte, para uso, consumo, ativo ou serviço do ISS" : "Consumidor final ou não contribuinte", notas};
}
// perguntas que ainda importam, dadas as respostas já marcadas (ex.: se o produto está na lista, o destinatário deixa de importar)
function visiveisSC(f){
  const q = f.scQ || [], r0 = f.scResp || {};
  const chave = r => { const z = resolverSC(f.scCod, r); return z.carga+"|"+z.base+"|"+(z.notas||[]).length; };
  return q.filter(x=>{
    const outras = q.filter(y=>y.id !== x.id);
    const combos = outras.reduce((acc,y)=>acc.flatMap(c=>(r0[y.id] ? [r0[y.id]] : y.ops.map(o=>o[0])).map(v=>Object.assign({}, c, {[y.id]:v}))), [{}]);
    return combos.some(c=>new Set(x.ops.map(o=>chave(Object.assign({}, c, {[x.id]:o[0]})))).size > 1);
  });
}
function respostaSCCompleta(f){ return visiveisSC(f).every(q=>f.scResp && f.scResp[q.id]); }
function aplicarSC(){
  if (!FICHA || !FICHA.scQ) return;
  if (!respostaSCCompleta(FICHA)) return;
  const z = resolverSC(FICHA.cod || FICHA.codigo || $("#ncm").value.replace(/\\D/g,""), FICHA.scResp);
  FICHA.scRes = z; $("#icms-venda").value = +(z.carga*100).toFixed(2);
}
function garantirOpcaoTrat(r){""")
s=sub1(s,"""  FICHA.sc = (TIPO === "produto" && FICHA.cor !== "cinza") ? icmsSC(cod) : null;
""","""  FICHA.sc = (TIPO === "produto" && FICHA.cor !== "cinza") ? icmsSC(cod) : null;
  FICHA.scCod = cod; FICHA.scResp = {}; FICHA.scRes = null;
  FICHA.scQ = FICHA.sc ? perguntasSC(cod) : null;
  if (FICHA.scQ && !FICHA.scQ.length){ FICHA.scRes = resolverSC(cod, {}); }
""")
# o preenchimento automático da rodada 16 passa a valer só quando não há pergunta
s=sub1(s,"""  if (FICHA.sc && FICHA.sc.fixa){ FICHA.scSel = 0; $("#icms-venda").value = +(FICHA.sc.ops[0].aliq*100).toFixed(2); }""",
 """  if (FICHA.scRes && MODO !== "compra"){ $("#icms-venda").value = +(FICHA.scRes.carga*100).toFixed(2); }
  else if (FICHA.sc && FICHA.sc.fixa && MODO === "compra"){ FICHA.scSel = 0; $("#icms-venda").value = +(FICHA.sc.ops[0].aliq*100).toFixed(2); }""")
s=s.replace("const z = resolverSC(FICHA.cod || FICHA.codigo || $(\"#ncm\").value.replace(/\\\\D/g,\"\"), FICHA.scResp);","const z = resolverSC(FICHA.scCod, FICHA.scResp);")
# desenho: na venda, perguntas e resultado; na compra, a lista anterior
s=sub1(s,"""  if (f.sc){
    const atual = num("icms-venda")/100;
    h += `<fieldset class="opc" style="margin-top:10px"><legend>ICMS em Santa Catarina, venda interna</legend>`""","""  if (f.sc && f.scQ && MODO !== "compra"){
    h += `<fieldset class="opc" style="margin-top:10px"><legend>ICMS em Santa Catarina, venda interna</legend>`;
    const vis = visiveisSC(f);
    if (vis.length) h += `<p class="dica" style="margin:4px 0 8px">Responda antes de usar a alíquota: o ICMS deste produto muda conforme a operação.</p>`
      + vis.map(q=>`<div class="scq"><b>${esc(q.txt)}</b>` + q.ops.map(o=>`<label class="${f.scResp[q.id]===o[0]?"sel":""}"><input type="radio" name="scq-${q.id}" value="${o[0]}" ${f.scResp[q.id]===o[0]?"checked":""}><span>${esc(o[1])}</span></label>`).join("") + `</div>`).join("");
    const z = f.scRes;
    if (z) h += `<div class="f-al" style="background:#E8F1EA;border-color:#2E7D4F"><b>ICMS da venda: ${z.carga === 0 ? "isento" : PCT(z.carga)}</b>${z.carga !== z.aliq && z.carga ? " (alíquota de "+PCT(z.aliq)+" com base reduzida)" : ""} · ${esc(z.rot)}<br><small>${esc(z.base)}${z.fim ? " · vale até 31/12/"+z.fim : ""}</small></div>`
      + (z.notas||[]).map(n=>`<div class="f-al">${esc(n)}</div>`).join("");
    else h += `<div class="f-al">Responda as perguntas para a alíquota entrar no campo de ICMS da venda.</div>`;
    h += `</fieldset>` + f.sc.notas.map(n=>`<div class="f-al">${esc(n)}</div>`).join("")
      + `<p class="dica">Não simulado: TTD, crédito presumido e substituição tributária. Venda para outro estado: use o campo de destino. ${esc(DB.sc.meta.aviso)}</p>`;
  } else if (f.sc){
    const atual = num("icms-venda")/100;
    h += `<fieldset class="opc" style="margin-top:10px"><legend>ICMS em Santa Catarina, venda interna</legend>`""")
s=sub1(s,"""    if (e.target.name === "scopt" && FICHA && FICHA.sc){""","""    if (e.target.name && e.target.name.startsWith("scq-") && FICHA && FICHA.scQ){
      FICHA.scResp[e.target.name.slice(4)] = e.target.value; FICHA.scRes = null; aplicarSC(); desenharFicha(); calcular(); }
    if (e.target.name === "scopt" && FICHA && FICHA.sc){""")
# venda para outro estado: art. 12-A (carnes), carga de 7% em vez de 12%
s=sub1(s,"""  const inter = $("#importado").checked ? 0.04 : (UF7.includes(uf) ? 0.07 : 0.12), d = UFS[uf], carga = (d[0] + d[1])/100;""",
 """  const carne12A = FICHA && FICHA.scCod && SC_CARNE_INTER.some(p=>FICHA.scCod.startsWith(p));
  const inter = $("#importado").checked ? 0.04 : (UF7.includes(uf) || carne12A ? 0.07 : 0.12), d = UFS[uf], carga = (d[0] + d[1])/100;""")
s=sub1(s,"""  el.textContent = "Alíquota interestadual de " + PCT(v.icmsInter) + ($("#importado").checked ? " (Resolução do Senado 13/2012)" : " (Resolução do Senado 22/1989)") + ". \"""",
 """  const c12A = FICHA && FICHA.scCod && SC_CARNE_INTER.some(p=>FICHA.scCod.startsWith(p)) && !$("#importado").checked && !UF7.includes(v.ufDest);
  el.textContent = "Alíquota interestadual de " + PCT(v.icmsInter) + ($("#importado").checked ? " (Resolução do Senado 13/2012)" : (c12A ? " (12% com base reduzida em 41,66%: RICMS/SC, Anexo 2, art. 12-A, carnes)" : " (Resolução do Senado 22/1989)")) + ". \"""")
s=sub1(s,"""</style>""","""div.scq{margin:6px 0 8px} div.scq>b{display:block;font-size:13px;margin-bottom:4px}
</style>""")
