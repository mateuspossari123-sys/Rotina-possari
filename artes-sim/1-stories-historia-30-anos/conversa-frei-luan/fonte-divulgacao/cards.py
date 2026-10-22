"""Name card (Frei Luan) and Kairós card frames, SIM identity."""
import numpy as np, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage as nd

R = '/tmp/claude-0/-home-user-Rotina-possari/fed8fb77-e0d9-58a7-971c-53ef8b1537cf/scratchpad/'
W3 = R + 'ref3/'; F = R + 'drop/fonts/'
W, H, FPS = 1080, 1920, 30
NOITE, OURO, OURO2, AZ, CREME = (3, 40, 58), (245, 207, 145), (217, 177, 107), (69, 131, 162), (253, 238, 224)
rng = np.random.default_rng(3)

def font(n, s, w=None):
    f = ImageFont.truetype(F + n, s)
    if w:
        try: f.set_variation_by_axes([w])
        except Exception: pass
    return f
eo = lambda u: 1 - (1 - min(max(u, 0), 1)) ** 3

def grain(im, k=10, seed=0):
    a = np.array(im).astype(np.int16)
    a += np.random.default_rng(seed).integers(-k, k + 1, (H, W, 1), dtype=np.int16)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))

def torn_strip(text, fnt, pad=(34, 18), seed=1):
    r = np.random.default_rng(seed)
    d0 = ImageDraw.Draw(Image.new('L', (10, 10)))
    b = d0.textbbox((0, 0), text, font=fnt)
    w, h = b[2] - b[0] + pad[0] * 2, b[3] - b[1] + pad[1] * 2
    m = Image.new('L', (w + 20, h + 20), 0); d = ImageDraw.Draw(m)
    top = [(10 + x, 10 + r.integers(0, 7)) for x in range(0, w + 1, 9)]
    bot = [(10 + x, 10 + h - r.integers(0, 7)) for x in range(w, -1, -9)]
    left = [(10 + r.integers(0, 6), 10 + y) for y in range(h, 0, -8)]
    d.polygon(top + [(10 + w - r.integers(0, 6), 10 + y) for y in range(0, h, 8)] + bot + left, fill=255)
    s = Image.new('RGBA', m.size, CREME + (255,)); s.putalpha(m)
    tx = ImageDraw.Draw(s); tx.text((10 + pad[0] - b[0], 10 + pad[1] - b[1]), text, font=fnt, fill=NOITE)
    return s

def sticker(im, border=12):
    a = np.array(im)[..., 3] > 60
    pad = border + 4
    big = np.pad(a, pad)
    sh = nd.binary_dilation(big, iterations=border)
    out = Image.new('RGBA', (big.shape[1], big.shape[0]), (0, 0, 0, 0))
    wh = Image.new('RGBA', out.size, (255, 255, 255, 255)); wh.putalpha(Image.fromarray((nd.gaussian_filter(sh.astype(float), 1) * 255).astype(np.uint8)))
    out.alpha_composite(wh); out.alpha_composite(im, (pad, pad))
    return out

