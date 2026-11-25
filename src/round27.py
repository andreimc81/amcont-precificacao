# ===== rodada 27 (versão 2026.8.14): R26-01 opção de base do ICMS e do ISS com ou sem CBS e IBS =====
s=sub1(s,"""      <div class="bloco">
        <div class="bloco-tit" id="tit-venda">""","""      <div class="bloco" id="b-base">
        <div class="bloco-tit">Base do ICMS e do ISS, de 2027 em diante</div>
        <div class="campo" id="c-base">
          <label for="base-sem">A CBS e o IBS entram na base do ICMS e do ISS?</label>
          <select id="base-sem">
            <option value="0">Sim: ICMS e ISS sobre o total da nota</option>
            <option value="1">Não: ICMS e ISS sobre o valor sem CBS e IBS</option>
          </select>
          <p class="dica">Tema sem lei. "Sim" é a posição de São Paulo, Minas Gerais e Paraná para o ICMS e da Prefeitura de São Paulo para o ISS, e é o cenário mais oneroso (padrão). "Não" é a tese do PLP 16/2025 e de decisões judiciais isoladas. Santa Catarina só se manifestou sobre 2026 (fora da base) e Criciúma não publicou posição sobre o ISS. No Simples Nacional não muda, porque o ICMS e o ISS ficam dentro do DAS.</p>
        </div>
      </div>

      <div class="bloco">
        <div class="bloco-tit" id="tit-venda">""")
s=sub1(s,"""function creditoCompra(pc, forn, ano, icmsCompra, aliqForn, anexoForn, trat){""","""/* R26-01: base do ICMS e do ISS com CBS e IBS (padrão) ou sem (opção da tela).
   i = alíquota nominal de ICMS ou ISS; c e b = CBS e IBS efetivas. Devolve, como fração do total da nota:
   iE = ICMS ou ISS; k = CBS mais IBS. Com CBS e IBS na base: ICMS = i x total. Sem: ICMS = i x (total - CBS - IBS). */
function baseSem(){ const e = document.getElementById("base-sem"); return !!e && e.value === "1"; }
function fatBase(i, c, b){
  if (baseSem()){ const D = 1 + (1-i)*(c+b); return {iE: i/D, k: (1-i)*(c+b)/D}; }
  return {iE: i, k: (1-i)*(c+b)/(1+c+b)};
}
function creditoCompra(pc, forn, ano, icmsCompra, aliqForn, anexoForn, trat){""")
s=sub1(s,"""    if (regular){ const a = (t.cbs + t.ibs)*(1-(trat||0)); cbsIbs = a ? pc*(1 - icmsCompra*t.fatorIcmsIss)/(1+a)*a : 0; }""",
"""    if (regular){ const a = (t.cbs + t.ibs)*(1-(trat||0)); cbsIbs = a ? pc*fatBase(icmsCompra*t.fatorIcmsIss, a, 0).k : 0; }""")
s=sub1(s,"""      const a = (t.cbs + t.ibs)*(1-(trat||0)), teto = a ? pc*(1 - icmsCompra*t.fatorIcmsIss)/(1+a)*a : 0;""",
"""      const a = (t.cbs + t.ibs)*(1-(trat||0)), teto = a ? pc*fatBase(icmsCompra*t.fatorIcmsIss, a, 0).k : 0;""")
s=sub1(s,"""  } else if (forn !== "mei" && forn !== "pf") icms = pc * icmsCompra * t.fatorIcmsIss;""",
"""  } else if (forn !== "mei" && forn !== "pf")
    icms = pc * ((ano >= 2027 && regular) ? fatBase(icmsCompra*t.fatorIcmsIss, (t.cbs + t.ibs)*(1-(trat||0)), 0).iE : icmsCompra * t.fatorIcmsIss);""")
s=sub1(s,"""  const s = o.is, k = (1-i)*(c+b)/(1+c+b), sg = s*(1-i-k)/(1+s);
  const den = 1 - i - k - sg - o.r*(1-k-sg);
  const nf = (mcAlvo + pcAno - cr.total) / den;
  const icms = nf*i, bc = nf*(1-i)/(1+c+b), cbs = bc*c, ibs = bc*b;""","""  const s = o.is, fb = fatBase(i, c, b), iE = fb.iE, k = fb.k, sg = s*(1-iE-k)/(1+s);
  const den = 1 - iE - k - sg - o.r*(1-k-sg);
  const nf = (mcAlvo + pcAno - cr.total) / den;
  const icms = nf*iE, bc = nf*(1-iE-k), cbs = bc*c, ibs = bc*b;""")
s=sub1(s,"""    const i = A.i, c = A.c, b = A.b, s = o.is, k = (1-i)*(c+b)/(1+c+b), sg = s*(1-i-k)/(1+s);
    const icms = pv*i, bc = pv*(1-i)/(1+c+b), cbs = bc*c, ibs = bc*b, impSel = pv*sg, lucro = o.r*pv*(1-k-sg);""","""    const i = A.i, c = A.c, b = A.b, s = o.is, fb = fatBase(i, c, b), iE = fb.iE, k = fb.k, sg = s*(1-iE-k)/(1+s);
    const icms = pv*iE, bc = pv*(1-iE-k), cbs = bc*c, ibs = bc*b, impSel = pv*sg, lucro = o.r*pv*(1-k-sg);""")
s=sub1(s,"""    const base = A.nf - A.icms - A.cbs - A.ibs;""","""    const base = A.nf - A.icms - A.cbs - A.ibs, bI = baseSem() ? A.nf - A.cbs - A.ibs : A.nf;""")
s=sub1(s,"""         ["Base do "+imp+": total da nota", A.nf, "sub"],""","""         ["Base do "+imp+(baseSem() ? ": valor sem CBS e IBS (opção da simulação)" : ": total da nota"), bI, "sub"],""")
s=sub1(s,"""+", SC para "+o.ufDest, A.nf*o.icmsInter*tAno(o.ano).fatorIcmsIss],""","""+", SC para "+o.ufDest, bI*o.icmsInter*tAno(o.ano).fatorIcmsIss],""")
s=sub1(s,"""["DIFAL para "+o.ufDest+", recolhido por você", A.nf*o.difal*tAno(o.ano).fatorIcmsIss] : null]""","""["DIFAL para "+o.ufDest+", recolhido por você", bI*o.difal*tAno(o.ano).fatorIcmsIss] : null]""")
s=sub1(s,"""O ICMS e o ISS foram calculados sobre o total da nota, incluindo CBS e IBS, que é a posição dos fiscos estaduais; o tema ainda não tem lei e há tese contrária.</li>""","""O ICMS e o ISS são calculados, por padrão, sobre o total da nota, incluindo CBS e IBS, que é a posição de São Paulo, Minas Gerais e Paraná para o ICMS e da Prefeitura de São Paulo para o ISS. O tema ainda não tem lei, há tese contrária e Santa Catarina não se manifestou sobre 2027: a opção "Base do ICMS e do ISS" simula os dois cenários.</li>""")
s=sub1(s,"""  montarAliq(); lerAliq();""","""  montarAliq(); lerAliq();
  $("#base-sem").addEventListener("change", calcular);""")
