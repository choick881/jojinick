# 브랜드 자산 · GPT 이미지 생성 가이드 (Phase 1.5)

로고·히어로·상품 실사처럼 "그림"으로 표현할 것은 OpenAI GPT 이미지 모델로 만든다. 이 문서는 **메타프롬프트 → 레퍼런스 → 로고 3안 → 이미지 생산** 순서를 정의한다.

---

## 0. 준비

```bash
export OPENAI_API_KEY=...            # 클라우드 세션이면 환경 설정의 환경변수로 등록
node scripts/gen-image.mjs --help    # 스킬 폴더 기준 경로
```

- 클라우드 컨테이너는 Network access에 `api.openai.com`이 허용되어 있어야 한다.
- 키·네트워크가 없으면 **이미지 단계만 보류**하고 사용자에게 설정을 요청한다. 스톡 이미지 URL이나 다른 모델 결과로 몰래 대체하지 않는다.

---

## 1. 메타프롬프트 (`brand/meta-prompt.md`)

인터뷰 답변을 아래 3블록으로 정리한다. 이후 로고·이미지·페이지 생성은 모두 이 파일을 근거로 하며, 사용자가 바꾸고 싶으면 이 파일만 고친다.

```markdown
# 1. 브랜드 바이블
- 한 줄 정의: (누구에게 / 무엇을 / 어떻게 다르게)
- 성격 키워드 3개: (예: 정직한, 따뜻한, 부지런한)
- 금지 키워드: (예: 프랜차이즈 같은, 과장된, 차가운)
- 컬러 토큰: --brand / --brand-ink / --accent / --paper / --muted (HEX)
- 타이포: 본문 Pretendard / 제목 (한 종)
- 사진 톤: 조명·색온도·배경·소품 규칙
- 카피 톤: 존댓말 수준, 문장 길이, 쓰지 않을 표현

# 2. 이미지 프롬프트 템플릿 (아래 4. 참고)

# 3. 페이지 빌드 프롬프트
- 섹션 순서, 섹션별 목적 한 줄, 핵심 카피, 레이아웃 지시, 반응형 규칙
```

---

## 2. 레퍼런스 조사

1. 인터뷰 답변(업종·톤·고객)으로 국내외 사이트 6~9곳을 고른다. 같은 업종 3~4곳 + 톤이 맞는 타 업종 3~5곳.
2. Playwright로 1440px·375px 스크린샷을 `brand/refs/`에 저장한다.
3. 표로 정리한다: | 사이트 | 가져올 점 | 피할 점 | 우리 적용 |
4. 레퍼런스의 로고·사진·카피를 **복제하지 않는다**. 구조와 분위기만 참고한다.

---

## 3. 로고 3안 → 확정

### 3-1. 생성
방향이 서로 다른 3안을 만든다. 같은 방향의 색만 다른 3개는 시안이 아니다.

| 안 | 방향 | 예시 |
|---|---|---|
| A | 심볼 + 워드마크 | 업종 도구/지역 상징을 단순화한 심볼 옆에 한글 상호 |
| B | 워드마크 중심 | 한글 상호 자체를 손글씨·붓·기하 형태로 디자인 |
| C | 엠블럼/배지 | 원형·사각 프레임 안에 심볼과 상호, 간판·스티커에 강함 |

```bash
node scripts/gen-image.mjs --name logo-A --n 2 --quality high --size 1024x1024 \
  --out brand/logo/candidates --prompt-file brand/prompts/logo-A.txt
```

로고 프롬프트 골격:

```
Logo design for a Korean [업종] brand named "[한글 상호]".
Type: [symbol + wordmark | wordmark | emblem].
Symbol idea: [모티브를 2~3단어로], simplified into flat geometric shapes.
Style: [성격 키워드], flat vector look, 2 colors only: [HEX1] and [HEX2].
Render the Korean text "[한글 상호]" exactly, no other text, no slogan.
Centered on a plain white background, generous margin.
Must stay readable at 32px and in one color. No gradients, no 3D, no photo, no mockup.
```

