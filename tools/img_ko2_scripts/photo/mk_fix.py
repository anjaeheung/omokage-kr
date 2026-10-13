"""지운 그림에서 남은 얼룩(분홍 조각·흰 점)을 찾아 고칠 마스크를 만든다. 긴 선(밑줄·테두리)은 건드리지 않는다.
  python mk_fix.py <이름> <조건식> [최대폭]"""
import json, sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd
name, cond = sys.argv[1], sys.argv[2]; maxw = int(sys.argv[3]) if len(sys.argv) > 3 else 150
spec = json.load(open('spec_%s.json' % name, encoding='utf-8'))
a = np.asarray(Image.open('erased_%s.png' % name).convert('RGB')).astype(np.int16)
r, g, b = a[..., 0], a[..., 1], a[..., 2]; lum = (r * 3 + g * 6 + b) / 10
hit = eval(cond, {'r': r, 'g': g, 'b': b, 'lum': lum})
# 지운 자리(원래 마스크) 안만 본다 — 나무·밑줄처럼 손대지 않은 곳은 제외. fix_extra 상자는 통째로 본다.
area = np.asarray(Image.open('mask_%s_rgba.png' % name))[..., 3] > 0
area = nd.binary_dilation(area, iterations=2)
for bx in spec['boxes']:
    if bx.get('nofix'):
        x0, y0, x1, y1 = bx['box']; area[y0-6:y1+6, x0-6:x1+6] = False
for bx in spec.get('fix_extra', []):
    x0, y0, x1, y1 = bx['box']; area[y0:y1, x0:x1] = True
hit &= area
lab, n = nd.label(hit); keep = []
for i, sl in enumerate(nd.find_objects(lab), 1):
    if sl[1].stop - sl[1].start <= maxw: keep.append(i)
m = nd.binary_dilation(np.isin(lab, keep), iterations=4)
rgba = np.zeros(m.shape + (4,), np.uint8); rgba[..., 0] = 255; rgba[..., 3] = m * 255
Image.fromarray(rgba, 'RGBA').save('fix_%s_rgba.png' % name); print('fix px', int(m.sum()), 'blobs', len(keep))
