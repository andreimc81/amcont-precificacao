# Monta o banco fiscal unificado (NCM, NBS, LC 116, cClassTrib, IS) a partir das planilhas de origem.
import openpyxl, json, re, sys, collections
D='/mnt/user-data/attachments/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/'
F_MAPA=D+'ad838324-Mapa-Classificacao2027.xlsx'
F_A8='/home/claude/work/fontes/anexoVIII_v1.02.00.xlsx'  # v1.02.00 de 26/10/2026 (antes: v1.01.00), registro R14-01
F_V4=D+'df9e4549-Mapa_NCM_RT2026_v4_BuscaAutomatica2026.xlsx'
S=[]; SI={}
def s(x):
    if x is None or str(x).strip()=='' : return -1
    x=str(x).strip()
    if x not in SI: SI[x]=len(S); S.append(x)
    return SI[x]
def red(x):
    if x is None: return None
    m=re.fullmatch(r'\s*(\d+(?:[.,]\d+)?)\s*%?\s*',str(x))
    return round(float(m.group(1).replace(',','.'))/100,4) if m else None
def tx(x): return None if x is None else str(x).strip()
def rows(wb,n): return list(wb[n].iter_rows(values_only=True))

wb=openpyxl.load_workbook(F_MAPA,read_only=True,data_only=True)
# ---------- NCM ----------
R=rows(wb,'BASE_NCM'); h=R[0]; ix={k:i for i,k in enumerate(h) if k}; RC='Redução de IBS e CBS (%)'
EST={'integral':'i','conferir':'c','escolher':'x'}
ncm={}; ncm_desc={}
for r in R[1:]:
    g=lambda k: r[ix[k]]
    e={'e':EST[g('estado')],'ax':tx(g('anexo')),'it':tx(g('item')),'r':red(g(RC)),'cst':tx(g('cst')),'ccl':tx(g('ccl')),
       'b':s(g('base')),'c':s(g('cond')),'q':s(g('oqc')),'a':s(g('alt')),'t':tx(g('tipos')),'m':s(g('msg'))}
    if g('sitncm') and not str(g('sitncm')).startswith('vigente'): e['s']=s(g('sitncm'))
    if e['e']=='x':
        o=[]
        for L in 'ABC':
            if r[ix[L+'_ccl']] is None and r[ix[L+'_anexo']] is None: continue
            o.append([tx(r[ix[L+'_anexo']]),tx(r[ix[L+'_item']]),red(r[ix[L+'_'+RC]]),tx(r[ix[L+'_cst']]),tx(r[ix[L+'_ccl']]),
                      s(r[ix[L+'_base']]),s(r[ix[L+'_cond']]),s(r[ix[L+'_resumo']])])
        e['o']=o
        assert len(o)>=2,(g('ncm'),o)
    ncm[g('ncm')]={k:v for k,v in e.items() if v is not None and v!=-1}
    ncm_desc[g('ncm')]=tx(g('descricao'))
# prefixos (so valem para codigo fora da tabela oficial)
R=rows(wb,'BASE_PREF_NCM'); h=R[0]; px={k:i for i,k in enumerate(h) if k}
pref={}
for r in R[1:]:
    g=lambda k: r[px[k]]
    pref[str(g('key'))]={'ax':tx(g('anexo')),'it':tx(g('item')),'rt':tx(g(RC)),'cst':tx(g('cst')),'ccl':tx(g('ccl')),
                         'b':s(g('base')),'c':s(g('cond')),'m':s(g('msg')),'t':tx(g('tipos'))}
vig=[r[0] for r in rows(wb,'NCM_VIGENTES')[1:] if r[0]]
# ---------- NBS (beneficios por anexo) ----------
R=rows(wb,'BASE_NBS'); h=R[0]; nx={k:i for i,k in enumerate(h) if k}
nbs={}; nbs_desc={}
for r in R[1:]:
    g=lambda k: r[nx[k]]
    k=re.sub(r'\D','',str(g('nbs')))
    if len(k)!=9: continue   # itens da lei sem NBS informado: sem consulta por codigo
    EST.setdefault('sem_beneficio','i')
    nbs[k]={kk:v for kk,v in {'e':EST[g('estado')],'ax':tx(g('anexo')),'it':tx(g('item')),'r':red(g(RC)),'cst':tx(g('cst')),'ccl':tx(g('ccl')),
            'b':s(g('base')),'c':s(g('cond')),'q':s(g('oqc')),'a':s(g('alt')),'t':tx(g('tipos')),'m':s(g('msg'))}.items() if v is not None and v!=-1}
    nbs_desc[k]=tx(g('descricao'))
R=rows(wb,'BASE_PREF_NBS'); h=R[0]; qx={k:i for i,k in enumerate(h) if k}
pref_nbs={}
for r in R[1:]:
    g=lambda k: r[qx[k]]
    pref_nbs[str(g('key'))]={'ax':tx(g('anexo')),'it':tx(g('item')),'rt':tx(g(RC)),'cst':tx(g('cst')),'ccl':tx(g('ccl')),
                             'b':s(g('base')),'c':s(g('cond')),'m':s(g('msg')),'t':tx(g('tipos'))}
# ---------- 30 regras sem lista de codigo ----------
R=rows(wb,'Regras e avisos'); regras=[]
for r in R[5:]:
    if not r[0] or not str(r[0]).isdigit(): break
    regras.append([int(r[0]),tx(r[1]),tx(r[2]),tx(r[3]),tx(r[4]),tx(r[5]),tx(r[6]),tx(r[8])])
# tipos de situacao (texto das instrucoes)
tipos={}
for r in rows(wb,'Instruções'):
    for c in r:
        m=re.match(r'(T\d+|NL)\.\s+(.*)',str(c or ''))
        if m: tipos[m.group(1)]=m.group(2)
versao=[c for r in rows(wb,'Versões') for c in r if c and str(c).startswith('LC 214/2025 compilada')][0]

