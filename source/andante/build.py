"""Gera o site da Andante em dist/: páginas fixas + uma página por viagem a partir de src/data/viagens/*.json."""
import json, pathlib, shutil
ROOT = pathlib.Path(__file__).parent; SRC = ROOT / "src"; OUT = ROOT.parent.parent / "andante"  # servido em thiagovitamina.com/andante (preview)
if OUT.exists(): shutil.rmtree(OUT)
shutil.copytree(SRC / "assets", OUT / "assets")
site = json.loads((SRC / "data/site.json").read_text())
viagens = [json.loads(p.read_text()) for p in sorted((SRC / "data/viagens").glob("*.json"))]
print(f"{len(viagens)} viagens:", ", ".join(v["slug"] for v in viagens))
(OUT / "index.html").write_text("""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Andante · em construção</title>
<link rel="stylesheet" href="assets/css/tokens.css">
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:var(--ground);color:var(--ink);font-family:var(--sans)}</style>
</head><body><main><p>Andante · em construção</p></main></body></html>
""")
