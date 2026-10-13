"""글자마다 세로 가운데를 맞춘 윤곽선 SVG — Diphylleia 의 오·모(낮음)와 카·게(위아래로 긺)가 한 줄에서 들쭉날쭉해 보이는 것을 고른다.
사용: python mk_svg_balanced.py 글자 출력.svg [긴글자_세로비율 | 공통높이(폰트 단위)]"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
text, out = sys.argv[1], sys.argv[2]
tall = float(sys.argv[3]) if len(sys.argv) > 3 else 0.9
f = TTFont('C:/Users/user/arg/omokage-kr/_adobe/fonts/Diphylleia-Regular.ttf')
gs = f.getGlyphSet(); cm = f.getBestCmap()
CY = 330  # 공통 세로 가운데(폰트 단위)
x = 0; paths = []
for ch in text:
    g = gs[cm[ord(ch)]]; b = BoundsPen(gs); g.draw(b); x0, y0, x1, y1 = b.bounds
    h = y1 - y0; k = (tall / h) if tall > 10 else (tall if h > 800 else 1.0)  # tall>10 이면 모든 글자를 그 높이로
    cy = (y0 + y1) / 2
    sp = SVGPathPen(gs)
    # 폰트 y 위로 → SVG y 아래로: y' = H - (CY + k*(y-cy))
    tp = TransformPen(sp, (1, 0, 0, -k, x, 1000 - CY + k * cy))
    g.draw(tp); paths.append(sp.getCommands())
    x += g.width
W = x
open(out, 'w', encoding='utf-8').write('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="1300" viewBox="0 0 %d 1300"><path fill="#820506" d="%s"/></svg>' % (W, W, ' '.join(paths)))
print(out, W)
