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
/* Bauhaus reveal, driven by the scroll.
   Approach: the modules fly in and lock into a closed grid (the school closes).
   Pinned: the band holds on screen, the grid breaks apart and the video grows to the full width. */
(()=>{const box=document.querySelector('.bh-reveal');if(!box)return;const g=box.querySelector('.bh-grid');
if(matchMedia('(prefers-reduced-motion: reduce)').matches){g.remove();return}
const track=document.createElement('div');track.className='bh-track';box.before(track);
const pin=document.createElement('div');pin.className='bh-pin';track.append(pin);pin.append(box);
const C=['#D9372B','#F2B705','#1F5FAD','#141414','#EDE6D6'],T=['sq','qc','ci','hc','qc','sq'];
let cells=[],extra=0,top0=0,maxS=1;
const cl=v=>Math.min(1,Math.max(0,v)),sm=q=>q*q*(3-2*q);
function build(){const cols=innerWidth<820?6:10,rows=Math.round(cols*9/16);g.style.gridTemplateColumns='repeat('+cols+',1fr)';g.style.gridTemplateRows='repeat('+rows+',1fr)';g.innerHTML='';cells=[];
  for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){const i=document.createElement('i');i.className=T[(r*7+c*3)%T.length];i.style.setProperty('--c',C[(r*5+c*2)%C.length]);
    const rot=[0,90,180,270][(r+c*3)%4],h=((r*13+c*7)%10)/10,ang=(r*37+c*61)%360*Math.PI/180,dist=120+h*220;
    g.append(i);cells.push({el:i,rot,d:(c/cols)*.55+(r/rows)*.25+h*.2,a:(1-c/cols)*.5+h*.5,ox:Math.cos(ang)*dist,oy:Math.sin(ang)*dist,spin:(h>.5?1:-1)*180})}}
function size(){box.style.transform='';const mw=box.offsetWidth,mh=box.offsetHeight,vh=innerHeight;
  extra=Math.round(vh*(innerWidth<820?.7:1.1));top0=Math.max(0,Math.round((vh-mh)/2));
  pin.style.top=top0+'px';track.style.height=(mh+extra)+'px';
  maxS=Math.max(1,Math.min(innerWidth/mw,(vh*.94)/mh))}
function draw(){const r=track.getBoundingClientRect(),vh=innerHeight;
  const enter=cl((vh-r.top)/Math.max(1,vh-top0));            // 0 when the band appears, 1 when it pins
  const t=cl((top0-r.top)/extra);                          // progress while pinned
  const grow=sm(cl((t-.3)/.6));
  box.style.transform='scale('+((.86+.14*sm(enter))*(1+(maxS-1)*grow)).toFixed(4)+')';
  const brk=cl((t-.12)/.55);
  let gone=true;
  for(const c of cells){
    const qa=sm(cl((enter*1.35-c.a*.35)/.65)),qb=sm(cl((brk*1.3-c.d)/.3));
    const x=c.ox*(1-qa),y=c.oy*(1-qa)-qb*40,rot=c.rot+c.spin*(1-qa)+qb*180,sc=(.5+.5*qa)*(1-qb),op=qa*(1-qb);
    c.el.style.transform='translate('+x.toFixed(1)+'%,'+y.toFixed(1)+'%) rotate('+rot.toFixed(1)+'deg) scale('+sc.toFixed(3)+')';
    c.el.style.opacity=op.toFixed(3);if(op>.001)gone=false}
  g.style.visibility=gone&&brk>=1?'hidden':'visible'}
let t=false;addEventListener('scroll',()=>{if(t)return;t=true;requestAnimationFrame(()=>{draw();t=false})},{passive:true});
let rz;addEventListener('resize',()=>{clearTimeout(rz);rz=setTimeout(()=>{build();size();draw()},150)});
addEventListener('load',()=>{size();draw()});
build();size();draw();})();

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

/* second act: each case and each live site rises into place once, when it enters the screen */
(()=>{if(matchMedia('(prefers-reduced-motion: reduce)').matches||!('IntersectionObserver' in window))return;
const items=[...document.querySelectorAll('.case,.live article,.xp details')];if(!items.length)return;
document.documentElement.classList.add('rv-on');
items.forEach(el=>{if(el.matches('details'))return;[...(el.matches('.case')?el.querySelector('.copy').children:el.children)].forEach((c,i)=>c.style.setProperty('--i',i))});
const io=new IntersectionObserver(es=>{
  const enter=es.filter(e=>e.isIntersecting).map(e=>e.target).sort((a,b)=>a.getBoundingClientRect().left-b.getBoundingClientRect().left);
  enter.sort((a,b)=>a.getBoundingClientRect().top-b.getBoundingClientRect().top||0);
  enter.forEach((el,k)=>{if(el.closest('.live'))el.style.setProperty('--d',(k*.12)+'s');if(el.matches('details'))el.style.setProperty('--d',(k*.09)+'s');el.classList.add('in');io.unobserve(el)})},
  {rootMargin:'0px 0px -12% 0px',threshold:.01});
items.forEach(el=>{if(el.getBoundingClientRect().top<innerHeight*.88)el.classList.add('in');else io.observe(el)});})();

/* from the card to the case: name the clicked card's image and title so they travel to the case page, and back */
(()=>{const name=(href,on)=>{const file=new URL(href,location.href).pathname.split('/').pop();
  const a=document.querySelector('.case h3 a[href="'+file+'"]');if(!a)return null;const c=a.closest('.case'),m=c.querySelector('.media');
  m.style.viewTransitionName=on?'case-media':'';a.style.viewTransitionName=on?'case-title':'';return c};
addEventListener('pageswap',e=>{if(!e.viewTransition||!e.activation)return;const to=e.activation.entry&&e.activation.entry.url;if(!to)return;
  if(name(to,true))e.viewTransition.finished.finally(()=>name(to,false))});
addEventListener('pagereveal',e=>{if(!e.viewTransition||!window.navigation||!navigation.activation)return;const from=navigation.activation.from&&navigation.activation.from.url;if(!from)return;
  const c=name(from,true);if(!c){return}
  c.classList.add('in');e.viewTransition.finished.finally(()=>name(from,false))});})();
