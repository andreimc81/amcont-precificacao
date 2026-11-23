const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign, ImageRun, TableLayoutType, Header, PageNumber } = require('docx');
const fs = require('fs');
const logoData = fs.readFileSync("logo_amcont.png");
const PETROLEO="2A5F6B", PETROLEO_L="D6E8EB", PETROLEO_M="4A8FA0", CINZA_L="F5F5F5", CINZA_BD="CCCCCC", BRANCO="FFFFFF", PRETO="1A1A1A";
const W=9360, FX=TableLayoutType.FIXED;
const border=(c=CINZA_BD)=>({style:BorderStyle.SINGLE,size:4,color:c});
const borders=(c=CINZA_BD)=>({top:border(c),bottom:border(c),left:border(c),right:border(c)});
const txt=(text,o={})=>new TextRun({text,font:"Arial",size:o.size??20,bold:o.bold??false,color:o.color??PRETO,italics:o.italic??false,language:{value:"pt-BR"}});
// texto com **negrito**
const rich=(s,o={})=>s.split(/(\*\*[^*]+\*\*)/).filter(Boolean).map(p=>p.startsWith("**")?txt(p.slice(2,-2),{...o,bold:true}):txt(p,o));
const par=(children,o={})=>new Paragraph({alignment:o.align??AlignmentType.LEFT,spacing:{before:o.before??0,after:o.after??0},keepNext:o.keepNext??false,children:Array.isArray(children)?children:[children]});
const cell=(w,fill,kids,o={})=>new TableCell({borders:borders(o.bc??CINZA_BD),shading:{fill,type:ShadingType.CLEAR},width:{size:w,type:WidthType.DXA},margins:{top:80,bottom:80,left:o.left??120,right:120},verticalAlign:o.va??VerticalAlign.CENTER,rowSpan:o.rowSpan,children:kids});
const tbl=(cols,rows)=>new Table({width:{size:W,type:WidthType.DXA},columnWidths:cols,layout:FX,rows});
const row=(cells,o={})=>new TableRow({children:cells,cantSplit:true,tableHeader:o.header??false});

function makeHeader(tipo,codigo,titulo,rev){
  return tbl([2200,4960,2200],[
    row([cell(2200,BRANCO,[new Paragraph({alignment:AlignmentType.CENTER,children:[new ImageRun({data:logoData,type:"png",transformation:{width:100,height:32}})]})],{bc:PETROLEO,rowSpan:2}),
         cell(4960,PETROLEO,[par([txt(tipo,{bold:true,size:24,color:BRANCO})],{align:AlignmentType.CENTER})],{bc:PETROLEO}),
         cell(2200,PETROLEO_L,[par([txt("Código:",{bold:true,size:18,color:PETROLEO})],{align:AlignmentType.CENTER}),par([txt(codigo,{bold:true,size:22,color:PETROLEO})],{align:AlignmentType.CENTER})],{bc:PETROLEO})]),
    row([cell(4960,PETROLEO_L,[par([txt(titulo,{bold:true,size:20,color:PETROLEO})],{align:AlignmentType.CENTER})],{bc:PETROLEO}),
         cell(2200,BRANCO,[par([txt("Rev.: "+rev,{size:18})],{align:AlignmentType.CENTER}),
           new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({font:"Arial",size:18,color:PRETO,children:["Folha: ",PageNumber.CURRENT," / ",PageNumber.TOTAL_PAGES]})]})],{bc:PETROLEO})]),
  ]);
}
const secTitle=t=>tbl([W],[row([cell(W,PETROLEO,[par([txt(t,{bold:true,size:20,color:BRANCO})],{keepNext:true})],{bc:PETROLEO,left:160})])]);
const labels=pairs=>tbl([2300,7060],pairs.map(([l,v])=>row([cell(2300,PETROLEO_L,[par([txt(l,{bold:true,color:PETROLEO})])],{bc:PETROLEO_M}),cell(7060,BRANCO,[par(rich(v))],{bc:PETROLEO_M})])));
const passos=(lista,cab="Descrição da etapa")=>tbl([600,8760],[
  row([cell(600,PETROLEO_M,[par([txt("Nº",{bold:true,color:BRANCO})],{align:AlignmentType.CENTER})],{bc:PETROLEO_M}),cell(8760,PETROLEO_M,[par([txt(cab,{bold:true,color:BRANCO})])],{bc:PETROLEO_M,left:160})],{header:true}),
  ...lista.map((p,i)=>row([cell(600,PETROLEO_L,[par([txt(String(i+1),{bold:true,color:PETROLEO})],{align:AlignmentType.CENTER})]),cell(8760,i%2?CINZA_L:BRANCO,[par(rich(p))],{left:160})]))]);
const alertas=lista=>tbl([500,8860],lista.map((a,i)=>row([cell(500,PETROLEO_L,[par([txt("!",{bold:true,color:PETROLEO})],{align:AlignmentType.CENTER})]),cell(8860,i%2?CINZA_L:BRANCO,[par(rich(a))],{left:160})])));
const grade=(cols,cab,linhas)=>tbl(cols,[
  row(cab.map((c,i)=>cell(cols[i],PETROLEO_M,[par([txt(c,{bold:true,size:18,color:BRANCO})])],{bc:PETROLEO_M})),{header:true}),
  ...linhas.map((l,j)=>row(l.map((c,i)=>cell(cols[i],j%2?CINZA_L:BRANCO,[par(rich(c,{size:18}))],{va:VerticalAlign.TOP}))))]);
const rodape=(data)=>tbl([2340,2340,2340,2340],[
  row([cell(2340,PETROLEO_L,[par([txt("Elaborado por:",{bold:true,size:18,color:PETROLEO})])],{bc:PETROLEO_M}),cell(2340,BRANCO,[par([txt("Andrei Constantino",{size:18})])],{bc:PETROLEO_M}),
       cell(2340,PETROLEO_L,[par([txt("Aprovado por:",{bold:true,size:18,color:PETROLEO})])],{bc:PETROLEO_M}),cell(2340,BRANCO,[par([txt("Andrei Constantino",{size:18})])],{bc:PETROLEO_M})]),
  row([cell(2340,PETROLEO_L,[par([txt("Data de emissão:",{bold:true,size:18,color:PETROLEO})])],{bc:PETROLEO_M}),cell(2340,BRANCO,[par([txt(data,{size:18})])],{bc:PETROLEO_M}),
       cell(2340,PETROLEO_L,[par([txt("Data de aprovação:",{bold:true,size:18,color:PETROLEO})])],{bc:PETROLEO_M}),cell(2340,BRANCO,[par([txt(data,{size:18})])],{bc:PETROLEO_M})])]);
const nota=t=>par(rich(t,{size:16,italic:true,color:"555555"}),{before:80});

function montar(spec,saida){
  const kids=[];
  spec.secoes.forEach(s=>{ kids.push(secTitle(s.t)); (s.c||[]).forEach(x=>kids.push(x)); kids.push(par("")); });
  kids.push(rodape(spec.data));
  if (spec.assinatura) kids.push(nota(spec.assinatura));
  const doc=new Document({ styles:{default:{document:{run:{font:"Arial",size:20,language:{value:"pt-BR"}}}}},
    sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:1000,right:1273,bottom:900,left:1273,header:500}}},
      headers:{default:new Header({children:[makeHeader(spec.tipo,spec.codigo,spec.titulo,spec.rev),par("")]})}, children:kids}]});
  return Packer.toBuffer(doc).then(b=>fs.writeFileSync(saida,b));
}
const HOJE="10/11/2026";

