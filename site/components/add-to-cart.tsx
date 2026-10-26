"use client";
import { useCart } from "./cart";
import { useT } from "./lang";
import { useToast } from "./toast";

export function AddToCart({ slug, name, soldOut, className = "" }: { slug: string; name: string; soldOut?: boolean; className?: string }) {
  const { add } = useCart();
  const toast = useToast();
  const t = useT().card;
  return (
    <button type="button" disabled={soldOut} aria-label={t.addLabel(name)}
      onClick={() => { add(slug); toast(t.added(name)); }}
      className={`min-h-10 min-w-[52px] rounded-[10px] border-[1.5px] border-brand bg-white px-2 text-[.8rem] font-bold text-brand disabled:cursor-not-allowed disabled:border-line disabled:text-[#B3A796] ${className}`}>
      {soldOut ? t.soldOut : t.add}
    </button>
  );
}
