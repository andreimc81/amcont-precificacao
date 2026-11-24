# Cruzamento ampliado planilha x calculadora: 80 cenarios aleatorios (semente fixa), incluindo venda interestadual
import openpyxl, subprocess, json, random
random.seed(2026)
P=['10063021','22030000','04012010','18063110','22021000','30049099','87083090','02013000','40111000','33049910',
   '22084000','08119000','15079011','84713012','94036000','61091000','19053100','21069090','90221411','03061200']
S=['123012200','115021000','101011100','113011000','122051900','125060000']
UFS=['RS','PR','SP','RJ','MG','BA','PE','GO','AM','ES','DF','SE','AL']
SC=[]
for k in range(80):
    tipo='produto' if random.random()<0.75 else 'servico'
    cod=random.choice(P if tipo=='produto' else S)
    reg=random.choice(['presumido','real','simples'])
    if tipo=='produto': ax,ah=random.choice([('comercio','comercio'),('industria','industria')]); aliq=random.choice([0.07,0.12,0.17,0.25])
    else: ax,ah=random.choice([('servicos em geral','servicos'),('servicos com equiparacao hospitalar','hospitalar')]); aliq=random.choice([0.02,0.03,0.05])
    ano=random.choice(range(2026,2034)); forn=random.choice(['regular','sn_regular','sn_tradicional','sn_sublimite','mei','pf'])
    das=random.choice([0.04,0.073,0.095,0.12]); pcx=random.choice(['auto','auto','normal','monofasico','monofasico_fab'])
    if tipo=='servico': pcx=random.choice(['auto','auto','normal'])  # R22-02: monofásico e alíquota zero não existem para serviço
    uf,dt,imp,dup='SC','contribuinte','N','S'
    if tipo=='produto' and random.random()<0.4:
        uf=random.choice(UFS); dt=random.choice(['contribuinte','contribuinte_uso','final']); imp=random.choice(['N','N','S']); dup=random.choice(['S','N'])
    SC.append(dict(tipo=tipo,cod=cod,reg=reg,ax=ax,ah=ah,aliq=aliq,ano=ano,forn=forn,das=das,pcx=pcx,uf=uf,dt=dt,imp=imp,dup=dup))
res=[]
for i,s in enumerate(SC):
    f=f'/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/am{i}.xlsx'
    wb=openpyxl.load_workbook('Amcont_Precificacao_Reforma_Tributaria.xlsx'); ws=wb['PRODUTO']
    ws['B4']=s['cod']; ws['B17']=s['tipo']; ws['B10']=s['reg']; ws['B11']=s['ax']; ws['B12']=s['aliq']; ws['B13']=s['ano']; ws['B20']=s['forn']; ws['E23']='N'  # testa a aliquota informada (B12); as perguntas tem teste proprio
    ws['B22']=s['das']; ws['B23']='I'; ws['B15']='I'; ws['B25']=s['pcx']; ws['E12']=s['uf']; ws['E13']=s['dt']; ws['E14']=s['imp']; ws['E15']=s['dup']
    wb.save(f); subprocess.run(['python3','/mnt/skills/public/xlsx/scripts/recalc.py',f,'180'],capture_output=True)
    w=openpyxl.load_workbook(f,data_only=True)['PRODUTO']
    res.append({'mc':w['B47'].value,'nf':w['B57'].value,'hib':w['C83'].value,'red':w['B33'].value,'is':w['B7'].value,'prova':w['B67'].value,'i17':w['I17'].value,'nfprova':w['G66'].value})
json.dump({'sc':SC,'res':res},open('cross_amplo.json','w'))
print('ok',len(res))
