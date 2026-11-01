# Modelos de post por pilar

Cada pilar tem uma "cara" própria para o feed não ficar repetitivo. Coordenadas abaixo são para feed 1080×1350; para story (1080×1920) mantenha as proporções e respeite a área segura (nada importante acima de y≈250 nem abaixo de y≈1700).

## Sumário
1. Liturgia e datas
2. Formação
3. Vida da missão
4. Palavra e oração
5. Santos
6. Convites e avisos

---

## 1. Liturgia e datas — "tipográfico solene"
Para: solenidades, festas, tempos litúrgicos, datas da Igreja.
- Fundo: `navy` (ou foto com tratamento + degradê marinho embaixo).
- Sobretítulo Montserrat 700 espaçado (sp 12–14) em CREAM ou GOLD.
- Título grande Playfair 900 (170–250 px) em CREAM. Sublinhado reto dourado só na palavra-chave, se houver.
- Data em Playfair itálico GOLD entre dois fios dourados.
- Logo pequeno (70–90 px) embaixo, centralizado.
- Exemplo aprovado: story "Fiéis Defuntos" (anjo + título), arte "Dia de Todos os Santos".

## 2. Formação — "carrossel claro"
Para: explicar algo da fé (por que, como, o que é). Preferir CARROSSEL de 3–6 lâminas no feed.
- Fundo: `creme` (variar com `claro` em uma das lâminas).
- Capa: pergunta grande em Playfair 900 NAVY + segunda linha em itálico GOLD.
- Lâminas internas: número grande dourado (01, 02…) à esquerda + texto Montserrat 600 (34–38 px) NAVY, fios dourados finos separando.
- Última lâmina: fonte/citação (Catecismo, Bíblia, documento) em itálico + logo.
- Exemplo aprovado: story 2 "Por que rezar pelos que partiram?" (versão escura). No feed, usar a versão clara para alternar.

## 3. Vida da missão — "foto em destaque"
Para: encontros, missões, retiros, bastidores, pessoas da comunidade. É o pilar que mais humaniza o perfil.
- Foto ocupa 100% (`cover` + `tratamento('quente')`).
- Pouco texto: no máximo 1 frase curta em Playfair itálico (60–80 px) + linha Montserrat pequena (local/data).
- Texto onde a foto tiver "respiro" (céu, parede, chão); escurecer só aquela faixa com `degrade`.
- Logo pequeno num canto (não no centro), 60–70 px.
- Textura `linho` leve.
- Variações já usadas no feed: (a) foto pura sem texto; (b) foto + **moldura branca fina** recortando parte da cena; (c) **frase-gancho** em sans condensada branca (Anton/Oswald) + itálico dourado sobre a foto escurecida ("VOCÊ SE LEMBRA...").
- Fotos: `assets/fotos/` + `INDICE.md`.

## 4. Palavra e oração — "santinho"
Para: versículo, jaculatória, oração curta, frase do dia.
- Fundo `creme` com `moldura` dupla (marinho + dourado), OU `dourado` com texto NAVY (usar de vez em quando — é o post mais "diferente" do feed).
- Sobretítulo espaçado GOLD ("REZE CONOSCO", "PALAVRA DO DIA").
- Texto central em Playfair 500 (64–80 px), linhas curtas centralizadas; final em itálico.
- Cruz fina dourada como separador. Referência bíblica em Montserrat pequeno.
- Exemplo aprovado: story 3 "Oração pelos fiéis defuntos".

## 5. Santos — "recorte + frase"
Para: memória de santos, testemunhos, frases de santos.
- Santo recortado (rembg: modelo `isnet-general-use`; se falhar em véu/capa, `u2net_human_seg`) sobre fundo `navy`, `claro` ou papel.
- Nome do santo grande (Playfair 900 ou letras altas finas) ATRÁS do recorte (o recorte vaza o nome).
- Frase do santo em itálico; assinatura "SÃO/SANTA ..., ROGAI POR NÓS!" em Montserrat.
- Alternativa: retrato em janela em arco com moldura dourada fina.
- Exemplos aprovados: arte São João Paulo II "O amor me explicou tudo", modelo MISERI/CÓRDIA.

## 6. Convites e avisos — "gráfico ousado"
Para: eventos, inscrições, horários, campanhas. Pode fugir um pouco do clássico para chamar atenção.
- Estilo retrô de janelas de computador (barra azul claro/amarela, sombra dura NAVY, botões ✕▢_), OU blocos de cor chapada.
- Título em letras grandes; informações (data · hora · local) numa faixa NAVY embaixo.
- Pode usar amarelo vivo `#F5B828` como cor de destaque NESTE pilar.
- Formato da casa: tipografia condensada enorme (Anton) em fundo dourado/creme + Playfair itálico + **pílulas arredondadas** no rodapé ("Kairós · Comunidade SIM"), como o post do Kairós. Se o evento for de uma campanha existente, use as cores da campanha.
- Exemplo aprovado: vídeo "Ou santo ou nada" versão retrô SIM.

---

## Ritmo do feed (grade de 3 colunas)
Pense em cada linha de 3 posts. Regras:
- Nunca dois fundos iguais lado a lado (navy | creme | foto é a combinação base).
- Pelo menos 1 foto real a cada 3 posts quando houver fotos disponíveis.
- Não repetir o mesmo pilar em sequência, exceto em datas fortes (ex.: Todos os Santos + Finados).
- Varie a posição do bloco de texto (alto / centro / baixo) entre posts vizinhos.
- Logo: centralizado em cima, embaixo, ou no canto — alterne.

Se o usuário disser qual foi o último post (ou mandar print do feed), escolha o modelo do próximo para "quebrar" o que veio antes.
