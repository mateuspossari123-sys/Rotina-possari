# Carrossel Finados — estilo "Dunamis" (granulado, tipografia gigante, papel anotado, bilhete) com cores SIM
import sys, os, math
K = sys.argv[1]
sys.path.insert(0, K + '/scripts')
from sim_kit import *
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps

W, H = 1080, 1350
OUT = os.path.dirname(os.path.abspath(__file__))
U = '/root/.claude/uploads/390b7722-2cfe-5f42-bc60-95d3ebc3ef6b'
ANJO, ORANTE = f'{U}/939797ab-image.webp', f'{U}/e018aafa-image.jpg'
OFF = (243, 238, 228)
OR = LARANJA            # laranja SIM
RED = (196, 70, 50)     # caneta
rng = np.random.default_rng(7)

def grao(img, s=22):
    a = np.array(img.convert('RGB'), np.float32)
    n = rng.normal(0, s, (H, W, 1))
    sp = (rng.random((H, W, 1)) < 0.012) * rng.choice([-90, 90], (H, W, 1))
    return Image.fromarray(np.clip(a + n + sp, 0, 255).astype(np.uint8)).convert('RGBA')

def pb(im, w, h, fx=.5, fy=.5, blur=0, contr=1.25):
    g = ImageOps.grayscale(cover(im, w, h, fx, fy))
    g = ImageEnhance.Contrast(g).enhance(contr)
    if blur: g = g.filter(ImageFilter.GaussianBlur(blur))
    return Image.merge('RGB', [g] * 3).convert('RGBA')

def dsm_tag(img, i, n=5, cor=CREAM):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((W - 150, 50, W - 40, 106), 28, fill=(20, 20, 24))
    d.text((W - 95, 88), f'{i}/{n}', font=font('MS700', 28), fill=CREAM, anchor='ms')
    logo(img, cor, 54, 50, H - 100)

def wobble(pts, amp=2.2):
    return [(x + rng.normal(0, amp), y + rng.normal(0, amp)) for x, y in pts]

def caneta(d, pts, cor=RED, w=5):
    d.line(wobble(pts), fill=cor, width=w, joint='curve')

def circulo(d, cx, cy, rx, ry, cor=RED, w=4):
    pts = [(cx + rx * math.cos(t) * (1 + 0.04 * math.sin(3 * t)), cy + ry * math.sin(t)) for t in np.linspace(0.3, 2 * math.pi + 0.7, 70)]
    caneta(d, pts, cor, w)

# ---------------- 1. capa: foto P&B + tipografia gigante alternada ----------------
img = pb(Image.open(ANJO), W, H, .5, .4, contr=1.35)
img = degrade(img, (10, 10, 12), 500, H, 200)
d = ImageDraw.Draw(img)
f = font('Anton', 190)
linhas = [('POR QUE', OR, 'l'), ('REZAMOS', CREAM, 'r'), ('PELOS', OR, 'l'), ('MORTOS?', CREAM, 'r')]
y = 600
for t, c, a in linhas:
    x = 70 if a == 'l' else W - 70 - f.getlength(t)
    d.text((x, y), t, font=f, fill=c, anchor='ls'); y += 190
spaced(d, 'COMEMORAÇÃO DE TODOS OS FIÉIS DEFUNTOS · 2/11', font('MS700', 24), 540, 1250, 5, CREAM)
img = grao(img, 26); dsm_tag(img, 1)
save(img, f'{OUT}/01_capa.jpg')

# ---------------- 2. cartão azul sobre foto + texto justificado gigante ----------------
img = pb(Image.open(ORANTE), W, H, .5, .55, blur=6, contr=1.1)
d = ImageDraw.Draw(img)
d.rectangle((150, 170, 930, 1180), fill=BLUE)
d.text((900, 220), 'NA FÉ DA IGREJA:', font=font('Archivo700', 26), fill=CREAM, anchor='rs')
spaced(d, 'O QUE ACONTECE DEPOIS DA MORTE?', font('Archivo700', 30), 90, 440, 0, CREAM, anchor='l')
txt = '"NÃO REZAMOS PARA QUE OS MORTOS SE SALVEM." QUEM ESTÁ NO PURGATÓRIO JÁ ESTÁ SALVO: SÓ PRECISA SER PURIFICADO PARA ENTRAR NO CÉU.'
f = font('Archivo900', 64)
words = txt.split(); lines = []; cur = []
for w_ in words:
    if f.getlength(' '.join(cur + [w_])) <= 900: cur.append(w_)
    else: lines.append(cur); cur = [w_]
