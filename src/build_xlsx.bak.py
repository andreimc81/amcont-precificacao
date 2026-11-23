# Leva o banco fiscal e a busca automatica para a planilha, sobre o arquivo atual.
import json, re, openpyxl
from copy import copy
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter as L
d=json.load(open('class_dump.json',encoding='utf-8'))
wb=openpyxl.load_workbook('plan_orig.xlsx')
PET='FF2A5F6B'; CLARO='FFD6E8EB'
f_h=Font(name='Arial',size=10,bold=True,color='FFFFFFFF'); fill_h=PatternFill('solid',fgColor=PET)
f_n=Font(name='Arial',size=9); f_b=Font(name='Arial',size=10,bold=True); f_10=Font(name='Arial',size=10)
f_in=Font(name='Arial',size=10,bold=True,color='FF0000FF'); fill_in=PatternFill('solid',fgColor='FFFFF2CC')
thin=Side(style='thin',color='FFC4CFCE'); box=Border(left=thin,right=thin,top=thin,bottom=thin)
fill_c=PatternFill('solid',fgColor=CLARO)
def pct(r): return 'aliquota zero' if r==1 else ('reducao de %d%%'%round(r*100) if r>0 else 'integral')
SIT={'Integral':'INTEGRAL','Conferir':'CONFERIR','Escolher':'ESCOLHER','Não localizado':'NAO LOCALIZADO'}
def titulo(ws,txt,ncol,sub=None):
    ws['A1']=txt; ws['A1'].font=Font(name='Arial',size=14,bold=True,color='FFFFFFFF'); ws['A1'].fill=fill_h
    ws.merge_cells(start_row=1,start_column=1,end_row=1,end_column=ncol); ws.row_dimensions[1].height=30
    ws['A1'].alignment=Alignment(vertical='center')
    if sub:
        ws['A2']=sub; ws['A2'].font=Font(name='Arial',size=9,italic=True); ws.merge_cells(start_row=2,start_column=1,end_row=2,end_column=ncol)
        ws['A2'].alignment=Alignment(wrap_text=True,vertical='top'); ws.row_dimensions[2].height=40
def cab(ws,row,cols,widths):
    for i,(c,w) in enumerate(zip(cols,widths),1):
        x=ws.cell(row,i,c); x.font=f_h; x.fill=fill_h; x.alignment=Alignment(wrap_text=True,vertical='center'); ws.column_dimensions[L(i)].width=w
    ws.freeze_panes=ws.cell(row+1,2)
def outras(x):
    o=[]
    for i,op in enumerate(x['ops']):
        if i==x['sel']: continue
        o.append('%s, CST %s, cClassTrib %s (%s)'%(pct(op['red']),op['cst'],op['ccl'],op['rot']))
    return ' | '.join(o)
AVISO='Apoio a classificacao. O codigo nao decide sozinho: o beneficio depende da condicao, de quem compra, da destinacao e da operacao. Fontes: '+'; '.join(d['meta']['fontes'])

# ---------------- BD_NCM ----------------
for n in ['BD_NCM','BD_NBS','BD_LC116','BD_CCLASSTRIB','BD_IS','BD_REGRAS','CLASSIFICACAO']:
    if n in wb.sheetnames: del wb[n]
ws=wb.create_sheet('BD_NCM'); ws.sheet_properties.tabColor='4A8FA0'
titulo(ws,'BASE DE NCM  |  REGRA DE CBS E IBS POR CODIGO',14,AVISO)
cab(ws,3,['NCM','Descricao','Situacao','Anexo e item','Reducao aplicada','CST','cClassTrib','Base legal','Condicao','O que confirmar','Outras classificacoes possiveis','IS 2027','Nota do Imposto Seletivo','Avisos','ICMS SC consumidor final','ICMS SC contribuinte','ICMS SC: regras, beneficios e notas','PIS/COFINS hoje','PIS/COFINS hoje: base legal e restricao','PIS+COFINS do fabricante ou importador (monofasico)'],
    [11,46,13,30,10,7,22,34,60,44,60,9,46,60,11,11,80,14,70,14])
PCN={'normal':'normal','mono':'monofasico','zero':'zero'}
def pc_cols(x):
    q=x.get('pc')
    if not q: return ['normal','','']
    nota=' | '.join(v for v in [q.get('grupo') or q.get('desc') or '',q.get('base',''),q.get('obs',''),'pela descricao ou Ex da TIPI' if q.get('ind') else ''] if v)
    return [PCN[q['reg']],nota,(round(q['conc'],6) if q.get('conc') else '')]
def sc_cols(x):
    sc=x.get('sc')
    if not sc: return ['','','']
    ops=sc['ops']; cf=ops[0]['aliq']
    ct=next((o['aliq'] for o in ops if o['rot'].startswith('Contribuinte')),cf)
    txt=' | '.join(('isento' if o['aliq']==0 else ('%g%%'%(o['aliq']*100)).replace('.',','))+': '+o['rot']+' ('+o['base']+(('; ate 31/12/%d'%o['fim']) if o.get('fim') else '')+')' for o in ops)
    return [cf,ct,txt+((' | '+' '.join(sc['notas'])) if sc['notas'] else '')]
r=4
for x in d['ncm']:
    o=x['ops'][x['sel']]; ex=dict(x['extra'])
    row=[x['cod'],x['desc'],SIT[x['selo']],o['rot'],o['red'],o['cst'],o['ccl'],o['base'],o['cond'] or x['msg'],ex.get('O que confirmar',''),outras(x),
         (x['is'] if x['is'] is not None else ('informar' if x['temIs'] else '')),x['isNota'],' | '.join(x['avisos'])]+sc_cols(x)+pc_cols(x)
    for i,v in enumerate(row,1):
        c=ws.cell(r,i,v); c.font=f_n
        if i in (1,6,7): c.number_format='@'
        if i in (5,15,16): c.number_format='0%'
        if i==20: c.number_format='0.00%'
        if i==12 and isinstance(v,float): c.number_format='0.0%'
    r+=1
