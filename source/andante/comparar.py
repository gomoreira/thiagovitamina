"""Página de apresentação em /andante: versão original e versão Vitamina lado a lado,
no design system do thiagovitamina.com (o mesmo padrão da página da Bammies)."""
import sys, pathlib, shutil, urllib.parse
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sistema

ROOT = pathlib.Path(sys.argv[1]); HERE = pathlib.Path(__file__).parent
(ROOT / "review").mkdir(parents=True, exist_ok=True)
for f in (HERE / "review").glob("*.webp"): shutil.copy(f, ROOT / "review" / f.name)
sistema.CHANGES.clear(); sistema.build((HERE / "src/assets/css/site.css").read_text())
n = len(sistema.CHANGES)

WHATS = "https://wa.me/5511956299380?text=" + urllib.parse.quote("thiago, vi os ajustes da andante. ")

def phone(v, letra, nome):
    return f'''<figure class="version">
          <figcaption><b>Versão {letra}</b> {nome}</figcaption>
          <div class="stage-box">
            <div class="phone"><div class="screen"><iframe src="/andante/{v}/" title="Site da Andante, versão {letra}, {nome}" loading="lazy"></iframe></div></div>
            <p class="hint">Role e toque dentro do celular.</p>
          </div>
          <a class="btn-ink" href="/andante/{v}/" target="_blank" rel="noopener"><span>Abrir a versão {letra}</span><span class="arw" aria-hidden="true"></span></a>
        </figure>'''

def shot(v, letra, nome):
    return f'''<figure class="version">
          <figcaption><b>Versão {letra}</b> {nome}</figcaption>
          <a class="shot" href="/andante/{v}/" target="_blank" rel="noopener" aria-label="Abrir a versão {letra} no computador"><img src="/andante/review/{v}-1440.webp" width="1440" height="2000" alt="Início do site da Andante na versão {letra}, numa tela de computador" loading="lazy" decoding="async"></a>
        </figure>'''


ICONS = {
  "tipo":    "M1.5 13 3.75 7.75 6 13M2.4 11h2.7M8 13l3-9.25 3 9.25M9.1 9.75h3.8",
  "botao":   "M1.75 4.75h12.5v6.5H1.75zM5 8h6",
  "ritmo":   "M2 2.75h12M2 13.25h12M8 5.25v5.5M6.25 7 8 5.25 9.75 7M6.25 9 8 10.75 9.75 9",
  "topo":    "M1.75 2.75h12.5v10.5H1.75zM1.75 5.75h12.5M8.5 4.25h4",
  "rodape":  "M1.75 2.75h12.5v10.5H1.75zM1.75 10.25h12.5M4 11.75h2.5M8.5 11.75h2.5",
  "contato": "M2 3h12v7.5H7.25L4 13.25V10.5H2z",
  "todos":   "M1.25 4.25h13.5v7.5H1.25zM3.5 6.75h1M6 6.75h1M8.5 6.75h1M11 6.75h1.5M4.5 9.25h7",
  "rapido":  "M9.25 1.5 3.5 9h4.25L6.75 14.5 12.5 7H8.25z",
  "achar":   "M6.75 3.5h-4v9.75H12.5v-4M9.5 2.75h3.75V6.5M13 3 7.5 8.5",
  "cor":     "M8 1.75a6.25 6.25 0 1 0 0 12.5V1.75zM8 1.75a6.25 6.25 0 0 1 0 12.5",
  "lista":   "M5.5 3.75h9M5.5 8h9M5.5 12.25h9M1.75 3.75h1.5M1.75 8h1.5M1.75 12.25h1.5",
  "carrossel": "M4.25 3.25h7.5v9.5h-7.5zM1.5 4.75v6.5M14.5 4.75v6.5",
  "aviso":   "M8 1.75 14.75 13.75H1.25zM8 6v3.75M8 11.25v1",
}
def ico_css():
    import urllib.parse
    out = []
    for k, d in ICONS.items():
        svg = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><path d='{d}' fill='none' stroke='#000' stroke-width='1.5' stroke-linecap='square'/></svg>"
        out.append(f'.ico--{k}{{--i:url("data:image/svg+xml,{urllib.parse.quote(svg)}")}}')
    return "\n".join(out)

