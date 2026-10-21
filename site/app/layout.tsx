import type { Metadata, Viewport } from "next";
import { Nanum_Pen_Script, Noto_Sans_KR, Noto_Serif_KR } from "next/font/google";
import { CartProvider } from "@/components/cart";
import { SiteFooter, SiteHeader } from "@/components/site-chrome";
import { ToastProvider } from "@/components/toast";
import "./globals.css";

// 한글 글꼴은 글자 수가 많아 미리 불러오지 않고(preload: false) 필요한 조각만 내려받는다.
const sans = Noto_Sans_KR({ variable: "--font-noto-sans", weight: ["400", "500", "700", "800"], preload: false, display: "swap" });
const serif = Noto_Serif_KR({ variable: "--font-noto-serif", weight: ["700", "900"], preload: false, display: "swap" });
const pen = Nanum_Pen_Script({ variable: "--font-pen", weight: "400", preload: false, display: "swap" });

const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: { default: "온담찬 · 양주 무인 반찬가게", template: "%s · 온담찬" },
  description: "매일 아침 만든 1~2인분 집밥 반찬을 미리 결제하고 퇴근길에 찾아가세요. 부모님께 보내는 어르신 밥상도 있어요.",
  openGraph: { type: "website", locale: "ko_KR", siteName: "온담찬", title: "온담찬 · 매일의 식사에 온기를 담다", description: "양주 무인 반찬가게. 미리 결제하고 퇴근길에 찾아가세요." },
};

export const viewport: Viewport = { themeColor: "#FBF6EC", viewportFit: "cover" };

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="ko" className={`${sans.variable} ${serif.variable} ${pen.variable} antialiased`} suppressHydrationWarning>
      <head>
        {/* 큰 글씨 설정을 첫 화면 전에 적용(깜빡임 방지) */}
        <script dangerouslySetInnerHTML={{ __html: `try{if(localStorage.getItem("ondamchan-bigtext")==="1")document.documentElement.classList.add("big")}catch(e){}` }} />
      </head>
      <body className="flex min-h-dvh flex-col">
        <CartProvider>
          <ToastProvider>
            <a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:left-3 focus:top-3 focus:z-50 focus:rounded focus:bg-white focus:px-3 focus:py-2">본문 바로가기</a>
            <SiteHeader />
            <main id="main" className="flex-1">{children}</main>
            <SiteFooter />
          </ToastProvider>
        </CartProvider>
      </body>
    </html>
  );
}
