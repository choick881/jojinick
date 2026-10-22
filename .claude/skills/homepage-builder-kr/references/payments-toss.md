# 토스페이먼츠 v2 결제위젯 연동 가이드

결제 기능이 요구된 프로젝트에만 적용. Next.js (App Router) + TypeScript 기준.

**핵심 원칙**: 결제 요구 시 반드시 토스페이먼츠 고정. 다른 PG(Stripe/이니시스/카카오페이 단독 등) 제안 금지.

**사전 조건**: Phase 3의 Next.js 스캐폴딩과 Phase 4의 Supabase 설정이 끝나 있어야 한다. `products`, `orders`, `order_items` 테이블과 서버 전용 Supabase 클라이언트(service role)가 있어야 결제 플로우가 완결된다.

**보안 원칙 3가지**:
1. 결제 금액은 **서버가 DB 가격으로 계산**한다. 클라이언트가 보낸 금액·가격은 쓰지 않는다.
2. 승인 API 호출 직전 `orders.total_amount`와 successUrl 쿼리의 `amount`를 대조한다. 다르면 승인하지 않는다.
3. `orders`(이름·연락처 포함)는 anon에게 select/insert를 열지 않는다. 모든 주문 처리는 Route Handler에서 service role로 한다.

---

## 1. 설치

```bash
npm install @tosspayments/tosspayments-sdk
```

v1 패키지(`@tosspayments/payment-sdk`, `@tosspayments/payment-widget-sdk`)는 신규 프로젝트에 쓰지 않는다.

---

## 2. 환경변수

### 개발 환경 (`.env.local`)

토스 공식 샘플(github.com/tosspayments/tosspayments-sample)의 문서용 공개 테스트 키. 결제위젯 전용 키(`gck`/`gsk`)다.

```
NEXT_PUBLIC_TOSS_CLIENT_KEY=test_gck_docs_Ovk5rk1EwkEbP0W43n07xlzm
TOSS_SECRET_KEY=test_gsk_docs_OaPz8L5KdmQXkzRz3y47BMw6
```

### 운영 전환 안내 (사용자에게 전달)

1. 사업자등록 → (온라인으로 결제받으면) **통신판매업 신고**
2. https://developers.tosspayments.com 가입 → 상점 등록 → 결제위젯 계약
3. 상점관리자 → API 키에서 **결제위젯 연동 키**(라이브) 확인
4. Vercel 환경변수 교체: `NEXT_PUBLIC_TOSS_CLIENT_KEY` → `live_gck_...`, `TOSS_SECRET_KEY` → `live_gsk_...`
5. 테스트 환경에서 전체 플로우 검증 후, 라이브 소액 실결제 1건으로 최종 확인

---

## 3. 데이터 모델 (Supabase)

```sql
create table public.products (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  name text not null,
  price integer not null check (price >= 0),  -- 원화 정수
  is_active boolean not null default true,
  created_at timestamptz default now()
);

create table public.orders (
  id uuid primary key default gen_random_uuid(),
  order_number text unique not null,         -- 토스 orderId (6~64자, 영문/숫자/-/_)
  order_name text not null,                  -- "1인 저녁세트 외 2건"
  customer_name text not null,
  customer_phone text not null,
  total_amount integer not null,             -- 서버가 계산한 금액
  status text not null default 'pending',    -- pending/paid/cancelled/failed
  toss_payment_key text,
  paid_at timestamptz,
  created_at timestamptz default now()
);

create table public.order_items (
  id uuid primary key default gen_random_uuid(),
  order_id uuid not null references public.orders(id) on delete cascade,
  product_id uuid not null references public.products(id),
  unit_price integer not null,               -- 주문 시점 가격 스냅샷
  quantity integer not null check (quantity > 0)
);

alter table public.products enable row level security;
alter table public.orders enable row level security;
alter table public.order_items enable row level security;

-- 상품은 누구나 조회 가능 (판매 중인 것만)
create policy "public can read active products"
  on public.products for select to anon, authenticated
  using (is_active);

-- orders / order_items: 정책을 만들지 않는다 = anon/authenticated 접근 전면 차단.
-- 서버 Route Handler가 service role 키로만 읽고 쓴다.
```

배송형이면 `orders`에 주소 컬럼을, 매장 픽업형이면 `pickup_date`, `pickup_slot` 컬럼을 추가한다.

