# andante-site

Site da Andante. HTML, CSS e JS estáticos, sem framework, no mesmo padrão do thiagovitamina.com.

- `src/templates/` páginas e o modelo de viagem
- `src/data/` textos do site (`site.json`) e uma viagem por arquivo (`viagens/*.json`)
- `src/assets/` CSS com os tokens da identidade, JS, fontes e imagens
- `build.py` gera o site em `dist/`
- `scripts/audit.sh` roda acessibilidade, SEO e performance

    python3 source/andante/build.py

Preview: `python3 source/andante/build.py` gera `/andante` (thiagovitamina.com/andante, noindex). Produção: Cloudflare Pages.

## Breakpoints (mobile first)

O CSS parte do mobile (layouts de 390px) e cresce com `min-width`:

| Faixa | Largura | O que muda |
| --- | --- | --- |
| base | até 599px | layout dos wireframes, 1 coluna |
| sm | 600px | tablet em pé: respiros maiores, grades de 2 colunas |
| md | 820px | tablet deitado: header completo, roteiro e ficha lado a lado |
| lg | 1100px | desktop: grid de 12 colunas, tipografia display maior |
| xl | 1440px | largura máxima do conteúdo, só as margens crescem |

Testar sempre em 320, 375, 390, 600, 820, 1100 e 1440px.
