"""Realistic fireworks over the neon sign frames (behind the sign)."""
import numpy as np, sys, os
from PIL import Image, ImageDraw
from scipy import ndimage as nd

D = os.path.dirname(os.path.abspath(__file__)) + '/'
SRC, OUT = sys.argv[1], sys.argv[2]
ONLY = float(sys.argv[3]) if len(sys.argv) > 3 else None   # render one preview time
os.makedirs(OUT, exist_ok=True)
FPS, DUR, W, H = 30, 12.7, 1080, 1350

def hx(h): h = h.lstrip('#'); return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], np.float32) / 255

# occlusion: sign + its extrusion + scaffold + ground hide the fireworks
occ = np.load(D + 'occ.npy')
ext = occ.copy()
for k in range(1, 27, 2): ext = np.maximum(ext, np.roll(np.roll(occ, k, 0), -int(k * .8), 1))
vis = (1 - ext.clip(0, 1))[..., None]

def src_index(t):
    if t < 7.0: return int(t * FPS)
    if t < 9.0: return int((4.5 + (t - 7.0)) * FPS)
    u = (t - 9.0) % 2.0; u = u if u < 1 else 2 - u
    return min(209, int((6.0 + u) * FPS))

rng = np.random.default_rng(21)
# vibrant colours that sit well with azul-noite + dourado
FW = [
    dict(x=205, y=175, R=215, t=8.7, outer='#FFB43A', inner='#FFF1C9', kind='willow', n=280),  # gold willow
    dict(x=905, y=330, R=190, t=9.45, outer='#FF3E8E', inner='#38E1FF', kind='peony', n=330),  # magenta + cyan
    dict(x=600, y=175, R=165, t=10.2, outer='#2FE0C2', inner='#FFD45E', kind='chrys', n=320),  # turquoise + gold
]
for f in FW:
    z = rng.uniform(-1, 1, f['n']); th = rng.uniform(0, 2 * np.pi, f['n'])
    s = np.sqrt(1 - z ** 2)
    f['dx'], f['dy'] = s * np.cos(th), s * np.sin(th)          # sphere projected → realistic density
    f['inner_mask'] = rng.random(f['n']) < .32
    f['life'] = rng.uniform(1.7, 2.6, f['n']) * (1.25 if f['kind'] == 'willow' else 1)
    f['ph'] = rng.uniform(0, 6.3, f['n'])
    f['y0'] = 1000

def pos(f, tt):
    """position of all stars at time tt after the burst (drag + gravity)."""
    drag = 2.6 if f['kind'] != 'willow' else 1.9
    g = 70 if f['kind'] != 'willow' else 120
    sp = f['R'] * drag
    e = (1 - np.exp(-drag * tt)) / drag
    x = f['x'] + f['dx'] * sp * e
    y = f['y'] + f['dy'] * sp * e + g * (tt - e) / drag * 1.0
    return x, y

def mixw(c, k): return c * k + (1 - k) * np.ones(3, np.float32)

