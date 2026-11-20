"""④ 자막 만들기 — 받아쓴 글을 바로잡고(한국어), 영어로 옮기고, 자막 장면(cue)으로 나눈다."""

from __future__ import annotations

import difflib
import re

from .job import Job
from .llm import complete_json
from .util import StageError, read_json

KO_LINE, KO_LINES = 18, 2      # 한국어: 한 줄 18자 이내, 최대 2줄
EN_LINE, EN_LINES = 42, 2      # 영어: 한 줄 42자 이내, 최대 2줄


def wrap(text: str, width: int) -> str:
    """가장 가운데에 가까운 띄어쓰기에서 줄바꿈 (한 줄이 width 이하면 그대로)."""
    text = " ".join(text.split())
    if len(text) <= width or " " not in text:
        return text
    mid = len(text) / 2
    best = min((abs(i - mid), i) for i, c in enumerate(text) if c == " ")[1]
    return text[:best] + "\n" + text[best + 1:]


def _split_long(text: str, width: int, lines: int) -> list[str]:
    """한 장면에 못 담는 길이면 의미 단위(쉼표·접속)에서 둘로 나눈다."""
    if len(text) <= width * lines:
        return [text]
    mid = len(text) // 2
    cands = [i for i, c in enumerate(text) if c in ",，、 " and 6 < i < len(text) - 6]
    cut = min(cands, key=lambda i: abs(i - mid)) if cands else mid
    return _split_long(text[:cut + 1].strip(), width, lines) + _split_long(text[cut + 1:].strip(), width, lines)


def _norm(t: str) -> str:
    return re.sub(r"[^가-힣A-Za-z0-9]", "", t or "").lower()


def mismatched(segs: list[dict], res: dict, thr: float = 0.45) -> list[int]:
    """AI 결과(교정 글)가 받아쓴 글과 너무 다른 구간 번호. 받아쓰기를 다시 해 구간이 바뀌었는데
    예전 결과 파일(llm_text.json)을 그대로 쓰면 글이 한두 구간씩 밀려 엉뚱한 시각에 붙는다 — 그걸 막는다."""
    bad = []
    for s in res.get("segments", []):
        i = int(s["id"])
        ko = "".join(p.get("ko") or "" for p in s.get("parts") or [])
        if i >= len(segs) or not ko:
            continue
        a, b = _norm(segs[i]["text"]), _norm(ko)
        if a and b and difflib.SequenceMatcher(None, a, b).ratio() < thr:
            bad.append(i)
    return bad


def run_stage(job: Job, log=print) -> dict:
    asr = read_json(job.work / "asr.json")
    if not asr:
        raise StageError("먼저 '받아쓰기' 단계가 필요합니다")
    segs = asr["segments"]
    payload = {"title": job.get("title"), "lecturer": job.lecturer, "source_language": job.get("source_language", "ko"),
               "glossary": job.glossary,
               "segments": [{"id": i, "start": s["start"], "end": s["end"], "text": s["text"]} for i, s in enumerate(segs)]}
    res = complete_json(job, "text", payload, log)
    bad = mismatched(segs, res)
    used = [s for s in res.get("segments", []) if s.get("parts")]
    if used and len(bad) > max(2, 0.25 * len(used)):
        raise StageError(
            f"AI 결과의 글이 지금 받아쓰기와 맞지 않습니다 (구간 {len(bad)}/{len(used)}곳: {bad[:8]}…).\n"
            "  받아쓰기를 다시 해서 구간이 바뀐 것으로 보입니다. 이대로 쓰면 자막이 엉뚱한 시각에 붙습니다.\n"
            f"  → work/llm_request_text.json 로 결과를 다시 만들어 input/llm_text.json 에 저장하세요.")
    for i in bad:
        log(f"      ⚠ 구간 {i}: AI 교정 글이 받아쓴 글과 많이 다릅니다 — 검수 때 확인")
    by_id = {int(s["id"]): s.get("parts") or [] for s in res.get("segments", [])}
    dropped = {int(s["id"]) for s in res.get("segments", []) if not s.get("parts")}   # 빈 parts = 겹친 조각이라 버림

    cues, warnings = [], []
    for i, s in enumerate(segs):
        if i in dropped:
            continue
        parts = [p for p in by_id.get(i, []) if (p.get("ko") or "").strip()]
        if not parts:
            warnings.append(f"구간 {i}: AI 결과 없음 → 받아쓴 글 그대로 사용 (영어 없음)")
            parts = [{"ko": s["text"], "en": ""}]
        nxt = segs[i + 1]["start"] if i + 1 < len(segs) else s["end"] + 1.0
        t0, t1 = s["start"], min(s["end"] + 0.45, nxt - 0.04)
        t1 = max(t1, t0 + 0.8)
        # 장면 길이는 한국어 글자 수에 비례해 나눈다
        weights = [max(1, len(p["ko"].replace(" ", ""))) for p in parts]
        tot, acc = sum(weights), t0
        for p, w in zip(parts, weights):
            d = (t1 - t0) * w / tot
            cues.append({"seg": i, "start": round(acc, 3), "end": round(acc + d, 3),
                         "ko": p["ko"].strip(), "en": (p.get("en") or "").strip()})
            acc += d
    # 너무 긴 장면은 둘로 쪼갠다 / 줄바꿈 계산
    out = []
    for c in cues:
        kos, ens = _split_long(c["ko"], KO_LINE, KO_LINES), _split_long(c["en"], EN_LINE, EN_LINES) if c["en"] else [""]
        if len(kos) == len(ens) or not c["en"]:
            ens = ens if c["en"] else [""] * len(kos)
        else:
            kos, ens = [c["ko"]], [c["en"]]
        d = (c["end"] - c["start"]) / len(kos)
        for k, (ko, en) in enumerate(zip(kos, ens)):
            out.append({"seg": c["seg"], "start": round(c["start"] + k * d, 3), "end": round(c["start"] + (k + 1) * d, 3),
                        "ko": wrap(ko, KO_LINE), "en": wrap(en, EN_LINE) if en else ""})
    for n, c in enumerate(out, 1):
        c["i"] = n
    # 서로 겹치지 않게 (앞 장면 끝 ≤ 다음 장면 시작)
    for a, b in zip(out, out[1:]):
        if a["end"] > b["start"]:
            a["end"] = b["start"]

    # 용어사전 점검: 한국어에 용어가 있으면 영어에도 정해진 표기가 있어야 한다
    for c in out:
        for ko_t, en_t in job.glossary.items():
            if ko_t in c["ko"].replace("\n", "") and c["en"] and en_t.lower() not in c["en"].replace("\n", " ").lower():
                warnings.append(f"#{c['i']} 용어 '{ko_t}' → '{en_t}' 표기가 영어에 없음")
    for w in warnings:
        log(f"      ⚠ {w}")
    long_ko = [c["i"] for c in out if any(len(l) > KO_LINE + 2 for l in c["ko"].split("\n"))]
    return {"cues": out, "warnings": warnings, "review_status": "검토 대기",
            "_summary": f"자막 {len(out)}장면 · 경고 {len(warnings)}건" + (f" · 긴 줄 {long_ko}" if long_ko else "")}
