"""단계 실행기 — 결과를 work/<단계>.json 에 저장하고, 입력이 바뀌지 않은 단계는 건너뛴다.

프로필(job.yaml 의 profile)
  default  기존 7단계 (특강·행사·전공 강의 후반작업)
  flip     플립러닝 사전학습 영상 — 슬라이드 전환·챕터·군더더기 컷 제안·컷 적용 단계를 더한다
코어 약속: STAGES·NAMES·LABEL·_key·run 은 그대로 두고 프로필은 '추가'만 한다 (숏폼 프로필과 공유).
"""

from __future__ import annotations

import importlib
import time
from datetime import datetime

from .job import Job
from .util import StageError, file_sig, read_json, sha, write_json

# (이름, 모듈, 이 단계에 영향을 주는 job.yaml 항목)
STAGES = [
    ("ingest", "s1_ingest", ["mask"]),
    ("clean", "s2_clean", []),
    ("asr", "s3_asr", ["asr", "source_language"]),
    ("text", "s4_text", ["glossary", "target_languages", "llm", "lecturer", "title"]),
    ("study", "s5_study", ["quiz", "llm", "title", "kind"]),
    ("outputs", "s6_outputs", ["title", "subtitle", "lecturer", "course", "event", "kind", "target_languages"]),
    ("print", "s7_print", ["title", "subtitle", "lecturer", "course", "event", "kind"]),
]
NAMES = [s[0] for s in STAGES]
LABEL = {"ingest": "① 접수·점검", "clean": "② 영상 정리", "asr": "③ 받아쓰기", "text": "④ 자막(한/영)",
         "study": "⑤ 요약·퀴즈", "outputs": "⑥ 산출물", "print": "⑦ 인쇄본"}

# ---- 프로필 (추가) ----
_S = {s[0]: s for s in STAGES}
FLIP_STAGES = [
    _S["ingest"], _S["clean"], _S["asr"],
    ("slides", "s8_slides", ["slides", "mask"]),
    _S["text"], _S["study"],
    ("chapters", "s9_chapters", ["chapters", "slides"]),
    ("trim", "s10_trim", ["trim"]),
    ("edit", "s11_edit", ["trim"]),
    _S["outputs"], _S["print"],
]
PROFILES = {"default": STAGES, "flip": FLIP_STAGES}
LABEL.update({"slides": "⑧ 슬라이드 전환", "chapters": "⑨ 챕터", "trim": "⑩ 군더더기 컷 제안", "edit": "⑪ 승인 컷 적용"})
ALL_NAMES = list(dict.fromkeys(n for st in PROFILES.values() for n, _m, _c in st))

# 단계별로 '검수 결과 파일'이 바뀌면 다시 실행 (review 화면이 저장하는 파일)
REVIEW_DEPS = {"chapters": ["review_chapters.json"], "edit": ["review_cuts.json"],
               "outputs": ["review_*.json"], "print": ["review_*.json"]}


def stages_for(job: Job) -> list:
    prof = job.get("profile", "default") or "default"
    if prof not in PROFILES:
        raise SystemExit(f"알 수 없는 profile: {prof} (가능: {', '.join(PROFILES)})")
    return PROFILES[prof]


def names_for(job: Job) -> list[str]:
    return [s[0] for s in stages_for(job)]


def _key(job: Job, idx: int, prev_key: str, stages: list | None = None) -> str:
    stages = stages or STAGES
    name, _mod, cfg = stages[idx]
    parts = [name, {k: job.data.get(k) for k in cfg}, prev_key]
    if name == "ingest":
        parts.append(file_sig(job.video))
    if name in ("text", "study"):  # 직접 작성한 결과 파일이 바뀌면 다시
        for f in sorted(job.input.glob("llm_*.json")):
            parts.append(file_sig(f))
    if name == "outputs":
        parts.append([file_sig(f) for f in sorted(job.work.glob("review_*.json"))])
    if name == "slides":  # 함께 받은 슬라이드 파일(PDF)
        parts.append([file_sig(f) for f in sorted(job.input.glob("*.pdf"))])
    for pat in REVIEW_DEPS.get(name, []):
        if name != "outputs":
            parts.append([file_sig(f) for f in sorted(job.work.glob(pat))])
    return sha(*parts)


def _runlog(job: Job, rec: dict) -> None:
    """실행 로그: work/run_log.jsonl (기계용) + out/실행로그.txt (사람용)."""
    import json
    with open(job.work / "run_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    with open(job.out / "실행로그.txt", "a", encoding="utf-8") as f:
        f.write(f"{rec['at']}  {rec['label']:<14} {rec['status']:<6} {rec.get('sec', 0):>6.1f}초  {rec.get('summary', '')}\n")


def run(job: Job, start: str | None = None, only: str | None = None, log=print, force: bool = False) -> None:
    job.work.mkdir(exist_ok=True)
    job.out.mkdir(exist_ok=True)
    stages = stages_for(job)
    names = [s[0] for s in stages]
    for nm in (start, only):
        if nm and nm not in names:
            raise SystemExit(f"이 작업(profile: {job.get('profile', 'default')})에는 '{nm}' 단계가 없습니다: {', '.join(names)}")
    begin = names.index(start) if start else 0
    prev = ""
    total = time.time()
    now = lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # noqa: E731
    for i, (name, mod, _cfg) in enumerate(stages):
        key = _key(job, i, prev, stages)
        path = job.work / f"{name}.json"
        cached = read_json(path)
        skip = (only and name != only) or i < begin and cached
        if not skip and not force and cached and cached.get("_key") == key and i >= begin and not start and not only:
            log(f"  {LABEL[name]}  — 이미 끝남 (건너뜀)")
            _runlog(job, {"at": now(), "stage": name, "label": LABEL[name], "status": "건너뜀",
                          "summary": cached.get("_summary", "")})
            prev = key
            continue
        if skip:
            prev = cached.get("_key", key) if cached else key
            continue
        log(f"  {LABEL[name]}  시작")
        t = time.time()
        try:
            res = importlib.import_module(f"ls.{mod}").run_stage(job, log)
        except StageError as e:
            _runlog(job, {"at": now(), "stage": name, "label": LABEL[name], "status": "멈춤",
                          "sec": round(time.time() - t, 1), "summary": str(e).splitlines()[0]})
            raise SystemExit(f"\n[{LABEL[name]}] {e}") from e
        res["_key"] = key
        res["_sec"] = round(time.time() - t, 1)
        write_json(path, res)
        log(f"  {LABEL[name]}  끝 ({time.time() - t:.0f}초) — {res.get('_summary', '')}")
        _runlog(job, {"at": now(), "stage": name, "label": LABEL[name], "status": "완료", "sec": res["_sec"],
                      "summary": res.get("_summary", "")})
        prev = key
    log(f"  전체 {time.time() - total:.0f}초")
