"""HY FLIP 이미지 생성기 — OpenAI Images API (gpt-image-2).

사용법
  export OPENAI_API_KEY=...            # 환경변수로만 받음 (코드·채팅에 키 적지 말 것)
  python gen_image.py --check          # 키·네트워크 진단 (생성 안 함, 비용 없음)
  python gen_image.py --list           # 생성할 목록 보기 (✓ = 이미 있음)
  python gen_image.py --all            # assets/manifest.json 전체 생성 (이미 있으면 건너뜀)
  python gen_image.py studio-hero      # 이름으로 골라서 생성
  python gen_image.py studio-hero --force   # 다시 만들기 (덮어쓰기)

manifest 항목에 "ref" (참고 이미지 경로, 예: 로고 PNG)가 있으면 /images/edits 로 보내
로고 모양을 그대로 살린 목업을 만듭니다.
일시적 오류(429·5xx·접속 끊김)는 2·4·8초 간격으로 최대 3번 다시 시도하고, 3장씩 동시에 만듭니다.
표준 라이브러리만 사용합니다.

종료 코드: 0 성공 · 1 일부 실패 · 2 키/네트워크 준비 안 됨
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import threading
import time
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets" / "manifest.json"
API = os.environ.get("HYFLIP_IMAGE_API", "https://api.openai.com/v1")  # 테스트용으로만 바꿈
MODEL = os.environ.get("HYFLIP_IMAGE_MODEL", "gpt-image-2")
WORKERS = int(os.environ.get("HYFLIP_IMAGE_WORKERS", "3"))
RETRY_WAITS = (2, 4, 8)

SETUP_HELP = """
  ▶ 설정 방법 (한 번만): 세션 상단 클라우드 환경 메뉴 → Edit
    1. 네트워크 접근 → Custom → 허용 도메인에 api.openai.com 추가 (기본 패키지 목록은 유지)
    2. 환경변수 OPENAI_API_KEY 등록  (키는 채팅에 붙여넣지 마세요)
    → 저장 후 '새 세션'을 열어야 적용됩니다.
"""

_print_lock = threading.Lock()


def say(msg):
    with _print_lock:
        print(msg, flush=True)


class ApiError(Exception):
    def __init__(self, msg, retry=False):
        super().__init__(msg)
        self.retry = retry


def _send(req, timeout=300):
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            return json.load(res)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")[:500]
        raise ApiError(f"API 오류 {e.code}: {body}", retry=e.code == 429 or e.code >= 500)
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        raise ApiError(f"접속 실패: {getattr(e, 'reason', e)}", retry=True)


def _post_json(path, payload, key):
    req = urllib.request.Request(
        f"{API}{path}", data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    return _send(req)


def _post_multipart(path, fields, files, key):
    boundary = uuid.uuid4().hex
    body = bytearray()
    for name, value in fields.items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode()
    for name, fpath in files:
        ctype = mimetypes.guess_type(fpath.name)[0] or "application/octet-stream"
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; filename=\"{fpath.name}\"\r\n"
                 f"Content-Type: {ctype}\r\n\r\n").encode()
        body += fpath.read_bytes() + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        f"{API}{path}", data=bytes(body),
        headers={"Authorization": f"Bearer {key}", "Content-Type": f"multipart/form-data; boundary={boundary}"})
    return _send(req)


def check():
    """키·네트워크 준비 상태를 진단. 준비되면 True."""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("✗ OPENAI_API_KEY 환경변수가 없습니다." + SETUP_HELP)
        return False
    req = urllib.request.Request(f"{API}/models", headers={"Authorization": f"Bearer {key}"})
    try:
        _send(req, timeout=20)
    except ApiError as e:
        msg = str(e)
        if msg.startswith("API 오류 401"):
            print("✗ API 키가 올바르지 않습니다 (401). 환경변수 OPENAI_API_KEY 값을 확인하세요.")
        elif msg.startswith("API 오류"):
            print(f"✗ OpenAI 응답 오류 — {msg}")
        else:
            print(f"✗ api.openai.com 에 접속할 수 없습니다 ({msg})." + SETUP_HELP)
        return False
    print(f"✓ 준비 완료 — 키 확인, api.openai.com 접속 가능 (모델: {MODEL})")
    return True


def generate(item, key, force=False):
    """한 장 생성. 결과 문자열('made'|'skip') 반환, 실패 시 ApiError."""
    out = ROOT / "assets" / item["file"]
    if out.exists() and not force:
        return "skip"
    params = {"model": MODEL, "prompt": item["prompt"], "size": item.get("size", "1536x1024"),
              "quality": item.get("quality", "high"), "n": 1}
    ref = ROOT / item["ref"] if item.get("ref") else None
    if ref and not ref.exists():
        raise ApiError(f"참고 이미지가 없습니다: {item['ref']} (node scripts/shoot.mjs --logos 로 만드세요)")
    for attempt in range(len(RETRY_WAITS) + 1):
        try:
            if ref:
                data = _post_multipart("/images/edits", {k: str(v) for k, v in params.items()}, [("image[]", ref)], key)
            else:
                data = _post_json("/images/generations", params, key)
            break
        except ApiError as e:
            if not e.retry or attempt == len(RETRY_WAITS):
                raise
            wait = RETRY_WAITS[attempt]
            say(f"   … {item['name']}: {e} → {wait}초 후 다시 시도 ({attempt + 1}/{len(RETRY_WAITS)})")
            time.sleep(wait)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".part")
    tmp.write_bytes(base64.b64decode(data["data"][0]["b64_json"]))
    tmp.replace(out)
    return "made"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", help="manifest 의 name (확장자 없이)")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    items = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if args.list:
        for it in items:
            mark = "✓" if (ROOT / "assets" / it["file"]).exists() else " "
            print(f"[{mark}] {it['name']:<18} {it.get('size', '1536x1024'):<10} {it['use']}")
        return 0
    if args.check:
        return 0 if check() else 2

    names = set(args.names)
    unknown = names - {it["name"] for it in items}
    if unknown:
        print(f"manifest 에 없는 이름: {', '.join(sorted(unknown))}  (목록: --list)")
        return 1
    chosen = items if args.all else [it for it in items if it["name"] in names]
    if not chosen:
        print("생성할 항목을 지정하세요 (--all 또는 이름). 목록: --list")
        return 1
    todo = [it for it in chosen if args.force or not (ROOT / "assets" / it["file"]).exists()]
    if not todo:
        print(f"✓ {len(chosen)}장 모두 이미 있습니다. 다시 만들려면 --force")
        return 0
    if not check():
        return 2
    key = os.environ["OPENAI_API_KEY"]

    print(f"→ {len(todo)}장 생성 시작 (이미 있는 {len(chosen) - len(todo)}장은 건너뜀, 동시 {WORKERS}장, 품질 high)")
    done, failed = 0, []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {pool.submit(generate, it, key, args.force): it for it in todo}
        for fut in as_completed(futs):
            it = futs[fut]
            done += 1
            try:
                fut.result()
                say(f"[{done}/{len(todo)}] {it['name']:<18} ✓ assets/{it['file']}")
            except ApiError as e:
                failed.append(it["name"])
                say(f"[{done}/{len(todo)}] {it['name']:<18} ✗ {e}")
    print(f"\n완료: 성공 {len(todo) - len(failed)}장 · 실패 {len(failed)}장")
    if failed:
        print(f"실패한 것만 다시: python3 scripts/gen_image.py {' '.join(failed)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
