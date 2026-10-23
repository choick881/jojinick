# 03. 홈페이지 메타 프롬프트

> **쉬운 설명** — 상세페이지가 "한 장짜리 안내서"라면, 홈페이지는 "사업단 건물의 로비"예요.
> 처음 온 교수님이 **어디로 가면 무엇이 있는지** 한눈에 보이고, 공지·신청 같은 자주 쓰는 문이 가까이 있어야 합니다.

---

> ✅ **확정 톤 (2차 문답)**: 상세페이지와 같은 **A+C 리믹스** — 밝은 아카데믹 본문 + 히어로·숫자·CTA 는 시네마틱 다크 밴드.
> 로고: 헤더 A 모노그램 · 푸터 D 인장 · SNS E 타일.

## Claude Design 용 프롬프트 (복사용)

```
(00_design-system 규칙, 선택된 HY FLIP 로고, 상세페이지에서 확정한 비주얼 방향을 따릅니다)

[목표] HY FLIP 사업단 홈페이지 메인 화면. 교수님이 1) 사업을 이해하고 2) 제작을 신청하고 3) 공지를 확인하게 하는 것.
[대상] 대학 교수님(주 사용자), 교내 관계자(보조).
[형식] 데스크톱 1440px + 모바일 390px. 상단 고정 메뉴, 모바일은 햄버거 메뉴.

[메뉴] 사업소개 · 제작절차 · 스튜디오 · 제작사례 · 공지사항 · 제작신청(골드 버튼)
[메인 화면 구성]
1. 헤더 — 왼쪽 HY FLIP 로고, 오른쪽 "UNIVERSITY EMBLEM" 자리표시 + 메뉴
2. 히어로 — 큰 헤드라인 "수업을 뒤집으면, 배움이 깊어집니다", 실사 스튜디오 이미지, [제작 신청] [사업 안내]
3. 빠른 바로가기 4칸 — 제작 신청 / 스튜디오 예약 / 제작 가이드 PDF / 자주 묻는 질문
4. 사업 소개 요약 — 3개 가치: "전문 제작", "교수설계 컨설팅", "AI 후반작업"
5. 숫자로 보는 HY FLIP — 4개 수치 (※ 예시)
6. 최신 제작 강의 — 썸네일 카드 4개 (과목명, 교수명 자리, 재생 아이콘)
7. 공지사항 + 일정 — 왼쪽 공지 목록 5개, 오른쪽 이번 학기 신청 일정 타임라인
8. 푸터 — 사업단 주소·연락처 자리표시, 교표 자리표시, 저작권 문구
[제약] 실제 대학 교표·실제 연락처 사용 금지(자리표시), 수치 ※ 예시.
```

### 3시안 요청 (같은 톤, 구성만 다르게)
```
A+C 리믹스 톤으로 구성이 다른 3시안을 만들어 주세요.
1 영상 히어로형   — 첫 화면 전체 다크 히어로 + 겹쳐 올라오는 바로가기 4칸
2 공지·포털형     — 왼쪽 헤드라인 | 오른쪽 공지 5개 + 일정 카드, 아래 다크 강의 레일
3 바로가기 허브형 — 첫 화면이 벤토 타일(다크 히어로 타일 + 신청·예약·가이드·FAQ·수치·다음 일정)
```

---

## GPT 이미지(gpt-image-2) 프롬프트 — 홈페이지 추가 사진

| 파일명 | 프롬프트 |
|---|---|
| `campus-dusk.png` (21:9) | Photorealistic wide photograph of a modern Korean university campus at blue hour, glass-and-stone academic building with warm lit windows, a few students walking, deep navy sky. No signage, no logos, no readable text. |
| `thumb-1..4.png` (16:9) | Photorealistic still frame from a university lecture video: a professor (vary: woman in her 50s / man in his 40s / woman in her 30s / man in his 60s) explaining in front of a clean navy studio backdrop with a subtle on-screen diagram. Broadcast-quality lighting. No readable text, no logos. |

---

## 🔑 핵심 키워드
**홈 = 로비 · 메뉴 6개 + 골드 신청 버튼 · 바로가기 4칸 · 공지+일정 · 상세페이지와 같은 방향으로 세트 맞춤**
