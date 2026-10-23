# 02. 사업 상세페이지 메타 프롬프트

> **쉬운 설명** — 상세페이지는 "교수님께 드리는 한 장짜리 안내서"를 웹으로 길게 펼친 거예요.
> 교수님이 위에서 아래로 내려가며 **① 이게 뭐지? → ② 나한테 뭐가 좋지? → ③ 어떻게 하지? → ④ 믿을 만한가? → ⑤ 신청!**
> 순서로 마음이 움직이도록 섹션을 배치합니다.

---

## Claude Design 용 프롬프트 (복사용) — 먼저 뼈대(와이어프레임)

```
(00_design-system 규칙과 선택된 HY FLIP 로고를 따릅니다)

[목표] 'HY FLIP 플립러닝 콘텐츠 개발 사업' 상세페이지. 교수님이 읽고 "제작 신청" 버튼을 누르게 하는 것.
[대상] 강의 영상 제작이 처음이거나 부담스러운 대학 교수님. 바쁘기 때문에 훑어봐도 이해되어야 함.
[형식] 세로로 긴 1페이지, 데스크톱 1440px + 모바일 390px 두 버전. 먼저 회색 와이어프레임으로.

[섹션 순서와 내용]
1. 히어로 — 헤드라인 "강의실 밖에서 시작되는 수업", 서브 "교수님은 강의만 하세요. 기획·촬영·편집·AI 자막까지 HY FLIP 이 함께합니다."
   버튼 [제작 신청하기] [안내서 내려받기], 오른쪽에 스튜디오 실사 이미지
2. 플립러닝이란 — 기존 수업 vs 플립러닝 2단 비교 (수업 전 영상 학습 → 수업 중 토론·실습)
3. 이런 교수님께 — 체크리스트 3개 ("영상 촬영이 처음", "토론 중심 수업으로 바꾸고 싶은", "기존 강의를 재활용하고 싶은")
4. 제작 절차 4단계 — 01 신청 → 02 기획(교수설계 컨설팅) → 03 촬영(전문 스튜디오) → 04 편집·검수, 단계별 소요기간과 교수님 준비물
5. 스튜디오·장비 — 크로마키, 라이트보드, 프롬프터, 4K 카메라, 전자칠판 / 사진 그리드
6. AI 활용 — AI 자막(한/영), AI 더빙, 강의 요약·퀴즈 자동 생성, 챕터 자동 분할 (아이콘 4개 카드)
7. 제작 사례 — 강의 썸네일 카드 3개 + 교수님 후기 인용 2개
8. 성과 수치 — 제작 강좌 120 · 참여 교수 45 · 학습자 만족도 4.7/5 · 누적 수강 18,000 (※ 예시 수치 표기)
9. FAQ — 촬영 시간, 비용, 저작권, 수정 횟수 (아코디언)
10. 신청 CTA — 남색 배경 + 골드 버튼, 담당자 연락처 자리
[제약] 실제 대학 교표 대신 "UNIVERSITY EMBLEM" 자리표시. 모든 수치 옆 "※ 예시".
```

### 2단계: 고해상도 3시안 요청 (뼈대 확정 후)

```
위 와이어프레임을 같은 내용·같은 섹션 순서로 3가지 비주얼 방향으로 만들어 주세요.
A "Classic Academic" — 흰/아이보리 바탕, 명조 대형 헤드라인, 남색 블록, 얇은 골드 밑줄, 대학 출판물 같은 정돈감
B "Modern Grid"      — 고딕 중심, 12칸 그리드 카드, 단계 번호를 크게, 정보 디자인처럼 명확하게
C "Cinematic Studio" — Deep Navy 다크 배경, 스튜디오 실사 사진 크게, 영화 크레딧 같은 타이포, 골드 하이라이트
```

---

## GPT 이미지(gpt-image-2) 프롬프트 — 상세페이지 사진

| 파일명 | 프롬프트 |
|---|---|
| `studio-hero.png` (16:9) | Photorealistic photograph of a modern university lecture-video studio. A middle-aged Korean professor in a navy blazer speaks naturally toward a camera with a teleprompter, softbox key light, dark navy acoustic wall, a glass lightboard on the side. Natural skin tones, shallow depth of field, 35mm, calm and trustworthy mood, desaturated navy-grey palette. No logos, no text, no watermark. |
| `flipped-class.png` (3:2) | Photorealistic photograph of a university seminar room during an active discussion class. Students in small groups around tables, a professor walking between them, laptops showing lecture video thumbnails, warm daylight from large windows. Candid moment, nobody looking at camera. No logos, no readable text. |
| `lightboard.png` (4:3) | Photorealistic photograph of a professor writing glowing equations on a transparent lightboard in a dark studio, the writing glows soft white and gold, rim light on the professor, black background. No readable brand text. |
| `chroma.png` (4:3) | Photorealistic photograph of a green chroma-key studio with a 4K cinema camera on a tripod, LED panel lights and a monitor showing a composited virtual classroom. Clean, professional, no people. |
| `editing.png` (4:3) | Photorealistic photograph of a video editor's desk with two monitors showing a lecture timeline and AI-generated subtitles, navy ambient light, late afternoon. Screen text unreadable / blurred. |

---

## 🔑 핵심 키워드
**이게 뭐지→좋은 점→방법→신뢰→신청 · 와이어프레임 먼저 · A 클래식 / B 그리드 / C 시네마틱 · 수치는 ※예시 · 사진은 photorealistic + 글자 금지**