/* =================== IT.002: CONTABILIDADE =================== */
const it002={tipo:"INSTRUÇÃO DE TRABALHO",codigo:"IT.002",titulo:"OPERAÇÃO: Envio e suporte das calculadoras da reforma tributária ao cliente",rev:"03",data:HOJE,
 secoes:[
 {t:"1. OBJETIVO",c:[labels([["Objetivo","Padronizar a preparação, o envio e o suporte das calculadoras de preço da reforma tributária entregues ao cliente, garantindo que ele receba somente os arquivos certos, na versão vigente e com orientação suficiente para não formar preço com dado errado."]])]},
 {t:"2. RESPONSÁVEL E APLICAÇÃO",c:[labels([["Responsável","Equipe fiscal e contábil da Amcont, com revisão do contador responsável"],["Periodicidade","A cada novo cliente e a cada nova versão dos dados"],["Sistema","Arquivos HTML (navegador), planilha Excel de uso interno e WhatsApp ou e-mail para envio"],["Prazo legal","Não se aplica. A CBS e o IBS passam a ser cobrados em 2027"]])]},
 {t:"3. O QUE VAI E O QUE NÃO VAI PARA O CLIENTE",c:[grade([3400,1400,4560],["Arquivo","Vai?","Motivo"],[
   ["amcont-cliente.html","**Sim**","Calculadora da empresa em modo cliente, sem a aba Configurar."],
   ["amcont-produto.html","**Sim**","Calculadora de um produto ou serviço: preço de venda com a nota fiscal, custo real de compra e busca por NCM, NBS e código do serviço."],
   ["MU.001 Manual do cliente (PDF)","**Sim**","Orientação de uso em linguagem simples."],
   ["amcont-precificacao.html","**Não**","Versão interna, com a aba Configurar aberta. O cliente poderia alterar alíquotas."],
   ["Amcont_Precificacao_Reforma_Tributaria.xlsx","**Não**","Ferramenta de trabalho da Amcont. Contém as bases completas e fórmulas abertas."],
   ["RC.001, MC.001, IT.001 e IT.002","**Não**","Documentos internos: roteiro comercial, memória de cálculo e instruções."],
   ["Pasta geradores_base_fiscal","**Não**","Scripts de atualização da base. Uso exclusivo da Amcont."],
   ["Arquivos .json de outros clientes","**Nunca**","Contêm dados de faturamento e custos. Cada cliente recebe apenas os próprios estudos."]]),
   nota("Não envie a pasta inteira zipada. O pacote do cliente tem três arquivos: duas calculadoras e o manual.")]},
 {t:"4. PASSO A PASSO DE PREPARAÇÃO E ENVIO",c:[passos([
   "**Confirmar a versão dos dados.** Abrir o amcont-precificacao.html, entrar na aba Configurar e conferir a versão (hoje 2026.2, de 10/11/2026, com base fiscal 2026.7) e o aviso da CBS provisória. Se houver norma nova, atualizar antes de enviar.",
   "**Definir a senha do cliente.** A senha padrão é de teste e não deve ir para o cliente. Solicitar ao responsável a geração dos dois HTMLs com a senha definida pela Amcont.",
   "**Conferir o botão de contato.** No amcont-cliente.html, clicar no botão final e confirmar que abre o WhatsApp da Amcont.",
   "**Testar os dois arquivos.** Abrir cada HTML no navegador, entrar com a senha e rodar um caso do próprio cliente (um produto ou serviço real, com o preço de compra e de venda atuais).",
   "**Fazer a triagem fiscal antes.** Na planilha, aba CLASSIFICACAO, colar os principais NCM ou NBS do cliente. Anotar os que saírem como CONFERIR ou ESCOLHER e definir com o cliente qual classificação se aplica. Para prestador de serviço, usar a aba SERVICO com o código do serviço da nota: se o item admitir mais de uma NBS, a Amcont escolhe e envia o estudo salvo (.json) com o pacote.",
   "**Montar o pacote.** Compactar somente amcont-cliente.html, amcont-produto.html e o MU.001 em PDF. Nome sugerido: Amcont-Calculadoras-Reforma-NomeDoCliente.zip.",
   "**Enviar em dois canais.** Arquivo por e-mail ou WhatsApp e senha por outro canal (ligação ou mensagem separada). Nunca enviar senha e arquivo na mesma mensagem.",
   "**Orientar na entrega.** Fazer uma chamada de 20 a 30 minutos na primeira entrega, simulando junto um produto do cliente e explicando os selos Integral, Conferir e Escolher.",
   "**Registrar o envio.** Anotar no cadastro do cliente a data, a versão dos dados enviada e quem recebeu.",
   "**Reenviar quando a versão mudar.** A cada atualização de alíquota ou de base fiscal, enviar novo pacote e pedir ao cliente que apague o anterior. Os estudos salvos em .json continuam abrindo na versão nova."])]},
 {t:"5. COMO O CLIENTE USA E O QUE A AMCONT CONFERE",c:[grade([2700,3330,3330],["Situação na ferramenta","O que o cliente vê","O que a Amcont faz"],[
   ["Selo **Integral**","Sem benefício nos anexos. Alíquota cheia de CBS e IBS.","Conferir se não há regra por adquirente, operação ou regime (aba BD_REGRAS)."],
   ["Selo **Conferir**","Há redução, mas condicionada. O painel mostra o preço com e sem o benefício.","Confirmar a condição legal com o cliente e registrar a decisão."],
   ["Selo **Escolher**","Mais de uma regra para o mesmo código. A simulação usa a menor redução até a escolha.","Definir a opção correta pelo produto e pela destinação reais."],
   ["Selo **Não localizado**","Código fora da tabela oficial.","Revisar o NCM ou a NBS no cadastro do cliente."],
   ["Aviso de **Imposto Seletivo**","Alíquota sugerida, ou campo em zero para veículos e cigarros.","Informar a alíquota correta nos casos em zero."],
   ["Painel do **Simples**","Compara permanecer no Simples tradicional com optar pelo regime regular.","Avaliar a opção considerando o perfil dos compradores e as janelas de opção."]])]},
 {t:"6. PONTOS DE ATENÇÃO",c:[alertas([
   "**Senha própria do cliente.** Ele pode definir uma senha no primeiro acesso, válida só no navegador dele. A senha original continua servindo para redefinir, pelo link Esqueci minha senha.",
   "**A senha não é segurança.** Ela apenas dificulta o acesso casual. Quem tem o arquivo e conhecimento técnico consegue abrir. Por isso nenhum dado de cliente fica gravado dentro do HTML.",
   "**Os dados do cliente ficam no computador dele.** As calculadoras não enviam nada pela internet. O estudo só existe no arquivo .json que o cliente salva.",
   "**A CBS é provisória.** Os 11,2% e 11,3% vêm do cálculo do TCU e aguardam resolução do Senado. Ao sair a resolução, atualizar e reenviar.",
   "**O código não decide sozinho.** A maioria dos benefícios é condicional. Nunca validar um preço com redução sem confirmar a condição.",
   "**PIS e COFINS de hoje por NCM:** monofásico e alíquota zero zeram o débito e o crédito atuais, o que aumenta a margem de hoje e, em geral, o preço necessário em 2027. Fabricante e importador de monofásico têm alíquota concentrada, não simulada. Conferir os casos com Ex da TIPI.",
   "**ICMS de SC cobre só a alíquota interna** (Lei 10.297/1996, art. 19, e RICMS/SC, Anexo 2). Não cobre ST, TTD, crédito presumido nem interestaduais. Isenção e carga de 7% da cesta básica vencem em 31/12/2026: conferir a prorrogação antes de simular 2027.",
   "**Premissa de cálculo:** CBS e IBS fora da própria base e fora do ICMS e ISS (LC 214, art. 12, § 2º); ICMS e ISS sobre o total da nota. Na versão interna, a premissa pode ser trocada para medir a tese do contribuinte.",
   "**Imposto Seletivo e regimes específicos são aproximações.** Veículos, cigarros, imóveis, bares, hotelaria, combustíveis e serviços financeiros exigem análise da Amcont.",
   "**A ferramenta apoia, não substitui o parecer.** Decisão de preço, de regime ou de classificação fiscal relevante deve ser registrada por escrito pela Amcont.",
   "**A base fiscal contém conteúdo de terceiros** (Mapa de Classificação). Manter a distribuição restrita aos clientes ativos."])]},
 {t:"7. DÚVIDAS FREQUENTES DO CLIENTE",c:[grade([3600,5760],["Pergunta","Resposta padrão"],[
   ["O arquivo não abre ou abre como texto.","Extrair o .zip antes de abrir e usar Chrome, Edge ou Firefox atualizados. Não abrir de dentro do .zip nem pelo visualizador do WhatsApp."],
   ["Preciso de internet?","Não para calcular. A internet só carrega as fontes de letra. Sem ela, a aparência muda, mas a conta é a mesma."],
   ["Funciona no celular?","Funciona, mas o uso recomendado é no computador, pela quantidade de campos."],
   ["Perdi o que digitei.","Os dados não ficam gravados ao fechar. Usar Salvar estudo ou Salvar simulação e guardar o arquivo .json."],
   ["Esqueci a senha.","Reenviar a senha por canal separado, após confirmar a identidade do solicitante."],
   ["O preço deu menor que o de hoje. Está certo?","Pode estar. Com crédito amplo na compra, a carga de alguns produtos cai. Conferir se a redução aplicada é devida."],
   ["Posso repassar a ferramenta a terceiros?","Não. O uso é exclusivo do cliente Amcont."]])]},
 {t:"8. CONTROLE DE REVISÕES",c:[grade([900,1700,4960,1800],["Rev.","Data","Descrição da alteração","Responsável"],[["01 a 03",HOJE,"Versão inicial, busca pelo código do serviço, nota fiscal da venda e simulação de compra.","A. Constantino"]])]},
 ]};

