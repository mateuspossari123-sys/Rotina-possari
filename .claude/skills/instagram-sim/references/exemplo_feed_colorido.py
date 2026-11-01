import sys, os
K = sys.argv[1]
sys.path.insert(0, K + '/scripts')
from sim_kit import *
from PIL import Image, ImageDraw
OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1350
FOT = K + '/assets/fotos/'

VINHO = (158, 43, 37); OLIVA = (79, 122, 58); ROXO = (91, 44, 131); ROSA = (217, 121, 139); OURO_CL = (233, 196, 106)
TERRA = (200, 85, 61); LARANJA = (224, 122, 69); CEU = (127, 183, 217); TURQ = (42, 157, 143); MOST = (245, 184, 40)

def solid(cor):
    return grain(Image.new('RGB', (W, H), cor), 4)

posts = []
def P(nome, img): img.convert('RGB').save(f'{OUT}/{nome}.jpg', quality=92); posts.append(nome)

# 1. Advento — roxo
img = solid(ROXO); d = ImageDraw.Draw(img)
spaced(d, 'TEMPO DO ADVENTO', font('MS700', 32), 540, 330, 14, OURO_CL)
d.text((540, 600), 'Vem,', font=font('PF900', 190), fill=CREAM, anchor='ms')
d.text((540, 790), 'Senhor Jesus!', font=font('PF700I', 130), fill=CREAM, anchor='ms')
sublinhar_palavra(img, 'Senhor Jesus!', 'Jesus', font('PF700I', 130), 540, 790, GOLD, 6, 28); d = ImageDraw.Draw(img)
spaced(d, 'APOCALIPSE 22,20', font('MS700', 26), 540, 960, 8, OURO_CL)
logo(img, CREAM, 72, None, 1200)
P('01_advento_roxo', img)

# 2. Tempo comum — creme + palavra oliva
img = canvas('feed', 'creme'); d = ImageDraw.Draw(img)
spaced(d, 'PALAVRA DO DIA', font('MS700', 30), 80, 260, 12, OLIVA, anchor='l')
d.text((80, 520), 'Sede', font=font('PF900', 230), fill=NAVY, anchor='ls')
d.text((80, 760), 'santos', font=font('PF900', 230), fill=OLIVA, anchor='ls')
wrap(d, 'porque eu sou santo.', font('PF700I', 72), 80, 880, 900, NAVY, 80, 'left')
spaced(d, '1 PEDRO 1,16', font('MS700', 26), 80, 980, 8, NAVY, anchor='l')
logo(img, NAVY, 64, W - 130, 1230)
P('02_tempo_comum_oliva', img)

# 3. Pentecostes — vinho
img = solid(VINHO); d = ImageDraw.Draw(img)
for i, (t, c) in enumerate([('VINDE,', CREAM), ('ESPÍRITO', CREAM), ('SANTO!', OURO_CL)]):
    d.text((80, 450 + i * 225), t, font=font('Anton', 195), fill=c, anchor='ls')
wrap(d, 'Enchei os corações dos vossos fiéis e acendei neles o fogo do vosso amor.', font('PF700I', 46), 80, 1020, 900, CREAM, 58, 'left')
logo(img, CREAM, 64, W - 130, 1235)
P('03_pentecostes_vinho', img)

# 4. Mariano — azul-céu
img = solid(CEU); d = ImageDraw.Draw(img)
spaced(d, 'COM MARIA', font('MS700', 30), 540, 300, 14, NAVY)
for i, ln in enumerate(['"Eis aqui', 'a serva', 'do Senhor."']):
    d.text((540, 540 + i * 150), ln, font=font('PF900' if i < 2 else 'PF700I', 140), fill=NAVY if i < 2 else CREAM, anchor='ms')
spaced(d, 'LUCAS 1,38', font('MS700', 26), 540, 1000, 8, NAVY)
logo(img, NAVY, 72, None, 1200)
P('04_mariano_ceu', img)

# 5. Gancho terracota
img = solid(TERRA); d = ImageDraw.Draw(img)
for i, t in enumerate(['REZE POR', 'QUEM VOCÊ', 'AMA HOJE.']):
    d.text((80, 520 + i * 190), t, font=font('Anton', 200), fill=CREAM, anchor='ls')
sublinhado(img, 80, 640, 948, NAVY, 10); d = ImageDraw.Draw(img)
wrap(d, 'A oração é o primeiro jeito de cuidar de alguém.', font('PF700I', 50), 80, 1070, 900, NAVY, 60, 'left')
logo(img, CREAM, 64, W - 130, 1235)
P('05_gancho_terracota', img)

# 6. Convite — foto + bloco turquesa
ph = tratamento(cover(Image.open(FOT + 'oson-multidao.jpg'), W, 760, .5, .5), 'quente')
img = solid(TURQ); img.alpha_composite(ph, (0, 0)); d = ImageDraw.Draw(img)
spaced(d, 'VEM COM A GENTE', font('MS700', 30), 80, 870, 12, CREAM, anchor='l')
d.text((80, 1050), 'Encontro', font=font('PF900', 150), fill=CREAM, anchor='ls')
d.text((80, 1170), 'de jovens', font=font('PF700I', 110), fill=NAVY, anchor='ls')
d.rounded_rectangle((680, 1220, 1000, 1290), 35, fill=NAVY)
d.text((840, 1268), 'SAIBA MAIS', font=font('MS700', 26), fill=CREAM, anchor='ms')
P('06_convite_turquesa', img)

