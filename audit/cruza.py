import re, json, collections
A=json.load(open('audit/anexos_docx.json',encoding='utf-8'))
D=json.load(open('class_dump.json',encoding='utf-8'))
U=[x['cod'] for x in D['ncm']]; B={x['cod']:x for x in D['ncm']}
COD=re.compile(r'(?<![\d.])(\d{2}\.\d{2}(?:\.\d{2}){0,2}|\d{4}(?:\.\d{1,2}){0,2})(?![\d])')
CAP=re.compile(r'[Cc]ap[íi]tulos?\s+(\d{1,2})(?:\s*(?:,|e)\s*(\d{1,2}))?(?:\s*(?:,|e)\s*(\d{1,2}))?')
EXC=re.compile(r'\b(exceto|excetuad|ressalvad)',re.I)
def norm(c): return c.replace('.','')
def tokens(txt):
    inc,exc=set(),set()
    for pm in re.finditer(r'\((?:exceto|excetuad|ressalvad)[^)]*\)',txt,re.I):
        for c in COD.findall(pm.group(0)):
            if len(norm(c))>=4: exc.add(norm(c))
    txt=re.sub(r'\((?:exceto|excetuad|ressalvad)[^)]*\)','',txt,flags=re.I)
    for seg in re.split(r';',txt):
        # parte antes e depois da palavra de exclusao
        m=EXC.search(seg); a,b=(seg[:m.start()],seg[m.start():]) if m else (seg,'')
        for part,dest in ((a,inc),(b,exc)):
            part=re.sub(r'\b1\.\d{4}(?:\.\d{1,2}){0,2}','',part)  # NBS
            for c in COD.findall(part):
                n=norm(c)
                if len(n)>=4: dest.add(n)
            for m2 in CAP.finditer(part):
                for g in m2.groups():
                    if g: dest.add(g.zfill(2))
    return inc,exc
NCMANX=['I','IV','V','VI','VII','VIII','IX','XI','XII','XIII','XV','XVII']
lei={}
for an in NCMANX:
    tab=A[an]['tab']; itens={}
    if an=='XVII':
        nome=None
        for r in tab:
            if len(r)==1 and not COD.search(r[0]): nome=r[0]; continue
            txt=' '.join(r); itens.setdefault(nome or '?','')
            itens[nome]+=' '+txt
    else:
        last=None
        for r in tab[1:]:
            if not r: continue
            it=r[0] if re.match(r'^\d+(\.\d+)?$',r[0]) else None
            txt=' ; '.join(r[1:]) if it else ' ; '.join(r)
            if it: last=it; itens[it]=txt
            elif last: itens[last]+=' ; '+txt
    lei[an]={}
    for it,txt in itens.items():
        inc,exc=tokens(txt)
        cov={u for u in U if any(u.startswith(p) for p in inc) and not any(u.startswith(p) for p in exc)}
        lei[an][it]={'txt':txt,'inc':sorted(inc),'exc':sorted(exc),'cov':cov}
# base: anexos citados por NCM
RX=re.compile(r'Anexo ([IVXL]+)(?:, item ([\w\.\- ]+?))?(?=$|[ |;:)]|,)')
base_an=collections.defaultdict(set)
for x in D['ncm']:
    for o in x['ops']:
        if o['red']==0 and o['ccl']=='000001' and not o['rot'].startswith('Anexo XVII') : continue
        for m in re.finditer(r'Anexo ([IVXL]+)',o['rot']+' '+(o['base'] or '')):
            base_an[x['cod']].add(m.group(1))
for x in D['ncm']:
    if x.get('is') or any('XVII' in o['rot'] for o in x['ops']): base_an[x['cod']].add('XVII')
rel={}
for an in NCMANX:
    cov=set().union(*[v['cov'] for v in lei[an].values()]) if lei[an] else set()
    nb={c for c,s in base_an.items() if an in s}
    rel[an]={'lei':len(cov),'base':len(nb),'so_lei':sorted(cov-nb),'so_base':sorted(nb-cov)}
    print('Anexo',an,'| itens',len(lei[an]),'| NCM cobertos pela lei',len(cov),'| na base',len(nb),'| so na lei',len(cov-nb),'| so na base',len(nb-cov))
json.dump({an:{k:v for k,v in r.items()} for an,r in rel.items()},open('audit/rel.json','w'),indent=0)
json.dump({an:{it:{'txt':v['txt'],'inc':v['inc'],'exc':v['exc'],'n':len(v['cov'])} for it,v in lei[an].items()} for an in lei},open('audit/lei_itens.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
