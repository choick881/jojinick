"use client";
// 토스 결제창이 돌려보낸 화면. 성공이면 서버에 승인을 요청하고(금액 대조는 서버가 한다), 실패면 이유를 보여 준다.
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import { won } from "@/lib/price";
import { useCart } from "./cart";

type Paid = { orderId: string; orderName: string; amount: number; pickupDate: string; pickupTime: string; recipientName: string | null };
type State = { kind: "checking" } | { kind: "paid"; order: Paid } | { kind: "error"; message: string };

const CONFIRM_ERROR: Record<string, string> = {
  AMOUNT_MISMATCH: "결제 금액이 주문 금액과 달라 결제를 진행하지 않았어요.",
  ORDER_NOT_FOUND: "주문을 찾지 못했어요.",
  ORDER_NOT_PENDING: "이미 처리되었거나 취소된 주문이에요.",
  NOT_CONFIGURED: "결제 준비가 아직 끝나지 않았어요. 가게에 문의해 주세요.",
};

function pickupLabel(date: string, time: string) {
  const d = new Date(`${date}T00:00:00+09:00`);
  const weekday = "일월화수목금토"[new Date(d.getTime() + 9 * 3600_000).getUTCDay()];
  return `${Number(date.slice(5, 7))}월 ${Number(date.slice(8, 10))}일 (${weekday}) ${time.slice(0, 5)}`;
}

function Shell({ hand, title, children }: { hand: string; title: string; children: React.ReactNode }) {
  return (
    <div className="grid justify-items-center gap-4 text-center">
      <span className="hand">{hand}</span>
      <h1 className="title text-[1.8rem]">{title}</h1>
      {children}
    </div>
  );
}

export function ConfirmPayment() {
  const params = useSearchParams();
  const cart = useCart();
  const [state, setState] = useState<State>({ kind: "checking" });
  const sent = useRef(false);

  const paymentKey = params.get("paymentKey");
  const orderId = params.get("orderId");
  const amount = params.get("amount");
  const { clear } = cart;

  useEffect(() => {
    if (sent.current) return;
    sent.current = true;
    if (!paymentKey || !orderId || !amount) {
      queueMicrotask(() => setState({ kind: "error", message: "결제 정보가 없어요. 주문 화면에서 다시 시도해 주세요." }));
      return;
    }
    fetch("/api/payments/confirm", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ paymentKey, orderId, amount: Number(amount) }),
    })
      .then(async (res) => {
        const data = (await res.json().catch(() => ({}))) as Partial<Paid> & { ok?: boolean; error?: string; message?: string };
        if (res.ok && data.ok) {
          clear();
          setState({ kind: "paid", order: data as Paid });
        } else {
          setState({ kind: "error", message: CONFIRM_ERROR[data.error ?? ""] ?? data.message ?? "결제를 확인하지 못했어요." });
        }
      })
      .catch(() => setState({ kind: "error", message: "인터넷 연결을 확인한 뒤 이 화면을 새로고침해 주세요." }));
  }, [paymentKey, orderId, amount, clear]);

  if (state.kind === "checking") return <p className="lead text-center" aria-live="polite">결제를 확인하고 있어요…</p>;
  if (state.kind === "error")
    return (
      <Shell hand="결제를 마치지 못했어요" title="결제가 완료되지 않았어요">
        <p className="lead" role="alert">{state.message}</p>
        <Link href="/checkout" className="btn btn-primary">주문 화면으로 돌아가기</Link>
      </Shell>
    );

  const o = state.order;
  return (
    <Shell hand="주문해 주셔서 고맙습니다" title="결제가 끝났어요">
      <dl className="card grid w-full gap-2.5 p-5 text-left text-[.95rem] [&_dt]:text-muted [&_dd]:font-bold">
        <div className="flex justify-between gap-3"><dt>주문 번호</dt><dd className="num">{o.orderId}</dd></div>
        <div className="flex justify-between gap-3"><dt>주문 상품</dt><dd>{o.orderName}</dd></div>
        <div className="flex justify-between gap-3"><dt>결제 금액</dt><dd className="num">{won(o.amount)}</dd></div>
        <div className="flex justify-between gap-3"><dt>픽업</dt><dd className="num">{pickupLabel(o.pickupDate, o.pickupTime)}</dd></div>
        {o.recipientName && <div className="flex justify-between gap-3"><dt>받는 분</dt><dd>{o.recipientName}</dd></div>}
      </dl>
      <p className="lead">픽업 시간에 매장 냉장고에서 찾아가 주세요. 주문 번호를 캡처해 두시면 편해요.</p>
      <Link href="/" className="btn">처음 화면으로</Link>
    </Shell>
  );
}

export function PaymentFailed() {
  const params = useSearchParams();
  const code = params.get("code");
  const message = params.get("message");
  return (
    <Shell hand="결제를 마치지 못했어요" title={code === "PAY_PROCESS_CANCELED" ? "결제를 취소했어요" : "결제가 완료되지 않았어요"}>
      {message && code !== "PAY_PROCESS_CANCELED" && <p className="lead" role="alert">{message}</p>}
      <p className="text-[.9rem] text-muted">담아 두신 상품은 그대로 있어요. 돈은 빠져나가지 않았습니다.</p>
      <Link href="/checkout" className="btn btn-primary">주문 화면으로 돌아가기</Link>
    </Shell>
  );
}
