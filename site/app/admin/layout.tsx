import type { Metadata, Viewport } from "next";
import { Noto_Serif_KR } from "next/font/google";
import "../globals.css";

// 관리자 화면은 한국어만. 손님 화면(app/[lang])과 따로 둔 루트 레이아웃이다.
const serif = Noto_Serif_KR({ variable: "--font-noto-serif", weight: "900", preload: false, display: "swap" });

export const metadata: Metadata = { title: { default: "관리자 · 온담찬", template: "%s · 온담찬" }, robots: { index: false, follow: false } };
export const viewport: Viewport = { themeColor: "#FBF6EC" };

export default function AdminLayout({ children }: LayoutProps<"/admin">) {
  return (
    <html lang="ko" className={`${serif.variable} antialiased`}>
      <body className="min-h-dvh">{children}</body>
    </html>
  );
}
