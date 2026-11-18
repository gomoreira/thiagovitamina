# andante-site

Site da Andante. HTML, CSS e JS estáticos, sem framework, no mesmo padrão do thiagovitamina.com.

- `src/templates/` páginas e o modelo de viagem
- `src/data/` textos do site (`site.json`) e uma viagem por arquivo (`viagens/*.json`)
- `src/assets/` CSS com os tokens da identidade, JS, fontes e imagens
- `build.py` gera o site em `dist/`
- `scripts/audit.sh` roda acessibilidade, SEO e performance

    python3 source/andante/build.py

Preview: `python3 source/andante/build.py` gera `/andante` (thiagovitamina.com/andante, noindex). Produção: Cloudflare Pages.
