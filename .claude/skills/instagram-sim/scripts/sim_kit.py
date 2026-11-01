"""Kit gráfico da SIM — funções reutilizáveis para montar posts e stories com Pillow.

Uso:
    import sys; sys.path.insert(0, '<pasta da skill>/scripts')
    from sim_kit import *
    img = canvas('feed', 'navy')          # 1080x1350 azul-marinho com granulado
    d = ImageDraw.Draw(img)
    spaced(d, 'DIA DE TODOS OS', font('MS700', 38), 540, 400, 12, CREAM)
    ...
    save(img, 'saida.jpg', textura='linho')

Tudo aqui foi extraído das peças aprovadas (camisetas, Todos os Santos, Fiéis Defuntos).
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(BASE, 'assets')

# ---------- paleta ----------
NAVY = (3, 40, 59)        # #03283B  azul-marinho (principal)
NAVY2 = (8, 28, 42)       # azul quase preto (degradês)
BLUE = (27, 79, 107)      # #1B4F6B  azul secundário
LIGHT = (70, 130, 160)    # #4682A0  azul claro
GOLD = (201, 160, 85)     # #C9A055  dourado
CREAM = (253, 239, 226)   # #FDEFE2  creme
INK = NAVY

FORMATOS = {'feed': (1080, 1350), 'story': (1080, 1920), 'quadrado': (1080, 1080)}

# ---------- fontes ----------
# PF900 = Playfair Display Black (títulos)   PF700I = Playfair itálico (destaques, frases)
# PF500 = Playfair regular (orações, textos longos)   PF800I = Playfair itálico pesado
# MS700/MS600 = Montserrat (sobretítulos espaçados, rodapés, tópicos)
_cache = {}
def font(nome, tam):
    k = (nome, tam)
    if k not in _cache:
        _cache[k] = ImageFont.truetype(os.path.join(ASSETS, 'fonts', f'{nome}.ttf'), tam)
    return _cache[k]

# ---------- fundo ----------
def grain(img, s=5, seed=4):
    w, h = img.size
    a = np.array(img.convert('RGB'), np.float32) + np.random.default_rng(seed).normal(0, s, (h, w, 1))
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert('RGBA')

def canvas(formato='feed', fundo='navy'):
    """fundo: 'navy' (degradê marinho), 'creme' (papel com vinheta), 'azul', 'dourado' ou uma tupla RGB."""
    W, H = FORMATOS[formato]
    if fundo == 'navy':
        yy = np.linspace(0, 1, H)[:, None, None]
        a = np.repeat(np.array(NAVY, np.float32) * (1 - yy) + np.array(NAVY2, np.float32) * yy, W, 1)
        return grain(Image.fromarray(a.astype(np.uint8)), 5)
    if fundo == 'creme':
        img = np.array(grain(Image.new('RGB', (W, H), CREAM), 7), np.float32)
        yy, xx = np.mgrid[0:H, 0:W]
        vig = 1 - 0.18 * np.clip(((xx - W / 2) / (W * .6)) ** 2 + ((yy - H / 2) / (H * .6)) ** 2, 0, 1)
        img[..., :3] *= vig[..., None]
        return Image.fromarray(img.astype(np.uint8))
    cor = {'azul': BLUE, 'claro': LIGHT, 'dourado': GOLD}.get(fundo, fundo)
    return grain(Image.new('RGB', (W, H), cor), 5)

# ---------- foto ----------
def cover(im, w, h, fx=.5, fy=.5):
    """Recorta a foto para preencher w x h, centralizando no ponto (fx, fy) da imagem (0–1)."""
    im = im.convert('RGB')
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x = int(np.clip(im.width * fx - w / 2, 0, im.width - w)); y = int(np.clip(im.height * fy - h / 2, 0, im.height - h))
    return im.crop((x, y, x + w, y + h))

def tratamento(im, estilo='quente'):
    """Tratamento de cor padrão das fotos. 'quente' = missão/alegria; 'frio' = luto/oração; 'pb' = preto e branco suave."""
    im = im.convert('RGB')
    if estilo == 'pb':
        g = ImageEnhance.Contrast(im.convert('L')).enhance(1.08)
        a = np.array(Image.merge('RGB', [g] * 3), np.float32) / 255
        a = a * np.array([1.0, 0.98, 0.94])
    elif estilo == 'frio':
        a = np.array(ImageEnhance.Color(im).enhance(0.45), np.float32) / 255
        a = a * np.array([0.92, 0.97, 1.03]) + np.array([0, 0.01, 0.03])
    else:
        a = np.array(ImageEnhance.Color(im).enhance(0.85), np.float32) / 255
        a = a * np.array([1.03, 0.99, 0.92]) + np.array([0.01, 0.005, 0])
    return Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8)).convert('RGBA')

def degrade(img, cor, y0, y1, forca=235, para_cima=False):
    """Escurece suavemente com 'cor' entre y0 e y1 (para dar legibilidade ao texto sobre foto)."""
    W, H = img.size
    t = np.clip((np.arange(H) - y0) / (y1 - y0), 0, 1)
    if para_cima: t = 1 - np.clip((np.arange(H) - y0) / (y1 - y0), 0, 1)
    ov = np.zeros((H, W, 4), np.uint8); ov[..., :3] = cor; ov[..., 3] = (t[:, None] * forca).astype(np.uint8)
    img.alpha_composite(Image.fromarray(ov, 'RGBA'))
    return img

# ---------- logo ----------
_LOGO = None
def logo(img, cor=CREAM, h=90, x=None, y=60):
    """Logo da SIM (traço) recolorido. x=None centraliza."""
    global _LOGO
    if _LOGO is None: _LOGO = Image.open(os.path.join(ASSETS, 'logo_sim_mask.png')).convert('L')
    m = _LOGO.resize((int(h * _LOGO.width / _LOGO.height), h), Image.LANCZOS)
    lg = Image.new('RGBA', m.size, tuple(cor) + (0,)); lg.putalpha(m)
    img.alpha_composite(lg, (((img.width - lg.width) // 2) if x is None else int(x), int(y)))
    return lg.size

# ---------- texto ----------
def spaced(d, txt, f, cx, base, sp, cor, anchor='m'):
    """Texto com espaçamento entre letras (sobretítulos). anchor 'm' centraliza em cx, 'l' começa em cx."""
    w = sum(f.getlength(c) for c in txt) + sp * (len(txt) - 1)
    x = cx - w / 2 if anchor == 'm' else cx
    for c in txt:
        d.text((x, base), c, font=f, fill=cor, anchor='ls'); x += f.getlength(c) + sp
    return w

def _lines(txt, f, maxw):
    out, cur = [], ''
    for p in txt.split():
        t = (cur + ' ' + p).strip()
        if f.getlength(t) <= maxw: cur = t
        else: out.append(cur); cur = p
    out.append(cur); return out

def wrap(d, txt, f, x, y, maxw, cor, lh, align='center'):
    """Quebra o texto em linhas. align 'center' (x = centro) ou 'left'. Retorna o y depois da última linha."""
    ls = _lines(txt, f, maxw)
    for i, ln in enumerate(ls):
        d.text((x, y + i * lh), ln, font=f, fill=cor, anchor='ms' if align == 'center' else 'ls')
    return y + len(ls) * lh

def sublinhado(img, x0, x1, y, cor=GOLD, esp=5):
    """Sublinhado reto (padrão aprovado — nunca curvo)."""
    ImageDraw.Draw(img).rectangle((x0, y, x1, y + esp), fill=cor)

def sublinhar_palavra(img, frase, palavra, f, cx, base, cor=GOLD, esp=5, gap=26):
    """Sublinha só uma palavra dentro de uma linha centralizada."""
    i = frase.index(palavra)
    x0 = cx - f.getlength(frase) / 2 + f.getlength(frase[:i])
    sublinhado(img, x0 + 4, x0 + f.getlength(palavra) - 4, base + gap, cor, esp)

def cruz(d, cx, cy, h, cor=GOLD, w=4):
    d.rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), fill=cor)
    d.rectangle((cx - h * 0.3, cy - h * 0.22 - w / 2, cx + h * 0.3, cy - h * 0.22 + w / 2), fill=cor)

def moldura(d, W, H, m=60, cor1=NAVY, cor2=GOLD):
    """Moldura dupla de 'santinho'."""
    d.rectangle((m, m, W - m, H - m), outline=cor1, width=4)
    d.rectangle((m + 20, m + 20, W - m - 20, H - m - 20), outline=cor2, width=2)

# ---------- texturas ----------
def linho(img, forca=0.045, soma=0.0, tom=True):
    """Textura de linho. Padrão aprovado: foto -> forca 0.045; fundo liso escuro -> forca 0, soma 0.013, tom False."""
    import cv2
    W, H = img.size
    r = np.random.default_rng(11)
    h, w = H // 3 + 1, W // 3 + 1
    rows = np.repeat(r.normal(0, 1, (h, 1)), w, 1) * (0.7 + 0.3 * cv2.resize(r.normal(0, 1, (h, w // 30 + 2)).astype(np.float32), (w, h)))
    cols = np.repeat(r.normal(0, 1, (1, w)), h, 0) * (0.7 + 0.3 * cv2.resize(r.normal(0, 1, (h // 30 + 2, w)).astype(np.float32), (w, h)))
    t = cv2.resize((0.5 * rows + 0.5 * cols + 0.35 * r.normal(0, 1, (h, w))).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    t = cv2.GaussianBlur(t, (0, 0), 0.9); t = (t - t.mean()) / t.std()
    a = np.array(img.convert('RGB'), np.float32) / 255
    a = a * (1 + forca * t[..., None]) + soma * t[..., None]
    if tom: a = a * 0.98 + np.array([0.02, 0.016, 0.01])
    return Image.fromarray(np.clip(a * 255, 0, 255).astype(np.uint8)).convert('RGBA')

def save(img, caminho, textura=None):
    """textura: None, 'linho' (foto) ou 'linho-sutil' (fundo liso)."""
    if textura == 'linho': img = linho(img)
    elif textura == 'linho-sutil': img = linho(img, 0.0, soma=0.013, tom=False)
    img.convert('RGB').save(caminho, quality=95)
    return caminho