/* =================== MU.001: CLIENTE =================== */
const mu001={tipo:"MANUAL DE USO",codigo:"MU.001",titulo:"Calculadoras de preço na reforma tributária",rev:"03",data:HOJE,
 assinatura:"Amcont Assessoria & Contabilidade  ·  CRC/SC 011862/O-0  ·  amcont@amcontassessoria.com.br  ·  WhatsApp (48) 99826-6207",
 secoes:[
 {t:"1. PARA QUE SERVE",c:[labels([["Objetivo","A partir de 2027 os tributos sobre as vendas mudam: entram a CBS e o IBS e, aos poucos, saem o PIS, a COFINS, o ICMS e o ISS. Estas calculadoras mostram **qual preço de venda mantém o mesmo ganho que você tem hoje**, ano a ano, até 2033."],
   ["O que você recebeu","**amcont-produto.html**: preço de um produto ou serviço específico. **amcont-cliente.html**: efeito no faturamento da empresa inteira. **Este manual.**"]])]},
 {t:"2. COMO ABRIR",c:[passos([
   "Salve o arquivo .zip no computador e **extraia** o conteúdo (botão direito, Extrair tudo). Não abra os arquivos de dentro do .zip.",
   "Dê dois cliques no arquivo .html. Ele abre no navegador (Chrome, Edge ou Firefox).",
   "Digite a **senha** que a Amcont enviou em mensagem separada e clique em Entrar.",
   "Pronto. Nada é instalado e nenhum dado seu é enviado pela internet: tudo fica no seu computador."])]},
 {t:"3. PREÇO DE UM PRODUTO OU SERVIÇO (amcont-produto.html)",c:[passos([
   "Escolha **Produto, por NCM** ou **Serviço, por NBS ou LC 116**.",
   "Digite o código ou parte da descrição no campo de busca e clique no item da lista. O NCM está na nota fiscal de compra do produto.",
   "**Para serviço, digite o código do serviço que você usa na nota fiscal**: o item da lista de serviços (04.01) ou o código de tributação nacional (040101). Clique na linha que começa com **LC 116**. Se o item tiver uma única classificação, a ficha já aparece pronta. Se tiver várias, a ferramenta lista os códigos NBS possíveis: marque o que descreve o seu serviço. Em caso de dúvida entre dois, não escolha: pergunte à Amcont.",
   "Leia a **ficha** que aparece abaixo da busca. Ela mostra o selo, a redução de imposto prevista e a condição para ter direito a ela (veja o item 4).",
   "Em **Sua empresa**, informe o regime tributário, a atividade e a alíquota de ICMS (produto) ou de ISS (serviço) da sua venda.",
   "Em **A compra deste produto**, informe quanto você paga hoje ao fornecedor, o regime dele e o ICMS da nota de compra. Para serviço, informe os insumos comprados com nota para prestar aquele serviço.",
   "Em **A venda deste produto**, informe o preço pelo qual você vende hoje. O campo **PIS e COFINS hoje** vem em Automático: a ferramenta identifica se o produto é monofásico ou tem alíquota zero, o que muda a sua margem atual.",
   "Escolha o **ano** (2027 a 2033). O painel da direita mostra o **preço necessário** para manter a mesma margem, com cada tributo detalhado.",
   "Logo abaixo, o quadro **Nota fiscal desta venda** mostra a nota de uma unidade: valor do produto, ICMS, CBS, IBS e o **total da nota, que é o que o seu cliente paga** e o preço de etiqueta ao consumidor.",
   "Veja o quadro **Mesmo produto, fornecedores diferentes**: ele compara o custo real de comprar de empresa do Lucro Real ou Presumido, do Simples, de MEI ou de pessoa física.",
   "Na ficha, o quadro **ICMS em Santa Catarina** mostra a alíquota interna conforme quem compra (consumidor final ou contribuinte) e os benefícios da cesta básica. Marque a opção para levá-la ao cálculo.",
   "Para consultar vários códigos de uma vez, clique em **Consultar tributação por código**, cole a lista de NCM, NBS ou códigos de serviço e clique em Consultar. Um código de serviço abre em uma linha para cada NBS possível. O botão Simular leva o código para a calculadora.",
   "Clique em **Salvar estudo** para guardar. Use **Imprimir ou salvar em PDF** para levar à reunião."],"O que fazer")]},
 {t:"4. CUSTO REAL DE UMA COMPRA (amcont-produto.html)",c:[passos([
   "Clique em **Simular uma compra: custo real**, no alto da tela, e busque o produto ou serviço como na venda.",
   "Em **Sua empresa**, informe o regime. No Simples, diga se recolhe a CBS e o IBS dentro do DAS ou pelo regime regular. Escolha a **destinação**: revenda ou insumo, uso e consumo ou imobilizado.",
   "Em **Cotações de compra**, uma linha por fornecedor: regime, valor total da nota e ICMS da nota. Para fornecedor do Simples, informe também o DAS e o anexo dele. O botão **Comparar os 5 regimes** repete o preço da 1ª linha em todos os regimes.",
   "O painel **Custo real da compra** mostra quanto cada nota custa de verdade depois dos créditos e avisa quando **a nota mais barata não é a compra mais barata**. A coluna **Preço máximo para empatar** é o teto a negociar com cada fornecedor.",
   "Clique em uma linha para ver a nota daquele fornecedor e o que você recupera. O botão **Levar a melhor cotação** usa essa compra na simulação de venda."],"O que fazer")]},
 {t:"5. COMO LER A FICHA DO PRODUTO OU SERVIÇO",c:[grade([2200,3580,3580],["Selo","O que significa","O que fazer"],[
   ["**Integral**","A lei não prevê redução para este código. Vale a alíquota cheia.","Pode simular. Se achar que seu caso tem benefício, fale com a Amcont."],
   ["**Conferir**","Existe redução, mas ela depende de uma condição (tipo de produto, quem compra, registro, destinação).","Leia a condição. **Só conte com a redução depois de confirmar com a Amcont.**"],
   ["**Escolher**","A lei traz mais de uma regra para o mesmo código.","Marque a opção que corresponde ao seu produto. Na dúvida, não escolha: pergunte."],
   ["**Não localizado**","O código não existe na tabela oficial.","Confira o código na nota fiscal ou com a Amcont."]]),
   nota("Quando há redução, o painel mostra em vermelho o **Risco do benefício**: quanto o preço teria de subir se a condição não for atendida. Use esse número para decidir com segurança.")]},
 {t:"6. EFEITO NA EMPRESA INTEIRA (amcont-cliente.html)",c:[passos([
   "Escolha o que quer calcular: **Preço de um produto novo** (parte do custo e da margem desejada) ou **Reajuste do preço atual** (parte do seu faturamento de hoje).",
   "Informe o **regime tributário**, a **atividade** e a alíquota de ICMS ou ISS das suas vendas.",
   "No reajuste, informe o **faturamento anual** e os **gastos do ano** separados por tipo de crédito. Se não souber separar, peça os valores à Amcont.",
   "Arraste o **ano** ao longo da transição e acompanhe como o preço e os tributos se comportam até 2033.",
   "Clique em **Salvar simulação** para guardar e em **Imprimir ou salvar em PDF** para registrar."],"O que fazer")]},
 {t:"7. SALVAR E REABRIR",c:[labels([["Salvar","O botão de salvar gera um arquivo com final **.json** na pasta de downloads. Guarde-o em uma pasta da empresa. Ao fechar o navegador sem salvar, os dados digitados se perdem."],
   ["Reabrir","Abra a calculadora, clique em **Abrir estudo** (ou Abrir simulação) e selecione o arquivo .json."],
   ["Enviar à Amcont","Para tirar dúvida sobre um cálculo, envie o arquivo .json. Assim vemos exatamente o que você simulou."]])]},
 {t:"8. PONTOS DE ATENÇÃO",c:[alertas([
   "**O resultado é uma simulação, não uma garantia.** Ele ajuda a decidir, mas não substitui a análise da Amcont para o seu caso.",
   "**A CBS ainda é provisória.** O percentual usado vem do cálculo oficial mais recente e aguarda definição do Senado. Quando mudar, a Amcont envia versão nova.",
   "**O código do produto não decide sozinho.** A redução de imposto depende de condições da lei. Selo Conferir ou Escolher pede confirmação antes de alterar preço.",
   "**ICMS de Santa Catarina é uma referência.** A ferramenta traz a alíquota interna da lei. Substituição tributária, regimes especiais (TTD) e vendas para outros estados não são calculados, e os benefícios da cesta básica valem até 31/12/2026.",
   "**Margem de contribuição não é lucro.** É o que sobra da venda depois da compra e dos tributos, antes das despesas fixas.",
   "**Não altere preços de tabela só com base na ferramenta.** Traga o estudo para validarmos juntos, principalmente em produtos de alto giro.",
   "**Uso exclusivo.** A ferramenta e a senha são para a sua empresa. Não repasse a terceiros."])]},
 {t:"9. DÚVIDAS FREQUENTES",c:[grade([3600,5760],["Pergunta","Resposta"],[
   ["O arquivo não abre.","Extraia o .zip antes e abra com Chrome, Edge ou Firefox. Não abra pelo visualizador do WhatsApp ou do e-mail."],
   ["Preciso de internet?","Não para calcular."],
   ["Funciona no celular?","Funciona, mas é mais confortável no computador."],
   ["Onde acho o NCM?","Na nota fiscal de compra, em cada item, ou no cadastro de produtos do seu sistema."],
   ["Onde acho o código do serviço?","Na sua nota fiscal de serviço, no campo do código de tributação ou do item da lista de serviços. São quatro ou seis dígitos, como 04.01 ou 040101."],
   ["Qual preço eu marco na etiqueta?","O **total da nota**, mostrado no quadro Nota fiscal desta venda. Se o seu sistema soma a CBS e o IBS por fora, cadastre o valor do produto mostrado no mesmo quadro. Confirme com o fornecedor do sistema antes de mudar o cadastro."],
   ["Como comparo dois fornecedores?","Pelo custo real, no modo **Simular uma compra**. Nota mais barata nem sempre é compra mais barata: depende do crédito que cada fornecedor transfere."],
   ["O que é NBS?","É a nomenclatura dos serviços usada na reforma tributária. A ferramenta encontra a NBS a partir do código do serviço que você já usa na nota."],
   ["O preço deu menor que o de hoje. Está certo?","Pode estar: em alguns casos o crédito na compra compensa o imposto novo. Envie o estudo para conferirmos."],
   ["Sou do Simples. Muda algo para mim?","A calculadora compara permanecer no Simples tradicional com optar pelo regime regular de CBS e IBS. Essa decisão deve ser tomada junto com a Amcont."],
   ["Posso trocar a senha?","Sim. Depois de entrar, clique em **Definir senha própria**. A nova senha vale só naquele navegador e computador."],
   ["Esqueci a senha.","Na tela de entrada, clique em **Esqueci minha senha** e digite a senha original enviada pela Amcont. Se não a tiver, fale conosco pelo WhatsApp (48) 99826-6207."]])]},
 ]};

