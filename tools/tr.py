#!/usr/bin/env python3
"""번역 작업 보조 (i18n.py 카탈로그 위에서 동작).

  dump [키 조각...]        미번역 조각을 앞뒤 공백을 걷어 한 줄씩. 줄바꿈은 ⏎.
                           형식: 번호<TAB>종류<TAB>원문   종류: t=본문 a=속성 j=JS문자열 p=템플릿 x=JSX텍스트
  ctx <키> <번호> [글자수]  그 조각 앞뒤 원문 코드를 보여 준다 (입력값과 비교되는 문자열인지 판단용)
  check <패치.json>        반영하지 않고 문맥 깨짐만 검사
  set <패치.json>          {키: {번호: 한국어}} 반영. 원문 앞뒤 공백 복원, ⏎ → 원문 줄바꿈 모양.
                           문맥을 깨는 문자를 막는다: attr 의 " / text 의 < / js 의 따옴표·실제 줄바꿈 /
                           tpl 의 ${…} 불일치 / jsx 의 < > { }
  left                     파일별 남은 개수
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import i18n  # noqa: E402

NL = "⏎"
LETTER = {"text": "t", "attr": "a", "js": "j", "tpl": "p", "jsx": "x", "tpltext": "h", "tplattr": "q"}


def split_ws(s):
    m = re.match(r"(\s*)(.*?)(\s*)\Z", s, re.S)
    return m.group(1), m.group(2), m.group(3)


def view(core):
    return re.sub(r"[ \t]*\n\s*", NL, core)


def cmd_dump(parts):
    for key, items in i18n.load().items():
        if parts and not any(p in key for p in parts):
            continue
        pend = [(n, it) for n, it in enumerate(items) if not it["ko"]]
        if not pend:
            continue
        print("##### %s" % key)
        for n, it in pend:
            print("%d\t%s\t%s" % (n, LETTER[it["kind"]], view(split_ws(it["ja"])[1])))


def cmd_ctx(key, idx, width=160):
    it = i18n.load()[key][int(idx)]
    raw = i18n.read(i18n.src_path(key))
    a, b = max(0, it["start"] - width), min(len(raw), it["end"] + width)
    print(raw[a:it["start"]] + "【" + raw[it["start"]:it["end"]] + "】" + raw[it["end"]:b])


def delimiter(key, it):
    raw = i18n.read(i18n.src_path(key))
    return raw[it["start"] - 1] if it["start"] > 0 else ""


def problem(key, it, body):
    kind = it["kind"]
    if kind == "attr" and '"' in body:
        return '속성값에 " 가 있음'
    if kind == "text" and "<" in body:
        return "본문에 < 가 있음"
    if kind == "jsx" and re.search(r"[<>{}]", body):
        return "JSX 텍스트에 < > { } 가 있음"
    if kind in ("tpltext", "tplattr"):
        if "`" in body or "${" in body:
            return "스크립트 속 HTML 조각에 ` 또는 ${ 가 있음"
        if kind == "tpltext" and "<" in body:
            return "스크립트 속 HTML 글자에 < 가 있음"
        if kind == "tplattr" and re.search(r"[\"']", body):
            return "스크립트 속 HTML 속성값에 따옴표가 있음"
        d = delimiter(key, it)
        if d in "'\"" and d in body:
            return "바깥 문자열 따옴표(%s)가 번역문에 있음" % d
    if kind in ("js", "tpl"):
        d = delimiter(key, it)
        if d and re.search(r"(?<!\\)" + re.escape(d), body):
            return "문자열 따옴표(%s)가 번역문에 있음 (\\%s 로 이스케이프)" % (d, d)
        if kind == "js" and "\n" in body:
            return "JS 문자열에 실제 줄바꿈"
        if kind == "tpl" and sorted(re.findall(r"\$\{[^}]*\}", body)) != sorted(re.findall(r"\$\{[^}]*\}", it["ja"])):
            return "템플릿 ${…} 가 원문과 다름"
    return None


def prepare(key, it, ko):
    lead, core, trail = split_ws(it["ja"])
    m = re.search(r"[ \t]*\n\s*", core)
    return lead, ko.replace(NL, m.group(0) if m else "\n"), trail


def cmd_set(path, write=True):
    patch = json.loads(Path(path).read_text(encoding="utf-8"))
    cat = i18n.load()
    done = bad_n = 0
    for key, entries in patch.items():
        if key.startswith("_"):
            continue
        if key not in cat:
            print("  !! 카탈로그에 없는 파일:", key)
            bad_n += 1
            continue
        for idx, ko in entries.items():
            items, i = cat[key], int(idx)
            if i >= len(items):
                print("  !! 범위 초과 %s[%s]" % (key, idx))
                bad_n += 1
                continue
            it = items[i]
            lead, body, trail = prepare(key, it, ko)
            bad = problem(key, it, body)
            if bad:
                print("  !! %s[%s] — %s" % (key, idx, bad))
                bad_n += 1
                continue
            if write:
                it["ko"] = lead + body + trail
            done += 1
    if write:
        i18n.save(cat)
        print("%d개 반영, 문제 %d개" % (done, bad_n))
    else:
        print("검사: 통과 %d개, 문제 %d개" % (done, bad_n))


def cmd_left():
    cat = i18n.load()
    tot = sum(len(v) for v in cat.values())
    done = sum(1 for v in cat.values() for it in v if it["ko"])
    print("번역 %d/%d" % (done, tot))
    for key, items in cat.items():
        n = sum(1 for it in items if not it["ko"])
        if n:
            print("%6d  %s" % (n, key))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "dump":
        cmd_dump(sys.argv[2:])
    elif cmd == "ctx":
        cmd_ctx(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 160)
    elif cmd == "check":
        cmd_set(sys.argv[2], write=False)
    elif cmd == "set":
        cmd_set(sys.argv[2])
    elif cmd == "left":
        cmd_left()
