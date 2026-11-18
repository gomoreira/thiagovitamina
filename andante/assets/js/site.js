// Andante · menu mobile: abre e fecha, prende o foco, fecha com Esc e devolve o foco ao botão.
(() => {
  const menu = document.getElementById('menu');
  const openBtn = document.querySelector('[data-menu-open]');
  if (!menu || !openBtn) return;
  const closeBtn = menu.querySelector('[data-menu-close]');
  const focusables = () => [...menu.querySelectorAll('a[href],button:not([disabled])')];

  const open = () => {
    menu.hidden = false;
    openBtn.setAttribute('aria-expanded', 'true');
    document.body.classList.add('is-locked');
    document.querySelectorAll('[data-inert-when-menu]').forEach(el => el.inert = true);
    requestAnimationFrame(() => { menu.classList.add('is-open'); closeBtn.focus(); });
  };
  const close = (returnFocus = true) => {
    menu.classList.remove('is-open');
    openBtn.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('is-locked');
    document.querySelectorAll('[data-inert-when-menu]').forEach(el => el.inert = false);
    const done = () => { menu.hidden = true; };
    matchMedia('(prefers-reduced-motion: reduce)').matches ? done() : setTimeout(done, 250);
    if (returnFocus) openBtn.focus();
  };

  openBtn.addEventListener('click', open);
  closeBtn.addEventListener('click', () => close());
  // link de âncora dentro do menu: fecha e deixa o navegador rolar até a seção
  menu.addEventListener('click', e => { if (e.target.closest('a[href]')) close(false); });
  document.addEventListener('keydown', e => {
    if (menu.hidden) return;
    if (e.key === 'Escape') { e.preventDefault(); close(); }
    if (e.key === 'Tab') {
      const f = focusables(), first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  // passou para o desktop com o menu aberto: fecha
  matchMedia('(min-width:1100px)').addEventListener('change', m => { if (m.matches && !menu.hidden) close(false); });
})();
