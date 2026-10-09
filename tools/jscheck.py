"""빌드된 JS(파일·HTML 안 인라인 스크립트)를 node --check 로 문법 검사한다."""
import re, subprocess, sys, tempfile
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
SITE = Path(__file__).resolve().parent.parent / "sites/omokage"
bad = 0
tmp = Path(tempfile.gettempdir()) / "omokage_jscheck.js"
jobs = [(p, p.read_text(encoding="utf-8")) for p in SITE.rglob("*.js")]
for p in sorted(SITE.rglob("*.html")):
    for i, m in enumerate(re.finditer(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", p.read_text(encoding="utf-8"), re.S)):
        jobs.append((Path("%s#%d" % (p.name, i)), m.group(1)))
for name, code in jobs:
    tmp.write_text(code, encoding="utf-8")
    r = subprocess.run(["node", "--check", str(tmp)], capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        bad += 1
        print("!! JS 문법 오류:", name, "\n", r.stderr.strip().splitlines()[0:5])
print("JS 검사 %d개, 오류 %d개" % (len(jobs), bad))
sys.exit(1 if bad else 0)