# ---------- Anexo VIII: LC 116 x NBS x indOp x cClassTrib ----------
wb8=openpyxl.load_workbook(F_A8,read_only=True,data_only=True)
R=rows(wb8,'tabela geral')
def cc(x): return None if x is None else str(x).strip().zfill(6)
lc=[]; ccl_nome={}
cur=None; grp=[]; item_ccl=None
for r in R[1:]:
    it,dit,nb,dnb,_,_,indop,local,c,cn=[r[i] for i in range(10)]
    if it:
        cur={'i':str(it).strip(),'d':tx(dit),'op':[],'n':[]}; lc.append(cur); grp=[]
    if cur is None: continue
    if indop:
        op=cc(indop); loc=tx(local)
        if not any(o[0]==op for o in cur['op']): cur['op'].append([op,loc])
        elif loc:
            for o in cur['op']:
                if o[0]==op and not o[1]: o[1]=loc
    if c: ccl_nome.setdefault(cc(c),tx(cn))
    if nb:
        k=re.sub(r'\D','',str(nb)); assert len(k)==9,(nb,)
        nbs_desc.setdefault(k,tx(dnb))
        # v1.02.00 repete a mesma NBS em linhas separadas do item, cada uma com outro cClassTrib: une as linhas
        ent=next((e for e in cur['n'] if e[0]==k),None)
        if ent is None: ent=[k,[]]; cur['n'].append(ent)
        if c:
            grp=[ent]
            if cc(c) not in ent[1]: ent[1].append(cc(c))
        else:
            if grp: ent[1].extend(x for x in grp[0][1] if x not in ent[1]) ; grp.append(ent)
            else: grp=[ent]
    elif c:
        tgt = grp if grp else []
        if len(grp)>1 and grp[0][1] and len(grp[-1][1])>=0:
            pass
        for ent in tgt:
            if cc(c) not in ent[1]: ent[1].append(cc(c))
        if not tgt: cur.setdefault('cx',[]).append(cc(c))
# ---------- Tabela IBPTax 26.2.D (vigencia 17/11 a 20/12/2026): NCM e NBS adicionais e descricoes ----------
ibpt=json.load(open('ibpt.json',encoding='utf-8'))
nbs_lei=len(nbs_desc)
for k,v in ibpt['nbs'].items(): nbs_desc.setdefault(k,v)
novos_ncm=sorted(set(ibpt['ncm'])-set(vig)-{'00000000'})
vig=sorted(set(vig)|set(novos_ncm))
for k in vig:
    if not ncm_desc.get(k) and ibpt['ncm'].get(k): ncm_desc.setdefault('~'+k, ibpt['ncm'][k])
print('NBS: %d da lei e do Anexo VIII + %d da tabela IBPT = %d | NCM novos: %s'%(nbs_lei,len(nbs_desc)-nbs_lei,len(nbs_desc),novos_ncm))
# ---------- cClassTrib (nomes e reducoes) ----------
wb4=openpyxl.load_workbook(F_V4,read_only=True,data_only=True)
ccl={}
for r in rows(wb4,'📋 154 cClassTribs'):
    if r[2] and re.fullmatch(r'\d{6}',str(r[2]).strip()):
        try: pr=float(r[4])
        except: pr=None
        ccl[str(r[2]).strip()]=[str(r[1]).strip(),tx(r[3]),pr,tx(r[7]) or '']
for k,v in ccl_nome.items():
    if k not in ccl: ccl[k]=[k[:3],v,None,'']
ccl.setdefault('200056',['200','Prestação de serviços de profissões intelectuais por profissional autônomo (novo na v1.70)',0.3,'Art. 127'])
ccl.setdefault('515001',['515','Diferimento com redução de alíquota (ver tabela oficial)',None,''])

# ---------- Imposto Seletivo: MP 1.399/2026, Anexos IV e V (texto oficial conferido em 10/11/2026) ----------
IS=[ # prefixo, aliquota ad valorem (None = nao simulavel por aliquota fixa), nota
 ['22021000',0.026,'Bebidas açucaradas: 2,6%.'],
 ['2203',0.042,'Cervejas de malte: 4,2%. Pequenos produtores têm redução de 10% a 40%.'],
 ['2204',0.08,'Vinhos: 8%. Vinhos do Porto, Madeira e Xerez: 16%.'],
 ['2205',0.12,'Vermutes: 12%.'],
 ['2206',0.08,'Outras bebidas fermentadas: 8%. Acima de 14% de teor alcoólico (2206.00.90): 16%.'],
 ['22084000',0.20,'Aguardente de cana: 20%. Rum e aguardente de melaço: 24%.'],
 ['2208',0.24,'Demais destilados: 24%. Bebidas refrescantes abaixo de 8% de teor alcoólico (2208.90.00): 16%.'],
 ['240220',None,'Cigarros: 66,7% sobre base própria (15% do preço de venda no varejo) mais R$ 3,50 por vintena. Não cabe em alíquota única: calcule à parte.'],
 ['2401',0.375,'Demais produtos fumígenos: 37,5%.'],['2402',0.375,'Demais produtos fumígenos: 37,5%. Cigarros e cigarrilhas têm regra própria.'],
 ['2403',0.375,'Demais produtos fumígenos: 37,5%.'],['2404',0.375,'Demais produtos fumígenos: 37,5%.'],
 ['8703',None,'Automóveis: alíquota base de 6,3%, ajustada por potência, combustível e critérios ambientais e multiplicada por 1,21. Exemplos divulgados: de 5,2% a 17,3%. Informe a alíquota do modelo.'],
 ['8704',None,'Comerciais leves das subposições 8704.21, 8704.31, 8704.41.00, 8704.51.00, 8704.60.00 e 8704.90.00: alíquota base de 3,9%, ajustada por critérios técnicos e multiplicada por 1,21. Caminhões estão fora do imposto. Informe a alíquota do modelo.'],
 ['89033',0.12,'Barcos a motor: 12%.'],['8903',0.078,'Demais embarcações de recreio ou de esporte a motor: 7,8%. Sem motor (veleiro sem motor auxiliar, caiaque, bote a remo), não incide: o Anexo XVII da LC 214/2025 alcança só embarcações com motor.'],
 ['8802',0.068,'Aeronaves (exceto 8802.60.00): 6,8%.'],
 ['2601',0.0,'Bens minerais extraídos: alíquota zero até 31/12/2027.'],['2709',0.0,'Bens minerais extraídos: alíquota zero até 31/12/2027.'],
 ['2711',0.0,'Bens minerais extraídos: alíquota zero até 31/12/2027.'],
]
# dicas por capitulo, derivadas das regras sem lista de NCM
DICAS=[ # prefixos, numero da regra, texto
 [['30'],1,'Medicamento não tem lista de NCM na lei. Se for registrado na Anvisa ou manipulado, pode ter redução de 60% (art. 133, cClassTrib 200032) ou alíquota zero conforme a lista do art. 146 (200009).'],
 [['01','02','03','04','05','06','07','08','09','10','11','12','13','14'],6,'Produto agropecuário, pesqueiro, florestal ou extrativista in natura pode ter redução de 60% (art. 137, cClassTrib 200036), mesmo fora dos anexos. O critério é o estado do produto, não o NCM.'],
 [['2710','2711','2207','3826'],18,'Combustíveis e biocombustíveis seguem regime específico monofásico (arts. 172 a 180, CST 620). Esta calculadora não simula esse regime.'],
 [['4901','4902','4903','4904','4905','4801','4802'],13,'Livros, jornais, periódicos e o papel destinado à sua impressão são imunes (art. 9º, CST 410). Confirme a destinação.'],
]

