# 01. 로고 메타 프롬프트 — HY FLIP 모노그램

> **쉬운 설명** — 로고는 두 단계로 나눠 만들어요.
> 1) **모양(벡터)**: H와 F를 엮은 글자 모양은 컴퓨터 도형(SVG)으로 정확하게 그립니다. AI 이미지 모델은 글자를 자주 틀리게 그리거든요.
> 2) **실사 목업**: 완성된 로고가 "실제 세상에 걸려 있는 모습"(황동 명판, 스튜디오 벽, 명함)은 GPT 이미지 모델로 사진처럼 만듭니다.
> 이렇게 하면 로고는 정확하고, 보여주는 이미지는 고급스러워져요.

---

## A. Claude Design 용 로고 프롬프트 (복사용)

```
(00_design-system 규칙을 따릅니다)

[목표] HY FLIP 의 모노그램 로고 3가지 시안을 한 보드(artboard)에 나란히 보여주세요.
[모노그램 규칙] 대문자 H 와 F 를 하나로 엮은 이니셜 로고. H 의 오른쪽 기둥 = F 의 기둥(공유).
  - 시안 A "Page Flip": F 의 위쪽 가로획 끝이 책장 넘기듯 접힌 모서리(골드 삼각형)
  - 시안 B "Academic Seal": 원형 인장. 바깥 링에 "HY FLIP · FLIPPED LEARNING CONTENT LAB" 원형 문구, 가운데 슬랩세리프 HF
  - 시안 C "Play Flip": H 의 가로획 자리에 골드 ▶ 재생 삼각형 (영상 콘텐츠 상징)
[각 시안마다 보여줄 것]
  1) 기본형(흰 바탕) 2) 반전형(남색 바탕) 3) 단색형(검정) 4) 16·32·64px 축소 테스트
  5) 가로 조합형: 심볼 + "HY FLIP" + 부제 "Flipped Learning Content Lab"
[대상] 처음 보는 교수님이 3초 안에 "대학 교육 · 영상 · 뒤집기"를 떠올려야 함
[제약] 선 굵기 일정, 골드는 한 군데만, 그라디언트·그림자 금지, 실제 대학 교표 모방 금지
```

> 💡 **팁**: 첫 결과가 나오면 "시안 A 의 접힌 모서리를 더 작게", "B 의 원형 문구 자간 넓게"처럼 **한 부분씩** 고쳐 달라고 하세요.
> 마음에 드는 두 시안의 장점을 섞어 달라고 하는 것(remix)도 좋아요.

---

## B. GPT 이미지(gpt-image-2) 프롬프트 — 로고 실사 목업

> 공식 가이드 순서: **배경 → 주제 → 세부 → 제약**. 실사는 "photorealistic" 을 꼭 넣어요.
> 로고 모양은 우리가 만든 SVG 를 **참고 이미지로 함께 넣어(image edit)** 정확도를 높입니다.

### B-1. 황동 명판 (스튜디오 입구)
```
Photorealistic product photograph for a brand presentation slide.
Background: a modern university media studio corridor, warm grey plaster wall, soft daylight from the left.
Subject: a brushed brass name plate mounted on the wall with the attached monogram logo engraved and filled with deep navy (#0E4A84) enamel,
below it engraved text "HY FLIP" and smaller "FLIPPED LEARNING CONTENT LAB".
Details: crisp engraving edges, subtle reflections, four small brass screws, shallow depth of field, 50mm lens.
Constraints: keep the monogram shape exactly as the reference, no extra text, no university crest, no watermark. Aspect 3:2.
```

### B-2. 스튜디오 벽면 사인 (백릿 입체 사인)
```
Photorealistic interior photograph.
Background: a professional lecture-video recording studio with a teleprompter, softbox lights and a glass lightboard, dark navy acoustic panels.
Subject: a large backlit dimensional sign of the attached monogram logo in matte white with a gold accent, mounted on the navy wall.
Details: soft halo glow behind the letters, cinematic but natural lighting, eye-level view, 35mm lens.
Constraints: logo shape identical to reference, no people, no other logos, no text except "HY FLIP". Aspect 16:9.
```

### B-3. 명함·문구류 세트
```
Photorealistic flat-lay stationery mockup.
Background: ivory textured paper surface (#F7F5F0), soft top-down daylight with gentle shadows.
Subject: business cards, an A4 letterhead and a navy folder printed with the attached HY FLIP monogram; gold foil on the monogram accent only.
Details: premium cotton paper texture, slight emboss, a fountain pen at the edge.
Constraints: monogram identical to reference, no fake Korean text (use simple grey lines for body text), no watermark. Aspect 4:3.
```

---

## 🔑 핵심 키워드
**H 기둥 = F 기둥 공유 · A 책장 접힘 / B 아카데믹 인장 / C 재생 버튼 · 로고는 SVG, 목업은 GPT · 한 번에 한 부분씩 수정**
