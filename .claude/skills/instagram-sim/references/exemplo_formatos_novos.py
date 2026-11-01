# Exemplo: 6 formatos novos (manchete-gancho, palavra quebrada, número gigante, notificação, parede tipográfica, frase manuscrita).
# Uso: python3 exemplo_formatos_novos.py <pasta-da-skill>
import sys, math
K = sys.argv[1]
sys.path.insert(0, K + '/scripts')
from sim_kit import *
from PIL import Image, ImageDraw
W, H = 1080, 1350
FOT = K + '/assets/fotos/'
YEL = (245, 184, 40)

def fit_font(nome, txt, maxw, start):
    s = start
    while font(nome, s).getlength(txt) > maxw and s > 10: s -= 4
    return font(nome, s)

# 1. Manchete-gancho sobre foto
ph = tratamento(cover(Image.open(FOT + 'form-familia.jpg'), W, H, .5, .5), 'quente')
img = degrade(ph, NAVY2, 300, 1350, 230); d = ImageDraw.Draw(img)
for i, (t, c) in enumerate([('QUANDO FOI A', CREAM), ('ÚLTIMA VEZ QUE', CREAM), ('ALGUÉM REZOU', GOLD), ('POR VOCÊ?', GOLD)]):
    f = font('Anton', 118)
    d.text((80, 700 + i * 140), t, font=f, fill=c, anchor='ls')
spaced(d, 'A INTERCESSÃO MUDA HISTÓRIAS', font('MS700', 24), 80, 1290, 6, CREAM, anchor='l')
logo(img, CREAM, 60, W - 120, 1235)
save(img, 'n1_manchete.jpg', 'linho')

# 2. Palavra quebrada
img = canvas('feed', 'creme'); d = ImageDraw.Draw(img)
spaced(d, 'O NOME DE DEUS É', font('MS700', 32), 80, 230, 12, NAVY, anchor='l')
f = font('PF900', 300)
d.text((60, 520), 'MISERI-', font=fit_font('PF900', 'MISERI-', 960, 300), fill=NAVY, anchor='ls')
d.text((60, 800), 'CÓRDIA', font=fit_font('PF900', 'MISERI-', 960, 300), fill=GOLD, anchor='ls')
d.text((80, 940), '— Papa Francisco', font=font('PF700I', 48), fill=NAVY, anchor='ls')
sublinhado(img, 80, 420, 980, GOLD, 4); d = ImageDraw.Draw(img)
wrap(d, 'Deus nunca se cansa de perdoar; somos nós que nos cansamos de pedir perdão.', font('MS600', 34), 80, 1090, 900, NAVY, 46, 'left')
logo(img, NAVY, 64, W - 130, 1240)
save(img, 'n2_palavra_quebrada.jpg')

# 3. Número gigante + foto histórica
img = canvas('feed', 'navy'); d = ImageDraw.Draw(img)
ph = tratamento(cover(Image.open(FOT + 'diga-sim-antigo.jpg'), 470, 700, .5, .5), 'pb')
d.rectangle((565, 290, 1045, 1000), fill=CREAM)
img.alpha_composite(ph, (570, 295)); d = ImageDraw.Draw(img)
d.text((40, 820), '30', font=font('Anton', 520), fill=GOLD, anchor='ls')
d.text((60, 920), 'anos dizendo', font=font('PF700I', 64), fill=CREAM, anchor='ls')
d.text((60, 1080), 'SIM', font=font('Anton', 170), fill=CREAM, anchor='ls')
spaced(d, '1996 — 2026', font('MS700', 26), 60, 1150, 8, GOLD, anchor='l')
logo(img, CREAM, 70, 60, 1210)
save(img, 'n3_numero.jpg', 'linho-sutil')

# 4. Retrato + frase manuscrita
ph = tratamento(cover(Image.open(FOT + 'form-alegria.jpg'), W, H, .5, .45), 'quente')
img = degrade(ph, NAVY2, 850, 1350, 200); d = ImageDraw.Draw(img)
for i, t in enumerate(['Santidade também', 'é dar risada', 'com quem caminha', 'com você.']):
    d.text((80, 1000 + i * 78), t, font=font('Caveat700', 92), fill=CREAM, anchor='ls')
logo(img, CREAM, 60, W - 120, 1240)
save(img, 'n4_manuscrita.jpg', 'linho')

# 5. Mockup do cotidiano: notificação de celular
img = canvas('feed', 'claro'); d = ImageDraw.Draw(img)
spaced(d, 'VOCÊ TEM UMA', font('MS700', 34), 540, 210, 12, CREAM)
d.text((540, 340), 'nova mensagem', font=font('PF700I', 110), fill=CREAM, anchor='ms')
def card(y, app, title, body, hl=False):
    d.rounded_rectangle((90, y, 990, y + 230), 40, fill=(250, 246, 240) if not hl else CREAM)
    d.rounded_rectangle((130, y + 40, 210, y + 120), 18, fill=NAVY)
    logo(img, CREAM, 60, 145, y + 50)
    d.text((240, y + 62), app, font=font('MS600', 28), fill=(120, 120, 120), anchor='ls')
    d.text((950, y + 62), 'agora', font=font('MS600', 26), fill=(150, 150, 150), anchor='rs')
    d.text((240, y + 112), title, font=font('MS700', 38), fill=NAVY, anchor='ls')
    wrap(d, body, font('MS600', 32), 240, y + 160, 700, (60, 60, 60), 42, 'left')
card(470, 'SIM · Oração', 'Jesus', '"Vinde a mim, todos vós que estais cansados." (Mt 11,28)', True)
card(730, 'SIM · Lembrete', 'Encontro de oração', 'Hoje tem! Traga um amigo.')
d.rounded_rectangle((300, 1050, 780, 1130), 40, fill=NAVY)
d.text((540, 1102), 'RESPONDER COM UM SIM', font=font('MS700', 28), fill=CREAM, anchor='ms')
logo(img, CREAM, 60, None, 1220)
save(img, 'n5_notificacao.jpg')

# 6. Parede tipográfica
img = canvas('feed', 'navy'); d = ImageDraw.Draw(img)
f = font('Anton', 96)
for i in range(11):
    y = 170 + i * 102
    hl = i == 5
    d.text((540, y), 'JESUS, EU CONFIO EM VÓS', font=font('Anton', 84),
           fill=GOLD if hl else (40, 70, 92), anchor='ms')
logo(img, CREAM, 70, None, 1240)
save(img, 'n6_parede.jpg', 'linho-sutil')

g = Image.new('RGB', (3 * 360 + 8, 2 * 450 + 4), (255, 255, 255))
for i, f in enumerate(['n1_manchete', 'n2_palavra_quebrada', 'n3_numero', 'n5_notificacao', 'n6_parede', 'n4_manuscrita']):
    g.paste(Image.open(f + '.jpg').resize((360, 450)), ((i % 3) * 364, (i // 3) * 454))
g.save('FEED_formatos_novos.jpg', quality=92)
print('ok')
