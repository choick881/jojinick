"use client";
import Link from "next/link";
import { useState } from "react";
import { MAX_QTY, priceCart, won, type PricedProduct } from "@/lib/price";
import { useCart } from "./cart";
import { PickupPicker } from "./pickup-picker";
import { useToast } from "./toast";

const PHONE = /^01[016789]-?\d{3,4}-?\d{4}$/;

/** 주문 화면. 결제(토스)는 주문 DB 연결(Phase 3·4) 뒤에 열린다. 여기 합계는 안내용이고 결제 금액은 서버가 다시 계산한다. */
export function CheckoutForm({ products }: { products: PricedProduct[] }) {
  const cart = useCart();
  const toast = useToast();
  const [forOther, setForOther] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const priced = cart.items.length ? priceCart(cart.items, products) : null;
  const bySlug = new Map(products.map((p) => [p.slug, p]));

  function submit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    const err: Record<string, string> = {};
    if (!String(f.get("name") ?? "").trim()) err.name = "이름을 적어 주세요.";
    if (!PHONE.test(String(f.get("tel") ?? "").trim())) err.tel = "휴대폰 번호를 010-0000-0000 형식으로 적어 주세요.";
    if (forOther) {
      if (!String(f.get("rname") ?? "").trim()) err.rname = "받는 분 성함을 적어 주세요.";
      if (!PHONE.test(String(f.get("rtel") ?? "").trim())) err.rtel = "받는 분 휴대폰 번호를 적어 주세요.";
    }
    if (!f.get("agree")) err.agree = "환불 정책 확인에 체크해 주세요.";
    setErrors(err);
    if (!cart.items.length) return toast("먼저 메뉴를 담아 주세요");
    if (Object.keys(err).length) return toast("빠진 항목을 확인해 주세요");
    toast("결제는 주문 DB를 연결한 뒤 열립니다 (준비 중)");
  }

  const err = (k: string) => (errors[k] ? <span className="text-[.8rem] font-bold text-accent-deep">{errors[k]}</span> : null);

  return (
    <form onSubmit={submit} noValidate className="grid gap-5 pb-18 md:grid-cols-[1fr_360px] md:items-start">
      <div className="grid min-w-0 gap-4">
        <div className="card grid gap-3.5 p-5">
          <h2 className="text-[1.15rem] font-extrabold">픽업 날짜와 시간</h2>
          <PickupPicker />
        </div>
        <div className="card grid gap-3.5 p-5">
          <h2 className="text-[1.15rem] font-extrabold">주문하시는 분</h2>
          <label className="grid gap-1.5"><span className="text-[.85rem] font-bold">이름</span><input name="name" autoComplete="name" className="field-input" placeholder="홍길동" aria-invalid={Boolean(errors.name)} />{err("name")}</label>
          <label className="grid gap-1.5"><span className="text-[.85rem] font-bold">휴대폰 번호</span><input name="tel" type="tel" inputMode="tel" autoComplete="tel" className="field-input" placeholder="010-0000-0000" aria-invalid={Boolean(errors.tel)} />{err("tel")}</label>
          <label className="flex items-start gap-2.5 text-[.92rem]">
            <input type="checkbox" checked={forOther} onChange={(e) => setForOther(e.target.checked)} className="mt-1 size-[22px] shrink-0 accent-[var(--brand)]" />
            <span><b>받는 분이 다른가요?</b> 부모님이 대신 찾아가시면 체크해 주세요.</span>
          </label>
          {forOther && (
            <div className="grid gap-3">
              <label className="grid gap-1.5"><span className="text-[.85rem] font-bold">받는 분 성함</span><input name="rname" className="field-input" placeholder="부모님 성함" />{err("rname")}</label>
              <label className="grid gap-1.5"><span className="text-[.85rem] font-bold">받는 분 휴대폰</span><input name="rtel" type="tel" inputMode="tel" className="field-input" placeholder="010-0000-0000" />{err("rtel")}</label>
            </div>
          )}
          <p className="rounded-[10px] bg-[var(--soft)] px-3 py-2.5 text-[.82rem] text-muted">근거리 배달·택배는 준비 중입니다. 지금은 매장 픽업만 가능해요.</p>
        </div>
        <div className="card grid gap-3.5 p-5">
          <h2 className="text-[1.15rem] font-extrabold">결제 수단</h2>
          <div className="grid gap-1 rounded-[14px] border-2 border-dashed border-line p-5 text-center text-[.88rem] text-muted">
            <b className="text-brand">토스페이먼츠 결제위젯 자리</b>
            <span>주문 DB를 연결한 뒤 카드·간편결제·계좌이체 결제창이 이 자리에 열립니다.</span>
          </div>
          <label className="flex items-start gap-2.5 text-[.92rem]">
            <input type="checkbox" name="agree" className="mt-1 size-[22px] shrink-0 accent-[var(--brand)]" />
            <span>주문 내용과 <Link href="/policy/refund" className="underline underline-offset-4">환불 정책</Link>을 확인했어요.</span>
          </label>
          {err("agree")}
        </div>
      </div>

      <aside className="card sticky top-24 grid gap-3 p-5" aria-label="주문 요약">
        <h2 className="text-[1.15rem] font-extrabold">주문 요약</h2>
        {!cart.ready ? null : cart.items.length === 0 ? (
          <p className="text-[.9rem] text-muted">담은 상품이 없어요. <Link href="/menu" className="font-bold text-brand underline underline-offset-4">메뉴 보러 가기</Link></p>
        ) : (
          <ul className="grid gap-2.5">
            {cart.items.map((i) => {
              const p = bySlug.get(i.slug);
              if (!p) return null;
              return (
                <li key={i.slug} className="grid gap-1.5 border-b border-line pb-2.5 text-[.92rem]">
                  <div className="flex justify-between gap-2"><span>{p.name}</span><span className="num">{won(p.price * i.qty)}</span></div>
                  <div className="flex items-center gap-1.5">
                    <button type="button" className="size-8 rounded-lg border border-line" aria-label={`${p.name} 줄이기`} onClick={() => cart.setQty(i.slug, i.qty - 1)}>−</button>
                    <span className="num min-w-6 text-center">{i.qty}</span>
                    <button type="button" className="size-8 rounded-lg border border-line" aria-label={`${p.name} 늘리기`} disabled={i.qty >= MAX_QTY} onClick={() => cart.setQty(i.slug, i.qty + 1)}>+</button>
                    <button type="button" className="ml-auto text-[.8rem] text-muted underline" onClick={() => cart.remove(i.slug)}>빼기</button>
                  </div>
                </li>
              );
            })}
          </ul>
        )}
        <div className="flex justify-between text-[1.1rem] font-extrabold"><span>결제 금액</span><span className="num">{priced?.ok ? won(priced.total) : won(0)}</span></div>
        <button type="submit" className="btn btn-primary w-full">{priced?.ok ? `${won(priced.total)} 결제하기` : "결제하기"}</button>
        <p className="staged">결제 연결 준비 중입니다. 실제 결제는 일어나지 않습니다.</p>
      </aside>
    </form>
  );
}