NCM_LAST=r-1; ws.auto_filter.ref='A3:T%d'%NCM_LAST
# ---------------- BD_NBS ----------------
ws=wb.create_sheet('BD_NBS'); ws.sheet_properties.tabColor='4A8FA0'
titulo(ws,'BASE DE NBS  |  REGRA DE CBS E IBS POR SERVICO, COM ITEM DA LC 116 E INDOP',13,AVISO)
cab(ws,3,['NBS','NBS formatado','Descricao','Situacao','Classificacao sugerida','Reducao aplicada','CST','cClassTrib','Base legal','Condicao','Outras classificacoes possiveis','Item da LC 116','indOp possiveis','Avisos'],
    [11,14,50,13,34,10,7,12,30,56,70,46,44,60])
r=4
for x in d['nbs']:
    o=x['ops'][x['sel']]; ex=dict(x['extra']); c0=x['cod']
    row=[c0,c0[0]+'.'+c0[1:5]+'.'+c0[5:7]+'.'+c0[7:],x['desc'],SIT[x['selo']],o['rot'],o['red'],o['cst'],o['ccl'],o['base'],o['cond'] or x['msg'],outras(x),
         ex.get('Item da LC 116',''),ex.get('indOp possíveis',''),' | '.join(x['avisos'])]
    for i,v in enumerate(row,1):
        c=ws.cell(r,i,v); c.font=f_n
        if i in (1,2,7,8): c.number_format='@'
        if i==6: c.number_format='0%'
    r+=1
NBS_LAST=r-1; ws.auto_filter.ref='A3:N%d'%NBS_LAST
# ---------------- BD_LC116 ----------------
ws=wb.create_sheet('BD_LC116'); ws.sheet_properties.tabColor='4A8FA0'
titulo(ws,'ITEM DA LC 116  x  NBS  x  INDOP  x  CCLASSTRIB  (Anexo VIII, versao 1.01.00)',7,'Uma linha por par item e NBS. Use o filtro para achar a NBS a partir do item da lista de servicos.')
cab(ws,3,['Item LC 116','Descricao do item','NBS','Descricao da NBS','cClassTrib possiveis','indOp possiveis','Local de incidencia do IBS'],[10,50,14,60,26,28,50])
r=4
for it in d['lc']:
    for cod,ccl in it['n']:
        cc=ccl+it.get('cx',[])
        row=[it['i'],it['d'],cod[0]+'.'+cod[1:5]+'.'+cod[5:7]+'.'+cod[7:],d['nbsDesc'].get(cod,''),', '.join(cc) or 'nao informado no Anexo VIII',
             ', '.join(o[0] for o in it['op']),'; '.join(sorted({o[1] for o in it['op'] if o[1]}))]
        for i,v in enumerate(row,1):
            c=ws.cell(r,i,v); c.font=f_n; c.number_format='@'
        r+=1
ws.auto_filter.ref='A3:G%d'%(r-1)
# ---------------- BD_CCLASSTRIB ----------------
ws=wb.create_sheet('BD_CCLASSTRIB'); ws.sheet_properties.tabColor='4A8FA0'
titulo(ws,'TABELA DE CCLASSTRIB  |  CST, NOME E REDUCAO',5,'Nomes e percentuais da tabela de 23/01/2026. Os codigos usados nas regras por NCM e NBS seguem a IT 2025.002 v1.70. Confira a tabela oficial vigente antes de emitir documento fiscal.')
cab(ws,3,['cClassTrib','CST','Nome','Reducao de IBS e CBS','Fundamento na LC 214/2025'],[12,7,90,12,30])
r=4
for k in sorted(d['ccl']):
    v=d['ccl'][k]
    for i,val in enumerate([k,v[0],v[1],v[2] if v[2] is not None else 'conferir',v[3]],1):
        c=ws.cell(r,i,val); c.font=f_n
        if i<3: c.number_format='@'
        if i==4 and isinstance(val,(int,float)): c.number_format='0%'
    r+=1
# ---------------- BD_IS ----------------
ws=wb.create_sheet('BD_IS'); ws.sheet_properties.tabColor='4A8FA0'
titulo(ws,'IMPOSTO SELETIVO  |  ALIQUOTAS DE 2027 (MP 1.399/2026)',3,'Extraido de fonte secundaria e sujeito a conversao da MP em lei. Cobranca a partir de fevereiro de 2027. Vale so para NCM do Anexo XVII da LC 214/2025. Confira os Anexos IV e V da MP antes de usar.')
cab(ws,3,['Prefixo de NCM','Aliquota ad valorem','Regra'],[14,14,120])
r=4
for p_,a,n in d['is']:
    ws.cell(r,1,p_).number_format='@'; c=ws.cell(r,2,a if a is not None else 'informar'); c.number_format='0.0%'; ws.cell(r,3,n)
    for i in (1,2,3): ws.cell(r,i).font=f_n
    r+=1
