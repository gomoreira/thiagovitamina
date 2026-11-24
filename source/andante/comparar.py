"""Página de apresentação em /andante: versão A e versão B lado a lado,
no design system do thiagovitamina.com (o mesmo padrão da página da Bammies)."""
import sys, pathlib, shutil, urllib.parse
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sistema

ROOT = pathlib.Path(sys.argv[1]); HERE = pathlib.Path(__file__).parent
(ROOT / "review").mkdir(parents=True, exist_ok=True)
for f in (HERE / "review").glob("*-1440.webp"): shutil.copy(f, ROOT / "review" / f.name)
sistema.CHANGES.clear(); sistema.build((HERE / "src/assets/css/site.css").read_text())
n = len(sistema.CHANGES)

WHATS = "https://wa.me/5511956299380?text=" + urllib.parse.quote("thiago, vi as duas versões da andante. prefiro a versão ")

def phone(v, letra, nome):
    return f'''<figure class="version">
          <figcaption><b>Versão {letra}</b> {nome}</figcaption>
          <div class="stage-box">
            <div class="phone"><div class="screen"><iframe src="/andante/{v}/" title="Site da Andante, versão {letra}, {nome}" loading="lazy"></iframe></div></div>
            <p class="hint">Role e toque dentro do celular.</p>
          </div>
          <a class="open" href="/andante/{v}/" target="_blank" rel="noopener">Abrir a versão {letra} em tela cheia<span class="arw" aria-hidden="true"></span></a>
        </figure>'''

def shot(v, letra, nome):
    return f'''<figure class="version">
          <figcaption><b>Versão {letra}</b> {nome}</figcaption>
          <a class="shot" href="/andante/{v}/" target="_blank" rel="noopener" aria-label="Abrir a versão {letra} no computador"><img src="/andante/review/{v}-1440.webp" width="1440" height="2000" alt="Início do site da Andante na versão {letra}, numa tela de computador" loading="lazy" decoding="async"></a>
        </figure>'''

MUDA = [
  ("Tipografia", "15 tamanhos escritos um a um, copiados do desenho", "7 tamanhos que crescem juntos, do celular ao computador"),
  ("Botões", "Texto de 14px e 38px de altura", "Texto do tamanho do texto corrido (16 a 18px) e 52 a 56px de altura, fácil de tocar"),
  ("Vermelho dos botões", "#f00000, com o texto branco abaixo do contraste mínimo de leitura", "#e60000, um tom mais fechado, que passa no contraste"),
  ("Espaçamento", "Medidas soltas entre os blocos", f"Uma escala só (4, 8, 16, 24, 32, 48, 64 e 104px), com {n} medidas ajustadas"),
  ("Grid", "Colunas definidas bloco a bloco", "4 colunas no celular, 8 no tablet e 12 no computador, com a mesma calha"),
  ("Cabeçalho no computador", "Menu e logo", "As seções do site e o botão de reserva sempre à vista"),
  ("Rodapé", "Logo e assinatura", "Logo, assinatura e os links das viagens, que ajudam a navegar e o Google a encontrar"),
  ("Contato", "Pelos botões dos grupos", "Também um bloco de contato pelo WhatsApp no fim da página"),
]

AMBAS = [
  "Navegação completa pelo teclado e menu que fecha com Esc.",
  "Leitura correta por leitor de tela, com descrição em todas as fotos.",
  "Fotos leves e no tamanho certo para cada tela, para abrir rápido no 4G.",
  "Nenhuma tela rola para os lados, do celular pequeno ao computador.",
  "Ícone na aba do navegador e na tela inicial do celular.",
  "Prévia própria ao compartilhar no WhatsApp e nas redes, e o que o Google precisa: título, descrição, mapa do site e os dados de cada viagem.",
  "Os cards dos grupos no modelo de referência que o Lucas escolheu.",
]