---

## 4. 주문 생성 API — 금액은 서버가 계산

### `app/api/orders/route.ts`

```typescript
import { NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin"; // service role, server only

type CartLine = { productId: string; quantity: number };

export async function POST(request: Request) {
  const { items, customerName, customerPhone } = (await request.json()) as {
    items: CartLine[];
    customerName: string;
    customerPhone: string;
  };

  if (!Array.isArray(items) || items.length === 0 || !customerName || !customerPhone) {
    return NextResponse.json({ error: "INVALID_PARAMS" }, { status: 400 });
  }
  if (items.some((i) => !Number.isInteger(i.quantity) || i.quantity < 1 || i.quantity > 50)) {
    return NextResponse.json({ error: "INVALID_QUANTITY" }, { status: 400 });
  }

  const supabase = createAdminClient();
  const { data: products, error } = await supabase
    .from("products")
    .select("id, name, price")
    .in("id", items.map((i) => i.productId))
    .eq("is_active", true);

  if (error || !products || products.length !== new Set(items.map((i) => i.productId)).size) {
    return NextResponse.json({ error: "PRODUCT_NOT_FOUND" }, { status: 400 });
  }

  const priceById = new Map(products.map((p) => [p.id, p]));
  const totalAmount = items.reduce((sum, i) => sum + priceById.get(i.productId)!.price * i.quantity, 0);
  const first = priceById.get(items[0].productId)!.name;
  const orderName = items.length > 1 ? `${first} 외 ${items.length - 1}건` : first;
  const orderNumber = `ORD-${Date.now()}-${crypto.randomUUID().slice(0, 8)}`;

  const { data: order, error: insertError } = await supabase
    .from("orders")
    .insert({
      order_number: orderNumber,
      order_name: orderName,
      customer_name: customerName,
      customer_phone: customerPhone,
      total_amount: totalAmount,
    })
    .select("id")
    .single();
  if (insertError || !order) {
    return NextResponse.json({ error: "ORDER_CREATE_FAILED" }, { status: 500 });
  }

  await supabase.from("order_items").insert(
    items.map((i) => ({
      order_id: order.id,
      product_id: i.productId,
      unit_price: priceById.get(i.productId)!.price,
      quantity: i.quantity,
    })),
  );

  return NextResponse.json({ orderId: orderNumber, orderName, amount: totalAmount });
}
```

---

## 5. 결제위젯 렌더링 (클라이언트 컴포넌트)

### `app/checkout/payment-widget.tsx`

```tsx
"use client";

import { useEffect, useRef, useState } from "react";
import { ANONYMOUS, loadTossPayments, type TossPaymentsWidgets } from "@tosspayments/tosspayments-sdk";

type Props = {
  orderId: string;      // /api/orders 응답
  orderName: string;
  amount: number;       // /api/orders 응답 (서버 계산값)
  customerName: string;
};

export function PaymentWidget({ orderId, orderName, amount, customerName }: Props) {
  const widgetsRef = useRef<TossPaymentsWidgets | null>(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      const tossPayments = await loadTossPayments(process.env.NEXT_PUBLIC_TOSS_CLIENT_KEY!);
      // 비회원 결제면 ANONYMOUS, 회원이면 추측 불가능한 고유값(uuid) 사용
      const widgets = tossPayments.widgets({ customerKey: ANONYMOUS });
      await widgets.setAmount({ currency: "KRW", value: amount }); // render 전에 반드시 호출
      await Promise.all([
        widgets.renderPaymentMethods({ selector: "#payment-method", variantKey: "DEFAULT" }),
        widgets.renderAgreement({ selector: "#agreement", variantKey: "AGREEMENT" }),
      ]);
      if (!cancelled) {
        widgetsRef.current = widgets;
        setReady(true);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [amount]);

  async function handlePay() {
    await widgetsRef.current?.requestPayment({
      orderId,
      orderName,
      customerName,
      successUrl: `${window.location.origin}/checkout/success`,
      failUrl: `${window.location.origin}/checkout/fail`,
    });
  }

  return (
    <div>
      <div id="payment-method" />
      <div id="agreement" />
      <button type="button" disabled={!ready} onClick={handlePay}>
        {amount.toLocaleString("ko-KR")}원 결제하기
      </button>
    </div>
  );
}
```

