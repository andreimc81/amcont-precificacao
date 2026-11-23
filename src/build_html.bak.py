import sys; sys.path.insert(0,'src')
# Gera amcont-produto.html com o banco fiscal embutido e a busca automatica.
import json, re, sys
src=open('produto_orig.html',encoding='utf-8').read()
db=json.load(open('db.json',encoding='utf-8'))
aux=json.load(open('ncm_aux.json',encoding='utf-8'))
def sub1(s,old,new,n=1):
    c=s.count(old)
    assert c==n, (c, old[:70])
    return s.replace(old,new)

# ---- lista de NCM vigente (tabela oficial de 07/10/2026) com descricao ----
cam=dict(json.loads(re.search(r'id="amcont-ncm"[^>]*>(.*?)</script>',src,re.S).group(1))['itens'])
itens=[]
for c in aux['vig']:
    d=cam.get(c) or (aux['desc'].get(c,'').split(' > ')[-1]) or aux['desc'].get('~'+c,'') or ''
    itens.append([c,re.sub(r'<[^>]+>','',d)])
ncmjson=json.dumps({'fonte':'Tabela NCM oficial do Portal Único Siscomex','vigencia':'Vigente em 07/10/2026','itens':itens},ensure_ascii=False,separators=(',',':'))
s=re.sub(r'(<script type="application/json" id="amcont-ncm">).*?(</script>)',lambda m:m.group(1)+ncmjson.replace('</','<\\/')+m.group(2),src,count=1,flags=re.S)
dbjson=json.dumps(db,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
s=sub1(s,'<script>\n"use strict";','<script type="application/json" id="amcont-fiscal">'+dbjson+'</script>\n<script>\n"use strict";')

# ---- parametros ----
s=sub1(s,'"cbs": 0.092','"cbs": 0.112',2); s=sub1(s,'"cbs": 0.093','"cbs": 0.113',5)
s=sub1(s,'"versaoDados": "2026.1"','"versaoDados": "2026.2"'); s=sub1(s,'"atualizadoEm": "2026-08-13"','"atualizadoEm": "2026-11-10"')
s=sub1(s,'"fonte": "EC 132/2023; LC 214/2025; LC 227/2026; Lei 9.249/1995; Lei 14.592/2023"',
 '"fonte": "EC 132/2023; LC 214/2025; LC 227/2026; LC 235/2026; MP 1.399/2026; Acórdão TCU 2933/2026; Lei 9.249/1995; Lei 14.592/2023"')
s=sub1(s,'"avisoLegal": "As aliquotas de CBS e IBS sao estimativas divulgadas pelo governo e nao texto legal. Confira contra a norma vigente antes de usar com cliente."',
 '"avisoLegal": "CBS provisória: 11,3% calculados pelo TCU (11,2% em 2027 e 2028), aguardando resolução do Senado. IBS de referência ainda é estimativa. Confira contra a norma vigente antes de usar com cliente."')
s=sub1(s,'''"redSaida": 0.6,
   "dica": "Transporte de passageiros tem presunção de 16% para IRPJ e 12% para CSLL."''','''"redSaida": 0.4,
   "dica": "Transporte intermunicipal e interestadual de passageiros: redução de 40% (LC 214, art. 286). Presunção de 16% para IRPJ e 12% para CSLL. O transporte urbano e metropolitano é isento e não deve ser simulado aqui."''')

# ---- textos ----
s=sub1(s,'<title>Amcont · Preço por Produto na Reforma Tributária</title>','<title>Amcont · Preço por Produto ou Serviço na Reforma Tributária</title>')
s=sub1(s,'<h1>Preço por produto na reforma tributária</h1>','<h1>Preço por produto ou serviço na reforma tributária</h1>')
s=sub1(s,'<span class="sub">Preço por produto na reforma tributária</span>','<span class="sub">Preço por produto ou serviço na reforma tributária</span>')

css='''
[hidden]{display:none!important}
/* tipo do item e ficha fiscal */
.seg{display:flex;gap:4px;margin-bottom:13px}
.seg button{flex:1;padding:8px 4px;border:1px solid var(--linha);border-radius:var(--r);background:var(--via-2);
  cursor:pointer;font:500 13px "IBM Plex Sans";color:#4E6165}
.seg button[aria-pressed=true]{background:var(--petroleo);color:#fff;border-color:var(--petroleo)}
#ficha{margin:2px 0 14px;background:var(--nota);border:1px solid var(--linha);border-left:4px solid var(--petroleo-3);
  border-radius:var(--r);padding:13px 14px;font-size:12.5px;line-height:1.45}
#ficha:empty{display:none}
#ficha.verde{border-left-color:var(--saldo)} #ficha.amarelo{border-left-color:#B98A14}
#ficha.vermelho{border-left-color:var(--carimbo)} #ficha.cinza{border-left-color:#7C8A8D}
.f-top{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap;margin-bottom:6px}
.selo{font:600 10px "IBM Plex Mono";letter-spacing:.14em;text-transform:uppercase;padding:2px 7px;border-radius:2px;color:#fff;background:#7C8A8D}
.verde .selo{background:var(--saldo)} .amarelo .selo{background:#B98A14} .vermelho .selo{background:var(--carimbo)}
.f-cod{font:600 14px "IBM Plex Mono";color:var(--petroleo)}
.f-desc{color:#3C4E52;margin-bottom:9px}
.f-msg{margin-bottom:9px;font-weight:500}
.opc{border:0;margin:0 0 9px}
.opc legend{font:600 10px "IBM Plex Mono";letter-spacing:.14em;text-transform:uppercase;color:var(--petroleo-2);margin-bottom:5px}
.opc label{display:flex;gap:8px;align-items:flex-start;font-weight:400;font-size:12.5px;padding:6px 8px;margin:0 0 4px;
  border:1px solid var(--linha);border-radius:var(--r);cursor:pointer;background:var(--via-2)}
.opc label.sel{border-color:var(--petroleo);background:#E7F0F1}
.opc input{width:auto;margin-top:3px}
.opc b{font-family:"IBM Plex Mono";font-weight:600}
.opc small{display:block;color:#5C6E72;font-size:11.5px}
.f-dl{display:grid;grid-template-columns:auto 1fr;gap:3px 10px;margin:0}
.f-dl dt{font:600 10px "IBM Plex Mono";letter-spacing:.1em;text-transform:uppercase;color:var(--petroleo-2);padding-top:2px;white-space:nowrap}
.f-dl dd{margin:0;overflow-wrap:anywhere}
.f-al{margin-top:8px;padding:7px 9px;background:#FBF3DC;border-radius:var(--r);color:#6B5210}
.f-al.is{background:#F6E3DC;color:var(--carimbo)}
#ficha details{margin-top:8px} #ficha summary{cursor:pointer;color:var(--petroleo);font-weight:500}
#ficha details ul{padding-left:16px;margin-top:5px;color:#4E6165}
.rod details{margin-top:14px;font-size:12.5px;color:#4E6165;max-width:100ch}
.rod summary{cursor:pointer;color:var(--petroleo);font-weight:600}
.rod table{border-collapse:collapse;margin-top:8px;width:100%}
.rod td,.rod th{border-bottom:1px solid var(--linha);padding:5px 8px 5px 0;text-align:left;vertical-align:top;font-size:12px}
.rod th{font:600 10px "IBM Plex Mono";letter-spacing:.1em;text-transform:uppercase;color:var(--petroleo-2)}
@media print{#gate,.barra,.btn{display:none!important}body{background:#fff}}'''
s=sub1(s,'\n@media print{#gate,.barra,.btn{display:none!important}body{background:#fff}}',css)

s=sub1(s,'''        <div class="bloco-tit">O produto</div>
        <div class="campo">
          <label for="ncm">NCM, por código ou descrição</label>
          <input id="ncm" type="text" autocomplete="off" placeholder="ex.: 1806 ou chocolate">
          <div id="ncm-lista"></div>
          <div id="ncm-desc" data-cod=""></div>
        </div>
        <div class="campo">
          <label for="is">Imposto Seletivo sobre este produto (%)</label>
          <input id="is" type="number" step="0.01" value="0">
          <p class="dica">Incide sobre bens prejudiciais à saúde ou ao meio ambiente e
             <b>integra a base da CBS e do IBS</b>. As alíquotas ainda não foram definidas em lei.</p>
        </div>
        <div class="campo">
          <label for="trat">Tratamento de CBS e IBS na venda</label>
          <select id="trat">
            <option value="0">Alíquota integral</option>
            <option value="0.3">Redução de 30%</option>
            <option value="0.6">Redução de 60%</option>
            <option value="1">Alíquota zero ou isento</option>
          </select>
          <p class="dica" id="dica-trat">Decorre das listas anexas à LC 214/2025, não do NCM isoladamente. Confirme com a Amcont.</p>
        </div>''','''        <div class="bloco-tit" id="tit-item">O produto ou serviço</div>
        <div class="seg" id="tipo" role="group" aria-label="Tipo do item">
          <button type="button" data-t="produto" aria-pressed="true">Produto, por NCM</button>
          <button type="button" data-t="servico" aria-pressed="false">Serviço, por NBS ou LC 116</button>
        </div>
        <div class="campo">
          <label for="ncm" id="lb-busca">NCM, por código ou descrição</label>
          <input id="ncm" type="text" autocomplete="off" placeholder="ex.: 1806 ou chocolate">
          <div id="ncm-lista"></div>
          <div id="ncm-desc" data-cod=""></div>
        </div>
        <div id="ficha" aria-live="polite"></div>
        <div class="campo">
          <label for="trat">Tratamento de CBS e IBS na venda</label>
          <select id="trat">
            <option value="0">Alíquota integral</option>
            <option value="0.3">Redução de 30%</option>
            <option value="0.4">Redução de 40%</option>
            <option value="0.5">Redução de 50%</option>
            <option value="0.6">Redução de 60%</option>
            <option value="0.7">Redução de 70%</option>
            <option value="0.8">Redução de 80%</option>
            <option value="1">Alíquota zero ou isento</option>
          </select>
          <p class="dica" id="dica-trat">Preenchido pela busca. Você pode ajustar manualmente, e a ficha avisa quando o valor difere da base.</p>
        </div>
        <div class="campo" id="c-is">
          <label for="is">Imposto Seletivo sobre este produto (%)</label>
          <input id="is" type="number" step="0.01" value="0">
          <p class="dica">Incide sobre bens prejudiciais à saúde ou ao meio ambiente e
             <b>integra a base do ICMS, da CBS e do IBS</b>. Alíquotas de 2027 pela MP 1.399/2026,
             com cobrança a partir de fevereiro de 2027 e sujeitas à conversão em lei.</p>
        </div>''')
s=sub1(s,'<div class="bloco-tit">A compra deste produto, hoje</div>','<div class="bloco-tit" id="tit-compra">A compra deste produto, hoje</div>')
s=sub1(s,'<label for="pc">Preço de compra por unidade, valor total da nota</label>','<label for="pc" id="lb-pc">Preço de compra por unidade, valor total da nota</label>')
s=sub1(s,'''          <div class="campo">
            <label for="icms-compra">ICMS na compra (%)</label>''','''          <div class="campo" id="c-icms-compra">
            <label for="icms-compra">ICMS na compra (%)</label>''')
s=sub1(s,'<div class="bloco-tit">A venda deste produto, hoje</div>','<div class="bloco-tit" id="tit-venda">A venda deste produto, hoje</div>')
s=sub1(s,'''      <li>A base de NCM é a nomenclatura oficial vigente e serve para identificar o produto. Ela não define sozinha o tratamento de CBS e IBS, que decorre das listas anexas à LC 214/2025.</li>
      <li>As alíquotas de CBS e IBS são estimativas divulgadas pelo governo e podem mudar até a vigência.</li>''','''      <li>A busca traz a regra que a LC 214/2025 atribui ao código. O código não decide sozinho: o benefício depende da condição, de quem compra, da destinação e da operação. Em caso de selo "conferir" ou "escolher", confirme com a Amcont antes de formar o preço.</li>
      <li>A CBS é provisória: 11,3% calculados pelo TCU (11,2% em 2027 e 2028), aguardando resolução do Senado. O IBS de referência ainda é estimativa.</li>
      <li>O Imposto Seletivo usa as alíquotas de 2027 da MP 1.399/2026, que ainda depende de conversão em lei.</li>''')
s=sub1(s,'''    </ol>
  </div>
</main>''','''    </ol>
    <details id="regras"><summary>Casos em que o código não decide: 30 regras sem lista de NCM ou NBS</summary><div id="regras-corpo"></div></details>
    <p class="dica" id="fontes-db" style="margin-top:12px;max-width:100ch"></p>
  </div>
</main>''')

# ---- JS ----
s=sub1(s,'''const MAPA = [''','''const MAPA_ANTIGO = [''')
s=sub1(s,'''const acharTrat = n => MAPA.find(m => n.startsWith(m.ncm.slice(0,8)));
const NCM  = JSON.parse(document.getElementById("amcont-ncm").textContent);''','''const NCM  = JSON.parse(document.getElementById("amcont-ncm").textContent);
const DB   = JSON.parse(document.getElementById("amcont-fiscal").textContent);
const St   = i => (i === undefined || i === null || i < 0) ? "" : DB.S[i];
const NCMDESC = new Map(NCM.itens);
let TIPO = "produto", FICHA = null;''')
# remove a semente antiga inteira
s=re.sub(r'/\* Mapa NCM -> tratamento\. Semente.*?\*/\nconst MAPA_ANTIGO = \[.*?\];\n','',s,count=1,flags=re.S)
assert 'MAPA_ANTIGO' not in s

s=sub1(s,'''  const icms = o.pv * o.icmsVenda;
  const pis  = (o.pv - icms) * o.pis, cof = (o.pv - icms) * o.cofins;''','''  const icms = o.pv * o.icmsVenda;
  // No ISS a base do PIS e da COFINS e a receita cheia; no ICMS, exclui o imposto.
  const bpc = o.servico ? o.pv : o.pv - icms;
  const pis  = bpc * o.pis, cof = bpc * o.cofins;''')
s=sub1(s,'''          det:[["ICMS na venda", icms], ["PIS", pis], ["COFINS", cof],''','''          det:[[(o.servico?"ISS":"ICMS")+" na venda", icms], ["PIS", pis], [fab ? "PIS e COFINS, alíquota concentrada" : "COFINS", cof],''')
s=sub1(s,'''    ano:ANO, regime:reg, trat:parseFloat($("#trat").value),
    icmsVenda:num("icms-venda")/100, icmsCompra:num("icms-compra")/100,''','''    ano:ANO, regime:reg, trat:parseFloat($("#trat").value), servico:TIPO==="servico",
    icmsVenda:num("icms-venda")/100, icmsCompra:TIPO==="servico" ? 0 : num("icms-compra")/100,''')
s=sub1(s,'''    is: ANO >= 2027 ? num("is")/100 : 0,''','''    is: (ANO >= 2027 && TIPO === "produto") ? num("is")/100 : 0,''')

busca_js=r'''/* ---------- busca de NCM ---------- */
function buscarNcm(q){
  q = q.trim().toLowerCase();
  if (q.length < 3) return [];
  const so = q.replace(/\D/g,"");
  const out = [];
  for (const [cod, desc] of NCM.itens){
    if ((so.length >= 3 && cod.startsWith(so)) || desc.toLowerCase().includes(q)){
      out.push([cod, desc]); if (out.length >= 40) break;
    }
  }
  return out;
}
function fmtNcm(c){ return c.slice(0,4)+"."+c.slice(4,6)+"."+c.slice(6); }
function fmtNbs(c){ return c[0]+"."+c.slice(1,5)+"."+c.slice(5,7)+"."+c.slice(7); }
const semAcento = t => t.normalize("NFD").replace(/[̀-ͯ]/g,"").toLowerCase();
const esc = t => String(t==null?"":t).replace(/[&<>"]/g, m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[m]));
const pctRed = r => r===1 ? "Alíquota zero" : (r>0 ? "Redução de "+Math.round(r*100)+"%" : "Alíquota integral");

/* ---------- indice de servicos: NBS x item da LC 116 ---------- */
const NBSIDX = new Map();   // nbs -> {desc, itens:[{i,d,op,ccl}]}
(function(){
  for (const it of DB.lc){
    for (const [cod, ccl] of it.n){
      if (!NBSIDX.has(cod)) NBSIDX.set(cod, {desc:DB.nbsDesc[cod]||"", itens:[]});
      NBSIDX.get(cod).itens.push({i:it.i, d:it.d, op:it.op, ccl:ccl.concat(it.cx||[])});
    }
  }
  for (const cod of Object.keys(DB.nbsDesc))
    if (!NBSIDX.has(cod)) NBSIDX.set(cod, {desc:DB.nbsDesc[cod]||"", itens:[]});
})();
function buscarNbs(q){
  const t = semAcento(q.trim()); if (t.length < 3) return [];
  const so = t.replace(/\D/g,""), out = [], visto = new Set();
  const add = (cod, extra)=>{ if (visto.has(cod) || out.length >= 40) return;
    visto.add(cod); out.push([cod, (NBSIDX.get(cod).desc||"") + (extra ? "  ·  LC 116 "+extra : "")]); };
  // por item da LC 116 (codigo ou descricao)
  const itemQ = /^\d{1,2}[.,]\d{1,2}/.test(t) ? t.replace(",",".").split(".").map(x=>x.replace(/\D/g,"").padStart(2,"0")).slice(0,2).join(".") : null;
  for (const it of DB.lc){
    if ((itemQ && it.i.startsWith(itemQ)) || (!itemQ && so.length < 3 && semAcento(it.d).includes(t)))
      for (const [cod] of it.n) add(cod, it.i);
  }
  for (const [cod, v] of NBSIDX){
    if ((so.length >= 3 && cod.startsWith(so)) || (so.length < 3 && semAcento(v.desc).includes(t)))
      add(cod, v.itens.length ? v.itens[0].i : "");
  }
  return out;
}

/* ---------- classificacao fiscal pela base ---------- */
function prefixo(mapa, cod){
  for (let n = cod.length; n >= 2; n--){ const k = cod.slice(0,n); if (mapa[k]) return [k, mapa[k]]; }
  return null;
}
function impostoSeletivo(cod){
  let best = null;
  for (const r of DB.is) if (cod.startsWith(r[0]) && (!best || r[0].length > best[0].length)) best = r;
  return best;
}
const INTEGRAL = {rot:"Sem benefício: tributação integral", red:0, cst:"000", ccl:"000001", base:"", cond:""};
function classificarNcm(cod){
  const e = DB.ncm[cod], vigente = NCMDESC.has(cod);
  const f = {tipo:"produto", cod, fmt:fmtNcm(cod), desc:NCMDESC.get(cod)||"", opcoes:[], avisos:[], extra:[]};
  if (e){
    if (e.e === "x"){
      f.cor = "vermelho"; f.selo = "Escolher";
      f.msg = "A lei dá mais de uma classificação para este NCM, com percentuais diferentes. Escolha a que corresponde ao produto e à destinação reais.";
      e.o.forEach((o,i)=>f.opcoes.push({rot:"Opção "+"ABC"[i]+": "+(o[0]||"")+(o[1]?", item "+o[1]:""), red:o[2]||0,
        cst:o[3], ccl:o[4], base:St(o[5]), cond:St(o[6]) || St(o[7])}));
      f.sel = f.opcoes.reduce((m,o,i)=> o.red < f.opcoes[m].red ? i : m, 0);
      f.avisos.push("Enquanto você não escolher, a simulação usa a opção de menor redução, que é a mais conservadora para o preço.");
    } else {
      const r = e.r || 0;
      f.cor = e.e === "i" ? "verde" : "amarelo"; f.selo = e.e === "i" ? "Integral" : "Conferir";
      f.opcoes.push({rot:(e.ax||"")+(e.it?", item "+e.it:""), red:r, cst:e.cst, ccl:e.ccl, base:St(e.b), cond:St(e.c)});
      if (r > 0) f.opcoes.push(INTEGRAL);
      f.sel = 0;
      f.msg = St(e.m) || (r > 0 ? "Há benefício previsto na lei, condicionado ao que está descrito abaixo. Confirme antes de formar o preço."
                                : "Sem benefício de CBS e IBS nos anexos da lei.");
    }
    if (e.q !== undefined) f.extra.push(["O que confirmar", St(e.q)]);
    if (e.a !== undefined) f.extra.push(["Alternativa", St(e.a)]);
    if (e.s !== undefined) f.extra.push(["Situação do código", St(e.s)]);
    f.tipos = e.t;
    if (cod.startsWith("30")){
      f.avisos.push("Capítulo 30: o resultado acima vem dos anexos de dispositivos, insumos agropecuários e uso veterinário e não vale para medicamento de uso humano, que não tem lista de NCM na lei. Para medicamento humano, use uma das duas últimas opções.");
      f.opcoes.push({rot:"Medicamento humano registrado na Anvisa ou manipulado", red:0.6, cst:"200", ccl:"200032", base:"LC 214/2025, art. 133", cond:"Exige registro na Anvisa ou farmácia de manipulação; a lista do art. 146 tem regra própria."});
      f.opcoes.push({rot:"Medicamento humano da lista do art. 146", red:1, cst:"200", ccl:"200009", base:"LC 214/2025, art. 146", cond:"Somente os medicamentos da lista publicada por ato conjunto a cada 120 dias."});
    }
  } else if (vigente){
    f.cor = "verde"; f.selo = "Integral";
    f.msg = "Este NCM não consta nos anexos de benefício da LC 214/2025: tributação integral de CBS e IBS (CST 000, cClassTrib 000001), salvo regra por operação, adquirente ou regime.";
    f.opcoes.push(Object.assign({}, INTEGRAL, {rot:"Fora dos anexos: tributação integral"})); f.sel = 0;
    for (const d of DB.dicas){
      if (!d[0].some(p=>cod.startsWith(p))) continue;
      f.cor = "amarelo"; f.selo = "Conferir"; f.avisos.push(d[2]);
      if (d[1] === 1){
        f.opcoes.push({rot:"Medicamento registrado na Anvisa ou manipulado", red:0.6, cst:"200", ccl:"200032", base:"LC 214/2025, art. 133", cond:"Exige registro na Anvisa ou farmácia de manipulação; a lista do art. 146 tem regra própria."});
        f.opcoes.push({rot:"Medicamento da lista do art. 146", red:1, cst:"200", ccl:"200009", base:"LC 214/2025, art. 146", cond:"Somente os medicamentos da lista publicada por ato conjunto a cada 120 dias."});
      }
      if (d[1] === 6)
        f.opcoes.push({rot:"Produto in natura", red:0.6, cst:"200", ccl:"200036", base:"LC 214/2025, art. 137", cond:"Produto agropecuário, aquícola, pesqueiro, florestal ou extrativista vegetal sem industrialização."});
    }
    f.tipos = "T1;T12";
  } else {
    const p = prefixo(DB.pref, cod);
    if (p){
      const v = p[1];
      f.cor = "amarelo"; f.selo = "Conferir";
      f.msg = "NCM não localizado na tabela oficial de 07/10/2026. O código cai sob o prefixo "+p[0]+" da lei, que soma os itens e não desconta ressalvas. Confirme o código.";
      String(v.rt||"").split("|").map(x=>parseFloat(x)/100).filter(x=>!isNaN(x)).forEach(r=>
        f.opcoes.push({rot:(v.ax||"")+(v.it?", item "+v.it:""), red:r, cst:v.cst, ccl:v.ccl, base:St(v.b), cond:St(v.c)}));
      f.opcoes.push(INTEGRAL);
      f.sel = f.opcoes.length - 1; f.tipos = v.t;
      f.avisos.push("Como o código não foi confirmado, a simulação parte da tributação integral. Marque o benefício somente depois de conferir o NCM.");
    } else {
      f.cor = "cinza"; f.selo = "Não localizado";
      f.msg = "NCM não localizado na tabela oficial de 07/10/2026. Pode ser código novo, extinto ou erro de digitação. A ferramenta não decide sobre ele.";
      f.opcoes.push(INTEGRAL); f.sel = 0; f.tipos = "NL";
    }
  }
  // IS so para NCM listado no Anexo XVII da base; aeronaves (88.02, exceto 8802.60.00) entram pela MP.
  const noXVII = !!(e && /XVII/.test(e.ax||"")), aeronave = cod.startsWith("8802") && cod !== "88026000" && vigente;
  const is = (noXVII || aeronave) ? impostoSeletivo(cod) : null;
  if (aeronave && !noXVII) f.avisos.push("Aeronave: a MP 1.399/2026 traz alíquota de Imposto Seletivo para a posição 88.02, mas o código não está marcado no Anexo XVII desta base. Confira o enquadramento antes de usar.");
  if (is || noXVII){
    f.is = is ? is[1] : null;
    f.isNota = is ? is[2] : "Bem do Anexo XVII, sujeito ao Imposto Seletivo. Informe a alíquota.";
  }
  return f;
}
const REG_ESPECIFICO = /^(20004[6-9]|20005[01]|01)/;
function classificarNbs(cod){
  const e = DB.nbs[cod], idx = NBSIDX.get(cod);
  const f = {tipo:"servico", cod, fmt:fmtNbs(cod), desc:(idx && idx.desc) || DB.nbsDesc[cod] || "", opcoes:[], avisos:[], extra:[]};
  const tem = c => f.opcoes.some(o=>o.ccl === c);
  if (e && e.ccl && e.ccl !== "000001"){
    f.opcoes.push({rot:(e.ax||"")+(e.it?", item "+e.it:""), red:e.r||0, cst:e.cst, ccl:e.ccl, base:St(e.b), cond:St(e.c)});
    if (e.q !== undefined) f.extra.push(["O que confirmar", St(e.q)]);
    if (e.a !== undefined) f.extra.push(["Alternativa", St(e.a)]);
  } else if (!e){
    const p = prefixo(DB.prefNbs, cod);
    if (p){ const v = p[1], r = parseFloat(v.rt)/100;
      if (!isNaN(r)) f.opcoes.push({rot:(v.ax||"")+" (pelo prefixo "+p[0]+" da lei)", red:r, cst:v.cst, ccl:v.ccl, base:St(v.b), cond:St(v.c)});
      f.avisos.push("O código não consta na lista de NBS da lei, mas cai sob um prefixo com benefício. Confirme a descrição do serviço contra o item do anexo.");
    }
  }
  const ops = [], itens = [];
  if (idx) for (const it of idx.itens){
    itens.push(it.i+" "+it.d);
    for (const o of it.op) if (!ops.some(x=>x[0]===o[0])) ops.push(o);
    for (const c of it.ccl){
      if (tem(c)) continue;
      const k = DB.ccl[c] || [c.slice(0,3), "cClassTrib "+c, null, ""];
      if (c === "000001") f.opcoes.push(Object.assign({}, INTEGRAL, {rot:"Tributação integral"}));
      else f.opcoes.push({rot:k[1], red:k[2]||0, cst:k[0], ccl:c, base:k[3] ? "LC 214/2025, "+k[3] : "", cond:"",
                          semRed:k[2] === null});
    }
  }
  if (!tem("000001")) f.opcoes.push(INTEGRAL);
  const beneficio = f.opcoes.some(o=>o.red > 0);
  if (!idx && !e){
    f.cor = "cinza"; f.selo = "Não localizado";
    f.msg = "NBS fora desta base, que cobre os códigos dos anexos da lei e os correlacionados aos itens da LC 116. Sem outra regra, a tributação é integral. Confira o código.";
    f.sel = f.opcoes.length - 1;
  } else if (!beneficio){
    f.cor = "verde"; f.selo = "Integral"; f.sel = f.opcoes.findIndex(o=>o.ccl==="000001");
    f.msg = (idx && idx.itens.length)
      ? "Sem benefício de CBS e IBS para este serviço nos anexos e na correlação oficial: tributação integral (CST 000, cClassTrib 000001)."
      : "NBS sem benefício nos anexos da lei e sem correlação com item da LC 116 nesta base: tributação integral (CST 000, cClassTrib 000001), salvo regra por prestador, tomador ou regime.";
  } else {
    f.cor = "amarelo"; f.selo = "Conferir";
    const iInt = f.opcoes.findIndex(o=>o.ccl==="000001" && o !== INTEGRAL);
    f.sel = (e && e.ccl && e.ccl !== "000001") ? 0 : (iInt >= 0 ? iInt : 0);
    f.msg = "Há mais de um tratamento possível para este serviço. A redução depende de quem presta, de quem contrata e da natureza da operação. Marque a opção que corresponde ao caso.";
  }
  if (f.opcoes.some(o=>REG_ESPECIFICO.test(o.ccl)))
    f.avisos.push("Há opção de regime específico (imóveis, bares e restaurantes, hotelaria, transporte, turismo ou serviços financeiros). A simulação aplica só a redução de alíquota; as regras próprias de base de cálculo e de crédito desses regimes não são simuladas.");
  if (f.opcoes.some(o=>o.ccl === "200052"))
    f.avisos.push("Redução de 30% para profissão intelectual regulamentada (art. 127): depende de quem presta, com sócios habilitados e fiscalizados por conselho, e não do código do serviço.");
  if (f.opcoes.some(o=>o.semRed))
    f.avisos.push("Há opção sem percentual de redução cadastrado nesta base. Confira a tabela oficial de cClassTrib e ajuste o tratamento manualmente.");
  if (itens.length) f.extra.push(["Item da LC 116", itens.slice(0,4).join("; ") + (itens.length > 4 ? "; e outros "+(itens.length-4) : "")]);
  if (ops.length) f.extra.push(["indOp possíveis", ops.map(o=>o[0]+(o[1]?" ("+o[1]+")":"")).join("; ")]);
  f.tipos = (e && e.t) || "T12";
  return f;
}

function garantirOpcaoTrat(r){
  const sel = $("#trat"), v = String(r);
  if (![...sel.options].some(o=>parseFloat(o.value) === r)){
    const o = document.createElement("option"); o.value = v; o.textContent = pctRed(r); sel.appendChild(o);
  }
  sel.value = [...sel.options].find(o=>parseFloat(o.value) === r).value;
}
function aplicarOpcao(i){
  if (!FICHA) return;
  FICHA.sel = i; FICHA.escolhido = true;
  garantirOpcaoTrat(FICHA.opcoes[i].red);
  desenharFicha(); calcular();
}
function selecionarCodigo(cod, manter){
  FICHA = TIPO === "produto" ? classificarNcm(cod) : classificarNbs(cod);
  $("#ncm").value = FICHA.fmt; $("#ncm-desc").dataset.cod = cod; $("#ncm-desc").textContent = "";
  $("#ncm-lista").style.display = "none";
  if (!manter){
    garantirOpcaoTrat(FICHA.opcoes[FICHA.sel].red);
    if (TIPO === "produto") $("#is").value = FICHA.is ? +(FICHA.is*100).toFixed(2) : 0;
  }
  desenharFicha(); calcular();
}
function desenharFicha(){
  const el = $("#ficha"), f = FICHA;
  if (!f){ el.innerHTML = ""; el.className = ""; return; }
  el.className = f.cor;
  const tratAtual = parseFloat($("#trat").value), o = f.opcoes[f.sel];
  let h = `<div class="f-top"><span class="selo">${esc(f.selo)}</span><span class="f-cod">${esc(f.fmt)}</span></div>`
    + `<div class="f-desc">${esc(f.desc || "Descrição não disponível nesta base.")}</div>`
    + `<div class="f-msg">${esc(f.msg)}</div>`
    + `<fieldset class="opc"><legend>${f.opcoes.length > 1 ? "Classificações possíveis" : "Classificação"}</legend>`
    + f.opcoes.map((x,i)=>`<label class="${i===f.sel?"sel":""}"><input type="radio" name="opc" value="${i}" ${i===f.sel?"checked":""}>`
        + `<span><b>${pctRed(x.red)}</b> · CST ${esc(x.cst)} · cClassTrib ${esc(x.ccl)}`
        + `<small>${esc(x.rot)}${x.semRed?" (percentual não cadastrado nesta base)":""}</small></span></label>`).join("")
    + `</fieldset><dl class="f-dl">`;
  if (o.base) h += `<dt>Base legal</dt><dd>${esc(o.base)}</dd>`;
  if (o.cond) h += `<dt>Condição</dt><dd>${esc(o.cond)}</dd>`;
  for (const [k,v] of f.extra) if (v) h += `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`;
  h += `</dl>`;
  if (f.isNota !== undefined)
    h += `<div class="f-al is"><b>Imposto Seletivo.</b> ${esc(f.isNota)}`
      + (f.is === null ? " O campo abaixo ficou em zero: preencha antes de usar o preço." : "") + `</div>`;
  for (const a of f.avisos) if (!(f.escolhido && a.startsWith("Enquanto você não escolher"))) h += `<div class="f-al">${esc(a)}</div>`;
  if (Math.abs(tratAtual - o.red) > 1e-9)
    h += `<div class="f-al">Tratamento ajustado manualmente para "${esc(pctRed(tratAtual))}", diferente da opção marcada na base.</div>`;
  const ts = String(f.tipos||"").split(";").filter(t=>DB.tipos[t]);
  if (ts.length) h += `<details><summary>Por que conferir (${ts.join(", ")})</summary><ul>`
    + ts.map(t=>`<li><b>${t}.</b> ${esc(DB.tipos[t])}</li>`).join("") + `</ul></details>`;
  el.innerHTML = h;
}
'''
a=s.index('/* ---------- busca de NCM ---------- */'); b=s.index('/* ---------- render ---------- */')
s=s[:a]+busca_js+'\n'+s[b:]

# painel do ano: rotulo de ICMS/ISS e sensibilidade sem beneficio
s=sub1(s,'''      + (A.icms>0.005 ? li("ICMS ou ISS na venda", -A.icms, "trib") : "")''','''      + (A.icms>0.005 ? li((o.servico?"ISS":"ICMS")+" na venda", -A.icms, "trib") : "")''')
s=sub1(s,'''         <b>${BRL.format(A.liquidoComprador)}</b>, e não ${BRL.format(A.nf)}.</p>`;
  } else {''','''         <b>${BRL.format(A.liquidoComprador)}</b>, e não ${BRL.format(A.nf)}.</p>`
      + (o.trat > 0 && ANO >= 2027 ? (()=>{ const S0 = noAno(Object.assign({}, o, {trat:0}), H.mc, o.pcAno, o.forn, o.aliqForn, o.anexoForn);
          return `<p class="dica" style="margin-top:9px;color:var(--carimbo)"><b>Risco do benefício.</b> Este preço conta com a
          ${pctRed(o.trat).toLowerCase()} de CBS e IBS. Se a condição não for atendida, o preço necessário passa a
          <b>${BRL.format(S0.nf)}</b> (${PCT(S0.nf/o.pv-1)} contra hoje), diferença de <b>${BRL.format(S0.nf - A.nf)}</b> por unidade.</p>`; })() : "");
  } else {''')
s=sub1(s,'''    + (o.regime==="simples" ? "" : li("Crédito de ICMS da compra", H.cred.icms, "cr"))''','''    + (o.regime==="simples" || o.servico ? "" : li("Crédito de ICMS da compra", H.cred.icms, "cr"))''')
s=sub1(s,'''  $("#dica-ano").textContent = ANO === 2026''','''  desenharFicha();
  $("#dica-ano").textContent = ANO === 2026''')
s=sub1(s,'''    : (ANO <= 2028 ? "CBS cheia e IBS em teste a 0,1%. ICMS integral."''','''    : (ANO <= 2028 ? "CBS provisória a "+PCT(t.cbs)+" e IBS em teste a 0,1%. ICMS e ISS integrais."''')

# eventos
a=s.index('  $("#ncm").addEventListener("input", e=>{'); b=s.index('  document.addEventListener("click", e=>{')
ev=r'''  $("#tipo").addEventListener("click", e=>{
    const b = e.target.closest("button"); if (!b || b.dataset.t === TIPO) return;
    definirTipo(b.dataset.t, true);
  });
  $("#ncm").addEventListener("input", e=>{
    const so = e.target.value.replace(/\D/g,"");
    const n = TIPO === "produto" ? 8 : 9;
    if (so.length === n && /^[\d.\s]+$/.test(e.target.value)){ selecionarCodigo(so); return; }
    if (FICHA && FICHA.cod !== so){ FICHA = null; desenharFicha(); }
    const r = TIPO === "produto" ? buscarNcm(e.target.value) : buscarNbs(e.target.value), l = $("#ncm-lista");
    if (!r.length){ l.style.display="none"; return; }
    l.innerHTML = r.slice(0,30).map(([c,d])=>
      `<div data-c="${c}"><b>${TIPO==="produto"?fmtNcm(c):fmtNbs(c)}</b>${esc(d)}</div>`).join("");
    l.style.display="block";
  });
  $("#ncm-lista").addEventListener("click", e=>{
    const d=e.target.closest("div[data-c]"); if(!d) return;
    selecionarCodigo(d.dataset.c);
  });
  $("#ficha").addEventListener("change", e=>{
    if (e.target.name === "opc") aplicarOpcao(+e.target.value);
  });
'''
s=s[:a]+ev+s[b:]
s=sub1(s,'''  $$("input, select").forEach(el=>{
    if (el.id==="senha") return;''','''  $$("input, select").forEach(el=>{
    if (el.id==="senha" || el.id==="ncm") return;''')
s=sub1(s,'''    baixar({tipo:"produto", app:"amcont-produto", geradoEm:new Date().toISOString().slice(0,10),
            ncm:$("#ncm").value, parametros:P, entradas:e},''','''    baixar({tipo:TIPO, app:"amcont-produto", geradoEm:new Date().toISOString().slice(0,10),
            ncm:$("#ncm").value, codigo:FICHA ? FICHA.cod : "", opcao:FICHA ? FICHA.sel : null,
            baseFiscal:DB.meta.versao, parametros:P, entradas:e},''')
s=sub1(s,'''      Object.keys(o.entradas).forEach(k=>{''','''      definirTipo(o.tipo === "servico" ? "servico" : "produto", false);
      if (o.codigo){ selecionarCodigo(String(o.codigo), true);
        if (FICHA && o.opcao != null && FICHA.opcoes[o.opcao]) FICHA.sel = o.opcao; }
      else { FICHA = null; }
      Object.keys(o.entradas).forEach(k=>{''')
s=sub1(s,'''      if (o.ncm) $("#ncm").value=o.ncm;
      sincronizar(); calcular(); avisar("Estudo carregado.","ok");''','''      if (o.ncm) $("#ncm").value=o.ncm;
      if (!$("#trat").value) garantirOpcaoTrat(parseFloat(o.entradas.trat)||0);
      sincronizar(); calcular(); avisar("Estudo carregado.","ok");''')
s=sub1(s,'''  sincronizar(); calcular();
}

function sincronizar(){''','''  $("#regras-corpo").innerHTML = `<table><thead><tr><th>Nº</th><th>Regra</th><th>Base legal</th><th>CST</th><th>cClassTrib</th><th>Redução</th></tr></thead><tbody>`
    + DB.regras.map(r=>`<tr><td>${r[0]}</td><td>${esc(r[1])}</td><td>${esc(r[2])}</td><td>${esc(r[3])}</td><td>${esc(r[4])}</td><td>${esc(r[5])}</td></tr>`).join("")
    + `</tbody></table>`;
  $("#fontes-db").textContent = "Base fiscal "+DB.meta.versao+", montada em "+DB.meta.montadoEm.split("-").reverse().join("/")+". Fontes: "+DB.meta.fontes.join("; ")+". "+DB.meta.aviso;
  sincronizar(); calcular();
}

function definirTipo(t, limpar){
  TIPO = t;
  $$("#tipo button").forEach(x=>x.setAttribute("aria-pressed", x.dataset.t === t));
  const sv = t === "servico";
  $("#lb-busca").textContent = sv ? "NBS ou item da LC 116, por código ou descrição" : "NCM, por código ou descrição";
  $("#ncm").placeholder = sv ? "ex.: 1.2301, 04.01 ou consultoria" : "ex.: 1806 ou chocolate";
  $("#tit-compra").textContent = sv ? "Insumos deste serviço com nota, hoje" : "A compra deste produto, hoje";
  $("#lb-pc").textContent = sv ? "Insumos e serviços tomados por unidade vendida, valor total das notas" : "Preço de compra por unidade, valor total da nota";
  $("#tit-venda").textContent = sv ? "A venda deste serviço, hoje" : "A venda deste produto, hoje";
  if (limpar){
    FICHA = null; $("#ncm").value = ""; $("#ncm-desc").textContent = ""; $("#ncm-lista").style.display = "none";
    $("#icms-venda").value = sv ? 5 : 18;
    $("#setor").value = sv ? "servicos" : "comercio";
    $("#anexo").value = sv ? "III" : "I";
    $("#trat").value = "0"; $("#is").value = 0;
    desenharFicha(); sincronizar(); calcular();
  }
}

function sincronizar(){''')
s=sub1(s,'''  $("#p-forn").hidden = false;
}''','''  $("#p-forn").hidden = false;
  const sv = TIPO === "servico";
  $("#c-is").hidden = sv; $("#c-icms-compra").hidden = sv;
  $("#lb-icms-venda").textContent = sv ? "Alíquota de ISS na sua venda (%)" : "Alíquota de ICMS na sua venda (%)";
}''')

from senha_js import SENHA_JS
s=sub1(s,'let HASH=null;',SENHA_JS+'let HASH=null;')
s=sub1(s,'''  if (h === (HASH || await sha256(CONFIG.SENHA_PADRAO))){
    document.getElementById("gate").remove();
    document.getElementById("app").hidden=false; iniciar();''','''  if (await senhaConfere(h, HASH || await sha256(CONFIG.SENHA_PADRAO))){
    document.getElementById("gate").remove();
    document.getElementById("app").hidden=false; iniciar(); montarTrocaSenha();''')
s=sub1(s,'''  // ICMS: MEI e pessoa fisica nao destacam; Simples tradicional destaca credito limitado
  let icms = 0;
  if (forn !== "mei" && forn !== "pf") icms = pc * icmsCompra * t.fatorIcmsIss;''','''  // ICMS: MEI e pessoa fisica nao transferem credito. O Simples tradicional transfere so o ICMS
  // efetivamente pago no DAS (LC 123/2006, art. 23, paragrafos 1 e 2): DAS x parcela de ICMS do anexo.
  let icms = 0;
  if (forn === "sn_tradicional"){
    const an = P.simplesAnexos[anexoForn] || P.simplesAnexos.I;
    icms = icmsCompra > 0 ? pc * aliqForn * an.icms * t.fatorIcmsIss : 0;
  } else if (forn !== "mei" && forn !== "pf") icms = pc * icmsCompra * t.fatorIcmsIss;''')
s=sub1(s,'''      <li>O crédito transferido por fornecedor do Simples é limitado à parcela de CBS e IBS embutida no DAS dele.</li>''','''      <li>O crédito transferido por fornecedor do Simples tradicional é limitado ao que ele paga dentro do DAS: a parcela de CBS e IBS e, no ICMS, a alíquota efetiva de ICMS da faixa dele, e não a alíquota cheia da nota.</li>''')

# ===== ajustes da validacao legal de 10/11/2026 =====
# LC 214, art. 12, par. 2, I e V: CBS e IBS fora da propria base e sem ICMS/ISS na base (ate 2032).
s=sub1(s,"""    if (regular){ const a = (t.cbs + t.ibs)*(1-(trat||0)); cbsIbs = a ? pc/(1+a)*a : 0; }""",
"""    // base da CBS e do IBS do fornecedor: valor da nota sem o ICMS e sem a propria CBS e IBS (LC 214, art. 12, par. 2)
    if (regular){ const a = (t.cbs + t.ibs)*(1-(trat||0)); cbsIbs = a ? pc*(1 - icmsCompra*t.fatorIcmsIss)/(1+a)*a : 0; }""")
s=sub1(s,"""  const s = o.is, k = (1-i)*(c+b), m = (1-k)/(1+s);
  const den = 1 - i - k - m*(s + o.r);
  const nf = (mcAlvo + pcAno - cr.total) / den;
  const icms = nf*i, bc = nf*(1-i), cbs = bc*c, ibs = bc*b;
  const impSel = s*nf*m, lucro = o.r*nf*m;""",
"""  // Bases conforme a lei: CBS e IBS sobre a nota sem ICMS ou ISS e sem a propria CBS e IBS (art. 12, par. 2, I e V);
  // Imposto Seletivo sobre a nota sem ICMS, CBS, IBS e o proprio IS (art. 417, I e par. 4);
  // ICMS ou ISS sobre o total da nota (posicao dos fiscos; tema ainda sem lei).
  const s = o.is, k = (1-i)*(c+b)/(1+c+b), sg = s*(1-i-k)/(1+s);
  const den = 1 - i - k - sg - o.r*(1-k-sg);
  const nf = (mcAlvo + pcAno - cr.total) / den;
  const icms = nf*i, bc = nf*(1-i)/(1+c+b), cbs = bc*c, ibs = bc*b;
  const impSel = nf*sg, lucro = o.r*nf*(1-k-sg);""")
s=sub1(s,"com cobrança a partir de fevereiro de 2027 e sujeitas à conversão em lei.","com efeitos a partir de 2 de fevereiro de 2027 (art. 19) e sujeitas à conversão em lei.")
s=sub1(s,"""<li>Análise de um produto, não da empresa.""","""<li>Bases de cálculo conforme a LC 214/2025: a CBS e o IBS não incidem sobre si mesmos nem sobre o ICMS e o ISS (art. 12, § 2º). O ICMS e o ISS foram calculados sobre o total da nota, incluindo CBS e IBS, que é a posição dos fiscos estaduais; o tema ainda não tem lei e há tese contrária.</li>
      <li>Análise de um produto, não da empresa.""")
s=sub1(s,"""  if (aeronave && !noXVII) f.avisos.push("Aeronave: a MP 1.399/2026 traz alíquota de Imposto Seletivo para a posição 88.02, mas o código não está marcado no Anexo XVII desta base. Confira o enquadramento antes de usar.");""",
"""  if (aeronave && !noXVII) f.avisos.push("Aeronave: a posição 88.02, exceto 8802.60.00, consta do Anexo XVII da LC 214/2025 e está sujeita ao Imposto Seletivo. Há alíquota zero e redução em casos específicos da MP 1.399/2026 (arts. 4º e 6º).");""")

# ===== rodada 3: ICMS de SC, consulta em lote, credito de PIS/COFINS no Lucro Real, LC 224 =====
s=sub1(s,"""function garantirOpcaoTrat(r){""","""/* ---------- ICMS de Santa Catarina, venda interna ---------- */
function icmsSC(cod){
  const S = DB.sc, hit = l => l.some(p=>cod.startsWith(p));
  const r = {notas:[], ops:[]};
  const s25 = S.r25.find(x=>cod.startsWith(x[0]));
  if (s25) r.ops.push({rot:"Produto supérfluo ("+s25[1]+"), qualquer destinatário", aliq:0.25, base:"Lei 10.297/1996, art. 19, II, b, e Anexo I, Seção I"});
  else {
    const m = S.r12.filter(x=>hit(x[0]));
    if (m.length){
      const x = m[0];
      r.ops.push({rot:x[1]+(x[3] ? "" : " (enquadramento pela descrição do produto)"), aliq:0.12, base:"Lei 10.297/1996, art. 19, III, e Anexo I, "+x[2], ind:!x[3]});
      if (!x[3]) r.ops.push({rot:"Consumidor final, se o produto não corresponder à descrição da lei", aliq:0.17, base:"Lei 10.297/1996, art. 19, I"});
    } else {
      r.ops.push({rot:"Consumidor final, uso e consumo ou ativo imobilizado", aliq:0.17, base:"Lei 10.297/1996, art. 19, I"});
      r.ops.push({rot:"Contribuinte, para revenda ou industrialização", aliq:0.12, base:"Lei 10.297/1996, art. 19, III, n"});
    }
    if (hit(S.textil)) r.notas.push("Têxteis, vestuário e artefatos de couro: os 12% entre contribuintes não valem para a saída feita pelo próprio fabricante (art. 19, § 3º, III).");
  }
  for (const x of S.c7) if (hit(x[0])) r.ops.push({rot:"Cesta básica, carga reduzida: "+x[1]+" (pela descrição)", aliq:0.07, base:"RICMS/SC, Anexo 2, art. 11-A", ind:true, fim:2026});
  for (const x of S.isento) if (x[0].includes(cod)) r.ops.push({rot:x[1], aliq:0, base:x[2], fim:2026});
  for (const x of S.outros) if (hit(x[0])) r.notas.push(x[1]);
  return r;
}
function garantirOpcaoTrat(r){""")
s=sub1(s,"""  FICHA = TIPO === "produto" ? classificarNcm(cod) : classificarNbs(cod);
""","""  FICHA = TIPO === "produto" ? classificarNcm(cod) : classificarNbs(cod);
  FICHA.sc = (TIPO === "produto" && FICHA.cor !== "cinza") ? icmsSC(cod) : null;
""")
s=sub1(s,"""  const ts = String(f.tipos||"").split(";").filter(t=>DB.tipos[t]);""","""  if (f.sc){
    const atual = num("icms-venda")/100;
    h += `<fieldset class="opc" style="margin-top:10px"><legend>ICMS em Santa Catarina, venda interna</legend>`
      + f.sc.ops.map((x,i)=>{ const on = f.scSel === i && Math.abs(atual - x.aliq) < 1e-9;
          return `<label class="${on?"sel":""}"><input type="radio" name="scopt" value="${i}" ${on?"checked":""}>`
          + `<span><b>${x.aliq === 0 ? "Isento" : PCT(x.aliq)}</b> · ${esc(x.rot)}<small>${esc(x.base)}`
          + (x.fim ? " · vale até 31/12/"+x.fim+"; depois depende de prorrogação" : "") + `</small></span></label>`; }).join("")
      + `</fieldset>`
      + f.sc.notas.map(n=>`<div class="f-al">${esc(n)}</div>`).join("")
      + `<p class="dica">Marque a opção para levar a alíquota ao campo de ICMS da venda. ${esc(DB.sc.meta.aviso)}</p>`;
  }
  const ts = String(f.tipos||"").split(";").filter(t=>DB.tipos[t]);""")
s=sub1(s,"""    if (e.target.name === "opc") aplicarOpcao(+e.target.value);""","""    if (e.target.name === "opc") aplicarOpcao(+e.target.value);
    if (e.target.name === "scopt" && FICHA && FICHA.sc){
      FICHA.scSel = +e.target.value; $("#icms-venda").value = +(FICHA.sc.ops[FICHA.scSel].aliq*100).toFixed(2); calcular(); }""")
# --- credito de PIS e COFINS da compra no Lucro Real (Leis 10.637 e 10.833; ICMS fora da base, Lei 14.592/2023)
s=sub1(s,"""  const lucro = o.pv * o.r;
  const trib = icms + pis + cof + lucro - cr.total;
  return {trib, mc:o.pv - o.pc - trib, cred:cr,""","""  const lucro = o.pv * o.r;
  const pcCred = (o.regime === "real" && o.forn !== "pf")
    ? o.pc * (1 - (o.forn === "regular" ? o.icmsCompra : 0)) * (o.pis + o.cofins) : 0;
  const trib = icms + pis + cof + lucro - cr.total - pcCred;
  return {trib, mc:o.pv - o.pc - trib, cred:cr, pcCred,""")
s=sub1(s,"""    + (o.regime==="simples" || o.servico ? "" : li("Crédito de ICMS da compra", H.cred.icms, "cr"))""","""    + (o.regime==="simples" || o.servico ? "" : li("Crédito de ICMS da compra", H.cred.icms, "cr"))
    + (H.pcCred > 0.005 ? li("Crédito de PIS e COFINS da compra", H.pcCred, "cr") : "")""")
# --- LC 224/2025
s=sub1(s,"""  "limiteAdicional": 240000,
  "aliqAdicional": 0.1
 },""","""  "limiteAdicional": 240000,
  "aliqAdicional": 0.1,
  "limitePresuncao": 5000000,
  "acrescimoPresuncao": 0.1
 },""")
s=sub1(s,"""          <p class="dica">No Lucro Presumido eles incidem sobre a receita, então entram no fluxo de caixa da venda.</p>""","""          <p class="dica">No Lucro Presumido eles incidem sobre a receita, então entram no fluxo de caixa da venda.</p>
          <label style="margin-top:9px"><input type="checkbox" id="lc224" style="width:auto;margin-right:7px">
            Receita anual acima de R$ 5 milhões</label>
          <p class="dica">A LC 224/2025 acresce 10% aos percentuais de presunção sobre a receita que excede R$ 5 milhões no ano (8% passa a 8,8%). Há decisões judiciais suspendendo a regra.</p>""")
s=sub1(s,"""    r: incl ? (at.presIrpj*P.lucro.aliqIrpj + at.presCsll*P.lucro.aliqCsll) : 0""","""    r: incl ? (at.presIrpj*P.lucro.aliqIrpj + at.presCsll*P.lucro.aliqCsll)
              * (1 + ($("#lc224").checked ? (P.lucro.acrescimoPresuncao || 0) : 0)) : 0""")
s=sub1(s,"""e, no ICMS, a alíquota efetiva de ICMS da faixa dele, e não a alíquota cheia da nota.</li>""","""e, no ICMS, a alíquota efetiva de ICMS da faixa dele, e não a alíquota cheia da nota. O crédito de ICMS só existe para mercadoria destinada a revenda ou industrialização.</li>
      <li>O ICMS de Santa Catarina é sugerido pela alíquota interna da lei. Substituição tributária, TTD, crédito presumido e operações interestaduais não são simulados.</li>""")
# --- consulta em lote
s=sub1(s,"""    <button type="button" class="btn forte" id="b-salvar">Salvar estudo</button>""","""    <button type="button" class="btn forte" id="b-salvar">Salvar estudo</button>
    <button type="button" class="btn" id="b-consulta">Consultar tributação por código</button>""")
s=sub1(s,"""  <div class="grade">""","""  <div id="tela-consulta" hidden>
    <div class="painel" style="margin-top:18px">
      <h3>Consulta de tributação por NCM ou NBS</h3>
      <p class="dica" style="margin-bottom:8px">Cole ou digite os códigos, um por linha ou separados por vírgula, com ou sem pontos: 8 dígitos para NCM (produto) e 9 para NBS (serviço). Até 200 por vez.</p>
      <textarea id="cq" rows="5" style="width:100%;padding:9px 11px;border:1px solid var(--linha);border-radius:var(--r);background:var(--via-2);font:500 14px 'IBM Plex Mono',monospace" placeholder="1006.30.21&#10;2202.10.00&#10;1.2301.22.00"></textarea>
      <div class="barra" style="padding-top:10px"><button type="button" class="btn forte" id="b-consultar">Consultar</button>
        <button type="button" class="btn" onclick="window.print()">Imprimir ou salvar em PDF</button></div>
      <div id="cq-res" style="margin-top:14px;overflow-x:auto"></div>
    </div>
  </div>
  <div class="grade">""")
s=sub1(s,"""\n[hidden]{display:none!important}""","""\n[hidden]{display:none!important}
table.cq{width:100%;border-collapse:collapse;font-size:12px;line-height:1.4}
table.cq th{text-align:left;font:600 10px "IBM Plex Mono";letter-spacing:.08em;text-transform:uppercase;color:var(--petroleo-2);padding:0 8px 6px 0;border-bottom:1px solid var(--linha);white-space:nowrap}
table.cq td{padding:7px 8px 7px 0;border-bottom:1px solid #EEEDE8;vertical-align:top}
table.cq td.c{font-family:"IBM Plex Mono";white-space:nowrap;color:var(--petroleo);font-weight:600}
table.cq .selo{display:inline-block}
table.cq button{margin-top:4px;font-size:11px;padding:3px 7px}""")
s=sub1(s,"""function definirTipo(t, limpar){""","""function consultarLote(){
  const itens = $("#cq").value.split(/[\\s,;]+/).map(x=>x.trim()).filter(Boolean).slice(0,200);
  const cor = {verde:"var(--saldo)", amarelo:"#B98A14", vermelho:"var(--carimbo)", cinza:"#7C8A8D"};
  const linhas = itens.map(bruto=>{
    const d = bruto.replace(/\\D/g,"");
    if (d.length !== 8 && d.length !== 9)
      return `<tr><td class="c">${esc(bruto)}</td><td colspan="7">Código inválido: use 8 dígitos para NCM ou 9 para NBS.</td></tr>`;
    const prod = d.length === 8, f = prod ? classificarNcm(d) : classificarNbs(d), o = f.opcoes[f.sel];
    const outras = f.opcoes.filter((x,i)=>i!==f.sel).map(x=>pctRed(x.red)+" (cClassTrib "+x.ccl+": "+x.rot+")").join("; ");
    const sc = (prod && f.cor !== "cinza") ? icmsSC(d) : null;
    return `<tr><td class="c">${esc(f.fmt)}<br><button type="button" class="btn" data-sim="${d}">Simular</button></td>`
      + `<td>${esc(f.desc || "Descrição não disponível")}</td>`
      + `<td><span class="selo" style="background:${cor[f.cor]}">${esc(f.selo)}</span></td>`
      + `<td><b>${pctRed(o.red)}</b><br>CST ${esc(o.cst)} · cClassTrib ${esc(o.ccl)}<br>${esc(o.rot)}`
      + (outras ? `<br><span style="color:#5C6E72">Outras possíveis: ${esc(outras)}</span>` : "") + `</td>`
      + `<td>${esc(o.base)}${o.cond ? "<br>"+esc(o.cond) : ""}${f.avisos.length ? "<br><i>"+esc(f.avisos.join(" "))+"</i>" : ""}</td>`
      + `<td>${(()=>{ if (!prod || f.cor === "cinza") return prod ? "" : "Normal"; const q = pcHoje(d);
            return "<b>"+esc(q.st ? "Substituição tributária" : PC_ROT[q.reg])+"</b>"+(q.base ? "<br>"+esc(q.base) : "")+(q.obs ? "<br><i>"+esc(q.obs)+"</i>" : "")+(q.ind ? "<br><i>Pela descrição ou Ex da TIPI</i>" : ""); })()}</td>`
      + `<td>${f.isNota !== undefined ? (f.is == null ? "Informar. " : PCT(f.is)+". ") + esc(f.isNota) : "Não se aplica"}</td>`
      + `<td>${sc ? sc.ops.map(x=>"<b>"+(x.aliq===0?"Isento":PCT(x.aliq))+"</b> "+esc(x.rot)+(x.fim?" (até 31/12/"+x.fim+")":"")).join("<br>")
                    + (sc.notas.length ? "<br><i>"+esc(sc.notas.join(" "))+"</i>" : "") : (prod ? "" : "ISS municipal")}</td></tr>`;
  });
  $("#cq-res").innerHTML = linhas.length
    ? `<table class="cq"><thead><tr><th>Código</th><th>Descrição</th><th>Situação</th><th>CBS e IBS</th><th>Base legal e condição</th><th>PIS e COFINS hoje</th><th>Imposto Seletivo 2027</th><th>ICMS em SC, venda interna</th></tr></thead><tbody>`
      + linhas.join("") + `</tbody></table><p class="dica" style="margin-top:10px">${esc(DB.meta.aviso)} ${esc(DB.sc.meta.aviso)}</p>`
    : `<p class="dica">Nenhum código informado.</p>`;
}
function telaConsulta(abrir){
  $("#tela-consulta").hidden = !abrir; document.querySelector(".grade").hidden = abrir;
  $("#b-consulta").textContent = abrir ? "Voltar à simulação de preço" : "Consultar tributação por código";
}
function definirTipo(t, limpar){""")
s=sub1(s,"""  $("#ficha").addEventListener("change", e=>{""","""  $("#b-consulta").addEventListener("click", ()=>telaConsulta($("#tela-consulta").hidden));
  $("#b-consultar").addEventListener("click", consultarLote);
  $("#cq-res").addEventListener("click", e=>{
    const b = e.target.closest("button[data-sim]"); if (!b) return;
    const d = b.dataset.sim; definirTipo(d.length === 8 ? "produto" : "servico", true); telaConsulta(false); selecionarCodigo(d);
    window.scrollTo({top:0});
  });
  $("#ficha").addEventListener("change", e=>{""")
s=sub1(s,"""    if (el.id==="senha" || el.id==="ncm") return;""","""    if (el.id==="senha" || el.id==="ncm" || el.id==="cq") return;""")

# ===== rodada 4: PIS e COFINS no regime atual (monofasico, aliquota zero) e ano de 2026 =====
s=sub1(s,"""/* ---------- ICMS de Santa Catarina, venda interna ---------- */""","""/* ---------- PIS e COFINS no regime atual (2026) ---------- */
function pcHoje(cod){
  if (!DB.pc.monoExc.includes(cod)){
    let best = null, n = 0;
    for (const r of DB.pc.monoR) for (const p of r[0]) if (cod.startsWith(p) && p.length > n){ best = r; n = p.length; }
    if (best) return {reg:"mono", grupo:best[3], g:best[1], st:best[1] === "5",
      base:(best[1] === "5" ? "Tabela 4.3.12, código " : "Tabela 4.3.10, código ")+best[2]+"; "+best[4], obs:best[7], conc:best[5]+best[6]};
  }
  const m = DB.pc.auto[cod];
  if (m) return {reg:"mono", grupo:"Autopeças", g:"3", base:"Tabela 4.3.10, código 302; "+St(m[0]), obs:St(m[1]), conc:DB.pc.autoConc[0]+DB.pc.autoConc[1], lista:true};
  if (!DB.pc.zeroExc.includes(cod)){
    const z = DB.pc.zero.find(x=>x[0].some(p=>cod.startsWith(p)));
    if (z) return {reg:"zero", desc:z[1], base:z[2], ind:!z[3]};
  }
  return {reg:"normal"};
}
const PC_ROT = {normal:"Tributação normal", mono:"Monofásico: alíquota zero na revenda", monofab:"Monofásico: fabricante ou importador", zero:"Alíquota zero", isento:"Isento, suspenso ou sem incidência"};
// aliquota concentrada do fabricante ou importador de monofasico (Tabela 4.3.10)
function pcConc(){ return (TIPO === "produto" && FICHA && FICHA.pc && FICHA.pc.conc) ? FICHA.pc.conc : 0; }
function pcRegime(){
  const v = $("#pc-hoje").value;
  if (v !== "auto") return v;
  return (TIPO === "produto" && FICHA && FICHA.pc) ? FICHA.pc.reg : "normal";
}
function pcCredito(o, pc, forn){
  return (o.regime === "real" && forn !== "pf" && (o.pcReg === "normal" || o.pcReg === "monofab"))
    ? pc * (1 - (forn === "regular" ? o.icmsCompra : 0)) * (o.pis + o.cofins) : 0;
}
/* ---------- ICMS de Santa Catarina, venda interna ---------- */""")
s=sub1(s,"""  FICHA.sc = (TIPO === "produto" && FICHA.cor !== "cinza") ? icmsSC(cod) : null;
""","""  FICHA.sc = (TIPO === "produto" && FICHA.cor !== "cinza") ? icmsSC(cod) : null;
  FICHA.pc = (TIPO === "produto" && FICHA.cor !== "cinza") ? pcHoje(cod) : null;
""")
s=sub1(s,"""  if (f.sc){
    const atual = num("icms-venda")/100;""","""  if (f.pc){
    const q = f.pc;
    h += `<fieldset class="opc" style="margin-top:10px"><legend>PIS e COFINS hoje, regime de 2026</legend></fieldset><dl class="f-dl">`
      + `<dt>Tratamento</dt><dd><b>${esc(q.st ? "Substituição tributária: sem PIS e COFINS na revenda" : PC_ROT[q.reg])}</b>${q.reg==="mono" ? " ("+esc(q.grupo)+")" : (q.reg==="zero" ? " ("+esc(q.desc)+")" : "")}</dd>`
      + (q.base ? `<dt>Base legal</dt><dd>${esc(q.base)}</dd>` : "") + (q.obs ? `<dt>Restrição</dt><dd>${esc(q.obs)}</dd>` : "") + `</dl>`;
    if (q.reg === "mono" && q.st) h += `<div class="f-al">O PIS e a COFINS da revenda já foram recolhidos pelo fabricante ou importador, por substituição tributária. Na revenda não há valor a pagar nem crédito na compra. O cálculo do fabricante substituto não é simulado. Em 2027 a substituição acaba e a venda passa a pagar CBS.</div>`;
    if (q.reg === "mono" && !q.st) h += `<div class="f-al">Na revenda não há PIS e COFINS a pagar nem crédito na compra. `
      + (q.g === "4" ? "Nas bebidas frias a alíquota zero vale para o varejista; atacadista e fabricante são tributados. " : "")
      + `Se você é o fabricante ou o importador, escolha "Monofásico: sou fabricante ou importador" no campo de PIS e COFINS: a alíquota concentrada deste produto é de ${PCT(q.conc||0)}. ${q.lista ? "A lista de NCM de autopeças não foi conferida contra os Anexos I e II da Lei 10.485/2002. " : ""}Em 2027 o regime monofásico acaba, exceto para combustíveis, e a venda passa a pagar CBS.</div>`;
    if (q.reg === "zero") h += `<div class="f-al">Venda sem PIS e COFINS hoje e compra sem crédito. ${q.ind ? "O enquadramento depende da descrição do produto ou do Ex da TIPI. " : ""}Em 2027 passa a valer a regra de CBS e IBS mostrada acima.</div>`;
  }
  if (f.sc){
    const atual = num("icms-venda")/100;""")
# campo de escolha
s=sub1(s,"""          <label><input type="checkbox" id="inc-lucro" checked style="width:auto;margin-right:7px">""","""          <label for="pc-hoje">PIS e COFINS hoje nesta venda</label>
          <select id="pc-hoje">
            <option value="auto">Automático, pela base do NCM</option>
            <option value="normal">Tributação normal</option>
            <option value="mono">Monofásico: alíquota zero na revenda</option>
            <option value="monofab">Monofásico: sou fabricante ou importador</option>
            <option value="zero">Alíquota zero</option>
            <option value="isento">Isento, suspenso ou sem incidência</option>
          </select>
          <p class="dica" id="dica-pc" style="margin-bottom:11px"></p>
          <label><input type="checkbox" id="inc-lucro" checked style="width:auto;margin-right:7px">""")
s=sub1(s,"""    ano:ANO, regime:reg, trat:parseFloat($("#trat").value), servico:TIPO==="servico",""","""    ano:ANO, regime:reg, trat:parseFloat($("#trat").value), servico:TIPO==="servico", pcReg:pcRegime(), pcConc:pcConc(),""")
# hoje()
s=sub1(s,"""  if (o.regime === "simples"){
    const das = o.pv * o.aliqSN;
    return {trib:das, mc:o.pv - o.pc - das, cred:{cbsIbs:0,icms:0,total:0},""","""  if (o.regime === "simples"){
    // Monofasico no Simples: a receita e segregada e o DAS sai sem as parcelas de PIS e COFINS (LC 123, art. 18, par. 4-A, I)
    const anH = P.simplesAnexos[o.anexo] || P.simplesAnexos.I;
    const monoH = o.pcReg === "mono" || o.pcReg === "monofab";
    const das = o.pv * (o.aliqSN * (1 - (monoH ? anH.pis + anH.cofins : 0)) + (o.pcReg === "monofab" ? o.pcConc : 0));
    return {trib:das, mc:o.pv - o.pc - das, cred:{cbsIbs:0,icms:0,total:0}, pcCred:0,""")
s=sub1(s,"""  const pis  = bpc * o.pis, cof = bpc * o.cofins;""","""  const pcOn = o.pcReg === "normal", fab = o.pcReg === "monofab";
  // fabricante ou importador de monofasico: aliquota concentrada da Tabela 4.3.10, lancada na linha da COFINS
  const pis  = pcOn ? bpc * o.pis : 0, cof = pcOn ? bpc * o.cofins : (fab ? bpc * o.pcConc : 0);""")
s=sub1(s,"""  const pcCred = (o.regime === "real" && o.forn !== "pf")
    ? o.pc * (1 - (o.forn === "regular" ? o.icmsCompra : 0)) * (o.pis + o.cofins) : 0;""","""  const pcCred = pcCredito(o, o.pc, o.forn);""")
# noAno: 2026 = regime atual
s=sub1(s,"""  if (o.regime === "simples"){
    // tradicional: CBS e IBS permanecem dentro do DAS, sem credito
    const nfT = (mcAlvo + pcAno) / (1 - o.aliqSN);""","""  if (o.regime !== "simples" && o.ano === 2026){
    // 2026 e o regime atual: PIS e COFINS ainda vigentes, sem CBS e IBS
    const pcC = pcCredito(o, pcAno, forn);
    const kpc = (o.pcReg === "normal" ? o.pis + o.cofins : (o.pcReg === "monofab" ? o.pcConc : 0)) * (o.servico ? 1 : 1 - i);
    const nf = (mcAlvo + pcAno - cr.icms - pcC) / (1 - i - kpc - o.r);
    const icms = nf*i, pisCof = nf*kpc, lucro = o.r*nf, trib = icms + pisCof + lucro - cr.icms - pcC;
    return {tipo:"geral", nf, cred:{cbsIbs:0, icms:cr.icms, total:cr.icms}, icms, cbs:0, ibs:0, impSel:0, lucro, pisCof, pcCred:pcC,
            trib, i, c:0, b:0, liquidoComprador:nf, mc:nf - pcAno - trib};
  }
  if (o.regime === "simples"){
    // tradicional: CBS e IBS permanecem dentro do DAS, sem credito
    const anT = P.simplesAnexos[o.anexo] || P.simplesAnexos.I;
    const monoT = o.ano === 2026 && (o.pcReg === "mono" || o.pcReg === "monofab");
    const aliqT = o.aliqSN * (1 - (monoT ? anT.pis + anT.cofins : 0)) + (o.ano === 2026 && o.pcReg === "monofab" ? o.pcConc : 0);
    const nfT = (mcAlvo + pcAno) / (1 - aliqT);""")
s=sub1(s,"""            trad:{nf:nfT, das:nfT*o.aliqSN, liquidoComprador:nfT},""","""            trad:{nf:nfT, das:nfT*aliqT, liquidoComprador:nfT},""")
s=sub1(s,"""      + (A.cbs>0.005 ? li("CBS "+PCT(A.c), -A.cbs, "trib") : "")""","""      + (A.pcCred>0.005 ? li("Crédito de PIS e COFINS", A.pcCred, "cr") : "")
      + (A.pisCof>0.005 ? li("PIS e COFINS", -A.pisCof, "trib") : "")
      + (A.cbs>0.005 ? li("CBS "+PCT(A.c), -A.cbs, "trib") : "")""")
s=sub1(s,"""  desenharFicha();
  $("#dica-ano").textContent = ANO === 2026""","""  desenharFicha();
  $("#dica-pc").textContent = (o.regime === "simples"
      ? "No Simples, só o monofásico reduz o DAS de hoje (receita segregada). Alíquota zero e isenção não se aplicam ao optante. "
      : "Monofásico e alíquota zero zeram o PIS e a COFINS de hoje e o crédito da compra. ")
    + "Tratamento em uso: " + PC_ROT[o.pcReg].toLowerCase() + "."
    + (o.pcReg !== "normal" ? " A partir de 2027 a venda passa a pagar CBS, o que tende a elevar o preço necessário." : "");
  $("#dica-ano").textContent = ANO === 2026""")
s=sub1(s,"""      <li>O ICMS de Santa Catarina é sugerido""","""      <li>O PIS e a COFINS de hoje seguem o tratamento do produto: monofásico e alíquota zero não pagam na revenda e não geram crédito na compra. Fabricante e importador de produto monofásico pagam a alíquota concentrada da Tabela 4.3.10 da EFD-Contribuições.</li>
      <li>O ICMS de Santa Catarina é sugerido""")


# ===== consulta em lote entra no arquivo salvo =====
s=sub1(s,"""            baseFiscal:DB.meta.versao, parametros:P, entradas:e},""","""            baseFiscal:DB.meta.versao, consulta:$("#cq").value, parametros:P, entradas:e},""")
s=sub1(s,"""      if (o.ncm) $("#ncm").value=o.ncm;""","""      if (o.ncm) $("#ncm").value=o.ncm;
      $("#cq").value = o.consulta || "";
      if (o.consulta){ consultarLote(); } else { $("#cq-res").innerHTML = ""; }""")
s=sub1(s,"""<button type="button" class="btn forte" id="b-consultar">Consultar</button>""","""<button type="button" class="btn forte" id="b-consultar">Consultar</button>
        <button type="button" class="btn" id="b-cq-salvar">Salvar consulta</button>
        <button type="button" class="btn" id="b-cq-abrir">Abrir consulta</button>""")
s=sub1(s,"""  $("#b-consultar").addEventListener("click", consultarLote);""","""  $("#b-consultar").addEventListener("click", consultarLote);
  $("#b-cq-salvar").addEventListener("click", ()=>$("#b-salvar").click());
  $("#b-cq-abrir").addEventListener("click", ()=>$("#arquivo").click());""")
s=sub1(s,"""      <p class="dica" style="margin-bottom:8px">Cole ou digite os códigos,""","""      <p class="dica" style="margin-bottom:8px">A lista de códigos é gravada junto com o estudo, no mesmo arquivo .json. Cole ou digite os códigos,""")
# ===== logotipo da Amcont =====
_logo=open('logo_b64.txt').read()
_img='<img class="%s" alt="Amcont Assessoria e Contabilidade" src="data:image/png;base64,'+_logo+'">'
s=sub1(s,'<div class="gate-mark">Amcont</div>',_img%'logo-gate')
s=sub1(s,'<span class="mark">AMCONT</span>',_img%'logo-hd')
s=sub1(s,'</style>','.logo-gate{display:block;height:58px;margin-bottom:18px;filter:brightness(0) invert(1)}\n.logo-hd{height:32px;align-self:center;filter:brightness(0) invert(1)}\n@media print{header{background:#fff!important;color:#10242A!important;border-bottom:2px solid #2A5F6B}.logo-hd{filter:none}header .sub,header .lei{color:#2A5F6B!important}}\n</style>')
open('amcont-produto.html','w',encoding='utf-8').write(s)
print('ok',len(s))
