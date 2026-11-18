"""Página de revisão em /andante: as duas versões lado a lado e o que muda entre elas."""
import sys, pathlib, shutil
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sistema

ROOT = pathlib.Path(sys.argv[1]); HERE = pathlib.Path(__file__).parent
(ROOT / "review").mkdir(parents=True, exist_ok=True)
for f in (HERE / "review").glob("*.webp"): shutil.copy(f, ROOT / "review" / f.name)
shutil.copy(ROOT / "original/favicon.ico", ROOT / "favicon.ico")
sistema.CHANGES.clear(); sistema.build((HERE / "src/assets/css/site.css").read_text())
n = len(sistema.CHANGES)

def par(w, alt):
    return "".join(
        f'<figure><figcaption>{nome}</figcaption><a href="/andante/{v}/">'
        f'<img src="/andante/review/{v}-{w}.webp" alt="{alt} na {nome.lower()}" loading="lazy" decoding="async"></a></figure>'
        for v, nome in (("original", "Versão original"), ("vitamina", "Versão Vitamina")))

ESCALA = [("Legenda", "14", "14"), ("Texto e botões", "16", "18"), ("Destaque", "20", "22"),
          ("Título pequeno", "24", "28"), ("Título de seção", "32", "48"),
          ("Título grande", "40", "64"), ("Abertura", "52", "88")]

