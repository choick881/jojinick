"""⑪ 승인 컷 적용 — 검수 화면에서 교수님이 '승인'한 컷만 잘라 work/edited.mp4 를 만든다.

승인한 컷이 없으면 아무것도 자르지 않는다 (clean.mp4 그대로).
자막·챕터·퀴즈 근거 시각은 ⑥ 산출물 단계에서 잘린 만큼 앞당겨진다 (review.final_*).
이음매는 0.03초 소리 페이드로 '툭' 끊기는 소리를 막는다 (화면 효과는 넣지 않음).
"""

from __future__ import annotations

from . import review
from .job import Job
from .util import StageError, read_json, run


def _merge(rngs: list[list[float]]) -> list[list[float]]:
    out = []
    for a, b in sorted(rngs):
        if out and a <= out[-1][1] + 0.05:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def run_stage(job: Job, log=print) -> dict:
    trim = read_json(job.work / "trim.json")
    if trim is None:
        raise StageError("먼저 '군더더기 컷 제안' 단계가 필요합니다")
    dur = float((read_json(job.work / "ingest.json") or {}).get("duration") or 0)
    ok = set(review.approved_cut_ids(job))
    chosen = [c for c in trim["cuts"] if c["id"] in ok]
    unknown = sorted(ok - {c["id"] for c in trim["cuts"]})
    if unknown:
        log(f"      ⚠ 승인 목록에 있지만 지금 제안에 없는 컷: {', '.join(unknown)} (컷 제안이 바뀌었습니다 — 다시 검수해 주세요)")
    if not chosen:
        log("      승인한 컷 없음 → 영상을 자르지 않습니다")
        return {"applied": [], "removed": [], "file": "clean.mp4", "_summary": "승인한 컷 없음 · 원본 길이 유지"}

    removed = _merge([[max(0.0, c["start"]), min(dur, c["end"])] for c in chosen])
    keep, t = [], 0.0
    for a, b in removed:
        if a - t > 0.05:
            keep.append([t, a])
        t = b
    if dur - t > 0.05:
        keep.append([t, dur])
    # trim/atrim + concat (구간마다 소리 끝을 살짝 페이드)
    fc, n = [], len(keep)
    for k, (a, b) in enumerate(keep):
        fd = min(0.03, (b - a) / 4)
        fc.append(f"[0:v]trim=start={a:.3f}:end={b:.3f},setpts=PTS-STARTPTS[v{k}]")
        fc.append(f"[0:a]atrim=start={a:.3f}:end={b:.3f},asetpts=PTS-STARTPTS,"
                  f"afade=t=in:d={fd:.3f},afade=t=out:st={max(0.0, b - a - fd):.3f}:d={fd:.3f}[a{k}]")
    fc.append("".join(f"[v{k}][a{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
    dst = job.work / "edited.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-i", job.work / "clean.mp4", "-filter_complex", ";".join(fc),
         "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-c:a", "aac",
         "-b:a", "192k", "-movflags", "+faststart", dst])
    cut_sec = sum(b - a for a, b in removed)
    for c in chosen:
        log(f"      적용 {c['id']} {c['kind']} {c['start']:.1f}–{c['end']:.1f}s")
    return {"applied": [c["id"] for c in chosen], "removed": removed, "keep": keep, "file": "edited.mp4",
            "removed_sec": round(cut_sec, 1), "duration_after": round(dur - cut_sec, 1),
            "_summary": f"승인 컷 {len(chosen)}건 적용 · {cut_sec:.1f}초 줄임 → {dur - cut_sec:.0f}초"}
