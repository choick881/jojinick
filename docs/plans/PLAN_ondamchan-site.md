# 실행 계획: 온담찬 실제 사이트 (`site/`)

**상태**: 진행 중 · **시작**: 2026-10-21 · **마지막 갱신**: 2026-10-21
**근거**: `docs/PLAN.md` F단계, 시안 확정(홈 1안 + 2안 현황판, 상세 A + B 요약표, 로고 C 엠블럼 + A 가로형)

**CRITICAL INSTRUCTIONS**: 각 Phase를 마치면
1. ✅ 완료한 작업 체크
2. 🧪 품질 게이트 명령 실행
3. ⚠️ 모든 게이트 통과 확인
4. 📅 "마지막 갱신" 날짜 수정
5. 📝 Notes에 배운 점 기록
6. ➡️ 그다음에만 다음 Phase로

⛔ 게이트를 건너뛰거나 실패한 채로 넘어가지 않는다

---

## 결정 사항

| 항목 | 결정 | 이유 |
|---|---|---|
| 스택 | Next.js (App Router) + TypeScript + Tailwind CSS | 주문·결제·관리자 등 서버 기능이 필요 |
| UI 부품 | 직접 만든 소수 컴포넌트 (shadcn/ui는 필요할 때만 추가) | 시안 디자인을 그대로 옮기기 쉬움, 의존성 최소 |
| 데이터 | `lib/catalog.ts` 한 곳에서 읽음. Supabase 환경변수가 없으면 `brand/menu.json` 복사본 사용 | DB 결정 전에도 화면 개발 가능 (사용자 결정: DB는 나중에) |
| DB | Supabase (Phase 3에서 생성 방법 확정: 무료 2개 한도 사용 중) | 사용자 확인 필요 |
| 결제 | 토스페이먼츠 v2 결제위젯, 문서용 공개 테스트 키 | 스킬 고정 규칙 |
| 배포 | Vercel, GitHub 연동, Root Directory `site/`, 미리보기 먼저 | 운영 배포는 사용자 확인 후 |
| 테스트 | Vitest(가격 계산·픽업 슬롯·주문 검증), Playwright(주요 흐름 스모크) | 비즈니스 로직 80% 이상 |

---

## Phase 1. 뼈대 · 디자인 토큰 · 공통 화면
**목표**: `site/`에서 빌드되는 Next.js 앱, 확정 톤(크림·된장·주홍, 18px, 큰 글씨)과 머리글·바닥글·로고·메타 적용
- [x] create-next-app (TS, Tailwind, App Router), `.gitignore`에 `.env*`
- [x] 디자인 토큰(`globals.css`), Noto Serif KR / Noto Sans KR / Nanum Pen Script (`next/font`)
- [x] 로고·파비콘·OG 이미지를 `public/`으로, `metadata` 기본값
- [x] 머리글(로고, 메뉴, 큰 글씨, 담은 상품), 바닥글(사업자 정보 자리)
- [x] Vitest·Playwright 설정
**게이트**: `npm run build`, `npm run lint`, 375/768/1440 캡처에서 겹침·잘림 없음
**되돌리기**: `site/` 폴더 삭제

## Phase 2. 화면: 홈 · 메뉴 · 상세 · 어르신 밥상 · 가게 이야기
**목표**: 시안을 실제 컴포넌트로. 데이터는 `lib/catalog.ts`
- [x] RED: `lib/slots.test.ts`(30분 슬롯, 마감 시각 이후 오늘 제외), `lib/price.test.ts`(합계·수량 한도)
- [x] GREEN: `lib/slots.ts`, `lib/price.ts`, `lib/catalog.ts`
- [x] 홈: 두 손님 카드 + 매장 현황판(제조 시각·판매 중 종류 수) + 오늘의 반찬 + 이용 방법 + 약속 + 어르신 밥상 + 매장 안내
- [x] `/menu`(분류 탭), `/menu/[slug]`(상세 A + 요약표, 정보 고시, FAQ), `/silver`, `/about`
- [x] 장바구니(로컬 저장) + 하단 구매 바
**게이트**: 테스트 통과, 빌드·린트, 모든 라우트 375/1440 캡처, 가로 스크롤 없음
**되돌리기**: 해당 커밋 되돌리기

## Phase 3. Supabase 스키마 · RLS · 시드 *(DB 생성 방법 확정 후)*
- [ ] 테이블: `products`, `pickup_slots`(용량), `orders`(fulfillment_type, recipient_*, address_* nullable), `order_items`, `store_status`(오늘 제조 시각)
- [ ] RLS: anon은 `products`·`store_status` 읽기만, `orders`·`order_items` 접근 불가
- [ ] 시드: `brand/menu.json`
**게이트**: anon 키로 `orders` select 0건, Supabase advisors 경고 없음
**되돌리기**: 마이그레이션 down SQL

