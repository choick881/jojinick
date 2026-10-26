import type { Metadata } from "next";
import { CheckoutForm } from "@/components/checkout-form";
import { OpeningNotice } from "@/components/opening-notice";
import { getLocalizedCatalog } from "@/lib/catalog";
import { getDict, hasLocale } from "@/lib/i18n";
import { getLang, getT } from "@/lib/i18n/server";
import { ORDERING_OPEN } from "@/lib/site";

export async function generateMetadata({ params }: PageProps<"/[lang]/checkout">): Promise<Metadata> {
  const { lang } = await params;
  return { title: hasLocale(lang) ? getDict(lang).checkout.title : undefined, robots: { index: false } };
}

export default async function CheckoutPage() {
  if (!ORDERING_OPEN) return <section className="gut sec"><OpeningNotice /></section>;
  const lang = await getLang();
  const t = (await getT()).checkout;
  // 화면에 보일 상품 이름은 화면 언어로. 결제 금액은 서버가 DB 가격으로 다시 계산한다
  const products = (await getLocalizedCatalog(lang)).products.map(({ slug, name, price, soldOut }) => ({ slug, name, price, soldOut }));
  return (
    <section className="gut pt-9">
      <div className="wrap">
        <div className="mb-6 grid gap-2"><span className="eyebrow">{t.eyebrow}</span><h1 className="title text-[clamp(1.7rem,5vw,2.3rem)]">{t.h1a}<br className="md:hidden" />{t.h1b}</h1></div>
        <CheckoutForm products={products} />
      </div>
    </section>
  );
}
