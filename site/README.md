# 온담찬 사이트 (`site/`)

양주 무인 반찬가게 온담찬의 홈페이지. Next.js 16 (App Router, Cache Components) + TypeScript + Tailwind CSS 4.

```bash
npm install
npm run dev          # http://localhost:3000
npm test             # Vitest (픽업 시간·금액 계산)
npm run typecheck && npm run lint
npm run build        # prebuild가 ../brand 의 메뉴·로고를 복사
```

- 메뉴와 로고의 원본은 저장소의 `brand/`입니다. 바꾼 뒤 `npm run sync:brand`.
- 데이터는 `lib/catalog.ts` 한 곳에서 읽습니다(Supabase, 실패하면 메뉴 파일).
- 결제 금액은 서버가 `lib/price.ts`로 다시 계산합니다(클라이언트 가격은 믿지 않음).
- 주문·결제: `/api/orders`(주문 저장) → 토스 결제위젯 → `/api/payments/confirm`(금액 대조 후 승인).
- 환경변수 목록은 `.env.example`. 값은 Vercel → Settings → **Environment Variables**에만 넣습니다(Environments 메뉴와 다름). 바꾼 뒤에는 새 배포가 있어야 반영됩니다.
- 서버 키 점검: 배포 주소의 `/api/health`가 `{"db":"ok"}`이면 `SUPABASE_SECRET_KEY`가 맞습니다.
- 진행 상황: `../docs/plans/PLAN_ondamchan-site.md`
