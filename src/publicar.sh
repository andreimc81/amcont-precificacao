#!/bin/bash
# Publica uma nova versão das ferramentas Amcont. Toda entrega passa por aqui, por menor que seja a mudança.
# Uso: bash src/publicar.sh "o que mudou" "R16-01 a R17-03"     (sobe a versão)
#      bash src/publicar.sh --mesma                             (regera a versão atual, sem subir)
set -e
cd /home/claude/work
if [ "$1" != "--mesma" ]; then python3 src/versao.py publicar "$1" "$2"; fi
V=$(python3 src/versao.py atual | cut -d' ' -f1)
echo "== gerando versão $V"
python3 src/build_db.py >/dev/null
python3 src/build_html.py >/dev/null
python3 src/build_prec.py >/dev/null
node src/dump_class.js >/dev/null
python3 src/build_xlsx.py >/dev/null
python3 /mnt/skills/public/xlsx/scripts/recalc.py Amcont_Precificacao_Reforma_Tributaria.xlsx 180 | grep -q '"total_errors": 0' || { echo "ERRO: planilha com erro de fórmula"; exit 1; }
node src/gera_manuais.js >/dev/null
python3 -c "
g=open('src/gera_manuais.js',encoding='utf-8').read(); h=g[:g.index('/* =================== IT.002')]
r=open('src/gera_relatorio.js',encoding='utf-8').read(); r=r[r.index('const T=JSON.parse'):].replace('fs0.readFileSync','fs.readFileSync')
open('src/gera_relatorio_full.js','w',encoding='utf-8').write(h+r)"
node src/gera_relatorio_full.js >/dev/null
python3 src/gera_registro.py >/dev/null
python3 -c "import sys; sys.path.insert(0,'src'); from versao import texto_historico; open('HISTORICO-VERSOES.txt','w',encoding='utf-8').write(texto_historico())"
gzip -c class_dump.json > monitor/class_dump.json.gz
echo "== bateria de testes (${BATERIA:-rapida})"
bash src/bateria.sh ${BATERIA:-rapida} > /dev/null || { echo "PUBLICAÇÃO BLOQUEADA: bateria reprovada. Veja TESTES-v$V.txt"; cat TESTES-v$V.txt; exit 1; }
P=/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/pdfs; rm -rf $P; mkdir -p $P
soffice --headless --convert-to pdf --outdir $P IT001-*.docx IT002-*.docx MC001-*.docx MU001-*.docx RC001-*.docx RT001-*.docx >/dev/null 2>&1
Z=zipfinal
cp amcont-cliente.html amcont-produto.html $P/MU001-*.pdf HISTORICO-VERSOES.txt $Z/1-Enviar-ao-cliente/
cp amcont-precificacao.html Amcont_Precificacao_Reforma_Tributaria.xlsx $Z/2-Uso-interno-Amcont/
cp IT001-*.docx IT002-*.docx MC001-*.docx MU001-*.docx RC001-*.docx RT001-*.docx $Z/3-Documentos/editaveis/; cp $P/*.pdf $Z/3-Documentos/pdf/
cp src/*.py src/*.js src/*.sh db.json pis_mono.json $Z/4-Base-e-geradores/ 2>/dev/null || true
cp monitor/registro_alteracoes.xlsx monitor/versao.json monitor/LEIA-ME.txt monitor/monitor_fontes.py monitor/monitor_legislacao.py $Z/4-Base-e-geradores/monitor/
rm -f $Z/TESTES-v*.txt pacote/TESTES-v*.txt; cp HISTORICO-VERSOES.txt TESTES-v$V.txt $Z/
sed -i "s/^Pacote completo de .*/Pacote completo, versão $V. Parâmetros 2026.2, base fiscal 2026.8./" $Z/LEIA-ME.txt
cp amcont-cliente.html amcont-produto.html $P/MU001-*.pdf HISTORICO-VERSOES.txt pacote/
rm -f Amcont-Reforma-Tributaria-Completo*.zip Amcont-Calculadoras-Reforma-Cliente*.zip
(cd zipfinal && zip -qr ../Amcont-Reforma-Tributaria-Completo-v$V.zip . -x '*__pycache__*')
(cd pacote && zip -qr ../Amcont-Calculadoras-Reforma-Cliente-v$V.zip .)
O=/mnt/user-data/outputs
rm -f $O/Amcont-Reforma-Tributaria-Completo*.zip $O/Amcont-Calculadoras-Reforma-Cliente*.zip
rm -f $O/TESTES-v*.txt
cp Amcont-Reforma-Tributaria-Completo-v$V.zip Amcont-Calculadoras-Reforma-Cliente-v$V.zip amcont-cliente.html amcont-precificacao.html amcont-produto.html Amcont_Precificacao_Reforma_Tributaria.xlsx HISTORICO-VERSOES.txt TESTES-v$V.txt $O/
cp IT001-*.docx IT002-*.docx MC001-*.docx MU001-*.docx RC001-*.docx RT001-*.docx $P/MU001-*.pdf $O/
python3 src/build_web.py site >/dev/null && (cd site && rm -f ../Amcont-Central-Fiscal-site-v$V.zip && zip -qr ../Amcont-Central-Fiscal-site-v$V.zip . )
mkdir -p historico/publicadas && cp Amcont-Reforma-Tributaria-Completo-v$V.zip historico/publicadas/
echo "== publicada $V"
