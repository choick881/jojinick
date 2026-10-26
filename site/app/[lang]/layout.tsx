import type { Metadata, Viewport } from "next";
import { Nanum_Pen_Script, Noto_Serif_KR } from "next/font/google";
import { notFound } from "next/navigation";
import { CartProvider } from "@/components/cart";
import { ChatWidget } from "@/components/chat-widget";
import { LangProvider } from "@/components/lang";
import { OpeningBanner } from "@/components/opening-notice";
import { SiteFooter, SiteHeader } from "@/components/site-chrome";
import { ToastProvider } from "@/components/toast";
import { LOCALES, alternates, getDict, hasLocale } from "@/lib/i18n";
import { IS_INDEXABLE, ORDERING_OPEN, SITE_URL, absoluteUrl, jsonLd } from "@/lib/site";
import "../globals.css";

// 한글 웹 글꼴은 무거워서 제목(명조 900)과 손글씨만 내려받는다.
// 본문은 기기에 깔린 한글 글꼴(iOS·맥 Apple SD Gothic Neo, 윈도우 맑은 고딕, 안드로이드 Noto Sans CJK)을 쓴다.
const serif = Noto_Serif_KR({ variable: "--font-noto-serif", weight: "900", preload: false, display: "swap" });
const pen = Nanum_Pen_Script({ variable: "--font-pen", weight: "400", preload: false, display: "swap" });

/** 한국어(/…)와 영어(/en/…) 두 벌을 미리 만든다 */
export function generateStaticParams() {
  return LOCALES.map((lang) => ({ lang }));
}

export async function generateMetadata({ params }: LayoutProps<"/[lang]">): Promise<Metadata> {
  const { lang } = await params;
  if (!hasLocale(lang)) return {};
  const t = getDict(lang).meta;
  return {
    metadataBase: new URL(SITE_URL),
    title: { default: t.title, template: t.template },
    description: t.description,
    robots: IS_INDEXABLE ? undefined : { index: false, follow: false },
    alternates: alternates(lang, "/"),
    openGraph: { type: "website", locale: t.ogLocale, siteName: getDict(lang).common.siteName, title: t.ogTitle, description: t.ogDescription },
  };
}

export const viewport: Viewport = { themeColor: "#FBF6EC", viewportFit: "cover" };

export default async function RootLayout({ children, params }: LayoutProps<"/[lang]">) {
  const { lang } = await params;
  if (!hasLocale(lang)) notFound();
  const t = getDict(lang);

  // 가게 정보(검색엔진·지도용). 주소·전화가 정해지면 address, telephone을 채운다.
  const storeLd = {
    "@context": "https://schema.org",
    "@type": "FoodEstablishment",
    name: t.common.siteName,
    description: t.meta.storeDescription,
    url: absoluteUrl(lang === "en" ? "/en" : "/"),
    logo: absoluteUrl("/brand/logo.svg"),
    image: absoluteUrl("/opengraph-image.png"),
    servesCuisine: t.meta.cuisine,
    priceRange: "₩3,000~₩14,000",
    areaServed: lang === "en" ? "Yangju-si, Gyeonggi-do" : "경기도 양주시",
    address: { "@type": "PostalAddress", addressLocality: lang === "en" ? "Yangju-si" : "양주시", addressRegion: lang === "en" ? "Gyeonggi-do" : "경기도", addressCountry: "KR" },
    openingHoursSpecification: [{ "@type": "OpeningHoursSpecification", dayOfWeek: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], opens: "06:00", closes: "23:00" }],
  };

  return (
    <html lang={lang} className={`${serif.variable} ${pen.variable} antialiased`} suppressHydrationWarning>
      <head>
        {/* 큰 글씨 설정을 첫 화면 전에 적용(깜빡임 방지) */}
        <script dangerouslySetInnerHTML={{ __html: `try{if(localStorage.getItem("ondamchan-bigtext")==="1")document.documentElement.classList.add("big")}catch(e){}` }} />
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: jsonLd(storeLd) }} />
      </head>
      <body className="flex min-h-dvh flex-col">
        <LangProvider lang={lang}>
          <CartProvider>
            <ToastProvider>
              <a href="#main" className="sr-only focus:not-sr-only focus:fixed focus:left-3 focus:top-3 focus:z-50 focus:rounded focus:bg-white focus:px-3 focus:py-2">{t.common.skipToContent}</a>
              {!ORDERING_OPEN && <OpeningBanner />}
              <SiteHeader />
              <main id="main" className="flex-1">{children}</main>
              <SiteFooter />
              <ChatWidget />
            </ToastProvider>
          </CartProvider>
        </LangProvider>
      </body>
    </html>
  );
}