### 3-2. 비교·선택
- 비교 페이지(시안 + 흰/검정 배경 + 32px 축소본 + 간판 가로형 모의)를 만들어 사용자에게 보여준다.
- 고르는 기준을 쉬운 말로 함께 적는다: "작게 줄여도 읽히나요? 한 색으로 찍어도 알아보나요? 업종이 바로 떠오르나요?"

### 3-3. SVG로 확정
gpt-image 계열은 **투명 배경을 보장하지 않고**(gpt-image-2는 transparent 배경 미지원), 글자 획도 미세하게 흔들린다. 그래서 선택안은 **SVG로 다시 그린다**.

- 심볼: 원본 PNG를 보며 단순 도형·패스로 재작성 (8~20개 패스 이내)
- 글자: 웹폰트 아웃라인(예: 선택 폰트)을 기반으로 하거나 획을 패스로 재작성
- 산출물 (`brand/logo/`): `logo.svg`(기본), `logo-horizontal.svg`(간판), `logo-mono.svg`(단색), `symbol.svg`, `favicon.svg` + `favicon-32.png`, `apple-touch-icon.png`(180), `og-image.png`(1200×630)
- 확정 후 원본 PNG 후보는 `brand/logo/candidates/`에 기록용으로만 둔다.

---

## 4. 이미지 프롬프트 템플릿

OpenAI 권장 구조: **배경/환경 → 피사체 → 세부 → 제약**. 짧은 "제작 브리프"처럼 쓴다.

```
[용도] Hero photo for a Korean neighborhood side-dish shop website, 16:9 landscape.
[배경] Small clean shop interior at early evening, warm 3000K light, glass refrigerated showcase.
[피사체] Rows of small transparent containers of Korean banchan (spinach namul, braised beef jangjorim, kimchi), labeled with plain stickers.
[세부] Shot on 35mm, f/2.8, eye level, shallow depth of field, natural textures, realistic food styling, steam-free.
[제약] Photorealistic. No text, no logos, no watermark, no people's faces in focus. Korean setting, not Japanese or Western.
```

규칙
- 재질·조명을 구체적으로 쓴다: "shiny" 대신 "brushed stainless steel", "light" 대신 "soft window light from left".
- 이미지 안 글자가 필요하면 **따옴표로 정확히** 쓰고 "no other text"를 붙인다. 가격·법정 표시 같은 정확해야 할 글자는 이미지에 넣지 말고 HTML로 올린다.
- 사람은 한국인 연령대·옷차림·상황을 구체적으로 쓴다. 실존 인물·유명인을 닮게 하지 않는다.
- 같은 상품을 여러 컷 만들 때는 첫 컷을 `--ref`로 넣어 일관성을 유지한다. 편집을 연달아 반복하면 화질이 떨어지므로, 원본에서 다시 생성하는 편이 낫다.
- 크기: 정사각 `1024x1024`(상품 카드), 가로 `1536x1024`(히어로·배너), 세로 `1024x1536`(상세페이지 컷). 시안 단계는 `--quality medium`, 확정 컷만 `high`로 비용을 아낀다.

### 연출 이미지 고지
가게·상품이 아직 실물 촬영 전이면 AI 이미지는 "연출 이미지"다. 상세페이지와 상품 카드 하단에 다음 문구를 넣는다.

> 상품 이미지는 연출된 예시로, 실제 상품과 구성·담음새가 다를 수 있습니다.

오픈 후에는 실제 사진으로 교체하는 것을 권한다(신뢰·표시광고 리스크).

---

## 5. 파일 규칙

```
brand/
  meta-prompt.md        # 3블록 메타프롬프트
  prompts/              # 재사용 프롬프트 txt
  prompts.jsonl         # gen-image.mjs 자동 기록 (프롬프트·크기·품질·파일)
  refs/                 # 레퍼런스 스크린샷 + refs.md 표
  logo/                 # 확정 SVG/PNG, candidates/
  images/               # 히어로·상품·상세 컷
```

웹에 올릴 때는 `next/image`(또는 `<picture>` + WebP/AVIF)로 최적화하고, 원본 PNG는 `brand/`에만 둔다.
