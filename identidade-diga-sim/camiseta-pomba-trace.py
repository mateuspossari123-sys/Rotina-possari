import sys, numpy as np, potrace, json
from PIL import Image, ImageFilter
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
W0, H0 = im.size; K = 3
im = im.resize((W0*K, H0*K), Image.LANCZOS).filter(ImageFilter.GaussianBlur(2.2))
a = np.asarray(im).astype(float)
L = 0.3*a[...,0] + 0.59*a[...,1] + 0.11*a[...,2]
h, w = L.shape; yy, xx = np.mgrid[0:h, 0:w]
# máscara elíptica suave para tirar o fundo das bordas
r = ((xx - w*0.5)/(w*0.47))**2 + ((yy - h*0.5)/(h*0.5))**2
L = L * np.clip((1.15 - r) / 0.3, 0, 1)
def trace(mask):
    plist = potrace.Bitmap(~mask).trace(turdsize=60, alphamax=1.1, opticurve=True, opttolerance=0.4)
    parts = []
    for c in plist:
        s = c.start_point; d = [f"M{s.x/K:.2f} {s.y/K:.2f}"]
        for seg in c.segments:
            if seg.is_corner: d.append(f"L{seg.c.x/K:.2f} {seg.c.y/K:.2f}L{seg.end_point.x/K:.2f} {seg.end_point.y/K:.2f}")
            else: d.append(f"C{seg.c1.x/K:.2f} {seg.c1.y/K:.2f} {seg.c2.x/K:.2f} {seg.c2.y/K:.2f} {seg.end_point.x/K:.2f} {seg.end_point.y/K:.2f}")
        d.append("Z"); parts.append("".join(d))
    return "".join(parts)
layers = {"laranja": trace(L > 62), "amarelo": trace(L > 135), "branco": trace(L > 200)}
json.dump({"w": W0, "h": H0, **layers}, open(out, "w"))
print({k: len(v) for k, v in layers.items()})