# ---------------- BD_REGRAS ----------------
ws=wb.create_sheet('BD_REGRAS'); ws.sheet_properties.tabColor='4A8FA0'
titulo(ws,'CASOS EM QUE O CODIGO NAO DECIDE  |  30 REGRAS SEM LISTA DE NCM OU NBS',8,'A lei reduz, zera ou suspende o IBS e a CBS conforme o produto, quem compra, a operacao e o regime. Leia antes de confiar em um resultado INTEGRAL.')
cab(ws,3,['No','Regra','Base legal','CST','cClassTrib','Reducao (%)','Tipo','Observacao'],[5,60,50,8,26,12,24,90])
r=4
for reg in d['regras']:
    for i,v in enumerate(reg,1):
        c=ws.cell(r,i,v); c.font=f_n; c.alignment=Alignment(wrap_text=True,vertical='top')
    r+=1

# ---------------- CLASSIFICACAO (consulta em lote) ----------------
ws=wb.create_sheet('CLASSIFICACAO', wb.sheetnames.index('PRODUTO')); ws.sheet_properties.tabColor='2A5F6B'
titulo(ws,'CLASSIFICACAO  |  CONSULTA EM LOTE POR NCM OU NBS',20,
 'Cole ou digite os codigos na coluna A, com ou sem pontos: 8 digitos para NCM (produto) e 9 digitos para NBS (servico). A planilha busca a regra de CBS e IBS, o cClassTrib, o Imposto Seletivo e a aliquota interna de ICMS de Santa Catarina. Situacao CONFERIR ou ESCOLHER exige confirmar a condicao antes de formar o preco.')
cols=['Codigo (cole aqui)','Tipo','Descricao','Situacao','Classificacao','Reducao de CBS e IBS','CST','cClassTrib','Base legal','Condicao','Outras classificacoes possiveis','IS 2027','Observacoes (IS, LC 116, indOp, avisos)','chave','linha','ICMS SC consumidor final','ICMS SC contribuinte','ICMS SC: regras, beneficios e notas','PIS/COFINS hoje','PIS/COFINS hoje: base legal e restricao']
cab(ws,3,cols,[18,9,44,15,30,11,7,20,30,56,56,9,60,11,7,11,11,80,14,70])
NR=f'$A$4:$A${NCM_LAST}'; SR=f'$A$4:$A${NBS_LAST}'
def ix(sheet,col,last): return f"INDEX({sheet}!${col}$4:${col}${last},$O{{r}})"
N=lambda col: ix('BD_NCM',col,NCM_LAST); S=lambda col: ix('BD_NBS',col,NBS_LAST)
exemplos=['1006.30.21','2202.10.00','1806.31.10','3004.90.99','1.2301.22.00','1.1502.10.00']
for k in range(300):
    r=4+k
    a=ws.cell(r,1,exemplos[k] if k<len(exemplos) else None); a.number_format='@'; a.font=f_in; a.fill=fill_in; a.border=box
    ws.cell(r,14,f'=IF($A{r}="","",IF(ISNUMBER($A{r}),IF($A{r}<100000000,TEXT($A{r},"00000000"),TEXT($A{r},"0")),SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(TRIM($A{r}),".","")," ",""),"-","")))')
    ws.cell(r,2,f'=IF($N{r}="","",IF(LEN($N{r})=8,"NCM",IF(LEN($N{r})=9,"NBS","INVALIDO")))')
    ws.cell(r,15,f'=IF($B{r}="NCM",IFERROR(MATCH($N{r},BD_NCM!{NR},0),0),IF($B{r}="NBS",IFERROR(MATCH($N{r},BD_NBS!{SR},0),0),0))')
    def both(nc,sc,vazio='""'):
        return (f'=IF(OR($B{r}="",$B{r}="INVALIDO"),{vazio},IF($O{r}=0,{vazio},IF($B{r}="NCM",{N(nc).format(r=r)},{S(sc).format(r=r)})))')
    ws.cell(r,3,both('B','C'))
    ws.cell(r,4,f'=IF($B{r}="","",IF($B{r}="INVALIDO","INVALIDO: use 8 ou 9 digitos",IF($O{r}=0,"NAO LOCALIZADO",IF($B{r}="NCM",{N("C").format(r=r)},{S("D").format(r=r)}))))')
    ws.cell(r,5,both('D','E')); ws.cell(r,6,both('E','F')); ws.cell(r,7,both('F','G')); ws.cell(r,8,both('G','H'))
    ws.cell(r,9,both('H','I')); ws.cell(r,10,both('I','J')); ws.cell(r,11,both('K','K'))
    ws.cell(r,12,f'=IF(OR($B{r}<>"NCM",$O{r}=0),"",IF({N("L").format(r=r)}="","",{N("L").format(r=r)}))')
    ws.cell(r,13,f'=IF(OR($B{r}="",$B{r}="INVALIDO",$O{r}=0),"",IF($B{r}="NCM",TRIM({N("M").format(r=r)}&" "&{N("N").format(r=r)}),TRIM("LC 116: "&{S("L").format(r=r)}&" | indOp: "&{S("M").format(r=r)}&" "&{S("N").format(r=r)})))')
    for cc,col in ((16,'O'),(17,'P'),(18,'Q'),(19,'R'),(20,'S')):
        ws.cell(r,cc,f'=IF(OR($B{r}<>"NCM",$O{r}=0),"",IF({N(col).format(r=r)}="","",{N(col).format(r=r)}))')
        ws.cell(r,cc).font=f_n
        if cc<18: ws.cell(r,cc).number_format='0%'
    for c in range(2,16):
        x=ws.cell(r,c); x.font=f_n
        if c==6: x.number_format='0%;;0%'
        if c==12: x.number_format='0.0%'
        if c in (7,8): x.number_format='@'
