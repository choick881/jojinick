"use client";
import Link from "next/link";
import { useState } from "react";
import { MAX_QTY, won } from "@/lib/price";
import { useCart } from "./cart";
import { PickupPicker } from "./pickup-picker";
import { useToast } from "./toast";

type Props = { slug: string; name: string; price: number; soldOut?: boolean };

/** 상세페이지 구매 영역 + 모바일 하단 고정 구매 바 */
export function BuyBox({ slug, name, price, soldOut }: Props) {
  const [qty, setQty] = useState(1);
  const { add } = useCart();
  const toast = useToast();
  const put = () => { add(slug, qty); toast(`${name} ${qty}개를 담았어요`); };

  return (
    <>
      <PickupPicker />
      <div className="grid gap-2">
        <span className="text-[.85rem] font-bold">수량</span>
        <div className="inline-flex w-max items-center rounded-[10px] border-[1.5px] border-line bg-white">
          <button type="button" className="size-12 text-[1.2rem]" aria-label="수량 줄이기" onClick={() => setQty((q) => Math.max(1, q - 1))}>−</button>
          <output className="num min-w-[2.2em] text-center font-bold" aria-live="polite">{qty}</output>
          <button type="button" className="size-12 text-[1.2rem]" aria-label="수량 늘리기" onClick={() => setQty((q) => Math.min(MAX_QTY, q + 1))}>+</button>
        </div>
      </div>
      <div className="flex items-baseline justify-between border-t border-line pt-3.5">
        <span>합계</span><b className="num text-[1.3rem]">{won(price * qty)}</b>
      </div>
      <div className="grid gap-2 sm:grid-cols-[1fr_auto]">
        <Link href="/checkout" onClick={put} aria-disabled={soldOut} className={`btn btn-primary ${soldOut ? "pointer-events-none !bg-[#C9B9A6]" : ""}`}>
          {soldOut ? "오늘은 품절이에요" : "미리 결제하기"}
        </Link>
        <button type="button" className="btn btn-ghost" disabled={soldOut} onClick={put}>담기</button>
      </div>

      <div className="fixed inset-x-0 bottom-0 z-20 flex items-center gap-3 border-t border-line bg-white shadow-[0_-6px_20px_rgba(43,33,26,.08)] md:hidden"
        style={{ padding: "10px max(16px, env(safe-area-inset-right, 0px)) calc(10px + env(safe-area-inset-bottom, 0px)) max(16px, env(safe-area-inset-left, 0px))" }}>
        <div className="grid leading-tight">
          <small className="text-[.72rem] text-muted">{name} × <span className="num">{qty}</span></small>
          <b className="num text-[1.05rem]">{won(price * qty)}</b>
        </div>
        <Link href="/checkout" onClick={put} aria-disabled={soldOut} className={`btn btn-primary min-h-[50px] flex-1 ${soldOut ? "pointer-events-none !bg-[#C9B9A6]" : ""}`}>
          {soldOut ? "품절" : "미리 결제하기"}
        </Link>
      </div>
    </>
  );
}
