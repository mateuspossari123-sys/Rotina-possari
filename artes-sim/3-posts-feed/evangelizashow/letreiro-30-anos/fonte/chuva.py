"""Stage-style spark fountains + spark rain + smoke (like the event photo)."""
import numpy as np, sys, os
from PIL import Image, ImageDraw
from scipy import ndimage as nd

D = os.path.dirname(os.path.abspath(__file__)) + '/'
W, H, FPS = 1080, 1350, 30
ROOF = 1105

def hx(h): h = h.lstrip('#'); return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], np.float32) / 255

rng = np.random.default_rng(4)
T0, T1 = float(os.environ.get('T0', 8.6)), float(os.environ.get('T1', 12.0))   # fountains on between T0..T1
EMIT = [(120, ROOF), (370, ROOF), (710, ROOF), (960, ROOF)]
G = 950.0
P = []
for ex, ey in EMIT:
    n = int((T1 - T0) * 430)
    te = np.sort(rng.uniform(T0, T1, n))
    P.append(dict(x0=ex + rng.normal(0, 6, n), y0=np.full(n, ey - 4.0), te=te,
                  vx=rng.normal(0, 130, n), vy=-rng.uniform(820, 1180, n),
                  life=rng.uniform(1.1, 1.9, n), star=rng.random(n) < .18, ph=rng.uniform(0, 6.3, n)))
# spark rain falling from the top of the frame
nr = int((T1 - T0 + 1) * 140)
RAIN = dict(x0=rng.uniform(-40, W + 40, nr), y0=rng.uniform(-60, 380, nr), te=rng.uniform(T0 + .35, T1 + .6, nr),
            vx=rng.normal(0, 25, nr), vy=rng.uniform(120, 320, nr), life=rng.uniform(.9, 1.8, nr),
            star=rng.random(nr) < .35, ph=rng.uniform(0, 6.3, nr))
GOLD, ORANGE, WHITE = hx('#FFD38A'), hx('#FF9B45'), hx('#FFF4E2')

def draw_set(d, ds, p, t, g):
    a = t - p['te']; on = (a >= 0) & (a < p['life'])
    if not on.any(): return
    a = a[on]; x = p['x0'][on] + p['vx'][on] * a; y = p['y0'][on] + p['vy'][on] * a + .5 * g * a * a
    vx = p['vx'][on]; vy = p['vy'][on] + g * a
    u = a / p['life'][on]
    b = (1 - u) ** .8 * (0.65 + .35 * np.sin(t * 50 + p['ph'][on] * 9))
    st = p['star'][on]
    for i in range(len(a)):
        if y[i] > ROOF + 4 or b[i] < .03: continue
        sl = .022                                   # shutter streak
        x0, y0 = x[i] - vx[i] * sl, y[i] - vy[i] * sl
        v = int(255 * min(1, b[i]))
        d.line([(x0, y0), (x[i], y[i])], fill=v, width=2)
        if st[i] and b[i] > .3:                     # star-shaped glint
            r = 6 + 8 * b[i]
            for ang, k in ((0, 1), (1.571, 1), (.785, .45), (2.356, .45)):
                dx, dy = np.cos(ang) * r * k, np.sin(ang) * r * k
                ds.line([(x[i] - dx, y[i] - dy), (x[i] + dx, y[i] + dy)], fill=int(v * k), width=1)

def render(t, base):
    if t < T0 - .05: return base
    L = Image.new('L', (W, H), 0); S = Image.new('L', (W, H), 0)
    d, ds = ImageDraw.Draw(L), ImageDraw.Draw(S)
    for p in P: draw_set(d, ds, p, t, G)
    draw_set(d, ds, RAIN, t, 160)
    m = np.array(L).astype(np.float32) / 255; s = np.array(S).astype(np.float32) / 255
    core = np.maximum(m, s)
    col = core[..., None] * (WHITE * .7 + GOLD * .3)
    glow = (nd.gaussian_filter(m, 2) * 1.3 + nd.gaussian_filter(m, 8) * 1.0 + nd.gaussian_filter(m, 30) * .5)[..., None] * ORANGE \
         + (nd.gaussian_filter(s, 1.5) * 1.2)[..., None] * GOLD
    # smoke clouds at the fountains, lit warm
    yy, xx = np.ogrid[:H, :W]
    k = min(1, (t - T0) / 1.0) * (1 if t < T1 else max(0, 1 - (t - T1) / 1.5))
    smoke = np.zeros((H, W), np.float32)
    for j, (ex, ey) in enumerate(EMIT):
        for q in range(3):
            cx = ex + np.sin(t * .7 + j + q * 2) * 30 + (q - 1) * 40
            cy = ey - 40 - q * 55 - (t - T0) * 12
            r = 45 + q * 18 + (t - T0) * 8
            smoke += np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * r * r)) * .28
    smoke = (smoke * k).clip(0, 1)
    out = base * (1 - smoke[..., None] * .55) + smoke[..., None] * .55 * (hx('#E9EEF5') * .65 + ORANGE * .15)
    # scene lit by the fountains
    lit = nd.gaussian_filter(m, 120)[..., None] * 9 * ORANGE
    out = 1 - (1 - out) * (1 - (glow + lit).clip(0, 1))
    out = np.maximum(out, col)
    return out

if __name__ == '__main__':
    src, outp = sys.argv[1], sys.argv[2]
    t = float(sys.argv[3]) if len(sys.argv) > 3 else 10.0
    base = np.array(Image.open(src)).astype(np.float32) / 255
    Image.fromarray((render(t, base).clip(0, 1) * 255).astype(np.uint8)).save(outp, quality=93)
    print('ok', outp)
