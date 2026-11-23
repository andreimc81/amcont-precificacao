import re, json, docx
from docx.table import Table
from docx.text.paragraph import Paragraph
d=docx.Document('/home/claude/dl/lc214/lc214_atual.docx')
body=d.element.body
cur=None; anexos={}; seen=set(); fim=False
for el in body.iterchildren():
    tag=el.tag.split('}')[1]
    if tag=='p':
        tx=Paragraph(el,d).text.strip()
        m=re.match(r'^ANEXO ([IVXL]+)$',tx)
        if m:
            n=m.group(1)
            if n in seen: fim=True; break
            seen.add(n); cur=n; anexos[n]={'titulo':'','notas':[],'tab':[]}
        elif cur and tx:
            if not anexos[cur]['titulo'] and not anexos[cur]['tab']: anexos[cur]['titulo']=tx
            else: anexos[cur]['notas'].append(tx)
    elif tag=='tbl' and cur:
        t=Table(el,d)
        for r in t.rows:
            cells=[]
            for c in r.cells:
                x=c.text.strip()
                if not cells or cells[-1]!=x: cells.append(x)
            anexos[cur]['tab'].append(cells)
    if 'XVII' in seen and cur=='XVIII': break
json.dump(anexos,open('/home/claude/work/audit/anexos_docx.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
for n,a in anexos.items():
    print(n,len(a['tab']),a['titulo'][:70],'| cab:',a['tab'][0] if a['tab'] else '', '| ex:',[c[:60] for c in a['tab'][1]] if len(a['tab'])>1 else '')
