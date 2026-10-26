import type { Metadata } from "next";
import { getDict, hasLocale } from "@/lib/i18n";
import { Suspense } from "react";
import { ConfirmPayment } from "@/components/confirm-payment";

export async function generateMetadata({ params }: PageProps<"/[lang]/checkout/success">): Promise<Metadata> {
  const { lang } = await params;
  return { title: hasLocale(lang) ? getDict(lang).confirm.successTitle : undefined, robots: { index: false } };
}

export default function CheckoutSuccessPage() {
  return (
    <section className="gut sec">
      <div className="narrow">
        <Suspense fallback={null}>
          <ConfirmPayment />
        </Suspense>
      </div>
    </section>
  );
}
