"""한 장 전체에서 글자 덩어리 줄을 찾는다(표 선은 뺀다). python autolines.py <이름> [밝기기준]"""
import sys, json
import numpy as np
from PIL import Image
from scipy import ndimage as nd
name = sys.argv[1]; th = int(sys.argv[2]) if len(sys.argv) > 2 else 120
a = np.asarray(Image.open('src_%s.png' % name).convert('RGB')).astype(np.int16)
lum = (a[..., 0] * 3 + a[..., 1] * 6 + a[..., 2]) / 10
m = lum < th
lab, n = nd.label(m)
for i, sl in enumerate(nd.find_objects(lab), 1):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if (h <= 5 and w > 40) or (w <= 5 and h > 40) or h > 60 or w > 400: m[lab == i] = False
# 가로로 가까운 글자를 이어 붙여 낱말 덩어리로
k = nd.binary_dilation(m, structure=np.ones((3, 15)))
lab, n = nd.label(k)
out = []
for sl in nd.find_objects(lab):
    y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
    if (y1 - y0) < 7 or (x1 - x0) < 10: continue
    out.append([x0 + 7, y0 + 1, x1 - 7, y1 - 1])
out.sort(key=lambda b: (b[1] // 10, b[0]))
for b in out: print(b)
