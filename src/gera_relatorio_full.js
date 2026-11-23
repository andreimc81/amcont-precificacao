const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign, ImageRun, TableLayoutType, Header, Footer, PageNumber } = require('docx');
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
const rodape=(data,pend)=>tbl([2340,2340,2340,2340],[
  row([cell(2340,PETROLEO_L,[par([txt("Elaborado por:",{bold:true,size:18,color:PETROLEO})])],{bc:PETROLEO_M}),cell(2340,BRANCO,[par([txt("Andrei Constantino",{size:18})])],{bc:PETROLEO_M}),
       cell(2340,PETROLEO_L,[par([txt("Aprovado por:",{bold:true,size:18,color:PETROLEO})])],{bc:PETROLEO_M}),cell(2340,BRANCO,[par([txt(pend?"Pendente":"Andrei Constantino",{size:18,bold:!!pend,color:pend?"B00020":PRETO})])],{bc:PETROLEO_M})]),
  row([cell(2340,PETROLEO_L,[par([txt("Data de emissão:",{bold:true,size:18,color:PETROLEO})])],{bc:PETROLEO_M}),cell(2340,BRANCO,[par([txt(data,{size:18})])],{bc:PETROLEO_M}),
       cell(2340,PETROLEO_L,[par([txt("Data de aprovação:",{bold:true,size:18,color:PETROLEO})])],{bc:PETROLEO_M}),cell(2340,BRANCO,[par([txt(pend?"Pendente":data,{size:18,bold:!!pend,color:pend?"B00020":PRETO})])],{bc:PETROLEO_M})])]);
const nota=t=>par(rich(t,{size:16,italic:true,color:"555555"}),{before:80});

function montar(spec,saida){
  const kids=[];
  spec.secoes.forEach(s=>{ kids.push(secTitle(s.t)); (s.c||[]).forEach(x=>kids.push(x)); kids.push(par("")); });
  kids.push(rodape(spec.data,spec.pendente));
  if (spec.assinatura) kids.push(nota(spec.assinatura));
  const doc=new Document({ styles:{default:{document:{run:{font:"Arial",size:20,language:{value:"pt-BR"}}}}},
    sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:1000,right:1273,bottom:900,left:1273,header:500}}},
      headers:{default:new Header({children:[makeHeader(spec.tipo,spec.codigo,spec.titulo,spec.rev),par("")]})},
      footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[
        new TextRun({text:spec.codigo+" rev. "+spec.rev+"  |  Ferramentas de precificação Amcont, versão "+VERS.v+" de "+VERS.br+"  |  Página ",font:"Arial",size:14,color:"555555"}),
        new TextRun({children:[PageNumber.CURRENT],font:"Arial",size:14,color:"555555"}),
        new TextRun({text:" de ",font:"Arial",size:14,color:"555555"}),
        new TextRun({children:[PageNumber.TOTAL_PAGES],font:"Arial",size:14,color:"555555"})]})]})},
      children:kids}]});
  return Packer.toBuffer(doc).then(b=>fs.writeFileSync(saida,b));
}
const VERS=(()=>{const v=JSON.parse(require('fs').readFileSync(__dirname+'/../monitor/versao.json','utf8')); const d=new Date(v.data); return {v:v.base+'.'+v.seq, br:v.data.slice(8,10)+'/'+v.data.slice(5,7)+'/'+v.data.slice(0,4)+' '+v.data.slice(11,16)};})();
const HOJE="10/11/2026";

