"""교수 검수 — 검수 결과 파일(work/review_*.json) 읽기·적용 + 검수 화면(이 컴퓨터 안 웹 페이지).

원칙: AI 결과는 늘 '검토 대기'. 교수님이 검수 화면에서 '승인'을 눌러야 '승인'이 된다.
      수정만 하고 승인하지 않으면 수정 내용은 반영하되 상태는 '검토 대기' 그대로.
      검수 화면은 127.0.0.1(이 컴퓨터)에서만 열리고, 영상·글을 외부로 보내지 않는다.

검수 파일
  review_text.json      {"status", "at", "cues":[{i,start,end,ko,en}]}
  review_study.json     {"status", "at", "study":{learning_goals, summary_ko, summary_en, keywords, quiz}}
  review_chapters.json  {"status", "at", "chapters":[{start,title_ko,title_en,type}]}
  review_cuts.json      {"status", "at", "approved":[컷 id], "rejected":[컷 id]}
"""

from __future__ import annotations

import json
import mimetypes
import re
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .job import Job
from .util import read_json, write_json

APPROVED, PENDING = "승인", "검토 대기"
KINDS = ("text", "study", "chapters", "cuts")
LABELS = {"text": "자막", "study": "요약·퀴즈", "chapters": "챕터", "cuts": "군더더기 컷"}


# ---------------------------------------------------------------- 검수 결과 읽기
def load(job: Job, kind: str) -> dict | None:
    return read_json(job.work / f"review_{kind}.json")


def status(job: Job, kind: str) -> str:
    r = load(job, kind)
    return APPROVED if r and r.get("status") == APPROVED else PENDING


def kinds_for(job: Job) -> tuple:
    """프로필에 있는 검수 항목만 (기본 프로필에는 군더더기 컷 단계가 없다)."""
    return KINDS if job.get("profile", "default") == "flip" else ("text", "study", "chapters")


def status_all(job: Job) -> dict:
    return {LABELS[k]: status(job, k) for k in kinds_for(job)}


def approved_cut_ids(job: Job) -> list[str]:
    r = load(job, "cuts") or {}
    return [str(x) for x in r.get("approved") or []]


# ---------------------------------------------------------------- 컷 적용 후 시간 옮기기
def _edit(job: Job) -> dict:
    e = read_json(job.work / "edit.json") or {}
    return e if e.get("applied") else {}


def removed_ranges(job: Job) -> list[list[float]]:
    return _edit(job).get("removed") or []


def tmap(t: float, removed: list[list[float]]) -> float | None:
    """원본 시각 → 컷 적용 영상의 시각. 잘려 나간 구간 안이면 None."""
    shift = 0.0
    for a, b in removed:
        if t >= b:
            shift += b - a
        elif t > a:
            return None
    return round(t - shift, 3)


def _tmap_start(t: float, removed) -> float:
    """구간 시작용: 잘린 구간 안이면 그 구간이 끝난 지점으로."""
    for a, b in removed:
        if a < t < b:
            t = b
    return tmap(t, removed)


# ---------------------------------------------------------------- 최종 결과 (산출물 단계가 쓰는 것)
def final_video(job: Job) -> Path:
    e = _edit(job)
    return job.work / e["file"] if e and (job.work / e["file"]).exists() else job.work / "clean.mp4"


def final_cues(job: Job) -> list[dict]:
    base = (read_json(job.work / "text.json") or {}).get("cues") or []
    r = load(job, "text")
    cues = r["cues"] if r and r.get("cues") else base
    rm = removed_ranges(job)
    out = []
    for c in cues:
        if not (c.get("ko") or "").strip() and not (c.get("en") or "").strip():
            continue
        s, e = _tmap_start(c["start"], rm), tmap(c["end"], rm)
        if e is None:          # 끝이 잘린 구간 안 → 구간 시작점에서 끝낸다
            e = next((tmap(a, rm) for a, b in rm if a < c["end"] < b), None)
        if s is None or e is None or e - s < 0.3:
            continue           # 장면 전체가 잘려 나감
        out.append({**c, "start": s, "end": e})
    for n, c in enumerate(out, 1):
        c["i"] = n
        c.setdefault("seg", n)
    return out


def final_study(job: Job) -> dict | None:
    st = read_json(job.work / "study.json")
    r = load(job, "study")
    if st and r and r.get("study"):
        st = {**st, **{k: v for k, v in r["study"].items() if v is not None}}
    if st:
        rm = removed_ranges(job)
        for q in st.get("quiz") or []:
            if "evidence_start" in q:
                q["evidence_start"] = _tmap_start(float(q["evidence_start"]), rm) or 0
    return st


def final_chapters(job: Job) -> list[dict]:
    r = load(job, "chapters")
    ch = (r or {}).get("chapters") or (read_json(job.work / "chapters.json") or {}).get("chapters")
    if not ch:
        ch = ((read_json(job.work / "study.json") or {}).get("chapters")) or []
    rm = removed_ranges(job)
    out = []
    for c in sorted(ch, key=lambda c: float(c["start"])):
        s = _tmap_start(float(c["start"]), rm)
        if s is None or (out and s - out[-1]["start"] < 1):
            continue
        out.append({**c, "start": s})
    return out


