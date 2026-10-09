#!/usr/bin/env python3
"""劇団おもかげ(공개 사이트 + 내부 기록 records/)의 번역 대상 문자열을 뽑고, 번역본을 주입해 sites/ 에 쓴다.

원본(_original*)은 절대 고치지 않는다. 카탈로그 위치는 원본 기준이고 apply 는 항상 원본을 읽어
sites/<사이트>/ 에 쓰므로 몇 번을 돌려도 결과가 같다. 카탈로그 키는 "<사이트>/<상대경로>".

추출 대상
  text  HTML 텍스트 노드
  attr  지정 속성값 (alt, title, placeholder, content, data-* 일부 …)
  js    스크립트 문자열 리터럴 '…' "…"   — 주석·이스케이프를 따라가는 토크나이저로 자른다
  tpl   템플릿 리터럴 `…`                — ${…} 는 번역문에서도 그대로 유지해야 한다
  jsx   React(JSX) 태그 사이 텍스트 >…<   — text/babel 스크립트와 JSX 가 든 .js

  extract            카탈로그 생성 (기존 번역은 (키, 원문) 기준으로 보존)
  dump [키 조각...]   미번역 문자열 출력
  set <patch.json>   {키: {인덱스: 한국어}} 반영
  apply              번역 주입 → sites/
  status             진행률
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tplsplit  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "tools/catalog.json"
SITES = {"omokage": "_original"}
OUT = ROOT / "sites"

JA = re.compile(r"[぀-ヿ㐀-鿿ｦ-ﾟ]")
TAG = re.compile(r"<[^>]*>", re.S)
ATTRS = ("placeholder", "alt", "title", "aria-label", "value", "content", "label",
         "data-caption", "data-title", "data-label", "data-text", "data-name", "data-message")
BLOCK = re.compile(r"<(script|style)\b([^>]*)>(.*?)</\1\s*>", re.S | re.I)
JSX_TEXT = re.compile(r">([^<>{}]*[぀-ヿ㐀-鿿ｦ-ﾟ][^<>{}]*)<(?=/?[A-Za-z])")
CODEISH = (");", "=>", "function(", "function ", "document.", "classList", "querySelector",
           "addEventListener", "getElementById", "localStorage", "return ", "const ", "let ", "var ")


def src_path(key):
    site, rel = key.split("/", 1)
    return ROOT / SITES[site] / rel


def out_path(key):
    return OUT / key


def read(path):
    return path.read_bytes().decode("utf-8", errors="replace")


def looks_like_code(piece):
    return any(tok in piece for tok in CODEISH)


def literals(src, offset=0):
    """(kind, start, end) — 문자열·템플릿 리터럴의 내용 위치. 주석은 건너뛴다."""
    out, i, n = [], 0, len(src)
    while i < n:
        if src.startswith("//", i) and (i == 0 or src[i - 1] != ":"):
            j = src.find("\n", i)
            i = n if j < 0 else j
            continue
        if src.startswith("/*", i):
            j = src.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        c = src[i]
        if c in "'\"`":
            j = i + 1
            while j < n:
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == c or (c != "`" and src[j] == "\n"):
                    break
                j += 1
            if j > i + 1:
                out.append(("tpl" if c == "`" else "js", offset + i + 1, offset + min(j, n)))
            i = j + 1
            continue
        i += 1
    return out


def jsx_segments(src, offset, taken):
    out = []
    for m in JSX_TEXT.finditer(src):
        s, e = offset + m.start(1), offset + m.end(1)
        if not any(a < e and s < b for _, a, b in taken):
            out.append(("jsx", s, e))
    return out


def script_segments(src, offset=0, jsx=False):
    segs = literals(src, offset)
    if jsx:
        segs += jsx_segments(src, offset, segs)
    return segs


def segments(html):
    out, blocked = [], []
    for m in BLOCK.finditer(html):
        blocked.append((m.start(), m.end()))
        if m.group(1).lower() == "script":
            is_jsx = "babel" in m.group(2).lower() or "jsx" in m.group(2).lower()
            out.extend(script_segments(m.group(3), m.start(3), jsx=is_jsx))

    def blocked_at(a, b):
        return any(s < b and a < e for s, e in blocked)

    pos = 0
    for m in TAG.finditer(html):
        if m.start() > pos and not blocked_at(pos, m.start()):
            out.append(("text", pos, m.start()))
        tag = m.group(0)
        if not tag.startswith(("</", "<!--")) and not blocked_at(m.start(), m.end()):
            for am in re.finditer(r'\b(' + "|".join(ATTRS) + r')\s*=\s*"([^"]*)"', tag, re.I):
                s = m.start() + am.start(2)
                out.append(("attr", s, s + len(am.group(2))))
        pos = m.end()
    if pos < len(html) and not blocked_at(pos, len(html)):
        out.append(("text", pos, len(html)))
    return sorted(out, key=lambda x: x[1])


def collect(key):
    raw = read(src_path(key))
    if key.endswith(".json"):
        segs = literals(raw)  # 검색 결과 JSON: "comment" 값 등 문자열만
    elif key.endswith(".js"):
        segs = script_segments(raw, 0, jsx=("React" in raw or "</" in raw))
    else:
        raw_no_comments = raw
        segs = segments(raw_no_comments)
    items, seen = [], set()
    expanded = []
    for kind, s, e in segs:
        piece = raw[s:e]
        # JSON 문자열은 데이터라 코드 판별을 하지 않는다 (주소의 incident_document.html 이 "document." 로 오인됐었다)
        if kind in ("js", "tpl") and not key.endswith(".json") and looks_like_code(piece):
            # 코드 같은 글자(style="…;…" 등) 때문에 건너뛰던 문자열 중 HTML 조각은 글자·속성만 따로 뽑는다
            if tplsplit.looks_like_html(piece):
                expanded.extend(tplsplit.html_bits(raw, s, e))
            continue
        expanded.append((kind, s, e))
    for kind, s, e in sorted(expanded, key=lambda x: x[1]):
        if (s, e) in seen:
            continue
        seen.add((s, e))
        piece = raw[s:e]
        if kind == "text" and "<!--" in raw[max(0, s - 4):s]:
            continue
        if piece.strip() and JA.search(piece):
            items.append({"kind": kind, "start": s, "end": e, "ja": piece, "ko": ""})
    return items


# 내부 기록 검색(searchData)은 postfix 가 한국어 검색어·제목으로 통째로 다시 쓴다
EXCLUDE = {"omokage/records/js/script.js"}


def targets():
    keys = []
    for site, folder in SITES.items():
        base = ROOT / folder
        for p in sorted(base.rglob("*")):
            if not p.is_file():
                continue
            rel = p.relative_to(base).as_posix()
            if site + "/" + rel in EXCLUDE:
                continue
            if (p.suffix == ".html"
                    or (p.suffix == ".js" and "vendor/" not in rel and not rel.endswith(".min.js"))
                    or (p.suffix == ".json" and rel.startswith("search/"))):
                keys.append(site + "/" + rel)
    return keys


def load():
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def save(catalog):
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=1), encoding="utf-8")


def cmd_extract():
    old = {}
    if CATALOG.exists():
        for key, items in load().items():
            for it in items:
                if it["ko"]:
                    old[(key, it["ja"])] = it["ko"]
    catalog, total, chars = {}, 0, 0
    per_site = {}
    for key in targets():
        items = collect(key)
        if not items:
            continue
        for it in items:
            it["ko"] = old.get((key, it["ja"]), "")
        catalog[key] = items
        total += len(items)
        n = sum(len(JA.findall(i["ja"])) for i in items)
        chars += n
        site = key.split("/", 1)[0]
        per_site[site] = per_site.get(site, 0) + n
    save(catalog)
    kept = sum(1 for v in catalog.values() for i in v if i["ko"])
    print("파일 %d개 / 문자열 %d개 / 일본어 %d자 %s / 번역 유지 %d개" % (len(catalog), total, chars, per_site, kept))


def cmd_dump():
    wanted = sys.argv[2:]
    for key, items in load().items():
        if wanted and not any(w in key for w in wanted):
            continue
        pending = [(n, it) for n, it in enumerate(items) if not it["ko"]]
        if pending:
            print("\n##### " + key)
            for n, it in pending:
                print("[%d] (%s) %r" % (n, it["kind"], it["ja"]))


def cmd_set():
    patch = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    catalog = load()
    n = 0
    for key, entries in patch.items():
        for idx, ko in entries.items():
            catalog[key][int(idx)]["ko"] = ko
            n += 1
    save(catalog)
    print("%d개 반영" % n)


def cmd_apply():
    catalog = load()
    files = 0
    for key, items in catalog.items():
        raw = read(src_path(key))
        ok = bad = 0
        for it in sorted((i for i in items if i["ko"]), key=lambda x: x["start"], reverse=True):
            if raw[it["start"]:it["end"]] != it["ja"]:
                print("  !! 위치 불일치, 건너뜀: %s @%d" % (key, it["start"]))
                bad += 1
                continue
            raw = raw[:it["start"]] + it["ko"] + raw[it["end"]:]
            ok += 1
        dest = out_path(key)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(raw.encode("utf-8"))
        files += 1
    print("%d개 파일 주입 → %s" % (files, OUT.relative_to(ROOT)))


def cmd_status():
    catalog = load()
    done = sum(1 for v in catalog.values() for i in v if i["ko"])
    total = sum(len(v) for v in catalog.values())
    print("번역 %d/%d" % (done, total))
    for key, items in catalog.items():
        d = sum(1 for i in items if i["ko"])
        if d != len(items):
            print("  %9s  %s" % ("%d/%d" % (d, len(items)), key))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"extract": cmd_extract, "dump": cmd_dump, "set": cmd_set,
     "apply": cmd_apply, "status": cmd_status}[sys.argv[1]]()
