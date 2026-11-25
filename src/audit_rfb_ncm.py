import sqlite3,json,collections
c=sqlite3.connect('/home/claude/rfb/base-oficial/calculadora-pro.db'); d=json.load(open('/home/claude/work/db.json',encoding='utf-8'))
H='2026-11-24'
regras=[(i,n.replace('.',''),cl) for i,n,cl,f,ax in c.execute("select NCMA_ID,NCMA_NCM_CD,CLTR_CD,NCMA_FIM_VIGENCIA,ANXO_NUMERO from NCM_APLICAVEL join CLASSIFICACAO_TRIBUTARIA on CLTR_ID=NCMA_CLTR_ID left join ANEXO on ANXO_ID=NCMA_ANXO_ID") if (not f or f>=H) and ax!='XVII']
AXR={(n.replace('.',''),cl):(ax,it) for n,cl,ax,it in c.execute("select NCMA_NCM_CD,CLTR_CD,ANXO_NUMERO,ANXO_NUMERO_ITEM from NCM_APLICAVEL join CLASSIFICACAO_TRIBUTARIA on CLTR_ID=NCMA_CLTR_ID left join ANEXO on ANXO_ID=NCMA_ANXO_ID")}
exc=collections.defaultdict(list)
for n,i,f in c.execute("select ENCM_NCM_CD,ENCM_NCMA_ID,ENCM_FIM_VIGENCIA from EXCECAO_NCM_APLICAVEL"):
    if not f or f>=H: exc[i].append(n.replace('.',''))
excg=collections.defaultdict(list)
for i,p,cl in regras: excg[(p,cl)]+=exc[i]
def oficial(cod):
    return {cl for i,p,cl in regras if cod.startswith(p) and not any(cod.startswith(x) for x in excg[(p,cl)])}
def nosso(cod):
    e=d['ncm'].get(cod); s=set()
    if e is None:
        for n in range(8,1,-1):
            if cod[:n] in d['pref']: e=d['pref'][cod[:n]]; break
    if e is None: return set()
    import re
    if e.get('ccl'): s|=set(re.findall(r'\d{6}',e['ccl']))
    for o in e.get('o',[]): s.add(o[4])
    return s
ncms=[n.replace('.','') for n,f in c.execute("select NCM_CD,NCM_FIM_VIGENCIA from NCM") if len(n.replace('.',''))==8 and (not f or f>=H)]
print('NCM oficiais vigentes de 8 dígitos',len(ncms))

INT={'000001','515001'}
pad=collections.Counter(); ex=collections.defaultdict(list); linhas=[]
for cod in ncms:
    o=oficial(cod)-INT; n=nosso(cod)-INT
    if o==n: continue
    k=('+of:'+','.join(sorted(o-n)) if o-n else '')+(' +nos:'+','.join(sorted(n-o)) if n-o else '')
    if len(o-n)>6: k='+of:(lista genérica %d classes)'%len(o-n)+(' +nos:'+','.join(sorted(n-o)) if n-o else '')
    pad[k]+=1; ex[k].append(cod); linhas.append((cod,sorted(n),sorted(o)))
for k,v in pad.most_common(40):
    caps=collections.Counter(c[:2] for c in ex[k]); print(v,'|',k,'| cap:',dict(caps.most_common(8)),'| ex:',ex[k][:4])
json.dump(linhas,open('/home/claude/rfb/diverg.json','w'))
print(len(linhas))

print('-----')
for r in c.execute("select CLTR_CD,CLTR_DESCRICAO,CLTR_ANEXO,CLTR_INICIO_VIGENCIA,CLTR_FIM_VIGENCIA from CLASSIFICACAO_TRIBUTARIA where CLTR_CD in ('200003','200004','200005','200008','200011','200013','200014','200033','200034','200038','200044','200031','200032','200009')"): print(r)
def regra_of(cod,cl):
    r=[(p,AXR.get((p,cl))) for i,p,c2 in regras if c2==cl and cod.startswith(p)]
    return r
for k in ['+of:200005','+of:200038','+of:200044','+of:200011','+of:200008','+of:200034',' +nos:200003',' +nos:200033',' +nos:200013','+of:200014 +nos:200034','+of:200004','+of:200014','+of:200011,200038']:
    print('==',k,len(ex[k]))
    cl=k.split(':')[1].split(' ')[0].split(',')[0]
    vis=collections.Counter()
    for cod in ex[k]:
        ro=regra_of(cod,cl) if k.startswith('+of') else None
        e=d['ncm'].get(cod) or next((d['pref'][cod[:n]] for n in range(8,1,-1) if cod[:n] in d['pref']),None)
        vis[(str(ro), (e or {}).get('ax'), (e or {}).get('it'), (e or {}).get('ccl'), (e or {}).get('e'))]+=1
    for a,b in vis.most_common(12): print('  ',b,a)
