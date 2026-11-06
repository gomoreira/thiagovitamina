/* mobile menu */
(()=>{const b=document.querySelector('.plus'),m=document.getElementById('mnav');if(!b||!m)return;
const set=o=>{b.setAttribute('aria-expanded',o);document.documentElement.classList.toggle('menu-open',o);document.body.style.overflow=o?'hidden':'';
  if(o){m.hidden=false;requestAnimationFrame(()=>m.classList.add('is-open'));m.querySelector('a').focus({preventScroll:true})}
  else{m.classList.remove('is-open');m.hidden=true}};
b.addEventListener('click',()=>set(b.getAttribute('aria-expanded')!=='true'));
m.addEventListener('click',e=>{if(e.target.closest('a'))set(false)});
addEventListener('keydown',e=>{if(b.getAttribute('aria-expanded')!=='true')return;
  if(e.key==='Escape'){set(false);b.focus();return}
  if(e.key==='Tab'){const f=[b,...m.querySelectorAll('a')],i=f.indexOf(document.activeElement);
    if(e.shiftKey&&i<=0){e.preventDefault();f[f.length-1].focus()}else if(!e.shiftKey&&i===f.length-1){e.preventDefault();f[0].focus()}}});
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

/* ink hover on names and titles: the ink starts where the cursor enters and leaves where it exits */
(()=>{if(!matchMedia('(hover: hover)').matches)return;
const els=document.querySelectorAll('.top .name,.top nav a,.copy h3 a,.xp-co');
els.forEach(el=>{el.classList.add('ink-text');const zone=el.closest('summary')||el;
  const at=e=>{const r=el.getBoundingClientRect();el.style.setProperty('--x',((e.clientX-r.left)/r.width*100).toFixed(1)+'%');el.style.setProperty('--y',((e.clientY-r.top)/r.height*100).toFixed(1)+'%')};
  zone.addEventListener('pointerenter',e=>{at(e);el.classList.add('is-in')});
  zone.addEventListener('pointerleave',e=>{at(e);el.classList.remove('is-in')})});})();
/* living favicon: the ink blot breathes in the tab. 32px canvas, ~8 frames a second, one small PNG per frame.
   Static favicon.svg stays as the fallback (Safari, reduced motion). */
(()=>{if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
const c=document.createElement('canvas');c.width=c.height=64;const x=c.getContext('2d');if(!x)return;
let l=document.querySelector('link[rel="icon"][type="image/svg+xml"]');if(!l)return;
const png=document.createElement('link');png.rel='icon';png.type='image/png';document.head.appendChild(png);
document.querySelectorAll('link[rel="icon"]').forEach(n=>{if(n!==png)n.remove()});
const N=48,R=26.5,p=[];
const draw=t=>{for(let i=0;i<N;i++){const a=i/N*Math.PI*2;
  const r=R*(1+.085*Math.sin(2*a+t*.55)+.06*Math.sin(3*a-t*.8+1.3)+.035*Math.sin(5*a+t*1.25+.4)+.02*Math.sin(7*a-t*1.7));
  p[i]=[32+Math.cos(a)*r+.8*Math.sin(t*.4),32+Math.sin(a)*r*.94+.6*Math.cos(t*.33)]}
  x.clearRect(0,0,64,64);x.fillStyle='#551A8B';x.beginPath();
  for(let i=0;i<N;i++){const a=p[i],b=p[(i+1)%N],m=[(a[0]+b[0])/2,(a[1]+b[1])/2];
    if(i===0){const z=p[N-1];x.moveTo((z[0]+a[0])/2,(z[1]+a[1])/2)}x.quadraticCurveTo(a[0],a[1],m[0],m[1])}
  x.fill();png.href=c.toDataURL('image/png')};
let t0=performance.now();draw(0);setInterval(()=>draw((performance.now()-t0)/1000),125);})();
