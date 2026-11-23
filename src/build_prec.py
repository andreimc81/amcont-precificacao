import sys; sys.path.insert(0,'src')
import re
def sub1(s,old,new,n=1):
    c=s.count(old); assert c==n,(c,old[:60]); return s.replace(old,new)
for src,dst in [('prec_orig.html','amcont-precificacao.html'),('cli_orig.html','amcont-cliente.html')]:
    s=open(src,encoding='utf-8').read()
    s=sub1(s,'"cbs": 0.092','"cbs": 0.112',2); s=sub1(s,'"cbs": 0.093','"cbs": 0.113',5)
    s=sub1(s,'"versaoDados": "2026.1"','"versaoDados": "'+__import__('json').load(open('monitor/versao.json'))['base']+'.'+str(__import__('json').load(open('monitor/versao.json'))['seq'])+'"'); s=sub1(s,'"atualizadoEm": "2026-08-13"','"atualizadoEm": "2026-11-10"')
    s=sub1(s,'"fonte": "EC 132/2023; LC 214/2025; LC 227/2026; Lei 9.249/1995; Lei 14.592/2023"',
     '"fonte": "EC 132/2023; LC 214/2025; LC 227/2026; LC 235/2026; Acórdão TCU 2933/2026; Lei 9.249/1995; Lei 14.592/2023"')
    s=sub1(s,'"avisoLegal": "As aliquotas de CBS e IBS sao estimativas divulgadas pelo governo e nao texto legal. Confira contra a norma vigente antes de usar com cliente."',
     '"avisoLegal": "CBS provisória: 11,3% calculados pelo TCU (11,2% em 2027 e 2028), aguardando resolução do Senado. IBS de referência ainda é estimativa. Confira contra a norma vigente antes de usar com cliente."')
    s=sub1(s,'''"redSaida": 0.6,
   "dica": "Transporte de passageiros tem presunção de 16% para IRPJ e 12% para CSLL."''','''"redSaida": 0.4,
   "dica": "Transporte intermunicipal e interestadual de passageiros: redução de 40% (LC 214, art. 286). Presunção de 16% para IRPJ e 12% para CSLL. O transporte urbano e metropolitano é isento e não deve ser simulado aqui."''')
    s=sub1(s,'<li>As alíquotas de CBS e IBS ainda são estimativas divulgadas pelo governo e podem mudar até a vigência.</li>',
     '<li>A CBS é provisória: 11,3% calculados pelo TCU (11,2% em 2027 e 2028), aguardando resolução do Senado. O IBS de referência ainda é estimativa.</li>')
    s=sub1(s,'''  if (salvo) PARAM = Object.assign(clonar(PADRAO), JSON.parse(salvo));''','''  // Ajuste local gravado em versao anterior dos dados e descartado, para nao esconder aliquotas atualizadas.
  if (salvo){
    const aj = JSON.parse(salvo);
    if (aj && aj.versaoDados === PADRAO.versaoDados) PARAM = Object.assign(clonar(PADRAO), aj);
    else localStorage.removeItem(CHAVE + "parametros");
  }''')

    s=sub1(s,'''              <option value="0.3">Redução de 30%</option>
              <option value="0.6">Redução de 60% (saúde, educação, alimentos e outros)</option>
              <option value="0.7">Redução de 70%</option>
            </select>''','''              <option value="0.3">Redução de 30% (profissões regulamentadas)</option>
              <option value="0.4">Redução de 40% (bares, hotelaria, transporte intermunicipal)</option>
              <option value="0.5">Redução de 50% (operações com imóveis)</option>
              <option value="0.6">Redução de 60% (saúde, educação, alimentos e outros)</option>
              <option value="0.7">Redução de 70%</option>
              <option value="0.8">Redução de 80%</option>
              <option value="1">Alíquota zero (cesta básica e outros), mantém os créditos</option>
              <option value="isento">Isenção ou imunidade, sem crédito das entradas</option>
            </select>
            <p class="dica" id="dica-reducao"></p>''')
    s=sub1(s,'''    redSaida:parseFloat($("#reducao").value),''','''    redSaida:$("#reducao").value === "isento" ? 1 : (parseFloat($("#reducao").value) || 0),''')
    # isencao e imunidade: anula o credito de CBS e IBS das entradas; aliquota zero e reducao mantem
    s=sub1(s,'''    gastos:coletarGastos(), baseImp''','''    gastos:coletarGastos().map(g => $("#reducao").value === "isento" ? Object.assign({}, g, {red:1}) : g), baseImp''')
    s=sub1(s,'''function rodar(premissa){''','''function dicaReducao(){
  const v = $("#reducao").value, d = $("#dica-reducao"); if (!d) return;
  d.textContent = v === "isento"
    ? "Venda isenta ou imune não gera débito de CBS e IBS e anula o crédito das entradas vinculadas. A simulação zera esses créditos. Exportação é exceção e mantém o crédito."
    : (v === "1" ? "Alíquota zero não gera débito de CBS e IBS e mantém o crédito das entradas, que pode ser ressarcido."
       : (parseFloat(v) > 0 ? "A redução de alíquota mantém o crédito integral das entradas. Confirme se a operação atende à condição da lei." : ""));
}
document.addEventListener("change", e => { if (e.target && e.target.id === "reducao") dicaReducao(); });
function rodar(premissa){
  dicaReducao();''')
    if 'cli' in src: s=sub1(s,'CONTATO: "https://wa.me/5500000000000"','CONTATO: "https://wa.me/5548998266207"')

    from senha_js import SENHA_JS
    s=sub1(s,'''let HASH_ALVO = null;''',SENHA_JS+'''let HASH_ALVO = null;''')
    s=sub1(s,'''  if (h === alvo) {
    document.getElementById("gate").remove();
    document.getElementById("app").hidden = false;
    calcular(true);''','''  if (await senhaConfere(h, alvo)) {
    document.getElementById("gate").remove();
    document.getElementById("app").hidden = false;
    calcular(true); montarTrocaSenha();''')

    s=sub1(s,'"premissaPadrao": "prof"','"premissaPadrao": "lc"')
    s=sub1(s,'<option value="prof">Compõem a base (leitura mais conservadora)</option>','<option value="prof">CBS e IBS dentro da própria base (modelo do curso, não é o texto da lei)</option>')
    s=sub1(s,'<option value="prof">Compõem a base do ICMS e do ISS (leitura conservadora)</option>','<option value="prof">CBS e IBS dentro da própria base (modelo do curso, não é o texto da lei)</option>')
    s=sub1(s,'<option value="lc">Excluir CBS e IBS da própria base (LC 214, art. 12)</option>','<option value="lc">Texto da lei: fora da própria base (LC 214, art. 12) e dentro da base do ICMS e do ISS</option>',2)
    s=sub1(s,'<option value="plp">Não compõem a base do ICMS e do ISS (PLP 16/2025)</option>','<option value="plp">Fora também da base do ICMS e do ISS (PLP 16/2025 e tese do contribuinte)</option>',2)
    s=sub1(s,'Conferido contra 66 pontos de\n   controle dos casos práticos de referência.','A premissa "prof" reproduz o material de referência;\n   o padrão é a premissa "lc", que segue o art. 12 da LC 214/2025.')

    # ===== rodada 3: credito sem ICMS na base, rampa do credito de ICMS, LC 224 =====
    FB = """  // A base da CBS e do IBS das entradas nao contem o ICMS destacado (LC 214, art. 12, par. 2, V).
  // O ICMS das entradas e rateado sobre os gastos que geram credito.
  { const icmsEnt = o.nomeImp === "ICMS" ? o.baseImp*o.imposto*a.fator : 0;
    const tot = o.gastos.filter(g => g.red < 1).reduce((s,g) => s+g.valor, 0);
    const fb = tot > 0 ? Math.max(0, 1 - icmsEnt/tot) : 1;
    credC *= fb; credB *= fb; }
"""
    s=sub1(s,"  const cred = credC + credB;\n", FB+"  const cred = credC + credB;\n")
    s=sub1(s,"  const credV = credC + credB;\n", FB+"  const credV = credC + credB;\n")
    s=sub1(s,"""  const impC   = o.nomeImp === "ICMS" ? o.baseImp*iAtual : 0;""","""  const impC   = o.nomeImp === "ICMS" ? o.baseImp*iAtual : 0;
  // No ano de referencia o ICMS das entradas segue a mesma rampa do ICMS das saidas (LC 87/1996, art. 31-A).
  const impCano = impC*a.fator;""")
    s=sub1(s,"  const base0 = liqAntes - impC + (o.ipi ? ipiC : 0) - cred;","  const base0 = liqAntes - impCano + (o.ipi ? ipiC : 0) - cred;")
    s=sub1(s,"  const tribApos = cbsRec+ibsRec+(impD-impC)+irpj+adic+csll;","  const tribApos = cbsRec+ibsRec+(impD-impCano)+irpj+adic+csll;")
    s=sub1(s,"          cbs:s.cbsD, ibs:s.ibsD, cbsRec, ibsRec, icms:impD-impC, irpj, csll, adic,","          cbs:s.cbsD, ibs:s.ibsD, cbsRec, ibsRec, icms:impD-impCano, irpj, csll, adic,")
    s=sub1(s,'            ano:[["CBS",s.cbsD,credC],["IBS",s.ibsD,credB],[o.nomeImp,impD,impC],','            ano:[["CBS",s.cbsD,credC],["IBS",s.ibsD,credB],[o.nomeImp,impD,impCano],')
    s=sub1(s,"""  $("#c-bimp").hidden         = simples;
  $("#lb-bimp").textContent   = "Do total acima, quanto gera crédito de "
    + (ATIV[setor].imp === "ISS" ? "ISS (o ISS é cumulativo e não gera)" : "ICMS");
  $("#c-imposto").hidden      = simples;""","""  $("#c-bimp").hidden         = false;
  $("#lb-bimp").textContent   = simples ? "Do total acima, quanto veio com ICMS destacado na nota"
    : "Do total acima, quanto gera crédito de " + (ATIV[setor].imp === "ISS" ? "ISS (o ISS é cumulativo e não gera)" : "ICMS");
  $("#c-imposto").hidden      = false;""")
    s=sub1(s,"""  $("#lb-imposto").textContent = at.imp === "ISS"
    ? "Alíquota de ISS nos seus serviços" : "Alíquota de ICMS nas suas vendas";""","""  $("#lb-imposto").textContent = simples ? "Alíquota de ICMS nas notas de compra"
    : (at.imp === "ISS" ? "Alíquota de ISS nos seus serviços" : "Alíquota de ICMS nas suas vendas");""")
    s=sub1(s,"""  "limiteAdicional": 240000,
  "aliqAdicional": 0.1
 },""","""  "limiteAdicional": 240000,
  "aliqAdicional": 0.1,
  "limitePresuncao": 5000000,
  "acrescimoPresuncao": 0.1
 },""")
    s=sub1(s,"""    presIrpj:num("p-irpj")/100, presCsll:num("p-csll")/100,""","""    // LC 224/2025: acrescimo de 10% na presuncao sobre a receita que excede R$ 5 milhoes no ano
    presIrpj:num("p-irpj")/100*fatorLC224(), presCsll:num("p-csll")/100*fatorLC224(),""")
    s=sub1(s,"""function opcoes(premissa){""","""function fatorLC224(){
  const R = num("receita"), L = AL().limitePresuncao || 0, A = AL().acrescimoPresuncao || 0;
  return (L > 0 && R > L) ? 1 + A*(R-L)/R : 1;
}
function opcoes(premissa){""")
    s=sub1(s,'<li>A CBS é provisória:','<li>Receita anual acima de R$ 5 milhões no Lucro Presumido: a presunção recebe o acréscimo de 10% da LC 224/2025 sobre a parcela excedente. Há decisões judiciais suspendendo a regra.</li>\n      <li>O crédito de CBS e IBS das entradas é calculado sem o ICMS destacado na base, e o crédito de ICMS acompanha a redução do imposto de 2029 a 2032.</li>\n      <li>A CBS é provisória:')

    # ===== rodada 4: parcela da receita sem PIS e COFINS hoje =====
    s=sub1(s,"""          <input id="receita" type="number" step="0.01" value="3100000">
        </div>""","""          <input id="receita" type="number" step="0.01" value="3100000">
        </div>
        <div class="campo" id="c-sempc">
          <label for="sem-pc">Parte da receita sem PIS e COFINS hoje (%)</label>
          <input id="sem-pc" type="number" step="0.1" value="0">
          <p class="dica">Revenda de produto monofásico (medicamentos, perfumaria, autopeças, pneus, bebidas frias, combustíveis), alíquota zero (cesta básica, hortifrúti) ou isento. Essa parcela não paga PIS e COFINS hoje nem gera crédito, e passa a pagar CBS em 2027.</p>
        </div>""")
    s=sub1(s,"""  const pisD = real ? (o.receita-o.receita*iAtual)*RA().pisNaoCumulativo : o.receita*o.pis;
  const cofD = real ? (o.receita-o.receita*iAtual)*RA().cofinsNaoCumulativo : o.receita*o.cofins;
  const bcPC = real ? o.gastos.filter(g=>g.pc).reduce((s,g)=>s+g.valor,0)*(1-iAtual) : 0;""","""  const comPC = 1 - Math.min(1, Math.max(0, o.semPc || 0));
  const pisD = comPC*(real ? (o.receita-o.receita*iAtual)*RA().pisNaoCumulativo : o.receita*o.pis);
  const cofD = comPC*(real ? (o.receita-o.receita*iAtual)*RA().cofinsNaoCumulativo : o.receita*o.cofins);
  const bcPC = comPC*(real ? o.gastos.filter(g=>g.pc).reduce((s,g)=>s+g.valor,0)*(1-iAtual) : 0);""")
    s=sub1(s,"""    regime:reg, receita:num("receita"),""","""    regime:reg, receita:num("receita"), semPc:num("sem-pc")/100,""")
    s=sub1(s,"""  $("#c-bimp").hidden         = false;""","""  $("#c-bimp").hidden         = false;
  $("#c-sempc").hidden        = simples;""")

    # ===== logotipo da Amcont =====
    _logo=open('logo_b64.txt').read()
    _img='<img class="%s" alt="Amcont Assessoria e Contabilidade" src="data:image/png;base64,'+_logo+'">'
    s=sub1(s,'<div class="gate-mark">Amcont</div>',_img%'logo-gate')
    s=sub1(s,'<span class="mark">AMCONT</span>',_img%'logo-hd')
    s=sub1(s,'</style>','.logo-gate{display:block;height:58px;margin-bottom:18px;filter:brightness(0) invert(1)}\n.logo-hd{height:32px;align-self:center;filter:brightness(0) invert(1)}\n@media print{header{background:#fff!important;color:#10242A!important;border-bottom:2px solid #2A5F6B}.logo-hd{filter:none}header .sub,header .lei{color:#2A5F6B!important}}\n</style>')
    # ===== versão na simulação salva e aviso ao abrir (rodada 18) =====
    s=sub1(s,"""          cliente:nome, parametros:PARAM, entradas:entradasAtuais()},
         "amcont-" + nome.toLowerCase().replace(/[^a-z0-9]+/g,"-").slice(0,40) + ".json");""","""          cliente:nome, versaoApp:window.AMCONT_VERSAO||"", parametros:PARAM, entradas:entradasAtuais()},
         "amcont-" + nome.toLowerCase().replace(/[^a-z0-9]+/g,"-").slice(0,40) + "-v" + (window.AMCONT_VERSAO||"") + ".json");""")
    s=sub1(s,"""      avisar("Simulação e parâmetros carregados" + (o.cliente ? " · " + o.cliente : "") + ".", "ok");""","""      { const va = window.AMCONT_VERSAO || "", vf = o.versaoApp || "", nm = x => x.split(".").map(n=>+n||0);
        const c = (()=>{ const A=nm(vf), B=nm(va); for (let i=0;i<3;i++){ if ((A[i]||0)!==(B[i]||0)) return (A[i]||0)-(B[i]||0); } return 0; })();
        const q = o.cliente ? " · " + o.cliente : "";
        if (!vf) avisar("Simulação carregada" + q + ". Ela foi salva antes do controle de versão: confira os valores nesta versão (" + va + ").", "err");
        else if (c > 0) avisar("Atenção: simulação salva na versão " + vf + ", mais nova que esta (" + va + "). Peça à Amcont a versão atual.", "err");
        else if (c < 0) avisar("Simulação salva na versão " + vf + " e recalculada nesta (" + va + "). Os valores podem ter mudado" + q + ".", "err");
        else avisar("Simulação e parâmetros carregados" + q + " (versão " + va + ").", "ok"); }""")
    from validade_js import VALIDADE_JS
    s=sub1(s,"</body>",VALIDADE_JS+"\n</body>")
    open(dst,'w',encoding='utf-8').write(s); print(dst,len(s))
