"""전단 글자 마스크: spec 의 상자 안에서 글자색(조건)에 맞는 픽셀을 찾아 번짐만큼 넓힌다.
  python mk_mask.py <이름>   (spec_<이름>.json 을 읽어 mask_<이름>_rgba.png, mask_<이름>_view.png 를 만든다)"""
import json, sys
import numpy as np
from PIL import Image
from scipy import ndimage as nd
name = sys.argv[1]
spec = json.load(open('spec_%s.json' % name, encoding='utf-8'))
a = np.asarray(Image.open(spec['src']).convert('RGB')).astype(np.int16)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = (r * 3 + g * 6 + b) / 10
m = np.zeros(a.shape[:2], bool)
for bx in spec['boxes']:
    x0, y0, x1, y1 = bx['box']
    sub = np.zeros_like(m)
    cond = eval(bx['cond'], {'r': r, 'g': g, 'b': b, 'lum': lum, 'np': np})
    sub[y0:y1, x0:x1] = cond[y0:y1, x0:x1]
    if bx.get('disk'):
        cx, cy, rr = bx['disk']; yy, xx = np.ogrid[:sub.shape[0], :sub.shape[1]]
        sub &= (xx - cx) ** 2 + (yy - cy) ** 2 <= rr ** 2
    if bx.get('near'):
        nr = eval(bx['near'], {'r': r, 'g': g, 'b': b, 'lum': lum, 'np': np})
        sub &= nd.binary_dilation(nr, iterations=bx.get('nearpx', 8))
    if bx.get('minblob'):
        lab, n = nd.label(sub); sz = nd.sum(sub, lab, range(1, n + 1))
        sub = np.isin(lab, [i + 1 for i, v in enumerate(sz) if v >= bx['minblob']])
    sub = nd.binary_dilation(sub, iterations=bx.get('grow', 4))
    clip = np.zeros_like(m); clip[y0:y1, x0:x1] = True
    m |= sub & clip
rgba = np.zeros(m.shape + (4,), np.uint8); rgba[..., 0] = 255; rgba[..., 3] = m * 255
Image.fromarray(rgba, 'RGBA').save('mask_%s_rgba.png' % name)
v = np.asarray(Image.open(spec['src']).convert('RGB')).copy(); v[m] = (v[m] * 0.3 + np.array([0, 255, 0]) * 0.7).astype(np.uint8)
Image.fromarray(v).save('mask_%s_view.png' % name)
print('mask px', int(m.sum()))
