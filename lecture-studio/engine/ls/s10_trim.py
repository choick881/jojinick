"""⑩ 군더더기 컷 '제안' — 자동으로 자르지 않는다. 목록만 만들고, 교수님이 승인한 것만 ⑪ 단계가 적용한다.

찾는 것
  긴 무음      말 사이 쉼이 trim.min_pause 초 이상 (소리 측정 + 받아쓰기 구간으로 이중 확인).
               자르더라도 trim.keep_pause 초는 남긴다 (숨 쉬는 틈·생각할 틈).
  앞뒤 여백    녹화 시작 직후·끝나기 직전의 말 없는 구간.
  NG·혼잣말   "다시 할게요", "잠깐만", "왜 안 넘어가" 같은 녹화 중 말 → 구간 전체 컷 제안.
  다시 말하기  거의 같은 문장을 바로 이어 다시 말한 경우 → 앞의 시도를 컷 제안.
  군말        "음·어·그" 만으로 된 짧은 구간 → 컷 제안. 문장 속 군말이 많으면 '참고'로만 알린다(자를 수 없음).
보존 권장 (학습 맥락을 해칠 수 있는 침묵 — 제안은 하되 기본값은 '자르지 않음')
  질문 뒤 침묵(학생이 생각할 시간) · 슬라이드 넘김 직후 · 화면 시연 중 침묵
"""

from __future__ import annotations

import difflib
import re

from .job import Job
from .util import StageError, mmss, read_json, run

FILLERS = {"음", "어", "그", "저", "아", "에", "뭐", "이제", "막", "좀", "음음", "어어", "으음", "어음"}
NG_WORDS = ["다시 할게", "다시 하겠", "다시 할까", "다시 갈게", "잠깐만", "잠시만요", "엔지", "NG", "아이씨", "미치겠",
            "안 넘어가", "왜 안 넘", "안 넘겨", "넘겨 줘", "넘겨줘", "녹화 다시", "처음부터 다시", "틀렸", "아 잠깐"]
QUESTION = re.compile(r"(\?|까요|을까|ㄹ까|일까|할까|습니까|나요|은가|는가)\s*\.?$")


def _silences(job: Job, min_len: float) -> list[tuple[float, float]]:
    p = run(["ffmpeg", "-hide_banner", "-nostats", "-i", job.work / "clean.mp4", "-vn", "-af",
             f"silencedetect=noise=-38dB:d={min_len}", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", p.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", p.stderr)]
    return list(zip(starts, ends + [None] * (len(starts) - len(ends))))


def _tokens(text: str) -> list[str]:
    return re.findall(r"[가-힣A-Za-z0-9]+", text)


def text_cuts(segs: list[dict], notes: list | None = None) -> list[dict]:
    """받아쓴 글만으로 찾는 컷 후보 (NG·혼잣말, 다시 말하기, 군말). notes 에는 '참고'를 덧붙인다."""
    out, notes = [], notes if notes is not None else []
    for k, seg in enumerate(segs):
        t = seg["text"].strip()
        ng = [w for w in NG_WORDS if w.lower() in t.lower()]
        if ng:
            out.append(dict(kind="NG·혼잣말 의심", a=max(0.0, seg["start"] - 0.2), b=seg["end"] + 0.3,
                            reason=f"녹화 중 말로 보임 ({', '.join(ng[:3])})", text=t))
            continue
        if k + 1 < len(segs):
            nxt = segs[k + 1]["text"].strip()
            head = nxt[: len(t) + 4]
            r = difflib.SequenceMatcher(None, t, head).ratio() if len(t) >= 8 else 0
            if r >= 0.75 and segs[k + 1]["start"] - seg["end"] < 6:
                out.append(dict(kind="다시 말하기", a=max(0.0, seg["start"] - 0.1), b=segs[k + 1]["start"] - 0.1,
                                reason=f"바로 뒤에 같은 말을 다시 함 (비슷함 {r:.0%}) → 앞의 시도를 컷", text=t))
                continue
        toks = _tokens(t)
        if toks and all(x in FILLERS for x in toks):
            out.append(dict(kind="군말", a=max(0.0, seg["start"] - 0.1), b=seg["end"] + 0.1,
                            reason="'음·어' 같은 군말만 있는 구간", text=t))
        elif len(toks) >= 6:
            nf = sum(x in FILLERS for x in toks)
            if nf / len(toks) >= 0.2:
                notes.append({"start": seg["start"], "end": seg["end"], "text": t,
                              "note": f"군말 {nf}개 / 낱말 {len(toks)}개 — 문장 속이라 자르지 않고 알려만 드립니다"})
    return out