# ---------- ICMS de Santa Catarina (Lei 10.297/1996 e RICMS/SC, consulta em 10/11/2026) ----------
SC={'meta':{'consulta':'2026-11-11','fontes':['Lei 10.297/1996, art. 19 e Anexo I (SEF/SC, conferida em 11/11/2026)','RICMS/SC, art. 26 e art. 27 (texto da SEF/SC, conferido em 11/11/2026)','RICMS/SC, Anexo 2, arts. 1º, 2º, 7º, 9º, 11-A, 12-A, 12-B e 12-E (SEF/SC, conferido em 11/11/2026)'],
  'aviso':'Alíquotas internas de SC. Não cobre substituição tributária, TTD, crédito presumido, operações interestaduais nem DIFAL. Quando a lei descreve a mercadoria sem NCM, o enquadramento é indicativo e depende da descrição do produto.'},
 # prefixos com 25% (Anexo I, Secao I: a lei traz o codigo)
 'r25':[['2203','Cervejas e chope'],['2204','Bebidas alcoólicas'],['2205','Bebidas alcoólicas'],['2206','Bebidas alcoólicas'],['2208','Bebidas alcoólicas'],
        ['2402','Cigarros e manufaturados de fumo'],['2403','Cigarros e manufaturados de fumo'],['3303','Perfumes e cosméticos'],['3304','Perfumes e cosméticos'],
        ['3305','Perfumes e cosméticos'],['3307','Perfumes e cosméticos'],['43','Peleteria'],['93','Armas e munições']],
 # 12%: [prefixos, descricao, base, exato(1 = a lei traz NCM)]
 'r12':[
  [['0207'],'Carnes e miudezas de aves','Seção II, item 01',0],[['0201','0202','0203','0204','0206','020810'],'Carnes e miudezas de bovino, suíno, ovino, caprino e coelho','Seção II, itens 02 e 22',0],
  [['021020'],'Charque e carne de sol','Seção II, item 03',0],[['0903'],'Erva-mate beneficiada','Seção II, item 04',0],[['1701'],'Açúcar','Seção II, item 05',0],
  [['090121','090122'],'Café torrado','Seção II, item 06',0],[['1101','110220','110290','110620'],'Farinhas de trigo, milho, arroz e mandioca','Seção II, item 07',0],
  [['0401','040510'],'Leite e manteiga','Seção II, item 08',0],[['1501'],'Banha de porco','Seção II, item 09',0],[['150790','151529'],'Óleos refinados de soja e de milho','Seção II, item 10',0],
  [['1517'],'Margarina e creme vegetal','Seção II, item 11',0],[['190211','190219'],'Espaguete, macarrão e aletria','Seção II, item 12',0],[['190590'],'Pão','Seção II, item 13',0],
  [['160413'],'Sardinha em lata','Seção II, item 14',0],[['2209'],'Vinagre','Seção II, item 15',0],[['2501'],'Sal de cozinha','Seção II, item 16',0],[['0406'],'Queijo','Seção II, item 17',0],
  [['100620','100630'],'Arroz polido, parboilizado ou integral','Seção II, item 18',0],[['190120'],'Misturas e pastas para pães','Seção II, item 19',1],[['07133'],'Feijão','Seção II, item 20',0],
  [['0409'],'Mel','Seção II, item 21',0],[['16041390'],'Manjuba em lata','Seção II, item 23',1],
  [['01'],'Animais vivos','Seção III, item 01',0],[['0302','0303','0306','0307'],'Peixes, crustáceos e moluscos frescos, resfriados ou congelados','Seção III, item 02',0],
  [['0701','0702','0703','0704','0705','0706','0707','0708','0709','0714'],'Hortícolas, raízes e tubérculos frescos','Seção III, item 03',0],
  [['0803','0804','0805','0806','0807','0808','0809','0810'],'Frutas frescas','Seção III, item 04',0],[['09011'],'Café não torrado','Seção III, item 05',0],
  [['1001','1002','1003','1004','1005','100610','1007','1008'],'Cereais em grão','Seção III, item 06',0],[['1201','1202','1204','1205','1206','1207','1213','1214'],'Sementes oleaginosas, palhas e forragens','Seção III, item 07',0],
  [['2401'],'Fumo em folha','Seção III, item 08',0],[['4401','4403'],'Lenha e madeira em toras','Seção III, item 09',0],[['0407'],'Ovos de aves com casca, frescos','Seção III, item 11',0],
  [['8701','8702','8703','8704','8706','8711','87163','870790','8903'],'Veículos automotores','Seção IV (a lista usa códigos antigos da NBM: confira o modelo)',0],
  [['6910'],'Louças sanitárias','art. 19, III, i',1],[['6907'],'Ladrilhos e placas cerâmicas','art. 19, III, j',1],[['6810'],'Blocos, telhas, lajes e pré-moldados de concreto','art. 19, III, l',1],
  [['25051000','392210','39259000','39172','39174','84818019','39222000','39229000','392510','4408','441820','681120','70052','732410','730830','8302','85381000','854411','68030000','69041000','69051000','69060000','73142000'],
   'Cesta básica da construção civil','Seção VI (há limites de dimensão e tipo em vários itens)',0]],
 # isencao da cesta basica ate 31/12/2026 (NCM na norma)
 'isento':[[['11010010','11022000','11062000','07133319','07133399','10063021','10063011','10062010','10062020'],'Cesta básica vendida a consumidor final em operação interna: farinhas de trigo, milho e mandioca, feijão preto e carioquinha e arroz, sem outros ingredientes. Exige estorno do crédito de ICMS.','RICMS/SC, Anexo 2, art. 1º, XXXVI; Lei 19.397/2025'],
           [['11029000'],'Farinha de arroz, operações internas.','RICMS/SC, Anexo 2, art. 1º, XXXVII; Convênio ICMS 224/17']],
 # reducao de base com carga de 7% ate 31/12/2026 (art. 11-A; so o inciso XIII traz NCM)
 'c7':[[['1101','110220','110620','110290'],'Farinhas de trigo, milho, mandioca e arroz'],[['190211','190219'],'Massas secas não recheadas, exceto grano duro'],[['190590'],'Pão francês'],
       [['07133'],'Feijão'],[['0409'],'Mel'],[['100620','100630'],'Arroz polido, parboilizado e integral'],[['0207','0203','02063','02064'],'Carnes e miudezas de aves e de suínos'],
       [['0903'],'Erva-mate beneficiada'],[['040110','040120'],'Leite esterilizado longa vida'],[['190120'],'Pastas de farinha de trigo para padaria']],
 # outras isencoes de alimentos (por descricao)
 'outros':[[['68118200'],'Telha ondulada de fibrocimento sem amianto, de produção própria: o fabricante pode optar por não usar os 12% entre contribuintes (RICMS/SC, art. 26, § 5º, IV).'],
  [['2704'],'Coque de carvão mineral: 12% em qualquer operação interna (RICMS/SC, art. 26, III, h).'],
  [['0401'],'Leite fresco, pasteurizado ou não, vendido a consumidor final: isento (Anexo 2, art. 1º, I).'],
           [['0701','0702','0703','0704','0705','0706','0707','0708','0709','0714','0803','0804','0805','0806','0807','0808','0809','0810'],'Hortifrutícolas in natura da lista do Anexo 2, art. 2º, I: isentos nas saídas internas e interestaduais.'],
           [['0407'],'Ovos: isentos, exceto quando destinados à industrialização (Anexo 2, art. 2º, II).']],
 # R16-03: códigos em que o NCM, sozinho, corresponde à descrição do Anexo I da Lei 10.297/1996 (Seções II e III),
 # conferida no texto da SEF/SC em 11/11/2026. Nesses, os 12% valem para qualquer destinatário e a opção de 17% não aparece.
 # Ficam de fora os códigos mais largos que a descrição (ex.: 0206.80 e 0206.90 incluem equídeos; 0306 e 0307 incluem cozidos;
 # 0803 a 0806 incluem frutas secas; 0705 e 0709 incluem hortícolas não listados; 1501, 1517.90, 1905.90, 2501, 1604.13).
 'r12nc':['0207','0201','0202','0203','0204','02061','02062','02063','02064','020810','0903','1701','090121','090122',
   '11010010','110220','040110','040120','040510','150790','151529','151710','2209','0406','1006','07133','0409',
   '0101','0102','0103','0104','0105','0302','0303','0701','0702','0703','0704','0706','0707','0708','0714',
   '0807','0808','0809','0810','09011','1001','1002','1003','1004','1005','1007','1201','1202','1204','1205','1206',
   '440111','440112','4403','04071','04072'],
 # R17-03: benefícios do RICMS/SC, Anexo 2, lidos no texto da SEF/SC em 11/11/2026 (conferir o dispositivo antes de aplicar).
 # Cada regra: prefixos, exclusões, pergunta (ou None) e opções [valor, rótulo, carga (0 = isento, None = sem benefício), base, fim, destinatários].
 'ben':[
  {'id':'maca_pera','pref':['080810','080830'],'excl':[],'q':None,
   'ops':[['-','Maçãs e peras',0,'RICMS/SC, Anexo 2, art. 2º, LXXVI (isenção nas saídas internas e interestaduais)',None,None]]},
  {'id':'hortifruti','pref':['0701','0702','0703','0704','0705','0706','0707','0708','0709','0714','0803','0804','0805','0806','0807','0808','0809','0810'],'excl':['080810','080830'],
   'q':'O produto está em estado natural e consta da lista de hortifrutícolas do RICMS/SC, Anexo 2, art. 2º, I?',
   'ops':[['sim','Sim',0,'RICMS/SC, Anexo 2, art. 2º, I (isenção)',None,None],['nao','Não',None,'',None,None]]},
  {'id':'ovos','pref':['0407'],'excl':[],'q':'A venda é de ovos que não vão para industrialização?',
   'ops':[['sim','Sim',0,'RICMS/SC, Anexo 2, art. 2º, II (isenção; sem estorno de crédito)',None,None],['nao','Não, vão para industrialização',None,'',None,None]]},
  {'id':'leite','pref':['0401'],'excl':[],'q':'É leite fresco, pasteurizado ou reconstituído (não é longa vida UHT)?',
   'ops':[['sim','Sim',0,'RICMS/SC, Anexo 2, art. 1º, I (isenção na venda a consumidor final)',None,['final']],['nao','Não',None,'',None,None]]},
  {'id':'caprino','pref':['020450','02068','02069'],'excl':[],'q':'É carne ou miúdo de caprino, e a venda não é para industrialização?',
   'ops':[['sim','Sim',0,'RICMS/SC, Anexo 2, art. 1º, XV (isenção)',None,None],['nao','Não',None,'',None,None]]},
  {'id':'moluscos','pref':['03071','03072','03073'],'excl':[],'q':'É ostra, vieira ou mexilhão em estado natural, resfriado ou congelado (sem cozimento ou preparo)?',
   'ops':[['sim','Sim',0,'RICMS/SC, Anexo 2, art. 1º, II (isenção; Convênio ICMS 147/92)',2026,None],['nao','Não',None,'',None,None]]},
  {'id':'ceramica','pref':['6904','6905','6906'],'excl':[],'q':'É produto de cerâmica vermelha feito de argila ou barro (tijolo, telha, tubo)?',
   'ops':[['sim','Sim',0.07,'RICMS/SC, Anexo 2, art. 7º, III (carga efetiva de 7%)',None,None],['nao','Não',None,'',None,None]]},
  {'id':'areia','pref':['2505','2514','2517'],'excl':[],'q':'É areia, ardósia ou pedra britada?',
   'ops':[['sim','Sim',0.07,'RICMS/SC, Anexo 2, art. 7º, VI (carga efetiva de 7%)',None,None],['nao','Não',None,'',None,None]]},
  {'id':'onibus','pref':['870210'],'excl':[],'q':None,
   'ops':[['-','Veículo para 10 ou mais passageiros',0.08,'RICMS/SC, Anexo 2, art. 12-E (carga efetiva de 8%)',None,None]]},
  {'id':'aco','pref':['72','73'],'excl':[],'q':'O produto de aço consta do RICMS/SC, Anexo 1, Seção XI (aço não plano)?',
   'ops':[['sim','Sim',0.12,'RICMS/SC, Anexo 2, art. 7º, IV (carga efetiva de 12%; até 31/12/2026)',2026,None],['nao','Não',None,'',None,None]]},
  {'id':'maquinas','pref':['84','85'],'excl':[],'q':'A máquina ou o equipamento consta do RICMS/SC, Anexo 1?',
   'ops':[['s6','Seção VI, máquinas e equipamentos industriais',0.088,'RICMS/SC, Anexo 2, art. 9º, I (carga efetiva de 8,8%; até 31/12/2026)',2026,None],
          ['s7','Seção VII, máquinas e implementos agrícolas',0.056,'RICMS/SC, Anexo 2, art. 9º, II (carga efetiva de 5,6%; até 31/12/2026)',2026,None],
          ['s19','Seção XIX, automação, informática e telecomunicações',0.12,'RICMS/SC, Anexo 2, art. 7º, VII (base reduzida em 29,412%: carga de 12%)',None,None],
          ['ativo','Fora dessas seções, para o ativo imobilizado do comprador',0.12,'RICMS/SC, Anexo 2, art. 7º, VIII (base reduzida em 29,411%: carga de 12%)',None,['uso']],
          ['nao','Nenhuma dessas',None,'',None,None]]},
  # R19-01: conferência com o texto do RICMS/SC, art. 26 (PDF do regulamento, versão de 01/09/2026)
  {'id':'protetor','pref':['3304'],'excl':[],'q':'É protetor solar?',
   'ops':[['sim','Sim',0.17,'RICMS/SC, art. 26, § 3º (Lei 14.835/2009): protetor solar sai dos 25% e paga 17%',None,None],['nao','Não',None,'',None,None]]},
  {'id':'combust','pref':['271012','27101921','27101922','271112','271113','271119','38260000','220710','220720'],'excl':[],'q':'Qual é o produto?',
   'ops':[['mono','Gasolina, óleo diesel, biodiesel ou GLP (ICMS monofásico)',0,'RICMS/SC, Anexo 12 (LC 192/2022): ICMS monofásico, cobrado por valor fixo por litro ou quilo na origem; na revenda não há débito',None,None],
          ['etanol','Etanol hidratado combustível (álcool carburante)',0.17,'RICMS/SC, art. 26, I, e § 5º, V: os 12% entre contribuintes não valem para álcool carburante (sujeito a substituição tributária)',None,None],
          ['nao','Não é combustível',None,'',None,None]]}],
 'textil':['50','51','52','53','54','55','56','57','58','59','60','61','62','63','42']}
