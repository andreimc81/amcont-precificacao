import re, json
t=open('/home/claude/dl/lc214/lc214_atual.txt',encoding='utf-8').read()
lines=t.split('\n')
# localizar anexos da LC 214 (primeira sequencia ANEXO I .. ANEXO XVII)
idx={}
for i,l in enumerate(lines):
    m=re.match(r'^ANEXO ([IVXL]+)\s*$',l)
    if m and m.group(1) not in idx: idx[m.group(1)]=i
    if 'XVIII' in idx: break
ordem=sorted(idx.items(),key=lambda x:x[1])
anexos={}
for k,(nome,ini) in enumerate(ordem):
    fim=ordem[k+1][1] if k+1<len(ordem) else ini+400
    bloco=lines[ini:fim]
    titulo=next((x.strip() for x in bloco[1:6] if x.strip()),'')
    itens={}; cur=None
    for l in bloco:
        m=re.match(r'^\s{0,4}(\d+(?:\.\d+)?)\s{2,}(\S.*)$',l)
        if m and not l.strip().startswith('---'):
            cur=m.group(1); itens[cur]=m.group(2).strip()
        elif cur and l.startswith(' '*7) and l.strip() and not l.strip().startswith('---'):
            itens[cur]+=' '+l.strip()
    anexos[nome]={'titulo':titulo,'itens':itens}
json.dump(anexos,open('/home/claude/work/audit/anexos_lei.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
for n,a in anexos.items(): print(n,len(a['itens']),a['titulo'][:90])
