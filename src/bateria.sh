#!/bin/bash
# Bateria de testes da versão. Uso: bash src/bateria.sh rapida|completa   -> grava TESTES-v<versão>.txt
cd /home/claude/work
V=$(python3 src/versao.py atual | cut -d' ' -f1); OUT=TESTES-v$V.txt; MODO=${1:-rapida}
echo "BATERIA DE TESTES ($MODO)  |  versão $V  |  $(TZ=America/Sao_Paulo date '+%d/%m/%Y %H:%M')" > $OUT
FALHA=0
tela(){ for t in t_lc t_cq t_pc t_compra t_user t_uf t_prud test_html test_load test_prec test_def test_emp test_red test_senha; do
  r=$(timeout 300 node src/$t.js 2>&1); e=$?; erros=$(echo "$r" | grep -c "Error\|ERRO" || true)
  if [ $e -ne 0 ] || [ "$erros" != "0" ]; then echo "REPROVADO  tela $t" >> $OUT; FALHA=1; else echo "aprovado   tela $t" >> $OUT; fi; done; }
linha(){ # $1 nome, $2 comando, $3 padrão de sucesso
  r=$(eval "$2" 2>&1 | tail -3); if echo "$r" | grep -qE "$3"; then echo "aprovado   $1: $(echo "$r" | grep -E "$3" | tail -1 | cut -c1-90)" >> $OUT; else echo "REPROVADO  $1: $(echo "$r" | tail -1 | cut -c1-150)" >> $OUT; FALHA=1; fi; }
tela
linha "perguntas de ICMS de SC (t_scq)" "node src/t_scq.js" "^[0-9]+ de [0-9]+ \[\]" 
grep -q "REPROVADO  perguntas" $OUT || { n=$(node src/t_scq.js | tail -1); a=$(echo $n|cut -d' ' -f1); b=$(echo $n|cut -d' ' -f3); [ "$a" = "$b" ] || { sed -i 's/^aprovado   perguntas/REPROVADO  perguntas/' $OUT; FALHA=1; }; }
linha "verificação independente (301 casos)" "node src/ref_coleta.js >/dev/null && python3 -I src/ref_independente.py" "COMPRA: 160 de 160"
linha "planilha x calculadora, 23 cenários" "python3 src/cross.py >/dev/null && node src/cross.js" "^23/23"
linha "busca por código de serviço" "python3 src/t_serv.py" "TUDO OK"
if [ "$MODO" = "completa" ]; then
  linha "planilha x calculadora, venda para outro estado" "python3 src/cross_uf.py >/dev/null && node src/cross_uf.js" "^7/7"
  linha "planilha x calculadora, compra (672)" "python3 src/cross_compra.py >/dev/null && node src/cross_compra.js" "672/672|672 de 672"
  linha "planilha x calculadora, 80 cenários aleatórios" "python3 src/cross_amplo.py >/dev/null && node src/cross_amplo.js" "80 de 80|80/80"
  linha "planilha x calculadora, perguntas de ICMS (99)" "python3 src/cross_scq.py >/dev/null && node src/cross_scq.js" "^99 de 99"
fi
[ $FALHA = 0 ] && echo "RESULTADO: APROVADA" >> $OUT || echo "RESULTADO: REPROVADA" >> $OUT
cat $OUT; exit $FALHA
