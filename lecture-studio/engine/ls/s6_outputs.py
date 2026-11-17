"""⑥ 산출물 — 자막 파일, 자막 입힌 영상, 강의 스크립트, 자막 스크립트, 요약·퀴즈 학습지."""

from __future__ import annotations

import shutil

from . import review, subs
from .docs import Doc
from .job import Job
from .util import FONTS, StageError, duration, ff_path, mmss, read_json, run

KO_SIZE, EN_SIZE = 56, 46


def _burn(job: Job, ass_path, dst, src=None) -> None:
    vf = f"ass='{ff_path(ass_path)}':fontsdir='{ff_path(FONTS)}'"
    run(["ffmpeg", "-y", "-v", "error", "-i", src or job.work / "clean.mp4", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", dst])


def run_stage(job: Job, log=print) -> dict:
    txt = read_json(job.work / "text.json")
    if not (job.work / "clean.mp4").exists() or not txt:
        raise StageError("먼저 앞 단계(영상 정리·자막)가 필요합니다")
    # 검수 결과(review_*.json)·승인 컷을 반영한 최종본
    src = review.final_video(job)
    cues = review.final_cues(job)
    study = review.final_study(job)
    chapters = review.final_chapters(job)
    st = review.status_all(job)
    if src.name != "clean.mp4":
        log(f"      승인 컷 적용 영상 사용: {src.name} (자막·챕터 시각도 맞춰 옮김)")
    out = job.out
    (out / "자막").mkdir(parents=True, exist_ok=True)
    (out / "문서").mkdir(exist_ok=True)
    made = []

    # 1) 자막 파일 (내용이 있는 언어만 — 번역을 쓰지 않는 강의도 멈추지 않게)
    langs = [(key, nm) for key, nm in (("ko", "한국어"), ("en", "영어")) if any((c.get(key) or "").strip() for c in cues)]
    if not langs:
        raise StageError("자막 글이 비어 있습니다 (자막 단계·검수 결과를 확인해 주세요)")
    for key, nm in langs:
        (out / "자막" / f"자막_{nm}.srt").write_text(subs.srt(cues, key), encoding="utf-8")
        (out / "자막" / f"자막_{nm}.vtt").write_text(subs.vtt(cues, key), encoding="utf-8")
        made += [f"자막/자막_{nm}.srt", f"자막/자막_{nm}.vtt"]
    have = {k for k, _ in langs}

    # 2) 영상: 영어 자막 입힌 영상 / 한글 자막 입힌 영상 / 자막 없음 / 자막 선택형
    for key, size, nm in (("en", EN_SIZE, "영어자막"), ("ko", KO_SIZE, "한글자막")):
        if key not in have:
            log(f"      {nm}: 글이 없어 건너뜀")
            continue
        a = job.work / f"burn_{key}.ass"
        a.write_text(subs.ass(cues, key, size), encoding="utf-8")
        dst = out / f"영상_{nm}.mp4"
        log(f"      영상에 {nm} 입히는 중 …")
        _burn(job, a, dst, src)
        made.append(dst.name)
    shutil.copy(src, out / "영상_자막없음.mp4")
    made.append("영상_자막없음.mp4")
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", src]
    for key, nm in langs:
        cmd += ["-i", out / "자막" / f"자막_{nm}.srt"]
    cmd += ["-map", "0:v", "-map", "0:a"] + sum((["-map", str(k + 1)] for k in range(len(langs))), [])
    cmd += ["-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text"]
    for k, (key, _nm) in enumerate(langs):
        cmd += [f"-metadata:s:s:{k}", "language=" + {"ko": "kor", "en": "eng"}[key]]
    run(cmd + ["-movflags", "+faststart", out / "영상_자막선택형.mp4"])
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
    def note(kind: str, lang: str) -> str:
        r = review.load(job, kind) or {}
        if st[review.LABELS[kind]] == review.APPROVED:
            return f"※ 교수님 검수 완료 ({r.get('at', '')})" if lang == "ko" else f"* Reviewed and approved by the lecturer ({r.get('at', '')})"
        return "※ 검토 대기 — AI 가 만든 초안입니다. 교수님 검수 후 확정됩니다." if lang == "ko" else "* PENDING REVIEW — AI-generated draft."

    for lang, key, nm, meta in (("ko", "ko", "한국어", base_meta), ("en", "en", "영어", base_meta_en)):
        d = Doc(f"강의 스크립트 ({nm})" if lang == "ko" else "Lecture Script (English)", meta + [note("text", lang)], lang)
        chs = chapters
        starts = [(ch["start"], ch.get("title_" + lang) or ch.get("title_ko")) for ch in chs]
        ci = 0
        for s_id in sorted(segs):
            t0 = segs[s_id][0]["start"]
            while ci < len(starts) and starts[ci][0] <= t0 + 0.5:
                d.h2(f"{mmss(starts[ci][0])}  {starts[ci][1]}")
                ci += 1
            d.tsp(t0, " ".join(c[key].replace("\n", " ") for c in segs[s_id] if c[key]))
        docs[f"강의스크립트_{nm}"] = d

    d = Doc("자막 스크립트 (한국어 · 영어)", base_meta + [f"자막 {len(cues)}장면 · 한 줄 한국어 18자/영어 42자 이내", note("text", "ko")])
    d.table(["#", "시간", "한국어", "English"],
            [[str(c["i"]), f"{c['start']:.1f}–{c['end']:.1f}", c["ko"].replace("\n", " "), c["en"].replace("\n", " ")] for c in cues],
            ["5%", "13%", "38%", "44%"])
    docs["자막스크립트_한영"] = d

    if study:
        for with_ans, nm in ((False, "학습지_학생용"), (True, "학습지_교수용_정답포함")):
            d = Doc(f"{title} — 학습지" + (" (교수용·정답 포함)" if with_ans else " (학생용)"),
                    base_meta + ([note("study", "ko")] if with_ans else []))
            d.h2("학습 목표").ul(study.get("learning_goals") or [])
            d.h2("강의 요약").p(study["summary_ko"]).p(study.get("summary_en", ""), "muted")
            d.h2("핵심 키워드").table(["한국어", "English"], [[k["ko"], k.get("en", "")] for k in study.get("keywords", [])], ["50%", "50%"])
            d.h2("챕터")
            d.table(["시작", "제목", "내용"], [[mmss(ch["start"]), f"{ch['title_ko']}\n{ch.get('title_en', '')}",
                                              (f"[{ch['type']}] " if ch.get("type") else "") + ch.get("summary_ko", "")]
                                             for ch in chapters], ["10%", "35%", "55%"])
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
    # 4) 챕터 타임스탬프 (LMS·유튜브 설명란용 텍스트 + 플레이어용 WebVTT 챕터)
    if chapters:
        dur_v = duration(src)
        lines = [f"{mmss(c['start'])} {c['title_ko']}" for c in chapters]
        (out / "챕터_타임스탬프.txt").write_text(
            "\n".join(lines) + f"\n\n({st['챕터']} · 영상 {mmss(dur_v)})\n", encoding="utf-8")
        ends = [c["start"] for c in chapters[1:]] + [dur_v]
        (out / "자막" / "챕터.vtt").write_text("WEBVTT\n\n" + "\n".join(
            f"{subs._t(c['start'], '.')} --> {subs._t(e, '.')}\n{c['title_ko']}\n" for c, e in zip(chapters, ends)), encoding="utf-8")
        made += ["챕터_타임스탬프.txt", "자막/챕터.vtt"]

    # 5) 검수 상태 — 승인 전에는 '검토 대기'
    edit = read_json(job.work / "edit.json") or {}
    (out / "검수상태.txt").write_text("\n".join(
        [f"{k}: {v}" for k, v in st.items()] +
        ([f"적용한 컷: {', '.join(edit.get('applied') or []) or '없음'}" + (f" ({edit.get('removed_sec')}초 줄임)" if edit.get("applied") else "")]
         if job.get("profile") == "flip" else []) + [
         "※ '검토 대기' 항목은 AI 초안입니다. 검수 화면(ls_cli.py review)에서 승인한 뒤 다시 실행하세요."]) + "\n", encoding="utf-8")
    made.append("검수상태.txt")
    pend = [k for k, v in st.items() if v != review.APPROVED]
    return {"files": made, "review_status": st, "video_source": src.name,
            "_summary": f"파일 {len(made)}개 · " + ("모두 승인" if not pend else f"검토 대기: {', '.join(pend)}")}

