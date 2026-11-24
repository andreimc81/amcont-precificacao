# ===== rodada 25 (versão 2026.8.12): R24-05 mensagem do Imposto Seletivo conforme o NCM =====
s=sub1(s,"""          <p class="dica">Incide sobre bens prejudiciais à saúde ou ao meio ambiente e
             <b>integra a base do ICMS, da CBS e do IBS</b>. Alíquotas de 2027 pela MP 1.399/2026,
             com efeitos a partir de 2 de fevereiro de 2027 (art. 19) e sujeitas à conversão em lei.</p>""","""          <p class="dica" id="dica-is">Incide sobre bens prejudiciais à saúde ou ao meio ambiente e
             <b>integra a base do ICMS, da CBS e do IBS</b>. Alíquotas de 2027 pela MP 1.399/2026,
             com efeitos a partir de 2 de fevereiro de 2027 (art. 19) e sujeitas à conversão em lei.</p>""")
s=sub1(s,"""function ajustarTopo(){""","""function dicaIS(){
  const el = $("#dica-is"); if (!el) return;
  const base = " Integra a base do ICMS, da CBS e do IBS. Alíquotas pela MP 1.399/2026, com efeitos a partir de 02/02/2027 (art. 19) e sujeitas à conversão em lei.";
  let t;
  if (typeof FICHA === "undefined" || !FICHA || FICHA.cor === "cinza"){
    t = "Incide sobre bens prejudiciais à saúde ou ao meio ambiente. Busque o NCM para saber se o produto está na lista." + base;
  } else {
    const v = parseFloat($("#is").value) || 0;
    if (FICHA.isNota === undefined){
      t = v === 0
        ? "Este NCM não consta nos bens sujeitos ao Imposto Seletivo (Anexo XVII da LC 214/2025 e Anexos IV e V da MP 1.399/2026): IS = 0%."
        : "Este NCM não consta nos bens sujeitos ao Imposto Seletivo, mas o campo foi preenchido manualmente com " + PCT(v/100) + ". Isso é uma simulação, não a regra da lei.";
    } else if (FICHA.is === null){
      t = "Este NCM está sujeito ao Imposto Seletivo, mas a alíquota depende do modelo ou de regra própria. Informe a alíquota; o campo foi deixado em zero." + base;
    } else {
      const igual = Math.abs(v/100 - FICHA.is) < 1e-9;
      t = igual ? "Este NCM está sujeito ao Imposto Seletivo: alíquota de " + PCT(FICHA.is) + " preenchida pela tabela." + base
                : "Este NCM está sujeito ao Imposto Seletivo (tabela: " + PCT(FICHA.is) + "). O campo foi alterado manualmente para " + PCT(v/100) + ".";
    }
  }
  el.textContent = t.trim();
}
function ajustarTopo(){""")
s=sub1(s,"""  atualizarTodos(o, H); sinalAliq();""","""  atualizarTodos(o, H); sinalAliq(); dicaIS();""")
