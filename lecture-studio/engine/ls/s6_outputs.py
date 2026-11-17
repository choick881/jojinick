"""⑥ 산출물 — 자막 파일, 자막 입힌 영상, 강의 스크립트, 자막 스크립트, 요약·퀴즈 학습지."""

from __future__ import annotations

import shutil

from . import subs
from .docs import Doc
from .job import Job
from .util import FONTS, StageError, ff_path, mmss, read_json, run

KO_SIZE, EN_SIZE = 56, 46


def _burn(job: Job, ass_path, dst) -> None:
    vf = f"ass='{ff_path(ass_path)}':fontsdir='{ff_path(FONTS)}'"
    run(["ffmpeg", "-y", "-v", "error", "-i", job.work / "clean.mp4", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", dst])


def run_stage(job: Job, log=print) -> dict:
    txt, study = read_json(job.work / "text.json"), read_json(job.work / "study.json")
    if not (job.work / "clean.mp4").exists() or not txt:
        raise StageError("먼저 앞 단계(영상 정리·자막)가 필요합니다")
    cues = txt["cues"]
    out = job.out
    (out / "자막").mkdir(parents=True, exist_ok=True)
    (out / "문서").mkdir(exist_ok=True)
    made = []

    # 1) 자막 파일
    for lang, key, nm in (("ko", "ko", "한국어"), ("en", "en", "영어")):
        (out / "자막" / f"자막_{nm}.srt").write_text(subs.srt(cues, key), encoding="utf-8")
        (out / "자막" / f"자막_{nm}.vtt").write_text(subs.vtt(cues, key), encoding="utf-8")
        made += [f"자막/자막_{nm}.srt", f"자막/자막_{nm}.vtt"]

    # 2) 영상: 영어 자막 입힌 영상 / 한글 자막 입힌 영상 / 자막 없음 / 자막 선택형
    for key, size, nm in (("en", EN_SIZE, "영어자막"), ("ko", KO_SIZE, "한글자막")):
        a = job.work / f"burn_{key}.ass"
        a.write_text(subs.ass(cues, key, size), encoding="utf-8")
        dst = out / f"영상_{nm}.mp4"
        log(f"      영상에 {nm} 입히는 중 …")
        _burn(job, a, dst)
        made.append(dst.name)
    shutil.copy(job.work / "clean.mp4", out / "영상_자막없음.mp4")
    made.append("영상_자막없음.mp4")
    run(["ffmpeg", "-y", "-v", "error", "-i", job.work / "clean.mp4", "-i", out / "자막" / "자막_한국어.srt",
         "-i", out / "자막" / "자막_영어.srt", "-map", "0:v", "-map", "0:a", "-map", "1", "-map", "2", "-c:v", "copy",
         "-c:a", "copy", "-c:s", "mov_text", "-metadata:s:s:0", "language=kor", "-metadata:s:s:1", "language=eng",
         "-movflags", "+faststart", out / "영상_자막선택형.mp4"])
    made.append("영상_자막선택형.mp4")

    # 3) 문서
    lec, title = job.lecturer, job.get("title")
    host = (job.get("event") or {}).get("host") or ""
    base_meta = [f"{job.kind_label} · {title}" + (f" — {job.get('subtitle')}" if job.get("subtitle") else ""),
                 f"{lec.get('name', '')} · {lec.get('affiliation', '')}" + (f"  |  {host}" if host else "")]
    base_meta_en = [f"{title}" if not job.get("subtitle") else f"{title}",
                    f"{lec.get('name_en') or lec.get('name', '')} · {lec.get('affiliation_en') or ''}"]
    docs = {}

    segs = {}
    for c in cues:
        segs.setdefault(c["seg"], []).append(c)
    for lang, key, nm, meta in (("ko", "ko", "한국어", base_meta), ("en", "en", "영어", base_meta_en)):
        d = Doc(f"강의 스크립트 ({nm})" if lang == "ko" else "Lecture Script (English)", meta + ["※ AI 가 만든 초안입니다. 교수님 검수 후 확정됩니다."] if lang == "ko"
                else meta + ["* AI-generated draft — pending the lecturer's review."], lang)
        chs = (study or {}).get("chapters") or []
        starts = [(ch["start"], ch.get("title_" + lang) or ch.get("title_ko")) for ch in chs]
        ci = 0
        for s_id in sorted(segs):
            t0 = segs[s_id][0]["start"]
            while ci < len(starts) and starts[ci][0] <= t0 + 0.5:
                d.h2(f"{mmss(starts[ci][0])}  {starts[ci][1]}")
                ci += 1
            d.tsp(t0, " ".join(c[key].replace("\n", " ") for c in segs[s_id] if c[key]))
        docs[f"강의스크립트_{nm}"] = d

    d = Doc("자막 스크립트 (한국어 · 영어)", base_meta + [f"자막 {len(cues)}장면 · 한 줄 한국어 18자/영어 42자 이내"])
    d.table(["#", "시간", "한국어", "English"],
            [[str(c["i"]), f"{c['start']:.1f}–{c['end']:.1f}", c["ko"].replace("\n", " "), c["en"].replace("\n", " ")] for c in cues],
            ["5%", "13%", "38%", "44%"])
    docs["자막스크립트_한영"] = d

    if study:
        for with_ans, nm in ((False, "학습지_학생용"), (True, "학습지_교수용_정답포함")):
            d = Doc(f"{title} — 학습지" + (" (교수용·정답 포함)" if with_ans else " (학생용)"), base_meta)
            d.h2("학습 목표").ul(study.get("learning_goals") or [])
            d.h2("강의 요약").p(study["summary_ko"]).p(study.get("summary_en", ""), "muted")
            d.h2("핵심 키워드").table(["한국어", "English"], [[k["ko"], k.get("en", "")] for k in study.get("keywords", [])], ["50%", "50%"])
            d.h2("챕터")
            d.table(["시작", "제목", "내용"], [[mmss(ch["start"]), f"{ch['title_ko']}\n{ch.get('title_en', '')}", ch.get("summary_ko", "")]
                                             for ch in study["chapters"]], ["10%", "35%", "55%"])
            d.h2("확인 퀴즈")
            kind = {"mcq": "객관식", "ox": "O/X", "short": "서술형"}
            for n, q in enumerate(study["quiz"], 1):
                d.h3(f"Q{n}. [{kind.get(q['type'], q['type'])}] {q['question_ko']}")
                d.p(q.get("question_en", ""), "muted")
                if q.get("choices_ko"):
                    d.ul([f"{'①②③④⑤'[i]} {ko}" + (f"  /  {en}" if i < len(q.get('choices_en') or []) and (en := q['choices_en'][i]) else "")
                          for i, ko in enumerate(q["choices_ko"])])
                if q["type"] == "short" and not with_ans:
                    d.p("답: ______________________________________________")
                if with_ans:
                    d.p(f"정답: {q['answer']}  ·  수준: {q.get('bloom', '')}  ·  근거: 강의 {mmss(q.get('evidence_start', 0))}", "ans")
                    d.p(f"해설: {q['explanation_ko']}")
                    d.p(q.get("explanation_en", ""), "muted")
            docs[nm] = d

    for name, doc in docs.items():
        p = out / "문서" / name
        p.with_suffix(".html").write_text(doc.to_html(), encoding="utf-8")
        p.with_suffix(".txt").write_text(doc.to_txt(), encoding="utf-8")
        doc.to_docx(p.with_suffix(".docx"))
        made += [f"문서/{name}.html", f"문서/{name}.txt", f"문서/{name}.docx"]
    return {"files": made, "_summary": f"파일 {len(made)}개"}
