import re, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

C = sys.argv[1]; LOGO_SVG = sys.argv[2]
BRANCO = "#ffffff"; LARANJA = "#f47a2a"; CAMISA = "#0b0b0b"

class Font:
    def __init__(self, path):
        self.f = TTFont(path); self.gs = self.f.getGlyphSet(); self.cmap = self.f.getBestCmap()
        self.upm = self.f['head'].unitsPerEm; self.hmtx = self.f['hmtx']
        os2 = self.f['OS/2']; self.cap = getattr(os2, 'sCapHeight', 0) or self.upm * .7
    def glyphs(self, text, tracking=0):
        x = 0; out = []
        for ch in text:
            g = self.cmap.get(ord(ch))
            out.append((g, x)); x += self.hmtx[g][0] + tracking * self.upm
        return out, x - tracking * self.upm
    def path(self, text, cap_mm, x0, baseline, tracking=0):
        """Text as outlined path; cap height = cap_mm; returns d, width_mm."""
        s = cap_mm / self.cap
        gl, w = self.glyphs(text, tracking)
        sp = SVGPathPen(self.gs)
        for g, gx in gl:
            tp = TransformPen(sp, (s, 0, 0, -s, x0 + gx * s, baseline))
            self.gs[g].draw(tp)
        return sp.getCommands(), w * s
    def width(self, text, cap_mm, tracking=0):
        return self.glyphs(text, tracking)[1] * cap_mm / self.cap

anton = Font(C + "/fonts/Anton.ttf"); archivo = Font(C + "/fonts/Archivo-800.ttf")

def fit_cap(font, text, width_mm, tracking=0):
    return width_mm / font.width(text, 1, tracking)

# ---------- Pomba (descendo, asas abertas) em caixa 100 x 60 ----------
def pomba_path(ox, oy, scale):
    # metade direita a partir do topo da cauda; pontos em coordenadas 0..100
    segs = [
        ('L', [(56, 1)]),
        ('L', [(54.5, 15)]),
        ('C', [(57, 17), (59, 18), (62, 17)]),
        ('C', [(74, 12), (86, 5), (99, 1.5)]),
        ('C', [(96, 7), (93, 10.5), (88.5, 13)]),
        ('L', [(92.5, 14)]),
        ('C', [(87, 18.5), (82.5, 21.5), (77.5, 23.5)]),
        ('L', [(81.5, 25.5)]),
        ('C', [(75, 29.5), (68.5, 31.5), (62.5, 32.5)]),
        ('L', [(65.5, 34.5)]),
        ('C', [(61.5, 36.5), (58.5, 37.5), (56.5, 38.5)]),
        ('C', [(57.5, 45), (56.5, 50.5), (53.5, 54)]),
        ('C', [(52.5, 56.5), (51.3, 58.3), (50, 59)]),
    ]
    start = (50, 0)
    # lista de pontos finais para inverter
    pts = [start]; 
    for t, p in segs: pts.append(p[-1])
    T = lambda p: (ox + p[0] * scale, oy + p[1] * scale)
    M = lambda p: (100 - p[0], p[1])
    d = "M%.2f %.2f" % T(start)
    for t, p in segs:
        d += t + " ".join("%.2f %.2f" % T(q) for q in p)
    # volta pela metade esquerda espelhada, em ordem inversa
    for i in range(len(segs) - 1, -1, -1):
        t, p = segs[i]; prev_end = pts[i]
        if t == 'L':
            d += "L%.2f %.2f" % T(M(prev_end))
        else:
            c1, c2, _ = p
            d += "C" + " ".join("%.2f %.2f" % T(M(q)) for q in (c2, c1, prev_end))
    return d + "Z"

# ---------- Globo em traço ----------
def globo(cx, cy, r, sw, cor):
    h = (r * r - (r / 2) ** 2) ** .5
    return (f'<g fill="none" stroke="{cor}" stroke-width="{sw}" stroke-linecap="round">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r*.42:.2f}" ry="{r}"/>'
            f'<line x1="{cx}" y1="{cy-r}" x2="{cx}" y2="{cy+r}"/>'
            f'<line x1="{cx-r}" y1="{cy}" x2="{cx+r}" y2="{cy}"/>'
            f'<line x1="{cx-h:.2f}" y1="{cy-r/2}" x2="{cx+h:.2f}" y2="{cy-r/2}"/>'
            f'<line x1="{cx-h:.2f}" y1="{cy+r/2}" x2="{cx+h:.2f}" y2="{cy+r/2}"/></g>')

