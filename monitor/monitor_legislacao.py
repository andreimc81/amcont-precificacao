#!/usr/bin/env python3
"""Monitor da legislacao da reforma tributaria (Amcont).

Uso:
  python3 monitor_legislacao.py --nova lc214.docx [--anterior foto_anterior.json]
         [--base class_dump.json(.gz)] [--aceitas aceitas.json]
         --saida relatorio.md --foto foto_nova.json

1. Fotografa a LC 214 consolidada (norma atualizada da Camara, .docx): artigos e itens dos anexos.
2. Compara com a fotografia anterior: artigos e itens alterados, incluidos ou revogados.
3. Audita a base da ferramenta contra os anexos: NCM e NBS cobertos pela lei e nao pela base, e o contrario,
   descontando as divergencias ja revisadas (aceitas.json).
Requer python-docx.
"""
import argparse, gzip, hashlib, json, re, sys, datetime, collections
import docx
from docx.table import Table
from docx.text.paragraph import Paragraph

ART = re.compile(r'^Art\.\s*(\d+)\s*(?:º|°|o)?\s*(-[A-Z])?\s*[.\-–]?\s')
NOTA = re.compile(r'Lei Complementar nº\s*(\d+),\s*de\s*(\d{1,2}/\d{1,2}/\d{4})')
# artigos que alimentam a ferramenta: base de calculo, Simples, creditos, regimes diferenciados e
# especificos, transicao e Imposto Seletivo
CRITICOS = [(4, 15), (41, 58), (125, 175), (176, 260), (343, 370), (409, 434)]

def ehcritico(n):
    try: k = int(re.match(r'\d+', n).group(0))
    except Exception: return False
    return any(a <= k <= b for a, b in CRITICOS)

def norm(s): return re.sub(r'\s+', ' ', s or '').strip()

def fotografar(caminho):
    d = docx.Document(caminho)
    artigos, anexos, notas = collections.OrderedDict(), collections.OrderedDict(), collections.Counter()
    cur_art, cur_an, fim_anexos = None, None, False
    for el in d.element.body.iterchildren():
        tag = el.tag.split('}')[1]
        if tag == 'p':
            tx = norm(Paragraph(el, d).text)
            if not tx: continue
            for m in NOTA.finditer(tx): notas['LC %s, de %s' % m.groups()] += 1
            m = re.match(r'^ANEXO ([IVXL]+)$', tx)
            if m:
                if m.group(1) in anexos: fim_anexos = True
                if not fim_anexos:
                    cur_an = m.group(1); anexos[cur_an] = {'titulo': '', 'itens': collections.OrderedDict(), 'notas': []}
                    cur_art = None
                continue
            if cur_an and not fim_anexos:
                a = anexos[cur_an]
                if not a['titulo']: a['titulo'] = tx
                else: a['notas'].append(tx)
                continue
            if fim_anexos: continue
            m = ART.match(tx)
            if m:
                cur_art = m.group(1) + (m.group(2) or '')
                artigos[cur_art] = tx
            elif cur_art:
                artigos[cur_art] += '\n' + tx
        elif tag == 'tbl' and cur_an and not fim_anexos:
            t = Table(el, d); a = anexos[cur_an]; ult = None
            for r in t.rows:
                cel = []
                for c in r.cells:
                    x = norm(c.text)
                    if not cel or cel[-1] != x: cel.append(x)
                if not cel or cel[0].upper() in ('ITEM', 'ANO'): continue
                if re.match(r'^\d+(\.\d+)?$', cel[0]):
                    k = cel[0]; txt = ' | '.join(cel[1:])
                    if k in a['itens']:
                        if txt not in a['itens'][k]: a['itens'][k] += ' || ' + txt
                    else: a['itens'][k] = txt
                    ult = k
                else:
                    k = ult or ('linha%d' % len(a['itens']))
                    a['itens'][k] = (a['itens'].get(k, '') + ' || ' + ' | '.join(cel)).strip(' |')
    h = hashlib.sha256(open(caminho, 'rb').read()).hexdigest()
    return {'meta': {'arquivo': caminho.split('/')[-1], 'sha256': h, 'fotografado_em': datetime.date.today().isoformat(),
                     'artigos': len(artigos), 'anexos': len(anexos),
                     'leis_alteradoras': dict(sorted(notas.items()))},
            'artigos': artigos, 'anexos': anexos}

