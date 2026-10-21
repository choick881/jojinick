import Image from "next/image";
import Link from "next/link";
import { BigTextToggle, CartButton, NavLinks } from "./header-tools";

export function SiteHeader() {
  return (
    <header className="gut sticky top-0 z-30 border-b border-line bg-paper/95 backdrop-blur" style={{ top: "env(safe-area-inset-top, 0px)" }}>
      <div className="wrap flex flex-wrap items-center gap-x-3.5 gap-y-1 py-2.5">
        <Link href="/" aria-label="온담찬 홈" className="shrink-0">
          <Image src="/brand/logo-horizontal.svg" alt="온담찬" width={106} height={32} priority className="h-8 w-auto" />
        </Link>
        <NavLinks />
        <div className="ml-auto flex items-center gap-1.5 md:ml-2">
          <BigTextToggle />
          <CartButton />
        </div>
      </div>
    </header>
  );
}

export function SiteFooter() {
  return (
    <footer className="gut bg-ink pb-28 pt-8 text-[.78rem] text-[#CDBEAB] md:pb-10">
      <div className="wrap grid gap-1">
        <b className="font-serif text-base text-paper">온담찬</b>
        <span>대표 ○○○ · 사업자등록번호 준비 중 · 통신판매업 신고번호 준비 중</span>
        <span>경기도 양주시 (주소 준비 중) · 무인 판매 06:00~23:00 · 픽업 17:30~20:30</span>
        <span className="flex flex-wrap gap-x-3">
          <Link href="/policy/terms" className="underline underline-offset-4">이용약관</Link>
          <Link href="/policy/refund" className="underline underline-offset-4">환불 정책</Link>
          <span>개인정보 처리방침(준비 중)</span>
        </span>
      </div>
    </footer>
  );
}
