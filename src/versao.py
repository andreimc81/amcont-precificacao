"""Controle de versão das ferramentas Amcont.
Formato: <base fiscal>.<publicação>, ex.: 2026.8.3. A publicação sobe 1 a cada entrega, por menor que seja a mudança.
Uso:  python3 src/versao.py atual
      python3 src/versao.py publicar "o que mudou" "R16-01 a R17-03"
Os geradores (HTML, planilha, documentos) leem a versão daqui."""
import json, os, sys, datetime
ARQ=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','monitor','versao.json')
def ler():
    v=json.load(open(ARQ,encoding='utf-8'))
    v['v']='%s.%d'%(v['base'],v['seq'])
    d=datetime.datetime.fromisoformat(v['data']); v['br']=d.strftime('%d/%m/%Y %H:%M')
    return v
def publicar(resumo, registros='', base=None):
    v=json.load(open(ARQ,encoding='utf-8'))
    if base and base!=v['base']: v['base']=base; v['seq']=0
    else: v['seq']+=1
    agora=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).strftime('%Y-%m-%dT%H:%M')
    v['data']=agora
    v['hist'].append({'v':'%s.%d'%(v['base'],v['seq']),'data':agora,'resumo':resumo,'registros':registros})
    json.dump(v,open(ARQ,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
    return ler()
def texto_historico():
    v=ler(); linhas=['HISTÓRICO DE VERSÕES  |  Ferramentas de precificação Amcont','Versão atual: %s, de %s'%(v['v'],v['br']),'']
    for h in reversed(v['hist']):
        d=datetime.datetime.fromisoformat(h['data']).strftime('%d/%m/%Y %H:%M')
        linhas.append('%s  (%s)  %s%s'%(h['v'],d,h['resumo'],('  Registro: '+h['registros']) if h.get('registros') else ''))
    return '\n'.join(linhas)+'\n'
VERSAO=ler()
if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='publicar':
        v=publicar(sys.argv[2], sys.argv[3] if len(sys.argv)>3 else '')
        print(v['v'], v['br'])
    else:
        print(VERSAO['v'], VERSAO['br'])
