"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { bigTextStore, useStore } from "@/lib/browser-store";
import { useCart } from "./cart";

const NAV = [
  { href: "/menu", label: "메뉴" },
  { href: "/silver", label: "어르신 밥상" },
  { href: "/about", label: "가게 이야기" },
];

export function NavLinks() {
  const path = usePathname();
  return (
    <nav aria-label="사이트 메뉴" className="order-3 -mx-1 flex basis-full gap-1 overflow-x-auto md:order-none md:ml-auto md:basis-auto">
      {NAV.map((n) => {
        const on = path === n.href || path.startsWith(n.href + "/");
        return (
          <Link key={n.href} href={n.href} aria-current={on ? "page" : undefined}
            className={`whitespace-nowrap rounded-lg px-2.5 py-1.5 text-[.82rem] md:text-[.85rem] ${on ? "bg-sand font-bold text-ink" : "text-muted hover:text-ink"}`}>
            {n.label}
          </Link>
        );
      })}
    </nav>
  );
}

export function BigTextToggle() {
  const on = useStore(bigTextStore);
  return (
    <button type="button" onClick={() => bigTextStore.set(!on)} aria-pressed={on} className="whitespace-nowrap rounded-lg border border-line bg-white px-2.5 py-1 text-[.78rem]">
      {on ? "기본 글씨" : "큰 글씨"}
    </button>
  );
}

export function CartButton() {
  const { count, ready } = useCart();
  return (
    <Link href="/checkout" className="whitespace-nowrap rounded-lg border border-line bg-white px-2.5 py-1 text-[.78rem]">
      담은 상품 <b className="num text-accent-deep">{ready ? count : 0}</b>
    </Link>
  );
}
