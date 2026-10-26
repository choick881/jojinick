"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { bigTextStore, useStore } from "@/lib/browser-store";
import { splitLocale, switchLocalePath } from "@/lib/i18n";
import { useCart } from "./cart";
import { useHref, useLang, useT } from "./lang";

export function NavLinks() {
  const t = useT().nav;
  const href = useHref();
  const path = splitLocale(usePathname()).path;
  const nav = [
    { path: "/menu", label: t.menu },
    { path: "/silver", label: t.silver },
    { path: "/about", label: t.about },
  ];
  return (
    <nav aria-label={t.label} className="order-3 -mx-1 flex basis-full gap-1 overflow-x-auto md:order-none md:ml-auto md:basis-auto">
      {nav.map((n) => {
        const on = path === n.path || path.startsWith(n.path + "/");
        return (
          <Link key={n.path} href={href(n.path)} aria-current={on ? "page" : undefined}
            className={`whitespace-nowrap rounded-lg px-2.5 py-1.5 text-[.82rem] md:text-[.85rem] ${on ? "bg-sand font-bold text-ink" : "text-muted hover:text-ink"}`}>
            {n.label}
          </Link>
        );
      })}
    </nav>
  );
}

/** 같은 화면을 다른 언어로(EN ↔ 한국어) */
export function LangSwitch() {
  const lang = useLang();
  const t = useT().nav;
  const pathname = usePathname();
  const to = lang === "ko" ? "en" : "ko";
  return (
    <Link href={switchLocalePath(pathname, to)} hrefLang={to} lang={to} aria-label={t.switchLabel} prefetch={false}
      className="whitespace-nowrap rounded-lg border border-line bg-white px-2.5 py-1 text-[.78rem] font-bold text-brand">
      {t.switchTo}
    </Link>
  );
}

export function BigTextToggle() {
  const on = useStore(bigTextStore);
  const t = useT().nav;
  return (
    <button type="button" onClick={() => bigTextStore.set(!on)} aria-pressed={on} className="whitespace-nowrap rounded-lg border border-line bg-white px-2.5 py-1 text-[.78rem]">
      {on ? t.normalText : t.bigText}
    </button>
  );
}

export function CartButton() {
  const { count, ready } = useCart();
  const t = useT().nav;
  const href = useHref();
  return (
    <Link href={href("/checkout")} className="whitespace-nowrap rounded-lg border border-line bg-white px-2.5 py-1 text-[.78rem]">
      {t.cart} <b className="num text-accent-deep">{ready ? count : 0}</b>
    </Link>
  );
}
