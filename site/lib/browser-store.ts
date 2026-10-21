"use client";
// 브라우저 전용 상태(장바구니, 큰 글씨, 현재 시각)를 useSyncExternalStore로 구독하기 위한 작은 저장소들.
// 서버 렌더에서는 기본값을 쓰고, 브라우저에서 hydration 뒤에 실제 값으로 바뀐다.
import { useSyncExternalStore } from "react";
import type { CartItem } from "./price";

export type Pickup = { date: string; time: string } | null;
export type CartState = { items: CartItem[]; pickup: Pickup };

function createStore<T>(initial: T, load: () => T | null, save: (v: T) => void) {
  let value = initial;
  let loaded = false;
  const listeners = new Set<() => void>();
  return {
    get(): T {
      if (!loaded && typeof window !== "undefined") {
        loaded = true;
        value = load() ?? initial;
      }
      return value;
    },
    set(next: T | ((v: T) => T)) {
      value = typeof next === "function" ? (next as (v: T) => T)(this.get()) : next;
      save(value);
      listeners.forEach((l) => l());
    },
    subscribe(l: () => void) {
      listeners.add(l);
      return () => listeners.delete(l);
    },
    initial,
  };
}

const CART_KEY = "ondamchan-cart-v1";
const EMPTY: CartState = { items: [], pickup: null };
export const cartStore = createStore<CartState>(
  EMPTY,
  () => {
    try {
      const v = JSON.parse(localStorage.getItem(CART_KEY) ?? "null");
      return v && Array.isArray(v.items) ? { items: v.items, pickup: v.pickup ?? null } : null;
    } catch { return null; }
  },
  (v) => { try { localStorage.setItem(CART_KEY, JSON.stringify(v)); } catch {} },
);

export const BIG_KEY = "ondamchan-bigtext";
export const bigTextStore = createStore<boolean>(
  false,
  () => document.documentElement.classList.contains("big"),
  (on) => {
    document.documentElement.classList.toggle("big", on);
    try { localStorage.setItem(BIG_KEY, on ? "1" : "0"); } catch {}
  },
);

export function useStore<T>(store: { get: () => T; subscribe: (l: () => void) => () => void; initial: T }): T {
  return useSyncExternalStore(store.subscribe.bind(store), store.get.bind(store), () => store.initial);
}

/** hydration이 끝났는지 (서버: false, 브라우저: true) */
const noop = () => () => {};
export function useHydrated(): boolean {
  return useSyncExternalStore(noop, () => true, () => false);
}

/** 1분마다 바뀌는 현재 시각(분 단위). 서버에서는 null. */
const clockListeners = new Set<() => void>();
let timer: number | undefined;
function subscribeClock(l: () => void) {
  clockListeners.add(l);
  if (timer === undefined) timer = window.setInterval(() => clockListeners.forEach((x) => x()), 30_000);
  return () => {
    clockListeners.delete(l);
    if (!clockListeners.size) { window.clearInterval(timer); timer = undefined; }
  };
}
export function useMinute(): number | null {
  return useSyncExternalStore(subscribeClock, () => Math.floor(Date.now() / 60_000), () => null);
}
