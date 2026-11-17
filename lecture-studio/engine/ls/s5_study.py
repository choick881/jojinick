"""⑤ 요약·학습 자료 — 학습목표, 요약, 키워드, 챕터(타임코드), 퀴즈(정답·해설·근거)."""

from __future__ import annotations

from .job import Job
from .llm import complete_json
from .util import StageError, read_json


def run_stage(job: Job, log=print) -> dict:
    txt = read_json(job.work / "text.json")
    if not txt:
        raise StageError("먼저 '자막' 단계가 필요합니다")
    n = int((job.get("quiz") or {}).get("count", 3))
    payload = {"title": job.get("title"), "lecturer": job.lecturer, "kind": job.kind_label, "quiz_count": n,
               "transcript": [{"start": c["start"], "ko": c["ko"].replace("\n", " ")} for c in txt["cues"]]}
    res = complete_json(job, "study", payload, log)

    problems = []
    quiz = res.get("quiz") or []
    if len(quiz) != n:
        problems.append(f"퀴즈 {len(quiz)}문항 (요청 {n})")
    for k, q in enumerate(quiz, 1):
        if not q.get("answer") or not q.get("explanation_ko"):
            problems.append(f"퀴즈 {k}: 정답 또는 해설 없음")
        if q.get("type") == "mcq" and not (3 <= len(q.get("choices_ko") or []) <= 5):
            problems.append(f"퀴즈 {k}: 객관식 보기 개수")
    if not res.get("summary_ko") or not res.get("chapters"):
        problems.append("요약 또는 챕터 없음")
    if problems:
        raise StageError("요약·퀴즈 결과를 확인해 주세요:\n  · " + "\n  · ".join(problems))
    res["review_status"] = "검토 대기"
    res["_summary"] = f"챕터 {len(res['chapters'])} · 키워드 {len(res.get('keywords') or [])} · 퀴즈 {len(quiz)}문항"
    return res
