# 강의 후반작업 AI 자동화 엔진 (HY FLIP · M4)

촬영한 강의 영상 1편 = 작업 1건. 영상을 넣으면 **자막(한/영) · 요약 · 퀴즈 · 강의 스크립트 · 자막 스크립트 · 인쇄용 PDF** 가 나옵니다.

## 쓰는 법
```
python -m venv .venv && .venv/bin/pip install sherpa-onnx numpy pyyaml python-docx pillow   # 처음 한 번 (Windows: .venv\Scripts\pip)
python engine/ls_cli.py new my-lecture          # jobs/my-lecture/ 만들기
#  → input/ 에 영상 넣고 job.yaml 채우기 (제목·교수·동의 항목)
python engine/ls_cli.py run my-lecture          # 끝까지 실행 (바뀐 단계만 다시)
python engine/ls_cli.py run my-lecture --from text   # 자막 검수 후 이 단계부터 다시
```
필요: ffmpeg(libass), 크롬/엣지(PDF), 받아쓰기 모델 → `models/whisper-medium/`, `models/silero_vad.onnx`
(sherpa-onnx 의 whisper-medium int8 + silero_vad, GitHub 릴리스에서 내려받기. 영상·음성은 컴퓨터 밖으로 나가지 않음).

## 단계
① 접수·점검 → ② 영상 정리(1080p·30fps·-16 LUFS·녹화 위젯 가림) → ③ 받아쓰기(로컬) → ④ 자막(한/영) → ⑤ 요약·퀴즈 → ⑥ 산출물 → ⑦ 인쇄 PDF

## AI(글만) 연결
`llm.backend: anthropic` + 환경변수 `ANTHROPIC_API_KEY` (키는 코드에 쓰지 않음, 교수 동의 `consent.*` 필수) /
`llm.backend: file` = `input/llm_text.json`, `input/llm_study.json` 에 직접 쓴 결과 사용 (샘플은 이 방식).
AI 결과는 항상 '검토 대기' — 교수·PD 검수 후 확정.
