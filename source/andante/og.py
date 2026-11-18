"""Imagens de compartilhamento (1200×630) para WhatsApp, redes e buscadores.
Foto da página, degradê para leitura, moldura vermelha e logo, como no topo do site."""
import pathlib, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = pathlib.Path(__file__).parent
F = HERE / "og/fonts"
W, H = 1200, 630
RED = (240, 0, 0)

def _font(name, size): return ImageFont.truetype(str(F / name), size)

def _logo(width):
    svg = (HERE / "src/partials/logo.svg").read_text().replace('fill="currentColor"', 'fill="#ffffff"')
    with tempfile.TemporaryDirectory() as d:
        s, p = pathlib.Path(d) / "l.svg", pathlib.Path(d) / "l.png"
        s.write_text(svg); subprocess.run(["rsvg-convert", "-w", str(width), str(s), "-o", str(p)], check=True)
        return Image.open(p).convert("RGBA")

def make(photo: pathlib.Path, out: pathlib.Path, serif: str, caps: str, meta: str = "", focus=(0.5, 0.6)):
    im = ImageOps.fit(Image.open(photo).convert("RGB"), (W, H), Image.LANCZOS, centering=focus)
    # degradê: escurece o topo (logo) e a base (título) para o texto branco ler sobre qualquer foto
    shade = Image.new("L", (1, H))
    for y in range(H):
        t = y / H
        a = 0.45 * max(0, 1 - t / 0.3) + 0.82 * max(0, (t - 0.38) / 0.62) ** 1.2
        shade.putpixel((0, y), int(255 * min(a, 0.85)))
    im = Image.composite(Image.new("RGB", (W, H), "black"), im, shade.resize((W, H)))
    d = ImageDraw.Draw(im)
    d.rectangle((32, 32, W - 33, H - 33), outline=RED, width=2)
    logo = _logo(300); im.paste(logo, (64, 64), logo)
    x, y = 64, H - 64
    if meta:
        fm = _font("Outfit-Medium.ttf", 26); y -= 26
        d.text((x, y), meta, font=fm, fill="white", anchor="ls"); y -= 48
    fc = _font("Outfit-SemiBold.ttf", 76); fs = _font("InstrumentSerif-Italic.ttf", 84)
    d.text((x, y), caps.upper(), font=fc, fill="white", anchor="ls")
    d.text((x, y - 78), serif, font=fs, fill="white", anchor="ls")
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=86, optimize=True, progressive=True)
    return out