ws.column_dimensions['N'].hidden=True; ws.column_dimensions['O'].hidden=True
from openpyxl.formatting.rule import FormulaRule
for txt,cor in [('INTEGRAL','FFD9EAD3'),('CONFERIR','FFFFF2CC'),('ESCOLHER','FFF4CCCC'),('NAO LOCALIZADO','FFD9D9D9')]:
    ws.conditional_formatting.add('D4:D303',FormulaRule(formula=[f'LEFT($D4,{len(txt)})="{txt}"'],fill=PatternFill('solid',bgColor=cor,fgColor=cor)))

# ---------------- PARAMETROS ----------------
wp=wb['PARAMETROS']
assert wp['B33'].value==0.092 and wp['B39'].value==0.093 and wp['A59'].value=='transporte de passageiros' and wp['E59'].value==0.6
wp['B33']=0.112; wp['B34']=0.112
for r in range(35,40): wp.cell(r,2,0.113)
wp['E59']=0.4
wp['E32']='CBS provisoria: 11,3% calculados pelo TCU (Acordao 2933/2026); 11,2% em 2027 e 2028.'; wp['E33']='Aguarda resolucao do Senado. Atualize a coluna B quando sair.'
wp['F59']='Intermunicipal e interestadual: 40% (art. 286). Urbano e isento: nao simular.'
for a in ('E32','E33','F59'): wp[a].font=Font(name='Arial',size=9,italic=True,color='FFA63D1B')

# ---------------- PRODUTO ----------------
ws=wb['PRODUTO']
# 1) servico: ICMS da compra nao gera credito; IS nao se aplica
for row in ws.iter_rows():
    for c in row:
        if isinstance(c.value,str) and c.value.startswith('=') and '$B$21' in c.value:
            c.value=re.sub(r'(?<![!A-Za-z])\$B\$21(?!\d)','($B$21*IF($B$17="servico",0,1))',c.value)
# credito de ICMS de fornecedor do Simples tradicional: so o ICMS pago no DAS (LC 123, art. 23)
SN_ICMS='$B$22*INDEX(PARAMETROS!$F$72:$F$76,MATCH($B$23,PARAMETROS!$A$72:$A$76,0))*IF($B$17="servico",0,1)'
pat=re.compile(r'IF\(OR\((\$B\$20|"[a-z_]+")="mei",\1="pf"\),0,(\$B\$\d+)\*\(\$B\$21\*IF\(\$B\$17="servico",0,1\)\)\*(\$B\$32|1)\)')
nsub=0
for row in ws.iter_rows():
    for c in row:
        if isinstance(c.value,str) and c.value.startswith('='):
            v,n=pat.subn(lambda m:'IF(OR(%s="mei",%s="pf"),0,IF(%s="sn_tradicional",%s*%s*%s,%s*($B$21*IF($B$17="servico",0,1))*%s))'%(m.group(1),m.group(1),m.group(1),m.group(2),SN_ICMS,m.group(3),m.group(2),m.group(3)),c.value)
            if n: c.value=v; nsub+=n
assert nsub==7,nsub
# ===== ajustes da validacao legal de 10/11/2026 =====
# credito de CBS e IBS da compra: base sem o ICMS (LC 214, art. 12, par. 2, V)
G='$B$24/(1+(B30+B31)*(1-B33))*(B30+B31)*(1-B33)'; n2=0
for row in ws.iter_rows():
    for c in row:
        if isinstance(c.value,str) and G in c.value:
            n2+=c.value.count(G); c.value=c.value.replace(G,'(1-($B$21*IF($B$17="servico",0,1))*$B$32)*'+G)
assert n2==6,n2
assert ws['B54'].value=='=(1-B36)*(B34+B35)'; ws['B54']='=(1-B36)*(B34+B35)/(1+B34+B35)'; ws['A54']='Fator k, peso de CBS e IBS (fora da propria base, art. 12)'
assert ws['B55'].value.startswith('=(1-B54)/(1+'); ws['B55']='=IF($B$13<2027,0,$B$7)*(1-B36-B54)/(1+IF($B$13<2027,0,$B$7))'; ws['A55']='Peso do Imposto Seletivo na nota (base sem ICMS, CBS e IBS, art. 417)'
assert ws['B56'].value.startswith('=1-B36-B54-B55*('); ws['B56']='=1-B36-B54-B55-B37*(1-B54-B55)'
assert ws['B60'].value=='=IF($B$10="simples",0,B57*(1-B36)*B34)'; ws['B60']='=IF($B$10="simples",0,B57*(1-B36)/(1+B34+B35)*B34)'
assert ws['B61'].value=='=IF($B$10="simples",0,B57*(1-B36)*B35)'; ws['B61']='=IF($B$10="simples",0,B57*(1-B36)/(1+B34+B35)*B35)'
assert ws['B62'].value.startswith('=IF($B$10="simples",0,B57*B55*'); ws['B62']='=IF($B$10="simples",0,B57*B55)'
assert ws['B63'].value=='=IF($B$10="simples",0,B57*B55*B37)'; ws['B63']='=IF($B$10="simples",0,B57*B37*(1-B54-B55))'
wp0=wb['PARAMETROS']; assert wp0['B5'].value.startswith('1 - Professor'); wp0['B5']='2 - LC 214 art. 12 par. 2 (exclui CBS/IBS da propria base)'
wl0=wb['LEIA-ME']
wl0['B32']='Premissa padrao alterada em 10/11/2026 para a 2 (LC 214, art. 12, par. 2). A premissa 1 reproduz o material de referencia,'
wl0['B33']='mas inclui a CBS e o IBS na propria base, o que contraria a lei. Motor atual: 55 de 66 pontos iguais ao material; os 11 restantes sao correcoes.'
assert ws['B42'].value.startswith('=IF($B$10="simples",0,($B$27-B41)*')
for a in ('B42','B43'): ws[a].value=ws[a].value.replace('($B$27-B41)','($B$27-IF($B$17="servico",0,B41))')
def inp(a,v):
    ws[a]=v; ws[a].font=copy(ws['B6'].font); ws[a].fill=copy(ws['B6'].fill); ws[a].border=copy(ws['B6'].border); ws[a].alignment=copy(ws['B6'].alignment)
