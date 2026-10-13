"""Diphylleia 글자 모양은 그대로 두고, 글자마다 크기·높낮이를 Noto Serif KR 같은 글자의 상자에 맞춘 윤곽선 SVG.
Diphylleia 는 손글씨풍이라 오보다 모가 작고 오·모가 낮게 앉아 간판 글자 크기가 제멋대로 보인다(콘테 10-13).
보통 글꼴의 글자 상자 비율을 빌리면 한 줄이 고르게 보인다.
사용: python mk_svg_even.py 글자 출력.svg [자간(em 비율, 기본 0.06)]"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
text, out = sys.argv[1], sys.argv[2]
track = float(sys.argv[3]) if len(sys.argv) > 3 else 0.06
D = TTFont('C:/Users/user/arg/omokage-kr/_adobe/fonts/Diphylleia-Regular.ttf'); dg = D.getGlyphSet(); dc = D.getBestCmap()
R = TTFont('C:/Windows/Fonts/NotoSerifKR-VF.ttf'); rg = R.getGlyphSet(); rc = R.getBestCmap(); ru = R['head'].unitsPerEm
E = 1000.0; TOP = 0.9 * E  # SVG 위쪽 여백 기준(글꼴 단위 0.9em 을 y=0 으로)
def bounds(gs, name):
    b = BoundsPen(gs); gs[name].draw(b); return b.bounds
paths = []; x = 0
for ch in text:
    x0, y0, x1, y1 = bounds(dg, dc[ord(ch)])
    a0, b0, a1, b1 = (v * E / ru for v in bounds(rg, rc[ord(ch)]))
    sx, sy = (a1 - a0) / (x1 - x0), (b1 - b0) / (y1 - y0)
    sp = SVGPathPen(dg)
    # Diphylleia 상자 → Noto 상자: X = x + a0 + sx*(px - x0), Y(SVG) = TOP - (b0 + sy*(py - y0))
    dg[dc[ord(ch)]].draw(TransformPen(sp, (sx, 0, 0, -sy, x + a0 - sx * x0, TOP - b0 + sy * y0)))
    paths.append(sp.getCommands())
    x += rg[rc[ord(ch)]].width * E / ru + track * E
W = x - track * E; H = 1.1 * E
open(out, 'w', encoding='utf-8').write('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><path fill="#820506" d="%s"/></svg>' % (W, H, W, H, ' '.join(paths)))
print(out, round(W), round(H))
