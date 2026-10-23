import numpy as np, sys
from PIL import Image, ImageDraw
from scipy import ndimage as nd
src, out = sys.argv[1], sys.argv[2]
im = np.array(Image.open(src)).astype(np.float32) / 255
H, W = im.shape[:2]; rng = np.random.default_rng(5)
def hx(h): h = h.lstrip('#'); return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], np.float32) / 255
def burst(cx, cy, R, col, n=90, p=1.0):
    L = Image.new('L', (W, H), 0); d = ImageDraw.Draw(L)
    for i in range(n):
        a = rng.random() * 2 * np.pi; r = R * (0.75 + 0.25 * rng.random())
        sag = r * r / R * .18                       # gravity droop
        steps = 18
        for s in range(steps):
            u0, u1 = s / steps, (s + 1) / steps
            x0, y0 = cx + np.cos(a) * r * u0, cy + np.sin(a) * r * u0 + sag * u0 ** 2
            x1, y1 = cx + np.cos(a) * r * u1, cy + np.sin(a) * r * u1 + sag * u1 ** 2
            d.line([(x0, y0), (x1, y1)], fill=int(255 * (u1 ** 2.2)), width=2)
        x, y = cx + np.cos(a) * r, cy + np.sin(a) * r + sag
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=255)
    m = np.array(L).astype(np.float32) / 255 * p
    glow = nd.gaussian_filter(m, 3) * 1.5 + nd.gaussian_filter(m, 14) * 1.2 + nd.gaussian_filter(m, 60) * 0.6
    C = hx(col)
    return glow[..., None] * C, m[..., None] * (C * .4 + .6)
def trail(x, y0, y1):
    L = Image.new('L', (W, H), 0); d = ImageDraw.Draw(L)
    for k in range(30):
        u = k / 30; d.ellipse([x - 1.5, y1 + (y0 - y1) * u - 1.5, x + 1.5, y1 + (y0 - y1) * u + 1.5], fill=int(200 * (1 - u)))
    m = np.array(L).astype(np.float32) / 255
    return (m + nd.gaussian_filter(m, 4) * 2)[..., None] * hx('#F5CF91')
G = np.zeros_like(im); Cmax = np.zeros_like(im)
for cx, cy, R, col in ((190, 150, 160, '#F5CF91'), (930, 380, 140, '#FDEEE0'), (620, 90, 110, '#4583A2'), (80, 470, 95, '#D9B16B'), (1010, 120, 85, '#F5CF91')):
    g, c = burst(cx, cy, R, col); G += g; Cmax = np.maximum(Cmax, c)

im = 1 - (1 - im) * (1 - G.clip(0, 1)); im = np.maximum(im, Cmax)
Image.fromarray((im.clip(0, 1) * 255).astype(np.uint8)).save(out, quality=93); print('ok')
