import numpy as np, sys, os
from PIL import Image, ImageDraw
from scipy import ndimage as nd
SRC, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
FPS, DUR = 30, 12.7
W, H = 1080, 1350
def hx(h): h = h.lstrip('#'); return np.array([int(h[i:i+2], 16) for i in (0, 2, 4)], np.float32) / 255
eo = lambda u: 1 - (1 - min(max(u, 0), 1)) ** 3
# frame map: keep the neon's own animation first, then calm frames for the ending
def src_index(t):
    if t < 7.0: return int(t * FPS)
    if t < 9.5: return int((4.5 + (t - 7.0)) * FPS)
    u = ((t - 9.5) % 2.0); u = u if u < 1 else 2 - u   # ping-pong over 6.0-7.0 s
    return min(209, int((6.0 + u) * FPS))
rng = np.random.default_rng(11)
FW = [dict(x=190, y=150, R=160, c='#F5CF91', t=9.2, y0=470),
      dict(x=930, y=360, R=140, c='#FDEEE0', t=10.0, y0=590),
      dict(x=620, y=95, R=115, c='#4583A2', t=10.8, y0=290)]
for f in FW: f['a'] = rng.random(95) * 2 * np.pi; f['k'] = .75 + .25 * rng.random(95)
for i in range(int(DUR * FPS)):
    t = i / FPS
    im = np.array(Image.open(f'{SRC}/f_{src_index(t):04d}.jpg')).astype(np.float32) / 255
    G = np.zeros_like(im); M = np.zeros_like(im)
    for f in FW:
        C = hx(f['c']); L = Image.new('L', (W, H), 0); d = ImageDraw.Draw(L)
        lt = t - f['t']
        if -0.6 <= lt < 0:                      # rising trail
            u = (lt + .6) / .6; yh = f['y0'] + (f['y'] - f['y0']) * eo(u)
            for k in range(16):
                yy = yh + k * 9; d.ellipse([f['x'] - 2, yy - 2, f['x'] + 2, yy + 2], fill=int(230 * (1 - k / 16)))
            m = np.array(L).astype(np.float32) / 255
            G += (nd.gaussian_filter(m, 4) * 2)[..., None] * hx('#F5CF91'); M = np.maximum(M, m[..., None])
        elif 0 <= lt < 2.2:                     # burst
            ex = eo(lt / .7); fade = max(0, 1 - lt / 2.2) ** 1.4
            for a, k in zip(f['a'], f['k']):
                r = f['R'] * k * ex; sag = 55 * lt ** 2
                x1, y1 = f['x'] + np.cos(a) * r, f['y'] + np.sin(a) * r + sag
                x0, y0 = f['x'] + np.cos(a) * r * .55, f['y'] + np.sin(a) * r * .55 + sag * .6
                d.line([(x0, y0), (x1, y1)], fill=int(150 * fade), width=2)
                sp = 1 if lt < 1.2 or np.sin(i * 3.1 + a * 9) > -.2 else 0   # sparkle at the end
                if sp: d.ellipse([x1 - 3, y1 - 3, x1 + 3, y1 + 3], fill=int(255 * fade))
            m = np.array(L).astype(np.float32) / 255
            flash = max(0, 1 - lt / .25)
            G += (nd.gaussian_filter(m, 3) * 1.5 + nd.gaussian_filter(m, 14) * 1.2 + nd.gaussian_filter(m, 60) * .6)[..., None] * C
            if flash > 0:
                yy, xx = np.ogrid[:H, :W]
                G += (np.exp(-((xx - f['x']) ** 2 + (yy - f['y']) ** 2) / (2 * 120 ** 2)) * .45 * flash)[..., None] * C
            M = np.maximum(M, m[..., None] * (C * .4 + .6))
    im = 1 - (1 - im) * (1 - G.clip(0, 1)); im = np.maximum(im, M)
    Image.fromarray((im.clip(0, 1) * 255).astype(np.uint8)).save(f'{OUT}/f_{i:04d}.jpg', quality=92)
print('ok')
