"""글자색 조건으로 줄 상자를 찾는다(가는 가로줄·테두리는 빼고). python find_lines.py <이름> <조건> x0 y0 x1 y1"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd
name, cond = sys.argv[1], sys.argv[2]; X0, Y0, X1, Y1 = map(int, sys.argv[3:7])
a = np.asarray(Image.open('src_%s.png' % name).convert('RGB')).astype(np.int16)
r, g, b = a[..., 0], a[..., 1], a[..., 2]; lum = (r * 3 + g * 6 + b) / 10
m = eval(cond)[Y0:Y1, X0:X1]
# 가로줄 제거: 한 행에서 이어진 칸이 아주 긴 것
lab, n = nd.label(m)
for i, sl in enumerate(nd.find_objects(lab), 1):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if h <= 8 and w > 200: m[lab == i] = False
rows = m.sum(1) > 0
y = 0; out = []
while y < len(rows):
    if rows[y]:
        s = y
        while y < len(rows) and rows[y]: y += 1
        if y - s >= 6:
            cols = np.where(m[s:y].sum(0) > 0)[0]
            out.append((X0 + cols[0], Y0 + s, X0 + cols[-1] + 1, Y0 + y))
    y += 1
# 가까운 줄(점·탁점 분리) 합치기
merged = []
for bx in out:
    if merged and bx[1] - merged[-1][3] < 6:
        p = merged[-1]; merged[-1] = (min(p[0], bx[0]), p[1], max(p[2], bx[2]), bx[3])
    else: merged.append(bx)
for bx in merged: print(list(map(int, bx)), 'h', bx[3] - bx[1])