def namecard(outdir, dur=3.8):
    os.makedirs(outdir, exist_ok=True)
    bg = Image.open(W3 + 'p7.png').convert('RGB').resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(18))
    bg = Image.blend(bg, Image.new('RGB', (W, H), NOITE), .62)
    cut = Image.open(W3 + 'cut_b.png').convert('RGBA')
    a = np.array(cut); a[270:, :120, 3] = 0; cut = Image.fromarray(a)     # drop the person at the bottom-left
    cut = cut.resize((int(cut.width * 2.75), int(cut.height * 2.75)), Image.LANCZOS)
    st = sticker(cut, 14).rotate(2, resample=Image.BICUBIC, expand=True)
    s1 = torn_strip('FREI', font('Archivo_wght_900.ttf', 150, 900), seed=2).rotate(4, expand=True, resample=Image.BICUBIC)
    s2 = torn_strip('LUAN', font('Archivo_wght_900.ttf', 150, 900), seed=5).rotate(-3, expand=True, resample=Image.BICUBIC)
    tg = Image.new('RGBA', (560, 70), OURO2 + (255,)); td = ImageDraw.Draw(tg)
    td.text((280, 36), 'PREGADOR DO KAIRÓS', font=font('Archivo_wght_700.ttf', 36, 800), fill=NOITE, anchor='mm')
    tg = tg.rotate(-3, expand=True, resample=Image.BICUBIC)
    lg = Image.open(R + 'neon/logo-sim-ouro.png').convert('RGBA').resize((250, 300), Image.LANCZOS)
    lga = np.array(lg)[..., 3].astype(np.float32) / 255
    halo = Image.new('RGBA', (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(halo)
    hd.ellipse([W / 2 - 330, 330 - 300, W / 2 + 330, 330 + 300], fill=(245, 207, 145, 120)); halo = halo.filter(ImageFilter.GaussianBlur(90))
    rays = Image.new('L', (W, H), 0); rd = ImageDraw.Draw(rays)
    for k in range(18):
        ang = k / 18 * 2 * np.pi
        rd.polygon([(W / 2, 330), (W / 2 + np.cos(ang - .05) * 1400, 330 + np.sin(ang - .05) * 1400), (W / 2 + np.cos(ang + .05) * 1400, 330 + np.sin(ang + .05) * 1400)], fill=60)
    rays = rays.filter(ImageFilter.GaussianBlur(14))
    for i in range(int(dur * FPS)):
        t = i / FPS
        fr = bg.copy().convert('RGBA')
        z = 1 + .04 * t / dur
        k = eo(t / .3); sc = (1.12 - .12 * k) * z
        c2 = st.resize((int(st.width * sc), int(st.height * sc)), Image.LANCZOS)
        fr.alpha_composite(c2, (int(W / 2 - c2.width / 2 + 20), int(H - c2.height + 40)))
        # SIM logo appears with light burst
        ul = eo((t - .25) / .45)
        if ul > 0:
            pulse = max(0, 1 - abs(t - .55) / .35)
            rr = rays.rotate(t * 12, center=(W / 2, 330))
            ra = Image.new('RGBA', (W, H), (245, 207, 145, 0)); ra.putalpha(Image.fromarray((np.array(rr) * (ul * .6 + pulse)).clip(0, 255).astype(np.uint8)))
            fr.alpha_composite(ra)
            hh = halo.copy(); hh.putalpha(Image.fromarray((np.array(halo)[..., 3] * (ul * .8 + pulse * .8)).clip(0, 255).astype(np.uint8))); fr.alpha_composite(hh)
            sc2 = .7 + .3 * ul + .06 * pulse
            l2 = lg.resize((int(250 * sc2), int(300 * sc2)), Image.LANCZOS)
            l2.putalpha(Image.fromarray((np.array(l2)[..., 3] * ul).astype(np.uint8)))
            fr.alpha_composite(l2, (int(W / 2 - l2.width / 2), int(330 - l2.height / 2)))
            if pulse > 0:
                fl = Image.new('RGBA', (W, H), (255, 244, 226, int(120 * pulse ** 2))); fr.alpha_composite(fl)
        # quick colour flashes at the start (like the reference)
        if t < .27:
            col = [OURO2, AZ, OURO2, CREME, AZ, NOITE, OURO2, AZ][int(t * FPS) % 8]
            ov = Image.new('RGBA', (W, H), col + (170,)); fr.alpha_composite(ov)
        for strip, t0, xy in ((s1, .45, (110, 600)), (s2, .6, (300, 770))):
            u = eo((t - t0) / .22)
            if u > 0:
                x = int(xy[0] - (1 - u) * 600)
                fr.alpha_composite(strip, (x, xy[1]))
        u = eo((t - .85) / .2)
        if u > 0:
            tt = tg.copy(); tt.putalpha(Image.fromarray((np.array(tt)[..., 3] * u).astype(np.uint8)))
            fr.alpha_composite(tt, (360, 960))
        grain(fr.convert('RGB'), 9, i).save(f'{outdir}/f_{i:04d}.jpg', quality=92)

def kairos(outdir, dur=4.6):
    os.makedirs(outdir, exist_ok=True)
    y = np.linspace(0, 1, H)[:, None, None]
    base = (np.array(NOITE) * (1.15 - .55 * y) + np.array([1, 8, 14]) * y).clip(0, 255)
    base = np.broadcast_to(base, (H, W, 3)).astype(np.float32)
    logo = Image.open(R + 'neon/logo-sim-ouro.png').convert('RGBA').resize((190, 228), Image.LANCZOS)
    fK = font('Archivo_wght_900.ttf', 200, 900)
    fT = font('Playfair_Display_ital_wght_1_700.ttf', 66)
    fD = font('Archivo_wght_700.ttf', 46, 800)
    fM = font('IBM_Plex_Mono_wght_500.ttf', 30)
    sp = rng.random((70, 4))
    for i in range(int(dur * FPS)):
        t = i / FPS
        a = base.copy()
        im = Image.fromarray(a.astype(np.uint8)).convert('RGBA'); d = ImageDraw.Draw(im)
        # drifting gold sparkles
        for k, (x, yy, s, ph) in enumerate(sp):
            py = (yy * H - t * (30 + 40 * s)) % H; b = .4 + .6 * abs(np.sin(t * 2 + ph * 6))
            r = 1 + 2.5 * s
            d.ellipse([x * W - r, py - r, x * W + r, py + r], fill=OURO + (int(180 * b),))
        glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        gd.ellipse([W / 2 - 420, 760 - 300, W / 2 + 420, 760 + 300], fill=(217, 177, 107, 40))
        im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120)))
        def fade(img, u):
            img = img.copy(); al = np.array(img)[..., 3]; img.putalpha(Image.fromarray((al * u).astype(np.uint8))); return img
        u = eo(t / .5)
        if u > 0: im.alpha_composite(fade(logo, u), (W // 2 - 95, 430 - int(20 * (1 - u))))
        # KAIRÓS with letter reveal
        L = Image.new('RGBA', (W, 330), (0, 0, 0, 0)); ld = ImageDraw.Draw(L)
        txt = 'KAIRÓS'; widths = [ld.textlength(c, font=fK) + 8 for c in txt]; x0 = (W - sum(widths)) / 2; x = x0
        for j, c in enumerate(txt):
            uj = eo((t - .3 - j * .07) / .3)
            if uj > 0: ld.text((x, 300 - int(40 * (1 - uj))), c, font=fK, fill=CREME + (int(255 * uj),), anchor='ls')
            x += widths[j]
        im.alpha_composite(L, (0, 640))
        u = eo((t - .95) / .45)
        d = ImageDraw.Draw(im)
        if u > 0: d.rectangle([W / 2 - 300 * u, 1010, W / 2 + 300 * u, 1014], fill=OURO2 + (255,))
        def ctext(s, f, yy, col, t0):
            u = eo((t - t0) / .4)
            if u > 0:
                l = Image.new('RGBA', (W, 140), (0, 0, 0, 0)); ImageDraw.Draw(l).text((W / 2, 70), s, font=f, fill=col + (int(255 * u),), anchor='mm')
                im.alpha_composite(l, (0, int(yy - 70 + 25 * (1 - u))))
        ctext('30 anos alcançados', fT, 1095, OURO, 1.1)
        ctext('pela misericórdia', fT, 1180, OURO, 1.2)
        ctext('22 DE NOVEMBRO · DOMINGO', fD, 1320, CREME, 1.5)
        ctext('CENTRO DE EVANGELIZAÇÃO SIM · DRACENA-SP', fM, 1390, CREME, 1.65)
        u = eo((t - 1.95) / .4)
        if u > 0:
            pl = Image.new('RGBA', (W, 160), (0, 0, 0, 0)); pd = ImageDraw.Draw(pl)
            pd.rounded_rectangle([W / 2 - 290, 40, W / 2 + 290, 120], radius=40, fill=OURO2 + (int(255 * u),))
            pd.text((W / 2, 81), 'INSCRIÇÕES · LINK NA BIO', font=font('Archivo_wght_700.ttf', 36, 800), fill=NOITE + (int(255 * u),), anchor='mm')
            im.alpha_composite(pl, (0, 1470 + int(20 * (1 - u))))
        grain(im.convert('RGB'), 8, 1000 + i).save(f'{outdir}/f_{i:04d}.jpg', quality=92)

if __name__ == '__main__':
    which = sys.argv[1]
    (namecard if which == 'name' else kairos)(sys.argv[2])
    print('ok', which)
