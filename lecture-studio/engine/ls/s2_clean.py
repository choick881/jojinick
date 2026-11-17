"""② 영상 정리 — 녹화 도구 가림 · 1920×1080 · 30fps · 음량 -16 LUFS (2단계 측정)."""

from __future__ import annotations

import json
import re

from .job import Job
from .util import FPS, H, TARGET_LRA, TARGET_LUFS, TARGET_TP, W, StageError, read_json, run


def _loudnorm_params(job: Job, af_pre: str) -> str:
    """1차: 측정 → 2차에 그대로 넣을 loudnorm 인자."""
    pre = af_pre + "," if af_pre else ""
    p = run(["ffmpeg", "-hide_banner", "-nostats", "-i", job.video, "-vn", "-af",
             f"{pre}loudnorm=I={TARGET_LUFS}:TP={TARGET_TP}:LRA={TARGET_LRA}:print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p.stderr, re.S)
    if not m:
        raise StageError("음량 측정 실패")
    d = json.loads(m.group(0))
    return (f"loudnorm=I={TARGET_LUFS}:TP={TARGET_TP}:LRA={TARGET_LRA}:measured_I={d['input_i']}:measured_TP={d['input_tp']}"
            f":measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}:linear=true")


def _calibrate(job: Job, box: dict, pad_color: str) -> tuple[str, str]:
    """ffmpeg 의 색 변환 때문에 지정한 색이 조금 달라진다 → 한 프레임으로 먼저 시험해 보고 그 차이만큼 미리 보정한다."""
    from PIL import Image
    want = tuple(int(box["color"][i:i + 2], 16) for i in (2, 4, 6))
    png = job.work / "calib.png"
    vf = (f"drawbox=x={box['x']}:y={box['y']}:w={box['w']}:h={box['h']}:color={box['color']}:t=fill,"
          f"scale={W}:{H}:force_original_aspect_ratio=decrease,format=yuv420p")
    run(["ffmpeg", "-y", "-v", "error", "-ss", "1", "-i", job.video, "-frames:v", "1", "-vf", vf, png])
    got = Image.open(png).convert("RGB").getpixel((box["x"] + box["w"] // 2, box["y"] + box["h"] // 2))
    fix = tuple(max(0, min(255, 2 * w - g)) for w, g in zip(want, got))
    hexs = lambda c: "0x%02x%02x%02x" % c  # noqa: E731
    pw = tuple(int(pad_color[i:i + 2], 16) for i in (2, 4, 6))
    return hexs(fix), hexs(tuple(max(0, min(255, p + f - w)) for p, f, w in zip(pw, fix, want)))


def run_stage(job: Job, log=print) -> dict:
    ing = read_json(job.work / "ingest.json")
    if not ing:
        raise StageError("먼저 '접수·점검' 단계가 필요합니다")
    vf = []
    box = ing.get("widget")
    pad_color = ing["pad_color"]
    if box:
        box = dict(box)
        box["color"], pad_color = _calibrate(job, box, pad_color)
        vf.append(f"drawbox=x={box['x']}:y={box['y']}:w={box['w']}:h={box['h']}:color={box['color']}:t=fill")
    vf.append(f"scale={W}:{H}:force_original_aspect_ratio=decrease")
    vf.append(f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color={pad_color}")
    vf.append(f"fps={FPS}")
    vf.append("format=yuv420p")
    ln = _loudnorm_params(job, "")
    log(f"      음량 측정 완료 → {TARGET_LUFS:g} LUFS 로 맞춥니다")
    dst = job.work / "clean.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", job.video, "-vf", ",".join(vf), "-af", ln + ",aresample=48000",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", dst])
    # 결과 음량 확인
    p = run(["ffmpeg", "-hide_banner", "-nostats", "-i", dst, "-vn", "-af", "loudnorm=print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p.stderr, re.S)
    got = json.loads(m.group(0)) if m else {}
    lufs, tp = float(got.get("input_i", 0)), float(got.get("input_tp", 0))
    log(f"      결과 {lufs:.1f} LUFS · 최고음 {tp:.1f} dBTP")
    return {"file": "clean.mp4", "lufs": lufs, "true_peak": tp, "masked": bool(box),
            "_summary": f"{W}×{H} {FPS}fps · {lufs:.1f} LUFS" + (" · 위젯 가림" if box else "")}
