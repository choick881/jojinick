#!/usr/bin/env python3
"""받아쓰기 모델 내려받기 (처음 한 번) — models/whisper-<크기>/ 와 models/silero_vad.onnx

  python engine/setup_models.py            # medium (정확도 우선, 기본값)
  python engine/setup_models.py small      # small  (속도 우선 — 저사양 PC)

sherpa-onnx 공식 GitHub 릴리스의 압축 파일을 받으면서 필요한 int8 파일만 꺼낸다 (압축 파일은 저장하지 않음).
모델은 이 컴퓨터에만 저장되고, 받아쓰기도 이 컴퓨터 안에서만 한다.
"""

import shutil
import sys
import tarfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "models"
REL = "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models"


def _get(url: str, dst: Path) -> None:
    with urllib.request.urlopen(url, timeout=60) as r, open(dst, "wb") as f:
        shutil.copyfileobj(r, f)


def main(size: str = "medium") -> None:
    MODELS.mkdir(exist_ok=True)
    vad = MODELS / "silero_vad.onnx"
    if not vad.exists():
        print("말소리 구간 모델(silero_vad) 받는 중 …")
        _get(f"{REL}/silero_vad.onnx", vad)
    out = MODELS / f"whisper-{size}"
    want = {f"{size}-encoder.int8.onnx", f"{size}-decoder.int8.onnx", f"{size}-tokens.txt"}
    if out.exists() and all((out / w).exists() for w in want):
        print(f"이미 있습니다: {out}")
        return
    out.mkdir(exist_ok=True)
    print(f"받아쓰기 모델(whisper-{size}) 받는 중 … (medium 은 약 1.9GB 를 읽어 940MB 만 저장, 몇 분 걸립니다)")
    with urllib.request.urlopen(f"{REL}/sherpa-onnx-whisper-{size}.tar.bz2", timeout=60) as r:
        with tarfile.open(fileobj=r, mode="r|bz2") as tar:
            for m in tar:
                name = Path(m.name).name
                if m.isfile() and name in want:
                    src = tar.extractfile(m)
                    with open(out / name, "wb") as f:
                        shutil.copyfileobj(src, f)
                    print(f"  {name}  {m.size / 1e6:.0f}MB")
    missing = [w for w in want if not (out / w).exists()]
    if missing:
        raise SystemExit(f"모델 파일을 찾지 못했습니다: {missing}")
    print(f"완료 → {out}   (job.yaml 의 asr.model 을 '{size}' 로 맞추세요)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "medium")
