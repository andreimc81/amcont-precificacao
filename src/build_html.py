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
s=sub1(s,'"versaoDados": "2026.1"','"versaoDados": "'+__import__('json').load(open('monitor/versao.json'))['base']+'.'+str(__import__('json').load(open('monitor/versao.json'))['seq'])+'"'); s=sub1(s,'"atualizadoEm": "2026-08-13"','"atualizadoEm": "2026-11-10"')
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
      f.cor = e.e === "i" || e.u ? "verde" : "amarelo"; f.selo = e.e === "i" ? "Integral" : (e.u ? "Benefício" : "Conferir");
      f.opcoes.push({rot:(e.ax||"")+(e.it?", item "+e.it:""), red:r, cst:e.cst, ccl:e.ccl, base:St(e.b), cond:St(e.c)});
      if (r > 0 && !e.u) f.opcoes.push(Object.assign({}, INTEGRAL, {rot:"Tributação integral, só se o produto não atender à condição acima", base:"Use apenas quando o produto real não corresponder ao NCM ou à descrição do item da lei (ex.: produto temperado, processado ou excluído pelo \"exceto\")."}));
      f.sel = 0;
      f.msg = St(e.m) || (e.u ? "Benefício previsto na lei para este NCM, sem outra condição. Basta o NCM do produto estar correto."
                         : r > 0 ? "Há benefício previsto na lei, condicionado ao que está descrito abaixo. Confirme antes de formar o preço."
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
  if (s25){ r.ops.push({rot:"Produto supérfluo ("+s25[1]+"), qualquer destinatário", aliq:0.25, base:"Lei 10.297/1996, art. 19, II, b, e Anexo I, Seção I"}); r.fixa = true; }
  else {
    const m = S.r12.filter(x=>hit(x[0]));
    if (m.length){
      const x = m[0], exato = x[3] || hit(S.r12nc || []);
      r.ops.push({rot:x[1]+(exato ? ", qualquer destinatário (o NCM corresponde à descrição da lei)" : " (enquadramento pela descrição do produto)"), aliq:0.12, base:"Lei 10.297/1996, art. 19, III, e Anexo I, "+x[2], ind:!exato});
      r.fixa = !!exato;
      if (!exato) r.ops.push({rot:"Consumidor final, se o produto não corresponder à descrição da lei", aliq:0.17, base:"Lei 10.297/1996, art. 19, I"});
    } else {
      r.ops.push({rot:"Consumidor final, uso e consumo ou ativo imobilizado", aliq:0.17, base:"Lei 10.297/1996, art. 19, I"});
      r.ops.push({rot:"Contribuinte, para revenda ou industrialização", aliq:0.12, base:"Lei 10.297/1996, art. 19, III, n"});
    }
    if (hit(S.textil)) r.notas.push("Têxteis, vestuário e artefatos de couro: os 12% entre contribuintes não valem para a saída feita pelo próprio fabricante (art. 19, § 3º, III).");
  }
  for (const x of S.c7) if (hit(x[0])) r.ops.push({rot:"Cesta básica, carga reduzida: "+x[1]+" (pela descrição)", aliq:0.07, base:"RICMS/SC, Anexo 2, art. 11-A", ind:true, fim:2026});
  for (const x of S.isento) if (x[0].includes(cod)) r.ops.push({rot:x[1], aliq:0, base:x[2], fim:2026});
  for (const x of S.outros) if (hit(x[0])) r.notas.push(x[1]);
  // só preenche sozinho quando não há outra alíquota possível (isenção ou carga de 7% da cesta básica exigem escolha)
  r.fixa = !!r.fixa && r.ops.length === 1;
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

# ===== rodada 6: busca pelo codigo de servico (item da LC 116) com os NBS possiveis =====
s=sub1(s,r"""function buscarNbs(q){""",r"""let LCP = null;   // item da LC 116 aberto no painel de NBS possiveis
const LCMAP = new Map(DB.lc.map(x=>[x.i, x]));
function itemLc(q){
  // aceita 4.01, 04.01, 0401, 401, 04.01.01 e 040101 (codigo de tributacao nacional da NFS-e)
  const t = String(q).trim().replace(",", ".");
  if (!/^[\d.\s]+$/.test(t)) return null;
  let p = t.split(".").map(x=>x.replace(/\D/g,"")).filter(Boolean);
  if (p.length === 1){ const d = p[0];
    if (d.length === 3) p = [d[0], d.slice(1)];
    else if (d.length === 4) p = [d.slice(0,2), d.slice(2)];
    else if (d.length === 6) p = [d.slice(0,2), d.slice(2,4), d.slice(4)];
    else return null; }
  if (p.length < 2 || p.length > 3 || p.some(x=>x.length > 2)) return null;
  p = p.map(x=>x.padStart(2,"0"));
  const k3 = p.join("."), k2 = p.slice(0,2).join(".");
  if (LCMAP.has(k3)) return {item:k3, desd:null};
  if (LCMAP.has(k2)) return {item:k2, desd:p[2]||null};
  return null;
}
function buscarItens(q){
  const t = semAcento(q.trim()); if (t.length < 2) return [];
  const ex = itemLc(q); if (ex) return [LCMAP.get(ex.item)];
  const m = /^(\d{1,2})[.,]?(\d?)$/.exec(t);
  if (m){ const g = m[1].padStart(2,"0");
    return DB.lc.filter(x=>x.i.startsWith(g+"."+m[2]) || (m[1].length === 2 && m[2] === "" && x.i.startsWith(m[1]))).slice(0,12); }
  if (/^[\d.\s]+$/.test(t) || t.length < 3) return [];
  return DB.lc.filter(x=>semAcento(x.d).includes(t)).slice(0,12);
}
function resumoNbs(cod, item){
  const f = classificarNbs(cod, item), o = f.opcoes[f.sel];
  const outras = f.opcoes.filter((x,i)=>i !== f.sel).map(x=>x.ccl);
  return {f, o, txt: pctRed(o.red)+" · CST "+o.cst+" · cClassTrib "+o.ccl + (outras.length ? " (ou "+outras.join(", ")+")" : "")};
}
function selecionarItem(item){
  const it = LCMAP.get(item); if (!it) return;
  $("#ncm-lista").style.display = "none";
  if (it.n.length === 1){ selecionarCodigo(it.n[0][0], false, item); return; }
  LCP = item; FICHA = null; $("#ncm").value = item; $("#ncm-desc").textContent = "";
  $("#trat").value = "0";
  desenharFicha(); calcular();
}
function desenharPainelLc(el){
  const it = LCMAP.get(LCP);
  el.className = it.n.length ? "amarelo" : "cinza";
  let h = `<div class="f-top"><span class="selo">${it.n.length ? "Escolher o NBS" : "Sem correlação"}</span><span class="f-cod">LC 116, item ${esc(it.i)}</span></div>`
    + `<div class="f-desc">${esc(it.d)}</div>`;
  if (!it.n.length){
    el.innerHTML = h + `<div class="f-msg">O Anexo VIII da NFS-e Nacional não traz NBS correlacionado a este item nesta base. Busque o NBS pela descrição do serviço.</div>`;
    return;
  }
  h += `<div class="f-msg">O Anexo VIII da NFS-e Nacional admite ${it.n.length} códigos NBS para este item. Marque o que descreve o serviço prestado: o cClassTrib e a redução já vêm classificados para cada um.</div>`
    + (it.n.length > 10 ? `<input id="lcp-f" type="text" placeholder="filtrar por palavra ou código" style="margin:8px 0 6px">` : "")
    + `<div class="opc lcp" style="max-height:340px;overflow:auto">`
    + it.n.map(([cod])=>{ const r = resumoNbs(cod, it.i);
        return `<label data-nbs="${cod}" data-t="${esc(semAcento(r.f.desc)+" "+cod+" "+fmtNbs(cod))}"><input type="radio" name="lcp" value="${cod}">`
          + `<span><b>${fmtNbs(cod)}</b> ${esc(r.f.desc)}<small>${esc(r.txt)}</small></span></label>`; }).join("")
    + `</div>`;
  if (it.op && it.op.length) h += `<dl class="f-dl"><dt>indOp possíveis</dt><dd>${esc(it.op.map(o=>o[0]+(o[1]?" ("+o[1]+")":"")).join("; "))}</dd></dl>`;
  el.innerHTML = h;
}
function buscarNbs(q){""")
s=sub1(s,r"""function classificarNbs(cod){
  const e = DB.nbs[cod], idx = NBSIDX.get(cod);""",r"""function classificarNbs(cod, item){
  const e = DB.nbs[cod], idx0 = NBSIDX.get(cod);
  const doItem = (item && idx0) ? idx0.itens.filter(x=>x.i === item) : [];
  const idx = doItem.length ? {desc:idx0.desc, itens:doItem} : idx0;""")
s=sub1(s,r"""  f.tipos = (e && e.t) || "T12";
  return f;""",r"""  f.tipos = (e && e.t) || "T12";
  if (doItem.length){ f.lc = item; f.lcQtd = LCMAP.get(item).n.length; }
  else if (idx0 && idx0.itens.length > 1){ f.lcItens = idx0.itens.map(x=>x.i);
    f.avisos.push("Este NBS corresponde a mais de um item da LC 116 e as opções acima reúnem todos. Informe o item do serviço para restringir a classificação."); }
  return f;""")
s=sub1(s,r"""function selecionarCodigo(cod, manter){
  FICHA = TIPO === "produto" ? classificarNcm(cod) : classificarNbs(cod);""",r"""function selecionarCodigo(cod, manter, item){
  LCP = null;
  FICHA = TIPO === "produto" ? classificarNcm(cod) : classificarNbs(cod, item);""")
s=sub1(s,r"""  if (!f){ el.innerHTML = ""; el.className = ""; return; }""",r"""  if (!f && LCP && TIPO === "servico"){ desenharPainelLc(el); return; }
  if (!f){ el.innerHTML = ""; el.className = ""; return; }""")
s=sub1(s,r"""  h += `</dl>`;
  if (f.isNota !== undefined)""",r"""  h += `</dl>`;
  if (f.lc && f.lcQtd > 1) h += `<div style="margin-top:6px"><button type="button" class="btn" data-lcp="${f.lc}">Trocar o NBS do item ${f.lc} (${f.lcQtd} possíveis)</button></div>`;
  if (f.lcItens) h += `<div style="margin-top:6px;font-size:12px">Restringir ao item: `
    + f.lcItens.map(i=>`<button type="button" class="btn" data-lcr="${i}" title="${esc(LCMAP.get(i).d)}">${i}</button>`).join(" ") + `</div>`;
  if (f.isNota !== undefined)""")
# eventos
s=sub1(s,r"""    if (FICHA && FICHA.cod !== so){ FICHA = null; desenharFicha(); }
    const r = TIPO === "produto" ? buscarNcm(e.target.value) : buscarNbs(e.target.value), l = $("#ncm-lista");
    if (!r.length){ l.style.display="none"; return; }
    l.innerHTML = r.slice(0,30).map(([c,d])=>
      `<div data-c="${c}"><b>${TIPO==="produto"?fmtNcm(c):fmtNbs(c)}</b>${esc(d)}</div>`).join("");""",r"""    if ((FICHA && FICHA.cod !== so) || LCP){ FICHA = null; LCP = null; desenharFicha(); }
    const r = TIPO === "produto" ? buscarNcm(e.target.value) : buscarNbs(e.target.value), l = $("#ncm-lista");
    const its = TIPO === "servico" ? buscarItens(e.target.value) : [];
    if (!r.length && !its.length){ l.style.display="none"; return; }
    l.innerHTML = its.map(x=>`<div data-lc="${x.i}"><b>LC 116 ${x.i}</b>${esc(x.d.length > 110 ? x.d.slice(0,110)+"..." : x.d)}`
        + `<span style="color:#5C6E72">  ·  ${x.n.length === 1 ? "1 NBS, classifica direto" : x.n.length+" NBS possíveis"}</span></div>`).join("")
      + r.slice(0,30).map(([c,d])=>
      `<div data-c="${c}"><b>${TIPO==="produto"?fmtNcm(c):fmtNbs(c)}</b>${esc(d)}</div>`).join("");""")
s=sub1(s,r"""    const d=e.target.closest("div[data-c]"); if(!d) return;
    selecionarCodigo(d.dataset.c);""",r"""    const li=e.target.closest("div[data-lc]"); if (li){ selecionarItem(li.dataset.lc); return; }
    const d=e.target.closest("div[data-c]"); if(!d) return;
    selecionarCodigo(d.dataset.c);""")
s=sub1(s,r"""    if (e.target.name === "opc") aplicarOpcao(+e.target.value);""",r"""    if (e.target.name === "opc") aplicarOpcao(+e.target.value);
    if (e.target.name === "lcp") selecionarCodigo(e.target.value, false, LCP);""")
s=sub1(s,r"""  $("#b-consultar").addEventListener("click", consultarLote);""",r"""  $("#b-consultar").addEventListener("click", consultarLote);
  $("#ficha").addEventListener("click", e=>{
    const a = e.target.closest("button[data-lcp]"); if (a){ selecionarItem(a.dataset.lcp); return; }
    const b = e.target.closest("button[data-lcr]"); if (b && FICHA) selecionarCodigo(FICHA.cod, false, b.dataset.lcr);
  });
  $("#ficha").addEventListener("input", e=>{
    if (e.target.id !== "lcp-f") return;
    const q = semAcento(e.target.value.trim());
    $$("#ficha .lcp label").forEach(l=>{ l.style.display = !q || l.dataset.t.includes(q) ? "" : "none"; });
  });""")
s=sub1(s,r"""    if (el.id==="senha" || el.id==="ncm" || el.id==="cq") return;""",r"""    if (el.id==="senha" || el.id==="ncm" || el.id==="cq" || el.id==="lcp-f") return;""")
s=sub1(s,r"""    FICHA = null; $("#ncm").value = ""; $("#ncm-desc").textContent = "";""",r"""    FICHA = null; LCP = null; $("#ncm").value = ""; $("#ncm-desc").textContent = "";""")
s=sub1(s,r"""sv ? "NBS ou item da LC 116, por código ou descrição" :""",r"""sv ? "Código do serviço (item da LC 116 ou código de tributação nacional), NBS ou descrição" :""")
s=sub1(s,r"""sv ? "ex.: 1.2301, 04.01 ou consultoria" :""",r"""sv ? "ex.: 04.01, 040101, 1.2301 ou consultoria" :""")
# salvar e abrir com o item
s=sub1(s,r"""codigo:FICHA ? FICHA.cod : "", opcao:FICHA ? FICHA.sel : null,""",r"""codigo:FICHA ? FICHA.cod : "", lcItem:FICHA && FICHA.lc ? FICHA.lc : "", opcao:FICHA ? FICHA.sel : null,""")
s=sub1(s,r"""      if (o.codigo){ selecionarCodigo(String(o.codigo), true);""",r"""      if (o.codigo){ selecionarCodigo(String(o.codigo), true, o.lcItem || undefined);""")
# consulta em lote: item da LC 116 abre em todos os NBS possiveis
s=sub1(s,r"""  const linhas = itens.map(bruto=>{
    const d = bruto.replace(/\D/g,"");
    if (d.length !== 8 && d.length !== 9)
      return `<tr><td class="c">${esc(bruto)}</td><td colspan="7">Código inválido: use 8 dígitos para NCM ou 9 para NBS.</td></tr>`;
    const prod = d.length === 8, f = prod ? classificarNcm(d) : classificarNbs(d), o = f.opcoes[f.sel];""",r"""  const lista = [];
  for (const bruto of itens){
    const d = bruto.replace(/\D/g,""), il = (d.length !== 8 && d.length !== 9) ? itemLc(bruto) : null;
    if (!il){ lista.push([bruto, d, null]); continue; }
    const it = LCMAP.get(il.item);
    if (!it.n.length) lista.push([bruto, "", il.item]);
    for (const [cod] of it.n) lista.push([bruto, cod, il.item]);
  }
  const linhas = lista.slice(0,600).map(([bruto, d, lcI])=>{
    if (lcI && !d)
      return `<tr><td class="c">LC 116 ${esc(lcI)}</td><td colspan="7">${esc(LCMAP.get(lcI).d)} Item sem NBS correlacionado no Anexo VIII desta base.</td></tr>`;
    if (d.length !== 8 && d.length !== 9)
      return `<tr><td class="c">${esc(bruto)}</td><td colspan="7">Código inválido: use 8 dígitos para NCM, 9 para NBS ou o item da LC 116 (ex.: 04.01).</td></tr>`;
    const prod = d.length === 8, f = prod ? classificarNcm(d) : classificarNbs(d, lcI || undefined), o = f.opcoes[f.sel];""")
s=sub1(s,r"""    return `<tr><td class="c">${esc(f.fmt)}<br><button type="button" class="btn" data-sim="${d}">Simular</button></td>`""",r"""    return `<tr><td class="c">${lcI ? "LC 116 "+esc(lcI)+"<br>" : ""}${esc(f.fmt)}<br><button type="button" class="btn" data-sim="${d}" data-lc="${lcI||""}">Simular</button></td>`""")
s=sub1(s,r"""telaConsulta(false); selecionarCodigo(d);""",r"""telaConsulta(false); selecionarCodigo(d, false, b.dataset.lc || undefined);""")
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
table.cot th{text-align:left;padding-left:6px}
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
  return REG_FORN.map(([v,n])=>({nome:"", reg:v, preco, icms:(v==="mei"||v==="pf") ? 0 : icms, das:das||9.403, anexo:"I"}));
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
  const quem = x => x.nome ? `<b>${esc(x.nome)}</b> (${esc(nomeReg(x.reg))})` : `<b>${esc(nomeReg(x.reg))}</b>`;
  if (NOTA_I === null || !L.some(x=>x.i === NOTA_I)) NOTA_I = best.i;
  let h = `<h3>Custo real da compra <em>${o.ano}</em></h3>`
    + `<div class="destaque"><div class="rot">Menor custo real</div><div class="val">${BRL.format(best.custo)}</div>`
    + `<div class="cmp">${quem(best)}: nota de ${BRL.format(best.preco)}, `
    + `com ${BRL.format(best.total)} de crédito.</div></div>`;
  if (barata.custo - min > 0.005)
    h += `<p class="dica" style="color:var(--carimbo);margin:10px 0 0"><b>A nota mais barata não é a compra mais barata.</b> `
      + (barata.total < 0.005
        ? `${quem(barata)} cobra ${BRL.format(barata.preco)} e não gera crédito: custa ${BRL.format(barata.custo - min)} a mais por unidade que a melhor opção.</p>`
        : `${quem(barata)} cobra ${BRL.format(barata.preco)}, mas depois dos créditos custa ${BRL.format(barata.custo)}, ${BRL.format(barata.custo - min)} a mais por unidade.</p>`);
  h += `<table class="cmp" style="margin-top:14px"><thead><tr><th>Fornecedor</th><th>Nota</th><th>Crédito CBS e IBS</th>`
    + (colIcms ? `<th>Crédito ICMS</th>` : "") + (colPc ? `<th>Crédito PIS e COFINS</th>` : "")
    + `<th>Custo real</th><th>Preço máximo para empatar</th><th>A mais</th></tr></thead><tbody>`
    + L.map(x=>{ const eq = x.taxa < 1 ? min/(1 - x.taxa) : 0, m = Math.abs(x.custo - min) < 0.005;
        return `<tr data-i="${x.i}" class="${m?"melhor":""}${x.i===NOTA_I?" ver":""}"><td>${x.nome ? esc(x.nome)+'<br><small style="color:#5C6E72">'+esc(nomeReg(x.reg))+'</small>' : esc(nomeReg(x.reg))}</td>`
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
    R = [["Valor do "+(o.servico?"serviço":"produto")+" (com "+imp+(A.impSel>0.005?" e Imposto Seletivo embutidos)":" embutido)"), A.nf - A.cbs - A.ibs],
         ["Base do "+imp+": total da nota", A.nf, "sub"], [imp+" "+PCT(A.i), A.icms],
         A.impSel > 0.005 ? ["Base do Imposto Seletivo", base - A.impSel, "sub"] : null,
         A.impSel > 0.005 ? ["Imposto Seletivo "+PCT(o.is), A.impSel] : null,
         ["Base da CBS e do IBS: valor sem "+imp+", CBS e IBS", base, "sub"],
         ["CBS "+PCT(A.c)+" · "+classifTexto(o), A.cbs], ["IBS "+PCT(A.b), A.ibs],
         ["Total da nota: o que o cliente paga", A.nf, "tot"],
         ["Para quem compra de você", "", "sep"],
         ["Crédito de CBS e IBS do comprador do regime regular", A.cbs + A.ibs, "cr"],
         ["Custo do comprador depois desse crédito"+(o.servico ? "" : ", antes do crédito de ICMS"), A.nf - A.cbs - A.ibs, "sub"]];
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
  $("#tit-venda").textContent = MODO === "compra" ? "PIS e COFINS do item, hoje (crédito do Lucro Real em 2026)"
    : (TIPO === "servico" ? "A venda deste serviço, hoje" : "A venda deste produto, hoje");
  calcular();
}
function prepararCompra(){
  [$("#tit-compra").closest(".bloco"), $("#pv").closest(".campo"), $("#c-is"), $("#c-setor"), $("#c-simples"),
   $("#inc-lucro").closest("label"), $("#inc-lucro").closest("label").nextElementSibling,
   $("#lc224").closest("label"), $("#lc224").closest("label").nextElementSibling, $("#p-ano"), $("#p-hoje"), $("#p-forn"), $("#p-simples")]
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
s=sub1(s,"""  $("#dica-ano").textContent = ANO === 2026""","""  if (MODO === "compra") calcCompra(o);
  $("#dica-ano").textContent = ANO === 2026""")
# salvar e abrir
s=sub1(s,"""baseFiscal:DB.meta.versao, consulta:$("#cq").value,""","""baseFiscal:DB.meta.versao, consulta:$("#cq").value, modo:MODO, cotacoes:lerCot(),""")
s=sub1(s,"""      if (o.consulta){ consultarLote(); } else { $("#cq-res").innerHTML = ""; }""","""      if (o.consulta){ consultarLote(); } else { $("#cq-res").innerHTML = ""; }
      if (Array.isArray(o.cotacoes) && o.cotacoes.length) escreverCot(o.cotacoes);
      MODO = o.modo === "compra" ? "compra" : "venda"; document.body.classList.toggle("modo-compra", MODO === "compra");
      $$("#modo button").forEach(b=>b.setAttribute("aria-pressed", b.dataset.m === MODO));""")
s=sub1(s,"""    if (el.id==="senha" || el.id==="ncm" || el.id==="cq" || el.id==="lcp-f") return;""","""    if (el.id==="senha" || el.id==="ncm" || el.id==="cq" || el.id==="lcp-f" || el.closest("#cot")) return;""")


# ===== rodada 8: Simples com ICMS fora do DAS (sublimite) e limite do credito do Simples =====
s=sub1(s,"""    else if (forn === "sn_tradicional"){
      const an = P.simplesAnexos[anexoForn] || P.simplesAnexos.I;
      const parcela = an.pis + an.cofins + (an.icms + an.iss)*(1 - t.fatorIcmsIss);
      cbsIbs = pc * aliqForn * parcela;
    }""","""    else if (forn === "sn_tradicional" || forn === "sn_sublimite"){
      const an = P.simplesAnexos[anexoForn] || P.simplesAnexos.I;
      const parcela = an.pis + an.cofins + (an.icms + an.iss)*(1 - t.fatorIcmsIss);
      // Premissa conservadora: o credito vindo do DAS nao passa do que um fornecedor do regime regular
      // transferiria pelo mesmo item. Com aliquota zero ou isencao, nao ha credito.
      const a = (t.cbs + t.ibs)*(1-(trat||0)), teto = a ? pc*(1 - icmsCompra*t.fatorIcmsIss)/(1+a)*a : 0;
      cbsIbs = Math.min(pc * aliqForn * parcela, teto);
    }""")
s=sub1(s,"""<option value="sn_regular">Simples optante pelo regime regular</option>
            <option value="sn_tradicional">Simples tradicional</option>""","""<option value="sn_regular">Simples, CBS e IBS fora do DAS (ICMS no DAS)</option>
            <option value="sn_tradicional">Simples tradicional, tudo no DAS</option>
            <option value="sn_sublimite">Simples com ICMS fora do DAS (sublimite excedido)</option>""")
s=sub1(s,"""const REG_FORN = [["regular","Lucro Real ou Presumido"],["sn_regular","Simples optante pelo regime regular"],
                  ["sn_tradicional","Simples tradicional"],""","""const REG_FORN = [["regular","Lucro Real ou Presumido"],["sn_regular","Simples, CBS e IBS fora do DAS (ICMS no DAS)"],
                  ["sn_tradicional","Simples tradicional, tudo no DAS"],["sn_sublimite","Simples com ICMS fora do DAS (sublimite excedido)"],""")
s=sub1(s,"""                   ["sn_regular","Simples optante pelo regime regular"],""","""                   ["sn_regular","Simples, CBS e IBS fora do DAS"],""")
s=sub1(s,"""const ehSN = r => r === "sn_tradicional" || r === "sn_regular";""","""const ehSN = r => r === "sn_tradicional" || r === "sn_regular" || r === "sn_sublimite";""")
s=sub1(s,"""  $("#c-aliqforn").hidden = !["sn_tradicional","sn_regular"].includes($("#forn").value);""","""  $("#c-aliqforn").hidden = !["sn_tradicional","sn_regular","sn_sublimite"].includes($("#forn").value);""")
s=sub1(s,"""Comparar os 5 regimes pelo preço da 1ª linha""","""Comparar todos os regimes pelo preço da 1ª linha""")
s=sub1(s,"""  } else if (x.reg === "sn_tradicional"){
    R.push(["Valor da nota", x.preco]);
    R.push(["DAS do fornecedor dentro do preço, "+PCT(x.das/100), x.preco*x.das/100, "sub"]);""","""  } else if (x.reg === "sn_tradicional" || x.reg === "sn_sublimite"){
    R.push(["Valor da nota", x.preco]);
    if (x.reg === "sn_sublimite" && !o.servico) R.push(["ICMS destacado, apurado fora do DAS, "+PCT(icC*f), x.preco*icC*f, "sub"]);
    R.push(["DAS do fornecedor dentro do preço, "+PCT(x.das/100), x.preco*x.das/100, "sub"]);""")
s=sub1(s,"""    if (!o.servico) R.push(["Parte do DAS que corresponde a ICMS", x.base.icms, "sub"]);""","""    if (!o.servico && x.reg === "sn_tradicional") R.push(["Parte do DAS que corresponde a ICMS", x.base.icms, "sub"]);""")
s=sub1(s,"""  if (L.some(x=>ehSN(x.reg))) notas.push("Fornecedor do Simples transfere crédito limitado ao que paga no DAS: no tradicional, CBS, IBS e ICMS; no optante do regime regular, só o ICMS fica limitado (LC 214/2025, art. 47, § 9º, II; LC 123/2006, art. 23).");""","""  if (L.some(x=>ehSN(x.reg))) notas.push("Fornecedor do Simples transfere crédito limitado ao que paga no DAS (LC 214/2025, art. 47, § 9º, II; LC 123/2006, art. 23): no tradicional, CBS, IBS e ICMS; com CBS e IBS fora do DAS, só o ICMS; com ICMS fora do DAS por excesso de sublimite, só a CBS e o IBS. Premissa conservadora: o crédito vindo do DAS não passa do que um fornecedor do regime regular transferiria; com alíquota zero ou isenção, é zero.");""")


# ===== rodada 9: operacoes interestaduais (aliquota interestadual e DIFAL) na venda e na compra =====
s=sub1(s,"""        <div class="campo">
          <label for="pc-hoje">PIS e COFINS hoje nesta venda</label>""","""        <div class="campo so-venda" id="c-dest">
          <label for="uf-dest">Destino da venda</label>
          <select id="uf-dest"></select>
          <div id="c-dest2" hidden style="margin-top:9px">
            <label for="dest-tipo">Quem compra no outro estado</label>
            <select id="dest-tipo">
              <option value="contrib">Contribuinte do ICMS, para revenda ou industrialização</option>
              <option value="contrib_uso">Contribuinte do ICMS, para uso, consumo ou imobilizado</option>
              <option value="final">Consumidor final não contribuinte</option>
            </select>
            <label style="margin-top:9px"><input type="checkbox" id="importado" style="width:auto;margin-right:7px">
              Mercadoria importada ou com conteúdo de importação acima de 40%</label>
          </div>
          <p class="dica" id="dica-dest"></p>
        </div>
        <div class="campo" id="c-dupla">
          <label><input type="checkbox" id="difal-dupla" checked style="width:auto;margin-right:7px">
            DIFAL com base dupla</label>
          <p class="dica">Base dupla: o DIFAL é calculado sobre uma base que embute a alíquota interna do estado de destino, o que o torna maior. Muitos estados adotam; confirme a regra da UF.</p>
        </div>
        <div class="campo">
          <label for="pc-hoje">PIS e COFINS hoje nesta venda</label>""")
s=sub1(s,"""/* ---------- simulacao de compra: custo real por fornecedor ---------- */""",r"""/* ---------- operacoes interestaduais ---------- */
// Aliquota interna modal e FCP geral por UF em 2026 (fontes secundarias concordantes, consulta em 10/11/2026).
const UFS = {AC:[19,0,"Acre"],AL:[20.5,1,"Alagoas"],AM:[20,0,"Amazonas"],AP:[18,0,"Amapá"],BA:[20.5,0,"Bahia"],CE:[20,0,"Ceará"],
  DF:[20,0,"Distrito Federal"],ES:[17,0,"Espírito Santo"],GO:[19,0,"Goiás"],MA:[23,0,"Maranhão"],MG:[18,0,"Minas Gerais"],
  MS:[17,0,"Mato Grosso do Sul"],MT:[17,0,"Mato Grosso"],PA:[19,0,"Pará"],PB:[20,0,"Paraíba"],PE:[20.5,0,"Pernambuco"],
  PI:[22.5,0,"Piauí"],PR:[19.5,0,"Paraná"],RJ:[20,2,"Rio de Janeiro"],RN:[20,0,"Rio Grande do Norte"],RO:[19.5,0,"Rondônia"],
  RR:[20,0,"Roraima"],RS:[17,0,"Rio Grande do Sul"],SE:[19,1,"Sergipe"],SP:[18,0,"São Paulo"],TO:[20,0,"Tocantins"]};
// Saindo de SC (Sul): 7% para Norte, Nordeste, Centro-Oeste e Espirito Santo; 12% para Sul e Sudeste (Res. Senado 22/1989).
const UF7 = ["AC","AL","AM","AP","BA","CE","DF","ES","GO","MA","MS","MT","PA","PB","PE","PI","RN","RO","RR","SE","TO"];
function difalTaxa(inter, carga, dupla){
  // DIFAL como fracao do valor da operacao. Base unica: carga - inter. Base dupla: base embute a carga do destino.
  const d = dupla ? (1 - inter)*carga/(1 - carga) - inter : carga - inter;
  return Math.max(0, d);
}
function vendaICMS(){
  const uf = $("#uf-dest").value || "SC", fora = TIPO === "produto" && uf !== "SC";
  if (!fora) return {icmsVenda:num("icms-venda")/100, icmsInter:0, difal:0, ufDest:"SC", fora:false};
  const inter = $("#importado").checked ? 0.04 : (UF7.includes(uf) ? 0.07 : 0.12), d = UFS[uf], carga = (d[0] + d[1])/100;
  const difal = $("#dest-tipo").value === "final" ? difalTaxa(inter, carga, $("#difal-dupla").checked) : 0;
  return {icmsVenda:inter + difal, icmsInter:inter, difal, ufDest:uf, fora:true, cargaDest:carga};
}
function textoDestino(){
  const v = vendaICMS(), el = $("#dica-dest");
  if (!v.fora){ el.textContent = TIPO === "servico" ? "Serviço: o ISS segue a regra do município; o destino não muda o cálculo aqui." : "Venda interna: vale a alíquota de ICMS de SC informada em Sua empresa."; return; }
  const d = UFS[v.ufDest], tipo = $("#dest-tipo").value;
  el.textContent = "Alíquota interestadual de " + PCT(v.icmsInter) + ($("#importado").checked ? " (Resolução do Senado 13/2012)" : " (Resolução do Senado 22/1989)") + ". "
    + (tipo === "final" ? "Consumidor final não contribuinte: você recolhe o DIFAL para " + d[2] + ", interna de " + PCT(d[0]/100) + (d[1] ? " mais " + PCT(d[1]/100) + " de FCP" : "") + " menos a interestadual, " + PCT(v.difal) + " sobre o valor da nota (EC 87/2015 e LC 190/2022)."
      : tipo === "contrib_uso" ? "O DIFAL do uso e consumo é recolhido pelo comprador, não entra no seu preço."
      : "Para revenda, não há DIFAL na sua nota. Pode haver substituição tributária por protocolo ou convênio, que não é simulada.")
    + ($("#regime").value === "simples" ? " No Simples, a venda usa o DAS: o DIFAL da venda a consumidor final de outro estado não é somado aqui, porque a cobrança do optante é controvertida (STF, ADI 5464). Confira com a Amcont." : "")
    + " Alíquota interna da UF pela modal de 2026, de fonte secundária; produtos podem ter alíquota ou FCP próprios no destino.";
}
/* ---------- simulacao de compra: custo real por fornecedor ---------- */""")
s=sub1(s,"""    icmsVenda:num("icms-venda")/100, icmsCompra:""","""    ...vendaICMS(), icmsSC:num("icms-venda")/100, difalDupla:$("#difal-dupla").checked, icmsCompra:""")
# iniciar: preencher UFs e eventos
s=sub1(s,"""function iniciar(){
  prepararCompra();""","""function iniciar(){
  $("#uf-dest").innerHTML = `<option value="SC">Dentro de Santa Catarina</option>`
    + Object.keys(UFS).sort().map(u=>`<option value="${u}">${UFS[u][2]} (${u}), interestadual de ${UF7.includes(u)?"7%":"12%"}</option>`).join("");
  ["#uf-dest","#dest-tipo","#importado","#difal-dupla"].forEach(id=>$(id).addEventListener("change", ()=>{ sincronizar(); calcular(); }));
  prepararCompra();""")
s=sub1(s,"""  const sv = TIPO === "servico";
  $("#c-is").hidden = sv; $("#c-icms-compra").hidden = sv;""","""  const sv = TIPO === "servico";
  $("#c-is").hidden = sv; $("#c-icms-compra").hidden = sv;
  const foraV = !sv && $("#uf-dest").value !== "SC";
  $("#c-dest").hidden = sv; $("#c-dest2").hidden = !foraV;
  $("#icms-venda").disabled = foraV && MODO === "venda";
  textoDestino();""")
# nota da venda: separar ICMS interestadual e DIFAL
s=sub1(s,"""         ["Base do "+imp+": total da nota", A.nf, "sub"], [imp+" "+PCT(A.i), A.icms],""","""         ["Base do "+imp+": total da nota", A.nf, "sub"],
         ...(o.fora ? [["ICMS interestadual "+PCT(o.icmsInter*tAno(o.ano).fatorIcmsIss)+", SC para "+o.ufDest, A.nf*o.icmsInter*tAno(o.ano).fatorIcmsIss],
                       o.difal > 0 ? ["DIFAL para "+o.ufDest+", recolhido por você", A.nf*o.difal*tAno(o.ano).fatorIcmsIss] : null]
                    : [[imp+" "+PCT(A.i), A.icms]]),""")
# compra: coluna fora de SC e DIFAL do uso, consumo e imobilizado
s=sub1(s,"""    + `<td><select data-k="anexo"${sn?"":" disabled"}>""","""    + `<td style="text-align:center"><input data-k="fora" type="checkbox" style="width:auto"${c.fora?" checked":""}></td>`
    + `<td><select data-k="anexo"${sn?"":" disabled"}>""")
s=sub1(s,"""<th>DAS %</th><th>Anexo</th><th></th>""","""<th>DAS %</th><th title="Fornecedor de outro estado">Fora de SC</th><th>Anexo</th><th></th>""")
s=sub1(s,"""            das:numTxt(g("das").value), anexo:g("anexo").value}; });""","""            das:numTxt(g("das").value), anexo:g("anexo").value, fora:g("fora").checked}; });""")
s=sub1(s,"""  const total = cbsIbs + icms + pc;
  return {cbsIbs, icms, pc, total, custo:c.preco - total, taxa:c.preco > 0 ? total/c.preco : 0, base};""","""  const total = cbsIbs + icms + pc;
  // DIFAL de SC na entrada de outro estado para uso, consumo ou imobilizado (pago pelo comprador, inclusive no Simples)
  const difal = (c.fora && !o.servico && o.destino !== "revenda")
    ? c.preco * difalTaxa(icmsC, o.icmsSC, o.difalDupla) * tAno(o.ano).fatorIcmsIss : 0;
  return {cbsIbs, icms, pc, total, difal, custo:c.preco - total + difal, taxa:c.preco > 0 ? (total - difal)/c.preco : 0, base};""")
s=sub1(s,"""  const colIcms = !sv && o.regime !== "simples" && o.destino !== "uso";""","""  const colIcms = !sv && o.regime !== "simples" && o.destino !== "uso";
  const colDif = L.some(x=>x.difal > 0.005);""")
s=sub1(s,"""    + (colIcms ? `<th>Crédito ICMS</th>` : "") + (colPc ? `<th>Crédito PIS e COFINS</th>` : "")""","""    + (colIcms ? `<th>Crédito ICMS</th>` : "") + (colPc ? `<th>Crédito PIS e COFINS</th>` : "") + (colDif ? `<th>DIFAL a pagar</th>` : "")""")
s=sub1(s,"""          + (colIcms ? `<td>${BRL.format(x.icms)}</td>` : "") + (colPc ? `<td>${BRL.format(x.pc)}</td>` : "")""","""          + (colIcms ? `<td>${BRL.format(x.icms)}</td>` : "") + (colPc ? `<td>${BRL.format(x.pc)}</td>` : "")
          + (colDif ? `<td class="neg">${BRL.format(x.difal)}</td>` : "")""")
s=sub1(s,"""  if (L.some(x=>x.reg === "pf")) notas.push(""","""  if (L.some(x=>x.fora) && !sv) notas.push(o.destino === "revenda"
    ? "Compra de outro estado para revenda: o crédito é o ICMS destacado (em geral 12%, ou 4% se importado). Antecipação ou substituição tributária na entrada não são simuladas."
    : "Compra de outro estado para uso, consumo ou imobilizado: você paga a SC o DIFAL, alíquota interna do item em SC ("+PCT(o.icmsSC)+") menos a destacada, "+(o.difalDupla ? "com base dupla" : "com base única")+". O DIFAL entra no custo.");
  if (L.some(x=>x.reg === "pf")) notas.push(""")
s=sub1(s,"""  if (x.pc > 0.005) R.push(["Crédito de PIS e COFINS", x.pc, "cr"]);""","""  if (x.pc > 0.005) R.push(["Crédito de PIS e COFINS", x.pc, "cr"]);
  if (x.difal > 0.005) R.push(["DIFAL pago a SC na entrada", -x.difal, "sub"]);""")
s=sub1(s,"""  $('label[for="trat"]').textContent = MODO === "compra" ? "Tratamento de CBS e IBS do item comprado" : "Tratamento de CBS e IBS na venda";""","""  $('label[for="trat"]').textContent = MODO === "compra" ? "Tratamento de CBS e IBS do item comprado" : "Tratamento de CBS e IBS na venda";
  sincronizar();""")
s=sub1(s,"""  $("#lb-icms-venda").textContent = sv ? "Alíquota de ISS na sua venda (%)" : "Alíquota de ICMS na sua venda (%)";""","""  $("#lb-icms-venda").textContent = MODO === "compra" ? "Alíquota interna de ICMS do item em SC (%), para o DIFAL"
    : (sv ? "Alíquota de ISS na sua venda (%)" : "Alíquota de ICMS na sua venda (%)");""")


# ===== rodada 10: frutas da posicao 08.11 com acucar e rotulo de posicao excluida =====
s=sub1(s,"""  return f;
}
const REG_ESPECIFICO""","""  for (const o of f.opcoes)
    if (o.red === 0 && o.ccl === "000001" && /^Anexo/.test(o.rot))
      o.rot = /^Anexo XVII/.test(o.rot) ? "Sujeito ao Imposto Seletivo (" + o.rot + "): CBS e IBS integrais"
                                       : "Excluída do benefício (" + o.rot + "): tributação integral";
  if (/^90221[34]/.test(cod)){
    const iz = f.opcoes.findIndex(o=>/Anexo XII, item 7/.test(o.rot)), ii = f.opcoes.findIndex(o=>o.ccl === "000001");
    if (iz >= 0 && ii >= 0){
      f.opcoes[iz].rot += " (código fora do listado na lei)"; f.sel = ii;
      f.avisos.push("O Anexo XII, item 7 (aparelho de raio X móvel), lista só o código 9022.19 da NCM, e o art. 144, I, exige a classificação indicada no anexo. Na leitura literal este código fica fora do item: a simulação usa tributação integral. Alíquota zero só com parecer que sustente o enquadramento.");
    }
  }
  if (cod.startsWith("0811"))
    f.avisos.push("Fruta congelada com açúcar ou outro edulcorante adicionado (Ex 01 da TIPI) não tem alíquota zero (Anexo XV, item 3) nem redução de 60% (Anexo VII, item 14): os dois itens exigem produto sem adição de açúcar. Nesse caso, marque Alíquota integral.");
  return f;
}
const REG_ESPECIFICO""")

# ===== rodada 11: validade da legislacao conferida =====
from validade_js import VALIDADE_JS
s=sub1(s,"</body>",VALIDADE_JS+"\n</body>")
# ===== rodada 12: integracao da auditoria independente (10/11/2026) =====
# F02: cClassTrib composto vira codigo principal + alternativas a confirmar
s=sub1(s,"""/* ---------- simulacao de compra: custo real por fornecedor ---------- */""",r"""/* ---------- cClassTrib composto: codigo principal e alternativas (auditoria F02) ---------- */
function normCcl(f){
  if (!f || !f.opcoes) return f;
  let alt = null;
  for (const o of f.opcoes){
    if (o.ccl && !/^\d{6}$/.test(o.ccl)){
      const m = String(o.ccl).match(/\d{6}/g);
      o.cclTexto = o.ccl; o.ccl = m ? m[0] : o.ccl; o.cclConfirmar = true;
      o.cond = (o.cond ? o.cond + " " : "") + "cClassTrib a confirmar: " + o.cclTexto + ".";
      if (!alt) alt = o;
    }
  }
  if (alt) f.avisos.push("Há mais de um cClassTrib possível para esta classificação (" + alt.cclTexto + "). A ferramenta usa o principal, " + alt.ccl + ", só para simular. Confirme o código com a Amcont antes de emitir a nota.");
  return f;
}
/* ---------- simulacao de compra: custo real por fornecedor ---------- */""")
s=sub1(s,"""function classifTexto(o){
  const x = FICHA && FICHA.opcoes[FICHA.sel];
  if (x && Math.abs(x.red - o.trat) < 1e-9) return "CST "+x.cst+" · cClassTrib "+x.ccl;""","""function classifTexto(o){
  const x = FICHA && FICHA.opcoes[FICHA.sel];
  if (x && Math.abs(x.red - o.trat) < 1e-9) return "CST "+x.cst+" · cClassTrib "+x.ccl+(x.cclConfirmar ? " (confirmar)" : "");""")
s=sub1(s,"""function iniciar(){""","""{ const _cN = classificarNcm, _cB = classificarNbs;
  classificarNcm = function(c){ return normCcl(_cN(c)); };
  classificarNbs = function(c, it){ return normCcl(_cB(c, it)); }; }
function iniciar(){""")

# F01 e C5: credito estimado x prudencial; PIS/COFINS sem ICMS na base quando o ICMS e destacado (regular e sublimite)
s=sub1(s,"""    ? pc * (1 - (forn === "regular" ? o.icmsCompra : 0)) * (o.pis + o.cofins) : 0;""","""    ? pc * (1 - ((forn === "regular" || forn === "sn_sublimite") ? o.icmsCompra : 0)) * (o.pis + o.cofins) : 0;""")
s=sub1(s,"""<button type="button" class="btn" id="b-cot-5">Comparar todos os regimes pelo preço da 1ª linha</button>
        </div>""","""<button type="button" class="btn" id="b-cot-5">Comparar todos os regimes pelo preço da 1ª linha</button>
        </div>
        <label style="margin-top:10px"><input type="checkbox" id="cred-prud" style="width:auto;margin-right:7px">
          Cenário prudencial: comparar sem crédito (nota sem destaque válido ou débito do fornecedor não pago)</label>""")
s=sub1(s,"""  const L = lerCot().map((c,i)=>Object.assign({i}, c, creditoComprador(c, o))).filter(x=>x.preco > 0);
  if (!L.length){""","""  const prud = $("#cred-prud").checked;
  const L = lerCot().map((c,i)=>{ const k = creditoComprador(c, o), semCred = c.preco + k.difal;
      return Object.assign({i}, c, k, {semCred}, prud ? {custo:semCred, taxa:c.preco > 0 ? -k.difal/c.preco : 0} : {}); })
    .filter(x=>x.preco > 0);
  if (!L.length){""")
s=sub1(s,"""    + `<th>Custo real</th><th>Preço máximo para empatar</th><th>A mais</th></tr></thead><tbody>`""","""    + `<th>${prud ? "Custo sem crédito" : "Custo real"}</th>${prud ? "" : "<th>Sem crédito</th>"}<th>Preço máximo para empatar</th><th>A mais</th></tr></thead><tbody>`""")
s=sub1(s,"""          + `<td><b>${BRL.format(x.custo)}</b></td><td>${m ? "" : BRL.format(eq)}</td>`""","""          + `<td><b>${BRL.format(x.custo)}</b></td>${prud ? "" : `<td>${BRL.format(x.semCred)}</td>`}<td>${m ? "" : BRL.format(eq)}</td>`""")
s=sub1(s,"""  notas.push("Preço máximo para empatar: o valor de nota""","""  notas.push(prud ? "Cenário prudencial: os créditos não são considerados, e a comparação usa o valor da nota mais o DIFAL."
    : "Os créditos são estimativas: só podem ser apropriados com documento fiscal idôneo e depois que o débito do fornecedor for extinto (LC 214/2025, art. 47, caput, § 1º, II, e § 2º, I). A coluna Sem crédito mostra o custo se o crédito não vier.");
  notas.push("Preço máximo para empatar: o valor de nota""")
s=sub1(s,"""  ["#uf-dest","#dest-tipo","#importado","#difal-dupla"].forEach(""","""  $("#cred-prud").addEventListener("change", calcular);
  ["#uf-dest","#dest-tipo","#importado","#difal-dupla"].forEach(""")
s=sub1(s,"""         ["Crédito de CBS e IBS do comprador do regime regular", A.cbs + A.ibs, "cr"],""","""         ["Crédito estimado de CBS e IBS do comprador do regime regular", A.cbs + A.ibs, "cr"],""")

# F04 e F10 e F01 na venda: projecao, sensibilidade, cenario sem credito e alcance da margem
s=sub1(s,"""  desenharNotaVenda(o, A);
  /* --- comparador de fornecedores --- */""","""  if (A.tipo === "geral" && ANO >= 2027){
    const T = P.transicao, ex = [];
    P.transicao = T.map(x=>x.ano === ANO ? Object.assign({}, x, {cbs:x.cbs + 0.005, ibs:x.ibs + 0.005}) : x);
    let S1; try { S1 = noAno(o, H.mc, o.pcAno, o.forn, o.aliqForn, o.anexoForn); } finally { P.transicao = T; }
    const S2 = noAno(o, H.mc, o.pcAno, "pf", o.aliqForn, o.anexoForn);
    const tA = tAno(ANO);
    ex.push(`<b>Projeção.</b> ${ANO} usa CBS de ${PCT(tA.cbs)} e IBS de ${PCT(tA.ibs)}, alíquotas de referência ainda provisórias: o resultado é simulação, não o imposto devido.`);
    ex.push(`Se a alíquota de referência (CBS mais IBS) for 1 ponto maior, o preço necessário passa a <b>${BRL.format(S1.nf)}</b> (${BRL.format(S1.nf - A.nf)} a mais).`);
    if (A.cred.total > 0.005) ex.push(`Se o crédito da compra não for aproveitado, o preço necessário passa a <b>${BRL.format(S2.nf)}</b>.`);
    ex.push("O preço mantém a margem de contribuição por unidade de hoje. Despesas fixas, volume, comissões e frete não entram: para o resultado da empresa, use a calculadora de empresa.");
    $("#p-ano").insertAdjacentHTML("beforeend", `<p class="dica" style="margin-top:9px">${ex.join(" ")}</p>`);
  }
  /* F06: beneficio de ICMS de SC com fim em 31/12/2026 aplicado em ano posterior */
  if (FICHA && FICHA.sc && TIPO === "produto" && vendaICMS().fora === false){
    const cur = num("icms-venda")/100, sel = FICHA.sc.ops.find(x=>Math.abs(x.aliq - cur) < 1e-9);
    if (sel && sel.fim && ANO > sel.fim && !FICHA.sc.ops.some(x=>!x.fim && Math.abs(x.aliq - cur) < 1e-9)){
      const alt = FICHA.sc.ops.find(x=>!x.fim);
      $("#p-ano").insertAdjacentHTML("beforeend", `<p class="dica" style="margin-top:9px;color:var(--carimbo)"><b>Benefício vencido.</b> A alíquota de ICMS de ${PCT(cur)} vem de benefício que vale até 31/12/${sel.fim}. Sem prorrogação, em ${ANO} a alíquota é ${alt ? PCT(alt.aliq) : "a geral"}.`
        + (alt ? ` <button type="button" class="btn" data-icms-alt="${alt.aliq*100}">Usar ${PCT(alt.aliq)}</button>` : "") + `</p>`);
    }
  }
  desenharNotaVenda(o, A);
  /* --- comparador de fornecedores --- */""")
s=sub1(s,"""  $("#cred-prud").addEventListener("change", calcular);""","""  $("#cred-prud").addEventListener("change", calcular);
  $("#p-ano").addEventListener("click", e=>{ const b = e.target.closest("[data-icms-alt]"); if (b){ $("#icms-venda").value = b.dataset.icmsAlt; calcular(); } });""")
# F09: Imposto Seletivo
s=sub1(s,"""    f.isNota = is ? is[2] : "Bem do Anexo XVII, sujeito ao Imposto Seletivo. Informe a alíquota.";""","""    f.isNota = (is ? is[2] : "Bem do Anexo XVII, sujeito ao Imposto Seletivo. Informe a alíquota.")
      + " Fonte: MP 1.399/2026, Anexos IV e V, texto oficial conferido em 10/11/2026 (alíquota inicial da TIPI vezes o fator de conversão). Efeitos a partir de 02/02/2027 e só até a lei prevista no art. 15 da MP: de 2028 em diante, a ferramenta repete a alíquota de 2027 como projeção. A MP ainda pode mudar na conversão em lei.";""")
# F03: Anexo VIII
s=sub1(s,"""O Anexo VIII da NFS-e Nacional admite ${it.n.length} códigos NBS para este item.""","""O Anexo VIII da NFS-e Nacional (versão 1.02.00, de 26/10/2026, ainda preliminar e sem regras de negócio) admite ${it.n.length} códigos NBS para este item.""")

# ===== rodada 16: ICMS de SC fixado pelo NCM (R16-03) =====
s=sub1(s,"""  FICHA.sc = (TIPO === "produto" && FICHA.cor !== "cinza") ? icmsSC(cod) : null;
""","""  FICHA.sc = (TIPO === "produto" && FICHA.cor !== "cinza") ? icmsSC(cod) : null;
  // alíquota de SC definida só pelo NCM (12% da lista ou 25%): já entra no campo, para não vender com 17% por engano
  if (FICHA.sc && FICHA.sc.fixa){ FICHA.scSel = 0; $("#icms-venda").value = +(FICHA.sc.ops[0].aliq*100).toFixed(2); }
""")
exec(open('src/round17.py',encoding='utf-8').read())
exec(open('src/round18.py',encoding='utf-8').read())
exec(open('src/round20.py',encoding='utf-8').read())
exec(open('src/round23.py',encoding='utf-8').read())
exec(open('src/round24.py',encoding='utf-8').read())
exec(open('src/round25.py',encoding='utf-8').read())
exec(open('src/round26.py',encoding='utf-8').read())
exec(open('src/round27.py',encoding='utf-8').read())
exec(open('src/round28.py',encoding='utf-8').read())
exec(open('src/round29.py',encoding='utf-8').read())
exec(open('src/round30.py',encoding='utf-8').read())
exec(open('src/round31.py',encoding='utf-8').read())
exec(open('src/round32.py',encoding='utf-8').read())
# ===== logotipo da Amcont =====
_logo=open('logo_b64.txt').read()
_img='<img class="%s" alt="Amcont Assessoria e Contabilidade" src="data:image/png;base64,'+_logo+'">'
s=sub1(s,'<div class="gate-mark">Amcont</div>',_img%'logo-gate')
s=sub1(s,'<span class="mark">AMCONT</span>',_img%'logo-hd')
s=sub1(s,'</style>','.logo-gate{display:block;height:58px;margin-bottom:18px;filter:brightness(0) invert(1)}\n.logo-hd{height:32px;align-self:center;filter:brightness(0) invert(1)}\n@media print{header{background:#fff!important;color:#10242A!important;border-bottom:2px solid #2A5F6B}.logo-hd{filter:none}header .sub,header .lei{color:#2A5F6B!important}}\n</style>')
import sys; sys.path.insert(0,'src'); from favicon import com_favicon
open('amcont-produto.html','w',encoding='utf-8').write(com_favicon(s))
print('ok',len(s))
