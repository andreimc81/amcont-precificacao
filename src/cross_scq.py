"""Planilha (perguntas E17 a E23 da aba PRODUTO) contra a calculadora (resolverSC). Grava cross_scq.json."""
import openpyxl, subprocess, shutil, json, itertools, random
SRC='Amcont_Precificacao_Reforma_Tributaria.xlsx'; TMP='/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/scq.xlsx'
random.seed(17)
cods=['02061000','02011000','02031100','22030000','84713012','61091000','17011400','08061000','10063021','11010010','11062000','04061010','02068000','07051100','08081000','04072100','04011010','69041000','87021000','84798999','84329000','72142000','25171000','03073100','33049910','27101259','22071090','27111910','84714900','84439199','84128000','88010000','87019490']
casos=[]
for c in cods:
    for _ in range(3):
        casos.append({'cod':c,'ben':random.choice('ABCDE'),'dest':random.choice(['contribuinte','contribuinte_uso','final','final','orgao_sc']),'desc':random.choice('SN'),'c7':random.choice('SN'),
                      'orig':random.choice(['sc','outro_estado','importacao']),'ativ':random.choice(['comercio','fabricante'])})
out=[]
for k in casos:
    shutil.copy(SRC,TMP); w=openpyxl.load_workbook(TMP); ws=w['PRODUTO']
    ws['B4']=k['cod'][:4]+'.'+k['cod'][4:6]+'.'+k['cod'][6:]; ws['B17']='produto'; ws['E12']='SC'
    ws['E13']=k['dest']; ws['E17']=k['desc']; ws['E19']=k['c7']; ws['E20']=k['orig']; ws['E21']=k['ativ']; ws['E23']='S'; ws['E24']=k['ben']
    w.save(TMP); subprocess.run(['python3','/mnt/skills/public/xlsx/scripts/recalc.py',TMP,'120'],capture_output=True)
    v=openpyxl.load_workbook(TMP,data_only=True)['PRODUTO']; k['xlsx']=v['E22'].value; k['i17']=v['I17'].value; out.append(k)
json.dump(out,open('cross_scq.json','w'),ensure_ascii=False); print(len(out))
