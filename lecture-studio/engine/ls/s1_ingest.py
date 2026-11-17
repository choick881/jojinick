"""① 접수·점검 — 영상 정보, 음량, 화면에 박힌 녹화 도구(위젯) 위치를 확인한다."""

from __future__ import annotations

import json
import re

from .job import Job
from .util import StageError, ffprobe, read_json, run

# 녹화 도구 'Rec' 위젯: 빨간 원 + 어두운 둥근 판. 빨간 점을 찾아 위젯 전체 크기를 짐작한다.
RED = lambda r, g, b: r > 190 and g < 100 and b < 100  # noqa: E731


def _frame(job: Job, t: float, name: str):
    from PIL import Image
    p = job.work / name
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", job.video, "-frames:v", "1", p])
    return Image.open(p).convert("RGB")


def _hex(rgb) -> str:
    return "0x%02x%02x%02x" % tuple(int(v) for v in rgb)


def _median(px):
    return tuple(sorted(c[i] for c in px)[len(px) // 2] for i in range(3))


def detect_widget(im) -> dict | None:
    w, h = im.size
    x0, y0 = int(w * 0.72), int(h * 0.62)          # 오른쪽 아래 사분면만 본다
    reg = im.crop((x0, y0, w, h))
    rw, rh = reg.size
    px = reg.load()
    xs, ys = [], []
    for y in range(rh):
        for x in range(rw):
            if RED(*px[x, y]):
                xs.append(x)
                ys.append(y)
    if len(xs) < 300:
        return None
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
    cx, cy = x0 + (bx0 + bx1) / 2, y0 + (by0 + by1) / 2
    half = max(bx1 - bx0, by1 - by0) * 1.12         # 빨간 원 지름의 약 2.2배 = 위젯 전체
    x, y = max(0, int(cx - half)), max(0, int(cy - half))
    bw, bh = min(w - x, int(half * 2)), min(h - y, int(half * 2))
    # 배경색은 가림 상자 '바깥' 둘레(왼쪽·위쪽 6픽셀 밖)에서 잰다 — 안쪽 모서리는 화면 가장자리 여백과 색이 다를 수 있다
    ring = [im.getpixel((max(0, x - 6), min(h - 1, y + k * bh // 8))) for k in range(1, 8)]
    ring += [im.getpixel((min(w - 1, x + k * bw // 8), max(0, y - 6))) for k in range(1, 8)]
    return {"x": x, "y": y, "w": bw, "h": bh, "color": _hex(_median(ring))}


def measure_loudness(job: Job) -> dict:
    p = run(["ffmpeg", "-hide_banner", "-nostats", "-i", job.video, "-vn", "-af",
             "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", p.stderr, re.S)
    if not m:
        raise StageError("음량을 재지 못했습니다 (소리가 없는 영상일 수 있습니다)")
    return json.loads(m.group(0))


def run_stage(job: Job, log=print) -> dict:
    info = ffprobe(job.video)
    v = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)
    if not v:
        raise StageError("영상 화면이 없는 파일입니다")
    if not a:
        raise StageError("소리가 없는 영상입니다 — 자막을 만들 수 없습니다")
    dur = float(info["format"]["duration"])
    num, den = (v.get("avg_frame_rate") or "30/1").split("/")
    fps = float(num) / float(den or 1)
    loud = measure_loudness(job)
    out = {"width": v["width"], "height": v["height"], "fps": round(fps, 2), "duration": round(dur, 3),
           "audio": {"codec": a["codec_name"], "channels": a["channels"], "rate": int(a["sample_rate"])},
           "loudness_in": loud, "warnings": []}
    log(f"      {v['width']}×{v['height']} · {fps:.1f}fps · {dur:.1f}초 · 소리 {float(loud['input_i']):.1f} LUFS")

    mask = job.get("mask", "auto")
    box = None
    if mask == "auto":
        box = detect_widget(_frame(job, min(1.0, dur / 2), "frame_probe.png"))
        if box:
            log(f"      녹화 도구 위젯 발견 → 가림 영역 x{box['x']} y{box['y']} {box['w']}×{box['h']}")
        else:
            log("      녹화 도구 위젯 없음 → 가림 없이 진행")
    elif isinstance(mask, list) and mask:
        im = _frame(job, min(1.0, dur / 2), "frame_probe.png")
        m = mask[0]
        px = [im.getpixel((min(im.size[0] - 1, m["x"] + 3), min(im.size[1] - 1, m["y"] + 3)))]
        box = {**m, "color": _hex(px[0])}
    out["widget"] = box
    out["pad_color"] = _hex(_frame(job, 0.5, "frame_probe0.png").getpixel((4, 4)))
    if abs(fps - 30) > 1:
        out["warnings"].append(f"프레임 {fps:.0f}fps → 30fps 로 맞춥니다")
    if float(loud["input_i"]) < -23:
        out["warnings"].append(f"소리가 작습니다({float(loud['input_i']):.0f} LUFS) → -16 LUFS 로 올립니다")
    out["_summary"] = f"{v['width']}×{v['height']}, {dur:.0f}초, 위젯 {'있음' if box else '없음'}"
    return out
