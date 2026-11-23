const { chromium } = require('playwright'); const fs=require('fs');
const SP='/tmp/claude-0/-home-claude/ad0e41b0-2ebc-575a-9ba1-f64b3d834613/scratchpad/';
const X=JSON.parse(fs.readFileSync(SP+'cross_compra.json'));
(async()=>{ const b=await chromium.launch(); const p=await b.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
 await p.goto('file:///home/claude/work/amcont-produto.html'); await p.fill('#senha','amcont2027'); await p.keyboard.press('Enter'); await p.waitForTimeout(400);
 let ok=0, n=0, bad=[];
 for (let s=0;s<X.sc.length;s++){
   const [tp,cod,reg,ano,dest,trat,isc,dup]=X.sc[s];
   const out = await p.evaluate(([tp,cod,reg,ano,dest,trat,rows,isc,dup])=>{
     definirModo("compra"); definirTipo(tp, true);
     selecionarCodigo(cod.replace(/\D/g,""));
     if (trat !== "auto") { $("#trat").value = {integral:"0",red30:"0.3",red60:"0.6",red70:"0.7",sem:"1"}[trat]; }
     $("#regime").value = reg.startsWith("simples") ? "simples" : reg; $("#sn-opcao").value = reg === "simples_regular" ? "regular" : "das";
     $("#destino").value = dest === "imobilizado" ? "imob" : dest; $("#pc-hoje").value = "auto"; $("#icms-venda").value = isc*100; $("#difal-dupla").checked = dup === "S"; $("#uf-dest").value = "SC";
     ANO = ano; sincronizar();
     escreverCot(rows.map(r=>({nome:r[0], reg:r[1], preco:r[2], icms:r[3]*100, das:(r[4]||0)*100, anexo:r[5]||"I", fora:r[6]==="S"})));
     calcular(); const o = opcoes();
     return {trat:o.trat, pcReg:o.pcReg, rows:lerCot().map(c=>{ const k=creditoComprador(c,o); return [k.cbsIbs,k.icms,k.pc,k.total,k.custo,k.difal]; })};
   }, [tp,cod,reg,ano,dest,trat,X.rows,isc,dup]);
   const R=X.res[s];
   let lin=true;
   if (Math.abs(out.trat-(R.red||0))>1e-9){ lin=false; bad.push([s,'red',out.trat,R.red]); }
   out.rows.forEach((h,k)=>{ const x=R.rows[k]; [[0,0],[1,1],[2,2],[3,3],[4,4],[5,10]].forEach(([j,jx])=>{ n++; if (Math.abs(h[j]-(x[jx]||0))<1e-6) ok++; else { lin=false; bad.push([s,k,j,h[j],x[jx]]); } }); });
   console.log(lin?'OK ':'ERRO', X.sc[s].join(' '), '| pc', out.pcReg, R.pc, '| custos', out.rows.map(r=>r[4].toFixed(2)).join(' '));
 }
 console.log(ok+'/'+n, bad.slice(0,10), errs); await b.close(); })();
