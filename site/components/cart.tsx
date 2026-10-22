"use client";
// 장바구니 + 고른 픽업 시간. 브라우저(localStorage)에만 저장하고, 결제 금액은 서버가 다시 계산한다.
import { cartStore, useHydrated, useStore, type Pickup } from "@/lib/browser-store";
import { MAX_QTY } from "@/lib/price";

export type { Pickup };

const clampQty = (q: number) => Math.max(0, Math.min(MAX_QTY, Math.round(q)));

const actions = {
  add: (slug: string, qty = 1) => cartStore.set((s) => {
    const cur = s.items.find((i) => i.slug === slug)?.qty ?? 0;
    const next = clampQty(cur + qty);
    return { ...s, items: cur ? s.items.map((i) => (i.slug === slug ? { slug, qty: next } : i)) : [...s.items, { slug, qty: next }] };
  }),
  setQty: (slug: string, qty: number) => cartStore.set((s) => {
    const q = clampQty(qty);
    return { ...s, items: q ? s.items.map((i) => (i.slug === slug ? { slug, qty: q } : i)) : s.items.filter((i) => i.slug !== slug) };
  }),
  remove: (slug: string) => cartStore.set((s) => ({ ...s, items: s.items.filter((i) => i.slug !== slug) })),
  setPickup: (pickup: Pickup) => cartStore.set((s) => ({ ...s, pickup })),
  clear: () => cartStore.set({ items: [], pickup: null }),
};

export function useCart() {
  const state = useStore(cartStore);
  const ready = useHydrated();
  return { ...state, ...actions, ready, count: state.items.reduce((n, i) => n + i.qty, 0) };
}

/** 예전 구조와의 호환용 감싸개 (상태는 cartStore가 가진다) */
export function CartProvider({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}
