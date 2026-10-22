import type { Metadata } from "next";
import { Suspense } from "react";
import { PaymentFailed } from "@/components/confirm-payment";

export const metadata: Metadata = { title: "결제 실패", robots: { index: false } };

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
