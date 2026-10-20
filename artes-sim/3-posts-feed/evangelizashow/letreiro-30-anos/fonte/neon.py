import numpy as np, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage as nd

D = '/tmp/claude-0/-home-user-Rotina-possari/fed8fb77-e0d9-58a7-971c-53ef8b1537cf/scratchpad/drop/'
W, H = 1080, 1350
VAR = sys.argv[1] if len(sys.argv) > 1 else 'dourado'
OUT = sys.argv[2] if len(sys.argv) > 2 else D + 'out.jpg'
rng = np.random.default_rng(7)

def hx(h): h = h.lstrip('#'); return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], float) / 255
PAL = {
    'dourado': dict(logo='#F5CF91', txt='#F5CF91', glow_l='#D9B16B', glow_t='#D9B16B'),
    'creme':   dict(logo='#FDEEE0', txt='#FDEEE0', glow_l='#F5CF91', glow_t='#F5CF91'),
    'azul':    dict(logo='#F5CF91', txt='#BFE0F0', glow_l='#D9B16B', glow_t='#4583A2'),
}[VAR]

def font(name, size, wght=None):
    f = ImageFont.truetype(D + 'fonts/' + name, size)
    if wght:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f

# ---------------- sky ----------------
y = np.linspace(0, 1, H)[:, None, None]
top, mid, hor = hx('#020f18'), hx('#03283A'), hx('#164560')
sky = np.where(y < .62, top + (mid - top) * (y / .62), mid + (hor - mid) * ((y - .62) / .2).clip(0, 1))
img = np.broadcast_to(sky, (H, W, 3)).copy()
# soft clouds near horizon
cl = rng.random((H // 20, W // 20)); cl = np.array(Image.fromarray((cl * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40))) / 255
band = np.exp(-((np.linspace(0, 1, H) - .74) / .07) ** 2)[:, None]
img += (cl * band * .10)[..., None] * hx('#4583A2')
# stars
for _ in range(230):
    sx, sy = rng.integers(0, W), rng.integers(0, int(H * .65))
    b = rng.random() ** 3 * .9 + .1
    r = 1 if rng.random() < .85 else 2
    img[max(0, sy - r + 1):sy + r, max(0, sx - r + 1):sx + r] += b * .8
# moon (crescent)
mx, my, mr = 820, 190, 46
yy, xx = np.mgrid[0:H, 0:W]
d1 = np.hypot(xx - mx, yy - my); d2 = np.hypot(xx - mx - 22, yy - my + 14)
moon = ((d1 < mr) & (d2 > mr * .92)).astype(float)
moon = ndimage_blur = nd.gaussian_filter(moon, 1.2)
halo = np.exp(-(d1 / 160) ** 2) * .10
img += moon[..., None] * hx('#FDEEE0') * .95 + halo[..., None] * hx('#F5CF91')

# ---------------- masks ----------------
def text_mask(txt, f, pad=30):
    b = f.getbbox(txt)
    m = Image.new('L', (b[2] - b[0] + pad * 2, b[3] - b[1] + pad * 2), 0)
    ImageDraw.Draw(m).text((pad - b[0], pad - b[1]), txt, font=f, fill=255)
    return np.array(m) / 255

def place(mask, cx, cy):
    out = np.zeros((H, W)); h, w = mask.shape
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    xs, ys = max(0, x0), max(0, y0); xe, ye = min(W, x0 + w), min(H, y0 + h)
    out[ys:ye, xs:xe] = mask[ys - y0:ye - y0, xs - x0:xe - x0]
    return out

# logo
lg = Image.open(D + 'logo-branco.png').convert('RGBA')
LH = 360; lg = lg.resize((int(lg.width * LH / lg.height), LH), Image.LANCZOS)
logo = place(np.array(lg)[..., 3] / 255, 455, 385)
# 30 anos
t30 = place(text_mask('30', font('Archivo_wght_900.ttf', 140, 900)), 700, 365)
anos = place(text_mask('anos', font('Playfair_Display_ital_wght_1_700.ttf', 56)), 700, 465)
# evangelizaSHOW : one word, two fonts
def build(k):
    fe = font('Playfair_Display_ital_wght_1_700.ttf', int(178 * k))
    fs = font('Archivo_wght_900.ttf', int(150 * k), 900)
    me = text_mask('evangeliza', fe); ms = text_mask('SHOW', fs)
    return me, ms, me.shape[1] + ms.shape[1] - 50
k = 1.0
while True:
    me, ms, tw = build(k)
    if tw - 60 <= 990: break
    k *= .97
gap = 0
cx, cy = W / 2, 790
word = place(me, cx - tw / 2 + me.shape[1] / 2, cy) + place(ms, cx + tw / 2 - ms.shape[1] / 2, cy + int(6 * k))
word = word.clip(0, 1)

def binm(m): return m > .5
def ring(m, w):
    b = binm(m); return (b & ~nd.binary_erosion(b, iterations=w)).astype(float)

# ---------------- structure (scaffold) ----------------
st = Image.new('L', (W, H), 0); sd = ImageDraw.Draw(st)
roof_y = 1105
for x in (250, 420, 660, 830):
    sd.line([(x, 520), (x + (x - 540) * .04, roof_y)], fill=255, width=9)
for x0, x1 in ((250, 420), (420, 660), (660, 830)):
    sd.line([(x0, 900), (x1, 1060)], fill=255, width=6); sd.line([(x1, 900), (x0, 1060)], fill=255, width=6)
sd.line([(200, 905), (880, 905)], fill=255, width=8)
sd.line([(320, 560), (780, 560)], fill=255, width=7)
for x in (340, 560, 760):
    sd.line([(x, 560), (x, 880)], fill=255, width=6)
stru = np.array(st.filter(ImageFilter.GaussianBlur(.8))) / 255

# channel backs
def channel(m, grow):
    return nd.binary_dilation(binm(m), iterations=grow)
ch_logo = channel(logo, 16) | channel(t30, 14) | channel(anos, 12)
# join top board: rounded plate behind logo + 30 anos
ch_word = channel(word, 15)

def draw_block(img, ch, depth=18):
    chf = ch.astype(float)
    for k in range(depth, 0, -1):
        sh = np.roll(np.roll(chf, k, 0), -k // 3, 1)
        a = sh * (sh > 0)
        col = hx('#03141d') * (0.6 + 0.4 * k / depth)
        img[:] = img * (1 - a[..., None]) + a[..., None] * col
    face = nd.gaussian_filter(chf, 1)
    img[:] = img * (1 - face[..., None]) + face[..., None] * hx('#071820')
    edge = (ch & ~nd.binary_erosion(ch, iterations=2)).astype(float)
    img[:] += nd.gaussian_filter(edge, .8)[..., None] * hx('#4583A2') * .25

# scaffold behind
img[:] = img * (1 - stru[..., None]) + stru[..., None] * hx('#051720')
draw_block(img, ch_logo)
draw_block(img, ch_word)

# ---------------- roof / parapet ----------------
ry = np.arange(H)[:, None]
treeline = (np.sin(np.arange(W) * .05) * 6 + np.sin(np.arange(W) * .013) * 10 + rng.random(W) * 5 + 1080)
tm = (ry > treeline[None, :]).astype(float)
img[:] = img * (1 - tm[..., None] * .9) + tm[..., None] * .9 * hx('#020c12')
roof = (ry > roof_y).astype(float) * np.ones((1, W))
rg = np.linspace(0, 1, H)[:, None, None]
rcol = hx('#06202d') * (1 - (rg - roof_y / H) * 1.6).clip(.3, 1)
img[:] = img * (1 - roof[..., None]) + roof[..., None] * rcol
img[roof_y:roof_y + 3] += hx('#4583A2') * .35

# ---------------- neon ----------------
def neon(img, m, col, gcol, tube=6, strength=1.0):
    r = ring(m, tube)
    r = nd.gaussian_filter(r, .7)
    C, G = hx(col), hx(gcol)
    glow = (nd.gaussian_filter(r, 2.5) * 1.0 + nd.gaussian_filter(r, 8) * 1.0 + nd.gaussian_filter(r, 22) * .9 + nd.gaussian_filter(r, 60) * .8) * strength
    img[:] = 1 - (1 - img) * (1 - (glow[..., None] * G).clip(0, 1))
    core = r[..., None] * (C * .55 + .45)
    img[:] = np.maximum(img, core)
    hot = nd.gaussian_filter((nd.binary_erosion(r > .5, iterations=1)).astype(float), .6)
    img[:] = np.maximum(img, hot[..., None] * (C * .25 + .75))

neon(img, logo, PAL['logo'], PAL['glow_l'], tube=3)
neon(img, t30, PAL['logo'], PAL['glow_l'], tube=6)
neon(img, anos, PAL['logo'], PAL['glow_l'], tube=4)
neon(img, word, PAL['txt'], PAL['glow_t'], tube=6)

# light spill on roof
spill = np.exp(-((xx - W / 2) / 420) ** 2) * np.exp(-((yy - roof_y) / 90) ** 2) * (yy > roof_y)
img += spill[..., None] * hx(PAL['glow_t']) * .18

# grain + vignette
img += (rng.standard_normal((H, W, 1)) * .025)
v = np.hypot((xx - W / 2) / W, (yy - H / 2) / H)
img *= (1 - (v ** 2) * .9)[..., None]
out = Image.fromarray((img.clip(0, 1) * 255).astype(np.uint8))

# ---------------- bottom info ----------------
dr = ImageDraw.Draw(out)
mono = font('IBM_Plex_Mono_wght_500.ttf', 25)
cre = (253, 238, 224)
def ctext(x, y, s, f, fill, anchor='mm'):
    dr.text((x, y), s, font=f, fill=fill, anchor=anchor)
ctext(175, 1188, '21 DE NOVEMBRO', mono, cre); ctext(175, 1222, 'SÁBADO · 19H30', mono, cre)
ctext(905, 1188, 'CENTRO DE EVANGELIZAÇÃO', font('IBM_Plex_Mono_wght_500.ttf', 19), cre); ctext(905, 1222, 'DRACENA · SP', mono, cre)
pf = font('Archivo_wght_700.ttf', 26, 700)
pw = dr.textlength('COMUNIDADE SIM', font=pf) + 60
dr.rounded_rectangle([W / 2 - pw / 2, 1180, W / 2 + pw / 2, 1230], radius=25, outline=cre, width=2)
ctext(W / 2, 1205, 'COMUNIDADE SIM', pf, cre)
out.save(OUT, quality=93)
print('ok', OUT)