MUDA = [
  ("tipo", "Títulos que crescem com a tela",
   "No computador, os títulos ganham tamanho e o texto fica mais confortável de ler. No celular, tudo continua do tamanho certo."),
  ("botao", "Botões mais fáceis de ler e de tocar",
   "O botão é onde a pessoa decide reservar. Na Vitamina ele é maior, com a letra do tamanho do texto, e num vermelho um pouco mais fechado, que deixa o branco legível pra todo mundo."),
  ("ritmo", "Mais respiro entre os blocos",
   "Os espaços seguem uma régua só. A página fica com o mesmo ritmo do começo ao fim, e cada página nova já nasce no mesmo padrão."),
  ("topo", "Menu sempre à vista no computador",
   "Na Vitamina, as seções e o botão de reserva ficam no topo da tela, sem precisar abrir o menu."),
  ("rodape", "Rodapé que leva às viagens",
   "Quem chega no fim da página encontra as viagens ali mesmo. E esses links ajudam o Google a achar cada viagem."),
  ("contato", "Um convite pra conversar",
   "No fim da Vitamina tem um bloco pra falar com vocês pelo WhatsApp. Na original, o contato fica só nos botões dos grupos."),
]

AMBAS = [
  ("todos", "Todo mundo consegue usar", ["Dá pra navegar só pelo teclado.", "Quem usa leitor de tela ouve a página na ordem certa, com a descrição de cada foto."]),
  ("rapido", "Abre rápido em qualquer tela", ["As fotos vêm leves e no tamanho de cada tela, pra abrir bem no 4G.", "Nada escapa pros lados, do celular pequeno ao computador."]),
  ("achar", "Fácil de achar e de compartilhar", ["Quando alguém manda o link no WhatsApp, aparece uma prévia com foto e título, como esta aqui.", "O Google recebe o nome, a descrição e os dados de cada viagem.", "O site tem ícone próprio na aba do navegador e no celular."]),
]

PASSOS = [  # (quando, o que acontece, o que falta de vocês)
  ("Agora", "Você confere os ajustes desta rodada.", ["Acesso à Hostinger, hoje (26/11), pelo compartilhamento de conta para designdasilva@gmail.com"]),
  ("Esta semana", "Textos e fotos do País Basco: recebidos, obrigado.", ["WhatsApp e telefone da Andante, para os botões de reserva e o rodapé"]),
  ("Em seguida", "Peru e Gaga e Piemonte.", ["Datas, vagas, preço, hotéis e nomes de quem conduz (o que está entre colchetes)"]),
  ("Até 2/12", "Ajustes da revisão.", ["Fotos em alta do País Basco e fotos sem marca d\u2019água para a home e as capas", "Valor do suplemento de quarto individual do País Basco"]),
  ("3/12", "Domínio e site na Hostinger de vocês.", ["Apontar o domínio para a Hostinger, ou me dizer onde ele está registrado"]),
  ("4/12", "Site no ar.", []),
]

AJUSTES = [
  ("botao", "cta", "Um botão mais calmo", "Pedido do Tiago",
   "O vermelho cheio gritava na página. Agora o botão usa um vermelho mais fechado, da mesma família da marca. Em fundo escuro, ele ganha o contorno no vermelho do logo, pra não se perder no preto.",
   "Texto branco sobre o vermelho antigo: 4,8:1, perto do mínimo. Sobre o novo: 7,9:1, o nível mais alto da norma de acessibilidade. Mais calmo e mais fácil de ler."),
  ("contato", "fale", "WhatsApp sempre à mão", "Pedido do Tiago",
   "Um botão fixo no canto da tela abre a conversa de qualquer ponto do site. Ele sai de cena quando já tem outro botão de WhatsApp à vista, pra não repetir. O rodapé ganhou WhatsApp e telefone.",
   "No celular, o botão tem 64px, acima dos 44px recomendados para o toque, e quem usa leitor de tela ouve \u201cFalar com a Andante no WhatsApp\u201d."),
  ("cor", "roteiro", "Cores mais leves no País Basco", "Pedido do Tiago",
   "Entrou a paleta que você testou: azul acinzentado, areia, grafite e ferrugem. Dois tons foram afinados para o texto continuar fácil de ler, e a tabela logo abaixo mostra o porquê.",
   ""),
  ("lista", "perfis", "\u201cPara quem é\u201d em lista", "Pedido do Tiago",
   "É o trecho em que a pessoa se reconhece na viagem. Em lista, os quatro perfis aparecem de uma vez. Num carrossel, só o primeiro fica à vista e os outros dependem de a pessoa arrastar.",
   ""),
  ("carrossel", "hoteis", "Hotéis e bikes em carrossel", "Pedido do Tiago",
   "Aqui o carrossel faz sentido: são fotos, na ordem da viagem, e a página fica bem mais curta no celular. O próximo card aparece na borda e o contador mostra quantos faltam. As fotos provisórias deram lugar às fotos que você mandou.",
   "Funciona também pelo teclado. No computador, os cards voltam a ficar lado a lado."),
  ("tipo", "hero", "Uma frase só no título", "Conversa com o Lucas",
   "O título volta à quebra do desenho do Lucas, \u201cO que interessa / é o TEMPO / VIVIDO\u201d, em que a serifada e a caixa alta dividem a mesma linha. E ficou cerca de 20% menor, mais delicado.",
   "A quebra é escrita à mão para cada tamanho de tela, então o título não se desmonta em blocos soltos."),
  ("ritmo", "faixa", "Respiro na abertura", "Conversa com o Lucas",
   "No computador, a faixa preta logo depois da foto ganhou espaço em cima e embaixo, e a frase voltou a um tamanho mais delicado. É a entrada do site, e agora ela respira antes da próxima faixa.",
   "No celular, a faixa já seguia o desenho do Lucas e ficou como estava."),
]