def lab(a,v,bold=True):
    ws[a]=v; ws[a].font=Font(name='Arial',size=10,bold=bold)
def calc(a,v,fmt=None,wrap=False):
    ws[a]=v; ws[a].font=Font(name='Arial',size=10,color='FF000000'); ws[a].fill=fill_c
    ws[a].alignment=Alignment(wrap_text=wrap,vertical='top',horizontal='left')
    if fmt: ws[a].number_format=fmt
ws['A1']='PRECO DE UM PRODUTO OU SERVICO  |  COMPRA, VENDA E MARGEM DE CONTRIBUICAO'
ws['A3']='O PRODUTO OU SERVICO'
lab('A4','NCM (8 digitos) ou NBS (9 digitos), com ou sem pontos'); ws['B4'].number_format='@'
lab('A5','Descricao pela base')
ws['B5']='=IF($I$7=0,"codigo nao localizado na base",IF($B$17="servico",INDEX(BD_NBS!$C$4:$C$%d,$I$7),INDEX(BD_NCM!$B$4:$B$%d,$I$7)))'%(NBS_LAST,NCM_LAST)
ws['B5'].font=Font(name='Arial',size=10); ws['B5'].fill=PatternFill(fill_type=None); ws['B5'].border=Border()
lab('A6','Tratamento de CBS e IBS (auto, integral, red30, red60, red70, sem)'); inp('B6','auto'); ws['C6']=None
lab('A7','Imposto Seletivo aplicado (automatico; manual em G7)'); ws['C7']=None
ws['B7']='=IF($B$17="servico",0,IF($G$7<>"",$G$7,IF(ISNUMBER($E$7),$E$7,0)))'
ws['B7'].font=Font(name='Arial',size=10,color='FF000000'); ws['B7'].fill=PatternFill(fill_type=None); ws['B7'].border=Border()
ws['A8']='Em "auto" a reducao vem da base pelo codigo. O codigo nao decide sozinho: confira a condicao em E8 e a aba CLASSIFICACAO.'
lab('A12','Aliquota de ICMS (produto) ou de ISS (servico) na sua venda')
lab('A17','Tipo do item (produto ou servico)'); inp('B17','produto')
lab('A18','A COMPRA DESTE PRODUTO OU OS INSUMOS DO SERVICO') if False else None
# validacoes
for dv in ws.data_validations.dataValidation:
    if 'B6' in str(dv.sqref): dv.formula1='"auto,integral,red30,red60,red70,sem"'
dv=DataValidation(type='list',formula1='"produto,servico"',allow_blank=False); ws.add_data_validation(dv); dv.add('B17')
# 2) reducao automatica
old=ws['B33'].value; assert old.startswith('=INDEX(PARAMETROS!$B$43:$B$47')
ws['B33']='=IF($B$6="auto",IF($I$7=0,0,$E$5),'+old[1:]+')'
# 3) ficha da base em D4:G8 e auxiliares em I
for col,w in (('D',24),('E',16),('F',16),('G',34),('H',3),('I',12)): ws.column_dimensions[col].width=w
lab('D4','SITUACAO NA BASE');  ws.merge_cells('E4:G4')
calc('E4','=IF($I$7=0,"NAO LOCALIZADO: confira o codigo e o tipo em B17",IF($B$17="servico",INDEX(BD_NBS!$D$4:$D$%d,$I$7),INDEX(BD_NCM!$C$4:$C$%d,$I$7)))'%(NBS_LAST,NCM_LAST))
lab('D5','Reducao pela base')
calc('E5','=IF($I$7=0,0,IF($B$17="servico",INDEX(BD_NBS!$F$4:$F$%d,$I$7),INDEX(BD_NCM!$E$4:$E$%d,$I$7)))'%(NBS_LAST,NCM_LAST),'0%')
ws.merge_cells('F5:G5')
calc('F5','=IF($I$7=0,"","CST "&IF($B$17="servico",INDEX(BD_NBS!$G$4:$G$%d,$I$7),INDEX(BD_NCM!$F$4:$F$%d,$I$7))&"  |  cClassTrib "&IF($B$17="servico",INDEX(BD_NBS!$H$4:$H$%d,$I$7),INDEX(BD_NCM!$G$4:$G$%d,$I$7)))'%(NBS_LAST,NCM_LAST,NBS_LAST,NCM_LAST))
lab('D6','Classificacao e base legal'); ws.merge_cells('E6:G6')
calc('E6','=IF($I$7=0,"",IF($B$17="servico",INDEX(BD_NBS!$E$4:$E$%d,$I$7)&"  |  "&INDEX(BD_NBS!$I$4:$I$%d,$I$7),INDEX(BD_NCM!$D$4:$D$%d,$I$7)&"  |  "&INDEX(BD_NCM!$H$4:$H$%d,$I$7)))'%(NBS_LAST,NBS_LAST,NCM_LAST,NCM_LAST))
lab('D7','IS sugerido para 2027')
calc('E7','=IF(OR($I$7=0,$B$17="servico"),"",IF(INDEX(BD_NCM!$L$4:$L$%d,$I$7)="","",INDEX(BD_NCM!$L$4:$L$%d,$I$7)))'%(NCM_LAST,NCM_LAST),'0.0%')
lab('F7','IS manual (opcional) ->'); ws['F7'].alignment=Alignment(horizontal='right')
inp('G7',None); ws['G7'].number_format='0.00%'
lab('D8','Condicao e alternativas'); ws.merge_cells('E8:G8')
calc('E8','=IF($I$7=0,"",IF($B$17="servico",INDEX(BD_NBS!$J$4:$J$%d,$I$7)&IF(INDEX(BD_NBS!$K$4:$K$%d,$I$7)="",""," || Outras: "&INDEX(BD_NBS!$K$4:$K$%d,$I$7)),INDEX(BD_NCM!$I$4:$I$%d,$I$7)&IF(INDEX(BD_NCM!$K$4:$K$%d,$I$7)="",""," || Outras: "&INDEX(BD_NCM!$K$4:$K$%d,$I$7))&IF(INDEX(BD_NCM!$M$4:$M$%d,$I$7)="",""," || IS: "&INDEX(BD_NCM!$M$4:$M$%d,$I$7))))'%((NBS_LAST,)*3+(NCM_LAST,)*5),wrap=True)
ws.row_dimensions[8].height=110; ws['A8'].alignment=Alignment(wrap_text=True,vertical='top')
for a,v in (('I3','auxiliar'),('I4','=IF(ISNUMBER($B$4),IF($B$17="servico",TEXT($B$4,"0"),TEXT($B$4,"00000000")),SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(TRIM($B$4),".","")," ",""),"-",""))'),
            ('I5','=IFERROR(MATCH($I$4,BD_NCM!%s,0),0)'%NR),('I6','=IFERROR(MATCH($I$4,BD_NBS!%s,0),0)'%SR),('I7','=IF($B$17="servico",$I$6,$I$5)')):
    ws[a]=v; ws[a].font=Font(name='Arial',size=8,color='FF7F7F7F'); ws[a].number_format='@' if a=='I4' else 'General'