/* =================== RC.001 rev. 03 =================== */
const rc001={tipo:"ROTEIRO COMERCIAL",codigo:"RC.001",titulo:"Reforma Tributária e Precificação",rev:"03",data:HOJE,
 secoes:[
 {t:"1. O QUE A AMCONT ESTÁ VENDENDO",c:[labels([
   ["Proposta","Não vendemos medo da reforma. Vendemos a resposta a uma pergunta que o cliente não consegue responder sozinho: **quanto ele precisa cobrar em cada ano da transição para continuar ganhando o mesmo**."],
   ["Por que só nós","A resposta depende de quatro dados que estão na escrituração que já fazemos: quanto ele compra de fornecedor que gera crédito, o regime desses fornecedores, como o produto é tributado hoje de PIS e COFINS e qual a regra de CBS e IBS do NCM ou do serviço."],
   ["Frase que sustenta a venda","\"O senhor não precisa de opinião sobre a reforma. Precisa de número. E o número depende de dados que já estão na sua escrituração, com a gente.\""]])]},
 {t:"2. O QUE NUNCA DIZER",c:[grade([3300,6060],["Não diga","Por quê"],[
   ["\"A reforma vai aumentar seus impostos.\"","Depende do produto e das compras. No mesmo cenário, o preço necessário em 2027 vai de queda de 11% (fabricante de medicamento) a alta de 5% (revenda de autopeças no Lucro Real). O sinal inverte."],
   ["\"Em 2027 não muda nada.\"","Vale para quem já paga PIS e COFINS cheios. Para quem revende produto monofásico ou com alíquota zero, 2027 é o ano do salto, porque a venda passa a pagar CBS."],
   ["\"O Simples vai acabar.\"","Não vai. Surge a opção de recolher CBS e IBS pelo regime regular, por semestre, com ponto de virada calculável."],
   ["\"Fornecedor do Simples fica inviável.\"","Ele transfere menos crédito: só o que paga dentro do DAS. A diferença é mensurável produto a produto e pode ser compensada no preço de compra."],
   ["Qualquer número sem dizer a premissa.","A lei não definiu se CBS e IBS entram na base do ICMS e do ISS. Isso muda o preço de 2027 em cerca de 1,2% e deixa de existir em 2033."],
   ["Qualquer número de CBS como definitivo.","A CBS de 11,2% e 11,3% é o cálculo do TCU e aguarda resolução do Senado."]])]},
 {t:"3. TRIAGEM DA CARTEIRA",c:[grade([1300,4030,4030],["Faixa","Critério objetivo","Como abordar"],[
   ["**ALTA**","Revende monofásico ou produto com alíquota zero de PIS e COFINS (farmácia, autopeças, bebidas, mercado); presta serviço no Lucro Presumido com poucas compras; vende a consumidor final com margem abaixo de 15%.","Reunião individual e paga. O impacto pode consumir parcela relevante da margem."],
   ["**MÉDIA**","Vende para empresa do regime regular; entradas divididas entre crédito integral e reduzido; margem entre 15% e 30%.","Reunião em grupo ou simulação enviada. O impacto existe e é absorvível."],
   ["**BAIXA**","Indústria ou comércio que já paga PIS e COFINS não cumulativos, compra de fornecedor do regime regular e vende para empresa.","Comunicado por escrito. Tende a manter ou reduzir preço."],
   ["**SIMPLES**","Optante do Simples Nacional, qualquer anexo.","Trilha própria. A pergunta é se compensa optar pelo regime regular. Próxima janela: março de 2027, para valer em julho."]]),
   nota("Erro de triagem mais comum: olhar só o volume de compras. Entrada com redução de 60% gera 40% do crédito de uma entrada integral, e compra de fornecedor do Simples gera só a parcela que ele paga no DAS.")]},
 {t:"4. NÚMEROS PARA SABER DE CABEÇA",c:[grade([3200,1500,4660],["Situação","Número","O que significa"],[
   ["Comércio no Lucro Real, ICMS de 12%, custo constante: 2027","+1,0%","Quem já paga PIS e COFINS não cumulativos quase não sente em 2027."],
   ["O mesmo caso em 2033","+3,8%","Teto de impacto, com custo mantido constante. O crédito maior nas compras reduz esse número."],
   ["Revenda de medicamento monofásico, Lucro Presumido, 2027","+1,8%","Antes da reforma não pagava PIS e COFINS na revenda. Passa a pagar CBS, com redução de 60%."],
   ["Revenda de autopeça, Lucro Real, 2028","+4,6%","Monofásico sem redução de CBS: é o perfil mais exposto."],
   ["Fabricante de medicamento, Lucro Presumido, 2027","-11%","Sai de 12% concentrados para a CBS reduzida. A carga migra para o revendedor."],
   ["Faixa da premissa jurídica em 2027","1,2%","Diferença entre incluir ou não a CBS e o IBS na base do ICMS. Zera em 2033."],
   ["Simples, Anexo I, receita de R$ 1 milhão: ponto de virada","R$ 645 mil","Compras que geram crédito. Acima disso, optar pelo regime regular reduz a carga."],
   ["Peso do crédito por faixa","100 / 70 / 40 / 30","Quanto vale o crédito de uma entrada integral, com redução de 30%, de 60% e de 70%."]]),
   nota("Números de referência calculados em 10/11/2026 com CBS provisória de 11,2% (2027 e 2028) e 11,3%, IBS de 0,1% em 2027 e 2028 e premissa da LC 214/2025, art. 12. Servem de referência mental, não de resposta ao caso do cliente.")]},
 {t:"5. ROTEIRO DA REUNIÃO, 40 MINUTOS",c:[grade([500,900,2500,5460],["Nº","Tempo","Bloco","O que fazer e o que falar"],[
   ["1","5 min","Ancoragem no negócio dele","Fazer o cliente falar primeiro. \"Hoje, como o senhor forma o preço? Pega o custo e multiplica, olha o concorrente ou usa outro critério?\""],
   ["2","3 min","Enquadrar o problema certo","Trocar \"vai aumentar?\" por \"quanto, quando e em qual produto?\". \"A reforma muda quem paga o quê ao longo da cadeia. Quem entende primeiro negocia melhor.\""],
   ["3","8 min","Simulação ao vivo","Abrir a calculadora de produto com dois ou três itens reais dele, já carregados. Mostrar a ficha do NCM: regra de CBS e IBS, PIS e COFINS de hoje e ICMS."],
   ["4","6 min","Linha do tempo até 2033","Mostrar o ano em que o produto dele sente mais. Para monofásico e alíquota zero é 2027. Para os demais, o efeito cresce de 2029 a 2033."],
   ["5","5 min","Mostrar a premissa e o risco","\"Existe um ponto que a lei ainda não resolveu e ele mexe no seu preço em cerca de 1%. E este benefício do seu produto depende de condição: se não valer, o preço é este outro.\""],
   ["6","8 min","Traduzir em decisão","Sair com ação: revisar preço em degraus, renegociar com fornecedor que não passa crédito, escolher o regime."],
   ["7","5 min","Fechar escopo e valor","Propor o serviço com escopo e prazo. \"Posso te mandar por escrito hoje ainda?\""]])]},
 {t:"6. OBJEÇÕES E RESPOSTAS",c:[grade([2600,4160,2600],["O cliente diz","Responda","Erro a evitar"],[
   ["\"Isso é só em 2033.\"","\"Para alguns produtos seus o efeito já vem em 2027. E reajuste em degraus o seu cliente absorve. De uma vez, ele troca de fornecedor.\"","Concordar que dá para deixar para depois."],
   ["\"Meu concorrente não vai aumentar.\"","\"Talvez ele nem tenha calculado. Se comprar pior que o senhor, vai ter de aumentar mais.\"","Prometer vantagem competitiva."],
   ["\"Não pode me dar um número certo?\"","\"Posso dar o número e a premissa. A CBS ainda depende do Senado e há um ponto da base de cálculo em aberto. Prefiro dizer isso agora.\"","Dar número único para agradar."],
   ["\"Isso não é obrigação do contador?\"","\"Apuração e entrega são. Precificação é decisão de negócio e não está no contrato.\"","Fazer de graça."],
   ["\"Vou esperar a lei ficar clara.\"","\"O que falta definir mexe em 1% a 2% do preço. O resto já dá para calcular. Esperar só encurta o prazo.\"","Concordar em esperar."],
   ["\"Quanto custa?\"","Item 7. Nunca improvisar valor na reunião.","Dar valor de cabeça."]])]},
 {t:"7. COMO PRECIFICAR O SERVIÇO",c:[grade([3000,1100,1300,3960],["Entregável","Horas","Valor","Escopo"],[
   ["Diagnóstico de exposição","2 a 3","","Classificação da faixa, simulação agregada e reunião de apresentação."],
   ["Classificação fiscal dos itens","4 a 8","","Consulta em lote dos NCM e NBS, definição dos casos Conferir e Escolher e registro da decisão."],
   ["Precificação por linha de produto","8 a 16","","Custos, créditos por fornecedor e preço sugerido por item."],
   ["Análise da carteira de fornecedores","4 a 6","","Comparação por custo real e identificação de quem não transfere crédito."],
   ["Estudo de regime (Simples)","3 a 5","","Ponto de virada, simulação nos dois cenários e recomendação."],
   ["Acompanhamento anual da transição","2 por ano","","Revisão do preço a cada mudança de alíquota, de 2027 a 2033."]]),
   nota("Venda por esforço, não por percentual de economia. Preencha a coluna Valor com a hora técnica da Amcont. O reajuste do contrato de honorários pela nova rotina fiscal é conversa separada.")]},
 {t:"8. CHECKLIST ANTES DE CADA REUNIÃO",c:[passos([
   "A faixa de triagem do cliente está definida.",
   "Os principais NCM ou NBS dele foram consultados em lote e os casos Conferir e Escolher já têm resposta.",
   "Os números dele já estão carregados na ferramenta. Nunca preencher na frente dele.",
   "As alíquotas de CBS e IBS foram conferidas contra a norma vigente, em especial a resolução do Senado.",
   "A proposta comercial está pronta para enviar no mesmo dia."],"Conferir")]},
 {t:"9. LIMITES DO QUE PODEMOS AFIRMAR",c:[grade([3300,6060],["Assunto","Postura"],[
   ["Alíquota da CBS","Cálculo do TCU, aguardando o Senado. Apresentar como provisória."],
   ["IBS a partir de 2029","Estimativa de 18,7% no regime pleno. A lei prevê revisão se a soma passar de 26,5%."],
   ["CBS e IBS na base do ICMS e do ISS","Ponto sem lei. O padrão segue os fiscos estaduais. Informar a premissa."],
   ["Benefício por NCM ou NBS","A maioria é condicional. Só contar com a redução depois de confirmar a condição."],
   ["ICMS de Santa Catarina","Só a alíquota interna. Não cobre substituição tributária, TTD nem interestaduais. Benefícios da cesta básica vencem em 31/12/2026."],
   ["Projeção até 2033","Mantém o custo constante. É teto de impacto, não previsão."],
   ["Decisão de preço","É do cliente. Entregamos o cálculo e o cenário."]])]},
 {t:"10. MENSAGENS PRONTAS",c:[labels([
   ["Abertura por WhatsApp (faixas ALTA e MÉDIA)","\"[Nome], tudo bem? Rodei uma simulação do impacto da reforma tributária no preço de venda da [Empresa], com os números da sua escrituração e a tributação dos seus principais produtos. Tem um ponto que vale o senhor ver antes de fechar o preço do próximo ano. Consegue 40 minutos nesta semana?\""],
   ["E-mail depois da reunião (mesmo dia, com a simulação em PDF)","\"[Nome], segue a simulação que vimos hoje. Três pontos para registro: (1) o preço necessário em [ano] para manter a sua margem é de [valor], com a premissa indicada no relatório; (2) a CBS usada é provisória e será revista quando o Senado fixar a alíquota; (3) os produtos marcados como Conferir dependem da condição que combinamos validar. A proposta segue em documento separado.\""],
   ["Comunicado para a faixa BAIXA (envio em massa)","\"[Nome], fizemos uma primeira análise do impacto da reforma tributária na [Empresa]. O seu perfil de compras gera crédito suficiente para que o impacto no preço seja pequeno. Não é necessária nenhuma ação agora. Avisaremos quando a alíquota definitiva for publicada.\""]])]},
 {t:"11. CONTROLE DE REVISÕES",c:[grade([900,1700,4960,1800],["Rev.","Data","Descrição da alteração","Responsável"],[
   ["01 e 02","13 e 16/08/2026","Emissão inicial e inclusão da análise por produto.","A. Constantino"],
   ["03",HOJE,"Números refeitos com a CBS do TCU e com a base de cálculo da LC 214/2025, art. 12. Triagem passa a considerar o PIS e a COFINS atuais (monofásico e alíquota zero). Inclui a classificação fiscal em lote como entregável.","A. Constantino"]])]},
 ]};

