# 온담찬 메타프롬프트 v1

로고·이미지·페이지를 만들 때 **이 파일이 유일한 기준**이다. 바꾸고 싶은 것이 생기면 이 파일을 먼저 고치고, 그다음 다시 생성한다.
근거: 사업계획서(양주시 1인 무인 반찬가게, 2026.08.21) + 문답 R1~R8 (2026-10-21).

---

## 1. 브랜드 바이블

### 정체성
- **이름**: 온담찬 — 온(溫, 온기) + 담(담다) + 찬(반찬). "온기를 담은 반찬"
- **한 줄 정의**: 양주 동네에서 아침마다 직접 만든 1~2인분 집밥 반찬을, 퇴근길에 미리 결제하고 찾아가는 무인 반찬가게
- **슬로건 (사용자 작성)**
  > 따뜻한 한 끼를 생각합니다
  > 매일의 식사에 온기를 담다.
  > 나를 위한 한 끼도, 부모님께 전하는 한 끼도.
  > 익숙한 집밥으로 마음을 전합니다.
- **대표 헤드라인**: 매일의 식사에 온기를 담다
- **두 손님** (첫 화면에 나란히)
  1. 나를 위한 한 끼 — 퇴근길 1~2인 가구·맞벌이. 불편: "퇴근 후 요리할 힘이 없다"
  2. 부모님께 전하는 한 끼 — 따로 사는 부모님을 챙기는 자녀. 불편: "부모님 식사가 걱정된다"
- **어르신 코너**: 「어르신 밥상」 — 부드러운 반찬 3종 세트, 어르신 1인 저녁세트

### 성격
| 이렇게 | 이렇게는 아니게 |
|---|---|
| 따뜻한, 정직한, 부지런한 | 프랜차이즈 같은, 공장식 |
| 동네 이웃 같은 | 유치한, 만화 캐릭터 |
| 정갈한 | 너무 고급스러워 비싸 보이는 |
| 지금의 집밥 | 올드한, 촌스러운 전통 |

### 컬러 토큰 (WCAG 검증값)
| 토큰 | HEX | 용도 | 대비(크림 바탕) |
|---|---|---|---|
| `--paper` | #FBF6EC | 기본 배경(크림) | — |
| `--sand` | #EFE4D0 | 섹션 배경, 카드 | — |
| `--ink` | #2B211A | 본문 글씨 | 14.6 |
| `--brand` | #7A4E2D | 된장 갈색 — 제목, 로고, 보조 버튼 | 6.6 |
| `--muted` | #6B5A4C | 보조 글씨 | 6.1 |
| `--accent` | #C8462B | 고추 주홍 — **장식·큰 숫자·아이콘만** | 4.46 (본문 글씨 금지) |
| `--accent-deep` | #A93A22 | 주홍 버튼 바탕(흰 글씨 6.3)·주홍 글씨 | 6.0+ |

규칙: 주홍은 한 화면에 한 가지 행동(결제·예약 버튼)에만. 나머지는 갈색과 크림으로.

### 타이포그래피
- 본문: **Pretendard** 400/500, **18px**, 줄간격 1.7, `word-break: keep-all`
- 제목: **Noto Serif KR** 700~900 (따뜻한 명조) — 한 페이지 두 종 이상 섞지 않음
- 숫자(가격·시간): Pretendard 700, 탭 숫자
- '큰 글씨 보기' 버튼: 본문 22px, 버튼 높이 56px 이상

### 카피 원칙
- 존댓말, 짧은 문장(한 문장 25자 안팎), 숫자는 구체적으로 ("아침 7시에 만든", "1인분 180g")
- 동사로 끝나는 버튼: "미리 결제하기", "픽업 시간 고르기"
- **쓰지 않는 표현**: 고령친화식품, KS 인증, 저염/나트륨 줄인(근거 전), 혈압·당뇨·치매 등 효능, 무첨가 100%, 최고·최초
- 대신: "부드러운 반찬", "간을 약하게 했어요(레시피 기준 공개)", "오늘 아침 만든"
- 요리사 소개는 프로필이 올라오기 전까지 "만드는 사람 — 곧 소개해 드릴게요" 자리만 둔다.

---

## 2. GPT 이미지 프롬프트 템플릿 (`gpt-image-2`)

공통 제약(모든 프롬프트 끝에 붙임):
```
Photorealistic. Korean home-style food in a Korean setting (not Japanese, not Western).
No people, no hands unless specified, no text, no logos, no watermark, no price tags.
Warm but natural color, true-to-life portions for 1–2 people.
```

### 2-1. 나무 식탁 위 집밥상 (히어로, 1536x1024)
```
[Purpose] Hero photo for a Korean neighborhood side-dish shop website, landscape.
[Background] Warm oak dining table by a window at early evening, soft 3000K light from the left, cream linen napkin.
[Subject] A one-person Korean dinner set: a bowl of steaming white rice, doenjang-jjigae in a small earthenware ttukbaegi with gentle steam, and four small side dishes in simple ceramic bowls (spinach namul, soy-braised beef jangjorim, stir-fried anchovies, cabbage kimchi).
[Details] 45-degree angle, 50mm lens, f/2.8, shallow depth of field, natural textures, honest home cooking, nothing glossy or staged-looking.
[Constraints] (공통 제약)
```