html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>Andante · duas versões para revisão</title>
<link rel="icon" href="/andante/favicon.ico" sizes="32x32">
<link rel="icon" href="/andante/original/assets/icons/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/andante/original/assets/css/fonts.css">
<style>
*,*::before,*::after{{box-sizing:border-box}}
body{{margin:0;font-family:Outfit,system-ui,sans-serif;font-size:16px;line-height:1.5;color:#000;background:#fff;-webkit-font-smoothing:antialiased}}
h1,h2,h3,p,ul,figure{{margin:0}}
a{{color:inherit;text-underline-offset:.2em}}
:focus-visible{{outline:2px solid #f00000;outline-offset:3px}}
.wrap{{max-width:1440px;margin:0 auto;padding:0 20px}}
header{{background:#000;color:#fff;padding:48px 0 64px}}
.serif{{font-family:'Instrument Serif',Georgia,serif;font-weight:400}}
h1{{font-size:40px;line-height:1.05;margin-top:16px}}
.lead{{font-size:20px;line-height:1.4;max-width:40ch;margin-top:24px}}
.open{{display:flex;flex-wrap:wrap;gap:16px;margin-top:32px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;min-height:52px;padding:0 32px;font-weight:500;text-decoration:none;border:1px solid #f00000}}
.btn--solid{{background:#e60000;border-color:#e60000;color:#fff}}
section{{padding:64px 0;border-top:1px solid #e3e3e3}}
h2{{font-size:32px;line-height:1.15;font-weight:600}}
h2+p{{margin-top:16px;max-width:60ch}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:32px}}
.pair figure{{display:flex;flex-direction:column;gap:8px}}
figcaption{{font-size:14px;font-weight:500}}
.pair img{{display:block;width:100%;height:auto;border:1px solid #e3e3e3}}
.cols{{display:grid;gap:48px;margin-top:32px}}
h3{{font-size:20px;line-height:1.3;font-weight:600}}
ul{{margin-top:16px;padding-left:20px;display:flex;flex-direction:column;gap:8px;max-width:60ch}}
table{{margin-top:16px;border-collapse:collapse;width:100%;max-width:520px}}
th,td{{text-align:left;padding:8px 16px 8px 0;border-bottom:1px solid #e3e3e3}}
th{{font-size:14px;font-weight:500}}
td+td,th+th{{width:96px}}
.note{{font-size:14px;color:#545454;margin-top:16px;max-width:60ch}}
@media (min-width:820px){{
  .wrap{{padding:0 40px}}
  h1{{font-size:64px}}
  .cols{{grid-template-columns:1fr 1fr;gap:64px}}
  .pair--mobile{{max-width:900px}}
}}
@media (min-width:1100px){{ .wrap{{padding:0 64px}} section{{padding:104px 0}} h2{{font-size:48px}} }}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <p>Andante · revisão de 18/11</p>
    <h1>Duas versões do site, <span class="serif"><i>para escolher juntos</i></span></h1>
    <p class="lead">A versão original segue o mobile do Figma. A versão Vitamina é o mesmo site com um sistema de tipografia, espaçamento e grid aplicado em todas as telas. O conteúdo, as cores e as fotos são os mesmos nas duas.</p>
    <div class="open">
      <a class="btn btn--solid" href="/andante/original/">Abrir a versão original</a>
      <a class="btn" href="/andante/vitamina/">Abrir a versão Vitamina</a>
    </div>
  </div>
</header>
<main>
<section aria-labelledby="t-mobile">
  <div class="wrap">
    <h2 id="t-mobile">No celular</h2>
    <p>O início da página em 390px de largura, o tamanho de um iPhone.</p>
    <div class="pair pair--mobile">{par(390, "Início da página no celular")}</div>
  </div>
</section>
<section aria-labelledby="t-desktop">
  <div class="wrap">
    <h2 id="t-desktop">No computador</h2>
    <p>O início da página em 1440px de largura.</p>
    <div class="pair">{par(1440, "Início da página no computador")}</div>
  </div>
</section>
<section aria-labelledby="t-muda">
  <div class="wrap">
    <h2 id="t-muda">O que muda na versão Vitamina</h2>
    <p>Hoje o site tem medidas escritas uma a uma, copiadas do desenho. A versão Vitamina troca essas medidas por poucas regras que valem para o site inteiro. Assim, cada página nova já nasce no mesmo ritmo, sem precisar desenhar tudo de novo. Foram {n} medidas ajustadas.</p>
    <div class="cols">
      <div>
        <h3>Tipografia em 7 tamanhos</h3>
        <table>
          <thead><tr><th scope="col">Uso</th><th scope="col">Celular</th><th scope="col">Computador</th></tr></thead>
          <tbody>{"".join(f"<tr><td>{u}</td><td>{m}</td><td>{d}</td></tr>" for u, m, d in ESCALA)}</tbody>
        </table>
        <p class="note">Antes eram 15 tamanhos escritos à mão, fora de uma escala. Valores em pixels.</p>
      </div>
      <div>
        <h3>Botões maiores</h3>
        <ul>
          <li>O texto dos botões passa do tamanho de legenda para o tamanho do texto corrido: 16px no celular e 18px no computador.</li>
          <li>A altura passa de 44px para 52px no celular e 56px no computador.</li>
          <li>É o ponto em que a pessoa decide reservar, então ele precisa ser lido sem esforço.</li>
        </ul>
        <h3 style="margin-top:48px">Espaçamento e grid</h3>
        <ul>
          <li>Todo espaço entre elementos sai de uma escala só: 4, 8, 16, 24, 32, 48, 64 e 104px.</li>
          <li>Grid de 4 colunas no celular, 8 no tablet e 12 no computador, com a mesma calha em todas as seções.</li>
          <li>As entrelinhas seguem uma grade de 4px, o que deixa os blocos de texto mais alinhados entre si.</li>
        </ul>
      </div>
    </div>
  </div>
</section>
<section aria-labelledby="t-ambas">
  <div class="wrap">
    <h2 id="t-ambas">O que já vale para as duas</h2>
    <p>Isso não muda o desenho. É o mínimo para o site funcionar bem para todo mundo e aparecer no Google.</p>
    <ul>
      <li>O vermelho do botão ficou um tom mais fechado (#e60000) para o texto branco ter contraste suficiente. No #f00000 ele fica abaixo do mínimo de leitura.</li>
      <li>Todo link e botão tem pelo menos 44px de área de toque.</li>
      <li>Navegação completa pelo teclado, com o foco sempre visível, e menu que fecha com Esc.</li>
      <li>Leitura correta por leitor de tela (VoiceOver), com descrição em todas as fotos.</li>
      <li>Fotos em formato leve e no tamanho certo para cada tela, para a página abrir rápido no 4G.</li>
      <li>Testado em 320, 390, 820, 1100 e 1440px de largura, sem rolagem para os lados.</li>
      <li>Ícone do site na aba do navegador e na tela inicial do celular.</li>
      <li>Em seguida: SEO, prévia de compartilhamento no WhatsApp e nas redes, e medição de visitas.</li>
    </ul>
  </div>
</section>
</main>
</body>
</html>
"""
(ROOT / "index.html").write_text(html)
print("comparar →", ROOT / "index.html", f"({n} medidas)")