ws.unmerge_cells('A3:G3'); ws.merge_cells('A3:G3')

# ---------------- LEIA-ME ----------------
wl=wb['LEIA-ME']
wl['B24']='CBS provisoria de 11,2% (2027 e 2028) e 11,3% (2029 em diante), pelo calculo do TCU (Acordao 2933/2026), e IBS de 0,1%. CONFIRMAR'
wl['B25']='a resolucao do Senado antes de usar com cliente. Sao parametros editaveis na aba PARAMETROS.'
base_font=copy(wl['B19'].font); head_font=copy(wl['A18'].font); head_fill=copy(wl['A18'].fill)
linhas=[('ATUALIZACAO DE 10/11/2026: BUSCA AUTOMATICA POR CODIGO',None),
 (None,'CLASSIFICACAO - cole ate 300 codigos de NCM ou NBS e veja a regra de CBS e IBS, o cClassTrib e o Imposto Seletivo.'),
 (None,'PRODUTO - digite o NCM ou a NBS em B4 e escolha o tipo em B17. Com B6 em "auto", a reducao e o IS vem da base.'),
 (None,'BD_NCM, BD_NBS, BD_LC116, BD_CCLASSTRIB, BD_IS e BD_REGRAS - bases de consulta. Nao editar; sao substituidas a cada atualizacao.'),
 (None,'Situacao INTEGRAL: sem beneficio nos anexos. CONFERIR: beneficio condicionado. ESCOLHER: mais de uma regra, a planilha usa a menor reducao.'),
 (None,'O codigo nao decide sozinho. O beneficio depende da condicao, de quem compra, da destinacao e da operacao (aba BD_REGRAS).'),
 (None,'Imposto Seletivo pela MP 1.399/2026 (aliquotas de 2027, cobranca a partir de fevereiro), sujeito a conversao em lei.'),
 (None,'Base fiscal '+d['meta']['versao']+': Mapa de Classificacao 1.0 de 14/10/2026 (LC 214/2025 com LC 227 e LC 235/2026; IT 2025.002 v1.70) e Anexo VIII v1.01.00.')]
r0=35
for i,(a,b) in enumerate(linhas):
    if a: 
        c=wl.cell(r0+i,1,a); c.font=head_font; c.fill=head_fill
        for cc in range(2,7): wl.cell(r0+i,cc).fill=head_fill
    if b: wl.cell(r0+i,2,b).font=base_font
# ===== rodada 3 =====
FAT='INDEX(PARAMETROS!$D$32:$D$39,MATCH(PARAMETROS!$B$4,PARAMETROS!$A$32:$A$39,0))'
wg=wb['GASTOS']; n3=0
for r in range(5,30):
    for col,al in (('G','H'),('J','K')):
        c=wg[f'{col}{r}']
        if isinstance(c.value,str) and c.value==f'=IF(N(B{r})=0,0,B{r}/(1+{al}{r}))':
            c.value=f'=IF(N(B{r})=0,0,B{r}*(1-N(D{r})*{FAT})/(1+{al}{r}))'; n3+=1
assert n3==50,n3
wg['A39']='A base do credito de CBS e IBS exclui o ICMS destacado na compra (coluna D), conforme a LC 214/2025, art. 12, par. 2, V.'
wm=wb['MOTOR_PRECO_2026']
assert wm['C51'].value=='=C12' and wm['B26'].value=='=C10+C11+IF(PARAMETROS!$B$10=0,0,C13)'
wm['C51']='=C12*'+FAT
wm['B26']='=C10+C11+IF(PARAMETROS!$B$10=0,0,C13)+C12-C51'
wm['A26']='(+) Creditos de PIS, COFINS e IPI que deixam de existir e ICMS que se reduz'
wp=wb['PARAMETROS']
for a,v in (('A63','LC 224/2025: receita anual a partir da qual a presuncao e acrescida'),('B63',5000000),('A65','LC 224/2025: acrescimo sobre os percentuais de presuncao'),('B65',0.1),
            ('A69','Fator da LC 224 aplicado (pela receita da aba MOTOR_PRECO_2026)'),('B69','=IF(MOTOR_PRECO_2026!$B$4>B63,1+B65*(MOTOR_PRECO_2026!$B$4-B63)/MOTOR_PRECO_2026!$B$4,1)')):
    wp[a]=v; wp[a].font=Font(name='Arial',size=10,bold=a.startswith('A'))