html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#FFFFFF">
<title>Andante · versões A e B · Thiago Vitamina</title>
<meta name="description" content="O site da Andante em duas versões lado a lado, para escolher juntos.">
<meta property="og:title" content="Andante · versões A e B">
<meta property="og:description" content="O site da Andante em duas versões lado a lado, para escolher juntos.">
<meta property="og:image" content="https://thiagovitamina.com/andante/original/assets/og/inicio.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/funnel-display-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/funnel-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>
@font-face{{font-family:'Funnel Display';font-style:normal;font-weight:400 800;font-display:swap;src:url(/assets/fonts/funnel-display-latin-ext.woff2) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C4,U+2113,U+2C60-2C7F,U+A720-A7FF}}
@font-face{{font-family:'Funnel Display';font-style:normal;font-weight:400 800;font-display:swap;src:url(/assets/fonts/funnel-display-latin.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}}
@font-face{{font-family:'Funnel Sans';font-style:normal;font-weight:400 600;font-display:swap;src:url(/assets/fonts/funnel-sans-latin-ext.woff2) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C4,U+2113,U+2C60-2C7F,U+A720-A7FF}}
@font-face{{font-family:'Funnel Sans';font-style:normal;font-weight:400 600;font-display:swap;src:url(/assets/fonts/funnel-sans-latin.woff2) format('woff2');unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}}

/* tokens do thiagovitamina.com */
:root{{
  --paper:#FFFFFF; --ink:#000000; --plum:#551A8B; --mute:#615C68; --rule:#E3E0E8; --well:#F4F2F7; --night:#0B0A0D;
  --on-dark:#F2EFEA; --mute-dark:#A39DAA; --link-dark:#C9A6F2;
  --display:"Funnel Display","Helvetica Neue",Arial,sans-serif; --text:"Funnel Sans","Helvetica Neue",Arial,sans-serif;
  --t-sm:14px; --t-base:16px; --t-md:20px; --t-lg:28px; --t-xl:44px; --t-2xl:72px;
  --sp-1:4px; --sp-2:8px; --sp-3:16px; --sp-4:24px; --sp-5:40px; --sp-6:64px; --sp-7:104px;
  --gap:var(--sp-4); --max:1440px; --section:var(--sp-7);
  --gut:max(var(--sp-5),env(safe-area-inset-left,0px)); --gutR:max(var(--sp-5),env(safe-area-inset-right,0px));
  --ease:cubic-bezier(.2,.8,.2,1);
  --arw:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath d='M3.5 12.5 12 4M5.5 3.75h6.75v6.75' fill='none' stroke='%23000' stroke-width='1.6' stroke-linecap='square'/%3E%3C/svg%3E");
  color-scheme:light;
}}
@media (max-width:1100px){{:root{{--t-2xl:56px;--t-xl:36px}}}}
@media (max-width:820px){{:root{{--t-md:18px;--t-lg:22px;--t-xl:30px;--t-2xl:42px;--section:var(--sp-6);--gap:var(--sp-3);--gut:max(16px,env(safe-area-inset-left,0px));--gutR:max(16px,env(safe-area-inset-right,0px))}}}}

*,*::before,*::after{{box-sizing:border-box}}
html{{-webkit-text-size-adjust:100%;scroll-behavior:smooth}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--text);font-size:var(--t-base);line-height:1.5;-webkit-font-smoothing:antialiased}}
h1,h2,h3,p,ol,ul,figure{{margin:0}}
img{{max-width:100%;height:auto;display:block}}
a{{color:var(--plum);text-underline-offset:.2em;text-decoration-thickness:1px}}
a:hover{{text-decoration-thickness:2px}}
:focus-visible{{outline:2px solid var(--plum);outline-offset:3px}}
::selection{{background:rgba(85,26,139,.24)}}
.wrap{{padding-left:var(--gut);padding-right:var(--gutR);max-width:calc(var(--max) + var(--gut) + var(--gutR));margin:0 auto}}
.grid{{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:var(--gap)}}
.arw{{display:inline-block;width:.72em;height:.72em;background:currentColor;-webkit-mask:var(--arw) center/contain no-repeat;mask:var(--arw) center/contain no-repeat;flex:none;transition:transform .35s var(--ease)}}
.skip{{position:absolute;left:var(--gut);top:-100px;z-index:50;background:var(--plum);color:var(--paper);padding:var(--sp-2) var(--sp-3)}}
.skip:focus{{top:var(--sp-2)}}

