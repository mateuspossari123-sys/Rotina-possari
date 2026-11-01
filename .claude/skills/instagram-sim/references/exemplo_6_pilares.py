# Exemplo completo: um post de feed por pilar + grade simulada do feed.
# Uso: python3 exemplo_6_pilares.py <pasta-da-skill> <pasta-com-cut/03.png> [pasta-com-foto_missao.jpg]
import sys
sys.path.insert(0, sys.argv[1] + '/scripts')
from sim_kit import *
from PIL import Image, ImageDraw
U = sys.argv[3] if len(sys.argv) > 3 else '.'   # pasta com a foto da missão
SRC = sys.argv[2]
W, H = 1080, 1350
out = []

# 1 liturgia
img = canvas('feed', 'navy'); d = ImageDraw.Draw(img)
spaced(d, '8 DE DEZEMBRO', font('MS700', 34), 540, 420, 14, GOLD)
spaced(d, 'SOLENIDADE DA', font('MS700', 34), 540, 520, 10, CREAM)
d.text((540, 690), 'Imaculada', font=font('PF900', 170), fill=CREAM, anchor='ms')
d.text((540, 870), 'Conceição', font=font('PF900', 170), fill=CREAM, anchor='ms')
sublinhar_palavra(img, 'Imaculada', 'Imaculada', font('PF900', 170), 540, 690, GOLD, 6, 22)
d = ImageDraw.Draw(img)
wrap(d, '"Eis a serva do Senhor."', font('PF700I', 46), 540, 1010, 900, GOLD, 56)
logo(img, CREAM, 80, None, 1160)
out.append(save(img, '1_liturgia.jpg', 'linho-sutil'))

# 2 formação (capa carrossel claro)
img = canvas('feed', 'creme'); d = ImageDraw.Draw(img)
spaced(d, 'FORMAÇÃO', font('MS700', 32), 90, 220, 14, GOLD, anchor='l')
d.text((90, 400), 'O que é', font=font('PF900', 120), fill=NAVY, anchor='ls')
d.text((90, 530), 'o Advento?', font=font('PF700I', 120), fill=NAVY, anchor='ls')
sublinhado(img, 90, 560, 560, GOLD, 6); d = ImageDraw.Draw(img)
for i, t in enumerate(['Tempo de espera e preparação para o Natal.', 'Quatro domingos antes de 25 de dezembro.', 'Cor litúrgica: roxo, sinal de conversão.']):
    y = 720 + i * 150
    d.text((90, y + 40), f'{i+1:02d}', font=font('PF900', 64), fill=GOLD, anchor='ls')
    wrap(d, t, font('MS600', 36), 210, y, 760, NAVY, 48, 'left')
spaced(d, 'ARRASTE PARA O LADO  »', font('MS700', 24), 90, 1250, 6, NAVY, anchor='l')
logo(img, NAVY, 70, W - 150, 1200)
out.append(save(img, '2_formacao.jpg'))

# 3 vida da missão (foto)
ph = tratamento(cover(Image.open(f'{U}/foto_missao.jpg'), W, H, .5, .55), 'quente')
img = degrade(ph, NAVY2, 900, 1350, 220); d = ImageDraw.Draw(img)
wrap(d, 'Rezar juntos é missão.', font('PF700I', 74), 80, 1170, 900, CREAM, 84, 'left')
spaced(d, 'ENCONTRO DE ORAÇÃO · NOVEMBRO', font('MS700', 24), 80, 1250, 6, GOLD, anchor='l')
logo(img, CREAM, 64, W - 130, 1195)
out.append(save(img, '3_missao.jpg', 'linho'))

# 4 palavra (fundo dourado)
img = canvas('feed', 'dourado'); d = ImageDraw.Draw(img)
spaced(d, 'PALAVRA DO DIA', font('MS700', 32), 540, 300, 14, NAVY)
cruz(d, 540, 400, 60, NAVY, 4)
for i, ln in enumerate(['"Vinde a mim,', 'todos vós que estais', 'cansados, e eu', 'vos aliviarei."']):
    d.text((540, 580 + i * 100), ln, font=font('PF700I' if i in (0, 3) else 'PF500', 78), fill=NAVY, anchor='ms')
spaced(d, 'MATEUS 11,28', font('MS700', 26), 540, 1010, 8, NAVY)
logo(img, NAVY, 70, None, 1180)
out.append(save(img, '4_palavra.jpg', 'linho-sutil'))

# 5 santos (recorte)
img = canvas('feed', 'claro'); d = ImageDraw.Draw(img)
d.text((540, 300), 'SANTA', font=font('PF900', 110), fill=CREAM, anchor='ms')
d.text((540, 520), 'TERESINHA', font=font('PF900', 175), fill=CREAM, anchor='ms')
st = Image.open(f'{SRC}/cut/03.png').convert('RGBA'); st = st.crop(st.getbbox())
st = st.resize((int(st.width * 700 / st.height), 700))
img.alpha_composite(st, ((W - st.width) // 2, 500))
img = degrade(img, NAVY, 960, 1350, 245); d = ImageDraw.Draw(img)
wrap(d, '"Minha vocação é o amor."', font('PF700I', 62), 540, 1150, 950, CREAM, 70)
spaced(d, 'SANTA TERESINHA, ROGAI POR NÓS!', font('MS700', 24), 540, 1230, 6, GOLD)
logo(img, CREAM, 56, None, 40)
out.append(save(img, '5_santos.jpg'))

# 6 convite (blocos ousados)
img = canvas('feed', 'creme'); d = ImageDraw.Draw(img)
d.rectangle((60, 120, 1020, 900), fill=NAVY)
d.rectangle((60, 120, 1020, 190), fill=(245, 184, 40)); d.line((60, 190, 1020, 190), fill=NAVY, width=5)
d.text((90, 158), 'CONVITE.EXE', font=font('MS700', 30), fill=NAVY, anchor='lm')
d.text((540, 430), 'RETIRO', font=font('PF900', 200), fill=CREAM, anchor='ms')
d.text((540, 600), 'de Advento', font=font('PF700I', 110), fill=(245, 184, 40), anchor='ms')
d.text((540, 790), 'Inscrições abertas', font=font('MS700', 44), fill=CREAM, anchor='ms')
d.rectangle((60, 990, 1020, 1160), fill=(245, 184, 40))
d.text((540, 1060), '06 E 07 DE DEZEMBRO', font=font('MS700', 50), fill=NAVY, anchor='ms')
d.text((540, 1125), 'Comunidade SIM', font=font('PF700I', 44), fill=NAVY, anchor='ms')
logo(img, NAVY, 70, None, 1220)
out.append(save(img, '6_convite.jpg'))

# grade 3x2 simulando o feed
g = Image.new('RGB', (3 * 360 + 8, 2 * 450 + 4), (255, 255, 255))
for i, f in enumerate(['3_missao', '1_liturgia', '2_formacao', '4_palavra', '6_convite', '5_santos']):
    g.paste(Image.open(f + '.jpg').resize((360, 450)), ((i % 3) * 364, (i // 3) * 454))
g.save('FEED_simulado.jpg', quality=92)
print('ok')
