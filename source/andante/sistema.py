"""Versão Vitamina: passa o site.css pela régua do sistema e gera system.css.

Cada medida escrita à mão vira o passo mais próximo da escala:
- font-size  → escala tipográfica (14 · 16 · 20 · 24 · 32 · 40 · 48 · 64 · 88)
- padding, margin, gap, inset → escala de espaço (4 · 8 · 16 · 24 · 32 · 48 · 64 · 104)
- line-height em px → próximo múltiplo de 4 acima (grade de linha de base)
O resultado é uma cópia completa do site.css (a cascata não muda), com os tokens
do sistema e os ajustes de desenho (MANUAL) no fim. Recuos de layout acima de 120px ficam.
Depois vêm os ajustes de desenho que a régua sozinha não resolve (MANUAL).
"""
import re, pathlib

TYPE = [14, 16, 20, 24, 32, 40, 48, 64, 88]
SPACE = [0, 4, 8, 16, 24, 32, 48, 64, 104]

TOKENS = """
:root{
  --fs-small:14px; --fs-body:16px; --fs-lead:20px;
  --fs-h3:24px; --fs-h2:32px; --fs-title:40px; --fs-display:40px; --fs-hero:40px;
  --s3:16px; --s5:24px; --s10:48px; --s24:104px;
  --edge:20px; --gutter:16px; --btn-h:52px;
}
@media (min-width:600px){ :root{ --edge:32px } }
@media (min-width:820px){ :root{ --edge:40px; --gutter:24px; --fs-lead:20px; --fs-h2:40px; --fs-title:48px; --fs-display:48px; --fs-hero:48px } }
@media (min-width:1100px){ :root{ --edge:48px; --fs-body:18px; --fs-lead:22px; --fs-h3:28px; --fs-h2:48px; --fs-title:64px; --fs-display:64px; --fs-hero:64px; --btn-h:56px } }
@media (min-width:1440px){ :root{ --edge:64px } }
"""

MANUAL = """
/* botão cheio em fundo escuro: contorno vermelho da marca (4,7:1 contra o preto) para o botão não se perder no fundo (WCAG 1.4.11 pede 3:1) */
.on-dark .btn--solid,.band--black .btn--solid,.band--forest .btn--solid,.band--earth .btn--solid,.menu .btn--solid{border-color:var(--red)}
/* Páginas de viagem no celular (pedido do cliente, 26/11): hotéis e bikes em carrossel; "para quem é" como lista */
@media (max-width:819px){
  ul.carousel{display:flex;gap:var(--s2);overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding-inline:var(--edge);margin-inline:calc(-1 * var(--edge));padding-inline:var(--edge);scrollbar-width:none;overscroll-behavior-x:contain}
  .carousel::-webkit-scrollbar{display:none}
  .carousel>li{flex:0 0 82%;scroll-snap-align:start}
  .carousel:focus-visible{outline:2px solid currentColor;outline-offset:4px}
  .carousel__count{display:flex;justify-content:space-between;align-items:center;margin-top:var(--s4)}
  .carousel__dots{display:flex;gap:var(--s1)}
  .carousel__dots i{display:block;width:8px;height:2px;background:currentColor;opacity:.35;transition:width .25s var(--ease),opacity .25s var(--ease)}
  .carousel__dots i.is-on{width:24px;opacity:1}
}
.tiles--perfis{gap:0;border-top:1px solid currentColor}
.tiles--perfis .tile{background:none;min-height:0;padding:var(--s6) 0;gap:var(--s2);border-bottom:1px solid currentColor;display:grid;grid-template-columns:40px 1fr;column-gap:var(--s4)}
.tiles--perfis .tile>*{grid-column:2}.tiles--perfis .tile>.small{grid-column:1;grid-row:1 / span 2;padding-top:8px}
.tiles--perfis .tile>p{margin-top:0}
@media (min-width:820px){.tiles--perfis{grid-template-columns:repeat(2,1fr);column-gap:var(--s6);border-top:0}.tiles--perfis .tile{border-top:1px solid currentColor;border-bottom:0}}
@media (prefers-reduced-motion:reduce){.carousel{scroll-behavior:auto}.carousel__dots i{transition:none}}
/* País Basco: paleta mais leve, a partir do teste do cliente (26/11). Contraste conferido: texto preto 8,3:1 e 10,7:1; branco 13,5:1 e 7,5:1 */
.paleta-clara{--sky:#8ea8ab;--olive:#d0b776;--lilac:#d0b776;--forest:#29302f;--earth:#82442a}
.paleta-clara .day-stay{color:#e6b48c}
/* botão cheio num vermelho mais fechado: pedido do cliente (25/11). Branco sobre ele: 7,9:1 */
:root{--red-fill:#9e1f17}
/* WhatsApp sempre à mão */
.wa-float{position:fixed;z-index:40;right:var(--s4);bottom:calc(var(--s4) + env(safe-area-inset-bottom));display:inline-flex;align-items:center;gap:var(--s2);min-height:48px;padding:0 var(--s5);background:var(--ink);color:var(--paper);border:1px solid var(--red);font-size:var(--fs-body);font-weight:500;text-decoration:none}
@media (hover:hover){.wa-float:hover{background:var(--red-fill);border-color:var(--red-fill)}}
.v-vitamina:has(.variant) .wa-float{bottom:80px}
body:has(.menu.is-open) .wa-float{display:none}
.wa-float{transition:opacity .25s var(--ease),transform .25s var(--ease)}
.wa-float.is-away{opacity:0;transform:translateY(8px);pointer-events:none}
/* no celular vira um círculo só com o ícone, para não cobrir o texto */
@media (max-width:819px){.wa-float{width:56px;min-height:56px;padding:0;justify-content:center;border-radius:50%}.wa-float span{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}.wa-float svg{width:24px;height:24px}}
@media (prefers-reduced-motion:reduce){.wa-float{transition:none}}
/* botões: chamada para ação no tamanho do texto, não da legenda */
.btn{min-height:var(--btn-h);min-width:200px;padding:0 var(--s8);font-size:var(--fs-body);line-height:24px}
.header__cta{min-height:48px;min-width:0;font-size:16px}
.more{font-size:var(--fs-body);line-height:24px}
/* títulos seguem a escala, sem tamanho próprio */
.quote__text{font-size:var(--fs-h2);line-height:1.1}
.hero__title{line-height:.98;text-wrap:wrap}
.t-line{display:block;white-space:nowrap}
@media (max-width:359px){.hero__title{font-size:32px}}
.groups__lead,.trip-lead,.trip-intro__quote{font-size:var(--fs-h3);line-height:1.2}
.why__title,.card__title,.choice h3{line-height:1.05}
.tile h3{font-size:var(--fs-h3);line-height:1.15}
.change__table td{font-size:var(--fs-lead);line-height:28px}
/* grid: mesma calha em todas as grades */
.cards,.tiles{gap:var(--gutter)}
@media (min-width:820px){
  .band--olive .split,.split,.change,.why__grid{column-gap:var(--gutter)}
  .quote__text{font-size:var(--fs-display)}
}
@media (min-width:1100px){
  .header__nav{font-size:16px}
  .groups__head,.band--white .narrow,.band--earth .narrow{column-gap:var(--gutter)}
  .groups__lead{font-size:var(--fs-h2);line-height:1.15}
  .quote__text{font-size:var(--fs-display);line-height:1.02}
  .change__table td{font-size:var(--fs-h3);line-height:32px}
}
"""