const T=JSON.parse(fs.readFileSync('relatorio_testes.json','utf8'));
const rt={tipo:"RELATÓRIO TÉCNICO",codigo:"RT.001",titulo:"Integração da auditoria independente ao precificador",rev:"04",data:HOJE,
secoes:[
{t:"1. RESUMO EXECUTIVO",c:[labels([
 ["Conclusão","A auditoria externa não encontrou erro de cálculo no motor, mas apontou três problemas reais que confirmamos: crédito apresentado como certo quando é estimativa (art. 47), 163 classificações com cClassTrib composto e falta de rótulo de projeção nas alíquotas futuras. A conferência dos apontamentos revelou um quarto erro, que a auditoria não viu: crédito de PIS e COFINS superestimado na compra de Simples com ICMS fora do DAS."],
 ["Correções","13 alterações pontuais (10 da auditoria e 3 da conferência com os arquivos oficiais salvos pela Amcont), todas no registro de alterações, sem reconstruir HTML nem planilha. Versão anterior arquivada em historico/v2026.7-pre-auditoria-externa."],
 ["Testes","Verificação independente aprovada em "+T.ind+". Planilha contra calculadora: "+T.cruz+". Testes de tela: "+T.tela+"."],
 ["Pendências","CBS do Senado ainda não publicada; alíquotas internas de ICMS dos outros estados vindas de fonte secundária; ICMS-ST, TTD e FCP por produto fora do escopo; monitor semanal ainda não ativado."],
 ["Aptidão","**Correções aprovadas pela Amcont em 10/11/2026; aplicativo não homologado integralmente.** Liberado para uso interno e para piloto controlado com um cliente, como simulação. Não apto para distribuição geral (seção 8)."]])]},
{t:"2. O QUE FOI APROVEITADO DA AUDITORIA",c:[grade([3000,6360],["Material","Uso no projeto"],[
 ["RELATORIO_TECNICO.md (F01 a F10)","Cada apontamento foi confrontado com o código, as fórmulas e a lei consolidada (seção 3)."],
 ["AMCONT_Auditoria_Motores (3.305 casos)","Amostras usadas para localizar os 163 cClassTrib compostos e o erro do crédito de PIS e COFINS. Zero erro de execução não foi tomado como prova de correção: os resultados foram refeitos por cálculo independente."],
 ["estrutura_xlsx.json (20 abas, 7.933 fórmulas)","Conferência de integridade. Após as correções, 7.941 fórmulas e zero erro de recálculo; a diferença são as fórmulas novas desta revisão."],
 ["monitor_fontes_oficiais.py","Incorporado como segunda camada do monitor (monitor_fontes.py), com hash do texto e não do HTML, para não gerar alerta falso a cada mudança de layout."],
 ["README_IMPLEMENTACAO.md","Procedimento de homologação adotado: nenhuma regra muda sem registro, testes e aprovação."]])]},
{t:"3. APONTAMENTOS CONFRONTADOS",c:[grade([700,2000,1500,5160],["Ref.","Tema","Classificação","Decisão e fundamento"],[
 ["F01","Crédito de CBS e IBS","**Incompleta**","Confirmado. A lei exige documento idôneo e extinção do débito (LC 214/2025, art. 47, caput, § 1º, II, e § 2º, I). Corrigido: crédito rotulado como estimado, custo sem crédito e cenário prudente."],
 ["F02","163 cClassTrib compostos","**Incorreta**","Confirmado. O campo da nota aceita um código de 6 dígitos. Corrigido: código principal no campo, alternativas como condição a confirmar."],
 ["F03","Anexo VIII v1.02.00","**Depende de dado externo**","Confirmado. Na rev. 03, a base passou para a v1.02.00 (R14-01): 35 pares mudaram, nenhum da saúde (item 04)."],
 ["F04","Alíquotas provisórias","**Incompleta**","Confirmado como falha de apresentação. Rótulo de projeção e sensibilidade de +1 ponto no HTML. A planilha ainda não tem a sensibilidade."],
 ["F05","ICMS-ST, TTD, FCP por produto","**Depende da operação**","Não é erro: limite de escopo já declarado. Exige dados de cada operação; fica como limitação."],
 ["F06","Cesta básica de SC após 31/12/2026","**Incompleta**","Confirmado. Aviso de benefício vencido e botão para alíquota cheia. Prazo a reconfirmar no RICMS/SC."],
 ["F07","PIS e COFINS: monofásico, zero, combustíveis","**Correta, com um erro achado**","Monofásico e alíquota zero corretos (tabelas 4.3.10 a 4.3.13 da EFD). Na conferência, achamos o crédito do Simples com ICMS fora do DAS calculado sem excluir o ICMS (Lei 14.592/2023). Corrigido. Lista de autopeças conferida com a Lei 10.485/2002 na rev. 02: 20 NCM saíram e 2 entraram (R13-01)."],
 ["F08","Senha e monitor inativo","**Parcialmente procedente**","Senha é barreira de conveniência, sem solução em arquivo HTML. Incluído bloqueio visual após 90 dias sem conferência. Monitor depende de ativação."],
 ["F09","Alíquotas do IS","**Incompleta**","Estrutura confirmada (TIPI × fator, MP 1.399/2026, art. 3º). Na rev. 02, as 20 regras foram conferidas com o texto oficial (Anexos IV e V): todas iguais; corrigida a embarcação sem motor 8903.12 (R13-02)."],
 ["F10","Margem de contribuição × lucro","**Correta**","Método certo; incluída nota de escopo para evitar leitura como lucro líquido."]])]},
{t:"4. AS OITO FRENTES PEDIDAS",c:[grade([3200,1600,4560],["Frente","Situação","Evidência"],[
 ["1. cClassTrib composto","Corrigida","163 de 4.019 antes; 0 depois (antes_depois.js)."],
 ["2. Apropriação de CBS e IBS","Corrigida","Estimado separado do apropriável; teto do Simples (art. 47, § 9º, II) mantido e retestado."],
 ["3. PIS e COFINS, monofásico, zero","Corrigida em um ponto","Sublimite: R$ 9,25 antes e R$ 8,14 depois, em nota de R$ 100 com ICMS de 12%, igual ao fornecedor regular."],
 ["4. ICMS, ST, DIFAL e benefícios","Correta no escopo; ST fora","Interestadual e DIFAL: 7 de 7 e 672 de 672. ST, TTD e FCP por produto não modelados."],
 ["5. Correlações NCM, NBS, CST, cClassTrib, cCredPres, LC 116","Correta, com pendência","Base conferida contra a lei consolidada (17 anexos). cCredPres não é usado: crédito presumido não é calculado."],
 ["6. Tabelas da NF-e e NFS-e","Atualizada","Anexo VIII v1.02.00 incorporado (R14-01). Tabela de cClassTrib da NF-e: a base usa a IT 2025.002 v1.70; versão mais nova não confirmada."],
 ["7. Transição 2026 a 2033","Correta, rotulada","Valores da lei e estimativas, agora identificados como projeção."],
 ["8. Consistência matemática","Aprovada","Verificação independente e cruzamento planilha contra calculadora (seção 6)."]])]},
{t:"5. CORREÇÕES IMPLEMENTADAS",c:[grade([1100,2300,2980,2980],["Registro","Regra afetada","Antes","Depois"],[
 ["R12-01","Crédito na compra e na venda","Só custo com crédito","Custo com e sem crédito; cenário prudente; preço do ano sem crédito"],
 ["R12-02","cClassTrib","163 campos com vários códigos","0; alternativas como condição"],
 ["R12-03","Crédito de PIS e COFINS, sublimite","R$ 9,25 em R$ 100","R$ 8,14 em R$ 100"],
 ["R12-04","Anexo VIII","Sem aviso","Aviso da v1.02.00 (base inalterada)"],
 ["R12-05","Painel do ano","Sem rótulo","Projeção e +1 ponto"],
 ["R12-06","ICMS cesta básica de SC","Selecionável sem aviso após 2026","Aviso e botão de alíquota cheia"],
 ["R12-07","Validade da versão","Aviso em 45 dias","Aviso em 45 e bloqueio visual em 90"],
 ["R12-08","Imposto Seletivo","Sem fonte","Nota da MP 1.399/2026"],
 ["R12-09","Margem","Sem nota","Nota de escopo"],
 ["R12-10","IS exibido na planilha em 2026","2,6% ou 20% exibidos como aplicados","Zero antes de 2027, igual à calculadora; preço inalterado"],
 ["R13-01","Autopeças (PIS e COFINS monofásico)","Bomba 8413.11: preço 2027 R$ 1.039,65 (lista com 20 NCM indevidos)","R$ 997,85; lista igual aos Anexos I e II da Lei 10.485/2002"],
 ["R14-01","Anexo VIII da NFS-e","v1.01.00: 980 pares","v1.02.00: 997 pares; 35 reclassificados (29.01 e 17.09 perdem redução; 30.01 e 25.03 ganham opção)"],
 ["R13-02","IS de embarcações","Inflável sem motor 8903.12: R$ 1.076,14 com IS de 7,8%","R$ 997,85 sem IS; notas citam o texto oficial e a projeção de 2028"]]),
 nota("Detalhe completo (norma, dispositivo, vigência, códigos, problema, testes e situação) no Registro de alterações da base fiscal, pasta do monitor no Google Drive.")]},
{t:"6. TESTES",c:[grade([4300,1500,3560],["Teste","Resultado","Observação"],T.linhas),
 nota("Ausência de erro de execução não foi tratada como prova de correção tributária. A verificação independente recalcula cada caso com código próprio, a partir das bases legais, sem usar as funções da calculadora.")]},
{t:"7. LIMITAÇÕES QUE PERMANECEM",c:[alertas([
 "**Alíquotas de referência.** CBS de 2027 aguarda resolução do Senado (prevista até 15/12/2026); IBS pleno de 18,7% é estimativa.",
 "**Anexo VIII v1.02.00** é preliminar e sem regras de negócio: pode mudar de novo. O monitor de fontes acompanha a página.",
 "**Alíquotas internas de ICMS dos outros estados** (venda interestadual e DIFAL) vêm de fonte secundária, como vinha a lista de autopeças: conferir antes de liberar a venda para outro estado.",
 "**ICMS-ST, TTD, FCP e alíquotas por produto em outros estados** não são calculados.",
 "**Imposto Seletivo**: alíquotas da MP 1.399/2026, ainda sujeita à conversão em lei; de 2028 em diante, projeção. Automóveis e comerciais leves exigem a alíquota do modelo.",
 "**Exceções (Ex) da TIPI** em autopeças e IS (molas 7320.10.00, cigarrilhas, vinhos do Porto) dependem do produto: a ferramenta avisa, não decide.",
 "**Planilha sem a sensibilidade de +1 ponto** que o HTML já mostra.",
 "**Exclusão do ICMS do crédito de PIS e COFINS** segue a Lei 14.592/2023, ainda discutida no Judiciário.",
 "**Monitor** criado e testado, mas a tarefa semanal e o fluxo do n8n ainda não estão ativos.",
 "**Senha** do arquivo não protege dados; não colocar informação de cliente nos HTML."])]},
{t:"8. APTIDÃO AO COMPARTILHAMENTO",c:[labels([
 ["Parecer técnico","O aplicativo **não está integralmente homologado**. Os cálculos conferidos estão consistentes, mas há regras dependentes de norma ainda não publicada e tabelas não confrontadas."],
 ["Uso interno","Apto, como ferramenta de simulação, com o selo de projeção."],
 ["Piloto com um cliente","Apto: correções aprovadas em 10/11/2026. Entregar com a ressalva escrita de que os valores de 2027 em diante são projeção."],
 ["Distribuição geral","Não apto. Condições: CBS do Senado incorporada, Anexo VIII v1.02.00 confrontado, monitor ativo por pelo menos uma semana e resultado do piloto avaliado."]])]},
{t:"9. PLANO DE AÇÃO PRIORIZADO",c:[passos([
 "**Concluído em 10/11/2026:** linhas R08-01 a R14-01 aprovadas no registro de alterações.",
 "**Ativar o monitor**: autorizar a tarefa semanal e importar o fluxo do n8n; rodar o monitor_fontes.py no computador do escritório uma vez para formar a linha de base.",
 "**Conferir as alíquotas internas de ICMS por estado** com a legislação de cada UF.",
 "**Escolher o cliente piloto** e entregar a versão candidata com a ressalva de projeção.",
 "**Atualizar a CBS** quando sair a resolução do Senado e repetir a bateria de testes.",
 "**Acompanhar a conversão da MP 1.399/2026** e repetir a conferência do IS se o texto mudar."])]},
{t:"10. CONTROLE DE REVISÕES",c:[grade([900,1700,4960,1800],["Rev.","Data","Descrição da alteração","Responsável"],[["01",HOJE,"Emissão: integração da auditoria independente de 10/11/2026.","A. Constantino"],["02",HOJE,"Conferência com os arquivos oficiais salvos pela Amcont: LC 214 consolidada sem mudança; Lei 10.485/2002 (R13-01); MP 1.399/2026 (R13-02).","A. Constantino"],["03",HOJE,"Anexo VIII da NFS-e atualizado para a v1.02.00 (R14-01).","A. Constantino"],["04",HOJE,"Aprovação da Amcont das linhas R08-01 a R14-01 e liberação da versão 2026.8 para uso interno e piloto.","A. Constantino"]])]}
]};
montar(rt,"RT001-IntegracaoAuditoria-Precificador-Amcont.docx").then(()=>console.log("RT OK"));
