import re, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

C = sys.argv[1]; LOGO_SVG = sys.argv[2]
PW, SIDE, INSET, R1, R2 = [float(v) for v in sys.argv[3:8]]
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

# ---------- FRENTE "DESCERÁ SOBRE VÓS" ----------
import json
AMARELO = "#ffc46b"
W = 300
partes_b, partes_l, partes_a = [], [], []
pc = json.load(open(C + "/pomba-camadas.json"))
pw = PW; ps = pw / pc["w"]; ph = pc["h"] * ps
px = W / 2 - pw / 2
tr = f'transform="translate({px:.2f} 0) scale({ps:.5f})"'
partes_l.append(f'<path fill="{LARANJA}" fill-rule="evenodd" {tr} d="{pc["laranja"]}"/>')
partes_a.append(f'<path fill="{AMARELO}" fill-rule="evenodd" {tr} d="{pc["amarelo"]}"/>')
partes_b.append(f'<path fill="{BRANCO}" fill-rule="evenodd" {tr} d="{pc["branco"]}"/>')
def palavra(txt, cap, x, base, alinhar, cor=BRANCO, track=.02):
    w = anton.width(txt, cap, track)
    x0 = x - w if alinhar == "dir" else (x - w / 2 if alinhar == "centro" else x)
    d, _ = anton.path(txt, cap, x0, base, track)
    (partes_b if cor == BRANCO else partes_l).append(f'<path fill="{cor}" d="{d}"/>')
COL = SIDE
cap_lado = fit_cap(anton, "DESCERÁ", COL, .02)
xl = px + INSET; xr = px + pw - INSET
palavra("DESCERÁ", cap_lado, xl, ph * R1, "dir")
palavra("SOBRE", cap_lado, xr, ph * R1, "esq")
palavra("VÓS", cap_lado, xl, ph * R2, "dir")
palavra("O", cap_lado, xr, ph * R2, "esq")
y = ph + 2
cap_es = fit_cap(anton, "ESPÍRITO SANTO", 250, .02)
y += cap_es
palavra("ESPÍRITO SANTO", cap_es, W / 2, y, "centro")
y += 4
cap_f = fit_cap(anton, "E VOS DARÁ FORÇA", 170, .02)
y += cap_f
palavra("E VOS DARÁ FORÇA", cap_f, W / 2, y, "centro", LARANJA)
H_front = round(y + 3, 1)
WF = W

# ---------- COSTAS (área 260 mm) ----------
W = 260
logo_d = re.search(r' d="([^"]*)"', open(LOGO_SVG).read()).group(1)
lw, lh = 497, 594
logo_h = 95; ls = logo_h / lh; lx = W / 2 - lw * ls / 2
costas = [f'<path fill="{BRANCO}" fill-rule="evenodd" transform="translate({lx:.2f} 4) scale({ls:.5f})" d="{logo_d}"/>']
yb = 4 + logo_h + 16
for txt in ("SOCIEDADE IRMÃOS DA MISERICÓRDIA",):
    cap = fit_cap(archivo, txt, 240, .12)
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
open(out + "/frente2.svg", "w").write(svg(WF, H_front, partes_l + partes_a + partes_b))
open(out + "/frente2-sobre-preto.svg", "w").write(svg(WF, H_front, partes_l + partes_a + partes_b, CAMISA))
open(out + "/frente2-tela-amarelo.svg", "w").write(svg(WF, H_front, sep(partes_a, AMARELO), "#ffffff"))
open(out + "/frente2-tela-branco.svg", "w").write(svg(WF, H_front, sep(partes_b, BRANCO), "#ffffff"))
open(out + "/frente2-tela-laranja.svg", "w").write(svg(WF, H_front, sep(partes_l, LARANJA), "#ffffff"))
open(out + "/costas.svg", "w").write(svg(W, H_back, costas))
open(out + "/costas-sobre-preto.svg", "w").write(svg(W, H_back, costas, CAMISA))
open(out + "/costas-tela-branco.svg", "w").write(svg(W, H_back, sep(costas, BRANCO), "#ffffff"))
print("frente", WF, "x", H_front, "mm | costas", W, "x", H_back, "mm")
