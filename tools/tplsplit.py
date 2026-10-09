#!/usr/bin/env python3
r"""스크립트 문자열 속 HTML 조각(innerHTML 템플릿 등)에서 번역할 텍스트·속성값 위치만 잘라낸다.

i18n.py 는 style="…;…" 처럼 코드 같은 글자가 든 문자열을 통째로 건너뛰는데, 이 게임은
잠금 화면·알림 같은 UI 를 `elBody.innerHTML = \`<div style="…">일본어</div>\`` 로 만드는 곳이 많다.
그런 문자열은 통째로 번역하면 태그·스타일이 깨질 위험이 있으므로, 태그 사이 글자와
표시용 속성값(placeholder 등)만 따로 뽑는다. ${…} 자리는 쪼개서 번역 대상에서 뺀다.

  tpltext  태그 사이 글자   — 번역문에 < ` ${ 를 넣으면 안 된다
  tplattr  표시용 속성값    — 번역문에 따옴표 ` ${ 를 넣으면 안 된다
"""
import re

TAG = re.compile(r"<[^>]*>", re.S)
PLACE = re.compile(r"\$\{[^}]*\}")
ATTR = re.compile(r'\b(placeholder|alt|title|aria-label|value|label)\s*=\s*(["\'])([^"\']*)\2', re.I)
JA = re.compile(r"[぀-ヿ㐀-鿿ｦ-ﾟ]")


def looks_like_html(piece):
    return re.search(r"</?[A-Za-z][^>]*>", piece) is not None


def _split_placeholders(src, kind, a, b):
    out, cur = [], a
    for m in PLACE.finditer(src, a, b):
        if m.start() > cur:
            out.append((kind, cur, m.start()))
        cur = m.end()
    if b > cur:
        out.append((kind, cur, b))
    return out


def html_bits(src, s, e):
    """src[s:e] 안의 (kind, start, end) — 일본어가 든 조각만."""
    bits, pos = [], s
    for m in TAG.finditer(src, s, e):
        if m.start() > pos:
            bits += _split_placeholders(src, "tpltext", pos, m.start())
        for am in ATTR.finditer(m.group(0)):
            a = m.start() + am.start(3)
            bits += _split_placeholders(src, "tplattr", a, a + len(am.group(3)))
        pos = m.end()
    if e > pos:
        bits += _split_placeholders(src, "tpltext", pos, e)
    return [(k, a, b) for k, a, b in bits if JA.search(src[a:b])]