CONTRASTE = [
  ("Nome do hotel no roteiro", "#B97A4F", "#29302F", "3,8:1", "#E6B48C", "#29302F", "7,2:1",
   "Era texto pequeno abaixo do mínimo de 4,5:1. O cobre ficou um pouco mais claro."),
  ("Texto branco na faixa ferrugem", "#FFFFFF", "#8A4A2C", "6,8:1", "#FFFFFF", "#82442A", "7,5:1",
   "Passava do mínimo, mas não do nível alto. Um tom mais escuro, quase igual a olho."),
  ("Botão de reserva no fundo preto", "#381E23", "#000000", "1,4:1", "#9E1F17", "#000000", "contorno 4,7:1",
   "O vinho escuro quase some no preto. Um botão precisa se destacar do fundo em pelo menos 3:1. Ficou o vermelho fechado, com o contorno da marca."),
]
MANTIDAS = [("Preto sobre azul acinzentado", "#000000", "#8EA8AB", "8,3:1"), ("Preto sobre areia", "#000000", "#D0B776", "10,7:1"), ("Branco sobre grafite", "#FFFFFF", "#29302F", "13,5:1")]

def chip(fg, bg, r):
    return f'<span class="chip" style="color:{fg};background:{bg}" aria-hidden="true"></span><span class="ratio">{r}</span>'

def contraste():
    rows = "".join(f'''<tr><th scope="row">{n}<small>{why}</small></th>
      <td><span class="cell">{chip(f1, b1, r1)}</span><span class="sr">antes, {r1}</span></td>
      <td><span class="cell">{chip(f2, b2, r2)}</span><span class="sr">depois, {r2}</span></td></tr>''' for n, f1, b1, r1, f2, b2, r2, why in CONTRASTE)
    keep = "".join(f'<li><span class="cell">{chip(f, b, r)}</span>{n}</li>' for n, f, b, r in MANTIDAS)
    return f'''<div class="contrast">
      <h3 class="sub">Por que mexemos no contraste</h3>
      <p class="contrast__lead">A norma internacional de acessibilidade (WCAG) mede o contraste entre o texto e o fundo. O mínimo para texto comum é 4,5:1, e o nível mais alto, que usamos no site todo, é 7:1. Isso não ajuda só quem enxerga pouco: é o que faz o texto ler bem no celular, na rua, com sol na tela.</p>
      <table><thead><tr><th scope="col">Onde</th><th scope="col">Antes</th><th scope="col">Depois</th></tr></thead><tbody>{rows}</tbody></table>
      <p class="contrast__keep">Já estavam ótimas e ficaram como você testou:</p>
      <ul class="contrast__list">{keep}</ul>
    </div>'''

def ajuste(i, ico, key, titulo, quem, texto, tec):
    extra = f'<p class="tec">{tec}</p>' if tec else ""
    return f'''<article class="change grid">
          <div class="change__text"><span class="num"><span class="ico ico--{ico}" aria-hidden="true"></span>{i} · {quem}</span><h3>{titulo}</h3><p>{texto}</p>{extra}</div>
          <div class="change__pair">
            <figure><figcaption>Antes</figcaption><img src="/andante/review/a-{key}-a.webp" alt="{titulo}, antes" loading="lazy" decoding="async"></figure>
            <figure><figcaption>Depois</figcaption><img src="/andante/review/a-{key}-b.webp" alt="{titulo}, depois" loading="lazy" decoding="async"></figure>
          </div>
        </article>''' + (contraste() if ico == "cor" else "")

