"""원작 사이트 omokage.site 을 _original/ 로 통째로 받는다(같은 도메인만). 다른 도메인 링크는 따로 적어 둔다."""
import re, sys, os, urllib.request, urllib.parse, time
sys.stdout.reconfigure(encoding="utf-8")
BASE = "https://omokage.site"
OUT = os.path.join(os.path.dirname(__file__), "..", "_original")
# 검색(search.json)으로만 닿는 숨은 페이지도 씨앗으로
HIDDEN = []
seen, queue, other = set(), ["/", "/index.html", "/robots.txt", "/sitemap.xml", "/404.html"] + HIDDEN, set()

def fetch(path):
    url = BASE + urllib.parse.quote(path, safe="/'()%")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read(), r.geturl()
    except Exception as e:
        print("  !", path, e); return None, None

REF = re.compile(r"""(?:src|href|srcset|data-src|poster|action)\s*=\s*["']([^"'#]+)|url\(\s*["']?([^"')]+)""", re.I)
STR = re.compile(r"""["'`]((?:\.{0,2}/)?[A-Za-z0-9_./%-]+\.(?:html|png|jpe?g|gif|webp|svg|mp3|wav|ogg|m4a|mp4|css|js|json|txt|pdf|woff2?|ttf|otf))["'`]""")
while queue:
    p = queue.pop(0).split("#")[0].split("?")[0]
    if p.endswith("/"): p += "index.html"
    if p in seen: continue
    seen.add(p)
    data, final = fetch(p)
    if data is None: continue
    dst = os.path.join(OUT, p.lstrip("/"))
    os.makedirs(os.path.dirname(dst) or OUT, exist_ok=True)
    open(dst, "wb").write(data)
    print(len(data), p)
    if re.search(r"\.(html|js|css|json|xml|txt)$", p):
        t = data.decode("utf-8", "replace")
        cands = set()
        for a, b in REF.findall(t):
            cands.add(a or b)
        cands |= set(STR.findall(t))
        # 터미널 기록 지도(data-record-map): 해시 → ./경로
        for m in re.findall(r'&quot;(\./[^&#]*)&quot;', t):
            cands.add(m)
        for c in cands:
            c = c.strip().rstrip("\,;")
            if not c or c.startswith(("data:", "mailto:", "javascript:", "tel:")): continue
            u = urllib.parse.urlparse(urllib.parse.urljoin(BASE + p, c))
            if u.netloc and u.netloc != "omokage.site":
                other.add(u.scheme + "://" + u.netloc + u.path); continue
            if u.path and u.path not in seen: queue.append(urllib.parse.unquote(u.path))
    time.sleep(0.12)
print("total", len(seen))
print("OTHER DOMAINS:"); [print("  ", o) for o in sorted(other)]
