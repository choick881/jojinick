import type { Metadata } from "next";
import { CheckoutForm } from "@/components/checkout-form";
import { OpeningNotice } from "@/components/opening-notice";
import { getCatalog } from "@/lib/catalog";
import { ORDERING_OPEN } from "@/lib/site";

export const metadata: Metadata = { title: "주문하기", robots: { index: false } };

export default async function CheckoutPage() {
  if (!ORDERING_OPEN) return <section className="gut sec"><OpeningNotice /></section>;
  const products = (await getCatalog()).products.map(({ slug, name, price, soldOut }) => ({ slug, name, price, soldOut }));
  return (
    <section className="gut pt-9">
      <div className="wrap">
        <div className="mb-6 grid gap-2"><span className="eyebrow">주문하기</span><h1 className="title text-[clamp(1.7rem,5vw,2.3rem)]">미리 결제하고<br className="md:hidden" /> 픽업 시간 고르기</h1></div>
        <CheckoutForm products={products} />
      </div>
    </section>
  );
}