def render(t, base):
    acc = np.zeros((H, W, 3), np.float32)
    smoke = np.zeros((H, W), np.float32)
    for f in FW:
        lt = t - f['t']
        if -0.75 <= lt < 0:  # rising shell with sparks
            u = (lt + .75) / .75; e = 1 - (1 - u) ** 2
            yh = f['y0'] + (f['y'] - f['y0']) * e
            L = Image.new('L', (W, H), 0); d = ImageDraw.Draw(L)
            for k in range(22):
                yy = yh + k * 7 * (1 - u * .5); wob = np.sin(k * .9 + t * 30) * 1.5
                d.ellipse([f['x'] + wob - 2, yy - 2, f['x'] + wob + 2, yy + 2], fill=int(255 * (1 - k / 22) ** 1.5))
            m = np.array(L).astype(np.float32) / 255
            acc += m[..., None] * hx('#FFD9A0') * 1.4
        if 0 <= lt < 3.4:
            Lo = Image.new('L', (W, H), 0); Li = Image.new('L', (W, H), 0)
            do, di = ImageDraw.Draw(Lo), ImageDraw.Draw(Li)
            ntr = 18 if f['kind'] == 'willow' else 14
            dt = .045 if f['kind'] == 'willow' else .038
            pts = [pos(f, max(0, lt - j * dt)) for j in range(ntr)]
            for i in range(f['n']):
                life = f['life'][i]
                if lt > life: continue
                fade = 1 if lt < life * .55 else max(0, 1 - (lt - life * .55) / (life * .45))
                if lt > life * .6 and np.sin(t * 40 + f['ph'][i] * 7) < -.3: fade *= .25   # crackle / twinkle
                dd = di if f['inner_mask'][i] else do
                for j in range(ntr - 1):
                    a = fade * (1 - j / ntr) ** 1.6
                    if a < .02: break
                    dd.line([(pts[j][0][i], pts[j][1][i]), (pts[j + 1][0][i], pts[j + 1][1][i])], fill=int(255 * a), width=2)
                x, y = pts[0][0][i], pts[0][1][i]
                r = 2.2 if lt < 1.2 else 1.6
                dd.ellipse([x - r, y - r, x + r, y + r], fill=int(255 * fade))
            mo = np.array(Lo).astype(np.float32) / 255; mi = np.array(Li).astype(np.float32) / 255
            hot = max(0, 1 - lt / .2) * .7                      # just after the burst everything is white-hot
            co = mixw(hx(f['outer']), 1 - hot * .7); ci = mixw(hx(f['inner']), 1 - hot * .7)
            acc += mo[..., None] * co * 1.6 + mi[..., None] * ci * 1.6
            if lt < .18:                                     # burst flash
                yy, xx = np.ogrid[:H, :W]
                acc += (np.exp(-((xx - f['x']) ** 2 + (yy - f['y']) ** 2) / (2 * 22 ** 2)) * (1 - lt / .18) * .7)[..., None]
            # drifting smoke lit by the burst
            yy, xx = np.ogrid[:H, :W]
            sm = np.exp(-((xx - f['x'] - lt * 12) ** 2 + (yy - f['y'] - lt * 18) ** 2) / (2 * (f['R'] * .75) ** 2))
            smoke += sm * min(1, lt / .6) * .05 * max(0, 1 - lt / 3.4)
    # bloom
    lum = acc
    bloom = nd.gaussian_filter(lum, (1.5, 1.5, 0)) * 1.0 + nd.gaussian_filter(lum, (7, 7, 0)) * .8 + nd.gaussian_filter(lum, (30, 30, 0)) * .35
    sky = nd.gaussian_filter(lum.mean(2), 120)[..., None] * 1.0   # whole sky lights up a little
    fw = (acc + bloom + sky * np.array([.9, .85, 1.0])) * vis
    out = base + smoke[..., None] * np.array([.55, .6, .7]) * (0.2 + nd.gaussian_filter(lum.mean(2), 60)[..., None] * 8).clip(0, 1.5)
    out = 1 - (1 - out) * (1 - fw.clip(0, 1))
    return out

if ONLY is not None:
    i = int(ONLY * FPS)
    base = np.array(Image.open(f'{SRC}/f_{src_index(ONLY):04d}.jpg')).astype(np.float32) / 255
    Image.fromarray((render(ONLY, base).clip(0, 1) * 255).astype(np.uint8)).save(f'{OUT}/preview_{ONLY}.jpg', quality=93)
else:
    for i in range(int(DUR * FPS)):
        t = i / FPS
        base = np.array(Image.open(f'{SRC}/f_{src_index(t):04d}.jpg')).astype(np.float32) / 255
        if t < FW[0]['t'] - .8:
            out = base
        else:
            out = render(t, base)
        Image.fromarray((out.clip(0, 1) * 255).astype(np.uint8)).save(f'{OUT}/f_{i:04d}.jpg', quality=92)
    print('ok')
