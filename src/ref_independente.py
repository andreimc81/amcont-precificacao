"""Verificacao independente (Amcont). Recalcula, a partir das definicoes legais e das premissas da MC.001, cada caso
coletado da calculadora, sem usar o codigo dela. Venda: a margem do ano, recalculada a partir do preco que a
calculadora devolveu, deve ser igual a margem de hoje recalculada a partir do preco atual. Compra: creditos e custo."""
import json, sys
C=json.load(open('ref_casos.json'))
def share_icms(an, anexo): return an[anexo]['icms'] if anexo in ('I','II') else 0.0
def cred_ano(pc, forn, t, ano, icmsC, das, anexo, trat, an, servico):
    f=t['fatorIcmsIss']; a=(t['cbs']+t['ibs'])*(1-trat)
    regc = pc*(1-icmsC*f)/(1+a)*a if a else 0.0
    cb=0.0
    if ano>=2027:
        if forn in ('regular','sn_regular'): cb=regc
        elif forn in ('sn_tradicional','sn_sublimite'):
            x=an.get(anexo,an['I']); cb=min(pc*das*(x['pis']+x['cofins']+(x['icms']+x['iss'])*(1-f)), regc)
    ic=0.0
    if not servico and forn not in ('mei','pf'):
        if forn in ('sn_tradicional','sn_regular'): ic = pc*das*share_icms(an,anexo)*f if icmsC>0 else 0.0
        else: ic = pc*icmsC*f
    return cb, ic
def cred_pc(o, pc, forn, icmsC):
    if o['regime']=='real' and forn!='pf' and o['pcReg'] in ('normal','monofab'):
        return pc*(1-(icmsC if forn in ('regular','sn_sublimite') else 0))*(o['pis']+o['cofins'])
    return 0.0
def mc_hoje(o, an, t26):
    if o['regime']=='simples': return None
    icC=0 if o['servico'] else o['icmsCompra']
    icms=o['pv']*o['icmsVenda']; base=o['pv'] if o['servico'] else o['pv']-icms
    pc_ = base*(o['pis']+o['cofins']) if o['pcReg']=='normal' else (base*o['pcConc'] if o['pcReg']=='monofab' else 0)
    lucro=o['pv']*o['r']
    _,ci=cred_ano(o['pc'],o['forn'],t26,2026,icC,o['aliqForn'],'I',o['trat'],an,o['servico'])
    return o['pv']-o['pc']-(icms+pc_+lucro-ci-cred_pc(o,o['pc'],o['forn'],icC))
def mc_ano(o, an, t, nf):
    f=t['fatorIcmsIss']; icC=0 if o['servico'] else o['icmsCompra']; i=o['icmsVenda']*f
    icms=nf*i
    if o['ano']==2026:
        k=(o['pis']+o['cofins'] if o['pcReg']=='normal' else (o['pcConc'] if o['pcReg']=='monofab' else 0))*(1 if o['servico'] else 1-i)
        _,ci=cred_ano(o['pcAno'],o['forn'],t,2026,icC,o['aliqForn'],'I',o['trat'],an,o['servico'])
        return nf-icms-nf*k-o['r']*nf-o['pcAno']+ci+cred_pc(o,o['pcAno'],o['forn'],icC)
    c=t['cbs']*(1-o['trat']); b=t['ibs']*(1-o['trat'])
    B=(nf-icms)/(1+c+b); cbs=B*c; ibs=B*b; s=o['is']; IS=B*s/(1+s)
    lucro=o['r']*(nf-cbs-ibs-IS)
    cb,ci=cred_ano(o['pcAno'],o['forn'],t,o['ano'],icC,o['aliqForn'],'I',o['trat'],an,o['servico'])
    return nf-icms-cbs-ibs-IS-lucro-o['pcAno']+cb+ci
ok=n=0; fal=[]
t26={'cbs':0,'ibs':0,'fatorIcmsIss':1}
for x in C['venda']:
    o=x['o']
    if o['regime']=='simples' or x['A']['tipo']!='geral': continue
    n+=1; m0=mc_hoje(o,x['anexos'],t26); m1=mc_ano(o,x['anexos'],x['t'],x['A']['nf'])
    good=abs(m0-x['H']['mc'])<0.005 and abs(m1-m0)<0.005
    ok+=good
    if not good: fal.append((o,m0,m1,x['H']['mc'],x['A']['nf']))
print('VENDA regime geral: %d de %d casos com a margem preservada pela definição legal'%(ok,n))
for f in fal[:4]: print('  falha',json.dumps(f)[:400])
# Simples tradicional: NF x (1 - DAS) = margem + compra (sem monofasico)
ok2=n2=0
for x in C['venda']:
    o=x['o']
    if o['regime']!='simples' or o['pcReg'] not in ('normal','zero') or x['A']['trad'] is None: continue
    n2+=1; ok2+= abs(x['A']['trad']*(1-o['aliqSN'])-o['pcAno']-x['H']['mc'])<0.005
print('VENDA Simples tradicional: %d de %d'%(ok2,n2))
# Compra
ok3=n3=0; fal3=[]
for x in C['compra']:
    o,c,k=x['o'],x['c'],x['k']; n3+=1
    icC=0 if o['servico'] else c['icms']/100
    cb,ci=cred_ano(c['preco'],c['reg'],x['t'],o['ano'],icC,c['das']/100,c['anexo'],o['trat'],x['anexos'],o['servico'])
    if o['regime']=='simples' and not o['snReg']: cb=0
    if o['regime']=='simples' or o['servico'] or o['destino']=='uso': ci=0
    pc_=cred_pc(o,c['preco'],c['reg'],icC) if (o['ano']<2027 and o['destino']=='revenda') else 0
    dif=0.0
    if c['fora'] and not o['servico'] and o['destino']!='revenda':
        car=o['icmsSC']; d=(1-icC)*car/(1-car)-icC if o['difalDupla'] else car-icC
        dif=c['preco']*max(0,d)*x['t']['fatorIcmsIss']
    custo=c['preco']-cb-ci-pc_+dif
    good=all(abs(a-b)<1e-6 for a,b in ((cb,k['cbsIbs']),(ci,k['icms']),(pc_,k['pc']),(dif,k['difal']),(custo,k['custo'])))
    ok3+=good
    if not good: fal3.append((o,c,[cb,ci,pc_,dif,custo],k))
print('COMPRA: %d de %d casos iguais (créditos, DIFAL e custo)'%(ok3,n3))
for f in fal3[:4]: print('  falha',json.dumps(f)[:500])
sys.exit(0 if (ok==n and ok2==n2 and ok3==n3) else 1)