exec(open('src/sc_anexo1.py',encoding='utf-8').read())  # R19-02

# ---------- PIS e COFINS no regime atual (2026): Tabelas 4.3.10 e 4.3.13 da EFD-Contribuicoes ----------
# Fonte oficial: Tabela 4.3.10 (arquivo enviado pelo usuario em 10/11/2026) e Tabela 4.3.13 versao 1.37, de 14/10/2026.
# Autopecas: a tabela remete aos Anexos I e II da Lei 10.485/2002 sem listar NCM; a lista vem de repositorio publico.
_mono=json.load(open('pis_mono.json',encoding='utf-8'))
GR={'1':'Combustíveis e álcool','2':'Medicamentos e perfumaria','3':'Veículos, autopeças e pneus','4':'Bebidas frias','5':'Substituição tributária'}
# [prefixos, grupo, codigo da tabela, descricao, base legal, PIS, COFINS do fabricante ou importador, restricao]
MONO_R=[
 [['27101259'],'1','101','Gasolinas, exceto de aviação','Lei 9.718/1998, art. 4º',0.0508,0.2344,'Produtor e importador costumam recolher por unidade (Tabela 4.3.11, versão 1.35): R$ 141,10 de PIS e R$ 651,40 de COFINS por metro cúbico desde 10/11/2026 (alíquota zero de 10/10 a 09/11/2026).'],
 [['27101921'],'1','102','Óleo diesel','Lei 9.718/1998, art. 4º',0.0421,0.1942,'Produtor e importador costumam recolher por unidade (Tabela 4.3.11, versão 1.35): R$ 62,61 e R$ 288,89 por metro cúbico desde 01/06/2026.'],
 [['27111910'],'1','103','Gás liquefeito de petróleo','Lei 9.718/1998, art. 4º',0.1020,0.4740,'Produtor e importador costumam recolher por unidade (Tabela 4.3.11, versão 1.35): R$ 29,85 e R$ 137,85 por tonelada, quando não destinado a uso doméstico. GLP de uso doméstico em recipiente de até 13 kg tem alíquota zero (Tabela 4.3.13, código 219).'],
 [['27101911'],'1','104','Querosene de aviação','Lei 10.560/2002, art. 2º',0.05,0.232,'Produtor e importador costumam recolher por unidade (Tabela 4.3.11, versão 1.35): R$ 12,69 e R$ 58,51 por metro cúbico desde 01/08/2026.'],
 [['38260000'],'1','109','Biodiesel','Lei 11.116/2005, art. 3º',0.0615,0.2832,'Apenas o Ex 01 (biodiesel). Produtor e importador costumam recolher por unidade (Tabela 4.3.11, versão 1.35): R$ 26,41 e R$ 121,59 por metro cúbico desde 01/08/2026.'],
 [['220710','2207201','22089000'],'1','112','Álcool, inclusive para fins carburantes','Lei 9.718/1998, art. 5º',0.0525,0.2415,'No código 2208.90.00, apenas o Ex 01 (álcool etílico). Alíquotas do produtor ou importador. Produtor e importador costumam recolher por unidade (Tabela 4.3.11, versão 1.35): etanol combustível, R$ 34,33 e R$ 157,87 por metro cúbico desde 10/11/2026.'],
 [['3001','3003','3004','3002101','3002102','3002103','3002201','3002202','3006301','3006302','30029020','30029092','30029099','30051010','30066000'],'2','201','Produtos farmacêuticos','Lei 10.147/2000, art. 1º, I, a',0.021,0.099,''],
 [['3303','3304','3305','3307','34011190','34012010','96032100'],'2','202','Perfumaria, toucador e higiene pessoal','Lei 10.147/2000, art. 1º, I, b',0.022,0.103,'No código 3401.11.90, exceto o Ex 01 (sabão de toucador, que tem alíquota zero).'],
 [['7309','731029','76129012','842481','8429','84306990','8432','8433','8434','8435','8436','8437','8701','8702','8703','8704','8705','8706','87162000'],'3','301','Veículos automotores e máquinas agrícolas','Lei 10.485/2002, art. 1º',0.02,0.096,''],
 [['4011','4013'],'3','304','Pneus novos e câmaras de ar','Lei 10.485/2002, art. 5º',0.02,0.095,'Pneus e câmaras de bicicleta (4011.50.00 e 4013.20.00) produzidos na ZFM têm alíquota zero.'],
 [['21069010','2201','2202','2203'],'4','411 a 434','Bebidas frias','Lei 13.097/2015, arts. 25 e 28',0.0186,0.0854,'Alíquota zero só na venda pelo varejista. Atacadista e fabricante são tributados: 1,86% e 8,54% na venda a varejista ou consumidor final, 2,32% e 10,68% nas demais. Confira os Ex da TIPI (águas minerais naturais e alguns itens da 2202 ficam fora).'],
 # substituicao tributaria (Tabela 4.3.12, atualizada em 17/11/2014): o fabricante ou importador recolhe pelo comerciante
 [['2402'],'5','101 e 102','Cigarros e cigarrilhas','LC 70/1991, art. 3º, e Lei 9.532/1997, art. 53',0,0,'O fabricante e o importador recolhem o PIS e a COFINS do varejista e do atacadista como substitutos.'],
 [['8711'],'5','201','Motocicletas e ciclomotores','MP 2.158-35/2001, art. 43',0,0,'O fabricante e o importador recolhem o PIS e a COFINS do varejista como substitutos.'],
]
MONO_EXC=['30039056','30049046']
_faixas=[p for r in MONO_R for p in r[0]]
pc_auto={}
for x in _mono:
    if x['grupo'].strip().startswith('3') and not any(x['ncm'].startswith(p) for p in _faixas):
        pc_auto[x['ncm']]=[s(re.sub(r'\s+',' ',x['leg']).strip().rstrip(';')), s(re.sub(r'\s+',' ',x.get('obs') or '').strip())]