def comparar(a, b):
    out = {'artigos': [], 'anexos': [], 'leis_novas': []}
    for lei in b['meta']['leis_alteradoras']:
        if lei not in a['meta']['leis_alteradoras']: out['leis_novas'].append(lei)
    for k in set(a['artigos']) | set(b['artigos']):
        x, y = a['artigos'].get(k), b['artigos'].get(k)
        if x != y:
            tipo = 'incluído' if x is None else ('suprimido' if y is None else 'alterado')
            out['artigos'].append({'art': k, 'tipo': tipo, 'critico': ehcritico(k), 'antes': x, 'depois': y})
    for an in set(a['anexos']) | set(b['anexos']):
        ia = a['anexos'].get(an, {'itens': {}, 'titulo': ''}); ib = b['anexos'].get(an, {'itens': {}, 'titulo': ''})
        if ia.get('titulo') != ib.get('titulo'):
            out['anexos'].append({'anexo': an, 'item': '(título)', 'antes': ia.get('titulo'), 'depois': ib.get('titulo')})
        for it in set(ia['itens']) | set(ib['itens']):
            x, y = ia['itens'].get(it), ib['itens'].get(it)
            if x != y: out['anexos'].append({'anexo': an, 'item': it, 'antes': x, 'depois': y})
    out['artigos'].sort(key=lambda z: (not z['critico'], int(re.match(r'\d+', z['art']).group(0))))
    out['anexos'].sort(key=lambda z: (z['anexo'], z['item']))
    return out

# ---------- auditoria da base contra os anexos ----------
COD = re.compile(r'(?<![\d.])(\d{2}\.\d{2}(?:\.\d{2}){0,2}|\d{4}(?:\.\d{1,2}){0,2})(?![\d])')
NBS = re.compile(r'(?<![\d.])1\.\d{4}(?:\.\d{1,2}){0,2}(?![\d])')
CAP = re.compile(r'[Cc]ap[íi]tulos?\s+(\d{1,2})(?:\s*(?:,|e)\s*(\d{1,2}))?(?:\s*(?:,|e)\s*(\d{1,2}))?')
EXC = re.compile(r'\b(exceto|excetuad|ressalvad)', re.I)
ANX_NCM = ['I', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'XI', 'XII', 'XIII', 'XV', 'XVII']
ANX_NBS = ['II', 'III', 'IX', 'X', 'XI']

def _tokens(txt, nbs=False):
    inc, exc = set(), set()
    if 'VETADO' in txt.upper() and len(txt) < 40: return inc, exc
    padrao = NBS if nbs else COD
    for pm in re.finditer(r'\((?:exceto|excetuad|ressalvad)[^)]*\)', txt, re.I):
        for c in padrao.findall(pm.group(0)): exc.add(c.replace('.', ''))
    txt = re.sub(r'\((?:exceto|excetuad|ressalvad)[^)]*\)', '', txt, flags=re.I)
    for seg in re.split(r';|\|\|', txt):
        m = EXC.search(seg); partes = ((seg[:m.start()], inc), (seg[m.start():], exc)) if m else ((seg, inc),)
        for parte, dest in partes:
            if nbs:
                for c in NBS.findall(parte): dest.add(c.replace('.', ''))
            else:
                parte = NBS.sub('', parte)
                for c in COD.findall(parte):
                    n = c.replace('.', '')
                    if len(n) >= 4: dest.add(n)
                for m2 in CAP.finditer(parte):
                    for g in m2.groups():
                        if g: dest.add(g.zfill(2))
    return inc, exc

def auditar(foto, base):
    res = {}
    for tipo, lista, chave in (('ncm', ANX_NCM, 'ncm'), ('nbs', ANX_NBS, 'nbs')):
        U = {x['cod']: x for x in base[chave]}
        cita = collections.defaultdict(set)
        for c, x in U.items():
            for o in x['ops']:
                if o['red'] == 0 and o['ccl'] == '000001' and 'XVII' not in o['rot']: continue
                for m in re.finditer(r'Anexo ([IVXL]+)\b', o['rot'] + ' ' + (o.get('base') or '')): cita[c].add(m.group(1))
            if tipo == 'ncm' and any('XVII' in o['rot'] for o in x['ops']): cita[c].add('XVII')
        for an in lista:
            itens = foto['anexos'].get(an, {}).get('itens', {})
            cov = set()
            for it, txt in itens.items():
                inc, exc = _tokens(txt, nbs=(tipo == 'nbs'))
                if not inc: continue
                cov |= {u for u in U if any(u.startswith(p) for p in inc) and not any(u.startswith(p) for p in exc)}
            nb = {c for c, s in cita.items() if an in s}
            res['%s:%s' % (tipo, an)] = {'lei': sorted(cov - nb), 'base': sorted(nb - cov)}
    return res

def carregar(p):
    if p.endswith('.gz'): return json.load(gzip.open(p, 'rt', encoding='utf-8'))
    return json.load(open(p, encoding='utf-8'))

