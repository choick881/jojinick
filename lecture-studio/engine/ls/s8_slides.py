"""⑧ 슬라이드 전환 감지 — 화면 변화로 슬라이드 경계를 찾는다 (챕터 후보·컷 포인트).

방법 (영상은 이 컴퓨터 안에서만 분석)
  1) 정리된 영상(clean.mp4)을 초당 2장, 192×108 흑백으로 줄여 읽는다.
  2) '늘 움직이는 영역'(교수 카메라 창, 녹화 시계, 마우스가 자주 지나는 곳)을 스스로 찾아 뺀다.
     → 영상 내내 자주 바뀌는 화소 = 살아 있는 영역. 슬라이드 영역은 전환 때만 바뀐다.
  3) 나머지(정지 영역)가 기준 화면과 크게 달라지고, 바뀐 화면이 1초 이상 그대로면 '전환'.
     바뀐 면적이 크면 새 슬라이드, 작으면 같은 슬라이드 안의 변화(글머리 나타나기 등).
  4) 변화가 몇 초 동안 계속되면 '연속 변화 구간'(시연·동영상 재생·스크롤)으로 따로 표시한다.
결과: work/slides.json, 슬라이드별 썸네일 work/slides/slide_###.jpg (검수 화면용)
"""

from __future__ import annotations

import subprocess

import numpy as np

from .job import Job
from .util import StageError, read_json, run

FPS, SW, SH = 2, 192, 108
PIX_THR = 18                         # 화소 밝기 차이 (0~255) 이상이면 '바뀜'
SENS = {"low": 0.03, "normal": 0.01, "high": 0.005}   # 정지 영역 중 바뀐 비율 → 전환 후보
NEW_SLIDE = 0.15                     # 이 이상 바뀌면 '새 슬라이드', 미만이면 '슬라이드 안 변화'
LIVE_RATE = 0.12                     # 프레임 쌍 중 이 비율 이상 바뀐 화소 = 늘 움직이는 영역


def read_frames(path) -> np.ndarray:
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={FPS},scale={SW}:{SH},format=gray",
           "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        raise StageError("화면을 읽지 못했습니다: " + p.stderr.decode("utf-8", "replace")[-300:])
    n = len(p.stdout) // (SW * SH)
    return np.frombuffer(p.stdout[: n * SW * SH], dtype=np.uint8).reshape(n, SH, SW).astype(np.int16)


def _dilate(m: np.ndarray, r: int = 2) -> np.ndarray:
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def live_mask(frames: np.ndarray) -> np.ndarray:
    if len(frames) < 3:
        return np.zeros(frames.shape[1:], bool)
    ch = np.abs(np.diff(frames, axis=0)) > PIX_THR
    return _dilate(ch.mean(axis=0) > LIVE_RATE)


def detect(frames: np.ndarray, sens: float, live: np.ndarray) -> tuple[list[dict], list[dict]]:
    """반환: (전환 이벤트 목록, 연속 변화 구간 목록). 시각은 초."""
    static = ~live
    area = max(1, int(static.sum()))

    def frac(a, b):
        return float(((np.abs(a - b) > PIX_THR) & static).sum()) / area

    events, motion = [], []
    ref = frames[0]
    i, n = 1, len(frames)
    busy_start, busy_last = None, None
    while i < n:
        f = frames[i]
        c = frac(f, ref)
        step = frac(f, frames[i - 1])
        # 연속 변화 추적 (이웃 프레임끼리 계속 바뀜)
        if step >= sens / 2:
            busy_start = i if busy_start is None else busy_start
            busy_last = i
        elif busy_start is not None and i - busy_last > 2:
            if (busy_last - busy_start + 1) / FPS >= 4.0:
                motion.append({"start": round(busy_start / FPS, 1), "end": round(busy_last / FPS, 1)})
            busy_start = None
        if c >= sens:
            # 새 화면이 1초(2장) 동안 안정적인가?
            nxt = frames[i + 1: i + 1 + FPS]
            if len(nxt) == FPS and all(frac(g, f) < sens / 2 for g in nxt):
                events.append({"t": round(i / FPS, 1), "change": round(c, 3),
                               "kind": "slide" if c >= NEW_SLIDE else "build"})
                ref = f
            elif len(nxt) < FPS:
                ref = f
        i += 1
    if busy_start is not None and (busy_last - busy_start + 1) / FPS >= 4.0:
        motion.append({"start": round(busy_start / FPS, 1), "end": round(busy_last / FPS, 1)})
    # 연속 변화 구간 안의 자잘한 '전환'은 지운다 (시연 중 화면 움직임)
    events = [e for e in events if not any(m["start"] - 0.5 <= e["t"] <= m["end"] + 1.0 for m in motion)
              or e["kind"] == "slide" and e["change"] >= 0.5]
    return events, motion


def _thumb(job: Job, t: float, dst) -> None:
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", job.work / "clean.mp4", "-frames:v", "1",
         "-vf", "scale=320:-2", "-q:v", "4", dst])


def run_stage(job: Job, log=print) -> dict:
    src = job.work / "clean.mp4"
    if not src.exists():
        raise StageError("먼저 '영상 정리' 단계가 필요합니다")
    dur = (read_json(job.work / "ingest.json") or {}).get("duration") or 0
    level = (job.get("slides") or {}).get("sensitivity", "normal")
    sens = SENS.get(level, SENS["normal"])
    frames = read_frames(src)
    live = live_mask(frames)
    events, motion = detect(frames, sens, live)
    dur = dur or len(frames) / FPS

    # 슬라이드 구간 = 새 슬라이드 전환 사이 (같은 슬라이드 안 변화는 구간 안 'builds' 로)
    cuts = [0.0] + [e["t"] for e in events if e["kind"] == "slide"] + [round(dur, 1)]
    tdir = job.work / "slides"
    tdir.mkdir(exist_ok=True)
    for old in tdir.glob("slide_*.jpg"):
        old.unlink()
    segs = []
    for k, (a, b) in enumerate(zip(cuts, cuts[1:]), 1):
        if b - a < 0.5:
            continue
        thumb = tdir / f"slide_{k:03d}.jpg"
        _thumb(job, min(a + 1.0, (a + b) / 2), thumb)
        segs.append({"i": len(segs) + 1, "start": a, "end": b, "thumb": f"slides/{thumb.name}",
                     "builds": [e["t"] for e in events if e["kind"] == "build" and a < e["t"] < b],
                     "motion": any(m["start"] < b and m["end"] > a for m in motion)})
    live_pct = round(100 * float(live.mean()), 1)
    log(f"      늘 움직이는 영역(카메라·시계 등) {live_pct}% 제외 · 민감도 {level}")
    for e in events:
        log(f"      {e['t']:7.1f}s  {'새 슬라이드' if e['kind'] == 'slide' else '슬라이드 안 변화'}  (바뀐 면적 {e['change']:.0%})")
    for m in motion:
        log(f"      {m['start']:7.1f}–{m['end']:.1f}s  연속 변화 (시연·영상·스크롤 추정)")
    n_slide = sum(e["kind"] == "slide" for e in events)
    return {"fps": FPS, "sensitivity": level, "live_area_pct": live_pct, "events": events, "motion": motion,
            "segments": segs,
            "_summary": f"슬라이드 {len(segs)}장 · 전환 {n_slide}회 · 안쪽 변화 {len(events) - n_slide}회 · 연속 변화 {len(motion)}구간"}