# Conferencia com o texto compilado da Lei 10.485/2002, Anexos I e II (Planalto, arquivo salvo em 10/11/2026, registro R13-01):
# a lista do repositorio trazia lenha (4401) e bombas da 8413 que a lei nao lista; faltavam 7320.10.00 Ex 01 e 9029.20.10.
LEI10485=('40161010 40169990 6813 70071100 70072100 70091000 73201000 83012000 83023000 84073390 84073490 840820 840991 840999 841330 '
  '84139100 84139110 84139190 84148021 84148022 841520 84212300 84213100 84314100 84314200 84339090 84818099 848310 84832000 848330 848340 848350 '
  '850520 85071000 8511 851220 85123000 851240 85129000 85272 85365090 853910 85443000 870600 8707 8708 90292010 90299010 90303921 '
  '90318040 9032892 91040000 94012000 '
  '4009 8431 84089090 84122110 84122190 84123110 84136019 84148019 84149039 84329000 84811000 84812090 84818092 8483601 85011019').split()
AUTO_FORA=sorted(k for k in pc_auto if not any(k.startswith(p_) for p_ in LEI10485))
for k in AUTO_FORA: del pc_auto[k]
pc_auto.setdefault('73201000',[s('Lei 10.485/2002, art. 3º, I, e Anexo I'),s('Apenas o Ex 01 (molas de folhas para veículos). Fora do Ex, tributação normal.')])
pc_auto.setdefault('90292010',[s('Lei 10.485/2002, art. 3º, I, e Anexo I'),-1])
if '84139110' in pc_auto and pc_auto['84139110'][1]==-1: pc_auto['84139110'][1]=s('Apenas o Ex 01 da antiga 8413.91.00 (Anexo I). Confira o Ex do produto.')
T13='Tabela 4.3.13, código '
L1='Lei 10.925/2004, art. 1º, '
PC={'meta':{'consulta':'2026-11-10','fontes':['Tabela 4.3.10 da EFD-Contribuições (Receita Federal), arquivo fornecido em 10/11/2026','Tabela 4.3.13 da EFD-Contribuições, versão 1.37, de 14/10/2026','Tabela 4.3.11, versão 1.35, e Tabela 4.3.12, de 17/11/2014, da EFD-Contribuições','Lei 10.925/2004, art. 1º, texto atualizado (Câmara dos Deputados)','Autopeças: Lei 10.485/2002, art. 3º, I e II, e Anexos I e II, texto compilado conferido em 10/11/2026 (registro R13-01); NCM com Ex da TIPI exigem conferência da descrição'],
  'aviso':'Tratamento de PIS e COFINS no regime atual, que vale só até 31/12/2026. Monofásico: alíquota zero na revenda, sem crédito na compra; fabricante e importador recolhem a alíquota concentrada. Confira os casos com Ex da TIPI.'},
 'grupos':GR,'monoR':MONO_R,'monoExc':MONO_EXC,'auto':pc_auto,'autoConc':[0.023,0.108],
 'zero':[ # prefixos, descricao, base, exato
  [['31'],'Adubos e fertilizantes',T13+'101; '+L1+'I',1],[['3808'],'Defensivos agropecuários',T13+'102; '+L1+'II',1],
  [['07133319','07133329','07133399','100620','100630','110620'],'Feijão, arroz e farinha de mandioca',T13+'105; '+L1+'V',1],
  [['300230'],'Vacinas para medicina veterinária',T13+'107; '+L1+'VII',1],
  [['110220','110313','110419'],'Farinha, grumos, sêmolas e grãos de milho',T13+'108; '+L1+'IX',1],[['010511'],'Pintos de um dia',T13+'109; '+L1+'X',1],
  [['0401','0402','0403'],'Leite fluido, leite em pó, leite fermentado, bebidas e compostos lácteos e fórmulas infantis (pela descrição; a norma não cita NCM)',T13+'110; '+L1+'XI',0],
  [['0406'],'Queijos mozarela, minas, prato, coalho, ricota, provolone, parmesão, fresco não maturado, do reino e requeijão (pela descrição)',T13+'111 e 120; '+L1+'XII',0],
  [['040410'],'Soro de leite fluido para industrialização de alimentos (pela descrição)',T13+'112; '+L1+'XIII',0],
  [['11010010'],'Farinha de trigo',T13+'113; '+L1+'XIV',1],[['1001'],'Trigo',T13+'114; '+L1+'XV',1],
  [['19012000','19059090'],'Pré-misturas para pão comum e pão comum (somente o Ex 01 da TIPI)',T13+'115; '+L1+'XVI',0],
  [['07','08'],'Produtos hortícolas e frutas',T13+'116; Lei 10.865/2004, art. 28, III',1],[['0407'],'Ovos',T13+'117; Lei 10.865/2004, art. 28, III',1],
  [['05111000','05119910','05119920'],'Sêmens e embriões',T13+'118',1],
  [['190211','190219','190220','190230'],'Massas alimentícias',T13+'119; '+L1+'XVIII',1],
  [['0201','0202','02061000','02062','02102000','05069000','05100010','150210','0203','0204','02063000','02064','0207','0209','02101','02068000','02109900'],'Carnes bovina, suína, ovina, caprina e de aves e derivados',T13+'121; '+L1+'XIX',1],
  [['0302','0303','0304'],'Peixes',T13+'122; '+L1+'XX',1],[['0901','21011'],'Café',T13+'123; '+L1+'XXI',1],[['17011400','17019900'],'Açúcar',T13+'124; '+L1+'XXII',1],
  [['1507','1508','1509','1510','1511','1512','1513','1514'],'Óleo de soja e outros óleos vegetais',T13+'125; '+L1+'XXIII',1],[['04051000'],'Manteiga',T13+'126; '+L1+'XXIV',1],
  [['15171000'],'Margarina',T13+'127; '+L1+'XXV',1],[['3306'],'Produtos de higiene bucal ou dentária',T13+'129; '+L1+'XXVII',1],[['48181000'],'Papel higiênico',T13+'130; '+L1+'XXVIII',1],
  [['8802'],'Aeronaves',T13+'201',1],[['8713'],'Cadeiras de rodas e outros veículos para pessoas com deficiência',T13+'301',1],
  [['902110'],'Artigos e aparelhos ortopédicos ou para fraturas',T13+'302',1],[['90213'],'Artigos e aparelhos de prótese',T13+'303',1],
  [['84433222','87142000','90214000','90219082','90219092'],'Produtos de acessibilidade e saúde listados',T13+'309',1],
  [['4901'],'Livros (pela definição da Lei 10.753/2003)',T13+'903; Lei 10.865/2004, art. 28, VI',0]],
 'zeroExc':['03029000']}
