import type { Metadata, Viewport } from "next";
import { Nanum_Pen_Script, Noto_Serif_KR } from "next/font/google";
import { CartProvider } from "@/components/cart";
import { SiteFooter, SiteHeader } from "@/components/site-chrome";
import { ToastProvider } from "@/components/toast";
import { OpeningBanner } from "@/components/opening-notice";
import { ChatWidget } from "@/components/chat-widget";
import { IS_INDEXABLE, ORDERING_OPEN, SITE_URL, absoluteUrl, jsonLd } from "@/lib/site";
import "./globals.css";

// 한글 웹 글꼴은 무거워서 제목(명조 900)과 손글씨만 내려받는다.
// 본문은 기기에 깔린 한글 글꼴(iOS·맥 Apple SD Gothic Neo, 윈도우 맑은 고딕, 안드로이드 Noto Sans CJK)을 쓴다.
const serif = Noto_Serif_KR({ variable: "--font-noto-serif", weight: "900", preload: false, display: "swap" });
const pen = Nanum_Pen_Script({ variable: "--font-pen", weight: "400", preload: false, display: "swap" });


export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: { default: "온담찬 · 양주 무인 반찬가게", template: "%s · 온담찬" },
  description: "매일 아침 만든 1~2인분 집밥 반찬을 미리 결제하고 퇴근길에 찾아가세요. 부모님께 보내는 어르신 밥상도 있어요.",
  robots: IS_INDEXABLE ? undefined : { index: false, follow: false },
  openGraph: { type: "website", locale: "ko_KR", siteName: "온담찬", title: "온담찬 · 매일의 식사에 온기를 담다", description: "양주 무인 반찬가게. 미리 결제하고 퇴근길에 찾아가세요." },
};

// 가게 정보(검색엔진·지도용). 주소·전화가 정해지면 address, telephone을 채운다.
const STORE_LD = {
  "@context": "https://schema.org",
  "@type": "FoodEstablishment",
  name: "온담찬",
  description: "매일 아침 만든 1~2인분 집밥 반찬을 미리 결제하고 찾아가는 양주 무인 반찬가게",
  url: SITE_URL,
  logo: absoluteUrl("/brand/logo.svg"),
  image: absoluteUrl("/opengraph-image.png"),
  servesCuisine: "한식 반찬",
  priceRange: "₩3,000~₩14,000",
  areaServed: "경기도 양주시",
  address: { "@type": "PostalAddress", addressLocality: "양주시", addressRegion: "경기도", addressCountry: "KR" },
  openingHoursSpecification: [{ "@type": "OpeningHoursSpecification", dayOfWeek: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], opens: "06:00", closes: "23:00" }],
};

export const viewport: Viewport = { themeColor: "#FBF6EC", viewportFit: "cover" };

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="ko" className={`${serif.variable} ${pen.variable} antialiased`} suppressHydrationWarning>
      <head>
        {/* 큰 글씨 설정을 첫 화면 전에 적용(깜빡임 방지) */}
        <script dangerouslySetInnerHTML={{ __html: `try{if(localStorage.getItem("ondamchan-bigtext")==="1")document.documentElement.classList.add("big")}catch(e){}` }} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: jsonLd(STORE_LD) }} />
      </head>
      <body className="flex min-h-dvh flex-col">
        <CartProvider>
          <ToastProvider>
            <a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:left-3 focus:top-3 focus:z-50 focus:rounded focus:bg-white focus:px-3 focus:py-2">본문 바로가기</a>
            {!ORDERING_OPEN && <OpeningBanner />}
            <SiteHeader />
            <main id="main" className="flex-1">{children}</main>
            <SiteFooter />
            <ChatWidget />
          </ToastProvider>
        </CartProvider>
      </body>
    </html>
  );
}