/* =================== IT.001 rev. 04 =================== */
const it001={tipo:"INSTRUÇÃO DE TRABALHO",codigo:"IT.001",titulo:"OPERAÇÃO: Diagnóstico de precificação na reforma tributária",rev:"05",data:HOJE,
 secoes:[
 {t:"1. OBJETIVO",c:[labels([["Objetivo","Padronizar o diagnóstico de precificação na reforma tributária, da triagem da carteira à entrega da proposta, garantindo que os cálculos sejam conferidos e que nenhum número saia do escritório sem prova real e sem a premissa informada."]])]},
 {t:"2. RESPONSÁVEL E APLICAÇÃO",c:[labels([["Responsável","Departamento fiscal, com validação do sócio responsável pela conta"],["Periodicidade","Triagem da carteira: anual e sempre que as alíquotas mudarem. Diagnóstico individual: sob demanda"],["Ferramentas","Planilha Amcont de Precificação, calculadora de empresa, calculadora de produto e serviço, Domínio Sistemas como origem dos dados"],["Documentos ligados","MC.001 memória de cálculo, RC.001 roteiro comercial, IT.002 envio ao cliente, MU.001 manual do cliente"],["Prazo legal","Não se aplica. A CBS e o IBS passam a ser cobrados em 01/2027"]])]},
 {t:"3. QUAL FERRAMENTA USAR EM CADA SITUAÇÃO",c:[grade([4160,2600,2600],["Situação","Ferramenta","Aba ou tela"],[
   ["Classificar a carteira inteira","Planilha","TRIAGEM"],
   ["Consultar a tributação de vários NCM ou NBS","Planilha ou calculadora de produto","CLASSIFICACAO ou Consultar tributação por código"],
   ["Achar a NBS e o cClassTrib pelo código do serviço","Planilha ou calculadora de produto","SERVICO ou busca por LC 116"],
   ["Diagnóstico completo de um cliente","Planilha","GASTOS e MOTOR_PRECO_2026"],
   ["Precificar um produto ou serviço específico","Calculadora de produto ou planilha","Tela de simulação ou aba PRODUTO"],
   ["Comparar cotações de compra pelo custo real","Calculadora de produto ou planilha","Modo Compra ou aba COMPRA"],
   ["Mostrar ao cliente a nota fiscal da venda","Calculadora de produto ou planilha","Nota fiscal desta venda ou PRODUTO D56"],
   ["Decidir a opção do Simples","Planilha ou calculadora de produto","SIMPLES ou painel do Simples"],
   ["Projetar até 2033","Planilha","LINHA_TEMPO"],
   ["Simular ao vivo na reunião","Calculadora de empresa ou de produto","Tela única"],
   ["Levar resultado impresso","Planilha ou calculadoras","RESUMO ou Imprimir em PDF"]])]},
 {t:"4. PASSO A PASSO",c:[passos([
   "**Conferir alíquotas.** Na aba PARAMETROS, comparar a CBS e o IBS (A32 a D39) com a norma vigente, em especial a resolução do Senado. Atualizar antes de qualquer cálculo.",
   "**Conferir a premissa.** PARAMETROS B5 deve estar em 2 (LC 214, art. 12). As premissas 1 e 3 servem apenas para medir cenários.",
   "**Triar a carteira.** Na aba TRIAGEM, uma linha por cliente, com faturamento, entradas por faixa de crédito e base de ICMS. Ordenar pela classificação e levar o painel aos sócios.",
   "**Classificar os itens do cliente.** Colar os principais NCM e NBS na aba CLASSIFICACAO. Resolver com o cliente os casos CONFERIR e ESCOLHER e registrar a decisão. Conferir a coluna de PIS e COFINS de hoje e a de ICMS de SC.",
   "**Classificar os serviços pelo código da nota.** Na aba SERVICO, digitar em B4 o item da LC 116 ou o código de tributação nacional (04.01, 0401 ou 040101). A aba lista as NBS que o Anexo VIII admite, cada uma com redução, CST e cClassTrib. Escolher a NBS que descreve o serviço, copiar para PRODUTO B4, informar o item em PRODUTO E10 e manter B17 em servico. F10 confirma se a classificação ficou restrita ao item. Registrar a NBS escolhida e o motivo.",
   "**Lançar os gastos.** Na aba GASTOS, linha a linha, com valor bruto, faixa de redução, percentual de crédito de ICMS e indicação de crédito de PIS e COFINS.",
   "**Apurar.** Na aba MOTOR_PRECO_2026, informar faturamento, regime e a parcela da receita sem PIS e COFINS hoje (B7). Conferir a prova real da linha 61.",
   "**Simples Nacional.** Usar a aba SIMPLES com o anexo, a alíquota efetiva do DAS e as bases creditáveis. Registrar o ponto de virada e a recomendação.",
   "**Analisar produtos.** Na calculadora de produto ou na aba PRODUTO: código, tipo, regime, compra, fornecedor e venda. Conferir o tratamento de PIS e COFINS de hoje, a opção de ICMS e a prova real.",
   "**Ler o risco do benefício.** Quando houver redução de CBS e IBS, anotar o preço com e sem o benefício.",
   "**Projetar.** Anotar o resultado do ano mais sensível do cliente (2027 para monofásico e alíquota zero, 2033 para os demais).",
   "**Fechar o dossiê.** Salvar em PDF o RESUMO ou a tela da calculadora. Guardar o arquivo .json do estudo na pasta do cliente.",
   "**Conduzir a reunião** conforme o RC.001 e enviar a simulação e a proposta no mesmo dia.",
   "**Entregar as calculadoras**, quando contratado, conforme a IT.002."])]},
 {t:"5. PONTOS DE ATENÇÃO",c:[alertas([
   "**Prova real diferente de zero** indica erro de lançamento, não de fórmula. Refaça os lançamentos antes de seguir.",
   "**O código não decide sozinho.** NCM e NBS trazem a regra da lei, mas o benefício depende de condição, adquirente, destinação e operação.",
   "**CBS provisória.** Os 11,2% e 11,3% vêm do TCU e aguardam o Senado. Todo estudo deve registrar a versão dos dados usada.",
   "**PIS e COFINS de hoje mudam o resultado.** Revenda de monofásico, de produto com alíquota zero ou com substituição tributária tem margem atual maior e salto em 2027. Fabricante e importador usam a alíquota concentrada.",
   "**ICMS de SC é referência de alíquota interna.** Para cliente com substituição tributária, TTD ou venda interestadual, informar a alíquota efetiva manualmente.",
   "**Imposto Seletivo** segue a MP 1.399/2026, com efeitos a partir de 02/02/2027 e sujeita a conversão em lei. Veículos e cigarros exigem alíquota informada.",
   "**Nunca alterar fórmula da planilha.** Mudança de regra segue a MC.001 e é refeita na planilha e nas calculadoras ao mesmo tempo.",
   "**Diferença pequena entre a calculadora de empresa e a planilha** (até 0,05%) decorre do rateio do ICMS das entradas. Na dúvida, prevalece a planilha."])]},
 {t:"6. CONTROLE DE REVISÕES",c:[grade([900,1700,4960,1800],["Rev.","Data","Descrição da alteração","Responsável"],[
   ["01 e 02","13 e 16/08/2026","Emissão inicial e inclusão da análise de um produto.","A. Constantino"],
   ["03",HOJE,"Inclui a classificação fiscal em lote, o PIS e a COFINS atuais, o ICMS de SC, a premissa da LC 214, art. 12, e a CBS provisória do TCU.","A. Constantino"],
   ["04 e 05",HOJE,"Classificação de serviços pelo código da nota (aba SERVICO e PRODUTO E10); simulação de compra (aba COMPRA) e nota fiscal da venda.","A. Constantino"]])]},
 ]};

