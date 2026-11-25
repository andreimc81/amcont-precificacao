# Ícone da aba do navegador: só o símbolo AM da marca, em branco sobre azul-petróleo
import base64
def com_favicon(html):
    if 'rel="icon"' in html: return html
    b=base64.b64encode(open('fontes/favicon64.png','rb').read()).decode()
    tag='<link rel="icon" type="image/png" href="data:image/png;base64,'+b+'">'
    i=html.lower().find('<meta charset'); assert i>=0
    j=html.find('>',i)+1
    return html[:j]+'\n'+tag+html[j:]
