import sys, os, numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chuva import render
SRC, OUT = sys.argv[1], sys.argv[2]; os.makedirs(OUT, exist_ok=True)
FPS, DUR = 30, 12.7
def src_index(t):
    if t < 7.0: return int(t * FPS)
    if t < 8.6: return int((4.5 + (t - 7.0)) * FPS)
    u = (t - 8.6) % 2.0; u = u if u < 1 else 2 - u
    return min(209, int((6.0 + u) * FPS))
for i in range(int(DUR * FPS)):
    t = i / FPS
    base = np.array(Image.open(f'{SRC}/f_{src_index(t):04d}.jpg')).astype(np.float32) / 255
    Image.fromarray((render(t, base).clip(0, 1) * 255).astype(np.uint8)).save(f'{OUT}/f_{i:04d}.jpg', quality=92)
print('ok')
