import re, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

C = '/tmp/claude-0/-home-user-Rotina-possari/0d0bb91d-b481-58d0-a72a-79bd41f35a67/scratchpad/camiseta'
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


def globo(cx, cy, r, sw, cor):
    h = (r * r - (r / 2) ** 2) ** .5
    return (f'<g fill="none" stroke="{cor}" stroke-width="{sw}" stroke-linecap="round">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}"/><ellipse cx="{cx}" cy="{cy}" rx="{r*.42:.2f}" ry="{r}"/>'
            f'<line x1="{cx}" y1="{cy-r}" x2="{cx}" y2="{cy+r}"/><line x1="{cx-r}" y1="{cy}" x2="{cx+r}" y2="{cy}"/>'
            f'<line x1="{cx-h:.2f}" y1="{cy-r/2}" x2="{cx+h:.2f}" y2="{cy-r/2}"/><line x1="{cx-h:.2f}" y1="{cy+r/2}" x2="{cx+h:.2f}" y2="{cy+r/2}"/></g>')
