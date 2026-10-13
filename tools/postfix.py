#!/usr/bin/env python3
"""빌드 결과(sites/omokage/)에 카탈로그 번역만으로는 안 되는 손질을 한다.

  · lang="ja" → "ko", 공유 주소(og:url·og:image)를 한국어판 주소로
  · 한글 글꼴: Shippori Mincho 옆에 Noto Serif KR, Noto Sans JP 앞에 Noto Sans KR
  · 내부 기록 검색(records/js/script.js 의 searchData): 한국어 검색어로만 찾게 하고(일본어 원문 검색어는 받지 않음 — 콘테 「일본어로 치면 나오면 안 되지」),
    띄어쓰기·대소문자를 가리지 않게, 결과 제목·문구를 한국어로
  · 엔딩 두 곳의 「X에 공유」 버튼을 뺀다(한국 플레이어는 X 를 잘 안 쓴다 — 자르댕·아임낫과 같게)
  · 「© うに」 아래 번역자 표기
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "sites/omokage"
ORIG_HOST = "https://omokage.site"
KO_HOST = "https://omokage-kr.pages.dev"
FAIL = []
RECORD_KO = {}  # scan.py 가 찾는 이름(이 작품엔 터미널 기록 없음)


def read(rel):
    return (SITE / rel).read_text(encoding="utf-8")


def write(rel, s):
    (SITE / rel).write_text(s, encoding="utf-8")


def pages():
    return sorted(p.relative_to(SITE).as_posix() for p in SITE.rglob("*.html"))


def fix_lang_and_host():
    n = 0
    for rel in pages():
        s = read(rel); o = s
        s = re.sub(r'<html lang="ja"', '<html lang="ko"', s, count=1)
        s = s.replace('content="' + ORIG_HOST + "/", 'content="' + KO_HOST + "/")
        if s != o:
            write(rel, s); n += 1
    print("  lang    lang=ko·공유 주소 %d개 페이지" % n)


def fix_fonts():
    n = 0
    for rel in pages():
        s = read(rel); o = s
        s = s.replace("family=Shippori+Mincho:wght@400;500;700",
                      "family=Shippori+Mincho:wght@400;500;700&family=Noto+Serif+KR:wght@400;500;700")
        s = re.sub(r"family=Noto\+Sans\+JP:wght@([0-9;]+)", r"family=Noto+Sans+KR:wght@\1&family=Noto+Sans+JP:wght@\1", s)
        s = s.replace('"Hiragino Sans",', '"Hiragino Sans",\n        "Malgun Gothic", "Apple SD Gothic Neo",')
        if s != o:
            write(rel, s); n += 1
    m = 0
    for rel in ("css/style.css", "records/css/style.css"):
        s = read(rel); o = s
        s = s.replace('font-family: "Shippori Mincho", serif;', 'font-family: "Shippori Mincho", "Noto Serif KR", serif;')
        s = re.sub(r'font-family:(\s*)"Noto Sans JP",', r'font-family:\1"Noto Sans KR", "Noto Sans JP",', s)
        if s != o:
            write(rel, s); m += 1
    if m != 2:
        FAIL.append("fonts: CSS 글꼴 줄을 다 못 바꿈(%d/2)" % m)
    print("  font    한글 글꼴 링크 %d개 페이지, CSS %d개" % (n, m))


def fix_hint_fonts():
    """힌트 페이지(hint/)는 글꼴 링크·CSS 모양이 본 사이트와 달라 따로 한글 글꼴을 붙인다."""
    rel = "hint/index.html"; s = read(rel); o = s
    s = s.replace("family=Shippori+Mincho:wght@500;700",
                  "family=Shippori+Mincho:wght@500;700&family=Noto+Serif+KR:wght@500;700&family=Noto+Sans+KR:wght@400;500;700")
    if s == o:
        FAIL.append("hint fonts: 글꼴 링크를 못 바꿈")
    write(rel, s)
    rel = "hint/css/style.css"; c = read(rel); o = c
    c = re.sub(r'"Shippori Mincho",(\s*)', r'"Shippori Mincho",\1"Noto Serif KR",\1', c)
    c = re.sub(r'"Hiragino Sans",(\s*)', r'"Hiragino Sans",\1"Noto Sans KR", "Malgun Gothic", "Apple SD Gothic Neo",\1', c)
    if c == o:
        FAIL.append("hint fonts: CSS 를 못 바꿈")
    write(rel, c)
    print("  hint    힌트 페이지 한글 글꼴")


# 일본어 검색어 → 한국어 검색어(본문에 그대로 보이는 낱말). 띄어쓰기·대소문자는 검색할 때 무시한다.
SEARCH_KO = {
    "同意書": ["동의서"],
    "ライフスタイル": ["라이프스타일"],
    "出荷": ["출하"],
    "劇団員手引き": ["극단원 안내서"],
    "SNSアカウント": ["SNS 계정"],
    "劇団員ページ": ["극단원 페이지"],
    "再演サービス": ["재연 서비스"],
    "アウトドア": ["아웃도어"],
    "家族": ["가족"],
    "信奉者": ["신봉자"],
    "半生": ["반평생"],
    "親友": ["절친"],
    "蘇った": ["되살아났다"],
    "美奈": ["미나"],
    "次期公演": ["차기 공연"],
}
TITLE_KO = {
    "新人役者募集項目": "신인 배우 모집 요강",
    "公演について": "공연에 관하여",
    "出荷記録一覧": "출하 기록 목록",
    "劇団員手引き": "극단원 안내서",
    "卒業後対応マニュアル": "졸업 후 대응 매뉴얼",
    "再演依頼書": "재연 의뢰서",
    "次回再演依頼書": "다음 재연 의뢰서",
}


def fix_search():
    rel = "records/js/script.js"; s = read(rel)
    if "searchNorm" in s:
        return
    titles = dict(TITLE_KO)
    titles.update({"劇団員ページ%03d" % i: "극단원 페이지%03d" % i for i in (1, 2, 3, 6, 9, 14, 22, 23, 26)})
    titles.update({"記録_%d" % i: "기록_%d" % i for i in range(1, 4)})
    block = (
        "\n\n/* 한국어판: 한국어 검색어로만 찾는다(일본어 원문 검색어는 받지 않음), 띄어쓰기·대소문자를 가리지 않는다 */\n"
        "const searchKo = " + json.dumps(SEARCH_KO, ensure_ascii=False) + ";\n"
        "const searchTitleKo = " + json.dumps(titles, ensure_ascii=False) + ";\n"
        "Object.keys(searchKo).forEach(ja => {\n"
        "  searchData[ja].forEach(item => { if (searchTitleKo[item.title]) item.title = searchTitleKo[item.title]; });\n"
        "});\n"
        "const searchNorm = s => s.replace(/[\\s\\u3000]+/g, \"\").toLowerCase();\n"
        "const searchIndex = {};\n"
        "Object.keys(searchKo).forEach(ja => { searchKo[ja].forEach(ko => { searchIndex[searchNorm(ko)] = searchData[ja]; }); });\n"
    )
    m = re.search(r"const searchData = \{.*?\n\};\n", s, re.S)
    if not m:
        FAIL.append("search: searchData 블록을 못 찾음"); return
    s = s[:m.end()] + block + s[m.end():]
    old = "searchData[keyword];"
    if old not in s:
        FAIL.append("search: 검색 줄을 못 찾음"); return
    s = s.replace(old, "searchIndex[searchNorm(keyword)];", 1)
    for ja, ko in (("${result.length}件ヒットしました", "${result.length}건이 검색되었습니다"),
                   ("検索結果がありません", "검색 결과가 없습니다"),
                   ("検索結果", "검색 결과")):
        if ja not in s:
            FAIL.append("search: 문구 「%s」 없음" % ja)
        s = s.replace(ja, ko)
    write(rel, s)
    missing = [ja for ja in SEARCH_KO if ('"%s"' % ja) not in s]
    if missing:
        FAIL.append("search: 원문 검색어 없음 %s" % missing)
    print("  search  내부 기록 검색어 %d개에 한국어 %d개" % (len(SEARCH_KO), sum(map(len, SEARCH_KO.values()))))


def check_search_words():
    """한국어 검색어가 실제 본문(번역문)에 보이는지 — 안 보이면 플레이어가 찾을 수 없다."""
    body = "".join(read(rel) for rel in pages())
    lost = [ko for kos in SEARCH_KO.values() for ko in kos[:1] if ko not in body]
    if lost:
        FAIL.append("search: 본문에 안 보이는 한국어 검색어 %s" % lost)


def fix_no_xshare():
    n = 0
    for rel in ("records/true-end.html", "records/another-end.html"):
        s = read(rel)
        new = re.sub(r'<a\s[^>]*href="https://twitter\.com/intent/tweet[^"]*"[^>]*>.*?</a>', "", s, count=1, flags=re.S)
        if "twitter.com/intent" in new:
            FAIL.append("xshare: %s 버튼을 못 지움" % rel)
        if new != s:
            write(rel, new); n += 1
    print("  xshare  엔딩 X 공유 버튼 뺌 %d곳" % n)


CREDIT = "<p>한국어 번역: Conte · 원작자 うに 님의 허락을 받아 만든 한국어판입니다.</p>"


def fix_credit():
    n = 0
    for rel in pages():
        s = read(rel)
        if "Conte" in s or "<p>© うに</p>" not in s:
            continue
        write(rel, s.replace("<p>© うに</p>", "<p>© うに</p>\n\n    " + CREDIT, 1)); n += 1
    print("  credit  번역자 표기 %d개 페이지" % n)


def fix_keyword_join():
    """원작은 단서 낱말 뒤에서 줄을 바꿔 「蘇った と、」처럼 띄워 보이게 했다. 한국어에선 「되살아났다 고,」가 되어 어색하니
    강조(span) 바로 뒤 조사는 붙인다."""
    rel = "records/member-003.html"; s = read(rel)
    new = re.sub(r'(<span class="keyword">되살아났다</span>)\s+고,', r"\1고,", s)
    if new == s and "되살아났다</span>고," not in s:
        FAIL.append("keyword: member-003 되살아났다 뒤 조사를 못 붙임")
    write(rel, new)
    print("  keyword 단서 낱말 뒤 조사 붙임")


HERO_CSS = """
/* 한국어판: 「극단 오모카게」가 폰에서 「게」만 다음 줄로 떨어지지 않게 — 낱말 중간에서 안 끊고, 좁은 화면에선 글자를 줄여 한 줄에 */
.hero-title { word-break: keep-all; }
@media screen and (max-width: 900px) { .hero-title { font-size: min(2.8rem, 10vw); } }
"""


def fix_hero_title():
    rel = "css/style.css"; s = read(rel)
    if ".hero-title {" not in s:
        FAIL.append("hero: .hero-title 없음"); return
    if "word-break: keep-all" not in s:
        write(rel, s + HERO_CSS)
    print("  hero    큰 제목 줄바꿈 막음")


def main():
    fix_lang_and_host()
    fix_hero_title()
    fix_fonts()
    fix_hint_fonts()
    fix_search()
    fix_no_xshare()
    fix_credit()
    fix_keyword_join()
    check_search_words()
    if FAIL:
        print("!! postfix 실패 %d건" % len(FAIL))
        for f in FAIL:
            print("   ", f)
        sys.exit(1)


if __name__ == "__main__":
    main()