# ---------- FRENTE (área 260 mm de largura) ----------
import json
AMARELO = "#ffc46b"
W = 260
partes_b, partes_l, partes_a = [], [], []
pc = json.load(open(C + "/pomba-camadas.json"))
pw = 220; ps = pw / pc["w"]; ph = pc["h"] * ps
px = W / 2 - pw / 2
tr = f'transform="translate({px:.2f} 0) scale({ps:.5f})"'
partes_l.append(f'<path fill="{LARANJA}" fill-rule="evenodd" {tr} d="{pc["laranja"]}"/>')
partes_a.append(f'<path fill="{AMARELO}" fill-rule="evenodd" {tr} d="{pc["amarelo"]}"/>')
partes_b.append(f'<path fill="{BRANCO}" fill-rule="evenodd" {tr} d="{pc["branco"]}"/>')
y = ph + 4
TW = 150
linhas = [("IDE POR TODO O MUNDO", BRANCO), ("E PREGAI O", BRANCO), ("EVANGELHO", LARANJA)]
gap = 3.2
cap_peq = fit_cap(anton, linhas[0][0], TW, .02)
for txt, cor in linhas:
    cap = cap_peq if cor == BRANCO else fit_cap(anton, txt, TW, .02)
    y += cap
    tw = anton.width(txt, cap, .02)
    d, w = anton.path(txt, cap, W / 2 - tw / 2, y, .02)
    (partes_b if cor == BRANCO else partes_l).append(f'<path fill="{cor}" d="{d}"/>')
    y += gap
# globo pequeno + referência na mesma linha
ref = "MARCOS 16,15"; rc = 3.6; gr = 4.2
rw = archivo.width(ref, rc, .3)
total = gr * 2 + 3 + rw
x0 = W / 2 - total / 2
y += 3 + gr
partes_l.append(globo(round(x0 + gr, 2), round(y, 2), gr, 0.9, LARANJA))
d, _ = archivo.path(ref, rc, x0 + gr * 2 + 3, y + rc / 2, .3)
partes_b.append(f'<path fill="{BRANCO}" d="{d}"/>')
H_front = round(y + gr + 3, 1)

# ---------- COSTAS (área 260 mm) ----------
logo_d = re.search(r' d="([^"]*)"', open(LOGO_SVG).read()).group(1)
lw, lh = 497, 594
logo_h = 150; ls = logo_h / lh; lx = W / 2 - lw * ls / 2
costas = [f'<path fill="{BRANCO}" fill-rule="evenodd" transform="translate({lx:.2f} 4) scale({ls:.5f})" d="{logo_d}"/>']
yb = 4 + logo_h + 22
for txt in ("SOCIEDADE IRMÃOS", "DA MISERICÓRDIA"):
    cap = fit_cap(archivo, txt, 200, .12)
    yb += cap
    tw = archivo.width(txt, cap, .12)
    d, _ = archivo.path(txt, cap, W / 2 - tw / 2, yb, .12)
    costas.append(f'<path fill="{BRANCO}" d="{d}"/>')
    yb += 7
H_back = round(yb + 2, 1)

def svg(w, h, body, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">{rect}{"".join(body)}</svg>'

def sep(body, cor):  # fotolito: tinta em preto sobre branco
    return [b.replace(f'"{cor}"', '"#000000"') for b in body]

out = C + "/out"
import os; os.makedirs(out, exist_ok=True)
open(out + "/frente.svg", "w").write(svg(W, H_front, partes_l + partes_a + partes_b))
open(out + "/frente-sobre-preto.svg", "w").write(svg(W, H_front, partes_l + partes_a + partes_b, CAMISA))
open(out + "/frente-tela-amarelo.svg", "w").write(svg(W, H_front, sep(partes_a, AMARELO), "#ffffff"))
open(out + "/frente-tela-branco.svg", "w").write(svg(W, H_front, sep(partes_b, BRANCO), "#ffffff"))
open(out + "/frente-tela-laranja.svg", "w").write(svg(W, H_front, sep(partes_l, LARANJA), "#ffffff"))
open(out + "/costas.svg", "w").write(svg(W, H_back, costas))
open(out + "/costas-sobre-preto.svg", "w").write(svg(W, H_back, costas, CAMISA))
open(out + "/costas-tela-branco.svg", "w").write(svg(W, H_back, sep(costas, BRANCO), "#ffffff"))
print("frente", W, "x", H_front, "mm | costas", W, "x", H_back, "mm")
