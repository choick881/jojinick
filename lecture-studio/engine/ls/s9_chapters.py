"""⑨ 챕터 — 슬라이드 경계 + 대본 의미로 챕터를 만들고 도입/개념/사례/시연/정리로 구분한다.

1) 경계 후보: 새 슬라이드(가장 강함) · AI 챕터(요약·퀴즈 단계) · 말이 1.5초 이상 끊긴 곳
2) AI 챕터가 있으면 그 시작점을 가까운 슬라이드 경계(±8초) 또는 문장 시작(±5초)에 맞춘다 (화면과 말이 함께 바뀌는 곳)
   AI 챕터가 없으면 슬라이드 구간을 그대로 쓰고, 제목은 그 구간 첫 문장으로 '제목 후보'를 단다.
3) 너무 짧은 챕터(chapters.min_sec)는 앞 챕터에 합치고, 최대 개수(chapters.max_count)를 넘으면 가장 짧은 것부터 합친다.
4) 유형: 대본 낱말(예를 들어→사례, 화면·실행→시연, 정리·요약→정리)과 화면 연속 변화(시연)로 정한다.
결과는 늘 '검토 대기' — 검수 화면에서 시작 시각·제목·유형을 고칠 수 있다.
"""

from __future__ import annotations

from .job import Job
from .util import StageError, mmss, read_json

TYPE_WORDS = {
    "도입": ["안녕하", "소개", "오늘은", "이번 시간", "이번 차시", "함께 살펴", "학습 목표"],
    "사례": ["예를 들어", "예를 들면", "예컨대", "사례", "실제로", "경험", "이야기", "가령"],
    "시연": ["화면을", "보시면", "클릭", "실행", "입력", "시연", "실습", "따라 해", "코드", "열어"],
    "정리": ["정리하면", "정리해", "요약", "마지막으로", "다음 시간", "다음 차시", "기억해", "핵심은", "결론"],
}


def _classify(text: str, idx: int, n: int, motion_ratio: float) -> tuple[str, str]:
    score = {k: sum(text.count(w) for w in ws) for k, ws in TYPE_WORDS.items()}
    if motion_ratio >= 0.3:
        score["시연"] += 3
    if idx == 0:
        score["도입"] += 1
    else:
        score["도입"] = 0              # 도입은 첫 챕터만
    if idx == n - 1:
        score["정리"] += 1
    best = max(score, key=lambda k: score[k])
    if score[best] < 2 and not (idx == 0 and score["도입"] >= 2):
        return "개념", "뚜렷한 단서 없음 → 개념 설명"
    hits = [w for w in TYPE_WORDS[best] if w in text][:3]
    why = ", ".join(f"'{w}'" for w in hits)
    if best == "시연" and motion_ratio >= 0.3:
        why = (why + " · " if why else "") + f"화면 연속 변화 {motion_ratio:.0%}"
    return best, why or "위치(첫·끝 챕터)"


def _title_from(text: str) -> str:
    t = text.replace("\n", " ").strip()
    for sep in (".", "?", "!", "다 "):
        k = t.find(sep)
        if 6 <= k <= 40:
            return t[: k + (1 if sep != "다 " else 1)].strip()
    return (t[:24] + "…") if len(t) > 24 else t


