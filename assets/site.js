/* mobile menu */
(()=>{const b=document.querySelector('.plus'),m=document.getElementById('mnav');if(!b||!m)return;
const set=o=>{b.setAttribute('aria-expanded',o);document.documentElement.classList.toggle('menu-open',o);document.body.style.overflow=o?'hidden':'';
  if(o){m.hidden=false;requestAnimationFrame(()=>m.classList.add('is-open'));m.querySelector('a').focus({preventScroll:true})}
  else{m.classList.remove('is-open');m.hidden=true}};
b.addEventListener('click',()=>set(b.getAttribute('aria-expanded')!=='true'));
m.addEventListener('click',e=>{if(e.target.closest('a'))set(false)});
addEventListener('keydown',e=>{if(e.key==='Escape'&&b.getAttribute('aria-expanded')==='true'){set(false);b.focus()}});
matchMedia('(min-width:821px)').addEventListener('change',e=>{if(e.matches)set(false)});})();
/* header + pages. Each page sticks by its bottom edge; the next page slides over it and the one below dims.
   The header inverts over the paint and turns to dark glass over dark pages. */
(()=>{const h=document.querySelector('.top');if(!h)return;
const paint=document.getElementById('paint'),pages=[paint,...document.querySelectorAll('.sheet')].filter(Boolean);
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
function size(){pages.forEach(p=>p.style.setProperty('--st',Math.min(0,innerHeight-p.offsetHeight)+'px'))}
function check(){const hb=h.offsetHeight,el=document.elementFromPoint(innerWidth/2,hb+2);
  const overPaint=!!(el&&el.closest('.paint'));
  h.classList.toggle('over-paint',overPaint);
  h.classList.toggle('on-dark',!overPaint&&!!(el&&el.closest('.dark,.contact')));
  if(reduce)return;
  for(let i=0;i<pages.length-1;i++){const t=pages[i+1].getBoundingClientRect().top,p=Math.min(1,Math.max(0,1-t/innerHeight));
    pages[i].style.setProperty('--dim',(.32*p).toFixed(3));
    if(pages[i]===paint)paint.style.transform=p>0?'scale('+(1-.05*p)+')':''}}
let last=scrollY,tick=false;
addEventListener('scroll',()=>{if(tick)return;tick=true;requestAnimationFrame(()=>{const y=scrollY;
  if(!document.documentElement.classList.contains('menu-open'))h.classList.toggle('tucked',y>last&&y>160);
  last=y;check();tick=false})},{passive:true});
addEventListener('resize',()=>{size();check()});
addEventListener('load',()=>{size();check()});
size();check();})();
/* ink buttons: remember where the cursor came in */
document.querySelectorAll('.btn-ink').forEach(b=>{const set=e=>{const r=b.getBoundingClientRect();b.style.setProperty('--x',(e.clientX-r.left)+'px');b.style.setProperty('--y',(e.clientY-r.top)+'px');b.style.setProperty('--k',Math.ceil(Math.hypot(r.width,r.height)/6)+1)};
  b.addEventListener('pointerenter',set);b.addEventListener('pointerleave',set)});
/* Bauhaus reveal: modules turn and shrink away as the video scrolls into view */
(()=>{const box=document.querySelector('.bh-reveal');if(!box)return;const g=box.querySelector('.bh-grid');
if(matchMedia('(prefers-reduced-motion: reduce)').matches){g.remove();return}
const C=['#D9372B','#F2B705','#1F5FAD','#141414','#EDE6D6'],T=['sq','qc','ci','hc','qc','sq'];
let cells=[];
function build(){const cols=innerWidth<820?8:14,rows=Math.round(cols*9/16);g.style.gridTemplateColumns='repeat('+cols+',1fr)';g.style.gridTemplateRows='repeat('+rows+',1fr)';g.innerHTML='';cells=[];
  for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){const i=document.createElement('i');i.className=T[(r*7+c*3)%T.length];i.style.setProperty('--c',C[(r*5+c*2)%C.length]);
    const rot=[0,90,180,270][(r+c*3)%4];i.style.transform='rotate('+rot+'deg)';g.append(i);
    const d=(c/cols)*.55+(r/rows)*.25+((r*13+c*7)%10)/10*.2;cells.push({el:i,rot,d})}}
function draw(){const r=box.getBoundingClientRect(),vh=innerHeight;
  const p=Math.min(1,Math.max(0,(vh-r.top)/(vh*0.95)));
  for(const c of cells){const q=Math.min(1,Math.max(0,(p*1.25-c.d)/.3));const e=q*q*(3-2*q);
    c.el.style.transform='rotate('+(c.rot+e*90)+'deg) scale('+(1-e)+')';c.el.style.opacity=1-e}
  g.style.visibility=p>=1&&cells.every(c=>c.el.style.opacity==='0')?'hidden':'visible'}
let t=false;addEventListener('scroll',()=>{if(t)return;t=true;requestAnimationFrame(()=>{draw();t=false})},{passive:true});
let rz;addEventListener('resize',()=>{clearTimeout(rz);rz=setTimeout(()=>{build();draw()},150)});
build();draw();})();
