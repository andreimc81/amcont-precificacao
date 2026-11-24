import openpyxl, subprocess, json, shutil, time
SC=[ # tipo, codigo, regime, ativ_xlsx, ativ_html, aliq, ano, forn
 ('produto','10063021','presumido','comercio','comercio',0.18,2027,'regular'),
 ('produto','22030000','real','industria','industria',0.25,2027,'regular'),
 ('produto','04012010','presumido','comercio','comercio',0.12,2033,'regular'),
 ('produto','18063110','presumido','comercio','comercio',0.17,2029,'sn_regular'),
 ('servico','123012200','presumido','servicos com equiparacao hospitalar','hospitalar',0.03,2027,'regular'),
 ('servico','115021000','presumido','servicos em geral','servicos',0.05,2033,'regular'),
 ('servico','101011100','real','servicos em geral','servicos',0.04,2030,'mei'),
 ('produto','22021000','simples','comercio','comercio',0.18,2027,'regular'),
 ('servico','113011000','presumido','servicos em geral','servicos',0.05,2028,'pf'),
 ('produto','30049099','presumido','comercio','comercio',0.17,2031,'sn_tradicional'),
 ('produto','04012010','presumido','comercio','comercio',0.12,2027,'sn_tradicional'),
 ('produto','18063110','real','comercio','comercio',0.17,2030,'sn_tradicional'),
 ('produto','30049099','presumido','comercio','comercio',0.17,2027,'regular'),
 ('produto','87083090','real','comercio','comercio',0.17,2028,'regular'),
 ('produto','02013000','real','comercio','comercio',0.12,2029,'sn_regular'),
 ('produto','18063110','real','comercio','comercio',0.17,2026,'regular'),
 ('produto','30049099','simples','comercio','comercio',0.17,2026,'regular'),
 ('produto','40111000','simples','comercio','comercio',0.17,2027,'regular'),
 ('produto','30049099','presumido','industria','industria',0.17,2027,'regular','monofasico_fab'),
 ('produto','87083090','real','industria','industria',0.17,2026,'regular','monofasico_fab'),
 ('produto','33049910','simples','industria','industria',0.17,2026,'regular','monofasico_fab'),
 ('produto','40111000','simples','comercio','comercio',0.17,2028,'regular','monofasico_fab'),
 ('produto','22084000','presumido','industria','industria',0.25,2032,'regular'),
]
res=[]
for i,sc in enumerate(SC):
    tipo,cod,reg,ax,ah,aliq,ano,forn=sc[:8]; pcx=sc[8] if len(sc)>8 else 'auto'
    f=f'/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/x{i}.xlsx'
    wb=openpyxl.load_workbook('Amcont_Precificacao_Reforma_Tributaria.xlsx'); ws=wb['PRODUTO']
    ws['B4']=cod; ws['B17']=tipo; ws['B10']=reg; ws['B11']=ax; ws['B12']=aliq; ws['B13']=ano; ws['B20']=forn; ws['B15']='I'; ws['B25']=pcx; ws['E23']='N'  # testa a aliquota informada (B12); as perguntas tem teste proprio
    wb.save(f); subprocess.run(['python3','/mnt/skills/public/xlsx/scripts/recalc.py',f,'180'],capture_output=True)
    ws=openpyxl.load_workbook(f,data_only=True)['PRODUTO']
    res.append({'mc':ws['B47'].value,'nf':ws['B57'].value,'red':ws['B33'].value,'is':ws['B7'].value,'prova':ws['B67'].value,'cad':ws['G82'].value,'mc2':ws['G87'].value,'cadT':ws['F82'].value,'mc2T':ws['F87'].value,'sit':ws['E4'].value})
json.dump({'sc':SC,'res':res},open('cross_xlsx.json','w'))
print('ok')
