/* Bammies, versão vitaminada: o app em si. Usado pelo tour (/bammies) e pela versão livre (/bammies/app). */
(function(){
  var FRETE_GRATIS = 150; // valor de exemplo, trocar pelo real

  var choc = '<svg width="58" height="58" viewBox="0 0 64 64" aria-hidden="true"><g transform="rotate(-40 32 32)"><rect x="18" y="4" width="28" height="30" rx="3" fill="#8B5A3C" stroke="#111" stroke-width="3"/><path d="M32 4v30M18 19h28" stroke="#111" stroke-width="3"/><rect x="16" y="28" width="32" height="32" rx="3" fill="WRAP" stroke="#111" stroke-width="3"/><path d="M32 51c-6-4-9-7-9-10a4 4 0 0 1 9-2 4 4 0 0 1 9 2c0 3-3 6-9 10z" fill="#E84D5B" stroke="#111" stroke-width="2"/></g></svg>';
  function bear(w){ return '<svg width="'+w+'" height="'+Math.round(w*1.29)+'" viewBox="0 0 84 108" aria-hidden="true"><g fill="#E7A9DE" stroke="#111" stroke-width="5"><circle cx="20" cy="14" r="10"/><circle cx="64" cy="14" r="10"/><ellipse cx="42" cy="30" rx="26" ry="22"/><ellipse cx="42" cy="72" rx="28" ry="30"/><circle cx="16" cy="64" r="10"/><circle cx="68" cy="64" r="10"/><circle cx="22" cy="96" r="11"/><circle cx="62" cy="96" r="11"/></g><circle cx="33" cy="24" r="3.5" fill="#111"/><circle cx="51" cy="24" r="3.5" fill="#111"/></svg>'; }

  // dados dos produtos: trocar pelos reais
  var PRODUCTS = [
    {id:'albino', list:'choc', name:'Barra Albino', desc:'chocolate, recheio e peso em uma linha', price:70, note:'apenas envio', bg:'#FCE4F3', img:choc.replace('WRAP','#FFFFFF')},
    {id:'envy', list:'choc', name:'Barra Envy', desc:'chocolate, recheio e peso em uma linha', price:75, note:'apenas envio', bg:'#E3F0FC', img:choc.replace('WRAP','#5DADEC'), top:true},
    {id:'bg', list:'bam', name:'Bammies G', desc:'peso ou unidades e sabores', price:null, note:'pronta entrega', ok:true, bg:'#FCE4F3', img:bear(52), size:'G'},
    {id:'bp', list:'bam', name:'Bammies P', desc:'peso ou unidades e sabores', price:null, note:'pronta entrega', ok:true, bg:'#FCE4F3', img:bear(36), size:'P'}
  ];

  var I = {
    plus:'<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
    minus:'<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14"/></svg>',
    star:'<svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2.5l2.9 6.2 6.6.7-5 4.5 1.4 6.6L12 17.2l-5.9 3.3 1.4-6.6-5-4.5 6.6-.7z"/></svg>',
    x:'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    back:'<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>'
  };
  function brl(v){ return v==null ? 'R$ 00,00' : 'R$ ' + v.toFixed(2).replace('.',','); }

  window.BammiesApp = function(root, opts){
    opts = opts || {};
    var uid = 'bm' + Math.random().toString(36).slice(2,7);
    root.classList.add('bm');
    root.innerHTML =
      '<div class="bm-app">'+
        '<div class="bm-bar">'+(opts.backHref?'<a class="bm-back" href="'+opts.backHref+'" aria-label="Voltar pra leitura">'+I.back+'</a>':'')+'BAMMIES</div>'+
        '<nav class="bm-chips" aria-label="Categorias"><a href="#" data-go="choc" aria-current="true">Chocolates</a><a href="#" data-go="bam">Bammies</a><a href="#" data-go="bam">Pra presentear</a></nav>'+
        '<div class="bm-sec" data-sec="choc">Chocolates</div><div class="bm-list" data-list="choc"></div>'+
        '<div class="bm-sec" data-sec="bam">Bammies</div><div class="bm-list" data-list="bam"></div>'+
      '</div>'+
      '<div class="bm-cart">'+
        '<div class="bm-frete" aria-live="polite"><span class="bm-frete-text"></span><div class="bm-track" aria-hidden="true"><div class="bm-fill"></div></div></div>'+
        '<div class="bm-cart-row"><span class="bm-cart-text" aria-live="polite"></span><button type="button" data-act="cart">ver carrinho</button></div>'+
      '</div>'+
      '<div class="bm-scrim" data-act="close"></div>'+
      '<div class="bm-sheet bm-product" role="dialog" aria-modal="true" aria-labelledby="'+uid+'p">'+
        '<button type="button" class="bm-close" data-act="close" aria-label="Fechar detalhes">'+I.x+'</button>'+
        '<h4 id="'+uid+'p">Barra Albino</h4>'+
        '<dl><dt>Chocolate</dt><dd>[tipo e % de cacau]</dd><dt>Recheio</dt><dd>[sabor do recheio]</dd><dt>Peso</dt><dd>[gramas]</dd><dt>Alergênicos</dt><dd>[leite, glúten, castanhas…]</dd><dt>Validade</dt><dd>[prazo]</dd></dl>'+
        '<button type="button" class="bm-add" data-act="sheetadd" style="justify-content:center">adicionar ao carrinho</button>'+
      '</div>'+
      '<div class="bm-sheet bm-checkout" role="dialog" aria-modal="true" aria-labelledby="'+uid+'c">'+
        '<button type="button" class="bm-close" data-act="close" aria-label="Fechar carrinho">'+I.x+'</button>'+
        '<h4 id="'+uid+'c">Seu pedido</h4>'+
        '<ul class="bm-lines bm-cart-lines"></ul>'+
        '<div class="bm-field"><label for="'+uid+'cep">CEP de entrega</label><input id="'+uid+'cep" class="bm-cep" inputmode="numeric" autocomplete="postal-code" placeholder="00000-000" maxlength="9"><output class="bm-cep-out" for="'+uid+'cep"></output></div>'+
        '<fieldset class="bm-pay"><legend>Pagamento</legend><label><input type="radio" name="'+uid+'pay" checked> Pix <small>aprova na hora</small></label><label><input type="radio" name="'+uid+'pay"> Cartão de crédito</label></fieldset>'+
        '<button type="button" class="bm-add" data-act="finish" style="justify-content:center;min-height:52px;font-size:15px">finalizar pedido</button>'+
        '<p class="bm-note">sem cadastro e sem senha</p>'+
      '</div>'+
      '<div class="bm-done"><div class="bm-done-card" role="status">'+
        '<div class="bm-check"><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#17663F" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg></div>'+
        '<h4>Pedido recebido!</h4><p>Pix aprovado. A gente te avisa pelo WhatsApp quando sair pra entrega.</p>'+
        '<ul class="bm-lines bm-done-lines"></ul>'+
        '<button type="button" class="bm-add" data-act="close">voltar pra loja</button>'+
      '</div></div>';

    var q = function(s){ return root.querySelector(s); };
    var app = q('.bm-app'), cart = q('.bm-cart'), cep = q('.bm-cep');
    var qty = {albino:0, envy:1, bg:0, bp:0};
    var current = null;
    var api = {root:root, app:app, qty:qty, products:PRODUCTS, onChange:null};

    // nada dentro do app pode rolar a "tela" em si
    root.addEventListener('scroll', function(){ root.scrollTop = 0; root.scrollLeft = 0; });

    function totals(){
      var n=0, t=0;
      PRODUCTS.forEach(function(p){ n+=qty[p.id]; t+=(p.price||0)*qty[p.id]; });
      return {n:n, t:t};
    }
    function lines(){
      var h='', T=totals();
      PRODUCTS.forEach(function(p){ if(qty[p.id]) h+='<li><span>'+qty[p.id]+'× '+p.name+'</span><span>'+brl(p.price==null?null:p.price*qty[p.id])+'</span></li>'; });
      h += '<li><span>Frete</span><span>'+(T.t>=FRETE_GRATIS?'grátis':'pelo CEP')+'</span></li>';
      h += '<li class="tot"><span>Total</span><span>'+brl(T.t)+'</span></li>';
      return h;
    }
    function control(p){
      var n = qty[p.id];
      if(!n) return '<button type="button" class="bm-add" data-add="'+p.id+'">'+I.plus+'adicionar <span class="sr">'+p.name+'</span></button>';
      return '<div class="bm-qty"><button type="button" data-dec="'+p.id+'" aria-label="Diminuir quantidade de '+p.name+'">'+I.minus+'</button><output aria-label="Quantidade de '+p.name+'">'+n+'</output><button type="button" data-inc="'+p.id+'" aria-label="Aumentar quantidade de '+p.name+'">'+I.plus+'</button></div>';
    }
    function updateCep(){
      var v = cep.value.replace(/\D/g,''), out = q('.bm-cep-out');
      out.textContent = v.length<8 ? '' : (totals().t>=FRETE_GRATIS ? 'frete grátis' : 'frete [valor]') + ' · chega em [prazo]';
    }
    function notify(){ if(api.onChange) api.onChange(); }

    function render(changed){
      ['choc','bam'].forEach(function(l){ q('[data-list="'+l+'"]').innerHTML=''; });
      PRODUCTS.forEach(function(p){
        var el = document.createElement('article');
        el.className = 'bm-item' + (qty[p.id] ? ' in-cart' : '');
        el.dataset.id = p.id;
        el.innerHTML =
          '<div class="bm-thumb" style="background:'+p.bg+'">'+p.img+(p.size?'<span class="bm-size">'+p.size+'</span>':'')+'</div>'+
          '<div class="bm-info"><div class="bm-name-row"><h3 class="bm-name">'+p.name+'</h3>'+(p.top?'<span class="bm-badge">'+I.star+'mais pedido</span>':'')+'</div>'+
          '<p class="bm-desc"><em>'+p.desc+'</em></p>'+
          '<button type="button" class="bm-more" data-more="'+p.id+'">mais detalhes <span class="sr">de '+p.name+'</span></button>'+
          '<div class="bm-row"><div class="bm-price"><b>'+brl(p.price)+'</b><small class="'+(p.ok?'ok':'')+'">'+p.note+'</small></div>'+control(p)+'</div></div>';
        q('[data-list="'+p.list+'"]').appendChild(el);
      });
      var T = totals(), falta = Math.max(0, FRETE_GRATIS - T.t);
      q('.bm-cart-text').innerHTML = '<b>'+T.n+(T.n===1?' item':' itens')+'</b> · '+brl(T.t);
      q('.bm-frete-text').innerHTML = falta>0 ? 'faltam <b>'+brl(falta)+'</b> pro frete grátis' : '<b>você ganhou frete grátis</b>';
      q('.bm-fill').style.width = Math.min(100, T.t/FRETE_GRATIS*100) + '%';
      cart.classList.toggle('empty', T.n===0);
      q('.bm-cart-lines').innerHTML = lines();
      q('.bm-done-lines').innerHTML = lines();
      updateCep();
      if(changed){
        cart.classList.remove('bump'); void cart.offsetWidth; cart.classList.add('bump');
        var ctl = q('.bm-item[data-id="'+changed+'"] .bm-qty') || q('.bm-item[data-id="'+changed+'"] .bm-add');
        if(ctl) ctl.classList.add('pop');
      }
      notify();
    }

    function closeAll(){ root.classList.remove('sheet-open','cart-open','done-open'); notify(); }
    function openSheet(id, auto){
      root.classList.remove('cart-open','done-open');
      current = PRODUCTS.filter(function(x){ return x.id===id; })[0];
      q('.bm-product h4').textContent = current.name;
      root.classList.add('sheet-open');
      if(!auto) setTimeout(function(){ q('.bm-product .bm-close').focus({preventScroll:true}); }, 30);
      notify();
    }
    function openCart(auto){
      root.classList.remove('sheet-open','done-open');
      root.classList.add('cart-open');
      if(!auto) setTimeout(function(){ q('.bm-checkout .bm-close').focus({preventScroll:true}); }, 30);
      notify();
    }
    function openDone(){
      root.classList.remove('sheet-open','cart-open');
      root.classList.add('done-open');
      notify();
    }

    root.addEventListener('click', function(e){
      var a = e.target.closest('[data-go]');
      if(a){
        e.preventDefault();
        root.querySelectorAll('.bm-chips a').forEach(function(x){ x.setAttribute('aria-current', x===a); });
        var sec = q('[data-sec="'+a.dataset.go+'"]');
        app.scrollTo({top: sec.offsetTop - 110, behavior:'smooth'});
        return;
      }
      var b = e.target.closest('button,[data-act]'); if(!b) return;
      var act = b.dataset.act;
      if(b.dataset.add){ qty[b.dataset.add]=1; render(b.dataset.add); }
      else if(b.dataset.inc){ qty[b.dataset.inc]++; render(b.dataset.inc); }
      else if(b.dataset.dec){ qty[b.dataset.dec]=Math.max(0,qty[b.dataset.dec]-1); render(b.dataset.dec); }
      else if(b.dataset.more){ openSheet(b.dataset.more); }
      else if(act==='close'){ closeAll(); }
      else if(act==='cart'){ openCart(); }
      else if(act==='finish'){ openDone(); }
      else if(act==='sheetadd'){ if(current){ qty[current.id]=(qty[current.id]||0)+1; closeAll(); render(current.id); } }
    });
    root.addEventListener('keydown', function(e){ if(e.key==='Escape') closeAll(); });
    root.addEventListener('animationend', function(e){ e.target.classList.remove('pop'); if(e.target===cart) cart.classList.remove('bump'); });
    cep.addEventListener('input', function(){
      var d = cep.value.replace(/\D/g,'').slice(0,8);
      cep.value = d.length>5 ? d.slice(0,5)+'-'+d.slice(5) : d;
      updateCep();
    });

    api.render = render; api.closeAll = closeAll; api.openSheet = openSheet; api.openCart = openCart; api.openDone = openDone;
    render();
    return api;
  };
})();