def relatorio(foto, dif, aud, aceitas, base):
    L = ['# Monitor da legislação: LC 214/2025 consolidada', '',
         'Arquivo: %s (sha256 %s...), fotografado em %s. Artigos: %d. Anexos: %d.' % (
             foto['meta']['arquivo'], foto['meta']['sha256'][:12], foto['meta']['fotografado_em'], foto['meta']['artigos'], foto['meta']['anexos']), '']
    L.append('Leis alteradoras citadas no texto: ' + '; '.join('%s (%d notas)' % kv for kv in foto['meta']['leis_alteradoras'].items()))
    L.append('')
    novos = []
    if aud is not None:
        for k, v in aud.items():
            ac = aceitas.get(k, {'lei': [], 'base': []})
            nl = [c for c in v['lei'] if c not in ac['lei']]; nbx = [c for c in v['base'] if c not in ac['base']]
            if nl or nbx: novos.append((k, nl, nbx))
    crit = (dif and (dif['anexos'] or any(a['critico'] for a in dif['artigos']) or dif['leis_novas'])) or novos
    L += ['## Resultado', '', '**AÇÃO NECESSÁRIA: revisar antes de enviar qualquer versão a cliente.**' if crit else
          '**Nenhuma alteração que afete a ferramenta.** A base continua aderente ao texto consolidado.', '']
    if dif is not None:
        L += ['## 1. Mudanças no texto desde a fotografia anterior', '']
        if dif['leis_novas']: L.append('Leis alteradoras novas: ' + '; '.join(dif['leis_novas'])); L.append('')
        if not dif['artigos'] and not dif['anexos']: L.append('Nenhuma mudança de texto.')
        for a in dif['anexos']:
            L.append('- **Anexo %s, item %s** (afeta a classificação)' % (a['anexo'], a['item']))
            L.append('  - Antes: %s' % ((a['antes'] or '(não existia)')[:600]))
            L.append('  - Depois: %s' % ((a['depois'] or '(suprimido)')[:600]))
        for a in dif['artigos']:
            L.append('- Art. %s %s%s' % (a['art'], a['tipo'], ' **(CRÍTICO para a ferramenta)**' if a['critico'] else ''))
            if a['critico']:
                L.append('  - Depois: %s' % ((a['depois'] or '(suprimido)')[:800].replace('\n', ' / ')))
        L.append('')
    if aud is not None:
        U = {x['cod']: x for x in base['ncm']}; U.update({x['cod']: x for x in base['nbs']})
        L += ['## 2. Base da ferramenta contra os anexos', '']
        if not novos: L.append('Sem divergência nova. As divergências já revisadas estão em aceitas.json.')
        for k, nl, nbx in novos:
            tipo, an = k.split(':')
            L.append('- **Anexo %s (%s)**' % (an, tipo.upper()))
            for c in nl[:40]: L.append('  - Coberto pela lei e sem esse anexo na base: %s %s' % (c, U[c]['desc'][:70]))
            for c in nbx[:40]: L.append('  - Na base com esse anexo, fora dos códigos da lei: %s %s' % (c, U[c]['desc'][:70]))
            if len(nl) > 40 or len(nbx) > 40: L.append('  - (lista truncada: %d e %d códigos)' % (len(nl), len(nbx)))
        L.append('')
    L += ['## 3. Checklist antes de liberar versão nova ao cliente', '',
          '1. Cada item acima foi lido no texto da lei e decidido (corrigir a base ou registrar em aceitas.json com o motivo).',
          '2. Geradores rodados: base, calculadoras e planilha.',
          '3. Testes: cruzamento planilha contra calculadora sem divergência; recálculo da planilha sem erro.',
          '4. MC.001 atualizada com a data e o que mudou.',
          '5. Versão nova enviada aos clientes que usam a ferramenta, com aviso do que mudou.', '']
    return '\n'.join(L)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nova', required=True); ap.add_argument('--anterior'); ap.add_argument('--base')
    ap.add_argument('--aceitas'); ap.add_argument('--saida', required=True); ap.add_argument('--foto', required=True)
    ap.add_argument('--gerar-aceitas', help='grava as divergencias atuais como revisadas neste arquivo')
    a = ap.parse_args()
    foto = fotografar(a.nova)
    json.dump(foto, open(a.foto, 'w', encoding='utf-8'), ensure_ascii=False)
    dif = comparar(carregar(a.anterior), foto) if a.anterior else None
    base = carregar(a.base) if a.base else None
    aud = auditar(foto, base) if base else None
    if a.gerar_aceitas and aud is not None:
        json.dump(aud, open(a.gerar_aceitas, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    aceitas = carregar(a.aceitas) if a.aceitas else {}
    open(a.saida, 'w', encoding='utf-8').write(relatorio(foto, dif, aud, aceitas, base))
    print(open(a.saida, encoding='utf-8').read()[:1500])

if __name__ == '__main__':
    main()
