/* mobile menu */
(()=>{const b=document.querySelector('.plus'),m=document.getElementById('mnav');if(!b||!m)return;
const set=o=>{b.setAttribute('aria-expanded',o);document.documentElement.classList.toggle('menu-open',o);document.body.style.overflow=o?'hidden':'';
  if(o){m.hidden=false;requestAnimationFrame(()=>m.classList.add('is-open'));m.querySelector('a').focus({preventScroll:true})}
  else{m.classList.remove('is-open');m.hidden=true}};
b.addEventListener('click',()=>set(b.getAttribute('aria-expanded')!=='true'));
m.addEventListener('click',e=>{if(e.target.closest('a'))set(false)});
addEventListener('keydown',e=>{if(e.key==='Escape'&&b.getAttribute('aria-expanded')==='true'){set(false);b.focus()}});
matchMedia('(min-width:821px)').addEventListener('change',e=>{if(e.matches)set(false)});})();
