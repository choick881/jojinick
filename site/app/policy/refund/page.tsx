import type { Metadata } from "next";

export const metadata: Metadata = { title: "환불 정책" };

export default function RefundPage() {
  return (
    <section className="gut sec">
      <article className="narrow grid gap-4 [&_h2]:mt-4 [&_h2]:text-[1.1rem] [&_h2]:font-bold">
        <h1 className="title text-[1.8rem]">환불 정책</h1>
        <p className="todo w-fit">초안 · 운영 정책 확정 필요</p>
        <h2>픽업 3시간 전까지</h2>
        <p>주문을 전액 취소할 수 있습니다. 결제한 수단으로 환불됩니다.</p>
        <h2>픽업 3시간 전 이후</h2>
        <p>주문에 맞춰 이미 만든 음식이라 취소가 어렵습니다.</p>
        <h2>상품에 문제가 있을 때</h2>
        <p>이물질, 변질, 구성 누락이 있으면 받으신 날 사진과 함께 알려 주세요. 확인 후 교환하거나 환불해 드립니다.</p>
        <h2>찾아가지 않은 주문</h2>
        <p>그날 매장 마감(23:00)까지 보관하고, 그 뒤에는 위생을 위해 폐기하며 환불되지 않습니다.</p>
      </article>
    </section>
  );
}
