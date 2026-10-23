"""Figma 로 만든 GPT 이미지(gpt-image-2.5-sunburst) 원본 내려받기.

  python scripts/fetch_figma.py            # 없는 것만 받기
  python scripts/fetch_figma.py --force    # 다시 받기
  python scripts/fetch_figma.py --check    # 접속만 확인 (받지 않음)

assets/figma_urls.json 의 주소는 생성 후 7일 동안만 유효합니다.
저장 위치: 페이지용 → assets/<name>.png · 목업 배경(blank-*) → assets/blank/ · 예비(*-alt) → assets/extra/
www.figma.com 접속이 막혀 있으면 설정 방법을 안내하고 종료코드 2 로 끝납니다.
"""

import argparse
import datetime
import io
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
URLS = ASSETS / "figma_urls.json"
BASE = os.environ.get("HYFLIP_FIGMA_BASE")  # 테스트용: https://www.figma.com 을 이 주소로 바꿈

HELP = """
  ▶ 설정 방법 (한 번만): 세션 상단 클라우드 환경 메뉴 → Edit → 네트워크 접근 → Custom
    허용 도메인에 www.figma.com 추가 (기본 패키지 목록은 유지) → 새 세션에서 다시 실행
"""


def dest(name):
    if name.startswith("blank-"):
        return ASSETS / "blank" / f"{name}.png"
    if name.endswith("-alt"):
        return ASSETS / "extra" / f"{name}.png"
    return ASSETS / f"{name}.png"


def url_of(item):
    u = item["url"]
    return u.replace("https://www.figma.com", BASE.rstrip("/")) if BASE else u


def get(url, timeout=60, tries=4):
    # Figma 는 파이썬 기본 User-Agent 에 빈 202 응답을 주므로 curl 처럼 요청하고, 빈 응답이면 잠시 후 재시도
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8.5.0", "Accept": "image/png,*/*"})
    for i in range(tries):
        with urllib.request.urlopen(req, timeout=timeout) as res:
            data = res.read()
            if res.status == 200 and data:
                return data
        time.sleep(2 ** i)
    raise RuntimeError(f"빈 응답 (HTTP {res.status}) — 잠시 후 다시 실행하세요")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    items = json.loads(URLS.read_text(encoding="utf-8"))["items"]
    expires = min(datetime.date.fromisoformat(i["expires"]) for i in items.values())
    left = (expires - datetime.date.today()).days
    if left < 0:
        print(f"✗ 주소가 만료됐습니다 ({expires}). Figma 에서 다시 생성해야 합니다.")
        return 1
    print(f"주소 유효기간: {expires} 까지 ({left}일 남음)")

    first = next(iter(items.values()))
    try:
        get(url_of(first), timeout=20)
    except urllib.error.HTTPError as e:
        print(f"✗ Figma 응답 오류 {e.code} — 주소가 만료됐거나 잘못됐을 수 있습니다.")
        return 1
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        print(f"✗ www.figma.com 에 접속할 수 없습니다 ({getattr(e, 'reason', e)})." + HELP)
        return 2
    print("✓ www.figma.com 접속 가능")
    if args.check:
        return 0

    ok, skip, failed = 0, 0, []
    for name, item in items.items():
        out = dest(name)
        if out.exists() and not args.force:
            skip += 1
            continue
        try:
            data = get(url_of(item))
            im = Image.open(io.BytesIO(data))
            im.load()
        except Exception as e:  # noqa: BLE001 — 한 장 실패가 전체를 막지 않게
            failed.append(name)
            print(f"✗ {name}: {e}")
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        im.convert("RGB").save(out, "PNG", optimize=True)
        ok += 1
        print(f"✓ {name:<18} {im.size[0]}×{im.size[1]} → {out.relative_to(ROOT)}")
    print(f"\n받음 {ok} · 이미 있음 {skip} · 실패 {len(failed)}")
    if failed:
        print("실패한 것: " + ", ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