import sys as _s; _s.path.insert(0,'src'); from versao import VERSAO as _V
meta={'versao':_V['v'],'montadoEm':_V['data'][:10],'conferidoEm':'2026-11-10',
 'fontes':[
  'Mapa de Classificação 1.0, de 14/10/2026 (Contador Protagonista): regras por NCM e NBS. Normas: '+versao,
  'Anexo VIII, correlação item LC 116, NBS, indOp e cClassTrib, versão 1.02.00, de 26/10/2026 (preliminar)',
  'Tabela de nomes e reduções de cClassTrib: Mapa NCM RT 2026 v4 (tabela de 23/01/2026)',
  'Tabela IBPTax 26.2.D, vigente de 17/11 a 20/12/2026: conferência da lista de NCM, descrições faltantes e lista de NBS',
  'Imposto Seletivo: MP 1.399/2026, Anexos IV e V, texto oficial (avulso do Congresso, DOU de 04/11/2026) conferido em 10/11/2026; sujeita à conversão em lei'],
 'aviso':'Apoio à classificação. O NCM ou a NBS não decide sozinho: o benefício depende da condição, de quem compra, da destinação e da operação. Quem decide é o emitente, com o contador.'}
# Anexo XVII da LC 214/2025: "embarcações com motor classificadas na posição 8903". O 8903.12 descreve barco
# inflável não concebido para motor, que nunca está no alcance do IS (conferido em 10/11/2026, registro R13-02).
if '89031200' in ncm and 'XVII' in str(ncm['89031200'].get('ax') or ''):
    ncm['89031200']['ax']=re.sub(r'\s*;?\s*Anexo XVII','',ncm['89031200']['ax']).strip(' ;') or None