lines.append(cur)
y = 540
for k, ln in enumerate(lines):
    last = k == len(lines) - 1
    tot = sum(f.getlength(w_) for w_ in ln)
    gap = (900 - tot) / max(1, len(ln) - 1) if not last else f.getlength(' ')
    x = 90
    for w_ in ln:
        d.text((x, y), w_, font=f, fill=CREAM, anchor='ls'); x += f.getlength(w_) + gap
    y += 74
d.text((900, 1100), 'CATECISMO 1030–1031', font=font('Archivo700', 26), fill=CREAM, anchor='rs')
img = grao(img, 24); dsm_tag(img, 2)
save(img, f'{OUT}/02_ja_estao_salvos.jpg')

# ---------------- 3. folha de papel anotada à mão ----------------
img = Image.new('RGBA', (W, H), BLUE + (255,))
bgph = pb(Image.open(ANJO), W, H, .5, .5, blur=14, contr=1.0)
img = Image.blend(img, Image.composite(Image.new('RGBA', (W, H), BLUE + (255,)), Image.new('RGBA', (W, H), NAVY + (255,)), bgph.convert('L')), 0.55)
d = ImageDraw.Draw(img)
px0, py0, px1, py1 = 140, 150, 940, 1200
sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).rectangle((px0 + 14, py0 + 18, px1 + 14, py1 + 18), fill=150)
img.paste((0, 0, 0, 255), (0, 0), sh.filter(ImageFilter.GaussianBlur(16)))
d = ImageDraw.Draw(img)
d.rectangle((px0, py0, px1, py1), fill=OFF)
d.line((px0, 700, px1, 700), fill=(220, 214, 202), width=2)       # dobra do papel
tape = Image.new('RGBA', (110, 300), (222, 210, 186, 210)); tape = tape.rotate(-6, expand=True)
img.alpha_composite(tape, (px1 - 70, 260)); d = ImageDraw.Draw(img)
# bloco 1
f1 = font('Archivo900', 44)
for k, t in enumerate(['ENTÃO, POR QUE', 'REZAR POR ELES?']):
    d.text((200, 270 + k * 52), t, font=f1, fill=NAVY, anchor='ls')
caneta(d, [(178, 225), (168, 228), (168, 340), (178, 344)], RED, 4)
wrap(d, 'As almas do purgatório não podem fazer mais nada por si mesmas. Elas dependem das nossas orações.', font('Archivo700', 30), 200, 420, 660, OR, 38, 'left')
caneta(d, [(200, 360), (330, 364), (470, 358), (600, 362)], RED, 4)
# bloco 2 (serifa)
fs = font('PF900', 54)
d.text((200, 800), 'REZAMOS POR TODOS,', font=fs, fill=NAVY, anchor='ls')
d.text((200, 862), 'NA MISERICÓRDIA.', font=fs, fill=NAVY, anchor='ls')
caneta(d, [(200, 884), (330, 880), (480, 886), (640, 879)], RED, 5)
caneta(d, [(215, 896), (400, 892), (600, 897)], RED, 3)
d.rectangle((855, 700, 905, 750), outline=RED, width=4)
caneta(d, [(863, 722), (877, 740), (915, 682)], RED, 5)
wrap(d, 'Não sabemos o destino de quem partiu: por isso confiamos todos a Deus.', font('PF700I', 34), 200, 930, 650, OR, 42, 'left')
# bloco 3
wrap(d, 'Rezar pelos mortos é um gesto de caridade e de esperança.', font('Archivo700', 34), 200, 1080, 520, NAVY, 42, 'left')
caneta(d, [(178, 1040), (168, 1044), (168, 1160), (178, 1164)], RED, 4)
for ang in range(0, 180, 45):                                         # asterisco
    t = math.radians(ang); cx, cy, r = 820, 1110, 48
    d.line((cx - r * math.cos(t), cy - r * math.sin(t), cx + r * math.cos(t), cy + r * math.sin(t)), fill=(230, 120, 105), width=16)
d.text((px1 - 30, py1 - 26), '2 MACABEUS 12,43-46 · CATECISMO 1032', font=font('MS700', 18), fill=NAVY, anchor='rs')
img = grao(img, 20); dsm_tag(img, 3)
save(img, f'{OUT}/03_por_que_rezar.jpg')

