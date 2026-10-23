import sys, json, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
AMARELO = "#ffc46b"
pc = json.load(open(C + "/pomba-camadas.json"))
OUT = C + "/modelos"; os.makedirs(OUT, exist_ok=True)

class Arte:
    def __init__(s): s.l, s.a, s.b = [], [], []
    def pomba(s, cx, top, pw):
        ps = pw / pc["w"]; ph = pc["h"] * ps; px = cx - pw / 2
        tr = f'transform="translate({px:.2f} {top:.2f}) scale({ps:.5f})"'
        s.l.append(f'<path fill="{LARANJA}" fill-rule="evenodd" {tr} d="{pc["laranja"]}"/>')
        s.a.append(f'<path fill="{AMARELO}" fill-rule="evenodd" {tr} d="{pc["amarelo"]}"/>')
        s.b.append(f'<path fill="{BRANCO}" fill-rule="evenodd" {tr} d="{pc["branco"]}"/>')
        return ph
    def texto(s, font, txt, cap, x, base, alinhar="centro", cor=BRANCO, track=.02):
        w = font.width(txt, cap, track)
        x0 = x - w if alinhar == "dir" else (x - w / 2 if alinhar == "centro" else x)
        d, _ = font.path(txt, cap, x0, base, track)
        s.add(f'<path fill="{cor}" d="{d}"/>', cor); return w
    def add(s, el, cor):
        {BRANCO: s.b, LARANJA: s.l, AMARELO: s.a}[cor].append(el)
    def arco(s, font, txt, cap, cx, cy, r, embaixo=False, cor=BRANCO, track=.06):
        gl, wu = font.glyphs(txt, track); k = cap / font.cap; total = wu * k
        for (g, gx) in gl:
            adv = font.hmtx[g][0] * k; sc = gx * k + adv / 2
            if embaixo:
                ang = math.pi / 2 - (sc - total / 2) / (r); rot = math.degrees(ang) - 90; rr = r
            else:
                ang = -math.pi / 2 + (sc - total / 2) / r; rot = math.degrees(ang) + 90; rr = r
            from fontTools.pens.svgPathPen import SVGPathPen
            from fontTools.pens.transformPen import TransformPen
            sp = SVGPathPen(font.gs); font.gs[g].draw(TransformPen(sp, (k, 0, 0, -k, -adv / 2, 0)))
            x, y = cx + rr * math.cos(ang), cy + rr * math.sin(ang)
            s.add(f'<path fill="{cor}" transform="translate({x:.2f} {y:.2f}) rotate({rot:.2f})" d="{sp.getCommands()}"/>', cor)
    def salvar(s, nome, w, h):
        body = s.l + s.a + s.b
        open(f"{OUT}/{nome}.svg", "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">{"".join(body)}</svg>')
        print(nome, w, "x", round(h, 1))

# 1 — SELO REDONDO
a = Arte(); W = 280; cx = W / 2; R = 108; cap = 15; cy = R + cap + 8
a.add(f'<circle cx="{cx}" cy="{cy}" r="{R - 5}" fill="none" stroke="{LARANJA}" stroke-width="1.6"/>', LARANJA)
a.add(f'<circle cx="{cx}" cy="{cy}" r="{R + cap + 3}" fill="none" stroke="{LARANJA}" stroke-width="1.6"/>', LARANJA)
a.arco(anton, "DESCERÁ SOBRE VÓS O ESPÍRITO SANTO", cap, cx, cy, R, False, BRANCO, .1)
a.arco(anton, "E VOS DARÁ FORÇA", cap, cx, cy, R + cap, True, LARANJA, .14)
for sx in (-1, 1):
    a.add(f'<circle cx="{cx + sx * (R + cap / 2):.2f}" cy="{cy - 1:.2f}" r="2.2" fill="{LARANJA}"/>', LARANJA)
ph = 235 * pc["h"] / pc["w"]
a.pomba(cx, cy - ph / 2 - 2, 235)
a.salvar("modelo-1-selo", W, cy + R + cap + 6)

# 2 — PÔSTER CENTRALIZADO
a = Arte(); W = 270; cx = W / 2
ph = a.pomba(cx, 0, 260); y = ph + 6
c1 = fit_cap(anton, "DESCERÁ SOBRE VÓS O", 150, .04); y += c1
a.texto(anton, "DESCERÁ SOBRE VÓS O", c1, cx, y, track=.04)
c2 = fit_cap(anton, "ESPÍRITO SANTO", 150, .02); y += c2 * 1.24
a.texto(anton, "ESPÍRITO SANTO", c2, cx, y); y += 4
c3 = fit_cap(archivo, "E VOS DARÁ FORÇA", 110, .22); y += c3
a.texto(archivo, "E VOS DARÁ FORÇA", c3, cx, y, cor=LARANJA, track=.22)
a.salvar("modelo-2-poster", W, y + 3)

# 3 — BLOCO LATERAL
a = Arte(); W = 300; xl = 8; TW = 130; y = 6
for i, txt in enumerate(["DESCERÁ", "SOBRE VÓS", "O ESPÍRITO", "SANTO"]):
    c = fit_cap(anton, txt, TW, .01); y += c * (1 if i == 0 else 1.24)
    a.texto(anton, txt, c, xl, y, "esq", track=.01)
y += 7; cf = fit_cap(archivo, "E VOS DARÁ FORÇA", TW, .12); y += cf
a.texto(archivo, "E VOS DARÁ FORÇA", cf, xl, y, "esq", LARANJA, .12)
pw = 200; ph = pw * pc["h"] / pc["w"]
a.pomba(xl + TW + pw / 2 - 30, y / 2 - ph / 2, pw)
a.salvar("modelo-3-lateral", W, max(y, y / 2 + ph / 2) + 3)

# 4 — PEITO DISCRETO
a = Arte(); W = 100; cx = W / 2
ph = a.pomba(cx, 0, 96); y = ph + 2
c2 = fit_cap(anton, "ESPÍRITO SANTO", 74, .03); y += c2 * 1.2
a.texto(anton, "ESPÍRITO SANTO", c2, cx, y, track=.03); y += 2.6
c3 = fit_cap(archivo, "E VOS DARÁ FORÇA", 60, .2); y += c3
a.texto(archivo, "E VOS DARÁ FORÇA", c3, cx, y, cor=LARANJA, track=.2)
a.salvar("modelo-4-peito", W, y + 2)
