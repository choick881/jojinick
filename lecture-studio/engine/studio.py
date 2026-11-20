#!/usr/bin/env python3
"""강의 편집기 — 교수님용 실행 프로그램 (Windows: 2_강의영상_편집.bat 에 영상을 끌어다 놓기)

  영상을 끌어다 놓으면 → 제목·이름을 묻고 → 끝까지 자동 처리 → 검수 화면 → 다시 만들기
  영상은 복사하지 않고 원래 자리에서 읽는다 (수 GB 강의도 그대로). 영상·음성은 이 컴퓨터 밖으로 나가지 않는다.

  python engine/studio.py [영상파일]                      대화식
  python engine/studio.py 영상.mp4 --title 제목 --name 이름 --no-ai --yes --no-menu   (자동 시험용)
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import subprocess
import sys
import threading
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ls import job as jobmod  # noqa: E402
from ls import pipeline, review  # noqa: E402
from ls.util import JOBS, need_tools  # noqa: E402

VIDEO_EXT = {".mp4", ".mov", ".mkv", ".avi", ".m4v", ".wmv", ".webm"}
LINE = "─" * 60


def ask(q: str, default: str = "") -> str:
    a = input(f"{q}" + (f" [{default}]" if default else "") + ": ").strip().strip('"')
    return a or default


def yes(q: str, default: bool = True) -> bool:
    a = input(f"{q} ({'Y/n' if default else 'y/N'}): ").strip().lower()
    return default if not a else a.startswith(("y", "ㅛ", "예", "네"))


def open_path(p: Path) -> None:
    try:
        if sys.platform.startswith("win"):
            os.startfile(str(p))  # noqa: S606 — 결과 폴더 열기
        elif sys.platform == "darwin":
            subprocess.run(["open", str(p)], check=False)
        else:
            print(f"   폴더: {p}")
    except OSError:
        print(f"   폴더: {p}")


def job_id_for(video: Path) -> str:
    stem = re.sub(r"[^0-9A-Za-z가-힣]+", "_", video.stem).strip("_")[:30] or "lecture"
    base = f"{dt.date.today():%Y%m%d}_{stem}"
    jid, n = base, 2
    while (JOBS / jid).exists():
        jid, n = f"{base}_{n}", n + 1
    return jid


def make_job(video: Path, a) -> jobmod.Job:
    print(LINE)
    print(f"영상: {video}  ({video.stat().st_size / 1e6:,.0f}MB)")
    title = a.title or ask("강의 제목 (예: 3주차 1차시 — 수요와 공급)", video.stem)
    name = a.name or ask("교수님 성함", os.environ.get("LS_LECTURER", ""))
    while not name:
        name = ask("교수님 성함 (꼭 필요합니다)")
    agreed = True if a.yes else yes("교수님이 이 영상의 AI 후반작업(자막·컷 제안 등)에 동의하셨나요?", True)
    if not agreed:
        raise SystemExit("교수님 동의 없이는 작업을 시작하지 않습니다.")
    backend = "none"
    if not a.no_ai:
        print("\nAI(Claude)를 쓰면 자막 교정·영어 번역·요약·퀴즈를 자동으로 만듭니다. 이때 '글'만 보내고 영상·음성은 보내지 않습니다.")
        if yes("AI 를 사용할까요? (학교 보안 정책에서 허용된 경우만)", False):
            if not os.environ.get("ANTHROPIC_API_KEY"):
                import getpass
                key = getpass.getpass("Claude API 키를 붙여 넣으세요 (화면에 보이지 않음, 이 컴퓨터에만 저장): ").strip()
                if key:
                    os.environ["ANTHROPIC_API_KEY"] = key
                    if sys.platform.startswith("win"):
                        subprocess.run(["setx", "ANTHROPIC_API_KEY", key], capture_output=True, check=False)
            backend = "anthropic" if os.environ.get("ANTHROPIC_API_KEY") else "none"
    if backend == "none":
        print("→ AI 없이 진행합니다: 자막은 받아쓴 글 그대로(검수 화면에서 고침), 요약·퀴즈는 만들지 않습니다.")

    jid = job_id_for(video)
    d = jobmod.create(jid, profile="flip")
    s = (d / "job.yaml").read_text(encoding="utf-8")
    q = lambda v: '"' + v.replace("\\", "/").replace('"', "'") + '"'  # noqa: E731
    s = s.replace('title: ""', f"title: {q(title)}", 1)
    s = s.replace('  name: ""', f"  name: {q(name)}", 1)
    s = s.replace("video: input.mp4", f"video: {q(str(video.resolve()))}", 1)   # 복사하지 않고 원래 자리에서 읽기
    s = s.replace("lecturer_agreed: false", "lecturer_agreed: true", 1)
    if backend == "anthropic":
        s = s.replace("external_ai_text: false", "external_ai_text: true", 1)
    s = s.replace("llm: { backend: file }", f"llm: {{ backend: {backend} }}", 1)
    if backend == "none":
        s = s.replace("target_languages: [en]", "target_languages: []", 1)
    (d / "job.yaml").write_text(s, encoding="utf-8")
    print(f"작업 폴더: {d}")
    return jobmod.load(jid)


def pick_job() -> jobmod.Job | None:
    jobs = sorted([p for p in JOBS.iterdir() if (p / "job.yaml").exists()], key=lambda p: p.stat().st_mtime, reverse=True) \
        if JOBS.exists() else []
    print(LINE)
    if jobs:
        print("최근 작업:")
        for i, p in enumerate(jobs[:9], 1):
            print(f"  {i}) {p.name}")
    a = ask("작업 번호를 고르거나, 영상 파일을 이 창에 끌어다 놓고 Enter")
    if a.isdigit() and 1 <= int(a) <= min(9, len(jobs)):
        return jobmod.load(jobs[int(a) - 1].name)
    if a and Path(a).is_file():
        return None if Path(a).suffix.lower() not in VIDEO_EXT else make_job(Path(a), argparse.Namespace(title="", name="", yes=False, no_ai=False))
    print("영상 파일이나 작업 번호를 찾지 못했습니다.")
    return None


def run(job: jobmod.Job) -> bool:
    print(LINE)
    print("처리를 시작합니다. 받아쓰기는 영상 길이의 1~2배 정도 걸립니다 (창을 닫지 마세요).")
    try:
        pipeline.run(job)
    except SystemExit as e:
        print(f"\n멈춤: {e}")
        return False
    print(f"\n끝났습니다 → {job.out}")
    return True


def open_review(job: jobmod.Job, port: int = 8765) -> None:
    from http.server import ThreadingHTTPServer
    for p in range(port, port + 20):
        try:
            srv = ThreadingHTTPServer(("127.0.0.1", p), review._handler(job))
            break
        except OSError:
            continue
    else:
        print("검수 화면을 열 포트를 찾지 못했습니다.")
        return
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_address[1]}"
    print(f"\n검수 화면: {url}  (이 컴퓨터 안에서만 열립니다)")
    webbrowser.open(url)
    input("검수(수정·승인)를 마쳤으면 이 창에서 Enter → ")
    srv.shutdown()


def menu(job: jobmod.Job) -> None:
    while True:
        print(LINE)
        st = review.status_all(job)
        print(f"[{job.id}]  " + " · ".join(f"{k} {v}" for k, v in st.items()))
        print("  1) 검수 화면 열기   2) 검수 반영해서 다시 만들기   3) 결과 폴더 열기   4) 끝내기")
        c = ask("번호", "1" if any(v != review.APPROVED for v in st.values()) else "4")
        if c == "1":
            open_review(job)
        elif c == "2":
            run(job)
        elif c == "3":
            open_path(job.out)
        else:
            break


def main() -> None:
    ap = argparse.ArgumentParser(description="강의 편집기")
    ap.add_argument("video", nargs="?")
    ap.add_argument("--title", default="")
    ap.add_argument("--name", default="")
    ap.add_argument("--no-ai", action="store_true", help="AI 미사용 (받아쓴 글 그대로)")
    ap.add_argument("--yes", action="store_true", help="동의 질문에 '예' (자동 시험용)")
    ap.add_argument("--no-menu", action="store_true", help="처리 후 메뉴·검수 화면 없이 끝내기")
    a = ap.parse_args()
    print("=" * 60 + "\n  HY FLIP 강의 편집기 — 플립러닝 사전학습 영상 자동 편집\n" + "=" * 60)
    need_tools()
    job = None
    if a.video:
        v = Path(a.video.strip('"'))
        if not v.is_file() or v.suffix.lower() not in VIDEO_EXT:
            raise SystemExit(f"영상 파일이 아닙니다: {v}")
        job = make_job(v, a)
    else:
        while job is None:
            job = pick_job()
    ok = run(job)
    if a.no_menu:
        raise SystemExit(0 if ok else 1)
    if ok:
        open_path(job.out)
        if yes("지금 검수 화면을 열까요?", True):
            open_review(job)
            if yes("검수 내용을 반영해 다시 만들까요?", True):
                run(job)
    menu(job)


if __name__ == "__main__":
    main()
