#!/usr/bin/env python3
"""빌드 결과(sites/<사이트>/)에 남은 일본어를 찾는다.

주석(HTML·JS·CSS)은 같은 길이의 공백으로 지우고 본다(줄 번호 유지).
일부러 남긴 것 — 입력 정답(accept 배열), 해시태그, 글리치 문자, 크레딧 — 은 KEEP 으로 뺀다.
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
SITES = ROOT / "sites"
# 가운뎃점 ・ 과 장음 ー 은 한국어판에도 쓰일 수 있어 시작 글자에서 뺀다
JA = re.compile(r"[\u3040-\u30fa\u3400-\u9fff\uff66-\uff9f][\u3000-\u30ff\u3400-\u9fff\uff01-\uff9f\w]*")
KEEP_FILE = ROOT / "tools/scan_keep.txt"


def keep_words():
    words = set()
    if KEEP_FILE.exists():
        words |= {line.strip() for line in KEEP_FILE.read_text(encoding="utf-8").splitlines()
                  if line.strip() and not line.startswith("#")}
    # postfix 가 넣은 한국어 검색어 표의 값(원래 일본어 검색어)
    sys.path.insert(0, str(ROOT / "tools"))
    import postfix  # noqa: E402
    # 판정에 쓰는 원래 일본어 낱말(검색어·터미널 기록 이름)은 한국어와 함께 남겨 둔다
    for k in list(postfix.SEARCH_KO) + list(postfix.RECORD_KO):
        words |= set(JA.findall(k))
    # 카탈로그에서 일부러 번역하지 않은 항목(입력 정답·해시태그·글리치·모지바케 등)의 글자도 뺀다
    cat = json.loads((ROOT / "tools/catalog.json").read_text(encoding="utf-8"))
    for items in cat.values():
        for it in items:
            if not it["ko"] or it["ko"] == it["ja"]:
                words |= set(JA.findall(it["ja"]))
    return words


def blank(m):
    return re.sub(r"[^\n]", " ", m.group(0))


def strip_comments(text, suffix):
    if suffix == ".html":
        text = re.sub(r"<!--.*?-->", blank, text, flags=re.S)
    if suffix in (".html", ".js", ".css"):
        text = re.sub(r"/\*.*?\*/", blank, text, flags=re.S)
    if suffix in (".html", ".js"):
        text = re.sub(r"(?<![:\"'\\])//[^\n]*", blank, text)
    return text


def main():
    keep = keep_words()
    total = 0
    for site_dir in sorted(p for p in SITES.iterdir() if p.is_dir()):
        site_total = 0
        for f in sorted(site_dir.rglob("*")):
            if f.suffix not in (".html", ".js", ".json", ".css") or "vendor" in f.parts:
                continue
            text = strip_comments(f.read_bytes().decode("utf-8", "replace"), f.suffix)
            hits = []
            for ln, line in enumerate(text.split("\n"), 1):
                if ".match(/" in line or "RegExp(" in line:
                    continue  # 입력값을 읽는 정규식(年·月 등)은 화면에 안 나온다
                words = [w for w in JA.findall(line) if not any(w in k for k in keep)]
                if words:
                    hits.append((ln, words))
            if not hits:
                continue
            site_total += len(hits)
            print("--- %s (%d줄)" % (f.relative_to(SITES).as_posix(), len(hits)))
            for ln, words in hits[:12]:
                print("  L%-5d %s" % (ln, " / ".join(words)[:110]))
            if len(hits) > 12:
                print("  … 외 %d줄" % (len(hits) - 12))
        print("== %s: 일본어가 남은 줄 %d" % (site_dir.name, site_total))
        total += site_total
    print("\n전체 일본어가 남은 줄: %d" % total)


if __name__ == "__main__":
    main()