wp['B63'].number_format='#,##0'; wp['B65'].number_format='0%'; wp['B69'].number_format='0.0000'
for a in ('B63','B65'): wp[a].font=copy(wp['B67'].font); wp[a].fill=copy(wp['B67'].fill)
assert wp['B25'].value.startswith('=IF(N(C25)>0,C25,INDEX(')
wp['B25']='=('+wp['B25'].value[1:]+')*$B$69'; wp['B26']='=('+wp['B26'].value[1:]+')*$B$69'
wsP=wb['PRODUTO']
wsP['A49']='Credito de PIS e COFINS da compra (somente Lucro Real, base sem ICMS)'; wsP['A49'].font=Font(name='Arial',size=10)
wsP['B49']='=IF(AND($B$10="real",$B$20<>"pf"),$B$19*(1-IF($B$20="regular",$B$21*IF($B$17="servico",0,1),0))*(PARAMETROS!$C$20+PARAMETROS!$C$21),0)'
wsP['B49'].number_format=wsP['B46'].number_format; wsP['B49'].font=copy(wsP['B46'].font)
assert wsP['B46'].value.endswith('B41+B42+B43+B44-B40)'); wsP['B46']=wsP['B46'].value[:-1]+'-B49)'
wsP['A28']='Receita anual acima de R$ 5 milhoes? (S/N, LC 224/2025)'; wsP['A28'].font=Font(name='Arial',size=10,bold=True)
wsP['B28']='N'; wsP['B28'].font=copy(wsP['B6'].font); wsP['B28'].fill=copy(wsP['B6'].fill); wsP['B28'].border=copy(wsP['B6'].border); wsP['B28'].alignment=copy(wsP['B6'].alignment)
dv2=DataValidation(type='list',formula1='"S,N"',allow_blank=False); wsP.add_data_validation(dv2); dv2.add('B28')
wsP['B37']='=('+wsP['B37'].value[1:]+')*(1+IF($B$28="S",PARAMETROS!$B$65,0))'
wsP['E8']=wsP['E8'].value+'&IF(OR($I$7=0,$B$17="servico"),"",IF(INDEX(BD_NCM!$Q$4:$Q$%d,$I$7)="",""," || ICMS SC: "&INDEX(BD_NCM!$Q$4:$Q$%d,$I$7)))'%(NCM_LAST,NCM_LAST)
wsP.row_dimensions[8].height=150
wl=wb['LEIA-ME']
for i,b in enumerate(['ICMS de Santa Catarina: aliquota interna por NCM nas abas CLASSIFICACAO e BD_NCM (Lei 10.297/1996 e RICMS/SC, consulta em 10/11/2026).',
   'Nao cobre substituicao tributaria, TTD, credito presumido nem operacoes interestaduais. Beneficios da cesta basica valem ate 31/12/2026.',
   'LC 224/2025: acrescimo de 10% na presuncao acima de R$ 5 milhoes (PARAMETROS linhas 63 a 69 e PRODUTO B28).']):
    wl.cell(43+i,2,b).font=copy(wl['B19'].font)
# ===== rodada 4: PIS e COFINS no regime atual e ano de 2026 =====
wsP=wb['PRODUTO']
wsP['A25']='PIS e COFINS hoje (auto, normal, monofasico, monofasico_fab, zero, isento)'; wsP['A25'].font=Font(name='Arial',size=10,bold=True)
wsP['B25']='auto'
for a_ in ('B25',): wsP[a_].font=copy(wsP['B6'].font); wsP[a_].fill=copy(wsP['B6'].fill); wsP[a_].border=copy(wsP['B6'].border); wsP[a_].alignment=copy(wsP['B6'].alignment)
dv3=DataValidation(type='list',formula1='"auto,normal,monofasico,monofasico_fab,zero,isento"',allow_blank=False); wsP.add_data_validation(dv3); dv3.add('B25')
SH='(INDEX(PARAMETROS!$B$72:$B$76,MATCH($B$15,PARAMETROS!$A$72:$A$76,0))+INDEX(PARAMETROS!$C$72:$C$76,MATCH($B$15,PARAMETROS!$A$72:$A$76,0)))'
aux={'I8':'=IF($B$25="auto",IF(OR($B$17="servico",$I$7=0),"normal",INDEX(BD_NCM!$R$4:$R$%d,$I$7)),$B$25)'%NCM_LAST,
     'I12':'=IF($I$8="monofasico_fab",IF(OR($I$7=0,$B$17="servico"),0,N(INDEX(BD_NCM!$T$4:$T$%d,$I$7))),0)'%NCM_LAST,
     'I9':'=IF($B$10="simples",0,IF($I$8="normal",IF($B$10="real",PARAMETROS!$C$20+PARAMETROS!$C$21,PARAMETROS!$B$20+PARAMETROS!$B$21),$I$12))',
     'I10':'=$B$16*(1-IF(AND($B$13=2026,OR($I$8="monofasico",$I$8="monofasico_fab")),'+SH+',0))+IF($B$13=2026,$I$12,0)',
     'I11':'=$B$16*(1-IF(OR($I$8="monofasico",$I$8="monofasico_fab"),'+SH+',0))+$I$12'}
