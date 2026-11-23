import json, openpyxl, subprocess
SP='/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/'
ROWS=[('A','regular',105,0.18,None,None,'N'),('B','sn_regular',100,0.12,0.0912,'II','S'),('C','sn_tradicional',92,0.18,0.0956,'III','N'),
      ('D','mei',90,0,None,None,'N'),('E','pf',100,0,None,None,'N'),('F','sn_tradicional',95,0.12,0.0703,'I','S'),('G','sn_sublimite',101,0.12,0.0703,'I','S'),('H','regular',97,0.04,None,None,'S')]
SC=[('produto','1806.31.10','presumido',2027,'uso','auto',0.17,'S'),('produto','1806.31.10','real',2030,'imobilizado','auto',0.12,'N'),
    ('produto','1806.31.10','simples_das',2027,'uso','auto',0.25,'S'),('produto','1806.31.10','presumido',2027,'revenda','auto'),('produto','1006.30.21','real',2029,'revenda','auto'),
    ('produto','1806.31.10','real',2026,'revenda','auto'),('produto','3004.90.99','real',2026,'revenda','auto'),
    ('produto','1806.31.10','simples_das',2030,'revenda','auto'),('produto','1806.31.10','simples_regular',2031,'uso','auto'),
    ('produto','2202.10.00','presumido',2033,'imobilizado','auto'),('servico','1.2301.22.00','presumido',2027,'revenda','auto'),
    ('servico','1.1502.10.00','simples_regular',2033,'uso','auto'),('produto','1806.31.10','real',2032,'uso','red60'),
    ('produto','1806.31.10','presumido',2026,'imobilizado','auto')]
res=[]
SC=[s if len(s)==8 else s+(0.17,'S') for s in SC]
for i,(tp,cod,reg,ano,dest,trat,isc,dup) in enumerate(SC):
    f=SP+'cc%d.xlsx'%i; wb=openpyxl.load_workbook('Amcont_Precificacao_Reforma_Tributaria.xlsx'); ws=wb['COMPRA']
    ws['B4']=ano; ws['B5']=reg; ws['B6']=dest; ws['B7']=tp; ws['B8']=cod; ws['B9']=trat; ws['B10']='auto'; ws['B12']=isc; ws['G12']=dup
    for k,row in enumerate(ROWS):
        for j,v in enumerate(row[:6],1): ws.cell(14+k,j,v)
        ws.cell(14+k,16,row[6])
    wb.save(f); subprocess.run(['python3','/mnt/skills/public/xlsx/scripts/recalc.py',f,'180'],capture_output=True)
    ws=openpyxl.load_workbook(f,data_only=True)['COMPRA']
    res.append({'red':ws['G7'].value,'pc':ws['G9'].value,'rows':[[ws.cell(14+k,j).value for j in range(7,18)] for k in range(len(ROWS))],'b24':ws['B24'].value,'b25':ws['B25'].value})
json.dump({'sc':SC,'rows':ROWS,'res':res},open(SP+'cross_compra.json','w'))
print('ok', res[0]['b24'], '|', res[0]['b25'])
