"""글(텍스트)만 다루는 AI 연결부.  영상·음성은 절대 여기로 오지 않는다.

백엔드(job.yaml 의 llm.backend)
  anthropic  Claude API 로 '글'을 보내 결과를 받는다.  환경변수 ANTHROPIC_API_KEY 필요 (키는 코드·작업서에 쓰지 않는다).
             모델은 LS_MODEL 환경변수로 바꿀 수 있다.  외부 전송 동의(consent.external_ai_text)가 있어야 한다.
  file       input/llm_<작업>.json 에 미리 써 둔 결과를 그대로 쓴다 (API 키가 없을 때·시연·검수 후 재사용).
  none       AI 를 쓰지 않는다. 자막 = 받아쓴 글 그대로(번역 없음), 요약·퀴즈 없음. 아무것도 외부로 보내지 않는다.
             처음 실행하면 work/llm_request_<작업>.json 에 'AI 에게 보낼 요청'을 만들어 준다.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from .job import Job
from .util import StageError, read_json, write_json

API = "https://api.anthropic.com/v1/messages"

PROMPTS = {
    "text": """당신은 대학 강의 자막 편집자입니다. 아래는 강의 받아쓰기(음성인식) 결과입니다. 오인식이 있을 수 있습니다.
각 구간(id)마다 다음을 합니다.
1) 문맥과 용어사전을 이용해 한국어 문장을 바로잡습니다 (말투·뜻은 유지, 군더더기 'ㅇ어', 반복만 정리, 내용을 새로 만들지 않기).
2) 한 구간을 자막 한 장면 길이(한국어 약 12~30자)의 의미 단위 parts 로 나누고, 각 part 에 영어 번역(en)을 붙입니다.
   영어는 자연스럽고 격식 있는 강연체, 한 줄 42자 안팎, 용어사전의 영어 표기를 반드시 사용, 기관·직함은 공식 영문명 사용.
출력은 JSON 하나만: {"segments":[{"id":0,"parts":[{"ko":"…","en":"…"}]}]}""",
    "study": """당신은 대학 교수설계 전문가입니다. 아래 강의 전체 대본(시간 포함)을 바탕으로 학습 자료를 만듭니다. 대본에 없는 내용은 쓰지 않습니다.
출력은 JSON 하나만:
{"learning_goals":["…"], "summary_ko":"…", "summary_en":"…",
 "keywords":[{"ko":"…","en":"…"}],
 "chapters":[{"start":초,"title_ko":"…","title_en":"…","summary_ko":"…"}],
 "quiz":[{"type":"mcq|ox|short","question_ko":"…","question_en":"…","choices_ko":[…],"choices_en":[…],"answer":"…(mcq 는 보기 번호 1~4, ox 는 O/X, short 는 모범답안)","explanation_ko":"…","explanation_en":"…","bloom":"기억|이해|적용|분석|평가|창안","evidence_start":초}]}
퀴즈는 요청한 개수만, 서로 다른 유형·수준으로 섞고 정답이 대본에서 근거를 찾을 수 있어야 합니다.""",
}


def complete_json(job: Job, task: str, payload: dict, log=print) -> dict:
    backend = (job.get("llm") or {}).get("backend", "file")
    if backend == "file":
        return _file(job, task, payload, log)
    if backend == "anthropic":
        return _anthropic(job, task, payload, log)
    if backend == "none":
        return _none(task, payload, log)
    raise StageError(f"알 수 없는 AI 연결 방식: {backend}")


def _none(task: str, payload: dict, log) -> dict:
    log("      AI 미사용 — 받아쓴 글 그대로 (검수 화면에서 고칠 수 있음)")
    if task == "text":
        return {"segments": [{"id": s["id"], "parts": [{"ko": s["text"], "en": ""}]} for s in payload.get("segments", [])]}
    return {"learning_goals": [], "summary_ko": "", "summary_en": "", "keywords": [], "chapters": [], "quiz": [], "_none": True}


def _file(job: Job, task: str, payload: dict, log) -> dict:
    src = job.input / f"llm_{task}.json"
    req = job.work / f"llm_request_{task}.json"
    write_json(req, {"prompt": PROMPTS[task], "payload": payload})
    data = read_json(src)
    if data is None:
        raise StageError(
            f"직접 작성한 결과 파일이 없습니다: {src}\n  AI 에게 보낼 요청을 {req} 에 만들어 두었습니다.\n"
            f"  → 이 요청의 결과(JSON)를 위 경로에 저장하거나, job.yaml 의 llm.backend 를 anthropic 으로 바꾸세요.")
    log(f"      AI 결과: 파일 {src.name} 사용 (외부 전송 없음)")
    return data


def _anthropic(job: Job, task: str, payload: dict, log) -> dict:
    if (job.get("consent") or {}).get("external_ai_text") is not True:
        raise StageError("글을 외부 AI 서비스에 보내는 동의(consent.external_ai_text)가 없습니다")
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise StageError("ANTHROPIC_API_KEY 환경변수가 없습니다 (키는 코드·작업서에 쓰지 말고 환경변수로만 넣으세요)")
    model = os.environ.get("LS_MODEL", "claude-sonnet-5-5")
    body = {"model": model, "max_tokens": 16000,
            "messages": [{"role": "user", "content": PROMPTS[task] + "\n\n" + json.dumps(payload, ensure_ascii=False)}]}
    r = urllib.request.Request(API, data=json.dumps(body).encode("utf-8"), method="POST", headers={
        "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=300) as resp:
            out = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise StageError(f"AI 서비스 오류 {e.code}: {e.read().decode('utf-8', 'replace')[:300]}") from e
    except urllib.error.URLError as e:
        raise StageError(f"AI 서비스에 연결하지 못했습니다: {e.reason}") from e
    text = "".join(b.get("text", "") for b in out.get("content", []))
    s, e = text.find("{"), text.rfind("}")
    if s < 0 or e < 0:
        raise StageError("AI 답변에서 JSON 을 찾지 못했습니다")
    log(f"      AI 결과: Claude({model}) — 글만 전송")
    return json.loads(text[s:e + 1])