def run_stage(job: Job, log=print) -> dict:
    asr = read_json(job.work / "asr.json")
    if not asr:
        raise StageError("먼저 '받아쓰기' 단계가 필요합니다")
    cfg = job.get("trim") or {}
    min_pause, keep = float(cfg.get("min_pause", 2.5)), float(cfg.get("keep_pause", 0.8))
    dur = float((read_json(job.work / "ingest.json") or {}).get("duration") or 0)
    segs = asr["segments"]
    slides = read_json(job.work / "slides.json") or {}
    slide_cuts = [e["t"] for e in slides.get("events", []) if e["kind"] == "slide"]
    motion = slides.get("motion") or []
    cuts, notes = [], []

    def add(kind, a, b, reason, text="", recommend="컷 제안", why_keep=""):
        if b - a < 0.4:
            return
        cuts.append({"id": f"c{len(cuts) + 1:03d}", "kind": kind, "start": round(a, 2), "end": round(b, 2),
                     "saving": round(b - a, 1), "reason": reason, "text": text, "recommend": recommend, "keep_reason": why_keep})

    # 1) 긴 무음 (소리 측정으로 찾고, 받아쓰기 구간과 겹치지 않는지 확인)
    for s, e in _silences(job, min_pause):
        e = dur if e is None else e
        if any(seg["start"] < e - 0.3 and seg["end"] > s + 0.3 for seg in segs):
            continue                      # 받아쓰기상 말이 있는 곳 (작은 목소리) → 건드리지 않음
        if segs and e <= segs[0]["start"] + 0.2:
            add("앞 여백", 0.0, max(0.0, e - 0.5), f"녹화 시작 후 {e:.1f}초 동안 말이 없음")
            continue
        if segs and s >= segs[-1]["end"] - 0.2:
            add("뒤 여백", min(dur, s + 1.0), dur, f"마지막 말 뒤 {dur - s:.1f}초 동안 말이 없음")
            continue
        a, b = s + keep / 2, e - keep / 2
        prev = max((seg for seg in segs if seg["end"] <= s + 0.3), key=lambda x: x["end"], default=None)
        why = ""
        if prev and QUESTION.search(prev["text"].strip()):
            why = "질문 뒤 침묵 — 학생이 생각할 시간일 수 있음"
        elif any(s - 1.0 <= t <= e + 0.5 for t in slide_cuts):
            why = "슬라이드 넘김과 겹침 — 화면을 읽을 시간일 수 있음"
        elif any(m["start"] < e and m["end"] > s for m in motion):
            why = "화면 시연 중 — 화면을 보여 주는 침묵일 수 있음"
        add("긴 무음", a, b, f"{e - s:.1f}초 쉼 → {keep:g}초만 남기고 줄이기",
            text=(prev or {}).get("text", "")[-30:], recommend="보존 권장" if why else "컷 제안", why_keep=why)

    # 2) NG·혼잣말 / 3) 다시 말하기 / 4) 군말
    for c in text_cuts(segs, notes):
        add(**c)

    cuts.sort(key=lambda c: c["start"])
    for n, c in enumerate(cuts, 1):
        c["id"] = f"c{n:03d}"
    for c in cuts:
        log(f"      {c['id']} {mmss(c['start']):>5}–{mmss(c['end']):<5} {c['kind']:<8} {c['recommend']:<5} "
            f"{c['saving']:>5.1f}초  {c['reason']}" + (f"  [{c['keep_reason']}]" if c["keep_reason"] else ""))
    sug = [c for c in cuts if c["recommend"] == "컷 제안"]
    return {"cuts": cuts, "notes": notes, "min_pause": min_pause, "keep_pause": keep, "review_status": "승인 대기",
            "_summary": f"컷 제안 {len(sug)}건({sum(c['saving'] for c in sug):.0f}초) · 보존 권장 {len(cuts) - len(sug)}건 · "
                        f"참고 {len(notes)}건 — 자동 적용 없음"}