for k,v in aux.items(): wsP[k]=v; wsP[k].font=Font(name='Arial',size=8,color='FF7F7F7F')
wsP['D25']='<- tratamento em uso:'; wsP['D25'].font=Font(name='Arial',size=9,italic=True); wsP['E25']='=$I$8'; wsP['E25'].font=Font(name='Arial',size=10,bold=True)
for a_ in ('B42','B43'):
    assert wsP[a_].value.startswith('=IF($B$10="simples",0,'); wsP[a_]='=IF($I$8="normal",1,0)*('+wsP[a_].value[1:]+')'
wsP['B43']=wsP['B43'].value+'+IF($B$10="simples",0,($B$27-IF($B$17="servico",0,B41))*$I$12)'
wsP['A43']='COFINS (no fabricante de monofasico, PIS e COFINS pela aliquota concentrada)'
assert wsP['B45'].value=='=IF($B$10="simples",$B$27*$B$16,0)'; wsP['B45']='=IF($B$10="simples",$B$27*$I$11,0)'
wsP['B49']='=IF(OR($I$8="normal",$I$8="monofasico_fab"),1,0)*('+wsP['B49'].value[1:]+')'
assert wsP['B53'].value=='=IF($B$10="simples",0,B51+B52)'; wsP['B53']='=IF($B$10="simples",0,B51+B52+IF(AND($B$13=2026,$B$19<>0),B49*$B$24/$B$19,0))'
KPC='IF($B$13=2026,$I$9*(1-IF($B$17="servico",0,B36)),0)'
wsP['B56']=wsP['B56'].value+'-'+KPC
assert wsP['B57'].value=='=IF($B$10="simples",($B$47+$B$24)/(1-$B$16),($B$47+$B$24-B53)/B56)'; wsP['B57']='=IF($B$10="simples",($B$47+$B$24)/(1-$I$10),($B$47+$B$24-B53)/B56)'
assert wsP['B64'].value=='=IF($B$10="simples",B57*$B$16,0)'; wsP['B64']='=IF($B$10="simples",B57*$I$10,0)'
assert wsP['B65'].value=='=IF($B$10="simples",B64,B59+B60+B61+B62+B63-B53)'; wsP['B65']='=IF($B$10="simples",B64,B59+B60+B61+B62+B63+B57*'+KPC+'-B53)'
assert wsP['B83'].value=='=($B$47+$B$24)/(1-$B$16)' and wsP['B85'].value=='=B83*$B$16'
wsP['B83']='=($B$47+$B$24)/(1-$I$10)'; wsP['B85']='=B83*$I$10'
n5=0
for r in range(70,75):
    key=re.search(r'OR\("([a-z_]+)"="mei"',wsP[f'C{r}'].value).group(1)
    old_e=wsP[f'E{r}'].value; tail=f'($B$47+$B$24-B{r}-C{r})/B56)'
    assert old_e.endswith(tail),old_e
    pcc=f'IF(AND($B$13=2026,$B$10="real","{key}"<>"pf",OR($I$8="normal",$I$8="monofasico_fab")),$B$24*(1-IF("{key}"="regular",$B$21*IF($B$17="servico",0,1),0))*(PARAMETROS!$C$20+PARAMETROS!$C$21),0)'
    wsP[f'E{r}']=old_e[:-len(tail)]+f'($B$47+$B$24-B{r}-C{r}-{pcc})/B56)'; n5+=1
wsP['E8']=wsP['E8'].value+'&IF(OR($I$7=0,$B$17="servico"),""," || PIS/COFINS hoje: "&INDEX(BD_NCM!$R$4:$R$%d,$I$7)&IF(INDEX(BD_NCM!$S$4:$S$%d,$I$7)="",""," ("&INDEX(BD_NCM!$S$4:$S$%d,$I$7)&")"))'%(NCM_LAST,NCM_LAST,NCM_LAST)
wm=wb['MOTOR_PRECO_2026']
wm['A7']='Parcela da receita sem PIS e COFINS hoje (monofasico, aliquota zero ou isento)'; wm['A7'].font=copy(wm['A6'].font)
wm['B7']=0; wm['B7'].font=copy(wm['B4'].font); wm['B7'].fill=copy(wm['B4'].fill); wm['B7'].border=copy(wm['B4'].border); wm['B7'].number_format='0.0%'
for a_ in ('B10','B11','C10','C11'): wm[a_]='=(1-$B$7)*('+wm[a_].value[1:]+')'
wl=wb['LEIA-ME']
for i,b in enumerate(['PIS e COFINS de hoje por NCM, pelas Tabelas 4.3.10 e 4.3.13 (versao 1.37, de 14/10/2026) da EFD-Contribuicoes: monofasico e aliquota zero.',
   'Em PRODUTO B25, "auto" busca o tratamento na base. Monofasico e aliquota zero zeram o PIS e a COFINS de hoje e o credito da compra. Use monofasico_fab para fabricante ou importador.',
   'Em MOTOR_PRECO_2026 B7, informe a parcela da receita sem PIS e COFINS. O ano de 2026 passou a reproduzir o regime atual na aba PRODUTO.']):
    wl.cell(47+i,2,b).font=copy(wl['B19'].font)
from openpyxl.drawing.image import Image as XImg
_lg=XImg('logo_amcont.png'); _lg.width=226; _lg.height=72
wl=wb['LEIA-ME']; wl.add_image(_lg,'E3')
wb.save('Amcont_Precificacao_Reforma_Tributaria.xlsx'); print('salvo',NCM_LAST,NBS_LAST,wb.sheetnames)