/* links e botões do site */
.open{{display:inline-flex;align-items:center;gap:var(--sp-1);align-self:flex-start;color:var(--plum);text-decoration:underline;min-height:24px}}
.btn-ink,.btn-ink:visited{{position:relative;isolation:isolate;overflow:hidden;align-self:flex-start;display:inline-flex;align-items:center;gap:var(--sp-3);padding:var(--sp-3) var(--sp-4);border:1.5px solid var(--plum);color:var(--plum);background:transparent;text-decoration:none;font-family:var(--display);font-weight:600;font-size:var(--t-md);letter-spacing:-.01em;line-height:1;transition:color .35s}}
.btn-ink::before{{content:"";position:absolute;z-index:-1;left:var(--x,50%);top:var(--y,50%);width:12px;height:12px;margin:-6px 0 0 -6px;border-radius:50%;background:var(--plum);transform:scale(0);transition:transform .55s var(--ease)}}
.btn-ink .arw{{width:.8em;height:.8em}}
@media (hover:hover){{
  .btn-ink:hover{{color:var(--paper)}}
  .btn-ink:hover::before{{transform:scale(var(--k,60))}}
  .btn-ink:hover .arw,.open:hover .arw{{transform:translate(3px,-3px)}}
}}
.btn-ink:focus-visible{{color:var(--paper)}}
.btn-ink:focus-visible::before{{transform:scale(var(--k,60))}}
@media (hover:none){{.btn-ink,.btn-ink:visited{{background:var(--plum);color:var(--paper)}}}}

/* topo */
.top{{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.72);-webkit-backdrop-filter:blur(18px) saturate(1.6);backdrop-filter:blur(18px) saturate(1.6);border-bottom:1px solid rgba(0,0,0,.06)}}
.top-in{{display:flex;justify-content:space-between;align-items:center;gap:var(--sp-2) var(--sp-4);flex-wrap:wrap;padding-block:var(--sp-3)}}
.top .name,.top .name:visited{{font-family:var(--display);font-weight:600;color:var(--ink);text-decoration:none}}
.top nav{{display:flex;gap:var(--sp-4);flex-wrap:wrap}}
.top nav a,.top nav a:visited{{color:var(--ink);text-decoration:none;display:inline-flex;gap:var(--sp-2);align-items:baseline;min-height:24px}}
.top nav a span{{font-size:var(--t-sm);color:var(--mute)}}
@media (hover:hover){{.top .name:hover,.top nav a:hover{{color:var(--plum);text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:.3em}}}}

/* abertura */
.opening{{padding-block:var(--sp-6) var(--sp-5);row-gap:var(--sp-4);align-items:end}}
.opening h1{{grid-column:1 / span 8;font-family:var(--display);font-weight:600;font-size:var(--t-2xl);line-height:.95;letter-spacing:-.035em;text-wrap:balance}}
.opening h1 span{{display:block;font-weight:400;color:var(--mute)}}
.opening .lead{{grid-column:9 / span 4;font-size:var(--t-md);line-height:1.4;max-width:44ch;text-wrap:pretty}}

/* partes */
.part{{padding-block:var(--sp-5) var(--section);scroll-margin-top:var(--sp-6)}}
.part + .part{{padding-top:var(--section)}}
.head{{border-top:1px solid var(--ink);padding-top:var(--sp-3);margin-bottom:var(--sp-6);row-gap:var(--sp-3)}}
.head h2{{grid-column:1 / span 3;font-family:var(--display);font-weight:600;font-size:var(--t-base);line-height:1.3}}
.head p{{grid-column:4 / span 7;font-family:var(--display);font-size:var(--t-lg);line-height:1.25;letter-spacing:-.012em;max-width:34ch;text-wrap:pretty}}
.sub{{font-family:var(--display);font-weight:600;font-size:var(--t-base);margin:var(--sp-6) 0 var(--sp-4)}}

/* lado a lado */
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:var(--gap)}}
.version{{display:flex;flex-direction:column;gap:var(--sp-3);min-width:0}}
.version figcaption{{font-size:var(--t-base);color:var(--mute)}}
.version figcaption b{{font-family:var(--display);font-weight:600;color:var(--ink);margin-right:var(--sp-2)}}
.stage-box{{position:relative;isolation:isolate;overflow:hidden;background:var(--night);display:flex;flex-direction:column;align-items:center;padding:var(--sp-6) var(--sp-4)}}
.stage-box::before{{content:"";position:absolute;inset:0;z-index:-2;background:url(/andante/original/assets/img/hero-1200.webp) center 70%/cover no-repeat}}
.stage-box::after{{content:"";position:absolute;inset:0;z-index:-1;background:var(--night);opacity:.72;pointer-events:none}}
.stage-box .hint{{font-size:var(--t-sm);color:var(--mute-dark);margin-top:var(--sp-3)}}
.stage-box :focus-visible{{outline-color:var(--link-dark)}}
.phone{{width:336px;max-width:100%;border-radius:44px;padding:12px;background:rgba(242,239,234,.16);-webkit-backdrop-filter:blur(22px) saturate(1.6);backdrop-filter:blur(22px) saturate(1.6);box-shadow:0 0 0 1px rgba(255,255,255,.16),inset 0 1px 0 rgba(255,255,255,.22),0 0 0 2px rgba(0,0,0,.4),0 28px 56px -14px rgba(0,0,0,.5)}}
.screen{{position:relative;height:700px;border-radius:32px;overflow:hidden;overflow:clip;background:var(--night)}}
.screen iframe{{position:absolute;inset:0;width:100%;height:100%;border:0}}
.shot{{display:block;border:1px solid var(--rule);overflow:hidden;aspect-ratio:1440/1100;background:var(--night)}}
.shot img{{width:100%;height:100%;object-fit:cover;object-position:top}}

