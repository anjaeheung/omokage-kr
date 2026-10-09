#!/usr/bin/env python3
"""빌드 결과(sites/jardin/)에 카탈로그 번역만으로는 안 되는 손질을 한다.

  · lang="ja" → "ko", 공유 주소(og:url 등)를 한국어판 주소로
  · 사이트 검색(search.json)의 검색어에 한국어 표기를 더한다 (일본어 원문도 계속 받는다)
  · 다케우치 기록 터미널(data-record-map): 한국어 기록 이름의 해시를 같은 경로로 더한다
  · 스크립트 속 템플릿 안 일본어(choice.js), 안건 번호 「号」 판정은 원문 그대로 둔다
  · 픽션 안내 끝에 번역자 표기
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "sites/jardin"
ORIG_HOST = "https://jardin-redi.com"
KO_HOST = "https://jardin-kr.pages.dev"
FAIL = []


def read(rel):
    return (SITE / rel).read_text(encoding="utf-8")


def write(rel, s):
    (SITE / rel).write_text(s, encoding="utf-8")


def pages():
    return sorted(p.relative_to(SITE).as_posix() for p in SITE.rglob("*.html"))


# ── 터미널 기록 이름: audit-shell.js 와 같은 정규화·해시 (FNV-1a 32bit)
def term_norm(v):
    return re.sub(r"[\s　]+", " ", unicodedata.normalize("NFKC", v).strip()).lower()


def term_hash(v):
    h = 0x811C9DC5
    for ch in term_norm(v):
        h ^= ord(ch)
        h = (h * 0x01000193) & 0xFFFFFFFF
    return "%08x" % h


# 원래 기록 이름 → 한국어로도 받을 이름들 (화면에 보이는 한국어 표기 + 띄어쓰기 변형)
RECORD_KO = {
    "本形町": ["혼가타초"],
    "下原谷戸": ["시모하라야토", "시모하라 야토"],
    "佐久間圭": ["사쿠마 케이", "사쿠마케이"],
    "ジャルダン代々木下原": ["자르댕 요요기시모하라", "자르댕요요기시모하라"],
    "週刊首都": ["주간 수도", "주간수도"],
    "代々木下原駅": ["요요기시모하라역", "요요기시모하라 역"],
    "メールの下書き": ["메일 초안", "메일초안"],
}


def fix_record_maps():
    n = 0
    for rel in pages():
        s = read(rel)
        m = re.search(r'data-record-map="([^"]*)"', s)
        if not m:
            continue
        pairs = json.loads(m.group(1).replace("&quot;", '"'))
        by_hash = dict(pairs)
        add = []
        for ja, kos in RECORD_KO.items():
            target = by_hash.get(term_hash(ja))
            if target is None:
                FAIL.append("record: %s 에 「%s」 기록이 없음" % (rel, ja)); continue
            for ko in kos:
                h = term_hash(ko)
                if h not in by_hash:
                    add.append([h, target]); by_hash[h] = target
        if add:
            new = json.dumps(pairs + add, ensure_ascii=False, separators=(",", ":")).replace('"', "&quot;")
            s = s.replace(m.group(0), 'data-record-map="%s"' % new, 1)
            write(rel, s); n += 1
    print("  record  터미널 한국어 기록 이름 %d개 페이지" % n)


# 사이트 검색어(search.json terms)에 한국어 표기 추가 — 검색은 공백을 지우고 「포함」으로 맞춘다
SEARCH_KO = {
    "竹内直哉": ["다케우치나오야", "다케우치 나오야"],
    "佐久間圭": ["사쿠마케이", "사쿠마 케이"],
    "下原谷戸": ["시모하라야토"],
    "村山": ["무라야마"],
    "村山部長": ["무라야마부장", "무라야마 부장"],
    "京西地盤解析": ["게이세이지반해석", "게이세이 지반해석"],
    "京西地盤解析株式会社": ["게이세이지반해석주식회사", "게이세이 지반해석 주식회사"],
    "2023-042号": ["2023-042호"],
}


def fix_search_json():
    n = 0
    for p in sorted(SITE.rglob("search.json")):
        data = json.loads(p.read_text(encoding="utf-8"))
        for rec in data:
            terms = rec.get("terms", [])
            for t in list(terms):
                for ko in SEARCH_KO.get(t, []):
                    if ko not in terms:
                        terms.append(ko); n += 1
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("  search  한국어 검색어 %d개" % n)


def fix_search_json_text():
    """search.json 의 제목·분류·요약도 한국어로(검색 결과 목록에 보인다)."""
    T = {
        "竹内 直哉｜社員紹介アーカイブ": "다케우치 나오야｜사원 소개 아카이브",
        "社員紹介": "사원 소개",
        "東湾都市開発の竹内直哉は、物件サイトおよび事業管理システムの更新環境移行を担当した後、本形町プロジェクトの副責任者に就任しました。":
            "도완 도시개발의 다케우치 나오야는 매물 사이트와 사업 관리 시스템의 갱신 환경 이전을 맡은 뒤, 혼가타초 프로젝트 부책임자로 취임했습니다.",
        "第3回住民説明会 議事録（2023年7月21日）": "제3회 주민 설명회 회의록(2023년 7월 21일)",
        "住民説明会": "주민 설명회",
        "公開ページです。": "공개 페이지입니다.",
        "佐久間圭｜職員紹介アーカイブ": "사쿠마 케이｜직원 소개 아카이브",
        "職員紹介": "직원 소개",
        "都市整備部で地域資料と住民説明を担当した職員の紹介アーカイブです。": "도시정비부에서 지역 자료와 주민 설명을 맡았던 직원의 소개 아카이브입니다.",
        "第2回住民説明会 議事録（2022年9月3日）": "제2회 주민 설명회 회의록(2022년 9월 3일)",
        "2022年9月3日に開催した本形町二丁目再整備事業の住民説明会議事録です。": "2022년 9월 3일 열린 혼가타초 2초메 재정비 사업 주민 설명회 회의록입니다.",
        "本形町東側 地形・排水調査依頼計画書（2022年9月）": "혼가타초 동쪽 지형·배수 조사 의뢰 계획서(2022년 9월)",
        "防災・安全": "방재·안전",
        "本形町東側の現地調査を東湾都市開発へ要請するための庁内伺いです。": "혼가타초 동쪽 현장 조사를 도완 도시개발에 요청하기 위한 구청 내부 품의서입니다.",
        "本形町二丁目地区 現地調査実施届（受理記録）": "혼가타초 2초메 지구 현장 조사 실시 신고(수리 기록)",
        "住まいとまち": "주거와 마을",
        "東湾都市開発から提出された現地調査実施届と調査報告書の受領状況を掲載しています。": "도완 도시개발이 제출한 현장 조사 실시 신고서와 조사 보고서의 수령 상황을 싣고 있습니다.",
        "案件番号 2023-042号　本形町二丁目地区 地盤・雨水排水予備調査（公開記録）": "안건 번호 2023-042호　혼가타초 2초메 지구 지반·빗물 배수 예비조사(공개 기록)",
        "調査報告書": "조사 보고서",
        "K-Projectで実施した地盤・地下水・雨水排水予備調査の公開記録です。": "K-Project로 실시한 지반·지하수·빗물 배수 예비조사의 공개 기록입니다.",
    }
    left = 0
    for p in sorted(SITE.rglob("search.json")):
        data = json.loads(p.read_text(encoding="utf-8"))
        for rec in data:
            for f in ("title", "section", "safeSnippet", "category"):
                if f in rec and rec[f] in T:
                    rec[f] = T[rec[f]]
                elif f in rec and re.search(r"[぀-ヿ一-鿿]", rec[f]):
                    left += 1; FAIL.append("search 글자 미번역: %s" % rec[f])
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("  search  검색 결과 제목·요약 한국어 (남은 것 %d)" % left)


def fix_lang_and_host():
    n = 0
    for rel in pages():
        s = read(rel); o = s
        s = re.sub(r'<html lang="ja"', '<html lang="ko"', s, count=1)
        s = s.replace('content="ja_JP"', 'content="ko_KR"')
        s = s.replace(ORIG_HOST + "/", KO_HOST + "/")
        if s != o:
            write(rel, s); n += 1
    print("  lang    lang=ko·공유 주소 %d개 페이지" % n)


def fix_scripts():
    rel = "assets/js/choice.js"; s = read(rel)
    old = '"送信しています" : "下書きを削除しています"'
    if old in s:
        write(rel, s.replace(old, '"보내는 중입니다" : "초안을 삭제하는 중입니다"'))
    elif "보내는 중입니다" not in s:
        FAIL.append("choice.js: 전송 문구를 못 찾음")
    # 안건 번호 검색: 판정은 원문 「号」 그대로, 화면에 찍히는 번호만 「호」로
    rel = "assets/js/geo-project-search.js"; s = read(rel)
    old = "meta.textContent = `${match.section} / ${query}`;"
    if old in s:
        write(rel, s.replace(old, "meta.textContent = `${match.section} / ${query.replace(\"号\", \"호\")}`;"))
    elif "query.replace" not in s:
        FAIL.append("geo-project-search.js: 결과 표시 줄을 못 찾음")
    # 휴대폰 화면에서 구청 사이트 「緊急」 배지는 CSS content 로 그린다
    rel = "assets/css/ward.css"; s = read(rel)
    if 'content: "緊急"' in s:
        write(rel, s.replace('content: "緊急"', 'content: "긴급"'))
    print("  script  choice.js 전송·삭제 문구, ward.css 긴급 배지")


def fix_no_xshare():
    """엔딩 뒤 숨은 기사(yamatai)의 「X에 클리어 결과 올리기」 버튼을 뺀다 — 한국 플레이어는 X 를 잘 안 쓴다(10-06 콘테).
    outcome-teaser.js 는 버튼이 없으면 건너뛴다(if (share))."""
    n = 0
    for rel in ("outcomes/send/yamatai/index.html", "outcomes/delete/yamatai/index.html"):
        s = read(rel)
        new = re.sub(r'<a class="outcome-teaser-share"[^>]*>.*?</a>', "", s, count=1, flags=re.S)
        if 'outcome-teaser-share"' in new:
            FAIL.append("xshare: %s 버튼을 못 지움" % rel)
        if new != s:
            write(rel, new); n += 1
    print("  xshare  숨은 기사 X 공유 버튼 뺌 %d곳" % n)


CREDIT =" 한국어 번역: Conte · 원작자 ikempty 님의 허락을 받아 만든 한국어판입니다."


def fix_credit():
    n = 0
    for rel in pages():
        s = read(rel)
        new = re.sub(r'(<p class="fiction-notice">)([^<]*)(</p>)',
                     lambda m: m.group(1) + m.group(2) + ("" if "Conte" in m.group(2) else CREDIT) + m.group(3), s, count=1)
        if new != s:
            write(rel, new); n += 1
    print("  credit  픽션 안내에 번역자 표기 %d개 페이지" % n)


def main():
    fix_lang_and_host()
    fix_record_maps()
    fix_search_json()
    fix_search_json_text()
    fix_scripts()
    fix_credit()
    fix_no_xshare()
    if FAIL:
        print("!! postfix 실패 %d건" % len(FAIL))
        for f in FAIL:
            print("   ", f)
        sys.exit(1)


if __name__ == "__main__":
    main()
