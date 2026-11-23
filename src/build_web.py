# Gera o site da Central Fiscal (subdomínio consultas) a partir das calculadoras para cliente.
# Uso: python3 src/build_web.py [destino]   (padrão: site/)
# O acesso é controlado pelo servidor (cPanel ou login do portal); por isso a tela de senha é retirada.
import json, re, os, sys, shutil, html
DEST = sys.argv[1] if len(sys.argv) > 1 else 'site'
V = json.load(open('monitor/versao.json', encoding='utf-8'))
VER = f"{V['base']}.{V['seq']}"
d = V['data'][:10].split('-'); DATA = f"{d[2]}/{d[1]}/{d[0]}"
shutil.rmtree(DEST, ignore_errors=True); os.makedirs(DEST)

ENTRADA = {
    'amcont-cliente.html': 'calcular(true);',
    'amcont-produto.html': 'iniciar();',
}
for arq, init in ENTRADA.items():
    s = open(arq, encoding='utf-8').read()
    assert '<div id="gate">' in s and '<div id="app" hidden>' in s, arq
    auto = ('<script>(function(){var g=document.getElementById("gate");if(!g)return;g.remove();'
            'document.getElementById("app").hidden=false;' + init +
            '})();</script>\n')
    i = s.rfind('</body>'); assert i > 0
    s = s[:i] + auto + s[i:]
    # o gate não pisca na abertura
    s = s.replace('<div id="gate">', '<div id="gate" style="display:none">', 1)
    open(os.path.join(DEST, arq), 'w', encoding='utf-8').write(s)

cli = open('amcont-cliente.html', encoding='utf-8').read()
logo = re.search(r'<img class="logo-hd"[^>]*src="(data:image/png;base64,[^"]+)"', cli).group(1)