/* o que muda */
.diff{{width:100%;border-collapse:collapse;border-top:1px solid var(--ink)}}
.diff th,.diff td{{text-align:left;vertical-align:top;padding:var(--sp-3) var(--sp-4) var(--sp-3) 0;border-bottom:1px solid var(--rule)}}
.diff thead th{{font-size:var(--t-sm);font-weight:400;color:var(--mute)}}
.diff tbody th{{font-family:var(--display);font-weight:600;width:22%}}
.diff td{{width:39%;text-wrap:pretty}}
.diff td:last-child{{font-weight:600}}
.both{{list-style:none;padding:0;border-top:1px solid var(--rule);max-width:72ch}}
.both li{{display:grid;grid-template-columns:var(--sp-5) 1fr;padding-block:var(--sp-3);border-bottom:1px solid var(--rule);text-wrap:pretty}}
.both li span{{color:var(--mute);font-size:var(--t-sm)}}

/* próximos passos */
.steps{{row-gap:var(--sp-5);align-items:start}}
.steps ol{{grid-column:1 / span 6;list-style:none;padding:0;border-top:1px solid var(--rule)}}
.steps li{{display:grid;grid-template-columns:104px 1fr;gap:var(--sp-3);padding-block:var(--sp-3);border-bottom:1px solid var(--rule)}}
.steps li b{{font-family:var(--display);font-weight:600}}
.steps .ask{{grid-column:8 / span 5;display:flex;flex-direction:column;gap:var(--sp-4)}}
.steps .ask p{{font-size:var(--t-md);line-height:1.45;text-wrap:pretty}}

/* rodapé */
.foot-simple{{border-top:1px solid var(--rule);padding-block:var(--sp-5)}}
.foot-simple .wrap{{display:flex;flex-wrap:wrap;justify-content:space-between;gap:var(--sp-2) var(--sp-4);font-size:var(--t-sm);color:var(--mute)}}
.foot-simple .open{{font-size:var(--t-sm)}}

@media (max-width:820px){{
  .grid{{display:flex;flex-direction:column}}
  .opening{{padding-block:var(--sp-5) var(--sp-4)}}
  .top{{position:relative}}
  .top nav{{gap:var(--sp-3);font-size:var(--t-sm)}}
  .head{{margin-bottom:var(--sp-5)}}
  .pair{{grid-template-columns:1fr;row-gap:var(--sp-6)}}
  .stage-box{{padding:var(--sp-5) var(--sp-3)}}
  .phone{{width:300px}}
  .screen{{height:600px}}
  .diff thead{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}}
  .diff tr{{display:grid;grid-template-columns:1fr 1fr;column-gap:var(--sp-3);padding-block:var(--sp-3);border-bottom:1px solid var(--rule)}}
  .diff th,.diff td{{width:auto;border:0;padding:0}}
  .diff tbody th{{grid-column:1 / -1;margin-bottom:var(--sp-2);width:auto}}
  .diff td::before{{content:attr(data-label);display:block;font-size:var(--t-sm);font-weight:400;color:var(--mute)}}
  .steps li{{grid-template-columns:88px 1fr}}
}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}*{{transition:none !important}}}}
</style>
</head>
<body>
<a class="skip" href="#main">Pular pro conteúdo</a>

<header class="top">
  <div class="wrap top-in">
    <a class="name" href="/">Thiago Vitamina</a>
    <nav aria-label="Partes da apresentação">
      <a href="#lado"><span>1</span>Lado a lado</a>
      <a href="#muda"><span>2</span>O que muda</a>
      <a href="#passos"><span>3</span>Próximos passos</a>
    </nav>
  </div>
