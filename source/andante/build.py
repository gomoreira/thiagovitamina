"""Gera o site da Andante: páginas fixas + uma página por viagem a partir de src/data/viagens/*.json.
Preview: thiagovitamina.com/andante (noindex). Produção: Cloudflare Pages com BASE=""."""
import json, os, pathlib, shutil
ROOT = pathlib.Path(__file__).parent; SRC = ROOT / "src"
OUT = pathlib.Path(os.environ.get("ANDANTE_OUT", ROOT.parent.parent / "andante"))
BASE = os.environ.get("ANDANTE_BASE", "/andante")
PREVIEW = BASE != ""
if OUT.exists(): shutil.rmtree(OUT)
shutil.copytree(SRC / "assets", OUT / "assets")

site = json.loads((SRC / "data/site.json").read_text())
viagens = [json.loads(p.read_text()) for p in sorted((SRC / "data/viagens").glob("*.json"))]
tpl = (SRC / "templates/base.html").read_text()
logo = (SRC / "partials/logo.svg").read_text().strip()
arrow = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 12h17M14 6l6 6-6 6"/></svg>'
burger = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M2 6h20M2 12h20M2 18h20"/></svg>'
xmark = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 4l16 16M20 4L4 20"/></svg>'
home = f"{BASE}/"
NAV = [("Home", home, "home"), ("Por que viajar", f"{home}#por-que-viajar", ""), ("Grupos", f"{home}#grupos", ""),
       ("Quem somos", f"{home}#quem-somos", ""), ("Contato", f"{home}#contato", "")]

def header(current):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if k and k == current else ""}>{t}</a>' for t, h, k in NAV[1:])
    return f'''<header class="header" data-inert-when-menu><div class="wrap header__bar">
<button class="header__menu" type="button" data-menu-open aria-expanded="false" aria-controls="menu" aria-label="Abrir menu">{burger}</button>
<a class="header__logo" href="{home}" aria-label="Andante, página inicial">{logo}</a>
<nav class="header__nav" aria-label="Principal">{links}</nav>
<a class="btn btn--solid header__cta" href="{home}#grupos">Reserve seu lugar</a>
</div></header>'''

def menu(current):
    items = "".join(f'<li><a href="{h}"{" aria-current=\"page\"" if k and k == current else ""}>{t}{arrow}</a></li>' for t, h, k in NAV)
    return f'''<div class="menu" id="menu" role="dialog" aria-modal="true" aria-label="Menu" hidden><div class="wrap menu__inner">
<div class="menu__top"><button class="menu__close" type="button" data-menu-close aria-label="Fechar menu">{xmark}</button>
<a class="header__logo" href="{home}" aria-label="Andante, página inicial">{logo}</a></div>
<div class="menu__box"><p class="menu__label" aria-hidden="true">Menu</p>
<nav aria-label="Menu principal"><ul class="menu__list" role="list">{items}</ul></nav></div>
<div class="menu__ctas"><a class="btn btn--solid" href="{home}#grupos">Reserve seu lugar</a><a class="btn btn--line" href="{home}#contato">Faça parte</a></div>
<div class="menu__foot"><p class="tagline"><b>{site["tagline_b"]}</b> <i>{site["tagline_i"]}</i></p></div>
</div></div>'''

def footer():
    trips = "".join(f'<a href="{BASE}/viagens/{v["slug"]}/">{v["titulo"]}</a>' for v in viagens)
    return f'''<footer class="footer" data-inert-when-menu><div class="wrap">
<div class="footer__top"><a class="footer__logo" href="{home}" aria-label="Andante, página inicial">{logo}</a>
<nav class="footer__nav" aria-label="Rodapé">
<div class="footer__col"><h2>Viagens</h2><a href="{home}#grupos">Grupos</a>{trips}</div>
<div class="footer__col"><h2>Andante</h2><a href="{home}">Home</a><a href="{home}#por-que-viajar">Por que viajar</a><a href="{home}#quem-somos">Quem somos</a><a href="{home}#contato">Faça parte</a></div>
<div class="footer__col"><h2>Ajuda</h2><a href="{home}#contato">Contato</a></div>
</nav></div>
<p class="footer__tag tagline"><b>{site["tagline_b"]}</b> <i>{site["tagline_i"]}</i></p>
<p class="footer__copy">© Andante</p>
</div></footer>'''

def page(path, title, content, current="", description=site["descricao"]):
    html = tpl
    for k, v in {"title": title, "description": description, "base": BASE, "content": content,
                 "robots": '<meta name="robots" content="noindex, nofollow">' if PREVIEW else "",
                 "header": header(current), "menu": menu(current), "footer": footer()}.items():
        html = html.replace("{{" + k + "}}", v)
    dest = OUT / path / "index.html"; dest.parent.mkdir(parents=True, exist_ok=True); dest.write_text(html)

# Início: estrutura de seções (o conteúdo entra na etapa de construção)
secoes = [("por-que-viajar", "Por que viajar"), ("grupos", "Grupos"), ("quem-somos", "Quem somos"), ("contato", "Contato")]
inicio = '''<section class="on-dark" style="min-height:100svh;display:flex;align-items:flex-end"><div class="wrap" style="padding-bottom:var(--s16)">
<h1 style="font-size:var(--fs-hero);line-height:1;font-weight:400"><span class="serif it">O que interessa<br>é o </span><span class="caps">tempo<br>vivido</span></h1></div></section>''' + "".join(
    f'<section id="{i}" style="padding-block:var(--s16)"><div class="wrap"><h2 class="h2">{t}</h2><span class="rule" aria-hidden="true" style="margin-top:var(--s6)"></span><p style="margin-top:var(--s6)">Em construção.</p></div></section>' for i, t in secoes)
page("", "Andante · Viagens bem vividas", inicio, "home")
for v in viagens:
    c = f'<section class="on-dark" style="min-height:70svh;display:flex;align-items:flex-end"><div class="wrap" style="padding-bottom:var(--s16)"><h1 class="serif" style="font-size:var(--fs-title);line-height:1.05">{v["titulo"]}</h1><p class="small" style="margin-top:var(--s4)">{v["resumo"]}</p></div></section>'
    page(f"viagens/{v['slug']}", f"{v['titulo']} · Andante", c)
print(f"{len(viagens)} viagens:", ", ".join(v["slug"] for v in viagens), "→", OUT)