### 2-2. 정갈한 용기 상품컷 (상품 카드 1024x1024 / 상세 1024x1536)
```
[Purpose] Product photo for an online menu card.
[Background] Plain warm cream backdrop (#FBF6EC tone), soft diffused daylight, subtle shadow.
[Subject] One small clear rectangular take-out container (about 180g) filled with {반찬 이름, 영문 묘사}, lid placed beside it, a blank kraft sticker label on the lid area (no text on it).
[Details] Top-down or 30-degree view, crisp focus on the food texture, colors true to life.
[Constraints] (공통 제약)
```

### 2-3. 따뜻한 가게 내부 (사업소개, 1536x1024)
```
[Purpose] Interior photo for the "about us" page of a small unmanned Korean side-dish shop.
[Background] A clean 10–15 pyeong shop at evening, warm wood shelves, cream walls.
[Subject] A glass refrigerated showcase neatly filled with small labeled containers of Korean banchan, a self-checkout kiosk at the side, a small pickup shelf with numbered cubbies.
[Details] Eye level, 28mm lens, warm 3000K lighting inside, calm and tidy, inviting.
[Constraints] (공통 제약) No readable signage text.
```

### 2-4. 어르신 밥상 (1024x1024)
```
[Purpose] Product photo for a "soft meal for seniors" menu.
[Background] Oak table, soft daylight, cream cloth.
[Subject] A small dinner tray: mild clear radish soup, soft braised tofu, finely shredded tender beef jangjorim, well-cooked soft namul, small portion of rice — all visibly soft and easy to chew.
[Details] 45-degree angle, gentle and calm mood, smaller portions than a regular set.
[Constraints] (공통 제약)
```

### 2-5. 로고 (1024x1024, 시안 단계 `--quality medium`)
```
Logo design for a Korean neighborhood side-dish shop named "온담찬".
Type: {A: symbol + wordmark | B: symbol + wordmark | C: round sticker emblem}.
Symbol idea: {A: a rice bowl with three soft rising lines of steam | B: two hands gently offering a bowl | C: a bowl with steam inside a circle, held by two hands}, simplified into flat shapes.
Style: warm, honest, neighborly, modern Korean home cooking. Not franchise-like, not childish, not luxurious, not old-fashioned.
Colors: deep doenjang brown #7A4E2D with one small chili-orange accent #C8462B, on plain cream #FBF6EC.
Render the Korean text "온담찬" exactly, no other text, no slogan.
Must stay readable at 32px and printable in one color on a small container sticker. Flat vector look, no gradients, no 3D, no mockup.
```

---

## 3. 페이지 빌드 프롬프트

공통: 모바일(375px) 먼저, 본문 18px, 크림 바탕, 사진은 2절의 GPT 이미지만 사용(없으면 "이미지 생성 대기" 자리), 모든 사진 아래 작은 글씨로 "연출된 이미지입니다".

### 홈 `/`
1. **히어로** — 헤드라인 "매일의 식사에 온기를 담다" + 두 갈래 카드
   - "나를 위한 한 끼" → 오늘의 저녁세트, [미리 결제하기]
   - "부모님께 전하는 한 끼" → 어르신 밥상, [부모님 반찬 보내기]
2. **공감** — "퇴근하고 요리할 힘, 남아 있나요?" / "부모님 식사, 매일 챙기기 어렵죠?"
3. **오늘의 반찬** — 메뉴 카드 6개(품절·소진임박 표시), [전체 메뉴]
4. **이용 방법 3단계** — ① 미리 결제하고 픽업 시간 고르기 ② 매장 픽업 선반에서 주문번호 확인 ③ 집에서 데우기만
5. **약속** — 매일 아침 제조, 모든 용기에 제조시간 라벨, 1~2인분 소포장
6. **어르신 밥상 소개** — 부드러움 단계, 큰 글씨, 대리주문
7. **매장 안내** — 카카오맵, 영업시간(06:00~23:00, 무인 판매), 픽업 시간 17:30~20:30
8. **푸터** — 상호·대표자·사업자등록번호·통신판매업 신고번호(준비 중)·주소·연락처, 이용약관·환불정책

### 사업소개 `/about`
가게 이야기 → 운영 원칙(판매시간만 무인, 당일 제조, 소포장, 폐기 줄이기) → 위생·신선도(쇼케이스 온도 관리, 제조시간 라벨) → "만드는 사람"(프로필 자리) → 가게 내부 사진

### 메뉴 `/menu`
카테고리 탭: 저녁세트 · 기본찬 · 메인찬 · 국·찌개 · 어르신 밥상. 카드 = 사진, 이름, 용량, 가격, 품절/소진임박 배지, [담기]

### 상세 `/menu/[slug]` (대표: 1인 저녁세트) — `references/detail-page.md` 구조
구매 영역(픽업 날짜·시간 30분 단위, 수량) → 후킹("퇴근길, 오늘 저녁이 준비되어 있어요") → 구성 → **제조시간 라벨 예시 크게** → 데우는 법 → 정보 고시 → 픽업 안내 → FAQ 4개(무인 매장 픽업 방법 / 보관 기간 / 픽업 시간을 놓치면 / 데우는 법) → 하단 고정 구매 바

### 어르신 밥상 `/silver`
큰 글씨 기본, 부드러움 3단계(가게 자체 기준: 씹기 쉬움 / 잇몸으로 / 혀로), 상품 2종, "자녀가 대신 주문하기" 안내, [전화로 주문] 버튼

### 결제 `/checkout`
주문 요약 → 픽업 날짜·시간 → 주문자(이름·전화) → "받는 분이 다른가요?"(부모님 성함·연락처) → [배송 옵션: 스위치 OFF 동안 숨김] → 토스 결제위젯 → 약관 동의 → [○○원 결제하기]
