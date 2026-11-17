"""작업(job.yaml) 로드·검증.

원칙: 강의 영상은 교수님의 저작물이고, 번역·요약·퀴즈에는 '글'만 외부 AI 서비스로 보낸다.
외부 AI 사용 동의(consent.external_ai_text)와 교수 확인이 없으면 AI 단계를 시작하지 않는다.
영상·음성은 어떤 경우에도 외부로 보내지 않는다(받아쓰기는 이 컴퓨터 안에서만).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .util import JOBS

KINDS = {
    "major": "전공 강의",
    "general": "교양 강의",
    "language": "외국어 강의",
    "special": "초청강의·특강",
    "event": "행사 강의",
    "flip": "플립러닝 사전학습 영상",
}

JOB_TEMPLATE = """# 강의 후반작업 작업서 — HY FLIP 강의 편집 시스템
id: {id}
kind: special                 # major 전공 | general 교양 | language 외국어 | special 초청강의·특강 | event 행사
title: ""                     # 강의 제목
subtitle: ""                  # 부제 (선택)
lecturer:
  name: ""                    # 교수·연사 이름
  name_en: ""                 # 영문 이름 (영어 자막·문서용)
  affiliation: ""
  affiliation_en: ""
course: {{ name: "", term: "" }}   # 과목명·학기 (전공·교양·외국어)
event: {{ host: "", date: "" }}    # 주최·일자 (특강·행사)
video: input.mp4              # input/ 폴더 안의 영상 파일
source_language: ko           # ko | en  (영어 강의면 en → 한국어 자막)
target_languages: [en]        # 번역 자막 언어
glossary: {{}}                 # 용어 사전  {{교수학습: teaching and learning}}
mask: auto                    # auto = 녹화 도구 위젯 자동 가림 | none | [{{x,y,w,h}}]
quiz: {{ count: 3 }}
consent:                      # 하나라도 비어 있으면 AI 단계를 시작하지 않습니다
  lecturer_agreed: false      # 교수님이 AI 후반작업·글 전송에 동의했습니다
  external_ai_text: false     # 번역·요약·퀴즈를 위해 '글'을 외부 AI 서비스(Claude)에 보내도 됩니다
asr: {{ backend: sherpa-whisper, model: medium }}   # sherpa-whisper | faster-whisper | words-file
llm: {{ backend: file }}                            # anthropic (API 키 필요) | file (직접 작성한 결과) | none (AI 미사용)
"""


FLIP_TEMPLATE = """# 플립러닝 사전학습 영상 작업서 — HY FLIP 강의 편집 시스템 (profile: flip)
id: {id}
profile: flip                 # flip = 슬라이드 전환·챕터·군더더기 컷 제안 단계 포함
kind: flip
title: ""                     # 차시 제목 (예: 3주차 1차시 — 수요와 공급)
subtitle: ""
lecturer:
  name: ""
  name_en: ""
  affiliation: ""
  affiliation_en: ""
course: {{ name: "", term: "", week: "" }}   # 과목명·학기·주차
event: {{ host: "", date: "" }}
video: input.mp4              # input/ 폴더 안의 영상 (슬라이드 PDF 를 같이 넣으면 슬라이드 감지가 더 정확해집니다)
source_language: ko
target_languages: [en]
glossary: {{}}
mask: auto
av_offset_ms: auto            # 립싱크(입모양-목소리) 자동 보정 | 0 = 끄기 | 숫자 = 직접(ms, + 소리 앞당김 / - 소리 늦춤)
quiz: {{ count: 3 }}
slides: {{ sensitivity: normal }}            # low | normal | high — 슬라이드 전환 감지 민감도
chapters: {{ min_sec: 45, max_count: 8 }}    # 챕터 최소 길이(초)·최대 개수
trim:                                       # 군더더기 컷 '제안' 기준 (자동 확정하지 않음 — 승인한 것만 적용)
  min_pause: 2.5              # 이 이상 쉬면 '긴 무음' 제안 (질문 뒤 생각할 시간은 보존 권장으로 표시)
  keep_pause: 0.8             # 컷을 적용해도 남겨 둘 쉼(초)
consent:
  lecturer_agreed: false
  external_ai_text: false
asr: {{ backend: sherpa-whisper, model: medium }}
llm: {{ backend: file }}
"""


class JobError(Exception):
    pass


@dataclass
class Job:
    id: str
    dir: Path
    data: dict
    cfg: dict = field(default_factory=dict)

    @property
    def input(self) -> Path:
        return self.dir / "input"

    @property
    def work(self) -> Path:
        return self.dir / "work"

    @property
    def out(self) -> Path:
        return self.dir / "out"

    @property
    def video(self) -> Path:
        return self.input / self.data.get("video", "input.mp4")

    @property
    def kind(self) -> str:
        return self.data.get("kind", "special")

    @property
    def kind_label(self) -> str:
        return KINDS.get(self.kind, self.kind)

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    @property
    def lecturer(self) -> dict:
        return self.data.get("lecturer") or {}

    @property
    def glossary(self) -> dict:
        return self.data.get("glossary") or {}


def create(job_id: str, profile: str = "default") -> Path:
    d = JOBS / job_id
    if d.exists():
        raise JobError(f"이미 있는 작업입니다: {d}")
    for sub in ("input", "work", "out"):
        (d / sub).mkdir(parents=True)
    tpl = FLIP_TEMPLATE if profile == "flip" else JOB_TEMPLATE
    (d / "job.yaml").write_text(tpl.format(id=job_id), encoding="utf-8")
    return d


def load(job_id: str, *, need_consent: bool = True) -> Job:
    d = JOBS / job_id
    path = d / "job.yaml"
    if not path.exists():
        raise JobError(f"작업서가 없습니다: {path}  →  먼저 'ls_cli.py new {job_id}'")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    job = Job(job_id, d, data)
    validate(job, need_consent=need_consent)
    return job


def validate(job: Job, *, need_consent: bool = True) -> None:
    d, problems = job.data, []
    if not d.get("title"):
        problems.append("title (강의 제목)")
    if not (job.lecturer.get("name")):
        problems.append("lecturer.name (교수·연사 이름)")
    if d.get("kind", "special") not in KINDS:
        problems.append(f"kind 는 {', '.join(KINDS)} 중 하나")
    if not job.video.exists():
        problems.append(f"영상 파일 없음: {job.video}")
    if d.get("source_language", "ko") not in ("ko", "en"):
        problems.append("source_language 는 ko 또는 en")
    if need_consent:
        c = d.get("consent") or {}
        if c.get("lecturer_agreed") is not True:
            problems.append("consent.lecturer_agreed (교수님 동의)")
        if c.get("external_ai_text") is not True and (d.get("llm") or {}).get("backend") == "anthropic":
            problems.append("consent.external_ai_text (글을 외부 AI 서비스에 보내는 것에 대한 동의)")
    if problems:
        raise JobError("작업서를 먼저 채워 주세요:\n  · " + "\n  · ".join(problems))
