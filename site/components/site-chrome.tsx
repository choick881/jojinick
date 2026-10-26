import Image from "next/image";
import Link from "next/link";
import { localePath } from "@/lib/i18n";
import { getLang, getT } from "@/lib/i18n/server";
import { BigTextToggle, CartButton, LangSwitch, NavLinks } from "./header-tools";

export async function SiteHeader() {
  const lang = await getLang();
  const t = await getT();
  return (
    <header className="gut sticky top-0 z-30 border-b border-line bg-paper/95 backdrop-blur" style={{ top: "env(safe-area-inset-top, 0px)" }}>
      <div className="wrap flex flex-wrap items-center gap-x-3.5 gap-y-1 py-2.5">
        <Link href={localePath(lang, "/")} aria-label={t.nav.home} className="shrink-0">
          <Image src="/brand/logo-horizontal.svg" alt={t.common.siteName} width={106} height={32} priority className="h-8 w-auto" />
        </Link>
        <NavLinks />
        <div className="ml-auto flex items-center gap-1.5 md:ml-2">
          <LangSwitch />
          <BigTextToggle />
          <CartButton />
        </div>
      </div>
    </header>
  );
}

export async function SiteFooter() {
  const lang = await getLang();
  const t = await getT();
  return (
    <footer className="gut bg-ink pb-28 pt-8 text-[.78rem] text-[#CDBEAB] md:pb-10">
      <div className="wrap grid gap-1">
        <b className="font-serif text-base font-black text-paper">{t.common.siteName}</b>
        <span>{t.footer.owner}</span>
        <span>{t.footer.address}</span>
        <span className="flex flex-wrap gap-x-3">
          <Link href={localePath(lang, "/policy/terms")} className="underline underline-offset-4">{t.footer.terms}</Link>
          <Link href={localePath(lang, "/policy/refund")} className="underline underline-offset-4">{t.footer.refund}</Link>
          <span>{t.footer.privacy}</span>
        </span>
      </div>
    </footer>
  );
}
