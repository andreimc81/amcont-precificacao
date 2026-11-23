import json, openpyxl, subprocess
SP='/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/'
SC=[('presumido',2027,'RS','contribuinte','N','S'),('presumido',2029,'BA','final','N','S'),('real',2027,'RJ','final','N','N'),
    ('real',2026,'SP','contribuinte_uso','N','S'),('presumido',2033,'PE','final','S','S'),('simples',2027,'SE','final','N','S'),('presumido',2031,'SC','final','N','S')]
res=[]
for i,(reg,ano,uf,dt,imp,dup) in enumerate(SC):
    f=SP+'uf%d.xlsx'%i; wb=openpyxl.load_workbook('Amcont_Precificacao_Reforma_Tributaria.xlsx'); ws=wb['PRODUTO']
    ws['B4']='1806.31.10'; ws['B17']='produto'; ws['B10']=reg; ws['B13']=ano; ws['E12']=uf; ws['E13']=dt; ws['E14']=imp; ws['E15']=dup; ws['E23']='N'  # testa a aliquota informada (B12); as perguntas tem teste proprio
    wb.save(f); subprocess.run(['python3','/mnt/skills/public/xlsx/scripts/recalc.py',f,'180'],capture_output=True)
    w=openpyxl.load_workbook(f,data_only=True)['PRODUTO']
    res.append({'nf':w['B57'].value,'mc':w['B47'].value,'i17':w['I17'].value,'prova':w['B67'].value,'f12':w['F12'].value,'g64':w['G64'].value,'c83':w['C83'].value})
json.dump({'sc':SC,'res':res},open(SP+'cross_uf.json','w')); print('ok')