def run_stage(job: Job, log=print) -> dict:
    text = read_json(job.work / "text.json")
    if not text:
        raise StageError("먼저 '자막' 단계가 필요합니다")
    cues = text["cues"]
    slides = read_json(job.work / "slides.json") or {}
    study = read_json(job.work / "study.json") or {}
    asr = read_json(job.work / "asr.json") or {}
    cfg = job.get("chapters") or {}
    min_sec, max_count = float(cfg.get("min_sec", 45)), int(cfg.get("max_count", 8))
    dur = float((read_json(job.work / "ingest.json") or {}).get("duration") or (cues[-1]["end"] if cues else 0))

    slide_cuts = [e["t"] for e in slides.get("events", []) if e["kind"] == "slide"]
    segs = asr.get("segments") or []
    sent_starts = [s["start"] for s in segs]
    pauses = [b["start"] for a, b in zip(segs, segs[1:]) if b["start"] - a["end"] >= 1.5]

    def snap(t: float) -> tuple[float, str]:
        near = [s for s in slide_cuts if abs(s - t) <= 8]
        if near:
            return min(near, key=lambda s: abs(s - t)), "슬라이드 경계"
        near = [s for s in sent_starts if abs(s - t) <= 5]
        if near:
            return min(near, key=lambda s: abs(s - t)), "문장 시작"
        return t, "AI 제안 그대로"

    items = []
    ai = study.get("chapters") or []
    if ai:
        for c in ai:
            t, how = snap(float(c["start"]))
            items.append({"start": round(t, 1), "title_ko": c.get("title_ko", ""), "title_en": c.get("title_en", ""),
                          "source": f"AI 챕터 → {how}", "ai_start": c["start"]})
        # AI 가 놓친 '새 슬라이드' 중 앞뒤 챕터와 충분히 떨어진 것은 후보로 더한다
        for s in slide_cuts:
            if all(abs(s - it["start"]) >= min_sec for it in items):
                items.append({"start": s, "title_ko": "", "title_en": "", "source": "슬라이드 경계 (AI 챕터 없음)"})
    else:
        bounds = [0.0] + (slide_cuts or pauses)
        for t in bounds:
            items.append({"start": round(t, 1), "title_ko": "", "title_en": "",
                          "source": "슬라이드 경계" if t in slide_cuts else ("말 끊김" if t else "시작")})
    items.sort(key=lambda c: c["start"])
    if items:
        items[0]["start"] = 0.0 if items[0]["start"] < min_sec else items[0]["start"]
    if not items or items[0]["start"] > 0:
        items.insert(0, {"start": 0.0, "title_ko": "", "title_en": "", "source": "시작"})

    # 짧은 챕터 합치기 → 개수 제한
    def merge_short(lst):
        out = []
        for c in lst:
            if out and c["start"] - out[-1]["start"] < min_sec:
                if not out[-1]["title_ko"] and c["title_ko"]:
                    out[-1].update({k: c[k] for k in ("title_ko", "title_en")})
                out[-1]["source"] += " + 짧아서 합침"
                continue
            out.append(dict(c))
        return out
    items = merge_short(items)
    while len(items) > max_count:
        lens = [(items[k + 1]["start"] if k + 1 < len(items) else dur) - items[k]["start"] for k in range(len(items))]
        k = min(range(1, len(items)), key=lambda j: lens[j])
        items.pop(k)

    motion = slides.get("motion") or []
    n = len(items)
    for k, c in enumerate(items):
        end = items[k + 1]["start"] if k + 1 < n else dur
        c["end"] = round(end, 1)
        body = " ".join(x["ko"].replace("\n", " ") for x in cues if c["start"] - 0.5 <= x["start"] < end)
        mov = sum(max(0.0, min(end, m["end"]) - max(c["start"], m["start"])) for m in motion)
        c["type"], c["type_reason"] = _classify(body, k, n, mov / max(1.0, end - c["start"]))
        if not c["title_ko"]:
            c["title_ko"] = _title_from(body) if body else f"챕터 {k + 1}"
            c["title_candidate"] = True
        c["slides"] = [s["i"] for s in slides.get("segments", []) if s["start"] < end and s["end"] > c["start"]]
        log(f"      {mmss(c['start']):>5}  [{c['type']}] {c['title_ko']}  ← {c['source']}")
    return {"chapters": items, "review_status": "검토 대기",
            "_summary": f"챕터 {n}개 (" + ", ".join(f"{t} {sum(c['type'] == t for c in items)}" for t in TYPE_WORDS | {"개념": 0}
                                          if any(c["type"] == t for c in items)) + ")"}