def snap(v, scale):
    return min(scale, key=lambda s: (abs(s - v), s))

def fix_value(prop, val):
    if "calc(" in val or "min(" in val or "max(" in val:
        return val
    if prop == "font-size":
        return re.sub(r"(\d+(?:\.\d+)?)px", lambda m: f"{snap(float(m.group(1)), TYPE)}px", val)
    if prop == "line-height":
        return re.sub(r"(\d+(?:\.\d+)?)px", lambda m: f"{max(4, -(-float(m.group(1)) // 4) * 4):.0f}px", val)
    if re.match(r"(padding|margin|gap|row-gap|column-gap|inset)", prop):
        def one(m):
            n = float(m.group(1)); s = -1 if m.group(0).startswith("-") else 1
            if n > 120: return m.group(0)  # recuo de layout, não espaçamento
            return f"{s * snap(abs(n), SPACE)}px"
        return re.sub(r"-?(\d+(?:\.\d+)?)px", one, val)
    return val

def blocks(css):
    """Divide em (prelude, corpo) no nível de cima; corpo de @media volta como texto."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    i, out = 0, []
    while i < len(css):
        j = css.find("{", i)
        if j < 0: break
        pre = css[i:j].strip(); depth, k = 1, j + 1
        while depth:
            depth += {"{": 1, "}": -1}.get(css[k], 0); k += 1
        out.append((pre, css[j + 1:k - 1])); i = k
    return out

CHANGES = []

def process(css):
    res = []
    for pre, body in blocks(css):
        if pre.startswith("@media") or pre.startswith("@supports"):
            res.append(f"{pre}{{{process(body)}}}")
        elif pre.startswith("@"):
            res.append(f"{pre}{{{body}}}")
        else:
            decls = []
            for decl in body.split(";"):
                if ":" not in decl: continue
                p, v = decl.split(":", 1); p, v = p.strip(), v.strip()
                nv = fix_value(p, v)
                if nv != v: CHANGES.append((pre, p, v, nv))
                decls.append(f"{p}:{nv}")
            res.append(f"{pre}{{{';'.join(decls)}}}")
    return "\n".join(res)

def build(site_css: str) -> str:
    return ("/* Gerado por sistema.py a partir de site.css. Não editar à mão. */\n"
            + process(site_css) + "\n/* tokens do sistema */" + TOKENS + "\n/* ajustes de desenho */" + MANUAL)

if __name__ == "__main__":
    src = pathlib.Path(__file__).parent / "src/assets/css/site.css"
    build(src.read_text())
    for pre, p, v, nv in CHANGES: print(f"{pre[:40]:40} {p:16} {v:>22} → {nv}")
    print(len(CHANGES), "medidas ajustadas")
