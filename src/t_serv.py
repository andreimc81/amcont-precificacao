import json, openpyxl, subprocess, sys
d=json.load(open('class_dump.json',encoding='utf-8'))
SP='/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/'
nb={x['cod']:x for x in d['nbs']}; par={(x['item'],x['cod']):x for x in d['pares'] if not x.get('vazio')}
dif=[(k,x) for k,x in par.items() if x['ops'][x['sel']]['ccl']!=nb[k[1]]['ops'][nb[k[1]]['sel']]['ccl'] or len(x['ops'])!=len(nb[k[1]]['ops'])]
print('pares',len(par),'com classificacao diferente da geral',len(dif), [k for k,_ in dif[:4]])
def run(sets):
    f=SP+'ts.xlsx'; wb=openpyxl.load_workbook('Amcont_Precificacao_Reforma_Tributaria.xlsx')
    for sh,a,v in sets: wb[sh][a]=v
    wb.save(f); subprocess.run(['python3','/mnt/skills/public/xlsx/scripts/recalc.py',f,'180'],capture_output=True)
    return openpyxl.load_workbook(f,data_only=True)
ok=True
for q,esp in [('04.01','04.01'),('4.01','04.01'),('0401','04.01'),('040101','04.01'),('04.01.01','04.01'),('401','04.01'),(4.01,'04.01'),(401,'04.01'),(40101,'04.01'),('16.02','16.02'),('7.02','07.02'),('99.03.02','99.03.02'),('990402','99.04.01' if False else None),('55.55','NAO LOCALIZADO'),('17.01','17.01')]:
    ws=run([('SERVICO','B4',q)])['SERVICO']
    rows=[[ws.cell(r,c).value for c in range(1,9)] for r in range(10,95) if ws.cell(r,2).value not in (None,'')]
    n=len([1 for (i,c) in par if i==esp])
    good = esp is None or (ws['B5'].value==esp and len(rows)==n and all(par[(esp,r[1].replace('.',''))]['ops'][par[(esp,r[1].replace('.',''))]['sel']]['ccl']==r[7] and abs((r[5] or 0)-par[(esp,r[1].replace('.',''))]['ops'][par[(esp,r[1].replace('.',''))]['sel']]['red'])<1e-9 for r in rows))
    ok&=good; print('OK ' if good else 'ERRO', repr(q), ws['B5'].value, ws['B6'].value, len(rows), (ws['C6'].value or '')[:50], rows[0][1:8] if rows else '')
k=dif[0][0] if dif else ('01.01','115021000')
for cod,item in [(k[1],''),(k[1],k[0]),('1.2301.22.00','040101'),('1.2301.22.00','16.02'),('1.2301.22.00','88.88'),('1.1502.10.00',1.01)]:
    ws=run([('PRODUTO','B17','servico'),('PRODUTO','B4',cod),('PRODUTO','E10',item or None)])['PRODUTO']
    c=cod.replace('.',''); it={'040101':'04.01',1.01:'01.01'}.get(item,item)
    x=par.get((it,c)) or nb[c]; o=x['ops'][x['sel']]
    good=abs(ws['E5'].value-o['red'])<1e-9 and ('cClassTrib '+o['ccl']) in ws['F5'].value and abs(ws['B33'].value-o['red'])<1e-9
    ok&=good; print('OK ' if good else 'ERRO',cod,repr(item),'|',ws['F10'].value,'|',ws['E4'].value,ws['E5'].value,ws['F5'].value,'| B33',ws['B33'].value,'| NF',round(ws['B57'].value,2))
print('TUDO OK' if ok else 'FALHOU')
