"""공용 도구: 경로, 외부 명령, ffprobe, 입력 해시, JSON 입출력."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # lecture-studio/
ASSETS = ROOT / "assets"
FONTS = ASSETS / "fonts"
TEMPLATES = ROOT / "templates"
JOBS = ROOT / "jobs"
MODELS = ROOT / "models"                             # 받아쓰기 모델 (gitignore)

W, H, FPS = 1920, 1080, 30
TARGET_LUFS, TARGET_TP, TARGET_LRA = -16.0, -1.5, 11.0


class StageError(Exception):
    """사용자가 조치해야 하는 문제 (메시지는 쉬운 한국어)."""


def run(cmd: list, *, cwd: Path | None = None, env: dict | None = None) -> subprocess.CompletedProcess:
    p = subprocess.run([str(c) for c in cmd], cwd=cwd, env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if p.returncode != 0:
        tail = "\n".join((p.stderr or p.stdout).strip().splitlines()[-12:])
        raise RuntimeError(f"명령 실패({p.returncode}): {' '.join(str(c) for c in cmd[:4])} …\n{tail}")
    return p


def ffprobe(path: Path) -> dict:
    return json.loads(run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path]).stdout)


def duration(path: Path) -> float:
    return float(ffprobe(path)["format"].get("duration") or 0)


def sha(*parts) -> str:
    h = hashlib.sha1()
    for p in parts:
        h.update(json.dumps(p, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8"))
    return h.hexdigest()[:16]


def file_sig(path: Path) -> list:
    st = path.stat()
    return [path.name, st.st_size, int(st.st_mtime)]


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def read_json(path: Path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def need_tools() -> None:
    missing = [t for t in ("ffmpeg", "ffprobe") if not shutil.which(t)]
    if missing:
        raise SystemExit(f"필수 프로그램이 없습니다: {', '.join(missing)}")


def ff_path(p: Path | str) -> str:
    """ffmpeg 필터 인자 안에 넣을 경로 이스케이프 (Windows 드라이브 콜론 포함)."""
    return str(p).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")


def mmss(sec: float) -> str:
    sec = max(0, int(round(sec)))
    return f"{sec // 60}:{sec % 60:02d}"


def hhmmss(sec: float) -> str:
    sec = max(0, int(round(sec)))
    return f"{sec // 3600:02d}:{(sec % 3600) // 60:02d}:{sec % 60:02d}"


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
