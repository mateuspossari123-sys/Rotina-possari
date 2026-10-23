import sys, os, re
sys.argv = [sys.argv[0]]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "modelos.py")).read()
# executa só as definições e o modelo 1
src = src[:src.index("# 2 — PÔSTER")]
ns = {"__file__": __file__}; exec(src, ns)
a = ns["Arte"]  # classe
# o modelo 1 já foi construído no exec; recupera a última instância
art = [v for v in ns.values() if isinstance(v, a)][-1]
OUT = sys.argv[0] and os.environ["OUT"]
W, H = 280, 260
def svg(body, bg=None):
    rect = f'<rect width="{W}" height="{H}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">{rect}{"".join(body)}</svg>'
def preto(body, cor): return [b.replace(f'"{cor}"', '"#000000"') for b in body]
L, A, B = ns["LARANJA"], ns["AMARELO"], ns["BRANCO"]
open(f"{OUT}/frente-selo.svg", "w").write(svg(art.l + art.a + art.b))
open(f"{OUT}/frente-selo-tela-laranja.svg", "w").write(svg(preto(art.l, L), "#ffffff"))
open(f"{OUT}/frente-selo-tela-amarelo.svg", "w").write(svg(preto(art.a, A), "#ffffff"))
open(f"{OUT}/frente-selo-tela-branco.svg", "w").write(svg(preto(art.b, B), "#ffffff"))
print("ok", len(art.l), len(art.a), len(art.b))
