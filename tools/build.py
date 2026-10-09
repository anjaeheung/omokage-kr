#!/usr/bin/env python3
"""_original → sites/omokage 로 한국어판을 만든다.

  1. 원본을 통째로 복사
  2. i18n.py apply 로 번역 주입
  3. postfix.py 로 주소·글꼴·안내 손질
  4. scan.py 로 남은 일본어 확인
"""
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_original"
OUT = ROOT / "sites/omokage"
SITES = ROOT / "sites"


def run(*args):
    r = subprocess.run([sys.executable] + list(args), cwd=ROOT)
    if r.returncode:
        sys.exit(r.returncode)


def main():
    print("=== 복사")
    if SITES.exists():
        shutil.rmtree(SITES)
    shutil.copytree(SRC, OUT)
    # 사이트 맨 앞(/)에 놓을 것(소개 페이지 그림 등)
    if (ROOT / "overrides_root").exists():
        shutil.copytree(ROOT / "overrides_root", SITES, dirs_exist_ok=True)
    n = sum(1 for p in OUT.rglob("*") if p.is_file())
    over = ROOT / "overrides"
    m = 0
    if over.exists():
        for p in sorted(over.rglob("*")):
            if p.is_file():
                dst = OUT / p.relative_to(over)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, dst)
                m += 1
    print("  원본 %d개 복사, overrides %d개 덮어씀" % (n, m))

    print("\n=== i18n.py apply")
    run("tools/i18n.py", "apply")

    print("\n=== postfix.py")
    run("tools/postfix.py")

    print("\n=== jscheck.py")
    run("tools/jscheck.py")

    print("\n=== scan.py")
    run("tools/scan.py")


if __name__ == "__main__":
    main()
