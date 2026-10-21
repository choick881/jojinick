"use client";
// 토스페이먼츠 v2 결제위젯: 결제 수단 고르기 + 약관. 결제 요청은 주문 저장 뒤 checkout-form이 한다.
import { ANONYMOUS, loadTossPayments, type TossPaymentsWidgets } from "@tosspayments/tosspayments-sdk";
import { useEffect, useRef, useState } from "react";
import { TOSS_CLIENT_KEY } from "@/lib/toss-client";

export type WidgetStatus = "loading" | "ready" | "error";

/** 금액이 생기면 결제위젯을 #payment-method, #agreement 자리에 그린다. 금액이 바뀌면 위젯 금액만 고친다. */
export function usePaymentWidgets(amount: number) {
  const [widgets, setWidgets] = useState<TossPaymentsWidgets | null>(null);
  const [status, setStatus] = useState<WidgetStatus>("loading");
  const rendered = useRef(false);

  useEffect(() => {
    let alive = true;
    loadTossPayments(TOSS_CLIENT_KEY)
      .then((tp) => alive && setWidgets(tp.widgets({ customerKey: ANONYMOUS })))
      .catch(() => alive && setStatus("error"));
    return () => {
      alive = false;
    };
  }, []);

  useEffect(() => {
    if (!widgets || amount <= 0) return;
    const value = { currency: "KRW", value: amount };
    if (rendered.current) {
      widgets.setAmount(value).catch(() => setStatus("error"));
      return;
    }
    rendered.current = true;
    (async () => {
      await widgets.setAmount(value);
      await Promise.all([
        widgets.renderPaymentMethods({ selector: "#payment-method", variantKey: "DEFAULT" }),
        widgets.renderAgreement({ selector: "#agreement", variantKey: "AGREEMENT" }),
      ]);
      setStatus("ready");
    })().catch(() => setStatus("error"));
  }, [widgets, amount]);

  return { widgets, status };
}

/** 위젯이 그려질 자리. 불러오는 동안·실패했을 때 안내 문구를 보여 준다. */
export function PaymentWidgetSlot({ status, hasItems }: { status: WidgetStatus; hasItems: boolean }) {
  return (
    <div className="grid gap-2">
      {!hasItems ? (
        <p className="rounded-[14px] border-2 border-dashed border-line p-5 text-center text-[.88rem] text-muted">메뉴를 담으면 결제 수단이 열립니다.</p>
      ) : status === "error" ? (
        <p role="alert" className="rounded-[14px] border-2 border-dashed border-line p-5 text-center text-[.88rem] text-muted">결제 수단을 불러오지 못했어요. 화면을 새로고침해 주세요.</p>
      ) : status === "loading" ? (
        <p className="rounded-[14px] bg-[var(--soft)] p-5 text-center text-[.88rem] text-muted" aria-live="polite">결제 수단을 불러오는 중이에요…</p>
      ) : null}
      {/* 위젯은 이 두 칸 안에 그려진다. 항상 화면에 두어야 금액이 바뀌어도 다시 그리지 않는다 */}
      <div id="payment-method" className={hasItems ? "" : "hidden"} />
      <div id="agreement" className={hasItems ? "" : "hidden"} />
    </div>
  );
}
