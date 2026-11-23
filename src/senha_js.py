# Trecho comum: senha propria por navegador (localStorage), com redefinicao pela senha original.
SENHA_JS = r'''
/* ---------- senha propria neste navegador ---------- */
const K_SENHA = "amcont_senha_propria";
let REDEFINIR = false;
function hashProprio(){ try { return localStorage.getItem(K_SENHA) || ""; } catch(e){ return ""; } }
async function senhaConfere(h, padrao){
  const p = hashProprio();
  if (p && REDEFINIR && h === padrao){ try { localStorage.removeItem(K_SENHA); } catch(e){} REDEFINIR = false; return true; }
  return p ? h === p : h === padrao;
}
(function(){
  if (!hashProprio()) return;
  const card = document.querySelector(".gate-card"); if (!card) return;
  const a = document.createElement("button"); a.type = "button"; a.id = "b-esqueci";
  a.textContent = "Esqueci minha senha";
  a.style.cssText = "background:none;border:0;color:#8FB0B7;text-decoration:underline;font:400 13px inherit;padding:0;margin-top:14px;cursor:pointer;text-transform:none;letter-spacing:0";
  a.addEventListener("click", ()=>{ REDEFINIR = true;
    document.getElementById("gate-erro").textContent = "Digite a senha original enviada pela Amcont. Ela remove a senha própria deste computador.";
    document.getElementById("senha").focus(); });
  card.appendChild(a);
})();
function montarTrocaSenha(){
  const barra = document.querySelector(".barra"); if (!barra || document.getElementById("b-senha")) return;
  const b = document.createElement("button"); b.type = "button"; b.className = "btn"; b.id = "b-senha";
  b.textContent = hashProprio() ? "Trocar senha" : "Definir senha própria";
  barra.appendChild(b);
  const f = document.createElement("form"); f.id = "troca-senha"; f.hidden = true;
  f.style.cssText = "margin-top:10px;padding:12px 14px;background:#FCFCFA;border:1px solid #C4CFCE;border-radius:3px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;font-size:13px";
  f.innerHTML = '<span style="flex-basis:100%">A senha própria vale só neste navegador e neste computador. Mínimo de 6 caracteres.</span>'
    + '<input type="password" id="ns1" placeholder="Nova senha" autocomplete="new-password" style="flex:1;min-width:150px;padding:8px 10px;border:1px solid #C4CFCE;border-radius:3px">'
    + '<input type="password" id="ns2" placeholder="Repita a nova senha" autocomplete="new-password" style="flex:1;min-width:150px;padding:8px 10px;border:1px solid #C4CFCE;border-radius:3px">'
    + '<button type="submit" class="btn forte">Gravar</button><button type="button" class="btn" id="ns-cancela">Cancelar</button>';
  const alvo = document.getElementById("aviso"); alvo.parentNode.insertBefore(f, alvo);
  f.style.display = "none";
  const abrir = v => { f.hidden = !v; f.style.display = v ? "flex" : "none"; };
  b.addEventListener("click", ()=>abrir(f.hidden));
  f.querySelector("#ns-cancela").addEventListener("click", ()=>abrir(false));
  f.addEventListener("submit", async e=>{
    e.preventDefault();
    const a = f.querySelector("#ns1").value, c = f.querySelector("#ns2").value;
    if (a.length < 6){ avisar("A senha precisa ter pelo menos 6 caracteres.", "err"); return; }
    if (a !== c){ avisar("As duas senhas não conferem.", "err"); return; }
    try { localStorage.setItem(K_SENHA, await sha256(a)); }
    catch(err){ avisar("Este navegador não permite gravar a senha. Use a senha enviada pela Amcont.", "err"); return; }
    f.reset(); abrir(false); b.textContent = "Trocar senha";
    avisar("Senha própria gravada neste navegador. No próximo acesso, use a nova senha.", "ok");
  });
  if (!hashProprio()) avisar("Primeiro acesso: se quiser, clique em Definir senha própria para trocar a senha neste computador.", "ok");
}
'''
