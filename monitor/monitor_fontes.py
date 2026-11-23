#!/usr/bin/env python3
"""Monitor passivo das fontes oficiais (Amcont). Camada complementar ao monitor_legislacao.py.

Origem: monitor_fontes_oficiais.py da auditoria independente de 10/11/2026, adaptado pela Amcont:
  1. o hash e calculado sobre o TEXTO normalizado da pagina (sem scripts, estilos, tags e espacos), para que
     mudancas de layout, tokens de sessao e banners nao gerem alerta falso a cada semana;
  2. fontes acrescentadas: Senado (LC 214 compilada), NFS-e Nacional (Anexo VIII) e Portal da Reforma;
  3. o relatorio diz, para cada fonte, quais regras da ferramenta ela alimenta, e grava o trecho novo
     (primeiros 4.000 caracteres do texto) para a avaliacao humana.
Nunca altera regra de calculo. Uma alteracao detectada vira uma linha no registro de alteracoes
(registro_alteracoes.xlsx), com situacao "Em analise", ate validacao tecnica e aprovacao.

Uso: python3 monitor_fontes.py --estado estado_fontes.json --saida relatorio_fontes.json [--offline]
Codigo de saida: 0 sem alerta; 1 alteracao ou falha de consulta.
"""
import argparse, datetime, hashlib, html, json, pathlib, re, sys, urllib.request

FONTES = {
  'LC214_Planalto':   ('https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp214.htm', 'Todas as regras de IBS, CBS e IS; anexos de redução e alíquota zero'),
  'LC214_Senado':     ('https://legis.senado.leg.br/norma/40236624', 'Texto compilado da LC 214 (redundância do Planalto)'),
  'LC227_Planalto':   ('https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp227.htm', 'Alterações da LC 214 (art. 146, créditos, Comitê Gestor)'),
  'EC132_Planalto':   ('https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc132.htm', 'Cronograma da transição 2026 a 2033'),
  'RFB_legislacao':   ('https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/reforma-tributaria-do-consumo/legislacao/', 'Decretos, MPs e instruções normativas da CBS e do IS'),
  'RFB_atos_conjuntos': ('https://www.gov.br/receitafederal/pt-br/acesso-a-informacao/acoes-e-programas/reforma-tributaria-do-consumo/legislacao/atos-conjuntos', 'Lista de medicamentos do art. 146; alíquotas de referência'),
  'NFSe_RTC':         ('https://www.gov.br/nfse/pt-br/biblioteca/documentacao-tecnica/rtc', 'Anexo VIII (correlação NBS, LC 116 e cClassTrib)'),
  'NFe_tabelas':      ('https://www.nfe.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=/NJarYc9nus=', 'Tabelas CST e cClassTrib da NF-e'),
  'ALESC_ICMS_SC':    ('https://leis.alesc.sc.gov.br/ato-normativo/legislativo/11810', 'ICMS de SC (Lei 10.297): alíquotas internas e consumo popular'),
}

def texto(data):
    s = data.decode('utf-8', 'replace')
    s = re.sub(r'(?is)<(script|style|noscript)[^>]*>.*?</\1>', ' ', s)
    s = re.sub(r'(?s)<!--.*?-->', ' ', s)
    s = re.sub(r'(?s)<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()

def baixar(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Amcont-Monitor/1.0 (consulta institucional)',
                                               'Accept': 'text/html,application/xhtml+xml'})
    with urllib.request.urlopen(req, timeout=25) as r:
        if int(getattr(r, 'status', 200)) != 200: raise RuntimeError('HTTP %s' % r.status)
        data = r.read(12_000_001)
    if len(data) > 12_000_000: raise RuntimeError('resposta acima do limite de segurança')
    return data

def run(estado, saida, offline=False, fontes=FONTES):
    antes = json.loads(estado.read_text(encoding='utf-8')) if estado.exists() else {'versao': 2, 'fontes': {}}
    novo = {'versao': 2, 'fontes': dict(antes.get('fontes', {}))}
    agora = datetime.datetime.now(datetime.timezone.utc).isoformat()
    achados = []
    for nome, (url, uso) in fontes.items():
        try:
            if offline: raise RuntimeError('execução offline: consulta não efetuada')
            t = texto(baixar(url)); h = hashlib.sha256(t.encode('utf-8')).hexdigest()
            prev = antes.get('fontes', {}).get(nome, {}).get('sha256_texto')
            st = 'BASELINE' if prev is None else ('ALTERAÇÃO DETECTADA' if prev != h else 'SEM ALTERAÇÃO')
            novo['fontes'][nome] = {'url': url, 'sha256_texto': h, 'caracteres': len(t), 'ultima_consulta': agora}
            a = {'fonte': nome, 'status': st, 'url': url, 'alimenta': uso, 'sha256_texto': h, 'hash_anterior': prev}
            if st == 'ALTERAÇÃO DETECTADA': a['trecho_inicial'] = t[:4000]
            achados.append(a)
        except Exception as e:
            achados.append({'fonte': nome, 'status': 'FALHA DE CONSULTA', 'url': url, 'alimenta': uso, 'erro': str(e)})
    res = {'gerado_em_utc': agora,
           'natureza': 'Monitor passivo: não comprova vigência e não altera regra de cálculo.',
           'resultados': achados,
           'alerta': any(x['status'] in ('ALTERAÇÃO DETECTADA', 'FALHA DE CONSULTA') for x in achados),
           'publicacao_liberada': False,
           'procedimento': ('1) Ler a alteração e conferir vigência. 2) Registrar em registro_alteracoes.xlsx (situação Em análise). '
                            '3) Se mudar regra: ajustar a base, rodar a bateria de testes e o cruzamento HTML x Excel. '
                            '4) Aprovação da Amcont. 5) Só então publicar nova versão.')}
    saida.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding='utf-8')
    if not offline: estado.write_text(json.dumps(novo, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'alerta': res['alerta'], 'fontes': len(achados),
                      'alteracoes': sum(x['status'] == 'ALTERAÇÃO DETECTADA' for x in achados),
                      'falhas': sum(x['status'] == 'FALHA DE CONSULTA' for x in achados)}, ensure_ascii=False))
    return res

if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('--estado', default='estado_fontes.json')
    a.add_argument('--saida', default='relatorio_fontes.json'); a.add_argument('--offline', action='store_true')
    v = a.parse_args(); r = run(pathlib.Path(v.estado), pathlib.Path(v.saida), v.offline)
    sys.exit(1 if r['alerta'] else 0)
