"""Gera o site da Andante: páginas fixas + uma página por viagem a partir de src/data/viagens/*.json.
Preview: thiagovitamina.com/andante (noindex). Produção: Cloudflare Pages com BASE=""."""
import json, os, pathlib, shutil
ROOT = pathlib.Path(__file__).parent; SRC = ROOT / "src"
OUT = pathlib.Path(os.environ.get("ANDANTE_OUT", ROOT.parent.parent / "andante"))
BASE = os.environ.get("ANDANTE_BASE", "/andante")
PREVIEW = BASE != ""
if OUT.exists(): shutil.rmtree(OUT)
shutil.copytree(SRC / "assets", OUT / "assets")

# imagens: WebP + JPEG em várias larguras, gerados a partir de src/img/*.jpg
from PIL import Image
WIDTHS = (480, 800, 1200, 1600)
IMGS = {}
(OUT / "assets/img").mkdir(parents=True, exist_ok=True)
for src in sorted((SRC / "img").glob("*.jpg")):
    im = Image.open(src).convert("RGB"); ws = [w for w in WIDTHS if w <= im.width] or [im.width]
    for w in ws:
        r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        r.save(OUT / f"assets/img/{src.stem}-{w}.webp", "WEBP", quality=78, method=6)
        r.save(OUT / f"assets/img/{src.stem}-{w}.jpg", "JPEG", quality=80, optimize=True, progressive=True)
    IMGS[src.stem] = (ws, im.width, im.height)

def img(name, cls="", alt="", loading="lazy", sizes="(min-width:1100px) 50vw, 100vw", pos=""):
    ws, w, h = IMGS[name]
    sset = lambda ext: ", ".join(f"{BASE}/assets/img/{name}-{x}.{ext} {x}w" for x in ws)
    big = ws[-1]; hh = round(h * big / w)
    style = f' style="object-position:{pos}"' if pos else ""
    fetch = ' fetchpriority="high"' if loading == "eager" else ""
    return (f'<picture><source type="image/webp" srcset="{sset("webp")}" sizes="{sizes}">'
            f'<img class="{cls}" src="{BASE}/assets/img/{name}-{ws[min(1,len(ws)-1)]}.jpg" srcset="{sset("jpg")}" sizes="{sizes}" '
            f'width="{big}" height="{hh}" alt="{alt}" loading="{loading}" decoding="async"{fetch}{style}></picture>')

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

import re, urllib.parse
def whatsapp(viagem=None):
    n = re.sub(r"\D", "", site.get("whatsapp", ""))
    if not n: return "#contato"  # número ainda não definido
    msg = f"Oi! Quero saber da viagem {viagem}." if viagem else "Oi! Quero saber dos próximos grupos da Andante."
    return f"https://wa.me/{n}?text={urllib.parse.quote(msg)}"

def card(v):
    acc = "".join(f'<details><summary>{t}</summary><p>{x}</p></details>' for t, x in v["destaques"])
    return (f'<li class="card">{img(v["img"], "card__img", v["img_alt"], sizes="(min-width:1100px) 33vw, (min-width:600px) 50vw, 100vw", pos=v.get("img_pos",""))}'
            f'<div class="card__body"><h3 class="card__title"><a href="{BASE}/viagens/{v["slug"]}/">{v["titulo"]}</a></h3>'
            f'<p class="card__meta">{v["meta"]}</p><div class="acc">{acc}</div>'
            f'<p class="card__cta"><a class="btn btn--solid" href="{whatsapp(v["titulo"])}" data-track="whatsapp" data-viagem="{v["slug"]}">Reserve seu lugar</a></p></div></li>')

viagens.sort(key=lambda v: v.get("ordem", 99))
symbol = (SRC / "partials/symbol.svg").read_text().strip()
inicio = (SRC / "templates/inicio.html").read_text()
inicio = re.sub(r"\{\{img:([^|}]+)\|([^|}]*)\|([^|}]*)(?:\|([^}]*))?\}\}",
                lambda m: img(m[1], m[2], m[3], m[4] or "lazy", sizes="100vw" if m[1] == "hero" else "(min-width:820px) 42vw, 100vw"), inicio)
inicio = inicio.replace("{{symbol}}", symbol).replace("{{cards}}", "".join(card(v) for v in viagens)).replace("{{whatsapp}}", whatsapp())
page("", "Andante · Viagens bem vividas", inicio, "home")
def foto(name, cls, alt, sizes="100vw", pos=""):
    if name and name in IMGS: return img(name, cls, alt, sizes=sizes, pos=pos)
    return f'<div class="ph {cls}" role="img" aria-label="{alt}"><span aria-hidden="true">Foto provisória</span></div>'

