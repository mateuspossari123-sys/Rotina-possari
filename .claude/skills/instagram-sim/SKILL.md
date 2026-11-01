---
name: instagram-sim
description: Cria posts, carrosséis e stories para o Instagram da SIM (comunidade/missão católica) e para seus retiros e encontros com identidade própria (Diga SIM a Deus, Santificai-vos, Kairós, Evangeliza Show, Ou Santo Ou Nada, Celebrai 30 anos), sempre perguntando antes para que é a arte, e seguindo a identidade visual da SIM (azul-marinho, creme e dourado, Playfair + Montserrat, logo de Nossa Senhora com a cruz) e variando o formato para o feed não ficar repetitivo. Use sempre que o usuário pedir arte, post, story, carrossel, capa, convite, aviso ou qualquer peça para o Instagram/redes da SIM, ou falar de datas litúrgicas, santos, orações, formação ou eventos da missão — mesmo que não diga "Instagram" ou "SIM" explicitamente.
---

# Instagram da SIM

A SIM é uma comunidade/missão católica (30 anos em 1996–2026). O perfil tem identidade visual definida, mas o feed estava ficando "tudo igual": mesmo fundo, mesmo título serifado, mesmo dourado em todo post. Esta skill existe para **manter a identidade e variar o formato**.

## Primeiro passo: perguntar para que é a arte
O usuário pediu que **toda arte comece com perguntas**, para acertar na montagem e manter o feed organizado. Antes de desenhar qualquer coisa, pergunte (de preferência numa única mensagem curta, ou com a ferramenta de perguntas de múltipla escolha, se houver) o que ainda não estiver claro no pedido:

1. **Para que é?** É de alguma **campanha/retiro/encontro** com identidade própria — Diga SIM a Deus, Santificai-vos, Kairós, Evangeliza Show, Ou Santo Ou Nada, Celebrai 30 anos — ou é um post do **perfil da SIM** (liturgia, formação, missão, oração, santos, aviso)?
2. **Onde vai?** Feed (4:5), story (9:16) ou carrossel? Carrossel: **4 a 5 lâminas no máximo**, conteúdo enxuto (capa + 2–3 de conteúdo + fechamento).
3. **Quando vai ao ar e qual foi o último post do feed?** (ou peça um print do feed) — para escolher um fundo/formato que contraste.
4. **Texto e informações:** frase principal, data, hora, local, link/inscrição. Se não houver texto, ofereça escrever uma proposta.
5. **Cor:** não pergunte em aberto — **sugira** uma cor da paleta (`references/paletas.md`) com 1 linha de motivo (tempo litúrgico, tipo de post, contraste com o último post) e peça confirmação. Em campanhas, as cores são as da campanha.
6. **Imagens:** usar foto do banco (`assets/fotos/`), arte sacra, foto que o usuário vai mandar, ou só tipografia?

Não pergunte o que o pedido já respondeu. Se a resposta for "tanto faz", decida você e diga o que escolheu.

## Depois das respostas
0. Leia `references/feed-atual.md`: o feed já tem formatos que funcionam. Evolua o que existe; não substitua.
1. **Se for campanha:** leia a seção dela em `references/campanhas.md`, abra as referências em `assets/campanhas/<nome>/` e siga a identidade DA CAMPANHA (cores, fontes, elementos). O logo SIM entra pequeno como assinatura. As regras de cor da SIM abaixo não se aplicam a ela.
2. **Se for post do perfil:** identifique o **pilar** (tabela abaixo) e leia em `references/modelos.md` só a seção dele.
3. Use o último post informado para escolher contraste — veja "Ritmo do feed" em `references/modelos.md`.
4. Para variar de verdade, consulte `references/inspiracoes.md` (Minha Biblioteca Católica, Padre Paulo Ricardo, Colo de Deus, Dunamis) e escolha um dos "formatos novos" quando o feed estiver repetitivo.
5. Antes de renderizar, diga em 2–3 linhas o plano (pilar/campanha, formato, layout); se o usuário já foi claro, siga direto.