## Phase 4. 주문 · 토스 테스트 결제
- [ ] RED: 주문 검증 테스트(빈 장바구니, 품절, 지난 슬롯, 금액 위조 → 400)
- [ ] `/checkout`(픽업 날짜·시간, 주문자, 받는 분, 배송 옵션은 스위치로 숨김), `/api/orders`(서버가 DB 가격으로 합계)
- [ ] 토스 결제위젯, `/api/payments/confirm`(금액 대조), `/checkout/success|fail`
- [ ] `/policy/terms`, `/policy/refund`
**게이트**: 테스트 키로 결제 → `orders.status = paid`, 위조 금액 거절
**되돌리기**: 결제 라우트 비활성 스위치

## Phase 5. 관리자 · 알림
- [ ] `/admin` Supabase Auth 이메일 로그인 (관리자 이메일 허용 목록)
- [ ] 오늘 제조 시각 입력, 품절 토글, 오늘 주문 목록(픽업 시간순)
- [ ] 주문 이메일 알림: 메일 서비스 키가 있을 때만, 없으면 관리자 화면 알림만
**게이트**: 비로그인 접근 차단, 품절 토글이 메뉴에 반영

## Phase 6. 검색 노출 · 점검 · 배포
- [x] `sitemap.ts`, `robots.ts`(미리보기 배포는 검색 차단), JSON-LD(FoodEstablishment·Product), 상품 메타·canonical
- [ ] Lighthouse 목표: 성능 90 / 접근성 95 / SEO 100 — 로컬 측정(모바일): 접근성·SEO·권장사항 100, 성능 메뉴 93·어르신 99·주문 91·상세 78·홈 74 (남은 원인: 명조·손글씨 웹 글꼴). Vercel에서 재측정
- [ ] 시크릿 스캔(`.env` 추적 여부)
- [ ] Vercel 프로젝트 연결(Root `site/`), 미리보기 배포 → 운영은 사용자 확인 후
**게이트**: 미리보기 URL에서 전체 흐름 확인

---

## 위험

| 위험 | 확률 | 영향 | 대응 |
|---|---|---|---|
| Supabase 무료 한도(2개) | 확정 | 높음 | Phase 3 전에 사용자 결정(일시정지 / Pro / 기존 프로젝트 공유) |
| 사진 없음 (OpenAI 키가 예시 문구) | 높음 | 중간 | 사진 자리 컴포넌트로 두고 키 교체 후 일괄 생성 |
| 식품 표시·환불 정책 미확정 | 높음 | 중간 | "확인 필요" 표시 유지, 오픈 전 체크리스트 |
| 토스 실키·통신판매업 신고 | 중간 | 높음 | 테스트 키로 개발, 운영 전환은 사업자 준비 후 |

## Notes
- 2026-10-21: 계획 승인. DB는 화면 완성 후 결정하기로 함.
- 2026-10-21 Phase 1·2 완료: Next.js 16.4.2(Cache Components 기본). 브라우저 상태(장바구니·큰 글씨·시각)는 React 19 린트 규칙에 맞춰 `useSyncExternalStore` 저장소(`lib/browser-store.ts`)로 구현. 픽업 시간은 KST 고정 계산, 슬롯 시작 60분 전 마감.
  - 게이트: Vitest 14개 통과, tsc·eslint 0건, `next build` 정적 30페이지, 375/768/1440 × 9개 경로 가로 스크롤·콘솔 오류 없음(404 페이지의 404 응답 제외), 담기→주문 화면 흐름 확인
  - 배운 점: 좁은 표 칸에서 `overflow-wrap: anywhere`가 "20:30"을 쪼갬 → `break-word` + `nowrap`
- 2026-10-21 6단계 일부: 사이트맵·robots·구조화 데이터 추가. 성능 개선 — 본문 웹 글꼴(Noto Sans KR 4굵기) 제거 → 기기 한글 글꼴, 명조는 900만. 홈 FCP 7.4s→3.8s, 전송량 1.2MB→0.6MB. 픽업 선택 칸을 같은 모양의 자리로 먼저 그려 상세 CLS 0.18→0.
- Vercel 미리보기: 커넥터에 choick1 팀 권한이 없어(403) 프로젝트 생성 불가 → 사용자가 vercel.com에서 Import(Root Directory=site)하거나 커넥터 재연결 필요
