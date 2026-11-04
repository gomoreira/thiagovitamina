/* Section ink: the same fluid ink as the hero, without video.
   Usage: <section data-ink="light"> or data-ink="dark". The canvas sits behind the section's content. */
(()=>{
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const THEMES={
  light:{bg:[1,1,1],rim:[.333,.102,.545],fill:[.894,.839,.969]},   // white page, plum rim, lilac fill: black text stays readable
  dark:{bg:[0,0,0],rim:[.788,.651,.949],fill:[.333,.102,.545]}     // black band, lilac rim, plum fill: white text stays readable
};
const VS=`#version 300 es
in vec2 aPos;uniform vec2 uTexel;out vec2 vUv,vL,vR,vT,vB;
void main(){vUv=aPos*.5+.5;vL=vUv-vec2(uTexel.x,0.);vR=vUv+vec2(uTexel.x,0.);vT=vUv+vec2(0.,uTexel.y);vB=vUv-vec2(0.,uTexel.y);gl_Position=vec4(aPos,0.,1.);}`;
const P='#version 300 es\nprecision highp float;precision highp sampler2D;in vec2 vUv,vL,vR,vT,vB;out vec4 o;\n';
const FS={
 splat:P+`uniform sampler2D uTarget;uniform float uAspect,uRadius;uniform vec2 uPoint;uniform vec3 uColor;
  void main(){vec2 p=vUv-uPoint;p.x*=uAspect;o=vec4(texture(uTarget,vUv).xyz+exp(-dot(p,p)/uRadius)*uColor,1.);}`,
 advect:P+`uniform sampler2D uVelocity,uSource;uniform vec2 uVelTexel;uniform float uDt,uDiss;
  void main(){o=uDiss*texture(uSource,vUv-uDt*texture(uVelocity,vUv).xy*uVelTexel);}`,
 curl:P+`uniform sampler2D uVelocity;void main(){o=vec4(.5*(texture(uVelocity,vR).y-texture(uVelocity,vL).y-texture(uVelocity,vT).x+texture(uVelocity,vB).x),0.,0.,1.);}`,
 vort:P+`uniform sampler2D uVelocity,uCurl;uniform float uCurlK,uDt;
  void main(){float L=texture(uCurl,vL).x,R=texture(uCurl,vR).x,T=texture(uCurl,vT).x,B=texture(uCurl,vB).x,C=texture(uCurl,vUv).x;
  vec2 f=.5*vec2(abs(T)-abs(B),abs(R)-abs(L));f/=length(f)+1e-4;f*=uCurlK*C;f.y*=-1.;o=vec4(clamp(texture(uVelocity,vUv).xy+f*uDt,-1000.,1000.),0.,1.);}`,
 div:P+`uniform sampler2D uVelocity;void main(){float L=texture(uVelocity,vL).x,R=texture(uVelocity,vR).x,T=texture(uVelocity,vT).y,B=texture(uVelocity,vB).y;
  vec2 C=texture(uVelocity,vUv).xy;if(vL.x<0.)L=-C.x;if(vR.x>1.)R=-C.x;if(vT.y>1.)T=-C.y;if(vB.y<0.)B=-C.y;o=vec4(.5*(R-L+T-B),0.,0.,1.);}`,
 clear:P+`uniform sampler2D uTex;uniform float uVal;void main(){o=uVal*texture(uTex,vUv);}`,
 press:P+`uniform sampler2D uPressure,uDiv;void main(){o=vec4((texture(uPressure,vL).x+texture(uPressure,vR).x+texture(uPressure,vB).x+texture(uPressure,vT).x-texture(uDiv,vUv).x)*.25,0.,0.,1.);}`,
 grad:P+`uniform sampler2D uPressure,uVelocity;void main(){float L=texture(uPressure,vL).x,R=texture(uPressure,vR).x,T=texture(uPressure,vT).x,B=texture(uPressure,vB).x;o=vec4(texture(uVelocity,vUv).xy-vec2(R-L,T-B),0.,1.);}`,
 show:P+`uniform sampler2D uDye;uniform vec3 uBg,uRim,uFill;
  void main(){float d=texture(uDye,vUv).r;float w=max(fwidth(d)*.9,.0015);
  float m=smoothstep(.42-w,.42+w,d),core=smoothstep(.54-w,.54+w,d);
  o=vec4(mix(uBg,mix(uRim,uFill,core),m),1.);}`
};
function ink(el,theme){
  const cv=document.createElement('canvas');cv.className='ink-canvas';cv.setAttribute('aria-hidden','true');el.prepend(cv);
  const gl=cv.getContext('webgl2',{alpha:false,antialias:false,premultipliedAlpha:false});
  if(!gl||!gl.getExtension('EXT_color_buffer_float')){cv.remove();return}
  const T=THEMES[theme]||THEMES.light;
  const sh=(t,s)=>{const x=gl.createShader(t);gl.shaderSource(x,s);gl.compileShader(x);if(!gl.getShaderParameter(x,gl.COMPILE_STATUS))throw new Error(gl.getShaderInfoLog(x));return x};
  const progs={};for(const k in FS){const p=gl.createProgram();gl.attachShader(p,sh(gl.VERTEX_SHADER,VS));gl.attachShader(p,sh(gl.FRAGMENT_SHADER,FS[k]));gl.bindAttribLocation(p,0,'aPos');gl.linkProgram(p);
    const u={};const n=gl.getProgramParameter(p,gl.ACTIVE_UNIFORMS);for(let i=0;i<n;i++){const nm=gl.getActiveUniform(p,i).name;u[nm]=gl.getUniformLocation(p,nm)}progs[k]={p,u}}
  const q=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,q);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW);gl.enableVertexAttribArray(0);gl.vertexAttribPointer(0,2,gl.FLOAT,false,0,0);
  const tex=(w,h,ifmt,fmt,filter)=>{const t=gl.createTexture();gl.bindTexture(gl.TEXTURE_2D,t);[gl.TEXTURE_MIN_FILTER,gl.TEXTURE_MAG_FILTER].forEach(p=>gl.texParameteri(gl.TEXTURE_2D,p,filter));
    gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);gl.texImage2D(gl.TEXTURE_2D,0,ifmt,w,h,0,fmt,gl.HALF_FLOAT,null);return t};
  const fbo=(w,h,ifmt,fmt,filter)=>{const t=tex(w,h,ifmt,fmt,filter),f=gl.createFramebuffer();gl.bindFramebuffer(gl.FRAMEBUFFER,f);gl.framebufferTexture2D(gl.FRAMEBUFFER,gl.COLOR_ATTACHMENT0,gl.TEXTURE_2D,t,0);gl.viewport(0,0,w,h);gl.clearColor(0,0,0,1);gl.clear(gl.COLOR_BUFFER_BIT);return {t,f,w,h,tx:[1/w,1/h]}};
  const dbl=(w,h,i,f,fl)=>{let a=fbo(w,h,i,f,fl),b=fbo(w,h,i,f,fl);return {get r(){return a},get w(){return b},swap(){[a,b]=[b,a]}}};
  const bind=(u,t)=>{gl.activeTexture(gl.TEXTURE0+u);gl.bindTexture(gl.TEXTURE_2D,t);return u};
  const blit=t=>{if(t){gl.bindFramebuffer(gl.FRAMEBUFFER,t.f);gl.viewport(0,0,t.w,t.h)}else{gl.bindFramebuffer(gl.FRAMEBUFFER,null);gl.viewport(0,0,gl.drawingBufferWidth,gl.drawingBufferHeight)}gl.drawArrays(gl.TRIANGLE_STRIP,0,4)};
  const use=(k,tx)=>{const g=progs[k];gl.useProgram(g.p);gl.uniform2f(g.u.uTexel,tx[0],tx[1]);return g.u};
  let W,H,vel,dye,prs,divT,curlT;
  function init(){W=el.clientWidth;H=el.clientHeight;const D=Math.min(2,devicePixelRatio||1);cv.width=Math.round(W*D);cv.height=Math.round(H*D);
    const a=W/H,res=b=>a>1?[Math.round(b*a),b]:[b,Math.round(b/a)];const [sw,sh2]=res(96),[dw,dh]=res(480);
    vel=dbl(sw,sh2,gl.RG16F,gl.RG,gl.LINEAR);dye=dbl(dw,dh,gl.R16F,gl.RED,gl.LINEAR);prs=dbl(sw,sh2,gl.R16F,gl.RED,gl.NEAREST);divT=fbo(sw,sh2,gl.R16F,gl.RED,gl.NEAREST);curlT=fbo(sw,sh2,gl.R16F,gl.RED,gl.NEAREST)}
  function splat(x,y,dx,dy,amt,rad){
    let u=use('splat',vel.r.tx);gl.uniform1i(u.uTarget,bind(0,vel.r.t));gl.uniform1f(u.uAspect,W/H);gl.uniform2f(u.uPoint,x,y);gl.uniform3f(u.uColor,dx,dy,0);gl.uniform1f(u.uRadius,rad*.6);blit(vel.w);vel.swap();
    u=use('splat',dye.r.tx);gl.uniform1i(u.uTarget,bind(0,dye.r.t));gl.uniform1f(u.uAspect,W/H);gl.uniform2f(u.uPoint,x,y);gl.uniform3f(u.uColor,amt,0,0);gl.uniform1f(u.uRadius,rad);blit(dye.w);dye.swap()}
  function step(dt){
    let u=use('curl',vel.r.tx);gl.uniform1i(u.uVelocity,bind(0,vel.r.t));blit(curlT);
    u=use('vort',vel.r.tx);gl.uniform1i(u.uVelocity,bind(0,vel.r.t));gl.uniform1i(u.uCurl,bind(1,curlT.t));gl.uniform1f(u.uCurlK,9);gl.uniform1f(u.uDt,dt);blit(vel.w);vel.swap();
    u=use('div',vel.r.tx);gl.uniform1i(u.uVelocity,bind(0,vel.r.t));blit(divT);
    u=use('clear',prs.r.tx);gl.uniform1i(u.uTex,bind(0,prs.r.t));gl.uniform1f(u.uVal,.8);blit(prs.w);prs.swap();
    u=use('press',prs.r.tx);gl.uniform1i(u.uDiv,bind(1,divT.t));for(let i=0;i<16;i++){gl.uniform1i(u.uPressure,bind(0,prs.r.t));blit(prs.w);prs.swap()}
    u=use('grad',vel.r.tx);gl.uniform1i(u.uPressure,bind(0,prs.r.t));gl.uniform1i(u.uVelocity,bind(1,vel.r.t));blit(vel.w);vel.swap();
    u=use('advect',vel.r.tx);gl.uniform2f(u.uVelTexel,vel.r.tx[0],vel.r.tx[1]);gl.uniform1i(u.uVelocity,bind(0,vel.r.t));gl.uniform1i(u.uSource,bind(0,vel.r.t));gl.uniform1f(u.uDt,dt);gl.uniform1f(u.uDiss,.985);blit(vel.w);vel.swap();
    u=use('advect',dye.r.tx);gl.uniform2f(u.uVelTexel,vel.r.tx[0],vel.r.tx[1]);gl.uniform1i(u.uVelocity,bind(0,vel.r.t));gl.uniform1i(u.uSource,bind(1,dye.r.t));gl.uniform1f(u.uDt,dt);gl.uniform1f(u.uDiss,.993);blit(dye.w);dye.swap()}
  function render(){const u=use('show',[1/cv.width,1/cv.height]);gl.uniform1i(u.uDye,bind(0,dye.r.t));gl.uniform3fv(u.uBg,T.bg);gl.uniform3fv(u.uRim,T.rim);gl.uniform3fv(u.uFill,T.fill);blit(null)}
  init();render();
  if(reduce)return;
  let ptr=null,visible=false,running=false,last=0,idle=0;
  const uv=e=>{const r=el.getBoundingClientRect();return [(e.clientX-r.left)/r.width,1-(e.clientY-r.top)/r.height]};
  function move(e){const [x,y]=uv(e);if(ptr){ptr.dx=x-ptr.x;ptr.dy=y-ptr.y}else ptr={dx:0,dy:0};ptr.x=x;ptr.y=y;ptr.moved=true;idle=0;wake()}
  el.addEventListener('pointermove',e=>{if(e.pointerType!=='touch')move(e)});
  el.addEventListener('pointerleave',e=>{if(e.pointerType!=='touch')ptr=null});
  el.addEventListener('touchstart',e=>{ptr=null;move(e.touches[0])},{passive:true});
  el.addEventListener('touchmove',e=>move(e.touches[0]),{passive:true});
  el.addEventListener('touchend',()=>{ptr=null},{passive:true});
  function loop(now){
    const dt=Math.min(.0166,(now-last)/1000||.016);last=now;
    if(ptr&&ptr.moved){const sp=Math.hypot(ptr.dx,ptr.dy);splat(ptr.x,ptr.y,ptr.dx*5000,ptr.dy*5000,.6+Math.min(.9,sp*25),.0022+Math.min(.004,sp*.06));ptr.moved=false}
    step(dt);render();idle+=dt;
    if(visible&&idle<6){requestAnimationFrame(loop)}else running=false;   // sleeps after the ink has dried
  }
  function wake(){if(!running&&visible){running=true;last=performance.now();requestAnimationFrame(loop)}}
  new IntersectionObserver(es=>{visible=es[0].isIntersecting;if(visible)wake()}).observe(el);
  let rt;addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(()=>{if(Math.abs(el.clientWidth-W)>2||Math.abs(el.clientHeight-H)>2){init();render()}},150)});
}
const go=()=>document.querySelectorAll('[data-ink]').forEach(el=>{try{ink(el,el.dataset.ink)}catch(e){console.error(e)}});
document.readyState==='loading'?document.addEventListener('DOMContentLoaded',go):go();
})();
