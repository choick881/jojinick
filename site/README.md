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
- 데이터는 `lib/catalog.ts` 한 곳에서 읽습니다. Supabase를 연결하면 이 파일만 바꿉니다.
- 결제 금액은 서버가 `lib/price.ts`로 다시 계산합니다(클라이언트 가격은 믿지 않음).
- 진행 상황: `../docs/plans/PLAN_ondamchan-site.md`
