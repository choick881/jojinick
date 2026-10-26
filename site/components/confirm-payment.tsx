"use client";
// 토스 결제창이 돌려보낸 화면. 성공이면 서버에 승인을 요청하고(금액 대조는 서버가 한다), 실패면 이유를 보여 준다.
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";
import type { Dict } from "@/lib/i18n";
import { useCart } from "./cart";
import { useHref, useT } from "./lang";

type Paid = { orderId: string; orderName: string; amount: number; pickupDate: string; pickupTime: string; recipientName: string | null };
type State = { kind: "checking" } | { kind: "paid"; order: Paid } | { kind: "error"; message: string };

function pickupLabel(t: Dict["pickup"], date: string, time: string) {
  const weekday = t.weekdays[new Date(`${date}T00:00:00Z`).getUTCDay()];
  return t.full(Number(date.slice(5, 7)), Number(date.slice(8, 10)), weekday, time.slice(0, 5));
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
  const all = useT();
  const t = all.confirm;
  const href = useHref();
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
      queueMicrotask(() => setState({ kind: "error", message: t.noInfo }));
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
          setState({ kind: "error", message: t.errors[data.error ?? ""] ?? data.message ?? t.failedGeneric });
        }
      })
      .catch(() => setState({ kind: "error", message: t.network }));
  }, [paymentKey, orderId, amount, clear, t]);

  if (state.kind === "checking") return <p className="lead text-center" aria-live="polite">{t.checking}</p>;
  if (state.kind === "error")
    return (
      <Shell hand={t.failHand} title={t.failTitle}>
        <p className="lead" role="alert">{state.message}</p>
        <Link href={href("/checkout")} className="btn btn-primary">{t.back}</Link>
      </Shell>
    );

  const o = state.order;
  return (
    <Shell hand={t.thanks} title={t.done}>
      <dl className="card grid w-full gap-2.5 p-5 text-left text-[.95rem] [&_dt]:text-muted [&_dd]:font-bold">
        <div className="flex justify-between gap-3"><dt>{t.orderNo}</dt><dd className="num">{o.orderId}</dd></div>
        <div className="flex justify-between gap-3"><dt>{t.items}</dt><dd>{o.orderName}</dd></div>
        <div className="flex justify-between gap-3"><dt>{t.amount}</dt><dd className="num">{all.money(o.amount)}</dd></div>
        <div className="flex justify-between gap-3"><dt>{t.pickup}</dt><dd className="num">{pickupLabel(all.pickup, o.pickupDate, o.pickupTime)}</dd></div>
        {o.recipientName && <div className="flex justify-between gap-3"><dt>{t.recipient}</dt><dd>{o.recipientName}</dd></div>}
      </dl>
      <p className="lead">{t.afterNote}</p>
      <Link href={href("/")} className="btn">{t.home}</Link>
    </Shell>
  );
}

export function PaymentFailed() {
  const params = useSearchParams();
  const t = useT().confirm;
  const href = useHref();
  const code = params.get("code");
  const message = params.get("message");
  return (
    <Shell hand={t.failHand} title={code === "PAY_PROCESS_CANCELED" ? t.canceledTitle : t.failTitle}>
      {message && code !== "PAY_PROCESS_CANCELED" && <p className="lead" role="alert">{message}</p>}
      <p className="text-[.9rem] text-muted">{t.keptNote}</p>
      <Link href={href("/checkout")} className="btn btn-primary">{t.back}</Link>
    </Shell>
  );
}