def head(label, title, hid):
    return f'<div class="sec-head"><p class="small">{label}</p><h2 class="h2" id="{hid}">{title}</h2><span class="rule" aria-hidden="true"></span></div>'

def ul(items, cls="list"):
    return f'<ul class="{cls}" role="list">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"

LEG = {"bike": '<path d="M0,3 L26,3" stroke="#f00000" stroke-width="3"/>', "van": '<path d="M0,3 L26,3" stroke="#f00000" stroke-width="1.6" stroke-dasharray="4 4"/>', "opcao": '<path d="M0,3 L26,3" stroke="#000" stroke-width="1" stroke-dasharray="2 3"/>'}

def viagem(v):
    h, wa, out = v["hero"], whatsapp(v["titulo"]), []
    out.append(f'''<section class="hero hero--trip on-dark" aria-labelledby="t-titulo">{img(h["img"], "hero__img", h["alt"], "eager", sizes="100vw")}
<div class="wrap hero__wrap"><div class="hero__frame" aria-hidden="true"></div>
<div class="hero__title"><nav class="crumb small" aria-label="Você está em"><a href="{home}#grupos">Grupos</a> / <span aria-current="page">{v["titulo"]}</span></nav>
<h1 id="t-titulo"><span class="serif it">{h["titulo_serif"]}</span><br><span class="caps">{h["titulo_caps"]}</span></h1></div>
<p class="hero__meta small">{h["meta"]}</p></div></section>''')
    fatos = "".join(f"<li>{f}</li>" for f in v["fatos"])
    conduz = "".join(f'<li><span class="avatar" aria-hidden="true">{n[0]}</span><span><span class="serif person">{n}</span><span class="small">{r}</span></span></li>' for n, r in v["conduz"])
    out.append(f'''<section class="trip-intro on-dark"><div class="wrap trip-intro__grid">
<div><p class="lead">{v["descricao"]}</p><ul class="facts serif" role="list">{fatos}</ul></div>
<div><p class="serif it trip-intro__quote">{v["frase"]}</p><a class="btn btn--line" href="#reserva">Reserve seu lugar</a>
<div class="hosts-mini"><p class="small">Quem conduz</p><ul role="list">{conduz}</ul></div></div></div></section>''')
    ficha = "".join(f"<div><dt class=\"small\">{a}</dt><dd class=\"serif\">{b}</dd></div>" for a, b in v["ficha"])
    gal = "".join(f"<li>{foto(n, 'gallery__img', a, sizes='(min-width:820px) 25vw, 50vw')}</li>" for n, a in v["galeria"])
    vis = "".join(f"<p>{x}</p>" for x in v["visao"])
    out.append(f'''<section class="band band--white trip-sec" aria-labelledby="s-visao"><div class="wrap">{head("Visão geral", "A viagem", "s-visao")}
<div class="trip-two"><div class="prose">{vis}</div><dl class="ficha">{ficha}</dl></div>
<ul class="gallery" role="list" aria-label="Fotos da viagem">{gal}</ul></div></section>''')
    pq = v.get("para_quem")
    if pq:
      perfis = "".join(f'<li class="tile"><span class="small">{i+1:02d}</span><h3 class="serif">{t}</h3><p>{x}</p></li>' for i, (t, x) in enumerate(pq["perfis"]))
      out.append(f'''<section class="band band--sky trip-sec" id="para-quem" aria-labelledby="s-quem"><div class="wrap">{head("Para quem é", "Para quem é<br>esta viagem", "s-quem")}
<p class="serif it trip-lead">{pq["lead"]}</p><ul class="tiles" role="list">{perfis}</ul></div></section>''')
    esc = "".join(f'<li class="choice"><h3 class="serif">{t}</h3><p>{x}</p></li>' for t, x in v["escolhas"])
    out.append(f'''<section class="band band--olive trip-sec" aria-labelledby="s-esc"><div class="wrap">{head("O que define esta viagem", "Nossas escolhas", "s-esc")}<ul class="choices" role="list">{esc}</ul></div></section>''')
    mapa = (SRC / f"data/mapas/{v['mapa']}.svg").read_text().strip() if v.get("mapa") else ""
    leg = "".join(f'<li><svg width="26" height="6" aria-hidden="true">{LEG[k]}</svg>{t}</li>' for k, t in v.get("legenda", []))
    dias = "".join(f'''<details><summary><span><span class="small">Dia {i+1}</span><span class="serif day-title">{t}</span></span></summary>
<div class="day">{f'<p class="small day-stay">Hospedagem · {hosp}</p>' if hosp else ''}{ul(itens, 'bullets')}</div></details>''' for i, (t, hosp, itens) in enumerate(v["roteiro"]))
    out.append(f'''<section class="band band--forest trip-sec" id="roteiro" aria-labelledby="s-rot"><div class="wrap">{head("Dia a dia", "Roteiro", "s-rot")}
<div class="route">{f'<figure class="map">{mapa}<ul class="map__legend" role="list">{leg}</ul></figure>' if mapa else ''}<div class="acc acc--light days">{dias}</div></div></div></section>''')
    out.append(f'''<section class="band band--mist trip-sec" aria-labelledby="s-inc"><div class="wrap">{head("Inclui e não inclui", "O que está incluído", "s-inc")}
<div class="acc acc--big"><details><summary>Inclui</summary>{ul(v["inclui"], "lines")}</details><details><summary>Não inclui</summary>{ul(v["nao_inclui"], "lines")}</details></div></div></section>''')
    if v.get("bikes"):
        b = v["bikes"]; bk = "".join(f'<li class="tile tile--media">{foto(None, "tile__img", alt)}<div><span class="small">{tipo}</span><h3 class="serif">{n}</h3><p>{x}</p></div></li>' for tipo, n, x, alt in b["itens"])
        out.append(f'''<section class="band band--white trip-sec" id="bicicletas" aria-labelledby="s-bike"><div class="wrap">{head("Bicicletas", "Sua bike na viagem", "s-bike")}<p class="trip-text">{b["texto"]}</p><ul class="tiles tiles--2" role="list">{bk}</ul></div></section>''')
    an = "".join(f'<li class="host">{foto(None, "host__img", alt)}<h3 class="serif">{n}</h3><p class="small">{r}</p><p>{x}</p></li>' for n, r, x, alt in v["anfitrioes"])
    out.append(f'''<section class="band band--lilac trip-sec" id="anfitrioes" aria-labelledby="s-anf"><div class="wrap">{head("Quem conduz", "Anfitriões", "s-anf")}<ul class="hosts" role="list">{an}</ul></div></section>''')
    ht = "".join(f'<li class="tile tile--media">{foto(None, "tile__img tile__img--short", alt)}<div><h3 class="serif">{n}</h3><p class="small">{m}</p><p>{x}</p></div></li>' for n, m, x, alt in v["hoteis"])
    out.append(f'''<section class="band band--sky trip-sec" aria-labelledby="s-hot"><div class="wrap">{head("Hospedagem", "Onde ficamos", "s-hot")}<ul class="tiles tiles--hotels" role="list">{ht}</ul>{f'<p class="small hotel-note">{v["hoteis_nota"]}</p>' if v.get("hoteis_nota") else ""}</div></section>''')
    fq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in v["faq"])
    out.append(f'''<section class="band band--earth trip-sec" aria-labelledby="s-faq"><div class="wrap">{head("Perguntas frequentes", "Antes de reservar", "s-faq")}<div class="acc acc--light acc--faq">{fq}</div></div></section>''')
    r = v["reserva"]
    out.append(f'''<section class="band band--black trip-sec" id="reserva" aria-labelledby="s-res"><div class="wrap narrow"><h2 class="h2" id="s-res">Reserve seu lugar</h2><span class="rule" aria-hidden="true"></span>
<p class="serif res-line">{r["linha"]}</p><p class="serif it res-note">{r["nota"]}</p>
<div class="res-ctas"><a class="btn btn--solid" href="{wa}" data-track="whatsapp" data-viagem="{v["slug"]}">Reserve seu lugar</a><a class="btn btn--line" href="{home}#grupos">Ver outros grupos</a></div></div></section>''')
    return "\n".join(out)

for v in viagens:
    if v.get("pagina"):
        c = viagem(v)
    else:
        c = f'<section class="on-dark" style="min-height:70svh;display:flex;align-items:flex-end"><div class="wrap" style="padding-bottom:var(--s16)"><h1 class="serif" style="font-size:var(--fs-title);line-height:1.05">{v["titulo"]}</h1><p class="small" style="margin-top:var(--s4)">{v["resumo"]}</p></div></section>'
    page(f"viagens/{v['slug']}", f"{v['titulo']} · Andante", c, description=v.get("descricao", site["descricao"]))
print(f"{len(viagens)} viagens:", ", ".join(v["slug"] for v in viagens), "→", OUT)
