"""단계 실행기 — 결과를 work/<단계>.json 에 저장하고, 입력이 바뀌지 않은 단계는 건너뛴다."""

from __future__ import annotations

import importlib
import time

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


def _key(job: Job, idx: int, prev_key: str) -> str:
    name, _mod, cfg = STAGES[idx]
    parts = [name, {k: job.data.get(k) for k in cfg}, prev_key]
    if name == "ingest":
        parts.append(file_sig(job.video))
    if name in ("text", "study"):  # 직접 작성한 결과 파일이 바뀌면 다시
        for f in sorted(job.input.glob("llm_*.json")):
            parts.append(file_sig(f))
    if name == "outputs":
        parts.append([file_sig(f) for f in sorted(job.work.glob("review_*.json"))])
    return sha(*parts)


def run(job: Job, start: str | None = None, only: str | None = None, log=print, force: bool = False) -> None:
    job.work.mkdir(exist_ok=True)
    job.out.mkdir(exist_ok=True)
    begin = NAMES.index(start) if start else 0
    prev = ""
    for i, (name, mod, _cfg) in enumerate(STAGES):
        key = _key(job, i, prev)
        path = job.work / f"{name}.json"
        cached = read_json(path)
        skip = (only and name != only) or i < begin and cached
        if not skip and not force and cached and cached.get("_key") == key and i >= begin and not start and not only:
            log(f"  {LABEL[name]}  — 이미 끝남 (건너뜀)")
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
            raise SystemExit(f"\n[{LABEL[name]}] {e}") from e
        res["_key"] = key
        write_json(path, res)
        log(f"  {LABEL[name]}  끝 ({time.time() - t:.0f}초) — {res.get('_summary', '')}")
        prev = key
