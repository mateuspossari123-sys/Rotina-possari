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
    sd.line([(x, 520), (x, 905)], fill=255, width=9)
for x0, x1 in ((250, 420), (420, 660), (660, 830)):
    sd.line([(x0, 900), (x1, 1060)], fill=255, width=6); sd.line([(x1, 900), (x0, 1060)], fill=255, width=6)
sd.line([(200, 905), (880, 905)], fill=255, width=8)
sd.line([(320, 560), (780, 560)], fill=255, width=7)
for x in (340, 560, 760):
    sd.line([(x, 560), (x, 880)], fill=255, width=6)
stru = np.array(st.filter(ImageFilter.GaussianBlur(.8))) / 255
stru_flat = stru


# ---------------- perspective (side view, like the reference) ----------------
SRC = [(0, 0), (W, 0), (W, H), (0, H)]
DST = [tuple(map(float, p.split(','))) for p in (sys.argv[3] if len(sys.argv) > 3 else '10,215;1075,-40;1095,1215;-10,1095').split(';')]
def coeffs(dst, src):
    A = []; B = []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]; B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float))
CO = coeffs(DST, SRC)
def warp(m):
    im = Image.fromarray((m.clip(0, 1) * 255).astype(np.uint8))
    return np.array(im.transform((W, H), Image.PERSPECTIVE, tuple(CO), Image.BICUBIC)) / 255
logo, t30, anos, word = warp(logo), warp(t30), warp(anos), warp(word)
roof_y_flat = roof_y
st2 = Image.new('L', (W, H), 0); sd2 = ImageDraw.Draw(st2)
# channel backs
def channel(m, grow):
    return nd.binary_dilation(binm(m), iterations=grow)
ch_logo = channel(logo, 16) | channel(t30, 14) | channel(anos, 12)
# join top board: rounded plate behind logo + 30 anos
ch_word = channel(word, 15)

def draw_block(img, ch, depth=26):
    chf = ch.astype(float)
    for k in range(depth, 0, -1):
        sh = np.roll(np.roll(chf, k, 0), -int(k * .8), 1)
        a = sh * (sh > 0)
        col = hx('#03141d') * (0.6 + 0.4 * k / depth)
        img[:] = img * (1 - a[..., None]) + a[..., None] * col
    face = nd.gaussian_filter(chf, 1)
    img[:] = img * (1 - face[..., None]) + face[..., None] * hx('#071820')
    edge = (ch & ~nd.binary_erosion(ch, iterations=2)).astype(float)
    img[:] += nd.gaussian_filter(edge, .8)[..., None] * hx('#4583A2') * .25

# scaffold behind
stru = warp(stru_flat)
# legs from warped frame down to the roof
FW = coeffs(SRC, DST)
def fwd(x, y):
    a, b, c, d, e, f, g, h = FW; den = g * x + h * y + 1
    return ((a * x + b * y + c) / den, (d * x + e * y + f) / den)
lg2 = Image.new('L', (W, H), 0); ld = ImageDraw.Draw(lg2)
for x in (250, 420, 660, 830):
    px, py = fwd(x, 900)
    ld.line([(px, py), (px + (px - 540) * .03, roof_y)], fill=255, width=int(8 + 4 * (px / W)))
legs = np.array(lg2.filter(ImageFilter.GaussianBlur(.8))) / 255
img[:] = img * (1 - legs[..., None]) + legs[..., None] * hx('#041219')
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

# ======== animation (like the reference video) ========
import os
FR = sys.argv[4] if len(sys.argv) > 4 else D + 'fr'
os.makedirs(FR, exist_ok=True)
FPS, DUR = 30, 7.0

def layer(m, tube):
    r = nd.gaussian_filter(ring(m, tube), .7).astype(np.float32)
    glow = (nd.gaussian_filter(r, 2.5) + nd.gaussian_filter(r, 8) + nd.gaussian_filter(r, 22) * .9 + nd.gaussian_filter(r, 60) * .8).astype(np.float32)
    hot = nd.gaussian_filter((nd.binary_erosion(r > .5, iterations=1)).astype(np.float32), .6)
    return glow, r, hot

# split the word into letters to flicker single ones
lab, n = nd.label(binm(word))
cents = nd.center_of_mass(binm(word), lab, range(1, n + 1))
order = np.argsort([c[1] for c in cents])
def pick(idxs):
    m = np.zeros_like(word)
    for i in idxs: m += (lab == order[i] + 1) * word
    return m
nZ = 8 if n > 12 else n // 2           # roughly the 'z' of evangeliza
nO = n - 2                              # the 'O' of SHOW
wz, wo = pick([nZ]), pick([nO])
wrest = (word - wz - wo).clip(0, 1)

EL = {
  'logo': (layer(logo, 3), 'l'), 't30': (layer(t30, 6), 'l'), 'anos': (layer(anos, 4), 'l'),
  'word': (layer(wrest, 6), 't'), 'z': (layer(wz, 6), 't'), 'o': (layer(wo, 6), 't'),
}
CL = {'l': (hx(PAL['logo']), hx(PAL['glow_l'])), 't': (hx(PAL['txt']), hx(PAL['glow_t']))}
base = img.copy()

# bottom text overlay
ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(ov)
mono = font('IBM_Plex_Mono_wght_500.ttf', 25); cre = (253, 238, 224, 255)
def ctext(x, y, s, f): dr.text((x, y), s, font=f, fill=cre, anchor='mm')
ctext(175, 1188, '21 DE NOVEMBRO', mono); ctext(175, 1222, 'SÁBADO · 19H30', mono)
ctext(905, 1188, 'CENTRO DE EVANGELIZAÇÃO', font('IBM_Plex_Mono_wght_500.ttf', 19)); ctext(905, 1222, 'DRACENA · SP', mono)
pf = font('Archivo_wght_700.ttf', 26, 700); pw = dr.textlength('COMUNIDADE SIM', font=pf) + 60
dr.rounded_rectangle([W / 2 - pw / 2, 1180, W / 2 + pw / 2, 1230], radius=25, outline=cre, width=2)
ctext(W / 2, 1205, 'COMUNIDADE SIM', pf)
ova = np.array(ov).astype(np.float32) / 255

