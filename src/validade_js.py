# Aviso de validade: a data e a da ultima conferencia da legislacao (monitor/ultima_conferencia.txt).
import os
_d=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','monitor','ultima_conferencia.txt')).read().strip()
_br='/'.join(reversed(_d.split('-')))
import sys as _s; _s.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from versao import VERSAO as _V
_VT='Versão %s, de %s. '%(_V['v'],_V['br'])
VALIDADE_JS='''<script>
window.AMCONT_VERSAO="%s";
(function(){
  var VT="%s", BASE="%s", LIMITE=45, dias=Math.floor((Date.now()-new Date(BASE+"T00:00:00").getTime())/864e5);
  var main=document.querySelector("main"); if(!main) return;
  var el=document.createElement("div"); el.id="validade";
  el.style.cssText="margin:14px auto 0;padding:10px 14px;border-left:4px solid "+(dias>LIMITE?"#A63D1B;background:#FBEDE7":"#4A8FA0;background:#EEF5F6")+";font:13px/1.45 Arial,sans-serif;color:#10242A";
  el.textContent = VT + (dias>LIMITE
    ? "Atenção: esta versão usa a legislação conferida em %s, há "+dias+" dias. Peça à Amcont a versão atualizada antes de decidir preços."
    : "Legislação conferida em %s (LC 214/2025 consolidada). Válida para simulação até "+new Date(new Date(BASE+"T00:00:00").getTime()+LIMITE*864e5).toLocaleDateString("pt-BR")+".") + " Confira com a Amcont se esta é a versão mais recente.";
  main.parentNode.insertBefore(el, main);
  document.title = document.title + " | v" + VT.split(",")[0].replace("Versão ","");
  var bd=document.createElement("div"); bd.id="selo-versao"; bd.textContent=VT.replace(/[.] $/,"");
  bd.style.cssText="position:fixed;right:10px;bottom:10px;z-index:50;padding:4px 9px;border-radius:3px;background:#2A5F6B;color:#fff;font:600 11px Arial,sans-serif;opacity:.88";
  document.body.appendChild(bd);
  if (dias > 2*LIMITE){
    document.body.classList.add("versao-vencida");
    var st=document.createElement("style");
    st.textContent="body.versao-vencida main .painel{opacity:.45} body.versao-vencida #validade{font-weight:700}";
    document.head.appendChild(st);
    el.textContent = VT + "VERSÃO VENCIDA: a legislação desta ferramenta foi conferida em %s, há "+dias+" dias. Os resultados não devem ser usados para decidir preços. Peça à Amcont a versão atualizada.";
  }
})();
</script>'''%(_V['v'],_VT,_d,_br,_br,_br)
