"""⑦ 인쇄본 — A4 PDF (문서별 + 한 권으로 묶은 인쇄 패키지). 크롬(헤드리스)으로 만든다."""

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

from .job import Job
from .util import StageError, run


def _chrome() -> str:
    for c in (os.environ.get("LS_CHROME"), "/opt/pw-browsers/chromium", shutil.which("chromium"), shutil.which("google-chrome"),
              shutil.which("chrome"), r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"):
        if c and Path(c).is_file():
            return c
    p = Path("/opt/pw-browsers")
    for f in p.glob("chromium-*/chrome-linux*/chrome") if p.exists() else []:
        return str(f)
    raise StageError("인쇄용 PDF 를 만들 크롬/엣지를 찾지 못했습니다 (LS_CHROME 환경변수로 경로 지정)")


def _pdf(chrome: str, html: Path, pdf: Path) -> None:
    run([chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--allow-file-access-from-files",
         "--no-pdf-header-footer", "--virtual-time-budget=4000", f"--print-to-pdf={pdf}", html.resolve().as_uri()])
    if not pdf.exists() or pdf.stat().st_size < 1000:
        raise StageError(f"PDF 를 만들지 못했습니다: {pdf.name}")


def run_stage(job: Job, log=print) -> dict:
    docs = job.out / "문서"
    htmls = sorted(docs.glob("*.html"))
    if not htmls:
        raise StageError("먼저 '산출물' 단계가 필요합니다")
    chrome = _chrome()
    pdfdir = job.out / "인쇄용PDF"
    pdfdir.mkdir(exist_ok=True)
    made = []
    for h in htmls:
        pdf = pdfdir / (h.stem + ".pdf")
        _pdf(chrome, h, pdf)
        made.append(pdf.name)
        log(f"      {pdf.name}")
    # 한 권으로 묶기: 각 문서의 <style>·<body> 를 이어 붙인다 (문서 사이 쪽 나눔)
    order = ["강의스크립트_한국어", "강의스크립트_영어", "자막스크립트_한영", "학습지_학생용", "학습지_교수용_정답포함"]
    parts, css = [], ""
    for stem in order:
        f = docs / f"{stem}.html"
        if not f.exists():
            continue
        t = f.read_text(encoding="utf-8")
        css = css or re.search(r"<style>(.*?)</style>", t, re.S).group(1)
        parts.append(re.search(r"<body>(.*)</body>", t, re.S).group(1))
    pkg = docs / "_인쇄패키지.html"
    pkg.write_text(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{job.get("title")}</title><style>{css}</style></head><body>'
                   + '<div class="pb"></div>'.join(parts) + "</body></html>", encoding="utf-8")
    _pdf(chrome, pkg, pdfdir / "인쇄패키지_전체.pdf")
    pkg.unlink()
    made.append("인쇄패키지_전체.pdf")
    return {"files": made, "_summary": f"PDF {len(made)}개 (A4)"}