# ---------- R16-02: código que a lei cita sem condição além do NCM (Anexos I e XV) ----------
# Leitura item a item do texto consolidado da LC 214/2025 (conferido em 11/11/2026). Só entra o código
# cuja inclusão no item depende apenas do NCM; ficam fora os trechos com descrição, requisito ou exceção por espécie.
SEM_COND={
 ('Anexo I','1'):(['100620','100630','10064000'],[]),
 ('Anexo I','5'):(['04051000'],[]), ('Anexo I','6'):(['15171000'],[]),
 ('Anexo I','7'):(['07133319','07133329','07133399','07133590'],[]),
 ('Anexo I','8'):(['0901','21011'],[]),
 ('Anexo I','10'):(['11062000','19030000'],[]), ('Anexo I','11'):(['11022000','11031300'],[]),
 ('Anexo I','12'):(['11041900','11042300'],[]), ('Anexo I','13'):(['11010010'],[]),
 ('Anexo I','14'):(['17011400','17019900'],[]), ('Anexo I','15'):(['19021'],[]),
 ('Anexo I','17'):(['11041200','11042200'],[]), ('Anexo I','18'):(['11029000'],[]), ('Anexo I','23'):(['0903'],[]),
 # item 19: alíneas a, b, d e a parte sem descrição da alínea c. Fígado de ave congelado (0207.45 e 0207.55) pode ser foie gras: fica condicionado.
 ('Anexo I','19'):(['0201','0202','02061000','02062','02102000','0203','02063000','02064','020910','02101','0204','02109920','0207','02099000','0210991'],
                   ['02074300','02075300','02074500','02075500','02109990','02068000','02069000']),
 # item 20: em 03.02 e 03.03 a exclusão é por código; em 03.04 é por espécie, salvo nas subposições 0304.3 e 0304.6.
 ('Anexo I','20'):(['0302','0303','03043','03046'],['03021','03023','03025100','03025200','03025300','03029','03031','03034','03036300','03036400','03036500','03039']),
 ('Anexo XV','1'):(['04072'],[]),
 ('Anexo XV','2'):(['0701','0702','0703','0704','0705','0706','0707','0708','0709','0710'],['07095','07108000']),
 # item 3: só as posições que contêm apenas fruta fresca ou refrigerada; 08.03 a 08.06 têm fruta seca e 08.11 depende de açúcar.
 ('Anexo XV','3'):(['0807','0808','0809','0810'],[]),
 ('Anexo XV','5'):(['0714'],[]), ('Anexo XV','6'):(['08011'],[]),
}
COND_NCM=s('O NCM, sozinho, enquadra o produto neste item: a lei cita o código sem outra condição. Confira só se o NCM do produto está correto.')
n_sc=0
for cod,e in ncm.items():
    if e.get('e')!='c' or not e.get('r'): continue
    regra=SEM_COND.get((e.get('ax'),str(e.get('it'))))
    if not regra: continue
    inc,exc=regra
    if any(cod.startswith(p_) for p_ in inc) and not any(cod.startswith(p_) for p_ in exc):
        e['u']=1; e['c']=COND_NCM; e.pop('q',None)
        e['t']=';'.join(t for t in str(e.get('t','')).split(';') if t and t!='T2') or 'T12'
        n_sc+=1
