#!/bin/bash
# Copia a base de trabalho para o repositório amcont-precificacao e envia ao GitHub (backup a cada publicação).
R=/home/claude/amcont-precificacao
[ -d "$R/.git" ] || { echo "backup: repositório não clonado em $R"; exit 0; }
V=$(python3 -c "import json;v=json.load(open('monitor/versao.json'));print(v['base']+'.'+str(v['seq']))")
cp -a . "$R/" 2>/dev/null
cd "$R" && git add -A && git -c user.name="Amcont" -c user.email="noreply@anthropic.com" commit -qm "Base de trabalho, versão $V" && git -c push.negotiate=true push -q origin main 2>&1 | grep -vi negotiat | grep -v "^fatal: expected 'acknowledgments'" ; echo "backup: versão $V enviada"