/* =================== MC.001 rev. 05 =================== */
const mc001={tipo:"MEMÓRIA DE CÁLCULO",codigo:"MC.001",titulo:"Precificação na reforma tributária",rev:"06",data:HOJE,
 secoes:[
 {t:"1. OBJETIVO E ALCANCE",c:[labels([["Objetivo","Registrar as fórmulas, as premissas, as fontes e os testes das ferramentas de precificação da Amcont, para que qualquer número entregue ao cliente possa ser refeito e defendido."],
   ["Ferramentas cobertas","Planilha Amcont_Precificacao_Reforma_Tributaria.xlsx; calculadora de empresa (versão interna e versão do cliente); calculadora de produto e serviço."],
   ["Versão dos dados","Parâmetros 2026.2 e base fiscal 2026.7, de 10/11/2026."]])]},
 {t:"2. PARÂMETROS E FONTES",c:[grade([2700,2400,4260],["Parâmetro","Valor","Fonte e situação"],[
   ["CBS em 2027 e 2028","11,2%","Cálculo do TCU de 11,3% (Acórdão 2933/2026) menos 0,1 ponto (LC 214/2025, art. 347). Aguarda resolução do Senado."],
   ["CBS de 2029 em diante","11,3%","Mesmo cálculo. Provisória."],
   ["IBS em 2027 e 2028","0,1%","LC 214/2025, art. 344: 0,05% estadual e 0,05% municipal."],
   ["IBS de 2029 a 2033","1,87% a 18,7%","Estimativa: 10%, 20%, 30% e 40% da alíquota plena estimada de 18,7%."],
   ["ICMS e ISS de 2029 a 2032","90%, 80%, 70% e 60%","ADCT, art. 128; LC 87/1996, art. 31-A. Extintos em 2033."],
   ["Reduções de alíquota","30%, 40%, 50%, 60%, 70% e zero","LC 214/2025, arts. 125 a 157, 261, 275, 281 e 286, por NCM, NBS ou atividade."],
   ["Imposto Seletivo","Por NCM","MP 1.399/2026, Anexos IV e V; efeitos a partir de 02/02/2027; sujeita a conversão."],
   ["PIS e COFINS atuais","0,65% e 3%; 1,65% e 7,6%","Leis 9.718/1998, 10.637/2002 e 10.833/2003. Tratamento por NCM pelas Tabelas 4.3.10 a 4.3.13 da EFD-Contribuições."],
   ["Presunção de IRPJ e CSLL","Por atividade","Lei 9.249/1995, arts. 15 e 20. Acréscimo de 10% acima de R$ 5 milhões por ano (LC 224/2025, fonte secundária)."],
   ["Repartição do DAS","Por anexo e ano","Novos anexos da LC 123/2006 (LC 214/2025, art. 519)."],
   ["ICMS de Santa Catarina","17%, 12%, 25% e benefícios","Lei 10.297/1996, art. 19 e Anexo I; RICMS/SC, Anexo 2."]])]},
 {t:"3. BASES DE CÁLCULO ADOTADAS",c:[grade([2700,6660],["Tributo","Base, sendo NF o total da nota"],[
   ["CBS e IBS","NF menos ICMS ou ISS, menos a própria CBS e o IBS. O Imposto Seletivo integra a base. LC 214/2025, art. 12, § 2º, I e V."],
   ["Imposto Seletivo","NF menos ICMS, CBS, IBS e o próprio IS. LC 214/2025, art. 417, I e § 4º."],
   ["ICMS e ISS","NF total, incluindo CBS, IBS e IS. É a posição dos fiscos estaduais; o tema não tem lei e há tese contrária (premissa 3)."],
   ["PIS e COFINS (2026)","NF menos ICMS. Nos serviços, NF cheia."],
   ["IRPJ e CSLL presumidos","NF menos CBS, IBS e IS, multiplicada pela presunção."]]),
   nota("Premissas disponíveis na planilha e na calculadora de empresa: 1, modelo do curso de referência, com CBS e IBS dentro da própria base (não é o texto da lei); 2, padrão, descrita acima; 3, CBS e IBS fora também da base do ICMS e do ISS (PLP 16/2025).")]},
 {t:"4. FÓRMULAS DA CALCULADORA DE PRODUTO E DA ABA PRODUTO",c:[grade([2700,6660],["Grandeza","Fórmula"],[
   ["Alíquotas do ano","i = ICMS ou ISS × fator do ano; c = CBS × (1 − redução); b = IBS × (1 − redução); s = Imposto Seletivo; r = carga de IRPJ e CSLL sobre a receita"],
   ["Peso de CBS e IBS","k = (1 − i) × (c + b) ÷ (1 + c + b)"],
   ["Peso do Imposto Seletivo","σ = s × (1 − i − k) ÷ (1 + s)"],
   ["Preço necessário","NF = (MC + Compra − Créditos) ÷ [1 − i − k − σ − r × (1 − k − σ)], em que MC é a margem de contribuição de hoje"],
   ["Crédito de CBS e IBS, fornecedor do regime regular","Compra × (1 − ICMS da compra × fator) × a ÷ (1 + a), com a = (CBS + IBS) × (1 − redução)"],
   ["Crédito de CBS e IBS, fornecedor do Simples","Compra × DAS do fornecedor × parcela de CBS e IBS do anexo no ano. LC 214/2025, art. 47, § 9º, II"],
   ["Crédito de ICMS","Regime regular: Compra × ICMS × fator. Simples, tradicional ou optante do regime regular de CBS e IBS: Compra × DAS × parcela de ICMS do anexo (só anexos I e II) × fator. MEI e pessoa física: zero. Em serviço: zero"],
   ["Margem de hoje, Lucro Presumido e Real","Venda − Compra − [ICMS ou ISS + PIS + COFINS + IRPJ e CSLL − crédito de ICMS − crédito de PIS e COFINS]"],
   ["PIS e COFINS de hoje","Normal: alíquota do regime. Monofásico, alíquota zero, substituição tributária ou isento: zero, sem crédito na compra. Fabricante ou importador de monofásico: alíquota concentrada do produto"],
   ["Crédito de PIS e COFINS (Lucro Real)","Compra × (1 − ICMS da compra) × 9,25%, salvo compra de pessoa física ou produto sem tributação normal"],
   ["Simples, hoje","DAS = Venda × alíquota efetiva × (1 − parcelas de PIS e COFINS, se monofásico)"],
   ["Simples tradicional, no ano","NF = (MC + Compra) ÷ (1 − alíquota efetiva)"],
   ["Nota fiscal da venda","Valor do produto = NF − CBS − IBS; base do ICMS ou ISS = NF; base da CBS e do IBS = NF − ICMS ou ISS − CBS − IBS; total = valor do produto + CBS + IBS"],
   ["Compra: custo real","Custo real = NF da compra − crédito de CBS e IBS − crédito de ICMS − crédito de PIS e COFINS (2026, Lucro Real, revenda ou insumo)"],
   ["Compra: regras do comprador","Simples no DAS: nenhum crédito (LC 214/2025, art. 47, § 9º, I). Simples no regime regular: só CBS e IBS. Uso e consumo: sem ICMS até 2032 (LC 87/1996, art. 33, I). Imobilizado: ICMS total, recuperado em 48 meses"],
   ["Compra: preço máximo para empatar","Menor custo real ÷ (1 − crédito da cotação ÷ NF da cotação)"],
   ["Simples optante do regime regular","Preço sem CBS e IBS = (MC + Compra − crédito de CBS e IBS) ÷ (1 − Th); CBS e IBS = Preço × Kb × alíquota, por fora; Th e Kb conforme a repartição do anexo no ano"]])]},
 {t:"5. FÓRMULAS DA CALCULADORA DE EMPRESA E DAS ABAS DE MOTOR",c:[grade([2700,6660],["Motor","Regra"],[
   ["Motor A, preço a partir do custo","P0 = Custo ÷ (1 − despesas − lucro). Premissa 2: NF = P0 ÷ [1 − i − (c + b)(1 − i) ÷ (1 + c + b)]. O custo é informado líquido de tributos recuperáveis e mantido constante: é teto de impacto."],
   ["Motor B, reajuste que preserva a receita líquida","Apura a receita líquida de hoje (débitos menos créditos de PIS, COFINS, ICMS, IPI, IRPJ e CSLL) e encontra a NF do ano que entrega a mesma receita líquida. O adicional de IRPJ é resolvido por duas hipóteses em forma fechada."],
   ["Créditos de CBS e IBS das entradas","Por faixa de redução, com a base sem o ICMS destacado. Na planilha, linha a linha; na calculadora, por rateio do ICMS sobre os gastos creditáveis."],
   ["Crédito de ICMS no ano","Crédito de hoje × fator do ano."],
   ["Receita sem PIS e COFINS hoje","Percentual informado reduz o débito e a base de crédito de PIS e COFINS do cenário atual."],
   ["Venda isenta ou imune","Zera o débito e anula o crédito de CBS e IBS das entradas (LC 214/2025, art. 51). Alíquota zero mantém o crédito (art. 52)."],
   ["Simples","Compara o DAS tradicional com o DAS reduzido mais CBS e IBS por fora, líquidos de créditos, e calcula a base de compras de equilíbrio."]])]},
 {t:"6. BASE FISCAL",c:[grade([3000,1500,4860],["Tabela","Registros","Origem"],[
   ["NCM vigentes","10.518","Tabela oficial de 07/10/2026 (via Mapa de Classificação), conferida com a Tabela IBPTax 26.2.C."],
   ["NCM com benefício de CBS e IBS","1.888","Mapa de Classificação 1.0, de 14/10/2026: LC 214/2025 com LC 227 e LC 235/2026."],
   ["NBS","1.238","732 da lei e do Anexo VIII (item da LC 116, indOp e cClassTrib) e 506 da Tabela IBPTax."],
   ["Item da LC 116 com NBS","208 itens e 980 pares","Anexo VIII da NFS-e Nacional, v1.01.00. Classificação própria por par; em 95 pares difere da geral da NBS. Cinco itens sem NBS."],
   ["cClassTrib","155","Tabela de 23/01/2026; os códigos das regras seguem a IT 2025.002 v1.70."],
   ["PIS e COFINS atuais por NCM","752 monofásicos ou com substituição e 739 com alíquota zero","Tabelas 4.3.10, 4.3.11 (v1.35), 4.3.12 e 4.3.13 (v1.37, de 14/10/2026) da EFD-Contribuições. Autopeças: lista de repositório público."],
   ["ICMS de SC","Regras por prefixo de NCM","Lei 10.297/1996 e RICMS/SC, consulta em 10/11/2026."],
   ["Imposto Seletivo","20 regras","MP 1.399/2026, aplicadas aos NCM do Anexo XVII da LC 214/2025."]])]},
 {t:"7. TESTES REALIZADOS EM 10/11/2026",c:[grade([4200,1500,3660],["Teste","Resultado","Observação"],[
   ["Planilha contra calculadora de produto","23 de 23","Produto e serviço, três regimes, 2026 a 2033, fornecedores, monofásico, alíquota zero e fabricante."],
   ["Prova pela definição legal das bases","4 de 4","Cada tributo dividido pela sua base devolve a alíquota da lei."],
   ["Prova real da margem de contribuição","Zero","Margem no ano igual à de hoje em todos os cenários."],
   ["Planilha contra calculadora de empresa","Diferença de 0,03%","Em 2027 e 2029, pelo rateio do ICMS das entradas. Zero em 2033."],
   ["Base de NCM contra a planilha de origem","1.888 de 1.888","Redução, CST e cClassTrib idênticos."],
   ["Busca pelo código do serviço, planilha contra calculadora","21 de 21","Redução e cClassTrib iguais nas duas ferramentas."],
   ["Compra, aba COMPRA contra modo Compra","440 de 440","11 cenários, 8 cotações, cinco créditos e custo real; quatro regimes do comprador e três destinações."],
   ["Nota fiscal da venda","Prova zero","Total da nota igual ao preço necessário em produto, serviço, Simples e 2026."],
   ["Motor de referência contra o material do curso","55 de 66","Os 11 pontos diferentes são correções deliberadas (adicional de IRPJ e Lucro Real). O motor em Python não foi atualizado para a premissa 2 nem para a CBS nova."]])]},
 {t:"8. LIMITES CONHECIDOS",c:[alertas([
   "**CBS e IBS de referência não são definitivos.** A CBS aguarda o Senado e o IBS pleno é estimativa.",
   "**IS na base do ICMS e a LC 224/2025** foram adotados com base em fonte secundária, sem leitura do texto oficial.",
   "**Crédito de ICMS de fornecedor do Simples** (LC 123/2006, art. 23) foi confirmado em fonte secundária e só existe para mercadoria de revenda ou industrialização, condição que a ferramenta não testa.",
   "**IPI nos anos futuros** é mantido como hoje nos motores de empresa. A reforma o reduz a zero para a maioria dos produtos.",
   "**Regimes específicos** (imóveis, bares, hotelaria, turismo, combustíveis, serviços financeiros) são aproximados pela redução de alíquota.",
   "**ICMS de SC** não cobre substituição tributária, TTD, crédito presumido nem operações interestaduais. A isenção de ICMS exige estorno de crédito, que a calculadora não faz sozinha.",
   "**Correlação do Anexo VIII.** Traz só os cClassTrib admitidos por item da LC 116 e NBS. Tratamento que depende do prestador ou do tomador pode não aparecer (exemplo: transporte coletivo urbano, item 16.02). Desdobramentos do código nacional não são validados.",
   "**Compra.** Crédito presumido de produtor rural, crédito de PIS e COFINS do imobilizado e o parcelamento do ICMS do imobilizado em 48 meses não são calculados.",
   "**Benefícios condicionais.** A ferramenta aplica a redução e mostra o preço sem ela; a confirmação da condição é do contador.",
   "**Fabricante substituto, combustíveis por unidade e as duas alíquotas de bebidas frias e de autopeças** não são simulados automaticamente."])]},
 {t:"9. COMO ALTERAR UMA REGRA",c:[passos([
   "Registrar a norma, o dispositivo e a data da consulta.",
   "Alterar os scripts da pasta geradores_base_fiscal (base, calculadoras e planilha) e gerar os arquivos de novo. Nunca editar fórmula direto na planilha ou no HTML.",
   "Recalcular a planilha e rodar o cruzamento com a calculadora de produto. Só liberar com todos os cenários iguais e prova real zerada.",
   "Atualizar a versão dos dados, esta memória de cálculo e os manuais, e reenviar o pacote aos clientes conforme a IT.002."])]},
 {t:"10. CONTROLE DE REVISÕES",c:[grade([900,1700,4960,1800],["Rev.","Data","Descrição da alteração","Responsável"],[
   ["01 a 04","13/08 a 10/11/2026","Emissão inicial, presunções, adicional de IRPJ e motor de produto. Na 04, reescrita: bases de cálculo conforme a LC 214/2025, arts. 12 e 417; CBS do TCU; crédito sem ICMS na base; crédito do Simples limitado ao DAS; PIS e COFINS atuais por NCM; ICMS de SC; base fiscal de NCM, NBS e cClassTrib; testes refeitos.","A. Constantino"],
   ["05 e 06",HOJE,"Busca pelo código do serviço (aba SERVICO e PRODUTO E10); simulação de compra; nota fiscal da venda; crédito de ICMS de fornecedor do Simples optante do regime regular limitado ao DAS.","A. Constantino"]])]},
 ]};
(async()=>{ await montar(it002,"IT002-EnvioSuporteCalculadoras-Amcont.docx"); await montar(mu001,"MU001-ManualCliente-Calculadoras-Amcont.docx"); await montar(rc001,"RC001-RoteiroComercial-ReformaTributaria-Amcont.docx"); await montar(it001,"IT001-DiagnosticoPrecificacao-Amcont.docx"); await montar(mc001,"MC001-MemoriaCalculo-Precificacao-Amcont.docx"); console.log("OK"); })();