def muda(i, key, titulo, texto):
    a = (f'<img src="/andante/review/c-{key}-a.webp" alt="{titulo}, versão original" loading="lazy" decoding="async">'
         if key != "contato" else '<div class="none">A versão original não tem esse bloco.</div>')
    return f'''<article class="change grid">
          <div class="change__text"><span class="num"><span class="ico ico--{key}" aria-hidden="true"></span>{i}</span><h3>{titulo}</h3><p>{texto}</p></div>
          <div class="change__pair">
            <figure><figcaption>Versão original</figcaption>{a}</figure>
            <figure><figcaption>Versão Vitamina</figcaption><img src="/andante/review/c-{key}-b.webp" alt="{titulo}, versão Vitamina" loading="lazy" decoding="async"></figure>
          </div>
        </article>'''

html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#FFFFFF">
<title>Andante · versão original e versão Vitamina · Thiago Vitamina</title>
<meta name="description" content="O site da Andante em duas versões lado a lado, para escolher juntos.">
<meta property="og:title" content="Andante · versão original e versão Vitamina">
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
@media (max-width:1100px){{:root{{--t-2xl:56px;--t-xl:36px}} .timeline{{grid-template-columns:repeat(3,minmax(0,1fr))}} .group{{grid-column:span 6}}}}
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

/* ícones: máscara SVG, um traço só, do tamanho do texto */
.ico{{display:inline-block;width:1em;height:1em;flex:none;background:currentColor;-webkit-mask:var(--i) center/contain no-repeat;mask:var(--i) center/contain no-repeat}}
{ico_css()}

/* o que muda */
.change{{row-gap:var(--sp-4);align-items:start;padding-block:var(--sp-5);border-top:1px solid var(--rule)}}
.change:first-of-type{{border-top:0;padding-top:0}}
.change__text{{grid-column:1 / span 4;display:flex;flex-direction:column;gap:var(--sp-3);max-width:40ch}}
.change__text .num{{display:flex;align-items:center;gap:var(--sp-3);font-size:var(--t-sm);color:var(--mute)}}
.change__text .num .ico{{font-size:var(--t-lg);color:var(--ink)}}
.change__text h3{{font-family:var(--display);font-weight:600;font-size:var(--t-lg);line-height:1.15;letter-spacing:-.012em;text-wrap:balance}}
.change__text p{{font-size:var(--t-md);line-height:1.45;text-wrap:pretty}}
.change__pair{{grid-column:5 / span 8;display:grid;grid-template-columns:1fr 1fr;gap:var(--sp-3);align-items:start}}
.change__pair figure{{display:flex;flex-direction:column;gap:var(--sp-2);min-width:0}}
.change__pair figcaption{{font-size:var(--t-sm);color:var(--mute)}}
.change__pair img{{width:100%;border:1px solid var(--rule)}}
.none{{display:grid;place-items:center;aspect-ratio:1000/276;background:var(--well);color:var(--mute);font-size:var(--t-sm);text-align:center;padding:var(--sp-3)}}

/* ajustes desta rodada */
.tec{{font-size:var(--t-base)!important;color:var(--mute);border-left:2px solid var(--plum);padding-left:var(--sp-3)}}
.contrast{{padding-block:var(--sp-5);border-top:1px solid var(--rule)}}
.contrast .sub{{margin-top:0}}
.contrast__lead{{font-size:var(--t-md);line-height:1.45;max-width:52ch;margin-bottom:var(--sp-5)}}
.contrast table{{width:100%;border-collapse:collapse}}
.contrast th,.contrast td{{text-align:left;vertical-align:top;padding:var(--sp-3) var(--sp-3) var(--sp-3) 0;border-top:1px solid var(--rule)}}
.contrast thead th{{font-size:var(--t-sm);color:var(--mute);font-weight:400;border-top:0}}
.contrast tbody th{{font-weight:600;width:50%}}
.contrast tbody th small{{display:block;font-weight:400;font-size:var(--t-sm);color:var(--mute);margin-top:var(--sp-1);max-width:44ch}}
.cell{{display:inline-flex;align-items:center;gap:var(--sp-2)}}
.chip::before{{content:"Aa"}}
.chip{{display:inline-grid;place-items:center;width:48px;height:48px;font-family:var(--display);font-weight:600;font-size:20px;border:1px solid var(--rule)}}
.ratio{{font-family:var(--display);font-weight:600;font-size:var(--t-md)}}
.sr{{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}}
.contrast__keep{{margin-top:var(--sp-5);color:var(--mute)}}
.contrast__list{{list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:var(--sp-3) var(--sp-5);margin-top:var(--sp-3)}}
.contrast__list li{{display:flex;align-items:center;gap:var(--sp-3)}}
@media (max-width:820px){{.contrast tbody th{{width:auto}}.chip{{width:40px;height:40px;font-size:16px}}.ratio{{font-size:var(--t-base)}}.contrast th,.contrast td{{padding-right:var(--sp-2)}}}}

