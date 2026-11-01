---
name: instagram-sim
description: Cria posts, carrosséis e stories para o Instagram da SIM (comunidade/missão católica), seguindo a identidade visual da SIM (azul-marinho, creme e dourado, Playfair + Montserrat, logo de Nossa Senhora com a cruz) e variando o formato para o feed não ficar repetitivo. Use sempre que o usuário pedir arte, post, story, carrossel, capa, convite, aviso ou qualquer peça para o Instagram/redes da SIM, ou falar de datas litúrgicas, santos, orações, formação ou eventos da missão — mesmo que não diga "Instagram" ou "SIM" explicitamente.
---

# Instagram da SIM

A SIM é uma comunidade/missão católica (30 anos em 1996–2026). O perfil tem identidade visual definida, mas o feed estava ficando "tudo igual": mesmo fundo, mesmo título serifado, mesmo dourado em todo post. Esta skill existe para **manter a identidade e variar o formato**.

## Antes de criar
0. Leia `references/feed-atual.md`: o feed já tem formatos que funcionam e campanhas com cara própria (Kairós, Evangeliza Show, Ou Santo Ou Nada, Santificai-vos). Evolua o que existe; não substitua.
1. Identifique o **pilar** do pedido (tabela abaixo). Se não estiver claro, escolha o mais provável e diga qual escolheu.
2. Pergunte (ou deduza) o **formato**: feed 4:5 (1080×1350), story 9:16 (1080×1920) ou carrossel. Padrão: feed 4:5.
3. Se o usuário contar qual foi o post anterior (ou mandar print do feed), escolha um modelo/fundo que contraste com ele — veja "Ritmo do feed" em `references/modelos.md`.
4. Leia em `references/modelos.md` só a seção do pilar escolhido.

| Pilar | Quando | Cara do post |
|---|---|---|
| 1. Liturgia e datas | solenidades, festas, tempos litúrgicos | tipográfico solene, fundo marinho |
| 2. Formação | explicar a fé (por quê, como, o que é) | carrossel claro, tópicos numerados |
| 3. Vida da missão | encontros, missões, bastidores, pessoas | foto real em destaque, pouco texto |
| 4. Palavra e oração | versículo, oração, jaculatória | "santinho" creme com moldura, ou fundo dourado |
| 5. Santos | memória, testemunho, frase de santo | santo recortado + nome grande + frase |
| 6. Convites e avisos | eventos, inscrições, horários | gráfico ousado (retrô/blocos), mais livre |

## Identidade visual (não negociável)
- Cores: azul-marinho `#03283B`, creme `#FDEFE2`, dourado `#C9A055`; apoio: azul `#1B4F6B`, azul claro `#4682A0`. Amarelo vivo `#F5B828` só no pilar 6.
- Fontes (em `assets/fonts`): Playfair Display (títulos 900, destaques em itálico 700, orações 500), Montserrat (sobretítulos espaçados, rodapés, tópicos) e uma sans condensada pesada — `Anton` ou `Oswald700` — para manchetes de campanha e frases-gancho, como já aparece no feed. A fonte oficial Awesome Serif é paga; Playfair é a substituta aprovada.
- Logo: `assets/logo_sim_mask.png` (traço; recolorir em creme ou marinho). Selo 30 anos: `assets/selo_30anos.png` (só em peças de aniversário).
- Não colocar o @ do Instagram nas artes.

## Preferências já aprovadas pelo usuário
- Sublinhado **reto** e dourado, só na palavra-chave (nunca curvo/pincel, nunca em tudo).
- Logo pequeno; quando há foto em cima, logo **embaixo**, não sobre a imagem.
- Texturas **bem leves**: linho na foto (`save(..., textura='linho')`) e quase imperceptível em fundo liso (`textura='linho-sutil'`). Papel de missal antigo foi recusado.
- Texto nunca cobrindo rosto, mãos ou o elemento principal da foto — mover o texto para a área de "respiro".
- Stories: deixar margem segura no topo e embaixo (barra de resposta do Instagram).

## Como produzir
Use o kit `scripts/sim_kit.py` (Pillow + numpy + opencv). Ele já tem: `canvas()`, `cover()`, `tratamento()`, `degrade()`, `logo()`, `spaced()`, `wrap()`, `sublinhado()`, `sublinhar_palavra()`, `cruz()`, `moldura()`, `linho()`, `save()`.

```python
import sys; sys.path.insert(0, '<pasta da skill>/scripts')
from sim_kit import *
img = canvas('feed', 'creme'); d = ImageDraw.Draw(img)
spaced(d, 'REZE CONOSCO', font('MS700', 34), 540, 300, 14, GOLD)
d.text((540, 430), 'Oração pelos', font=font('PF900', 90), fill=NAVY, anchor='ms')
...
save(img, 'post.jpg')
```

Exemplo completo de um post por pilar: `references/exemplo_6_pilares.py` (resultado em `references/feed_simulado.jpg`).

Cuidados técnicos: as fontes só têm caracteres latinos — evite setas (→) e emojis; use » ou —. Ao sublinhar palavra numa linha de título grande, confira se o traço não encosta na linha de baixo.

Sempre: renderize, **olhe o resultado** (reduza e leia a imagem) e corrija sobreposições, textos cortados ou ilegíveis antes de entregar. Entregue JPG (e PDF se pedirem, com uma página por arte).

## Conteúdo católico
- Citações bíblicas com referência (livro capítulo,versículo). Frases de santos só se forem conhecidas e de autoria confiável; na dúvida, prefira a Bíblia ou o Catecismo e diga ao usuário.
- Tom: acolhedor, jovem, sem ser informal demais; textos curtos no feed.
- Se o usuário não mandar o texto, proponha uma versão e deixe claro que é sugestão para ele ajustar.

## Fotos
- Banco de fotos da comunidade: `assets/fotos/` (24 fotos; veja `assets/fotos/INDICE.md` para escolher pelo tema). Para o pilar 3, use dessas; se precisar de mais, peça ao usuário (ele pode baixar do Facebook da comunidade). Evite repetir a mesma foto em posts próximos.
- Tratamento padrão: `tratamento(im, 'quente')`; datas de luto/oração: `'frio'`.
- Imagens de santos da internet podem ter direitos autorais — avise se a peça for para venda/impressão.
