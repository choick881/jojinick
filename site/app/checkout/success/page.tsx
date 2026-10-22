import type { Metadata } from "next";
import { Suspense } from "react";
import { ConfirmPayment } from "@/components/confirm-payment";

export const metadata: Metadata = { title: "결제 확인", robots: { index: false } };

export default function CheckoutSuccessPage() {
  return (
    <section className="gut sec">
      <div className="narrow">
        <Suspense fallback={<p className="lead text-center">결제를 확인하고 있어요…</p>}>
          <ConfirmPayment />
        </Suspense>
      </div>
    </section>
  );
}