INDEX = f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Central Fiscal Amcont</title>
<meta name="robots" content="noindex,nofollow">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Sans+Condensed:wght@500;600;700&display=swap" rel="stylesheet">
<style>
:root{{--petroleo:#2A5F6B;--petroleo-2:#4A8FA0;--petroleo-3:#D6E8EB;--tinta:#1E2B2F;--fundo:#F6F9FA;--r:10px}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"IBM Plex Sans",system-ui,sans-serif;color:var(--tinta);background:var(--fundo);min-height:100vh;display:flex;flex-direction:column}}
header{{background:var(--petroleo);color:#fff;padding:22px 16px}}
.wrap{{max-width:980px;margin:0 auto;width:100%}}
header .wrap{{display:flex;align-items:center;gap:18px;flex-wrap:wrap}}
header img{{height:44px;filter:brightness(0) invert(1)}}
header h1{{font-family:"IBM Plex Sans Condensed","IBM Plex Sans",system-ui,sans-serif;font-weight:600;font-size:clamp(22px,4vw,30px)}}
header p{{color:var(--petroleo-3);font-size:14px;margin-top:2px}}
main{{flex:1;padding:28px 16px}}
.sec{{font-family:"IBM Plex Sans Condensed","IBM Plex Sans",system-ui,sans-serif;letter-spacing:.2em;text-transform:uppercase;font-size:12px;color:var(--petroleo);margin:0 0 12px}}
.grade{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin-bottom:28px}}
.card{{background:#fff;border:1px solid var(--petroleo-3);border-radius:var(--r);padding:20px;display:flex;flex-direction:column;gap:10px;text-decoration:none;color:inherit;transition:border-color .15s,box-shadow .15s}}
a.card:hover{{border-color:var(--petroleo-2);box-shadow:0 4px 16px rgba(42,95,107,.12)}}
.card h2{{font-size:18px;color:var(--petroleo)}}
.card p{{font-size:14px;line-height:1.5}}
.card .ir{{margin-top:auto;font-weight:600;color:var(--petroleo-2);font-size:14px}}
.card.breve{{opacity:.6}}
.card.breve .ir{{color:#7a8a8f}}
.aviso{{background:#fff;border-left:4px solid var(--petroleo-2);padding:14px 16px;font-size:13px;line-height:1.55;border-radius:6px}}
footer{{padding:16px;font-size:12px;color:#5d6d72;border-top:1px solid var(--petroleo-3)}}
footer .wrap{{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}}
</style></head>
<body>
<header><div class="wrap"><img alt="Amcont Assessoria e Contabilidade" src="{logo}">
<div><h1>Central Fiscal</h1><p>Consultas e simuladores da Reforma Tributária</p></div></div></header>
<main><div class="wrap">
<p class="sec">Consulta tributária</p>
<div class="grade">
<a class="card" href="amcont-produto.html"><h2>Consulta por produto ou serviço</h2>
<p>Informe o NCM ou o NBS e veja a classificação na LC 214/2025, o ICMS de Santa Catarina e o preço de venda de 2026 a 2033.</p><span class="ir">Abrir consulta</span></a>
<a class="card" href="amcont-cliente.html"><h2>Simulador da empresa</h2>
<p>Compare a carga tributária atual com a da reforma, ano a ano, e veja o efeito no preço e na margem.</p><span class="ir">Abrir simulador</span></a>
</div>
<p class="sec">Em breve</p>
<div class="grade">
<div class="card breve"><h2>Consulta cadastral</h2><p>Situação cadastral, regime e atividades do CNPJ.</p><span class="ir">Em preparação</span></div>
<div class="card breve"><h2>Validador fiscal</h2><p>Conferência de NCM, CST e classificação do cadastro de produtos.</p><span class="ir">Em preparação</span></div>
</div>
<div class="aviso"><strong>Estimativa.</strong> Os resultados são simulações com base na legislação vigente na data da versão e nos dados informados. Não substituem a análise da Amcont para a sua operação. Confirme com a equipe antes de alterar preços ou contratos.</div>
</div></main>
<footer><div class="wrap"><span>Amcont Assessoria e Contabilidade · CRC/SC 011862/O-0</span><span>Versão {VER} de {DATA}</span></div></footer>
</body></html>
'''
open(os.path.join(DEST, 'index.html'), 'w', encoding='utf-8').write(INDEX)

open(os.path.join(DEST, 'versao.json'), 'w', encoding='utf-8').write(
    json.dumps({'versao': VER, 'data': V['data']}, ensure_ascii=False, indent=1))

# Apache (HostGator): sem listagem de pastas, HTTPS obrigatório, cabeçalhos de segurança, sem cache do HTML
open(os.path.join(DEST, '.htaccess'), 'w').write('''Options -Indexes
RewriteEngine On
RewriteCond %{HTTPS} !=on
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
<FilesMatch "^(\\.cpanel\\.yml|LEIA-ME\\.md)$">
  Require all denied
</FilesMatch>
<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set X-Frame-Options "SAMEORIGIN"
  <FilesMatch "\\.(html|json)$">
    Header set Cache-Control "no-cache"
  </FilesMatch>
</IfModule>
''')

# Implantação pelo Git do cPanel: o ramo "main" vai para produção, o ramo "teste" para homologação.
# Ajuste as duas pastas abaixo para as pastas raiz dos subdomínios criados no cPanel.
open(os.path.join(DEST, '.cpanel.yml'), 'w').write('''---
deployment:
  tasks:
    - export RAMO=$(git rev-parse --abbrev-ref HEAD)
    - if [ "$RAMO" = "main" ]; then export SUB=consultas; elif [ "$RAMO" = "teste" ]; then export SUB=consultas-teste; else export SUB=; fi
    - export DEST=; for d in $HOME/$SUB.amcontassessoria.com.br $HOME/public_html/$SUB.amcontassessoria.com.br $HOME/public_html/$SUB; do if [ -n "$SUB" ] && [ -z "$DEST" ] && [ -d "$d" ]; then export DEST=$d; fi; done
    - if [ -n "$DEST" ]; then /bin/cp -f index.html amcont-produto.html amcont-cliente.html versao.json .htaccess "$DEST/"; fi
''')
print('site gerado em', DEST, 'versão', VER)