# ---------------- 4. bolha laranja + palavra gigante ----------------
img = Image.new('RGBA', (W, H), OFF + (255,))
yy, xx = np.mgrid[0:H, 0:W]
r = np.sqrt(((xx - 540) / 430) ** 2 + ((yy - 690) / 470) ** 2)
a = np.clip(1.15 - r, 0, 1) ** 0.9
a = np.clip(a + rng.normal(0, 0.12, a.shape) * (a > 0.02), 0, 1)
blob = np.zeros((H, W, 4), np.uint8); blob[..., :3] = TERRACOTA; blob[..., 3] = (a * 255).astype(np.uint8)
img.alpha_composite(Image.fromarray(blob, 'RGBA')); d = ImageDraw.Draw(img)
fa = font('Anton', 260)
d.text((540, 790), 'REZE', font=fa, fill=NAVY, anchor='ms')
wrap(d, 'Como ajudar as almas:', font('Archivo900', 44), 70, 130, 900, NAVY, 52, 'left')
y = 200
for t in ['Participe da Santa Missa por elas.', 'Reze o terço pelos falecidos.']:
    y = wrap(d, t, font('Archivo700', 38), 70, y, 800, NAVY, 46, 'left') + 4
y = 1060
for t in ['De 1º a 8 de novembro: indulgência', 'plenária visitando o cemitério', 'e rezando pelos mortos.']:
    d.text((W - 70, y), t, font=font('PF700I', 40), fill=NAVY, anchor='rs'); y += 50
d.text((W - 70, y + 10), '(com confissão, comunhão e oração pelo Papa)', font=font('MS600', 24), fill=NAVY, anchor='rs')
img = grao(img, 18); dsm_tag(img, 4, cor=NAVY)
save(img, f'{OUT}/04_como_ajudar.jpg')

# ---------------- 5. azul + texto espalhado + bilhete com a oração ----------------
img = Image.new('RGBA', (W, H), BLUE + (255,)); d = ImageDraw.Draw(img)
fb = font('Archivo900', 64)
for t, x, y_ in [('Rezar pelos', 90, 190), ('mortos é', 560, 270), ('amar além', 90, 350), ('da morte.', 600, 430)]:
    d.text((x, y_), t, font=fb, fill=CREAM, anchor='ls')
note = Image.new('RGBA', (760, 520), (244, 230, 160, 255)); nd = ImageDraw.Draw(note)
nd.text((380, 70), 'REZE CONOSCO', font=font('MS700', 24), fill=RED, anchor='ms')
for k, ln in enumerate(['Dai-lhes, Senhor, o descanso eterno,', 'e brilhe para eles a vossa luz.', 'Descansem em paz.', 'Amém.']):
    nd.text((380, 160 + k * 72), ln, font=font('PF700I' if k >= 2 else 'PF500', 42 if k < 2 else 48), fill=NAVY, anchor='ms')
nd.text((380, 480), 'Pai-Nosso, Ave-Maria e Glória pelas almas', font=font('MS600', 22), fill=RED, anchor='ms')
note = note.rotate(-6, expand=True, resample=Image.BICUBIC)
shd = Image.new('RGBA', note.size, (0, 0, 0, 0)); shd.putalpha(note.split()[3].point(lambda v: v * 0.45))
img.alpha_composite(shd.filter(ImageFilter.GaussianBlur(14)), (140 + 14, 560 + 22))
img.alpha_composite(note, (140, 560)); d = ImageDraw.Draw(img)
for t, x, y_ in [('Descansem', 90, 1240), ('em paz.', 620, 1240)]:
    d.text((x, y_), t, font=font('Archivo900', 56), fill=CREAM, anchor='ls')
img = grao(img, 22); dsm_tag(img, 5)
save(img, f'{OUT}/05_oracao.jpg')

ims = [Image.open(f'{OUT}/{f}') for f in sorted(os.listdir(OUT)) if f[:2].isdigit() and f.endswith('.jpg')]
ims[0].convert('RGB').save(f'{OUT}/CARROSSEL_FINADOS_ESTILO_DSM.pdf', save_all=True, append_images=[i.convert('RGB') for i in ims[1:]])
g = Image.new('RGB', (5 * 330, 410), (120, 120, 120))
for i, m in enumerate(ims): g.paste(m.resize((320, 400)), (i * 330, 0))
g.save(f'{OUT}/_chk.png')
print('ok')