# ---------------------------------------------------------------- 검수 화면 (로컬 웹)
def _data(job: Job) -> dict:
    w = job.work
    text, study = read_json(w / "text.json") or {}, read_json(w / "study.json") or {}
    rv = {k: load(job, k) for k in KINDS}
    return {
        "job": {"id": job.id, "title": job.get("title"), "lecturer": job.lecturer, "profile": job.get("profile", "default"),
                "kind": job.kind_label},
        "status": {k: status(job, k) for k in KINDS},
        "kinds": list(kinds_for(job)),
        "cues": (rv["text"] or {}).get("cues") or text.get("cues") or [],
        "text_warnings": text.get("warnings") or [],
        "study": {**{k: study.get(k) for k in ("learning_goals", "summary_ko", "summary_en", "keywords", "quiz")},
                  **((rv["study"] or {}).get("study") or {})},
        "chapters": (rv["chapters"] or {}).get("chapters") or (read_json(w / "chapters.json") or {}).get("chapters")
        or study.get("chapters") or [],
        "chapter_types": ["도입", "개념", "사례", "시연", "정리"],
        "cuts": (read_json(w / "trim.json") or {}).get("cuts") or [],
        "cuts_review": rv["cuts"] or {},
        "slides": (read_json(w / "slides.json") or {}).get("segments") or [],
        "has_video": (w / "clean.mp4").exists(),
    }


def save(job: Job, kind: str, body: dict) -> dict:
    if kind not in KINDS:
        raise ValueError(kind)
    st = APPROVED if body.get("status") == APPROVED else PENDING
    rec = {"status": st, "at": datetime.now().strftime("%Y-%m-%d %H:%M"), "reviewer": body.get("reviewer") or ""}
    if kind == "text":
        rec["cues"] = [{k: c.get(k) for k in ("i", "seg", "start", "end", "ko", "en")} for c in body.get("cues") or []]
    elif kind == "study":
        rec["study"] = {k: body.get("study", {}).get(k) for k in ("learning_goals", "summary_ko", "summary_en", "keywords", "quiz")}
    elif kind == "chapters":
        rec["chapters"] = [{"start": float(c["start"]), "title_ko": c.get("title_ko", ""), "title_en": c.get("title_en", ""),
                            "type": c.get("type", "개념")} for c in body.get("chapters") or []]
    elif kind == "cuts":
        rec["approved"] = [str(x) for x in body.get("approved") or []]
        rec["rejected"] = [str(x) for x in body.get("rejected") or []]
    write_json(job.work / f"review_{kind}.json", rec)
    return rec


def _handler(job: Job):
    page = (Path(__file__).parent / "review_page.html").read_text(encoding="utf-8")

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):  # 조용히
            pass

        def _send(self, code, body: bytes, ctype: str, extra: dict | None = None):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(body)

        def _file(self, p: Path):
            if not p.exists():
                return self._send(404, b"not found", "text/plain")
            size = p.stat().st_size
            ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
            rng = re.match(r"bytes=(\d*)-(\d*)", self.headers.get("Range", ""))
            a, b = 0, size - 1
            if rng and (rng.group(1) or rng.group(2)):
                a = int(rng.group(1)) if rng.group(1) else size - int(rng.group(2))
                b = int(rng.group(2)) if rng.group(1) and rng.group(2) else size - 1
            if rng:
                b = min(b, size - 1, a + 8 * 1024 * 1024 - 1)    # 범위 요청은 한 번에 최대 8MB (영상 넘겨보기)
            self.send_response(206 if rng else 200)
            self.send_header("Content-Type", ctype)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(b - a + 1))
            if rng:
                self.send_header("Content-Range", f"bytes {a}-{b}/{size}")
            self.end_headers()
            with open(p, "rb") as f:
                f.seek(a)
                left = b - a + 1
                while left > 0:
                    chunk = f.read(min(left, 1024 * 1024))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    left -= len(chunk)

        def do_GET(self):
            path = self.path.split("?")[0]
            if path == "/":
                return self._send(200, page.encode("utf-8"), "text/html; charset=utf-8")
            if path == "/api/data":
                return self._send(200, json.dumps(_data(job), ensure_ascii=False).encode("utf-8"), "application/json")
            if path == "/video":
                return self._file(job.work / "clean.mp4")
            m = re.match(r"^/slides/(slide_\d{3}\.jpg)$", path)
            if m:
                return self._file(job.work / "slides" / m.group(1))
            return self._send(404, b"not found", "text/plain")

        def do_POST(self):
            m = re.match(r"^/api/save/(\w+)$", self.path)
            if not m or m.group(1) not in KINDS:
                return self._send(404, b"not found", "text/plain")
            n = int(self.headers.get("Content-Length", 0))
            try:
                rec = save(job, m.group(1), json.loads(self.rfile.read(n).decode("utf-8")))
            except (ValueError, KeyError, TypeError) as e:
                return self._send(400, str(e).encode("utf-8"), "text/plain; charset=utf-8")
            return self._send(200, json.dumps(rec, ensure_ascii=False).encode("utf-8"), "application/json")

    return H


def serve(job: Job, port: int = 8765) -> None:
    srv = ThreadingHTTPServer(("127.0.0.1", port), _handler(job))
    print(f"검수 화면: http://127.0.0.1:{port}  (이 컴퓨터 안에서만 열립니다 · 끝내려면 Ctrl+C)")
    print(f"검수를 마친 뒤:  ls_cli.py run {job.id}   (바뀐 단계만 다시 만듭니다)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n검수 화면을 닫았습니다.")