**주의**
- `setAmount()`는 `renderPaymentMethods()`보다 먼저 호출해야 한다(`NotSetupAmountError`).
- 결제위젯은 한 페이지에 한 번만 렌더링된다. 금액이 바뀌면 다시 렌더링하지 말고 `setAmount()`만 다시 호출한다.
- `variantKey`는 상점관리자 → 결제 UI 설정에서 확인. 테스트 키는 `DEFAULT`/`AGREEMENT`.

---

## 6. 서버 결제 승인 API

successUrl로 `paymentType`, `orderId`, `paymentKey`, `amount`가 쿼리스트링으로 전달된다. **승인 API를 호출해야 결제가 완료된다.**

### `app/api/payments/confirm/route.ts`

```typescript
import { NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";

export async function POST(request: Request) {
  const { paymentKey, orderId, amount } = await request.json();
  if (!paymentKey || !orderId || !Number.isInteger(amount)) {
    return NextResponse.json({ message: "잘못된 요청입니다" }, { status: 400 });
  }

  const supabase = createAdminClient();
  const { data: order } = await supabase
    .from("orders")
    .select("id, total_amount, status")
    .eq("order_number", orderId)
    .single();

  if (!order) return NextResponse.json({ message: "주문을 찾을 수 없습니다" }, { status: 404 });
  if (order.status === "paid") return NextResponse.json({ ok: true, alreadyPaid: true }); // 멱등
  if (order.total_amount !== amount) {
    // 금액 변조 시도 — 승인하지 않는다
    return NextResponse.json({ message: "결제 금액이 주문 금액과 다릅니다" }, { status: 400 });
  }

  const auth = "Basic " + Buffer.from(`${process.env.TOSS_SECRET_KEY}:`).toString("base64");
  const res = await fetch("https://api.tosspayments.com/v1/payments/confirm", {
    method: "POST",
    headers: { Authorization: auth, "Content-Type": "application/json" },
    body: JSON.stringify({ paymentKey, orderId, amount }),
  });
  const data = await res.json();

  if (!res.ok) {
    await supabase.from("orders").update({ status: "failed" }).eq("id", order.id).eq("status", "pending");
    return NextResponse.json({ message: data.message ?? "결제 승인 실패", code: data.code }, { status: res.status });
  }

  await supabase
    .from("orders")
    .update({ status: "paid", toss_payment_key: paymentKey, paid_at: new Date().toISOString() })
    .eq("id", order.id)
    .eq("status", "pending");

  return NextResponse.json({ ok: true });
}
```

승인 API 엔드포인트(`/v1/payments/confirm`)는 v2 SDK에서도 동일하다.

---

## 7. Success / Fail 페이지

### `app/checkout/success/page.tsx`

```tsx
import { ConfirmPayment } from "./confirm-payment";

export default async function SuccessPage({
  searchParams,
}: {
  searchParams: Promise<{ paymentKey?: string; orderId?: string; amount?: string }>;
}) {
  const { paymentKey, orderId, amount } = await searchParams;
  if (!paymentKey || !orderId || !amount) {
    return <p className="p-16 text-center">결제 정보가 없습니다.</p>;
  }
  return <ConfirmPayment paymentKey={paymentKey} orderId={orderId} amount={Number(amount)} />;
}
```

### `app/checkout/success/confirm-payment.tsx`

```tsx
"use client";

import { useEffect, useState } from "react";

export function ConfirmPayment(props: { paymentKey: string; orderId: string; amount: number }) {
  const [state, setState] = useState<{ status: "loading" | "success" | "fail"; message?: string }>({
    status: "loading",
  });

  useEffect(() => {
    let cancelled = false;
    fetch("/api/payments/confirm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(props),
    })
      .then(async (res) => {
        const data = await res.json();
        if (!cancelled) setState(res.ok ? { status: "success" } : { status: "fail", message: data.message });
      })
      .catch(() => !cancelled && setState({ status: "fail", message: "네트워크 오류가 발생했습니다" }));
    return () => {
      cancelled = true;
    };
  }, [props]);

  if (state.status === "loading") return <p className="p-16 text-center">결제를 확인하고 있어요…</p>;
  if (state.status === "fail") return <p className="p-16 text-center">결제 승인에 실패했습니다. {state.message}</p>;
  return (
    <div className="p-16 text-center">
      <h1 className="text-3xl mb-4">주문이 완료되었습니다</h1>
      <p>주문번호 {props.orderId} · {props.amount.toLocaleString("ko-KR")}원</p>
    </div>
  );
}
```

