# ===== rodada 18: versão no estudo salvo e aviso ao abrir estudo de outra versão =====
s=sub1(s,"""            baseFiscal:DB.meta.versao, consulta:""","""            baseFiscal:DB.meta.versao, versaoApp:window.AMCONT_VERSAO||"", consulta:""")
s=sub1(s,"""           "amcont-produto-"+($("#ncm").value.replace(/\\D/g,"")||"estudo")+".json");""","""           "amcont-produto-"+($("#ncm").value.replace(/\\D/g,"")||"estudo")+"-v"+(window.AMCONT_VERSAO||"")+".json");""")
s=sub1(s,"""      sincronizar(); calcular(); avisar("Estudo carregado.","ok");""","""      sincronizar(); calcular();
      const va = window.AMCONT_VERSAO || "", vf = o.versaoApp || "";
      const num = x => x.split(".").map(n=>+n||0), cmp = (a,b) => { const A=num(a), B=num(b); for (let i=0;i<3;i++){ if ((A[i]||0)!==(B[i]||0)) return (A[i]||0)-(B[i]||0); } return 0; };
      if (!vf) avisar("Estudo carregado. Ele foi salvo antes do controle de versão: confira os valores nesta versão ("+va+").","err");
      else if (cmp(vf,va) > 0) avisar("Atenção: este estudo foi salvo na versão "+vf+", mais nova que esta ("+va+"). Peça à Amcont a versão atual da ferramenta.","err");
      else if (cmp(vf,va) < 0) avisar("Estudo salvo na versão "+vf+" e recalculado nesta versão ("+va+"). Os valores podem ter mudado: confira o histórico de versões.","err");
      else avisar("Estudo carregado (versão "+va+").","ok");""")