# 7. Mostarda — aviso ousado
img = solid(MOST); d = ImageDraw.Draw(img)
d.text((540, 600), 'VEM', font=font('Anton', 420), fill=NAVY, anchor='ms')
d.text((540, 820), 'AÍ!', font=font('Anton', 260), fill=CREAM, anchor='ms')
d.rectangle((80, 950, 1000, 1110), fill=NAVY)
d.text((540, 1050), 'Novidade da SIM em breve', font=font('PF700I', 60), fill=MOST, anchor='ms')
logo(img, NAVY, 70, None, 1190)
P('07_aviso_mostarda', img)

# 8. Foto + palavra rosa
ph = tratamento(cover(Image.open(FOT + 'form-alegria.jpg'), W, H, .5, .4), 'quente')
img = degrade(ph, NAVY2, 820, 1350, 220); d = ImageDraw.Draw(img)
d.text((80, 1130), 'Amizade', font=font('PF900', 130), fill=CREAM, anchor='ls')
d.text((80, 1240), 'que leva a Deus.', font=font('PF700I', 80), fill=ROSA, anchor='ls')
logo(img, CREAM, 60, W - 120, 1240)
P('08_foto_rosa', img)

# 9. Base marinho/dourado (o padrão de sempre)
img = canvas('feed', 'navy'); d = ImageDraw.Draw(img)
spaced(d, 'JESUS,', font('MS700', 40), 540, 520, 16, GOLD)
d.text((540, 720), 'eu confio', font=font('PF700I', 150), fill=CREAM, anchor='ms')
d.text((540, 880), 'em Vós', font=font('PF900', 170), fill=CREAM, anchor='ms')
logo(img, CREAM, 72, None, 1200)
P('09_base_marinho', img)

# ---------- prancha de paletas ----------
BW, BH = 2160, 1500
b = Image.new('RGB', (BW, BH), CREAM); d = ImageDraw.Draw(b)
d.text((100, 150), 'Paletas para dar cor ao feed da SIM', font=font('PF900', 84), fill=NAVY, anchor='ls')
d.text((100, 215), 'Base fixa + uma cor viva por post (regra 60 · 30 · 10)', font=font('PF700I', 44), fill=GOLD, anchor='ls')
def row(y, titulo, itens):
    d.text((100, y), titulo, font=font('MS700', 34), fill=NAVY, anchor='ls')
    for i, (nome, cor, uso) in enumerate(itens):
        x = 100 + i * 400
        d.rounded_rectangle((x, y + 30, x + 360, y + 230), 24, fill=cor)
        dark = sum(cor) / 3 < 150
        d.text((x + 24, y + 200), '#%02X%02X%02X' % cor, font=font('MS700', 28), fill=CREAM if dark else NAVY, anchor='ls')
        d.text((x, y + 280), nome, font=font('MS700', 30), fill=NAVY, anchor='ls')
        d.text((x, y + 320), uso, font=font('MS600', 24), fill=(90, 90, 90), anchor='ls')
row(330, 'BASE (identidade SIM — sempre)', [('Azul-marinho', NAVY, 'fundo, títulos'), ('Creme', (240, 226, 210), 'fundo claro'), ('Dourado', GOLD, 'detalhes, itálicos'), ('Azul claro', LIGHT, 'apoio')])
row(750, 'CORES LITÚRGICAS (destaque com significado)', [('Roxo', ROXO, 'Advento e Quaresma'), ('Verde-oliva', OLIVA, 'Tempo Comum'), ('Vinho', VINHO, 'Pentecostes, mártires'), ('Rosa antigo', ROSA, 'Gaudete, Laetare, Maria'), ('Ouro claro', OURO_CL, 'Natal, Páscoa')])
row(1130, 'CORES DE APOIO (vibrantes, para quebrar o feed)', [('Terracota', TERRA, 'frases-gancho'), ('Laranja', LARANJA, 'campanhas, energia'), ('Azul-céu', CEU, 'mariano, leveza'), ('Turquesa', TURQ, 'jovens, convites'), ('Mostarda', MOST, 'avisos ousados')])
b.save(f'{OUT}/PALETAS_SIM.jpg', quality=93)

# ---------- feed simulado ----------
order = ['06_convite_turquesa', '09_base_marinho', '02_tempo_comum_oliva',
         '05_gancho_terracota', '08_foto_rosa', '04_mariano_ceu',
         '01_advento_roxo', '07_aviso_mostarda', '03_pentecostes_vinho']
g = Image.new('RGB', (3 * 360 + 8, 3 * 450 + 8), (255, 255, 255))
for i, f in enumerate(order):
    g.paste(Image.open(f'{OUT}/{f}.jpg').resize((360, 450)), ((i % 3) * 364, (i // 3) * 454))
g.save(f'{OUT}/FEED_COLORIDO_exemplo.jpg', quality=92)
print('ok')
