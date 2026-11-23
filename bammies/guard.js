/* Bammies: assinatura da proposta.
   Não bloqueia nada que a pessoa precise (selecionar, atalhos, leitor de tela).
   Só troca o menu do botão direito por um aviso e assina o que for copiado. */
(function(){
  var WA = 'https://wa.me/5511956299380?text=' + encodeURIComponent('oi thiago, vi a leitura da bammies e quero conversar');
  var SIGN = '\n\nLeitura de UX da Bammies por Thiago Vitamina · thiagovitamina.com/bammies';

  // dentro da moldura (iframe), quem mostra o aviso é a página de fora
  if (window.self !== window.top) {
    document.addEventListener('contextmenu', function(e){
      if (e.target.closest('input,textarea')) return;
      e.preventDefault();
      try { window.top.BammiesGuard && window.top.BammiesGuard.show(); } catch(_){}
    });
    document.addEventListener('dragstart', function(e){ if (e.target.tagName === 'IMG') e.preventDefault(); });
    return;
  }

  var css = document.createElement('style');
  css.textContent =
    '.bg-toast{position:fixed;left:50%;bottom:max(24px,env(safe-area-inset-bottom));z-index:100;width:min(440px,calc(100vw - 32px));transform:translate(-50%,24px);opacity:0;pointer-events:none;'+
    'background:rgba(255,255,255,.72);-webkit-backdrop-filter:blur(18px) saturate(1.6);backdrop-filter:blur(18px) saturate(1.6);border:1px solid rgba(0,0,0,.06);'+
    'padding:24px;display:flex;flex-direction:column;gap:16px;font-family:"Funnel Sans","Helvetica Neue",Arial,sans-serif;color:#000;'+
    'transition:opacity .25s cubic-bezier(.2,.8,.2,1),transform .25s cubic-bezier(.2,.8,.2,1)}'+
    '.bg-toast.on{opacity:1;transform:translate(-50%,0);pointer-events:auto}'+
    '.bg-toast p{margin:0;font-size:16px;line-height:1.5}'+
    '.bg-toast b{display:block;font-family:"Funnel Display","Helvetica Neue",Arial,sans-serif;font-weight:600;font-size:20px;line-height:1.2;letter-spacing:-.01em;margin-bottom:4px}'+
    '.bg-toast .row{display:flex;align-items:center;gap:24px}'+
    '.bg-toast a{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px;border:1.5px solid #551A8B;background:#551A8B;color:#fff;text-decoration:none;font-family:"Funnel Display","Helvetica Neue",Arial,sans-serif;font-weight:600}'+
    '.bg-toast a:focus-visible,.bg-toast button:focus-visible{outline:2px solid #551A8B;outline-offset:3px}'+
    '.bg-toast button{background:none;border:0;padding:8px 0;font:inherit;color:#551A8B;text-decoration:underline;text-underline-offset:.2em;cursor:pointer}'+
    '@media (prefers-reduced-motion:reduce){.bg-toast{transition:none}}';
  document.head.appendChild(css);

  var t = document.createElement('div');
  t.className = 'bg-toast';
  t.setAttribute('role', 'status');
  t.innerHTML =
    '<p><b>Essa proposta foi feita pela Vitamina.</b>Gostou do que viu? Vamos fechar.</p>'+
    '<div class="row"><a href="'+WA+'" target="_blank" rel="noopener">Conversar no WhatsApp <svg width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="square" aria-hidden="true"><path d="M3.5 12.5 12 4M5.5 3.75h6.75v6.75"/></svg></a>'+
    '<button type="button">Fechar aviso</button></div>';
  document.body.appendChild(t);

  var timer;
  function hide(){ t.classList.remove('on'); }
  function show(){
    t.classList.add('on');
    clearTimeout(timer); timer = setTimeout(hide, 8000);
  }
  t.querySelector('button').addEventListener('click', hide);
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape') hide(); });
  window.BammiesGuard = {show: show};

  // botão direito (e toque longo em imagem): aviso no lugar do menu
  document.addEventListener('contextmenu', function(e){
    if (e.target.closest('input,textarea,.bg-toast')) return;
    e.preventDefault();
    show();
  });
  // imagens não saem arrastando
  document.addEventListener('dragstart', function(e){ if (e.target.tagName === 'IMG') e.preventDefault(); });
  // o que for copiado leva a assinatura
  document.addEventListener('copy', function(e){
    var sel = String(window.getSelection() || '');
    if (!sel || e.target.closest && e.target.closest('input,textarea')) return;
    e.clipboardData.setData('text/plain', sel + SIGN);
    e.preventDefault();
    show();
  });
})();
