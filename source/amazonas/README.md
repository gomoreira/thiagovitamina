# Agência Amazonas · material para o thumbnail do Also live

Decisão (11/11/2026): fica no Also live, não vira case. Aguarda a nova dinâmica dos thumbnails para gerar v/amazonas.mp4.

Capturado em 11/11/2026 no Chrome, desktop 1440 px de largura, 1x, a partir de https://www.agenciaamazonas.am.gov.br. Fica em `source/`, que não vai para o deploy (`.vercelignore`).

## Entrada no site (já está em source/index.html, sem vídeo)

- Título: Agência Amazonas
- Link: https://www.agenciaamazonas.am.gov.br (texto do link: agenciaamazonas.am.gov.br)
- Texto atual: The official news agency of the Amazonas state government. I designed it in Figma and led the development, built in WordPress.
- Texto proposto (mesmo ritmo de ECCON e CEPA, só fatos que dá para ver no site):
  The official news agency of the Amazonas state government. News, radio, photos and audio in one place, with a dark mode and adjustable text size. I designed it in Figma and led the development, built in WordPress.
- aria-label do vídeo (proposto): Screen recording of the Agência Amazonas website, from the front-page headlines to the list of sections.
- Arquivos esperados: v/amazonas.mp4 + v/amazonas.jpg (poster), mesmo formato de v/eccon.mp4 e v/cepa.mp4: 900×720, 12 s, 30 fps, H.264, sem som.

## Quadros (frames/, 1440×757, resolução real)

| Arquivo | O que mostra |
|---|---|
| home-01-top.jpg | Barra da rádio, atalhos de acessibilidade (A+ A A- e modo escuro), links de governo, logo, busca, banners e o destaque |
| home-02-headlines.jpg | Títulos dos destaques e a grade de notícias com categoria |
| home-03-editorias.jpg | Faixa verde com todas as editorias em pílulas + "Outros destaques" |
| home-04-ultimas.jpg | Últimas Notícias, grade de 4 colunas |
| home-05-ultimas-2.jpg | Segunda linha das Últimas Notícias |
| home-dark-top.jpg | O mesmo topo com o modo escuro ligado |
| article-pesca.jpg | Página de notícia (título, data, linha fina, foto com crédito) |
| home-fullpage-top-3785.jpg | Os cinco quadros da home costurados em uma imagem só (1440×3785), boa para rolar ou recortar |

ref/: o resto da home (rádio, fotos, áudios, notas, newsletter, rodapé) e as editorias no escuro, em resolução baixa, só como referência.

## Identidade do site (lida do CSS)

- Fonte: Montserrat
- Azul-marinho #223058 (títulos, logo), verde #0A853B e #009D4B (pílulas, rodapé), verde-limão da faixa de editorias, vinho #B32355 (categorias), laranja #E07931 (áudios)
- Dentro do thumbnail essas cores são do trabalho, não do portfólio. A moldura em volta segue a paleta do portfólio (sem segunda cor de acento).

## Cuidados

- O conteúdo é notícia do dia e muda sempre. Os quadros mostram o governador e outras autoridades. Para o portfólio, prefira os trechos de estrutura (topo, editorias, grade) aos rostos.
- Não usar a notícia "PC-AM divulga imagens de dois homens que desapareceram" (home-04, primeira coluna): é um aviso de pessoa desaparecida. Recortar, desfocar ou trocar esse quadro.
- A barra da rádio mostra a música que estava tocando (Detonautas). É detalhe do momento da captura.
- O selo do reCAPTCHA e o botão de voltar ao topo foram escondidos na captura. Nada mais foi mexido.
- Não há captura de celular: a janela do Chrome não desce abaixo de 606 px. Se o novo thumbnail precisar de tela de celular, capturar no iPhone ou no modo responsivo do DevTools.

## Layout original (original-2020/)

Dois mockups em perspectiva, 1920×1280, da pasta "Agencia Amazonas" no Google Drive do Thiago (subidos em nov/2022). Mostram a home com conteúdo de junho de 2020 (Covid, Parintins) e texto de exemplo em lorem ipsum: topo e destaques, outros destaques, grade de notícias, fotos, vídeos, áudios, últimas notas, newsletter, "Checagem de fatos" e rodapé.

- mockup-01-home-top.jpg
- mockup-02-home-bottom.jpg

Contexto do Drive: pasta "AGÊNCIA AMAZONAS - NOTÍCIAS PARA O LAYOUT", compartilhada pela equipe da Secom em 12/06/2020, com as notícias e fotos usadas para preencher o layout. Em 2022 houve uma segunda rodada de ajustes no portal (orçamentos de abril de 2022; os valores não entram no portfólio).

O arquivo do Figma não foi localizado; como ficou no Also live, não é necessário.