print('R16-02 codigos sem condicao:',n_sc)
db={'meta':meta,'S':S,'ncm':ncm,'pref':pref,'nbs':nbs,'prefNbs':pref_nbs,'nbsDesc':nbs_desc,'lc':lc,'ccl':ccl,'tipos':tipos,'regras':regras,'is':IS,'dicas':DICAS,'sc':SC,'pc':PC}
json.dump(db,open('db.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
json.dump({'vig':vig,'desc':ncm_desc},open('ncm_aux.json','w',encoding='utf-8'),ensure_ascii=False)
print('strings',len(S),'ncm',len(ncm),'pref',len(pref),'nbs',len(nbs),'prefNbs',len(pref_nbs),'nbsDesc',len(nbs_desc),'lc',len(lc),'ccl',len(ccl),'regras',len(regras),'tipos',len(tipos))
import os; print(os.path.getsize('db.json'))
print([k for k,v in ccl.items() if v[2] is None])
print(json.dumps(lc[0],ensure_ascii=False)[:900]); 
m=[x for x in lc if x['i']=='04.01'][0]; print(json.dumps(m,ensure_ascii=False)[:700])
print(sum(1 for x in lc for n in x['n'] if not n[1]),'nbs sem ccl', [ (x['i'],x.get('cx')) for x in lc if x.get('cx')][:10])
print(collections.Counter(v['rt'] for v in pref.values()).most_common(8))
print(regras[0]); print(tipos.get('T2'))