| Pilar | Quando | Cara do post |
|---|---|---|
| 1. Liturgia e datas | solenidades, festas, tempos litúrgicos | tipográfico solene, fundo marinho |
| 2. Formação | explicar a fé (por quê, como, o que é) | carrossel claro, tópicos numerados |
| 3. Vida da missão | encontros, missões, bastidores, pessoas | foto real em destaque, pouco texto |
| 4. Palavra e oração | versículo, oração, jaculatória | "santinho" creme com moldura, ou fundo dourado |
| 5. Santos | memória, testemunho, frase de santo | santo recortado + nome grande + frase |
| 6. Convites e avisos | eventos, inscrições, horários | gráfico ousado (retrô/blocos), mais livre |

## Identidade visual da SIM (posts do perfil; campanhas seguem `references/campanhas.md`)
- Cores base: azul-marinho `#03283B`, creme `#FDEFE2`, dourado `#C9A055`; apoio: azul `#1B4F6B`, azul claro `#4682A0`.
- Cores vivas aprovadas (litúrgicas + apoio): veja `references/paletas.md` — uma por post, para dar cor ao feed.
- Fontes (em `assets/fonts`): Playfair Display (títulos 900, destaques em itálico 700, orações 500), Montserrat (sobretítulos espaçados, rodapés, tópicos) e uma sans condensada pesada — `Anton` ou `Oswald700` — para manchetes de campanha e frases-gancho, como já aparece no feed. A fonte oficial Awesome Serif é paga; Playfair é a substituta aprovada.
- Logo: `assets/logo_sim_mask.png` (traço; recolorir em creme ou marinho). Selo 30 anos: `assets/selo_30anos.png` (só em peças de aniversário).
- Não colocar o @ do Instagram nas artes.

## Preferências já aprovadas pelo usuário
- Sublinhado **reto** e dourado, só na palavra-chave (nunca curvo/pincel, nunca em tudo).
- Logo pequeno; quando há foto em cima, logo **embaixo**, não sobre a imagem.
- Textura **não faz parte da identidade** — é opcional e com moderação. Padrão: fundo **liso**. Use linho bem leve só onde reforça o sentido: peças orantes/sóbrias (oração, luto, santinho) e fotos (`textura='linho'` na foto, `'linho-sutil'` em fundo liso). Em formação, convites e campanhas, deixe liso. Num carrossel, só algumas lâminas (ex.: a da foto e a da oração). Papel de missal antigo foi recusado.
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

Exemplos prontos: `references/exemplo_formatos_novos.py` (resultado em `references/feed_formatos_novos.jpg`; fonte manuscrita `Caveat700`) e, um post por pilar, `references/exemplo_6_pilares.py` (resultado em `references/feed_simulado.jpg`).

Cuidados técnicos: as fontes só têm caracteres latinos — evite setas (→) e emojis; use » ou —. Ao sublinhar palavra numa linha de título grande, confira se o traço não encosta na linha de baixo.

Sempre: renderize, **olhe o resultado** (reduza e leia a imagem) e corrija sobreposições, textos cortados ou ilegíveis antes de entregar. Entregue JPG (e PDF se pedirem, com uma página por arte).

## Conteúdo católico
- Citações bíblicas com referência (livro capítulo,versículo). Frases de santos só se forem conhecidas e de autoria confiável; na dúvida, prefira a Bíblia ou o Catecismo e diga ao usuário.
- Tom: acolhedor, jovem, sem ser informal demais; textos curtos no feed.
- Se o usuário não mandar o texto, proponha uma versão e deixe claro que é sugestão para ele ajustar.

## Arte sacra
- Pinturas clássicas (antigas, domínio público) funcionam muito bem como imagem nobre. Prefira obras antigas conhecidas; cite o pintor quando souber. Se precisar de uma imagem específica, peça ao usuário ou procure em acervos de domínio público.

## Fotos
- Banco de fotos da comunidade: `assets/fotos/` (24 fotos; veja `assets/fotos/INDICE.md` para escolher pelo tema). Para o pilar 3, use dessas; se precisar de mais, peça ao usuário (ele pode baixar do Facebook da comunidade). Evite repetir a mesma foto em posts próximos.
- Tratamento padrão: `tratamento(im, 'quente')`; datas de luto/oração: `'frio'`.
- Imagens de santos da internet podem ter direitos autorais — avise se a peça for para venda/impressão.