</header>

<main id="main">

  <section class="wrap opening grid" aria-labelledby="h-top">
    <h1 id="h-top">Andante, em duas versões. <span>O mesmo site, pra escolher juntos.</span></h1>
    <p class="lead">A versão A é o desenho do Lucas, do jeito que ele fez. A B é a mesma página com um sistema de tipografia, espaçamento e grid, e ajustes de leitura e de toque. O conteúdo e as fotos são os mesmos nas duas.</p>
  </section>

  <section class="part" id="lado" aria-labelledby="h-lado">
    <div class="wrap">
      <div class="head grid">
        <h2 id="h-lado">1 · Lado a lado</h2>
        <p>As duas funcionam de verdade. Dá pra rolar, abrir o menu e entrar nas viagens dentro de cada celular.</p>
      </div>
      <div class="pair">
        {phone("original", "A", "o desenho original")}
        {phone("vitamina", "B", "com o sistema e os ajustes")}
      </div>
      <h3 class="sub">No computador</h3>
      <div class="pair">
        {shot("original", "A", "o desenho original")}
        {shot("vitamina", "B", "com o sistema e os ajustes")}
      </div>
    </div>
  </section>

  <section class="part" id="muda" aria-labelledby="h-muda">
    <div class="wrap">
      <div class="head grid">
        <h2 id="h-muda">2 · O que muda na B</h2>
        <p>Poucas regras que valem pro site inteiro, no lugar de medidas escritas uma a uma. Assim cada página nova já nasce no mesmo ritmo.</p>
      </div>
      <table class="diff">
        <thead><tr><th scope="col">O quê</th><th scope="col">Versão A</th><th scope="col">Versão B</th></tr></thead>
        <tbody>
          {"".join(f'<tr><th scope="row">{o}</th><td data-label="Versão A">{a}</td><td data-label="Versão B">{b}</td></tr>' for o, a, b in MUDA)}
        </tbody>
      </table>
      <h3 class="sub">O que já vale pras duas</h3>
      <ul class="both">
        {"".join(f'<li><span>{i}</span>{t}</li>' for i, t in enumerate(AMBAS, 1))}
      </ul>
    </div>
  </section>

  <section class="part" id="passos" aria-labelledby="h-passos">
    <div class="wrap">
      <div class="head grid">
        <h2 id="h-passos">3 · Próximos passos</h2>
        <p>O que estiver entre colchetes é provisório e entra quando o conteúdo chegar.</p>
      </div>
      <div class="steps grid">
        <ol>
          <li><b>Agora</b><span>Escolher entre a versão A e a B.</span></li>
          <li><b>Esta semana</b><span>Conteúdo do País Basco, da home e do quem somos. Peru e Gaga e Piemonte quando estiverem prontos.</span></li>
          <li><b>Até 2/12</b><span>Ajustes da revisão.</span></li>
          <li><b>3/12</b><span>Domínio e site na Hostinger da Andante.</span></li>
          <li><b>4/12</b><span>Site no ar.</span></li>
        </ol>
        <div class="ask">
          <p>Olhou as duas? Me conta qual prefere, ou o que pegaria de cada uma.</p>
          <a class="btn-ink" href="{WHATS}" target="_blank" rel="noopener"><span>Responder no WhatsApp</span><span class="arw" aria-hidden="true"></span></a>
        </div>
      </div>
    </div>
  </section>

</main>

<footer class="foot-simple">
  <div class="wrap">
    <span>Andante · proposta de site · Thiago Vitamina</span>
    <a class="open" href="https://thiagovitamina.com/" target="_blank" rel="noopener">thiagovitamina.com<span class="arw" aria-hidden="true"></span></a>
  </div>
</footer>
<script>
// a tinta do botão entra de onde o cursor chegou, como no site
document.querySelectorAll('.btn-ink').forEach(b=>b.addEventListener('pointerenter',e=>{{const r=b.getBoundingClientRect();b.style.setProperty('--x',(e.clientX-r.left)+'px');b.style.setProperty('--y',(e.clientY-r.top)+'px');b.style.setProperty('--k',Math.ceil(Math.hypot(r.width,r.height)/6)+2)}}));
</script>
</body>
</html>
"""
(ROOT / "index.html").write_text(html)
print("comparar →", ROOT / "index.html", f"({n} medidas)")
