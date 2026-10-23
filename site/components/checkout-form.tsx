"use client";
import Link from "next/link";
import { useState } from "react";
import { MAX_QTY, priceCart, type PricedProduct } from "@/lib/price";
import { isTestMode } from "@/lib/toss-client";
import { useCart } from "./cart";
import { useHref, useT } from "./lang";
import { PaymentWidgetSlot, usePaymentWidgets } from "./payment-widget";
import { PickupPicker, useEffectivePickup } from "./pickup-picker";
import { useToast } from "./toast";

const PHONE = /^01[016789]-?\d{3,4}-?\d{4}$/;

type OrderCreated = { orderId: string; orderName: string; amount: number; customerName: string; customerMobilePhone: string };

/** 주문 화면. 여기 합계는 안내용이고, 결제 금액은 서버(/api/orders)가 DB 가격으로 다시 계산한 값을 쓴다. */
export function CheckoutForm({ products }: { products: PricedProduct[] }) {
  const cart = useCart();
  const toast = useToast();
  const all = useT();
  const t = all.checkout;
  const won = all.money;
  const href = useHref();
  const { pickup } = useEffectivePickup();
  const [forOther, setForOther] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [busy, setBusy] = useState(false);
  const priced = cart.items.length ? priceCart(cart.items, products) : null;
  const total = priced?.ok ? priced.total : 0;
  const { widgets, status } = usePaymentWidgets(total);
  const bySlug = new Map(products.map((p) => [p.slug, p]));

  async function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (busy) return;
    const f = new FormData(e.currentTarget);
    const val = (k: string) => String(f.get(k) ?? "").trim();
    const err: Record<string, string> = {};
    if (!val("name")) err.name = t.errName;
    if (!PHONE.test(val("tel"))) err.tel = t.errTel;
    if (forOther) {
      if (!val("rname")) err.rname = t.errRname;
      if (!PHONE.test(val("rtel"))) err.rtel = t.errRtel;
    }
    if (!f.get("agree")) err.agree = t.errAgree;
    setErrors(err);
    if (!cart.items.length) return toast(t.toastEmpty);
    if (Object.keys(err).length) return toast(t.toastMissing);
    if (!pickup?.time) return toast(t.toastPickup);
    if (!widgets || status !== "ready") return toast(t.toastWidget);

    setBusy(true);
    try {
      const res = await fetch("/api/orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          items: cart.items,
          customer: { name: val("name"), phone: val("tel") },
          recipient: forOther ? { name: val("rname"), phone: val("rtel") } : null,
          pickup,
          agree: true,
        }),
      });
      const data = (await res.json().catch(() => ({}))) as Partial<OrderCreated> & { error?: string };
      if (!res.ok || !data.orderId) {
        setBusy(false);
        return toast(all.orderErrors[data.error ?? ""] ?? all.orderErrors.SERVER);
      }
      const order = data as OrderCreated;
      // 서버가 계산한 금액으로 결제한다(화면 금액과 다르면 여기서 맞춰진다)
      await widgets.setAmount({ currency: "KRW", value: order.amount });
      await widgets.requestPayment({
        orderId: order.orderId,
        orderName: order.orderName,
        customerName: order.customerName,
        customerMobilePhone: order.customerMobilePhone,
        successUrl: `${location.origin}${href("/checkout/success")}`,
        failUrl: `${location.origin}${href("/checkout/fail")}`,
      });
    } catch (error) {
      // 결제창을 닫았거나(USER_CANCEL) 위젯 약관 미동의 등. 토스가 주는 문구는 한국어다
      setBusy(false);
      const { code, message } = (error ?? {}) as { code?: string; message?: string };
      toast(code === "USER_CANCEL" ? t.toastCanceled : (message ?? t.toastStartFail));
    }
  }

  const err = (k: string) => (errors[k] ? <span className="text-[.8rem] font-bold text-accent-deep">{errors[k]}</span> : null);

  return (
    <form onSubmit={submit} noValidate className="grid gap-5 pb-18 md:grid-cols-[1fr_360px] md:items-start">
      <div className="grid min-w-0 gap-4">
        <div className="card grid gap-3.5 p-5">
          <h2 className="text-[1.15rem] font-extrabold">{t.pickupBox}</h2>
          <PickupPicker />
        </div>
        <div className="card grid gap-3.5 p-5">
          <h2 className="text-[1.15rem] font-extrabold">{t.customerBox}</h2>
          <label className="grid gap-1.5"><span className="text-[.85rem] font-bold">{t.name}</span><input name="name" autoComplete="name" className="field-input" placeholder={t.namePlaceholder} aria-invalid={Boolean(errors.name)} />{err("name")}</label>
          <label className="grid gap-1.5"><span className="text-[.85rem] font-bold">{t.phone}</span><input name="tel" type="tel" inputMode="tel" autoComplete="tel" className="field-input" placeholder="010-0000-0000" aria-invalid={Boolean(errors.tel)} />{err("tel")}</label>
          <label className="flex items-start gap-2.5 text-[.92rem]">
            <input type="checkbox" checked={forOther} onChange={(e) => setForOther(e.target.checked)} className="mt-1 size-[22px] shrink-0 accent-[var(--brand)]" />
            <span><b>{t.forOtherStrong}</b>{t.forOther}</span>
          </label>
          {forOther && (
            <div className="grid gap-3">
              <label className="grid gap-1.5"><span className="text-[.85rem] font-bold">{t.rname}</span><input name="rname" className="field-input" placeholder={t.rnamePlaceholder} />{err("rname")}</label>
              <label className="grid gap-1.5"><span className="text-[.85rem] font-bold">{t.rphone}</span><input name="rtel" type="tel" inputMode="tel" className="field-input" placeholder="010-0000-0000" />{err("rtel")}</label>
            </div>
          )}
          <p className="rounded-[10px] bg-[var(--soft)] px-3 py-2.5 text-[.82rem] text-muted">{t.pickupOnly}</p>
        </div>
        <div className="card grid gap-3.5 p-5">
          <h2 className="text-[1.15rem] font-extrabold">{t.payBox}</h2>
          <PaymentWidgetSlot status={status} hasItems={total > 0} />
          <label className="flex items-start gap-2.5 text-[.92rem]">
            <input type="checkbox" name="agree" className="mt-1 size-[22px] shrink-0 accent-[var(--brand)]" />
            <span>{t.agreeBefore}<Link href={href("/policy/refund")} className="underline underline-offset-4">{t.agreeLink}</Link>{t.agreeAfter}</span>
          </label>
          {err("agree")}
          {t.payNotice && <p className="text-[.8rem] text-muted">{t.payNotice}</p>}
        </div>
      </div>

      <aside className="card sticky top-24 grid gap-3 p-5" aria-label={t.summary}>
        <h2 className="text-[1.15rem] font-extrabold">{t.summary}</h2>
        {!cart.ready ? null : cart.items.length === 0 ? (
          <p className="text-[.9rem] text-muted">{t.empty}<Link href={href("/menu")} className="font-bold text-brand underline underline-offset-4">{t.goMenu}</Link></p>
        ) : (
          <ul className="grid gap-2.5">
            {cart.items.map((i) => {
              const p = bySlug.get(i.slug);
              if (!p) return null;
              return (
                <li key={i.slug} className="grid gap-1.5 border-b border-line pb-2.5 text-[.92rem]">
                  <div className="flex justify-between gap-2"><span>{p.name}</span><span className="num">{won(p.price * i.qty)}</span></div>
                  <div className="flex items-center gap-1.5">
                    <button type="button" className="size-8 rounded-lg border border-line" aria-label={t.less(p.name)} onClick={() => cart.setQty(i.slug, i.qty - 1)}>−</button>
                    <span className="num min-w-6 text-center">{i.qty}</span>
                    <button type="button" className="size-8 rounded-lg border border-line" aria-label={t.more(p.name)} disabled={i.qty >= MAX_QTY} onClick={() => cart.setQty(i.slug, i.qty + 1)}>+</button>
                    <button type="button" className="ml-auto text-[.8rem] text-muted underline" onClick={() => cart.remove(i.slug)}>{t.remove}</button>
                  </div>
                </li>
              );
            })}
          </ul>
        )}
        <div className="flex justify-between text-[1.1rem] font-extrabold"><span>{t.amount}</span><span className="num">{won(total)}</span></div>
        <button type="submit" className="btn btn-primary w-full" disabled={busy} aria-busy={busy}>{busy ? t.opening : total ? t.payAmount(won(total)) : t.pay}</button>
        {isTestMode && <p className="staged">{t.testMode}</p>}
      </aside>
    </form>
  );
}
