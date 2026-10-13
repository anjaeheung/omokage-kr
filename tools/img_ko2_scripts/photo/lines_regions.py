import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage as nd
name = sys.argv[1]; regs = json.loads(sys.argv[2]); cond = sys.argv[3] if len(sys.argv) > 3 else "(lum<120)"
a = np.asarray(Image.open('src_%s.png' % name).convert('RGB')).astype(np.int16)
r, g, b = a[..., 0], a[..., 1], a[..., 2]; lum = (r * 3 + g * 6 + b) / 10
M = eval(cond)
for key, (X0, Y0, X1, Y1) in regs.items():
    m = M[Y0:Y1, X0:X1].copy()
    lab, n = nd.label(m)
    for i, sl in enumerate(nd.find_objects(lab), 1):
        h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
        if (h <= 6 and w > 60) or (w <= 6 and h > 60) or (h > 30 and w > 120): m[lab == i] = False
    rows = m.sum(1) > 0; y = 0; out = []
    while y < len(rows):
        if rows[y]:
            s = y
            while y < len(rows) and rows[y]: y += 1
            if y - s >= 4:
                cols = np.where(m[s:y].sum(0) > 0)[0]; out.append([X0 + int(cols[0]), Y0 + s, X0 + int(cols[-1]) + 1, Y0 + y])
        y += 1
    mg = []
    for bx in out:
        if mg and bx[1] - mg[-1][3] < 4: p = mg[-1]; mg[-1] = [min(p[0], bx[0]), p[1], max(p[2], bx[2]), bx[3]]
        else: mg.append(bx)
    print(key, json.dumps(mg))
