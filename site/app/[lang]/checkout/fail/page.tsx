import type { Metadata } from "next";
import { getDict, hasLocale } from "@/lib/i18n";
import { Suspense } from "react";
import { PaymentFailed } from "@/components/confirm-payment";

export async function generateMetadata({ params }: PageProps<"/[lang]/checkout/fail">): Promise<Metadata> {
  const { lang } = await params;
  return { title: hasLocale(lang) ? getDict(lang).confirm.failPageTitle : undefined, robots: { index: false } };
}

export default function CheckoutFailPage() {
  return (
    <section className="gut sec">
      <div className="narrow">
        <Suspense fallback={null}>
          <PaymentFailed />
        </Suspense>
      </div>
    </section>
  );
}