vig = (1 - (np.hypot((xx - W / 2) / W, (yy - H / 2) / H) ** 2) * .9)[..., None].astype(np.float32)
spill = (np.exp(-((xx - W / 2) / 420) ** 2) * np.exp(-((yy - roof_y) / 90) ** 2) * (yy > roof_y))[..., None].astype(np.float32)

def fl(t, s): return 1.0 if rnd(int(t * FPS) * 13 + s) > .45 else 0.0
def rnd(k): x = np.sin(k * 127.1 + 311.7) * 43758.5453; return x - np.floor(x)
def win(t, a, b): return a <= t < b
def master(t):
    # two blackouts with flicker in/out, like the reference
    for a, b in ((1.45, 1.95), (3.55, 3.85)):
        if win(t, a - .15, a): return fl(t, 1) * .9
        if win(t, a, b): return 0.0
        if win(t, b, b + .15): return fl(t, 2)
    if t < .25: return fl(t, 3) if t < .2 else 1.0
    return 1.0
def inten(name, t):
    m = master(t)
    if name == 'z' and win(t, 4.3, 5.1): m *= fl(t, 5) * .8
    if name == 'o' and win(t, 5.4, 5.9): m *= fl(t, 7)
    if name == 'anos' and win(t, 2.9, 3.1): m *= .3
    return m * (0.96 + 0.04 * np.sin(t * 50 + hash(name) % 7))

def arc_layer(t, p0, p1, seed):
    im = Image.new('L', (W, H), 0); d = ImageDraw.Draw(im)
    rs = np.random.default_rng(seed * 1000 + int(t * FPS))
    N = 26; pts = []
    for i in range(N + 1):
        u = i / N; x = p0[0] + (p1[0] - p0[0]) * u; y = p0[1] + (p1[1] - p0[1]) * u
        j = 0 if i in (0, N) else rs.normal(0, 22)
        pts.append(fwd(x, y + j))
    d.line(pts, fill=255, width=4, joint='curve')
    for i in rs.choice(N, 3):     # little branches
        x, y = pts[i]; d.line([(x, y), (x + rs.normal(0, 30), y + rs.normal(0, 30))], fill=180, width=2)
    a = np.array(im).astype(np.float32) / 255
    return a, nd.gaussian_filter(a, 4) * 1.6 + nd.gaussian_filter(a, 16) * 1.4

ARCS = [(0.35, 0.85, (60, 800), (1020, 770), 1), (2.25, 2.7, (250, 340), (650, 450), 2), (5.0, 5.35, (520, 800), (1020, 760), 3)]

def star_layer(t):
    a0, a1 = 2.4, 3.6
    if not win(t, a0, a1): return None
    u = (t - a0) / (a1 - a0)
    im = Image.new('L', (W, H), 0); d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = -80, 120, 1180, 330
    hx_, hy_ = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
    for k in range(40):
        f = k / 40; tx, ty = hx_ - (x1 - x0) * .18 * f, hy_ - (y1 - y0) * .18 * f
        d.ellipse([tx - 3 * (1 - f), ty - 3 * (1 - f), tx + 3 * (1 - f), ty + 3 * (1 - f)], fill=int(255 * (1 - f) ** 1.5))
    a = np.array(im).astype(np.float32) / 255
    return a + nd.gaussian_filter(a, 6) * 1.5

for fi in range(int(DUR * FPS)):
    t = fi / FPS
    G = {'l': np.zeros((H, W), np.float32), 't': np.zeros((H, W), np.float32)}
    out = base.astype(np.float32).copy()
    cores = []
    tot = 0
    for name, ((glow, r, hot), g) in EL.items():
        k = inten(name, t); tot += k
        G[g] += glow * k
        cores.append((r, hot, g, k))
    for g in G:
        out = 1 - (1 - out) * (1 - (G[g][..., None] * CL[g][1]).clip(0, 1))
    for r, hot, g, k in cores:
        C = CL[g][0]
        kk = max(k, .09)  # off tubes stay faintly visible (dark glass)
        col = (C * .55 + .45) if k > .1 else (C * .35 + .05)
        out = np.maximum(out, r[..., None] * col * kk)
        if k > .1: out = np.maximum(out, hot[..., None] * (C * .25 + .75) * k)
    out += spill * CL['t'][1] * .18 * (tot / len(EL))
    for a0, a1, p0, p1, sd in ARCS:
        if win(t, a0, a1) and fl(t, 11 + sd) > 0:
            a, g = arc_layer(t, p0, p1, sd)
            out = 1 - (1 - out) * (1 - (g[..., None] * np.array([.85, .9, 1.0])).clip(0, 1))
            out = np.maximum(out, a[..., None])
    s = star_layer(t)
    if s is not None: out = 1 - (1 - out) * (1 - (s[..., None] * hx('#FDEEE0')).clip(0, 1))
    out = out * vig + np.random.default_rng(fi).standard_normal((H, W, 1)).astype(np.float32) * .022
    out = out * (1 - ova[..., 3:]) + ova[..., :3] * ova[..., 3:]
    Image.fromarray((out.clip(0, 1) * 255).astype(np.uint8)).save(f'{FR}/f_{fi:04d}.jpg', quality=92)
print('frames ok')