/* nas duas */
.groups{{row-gap:var(--sp-5);align-items:start}}
.group{{grid-column:span 4;display:flex;flex-direction:column;gap:var(--sp-3);border-top:2px solid var(--ink);padding-top:var(--sp-3)}}
.group h3{{display:flex;flex-direction:column;gap:var(--sp-3);font-family:var(--display);font-weight:600;font-size:var(--t-md);line-height:1.2}}
.group h3 .ico{{font-size:var(--t-lg)}}
.group ul{{padding-left:var(--sp-4);display:flex;flex-direction:column;gap:var(--sp-2)}}
.group li{{text-wrap:pretty}}
.share{{margin-top:var(--sp-2);max-width:340px;background:#E7F6E3;border-radius:12px;padding:6px;font-size:var(--t-sm);line-height:1.35}}
.share img{{border-radius:8px 8px 0 0}}
.share div{{background:rgba(0,0,0,.05);border-radius:0 0 8px 8px;padding:var(--sp-2) var(--sp-3)}}
.share b{{display:block}}
.share small{{color:var(--mute)}}
.share p{{padding:var(--sp-2) var(--sp-2) 2px;color:var(--plum);text-decoration:underline}}

/* próximos passos */
.timeline{{list-style:none;padding:0;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:var(--gap)}}
.timeline li{{display:flex;flex-direction:column;gap:var(--sp-2);border-top:2px solid var(--rule);padding-top:var(--sp-3)}}
.timeline li:first-child{{border-top-color:var(--ink)}}
.timeline b{{font-family:var(--display);font-weight:600;font-size:var(--t-md)}}
.timeline span{{text-wrap:pretty}}
/* o que falta: um toque de laranja de aviso, pedido do Thiago (exceção à regra de cor única, só nesta página) */
.timeline li.is-pending{{border-top-color:#FF7A1A}}
.timeline li:first-child.is-pending{{border-top-color:#FF7A1A}}
.need{{margin-top:var(--sp-2);background:#FFEBDB;padding:var(--sp-3);display:flex;flex-direction:column;gap:var(--sp-2)}}
.need__tag{{display:inline-flex;align-self:flex-start;align-items:center;gap:var(--sp-1);background:#FF7A1A;color:var(--ink);font-size:var(--t-sm);font-weight:600;line-height:1;padding:6px 8px}}
.need__tag .ico{{font-size:14px}}
.need ul{{list-style:none;padding:0;display:flex;flex-direction:column;gap:var(--sp-2);font-size:var(--t-sm);line-height:1.4}}
.need li{{border:0!important;padding:0!important;display:block!important}}
/* todas as caixas com o mesmo tamanho e começando na mesma altura */
@media (min-width:821px){{.timeline{{grid-template-rows:auto auto 1fr}}.timeline>li{{display:grid;grid-row:span 3;grid-template-rows:subgrid;align-content:start}}.timeline>li>.need{{margin-top:var(--sp-2);height:100%}}}}
@media (min-width:821px) and (max-width:1100px){{.timeline{{grid-template-columns:repeat(3,minmax(0,1fr));row-gap:var(--sp-5)}}}}
.need ul{{overflow-wrap:anywhere}}
.ask{{display:flex;flex-wrap:wrap;align-items:center;gap:var(--sp-4);margin-top:var(--sp-6);padding-top:var(--sp-5);border-top:1px solid var(--rule)}}
.ask p{{font-family:var(--display);font-size:var(--t-lg);line-height:1.25;letter-spacing:-.012em;max-width:30ch}}

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
  .change__pair{{grid-template-columns:1fr;gap:var(--sp-4)}}
  .timeline{{grid-template-columns:1fr}}
  .timeline li{{display:grid;grid-template-columns:96px 1fr;gap:var(--sp-3)}} .timeline .need{{grid-column:2}}
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
      <a href="#ajustes"><span>1</span>Ajustes</a>
      <a href="#lado"><span>2</span>Lado a lado</a>
      <a href="#muda"><span>3</span>O que muda</a>
      <a href="#passos"><span>4</span>Próximos passos</a>
    </nav>
  </div>
</header>

<main id="main">

  <section class="wrap opening grid" aria-labelledby="h-top">
    <h1 id="h-top">Andante, em duas versões. <span>O mesmo site, pra escolher juntos.</span></h1>
    <p class="lead">A versão original é o desenho do Lucas, do jeito que ele fez. A Vitamina é a mesma página com um sistema de tipografia, espaçamento e grid, e ajustes de leitura e de toque. O conteúdo e as fotos são os mesmos nas duas.</p>
  </section>

  <section class="part" id="ajustes" aria-labelledby="h-ajustes">
    <div class="wrap">
      <div class="head grid">
        <h2 id="h-ajustes">1 · Ajustes desta rodada</h2>
        <p>O que mudou na versão Vitamina depois da nossa conversa de 25/11. Em cada um, o mesmo pedaço do site antes e depois, e o motivo técnico quando ele existe.</p>
      </div>
      {"".join(ajuste(i, *a) for i, a in enumerate(AJUSTES, 1))}
    </div>
  </section>

  <section class="part" id="lado" aria-labelledby="h-lado">
    <div class="wrap">
      <div class="head grid">
        <h2 id="h-lado">2 · Lado a lado</h2>
        <p>As duas funcionam de verdade. Dá pra rolar, abrir o menu e entrar nas viagens dentro de cada celular.</p>
      </div>
      <div class="pair">
        {phone("original", "original", "o desenho do Lucas")}
        {phone("vitamina", "Vitamina", "com o sistema e os ajustes")}
      </div>
      <h3 class="sub">No computador</h3>
      <div class="pair">
        {shot("original", "original", "o desenho do Lucas")}
        {shot("vitamina", "Vitamina", "com o sistema e os ajustes")}
      </div>
    </div>
  </section>

  <section class="part" id="muda" aria-labelledby="h-muda">
    <div class="wrap">
      <div class="head grid">
        <h2 id="h-muda">3 · O que muda na Vitamina</h2>
        <p>Seis mudanças. Em cada uma, o mesmo pedaço do site nas duas versões.</p>
      </div>
      {"".join(muda(i, *m) for i, m in enumerate(MUDA, 1))}
      <h3 class="sub">E o que já vem nas duas</h3>
      <div class="groups grid">
        {"".join(f'<div class="group"><h3><span class="ico ico--{k}" aria-hidden="true"></span>{t}</h3><ul>{"".join(f"<li>{x}</li>" for x in itens)}</ul>' + ('<div class="share"><img src="/andante/vitamina/assets/og/inicio.jpg" width="1200" height="630" alt="Imagem de prévia da Andante: foto do lago com o logo e o título O que interessa é o tempo vivido" loading="lazy"><div><b>Andante · Viagens bem vividas</b><small>Viagens em pequenos grupos</small></div></div>' if i == 2 else "") + "</div>" for i, (k, t, itens) in enumerate(AMBAS))}
      </div>
    </div>
  </section>

  <section class="part" id="passos" aria-labelledby="h-passos">
    <div class="wrap">
      <div class="head grid">
        <h2 id="h-passos">4 · Próximos passos</h2>
        <p>Até o site no ar. O que estiver entre colchetes é provisório e entra quando o conteúdo chegar.</p>
      </div>
      <ol class="timeline">
        {"".join(f'<li{" class=is-pending" if f else ""}><b>{d}</b><span>{t}</span>' + (f'<div class="need"><p class="need__tag"><span class="ico ico--aviso" aria-hidden="true"></span>Falta de vocês</p><ul>{"".join(f"<li>{x}</li>" for x in f)}</ul></div>' if f else "") + "</li>" for d, t, f in PASSOS)}
      </ol>
      <div class="ask">
        <p>Conferiu os ajustes? Me conta o que achou.</p>
        <a class="btn-ink" href="{WHATS}" target="_blank" rel="noopener"><span>Responder no WhatsApp</span><span class="arw" aria-hidden="true"></span></a>
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