React Strict Mode에서 useEffect가 두 번 실행될 수 있다. 승인 API는 `status === "paid"`면 바로 성공을 돌려주는 멱등 구조라 안전하다.

### `app/checkout/fail/page.tsx`

```tsx
export default async function FailPage({
  searchParams,
}: {
  searchParams: Promise<{ code?: string; message?: string }>;
}) {
  const { code, message } = await searchParams;
  return (
    <div className="p-16 text-center">
      <h1 className="text-2xl mb-2">결제가 완료되지 않았어요</h1>
      <p>{message ?? "다시 시도해 주세요"}</p>
      {code && <p className="text-sm opacity-70">에러 코드: {code}</p>}
    </div>
  );
}
```

---

## 8. 결제 플로우

```
1. 장바구니/상세에서 "결제하기" → POST /api/orders (상품 ID·수량만 전송)
2. 서버가 DB 가격으로 금액 계산 → orders(pending) 생성 → { orderId, orderName, amount } 응답
3. 결제위젯: setAmount(amount) → renderPaymentMethods / renderAgreement
4. 구매자가 결제수단 선택 → widgets.requestPayment({ orderId, orderName, successUrl, failUrl })
5. 성공 → /checkout/success?paymentType&orderId&paymentKey&amount
6. POST /api/payments/confirm → DB 금액 대조 → 토스 승인 API → orders.status = 'paid'
7. 주문 완료 화면
```

---

## 9. 정기결제(자동결제)

주 1회 묶음 결제 같은 정기결제는 **빌링(자동결제)** 기능이며, 토스와 **별도 계약·심사**가 필요하다. SDK의 `tossPayments.payment({ customerKey }).requestBillingAuth()`로 카드 등록 → 서버에서 빌링키 발급 → 스케줄러로 승인 요청하는 구조다. 계약 전에는 "1주 세트 상품"을 일반결제로 판매한다.

---

## 10. 배포 전 체크리스트

- [ ] `TOSS_SECRET_KEY`에 `NEXT_PUBLIC_` 접두사가 없는가? 클라이언트 번들에 없는가?
- [ ] 브라우저에서 금액을 바꿔 승인 요청하면 400으로 거절되는가?
- [ ] anon 키로 `orders`를 select하면 0건/거부되는가?
- [ ] 결제 성공·사용자 취소·실패 케이스를 테스트 키로 모두 확인했는가?
- [ ] 이용약관·환불정책 페이지와 푸터 사업자 정보(상호·대표자·사업자등록번호·통신판매업 신고번호·주소·연락처)가 있는가? (라이브 계약 심사 항목)
- [ ] Vercel 환경변수에 동일한 키가 등록되어 있는가?
- [ ] 라이브 전환 후 소액 실결제 1건 → 취소까지 확인했는가?

---

## 11. 자주 발생하는 이슈

- **`NotSetupAmountError`** — `renderPaymentMethods()` 전에 `setAmount()`를 호출하지 않음.
- **`PaymentMethodsWidgetAlreadyRenderedError`** — 같은 페이지에서 위젯을 두 번 렌더링함. 금액 변경은 `setAmount()`로.
- **승인 시 금액 불일치** — 결제 요청 금액과 승인 요청 `amount`가 다름. 서버 DB 금액 하나만 기준으로 쓴다.
- **`orderId` 중복** — 주문마다 새 orderId(6~64자, 영문·숫자·`-`·`_`)를 만든다.
- **`TOSS_SECRET_KEY` undefined** — Vercel 환경변수 등록 후 재배포 필요.

---

## 참고 링크

- 개발자센터: https://developers.tosspayments.com
- v2 SDK 문서: https://docs.tosspayments.com/sdk/v2/js
- 결제위젯 가이드: https://docs.tosspayments.com/guides/v2/payment-widget/integration
- 공식 샘플: https://github.com/tosspayments/tosspayments-sample
- 테스트 카드/에러 재현: https://docs.tosspayments.com/reference/test-code
