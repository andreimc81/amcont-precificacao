"""Compara duas versoes do Anexo VIII da NFS-e com o mesmo parser da base."""
import openpyxl, re, sys, json
def tx(x): return None if x is None else re.sub(r'\s+',' ',str(x)).strip()
def cc(x): return None if x is None else str(x).strip().zfill(6)
def ler(f):
    w=openpyxl.load_workbook(f,read_only=True,data_only=True); R=list(w['tabela geral'].iter_rows(values_only=True))
    lc={}; cur=None; grp=[]; nom={}; desc={}
    for r in R[1:]:
        r=list(r)+[None]*12
        it,dit,nb,dnb,_,_,indop,local,c,cn=[r[i] for i in range(10)]
        if it: cur={'d':tx(dit),'op':{},'n':{}, 'cx':[]}; lc[str(it).strip()]=cur; grp=[]
        if cur is None: continue
        if indop: cur['op'].setdefault(cc(indop),tx(local))
        if c: nom.setdefault(cc(c),tx(cn))
        if nb:
            k=re.sub(r'\D','',str(nb)); desc[k]=tx(dnb); ent=[k,cur['n'].setdefault(k,[])]
            if c:
                grp=[ent]
                if cc(c) not in ent[1]: ent[1].append(cc(c))
            else:
                if grp: ent[1].extend(x for x in grp[0][1] if x not in ent[1]); grp.append(ent)
                else: grp=[ent]
        elif c:
            for ent in grp:
                if cc(c) not in ent[1]: ent[1].append(cc(c))
            if not grp: cur['cx'].append(cc(c))
    return lc,nom,desc
a,na,da=ler(sys.argv[1]); b,nb_,db=ler(sys.argv[2])
out={'itens_novos':sorted(set(b)-set(a)),'itens_removidos':sorted(set(a)-set(b)),'pares_novos':[],'pares_removidos':[],'ccl_mudou':[],'indop_mudou':[],'desc_item':[],'ccl_nome_mudou':[],'ccl_novos':sorted(set(nb_)-set(na))}
for i in sorted(set(a)&set(b)):
    A,B=a[i],b[i]
    for k in sorted(set(B['n'])-set(A['n'])): out['pares_novos'].append([i,k,B['n'][k],db.get(k)])
    for k in sorted(set(A['n'])-set(B['n'])): out['pares_removidos'].append([i,k,A['n'][k],da.get(k)])
    for k in sorted(set(A['n'])&set(B['n'])):
        if sorted(A['n'][k])!=sorted(B['n'][k]): out['ccl_mudou'].append([i,k,A['n'][k],B['n'][k]])
    if A['op']!=B['op']: out['indop_mudou'].append([i,A['op'],B['op']])
    if A['d']!=B['d']: out['desc_item'].append([i,A['d'],B['d']])
for k in set(na)&set(nb_):
    if na[k]!=nb_[k]: out['ccl_nome_mudou'].append([k,na[k],nb_[k]])
print(json.dumps({k:(len(v) if isinstance(v,list) else v) for k,v in out.items()}))
print('pares v1.01:',sum(len(x['n']) for x in a.values()),'v1.02:',sum(len(x['n']) for x in b.values()),'itens',len(a),len(b))
json.dump(out,open(sys.argv[3],'w',encoding='utf-8'),ensure_ascii=False,indent=1)
