# 강의 후반작업 AI 자동화 엔진 (HY FLIP · M4)

촬영한 강의 영상 1편 = 작업 1건. 영상을 넣으면 **자막(한/영) · 요약 · 퀴즈 · 강의 스크립트 · 자막 스크립트 · 인쇄용 PDF** 가 나옵니다.
`profile: flip` 작업은 여기에 **슬라이드 전환 감지 · 챕터 · 군더더기 컷 제안 · 교수 검수 화면**이 더해집니다 (플립러닝 사전학습 영상용).

## 설치 (처음 한 번)
```
python -m venv .venv && .venv/bin/pip install sherpa-onnx numpy pyyaml python-docx pillow   # Windows: .venv\Scripts\pip
python engine/setup_models.py          # 받아쓰기 모델 (medium, 약 940MB) — 저사양 PC 는: setup_models.py small
```
그 밖에 필요: ffmpeg(libass 포함), 크롬 또는 엣지(PDF). 영상·음성은 컴퓨터 밖으로 나가지 않습니다.

## 쓰는 법
```
python engine/ls_cli.py new my-lecture --profile flip   # jobs/my-lecture/ 만들기 (flip = 플립러닝)
#  → input/ 에 영상 넣고 job.yaml 채우기 (제목·교수·동의 항목)
python engine/ls_cli.py run my-lecture                  # 끝까지 실행 (바뀐 단계만 다시)
python engine/ls_cli.py review my-lecture               # 교수 검수 화면 → http://127.0.0.1:8765
python engine/ls_cli.py run my-lecture                  # 검수·승인 내용을 반영해 산출물 다시 만들기
python engine/ls_cli.py status my-lecture               # 단계별 상태
```

## 단계
기본: ① 접수·점검 → ② 영상 정리(1080p·30fps·-16 LUFS·녹화 위젯 가림) → ③ 받아쓰기(로컬) → ④ 자막(한/영) → ⑤ 요약·퀴즈 → ⑥ 산출물 → ⑦ 인쇄 PDF

flip: ①②③ → **⑧ 슬라이드 전환** → ④⑤ → **⑨ 챕터** → **⑩ 군더더기 컷 제안** → **⑪ 승인 컷 적용** → ⑥⑦

| 단계 | 하는 일 | 자동화 |
|---|---|---|
| ⑧ 슬라이드 전환 (`s8_slides.py`) | 화면 변화로 슬라이드 경계를 찾음. 교수 카메라 창·녹화 시계처럼 늘 움직이는 영역은 스스로 찾아 제외. 새 슬라이드 / 슬라이드 안 변화(글머리) / 연속 변화(시연·스크롤) 구분. 슬라이드별 썸네일 | 자동 |
| ⑨ 챕터 (`s9_chapters.py`) | AI 챕터를 슬라이드 경계(±8초)·문장 시작(±5초)에 맞추고, 도입/개념/사례/시연/정리로 구분. AI 결과가 없으면 슬라이드 구간으로 | 제안 → 검수 |
| ⑩ 군더더기 컷 제안 (`s10_trim.py`) | 긴 무음·앞뒤 여백·NG/혼잣말·다시 말하기·군말을 **목록으로만** 제안. 질문 뒤 침묵·슬라이드 넘김·시연 중 침묵은 '보존 권장' | 제안만 |
| ⑪ 승인 컷 적용 (`s11_edit.py`) | 검수 화면에서 **승인한 컷만** 잘라냄. 자막·챕터·퀴즈 근거 시각은 자동으로 앞당김 | 승인한 것만 |
| 교수 검수 화면 (`review.py`) | 자막·요약퀴즈·챕터·컷을 영상과 함께 보고 고친 뒤 '승인'. `work/review_*.json` 에 저장 | 사람 |

## 산출물 (`out/`)
자막(`자막/*.srt·vtt`, `자막/챕터.vtt`) · 영상 4종(한글자막·영어자막·자막없음·자막선택형) · 문서(`문서/*.docx·html·txt`, 학습지) · 인쇄용 PDF ·
`챕터_타임스탬프.txt`(LMS·유튜브 설명란용) · `검수상태.txt`(승인 전에는 '검토 대기') · `실행로그.txt`(단계별 소요 시간·요약)

## AI(글만) 연결
`llm.backend: anthropic` + 환경변수 `ANTHROPIC_API_KEY` (키는 코드에 쓰지 않음, 교수 동의 `consent.*` 필수) /
`llm.backend: file` = `input/llm_text.json`, `input/llm_study.json` 에 직접 쓴 결과 사용.
AI 결과는 항상 '검토 대기' — 교수 검수 화면에서 승인해야 '승인'으로 바뀝니다.

## 지키는 원칙
- 영상·음성은 PC 밖으로 보내지 않음 (외부 호출은 `llm.py` 의 글 전송뿐, 동의 필수). 검수 화면도 127.0.0.1 에서만 열림
- 군더더기 컷은 자동 확정하지 않음. 숏폼식 효과(펀치 줌·whoosh·상시 BGM·단어 하이라이트) 없음
- 공통 코어(`job.py util.py llm.py pipeline.py s1~s3`)는 시그니처를 바꾸지 않고 추가만 (숏폼 프로필과 공유)

## 시험
```
python engine/tests/test_flip.py        # 또는 python -m pytest engine/tests
```

## 처리 속도 (참고 · 클라우드 4코어 CPU, GPU 없음)
1분54초 영상: 받아쓰기(medium) 215초 · 영상 정리 16초 · 산출물 29초 · PDF 5초 → 전체 약 4분.
받아쓰기가 영상 길이의 약 1.9배 → 12분 강의는 약 23분.

| 받아쓰기 모델 | 1분54초 처리 | 영상 길이 대비 | 정확도 (같은 샘플) |
|---|---|---|---|
| medium (기본) | 215초 | 약 1.9배 | 오인식 적음 ('조력자' 등 정확) |
| small (`setup_models.py small`, `asr.model: small`) | 55초 | 약 0.5배 | 오인식 많음 ('교육 석신처'·'조륙자'·없는 '감사합니다' 끼어듦) → 검수 부담 큼 |
