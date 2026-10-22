import type { Metadata } from "next";

export const metadata: Metadata = { title: "이용약관" };

export default function TermsPage() {
  return (
    <section className="gut sec">
      <article className="narrow grid gap-4 [&_h2]:mt-4 [&_h2]:text-[1.1rem] [&_h2]:font-bold">
        <h1 className="title text-[1.8rem]">이용약관</h1>
        <p className="todo w-fit">초안 · 사업자 정보와 법률 검토 후 확정</p>
        <h2>제1조 (목적)</h2>
        <p>이 약관은 온담찬(이하 &lsquo;가게&rsquo;)이 운영하는 홈페이지에서 반찬을 미리 결제하고 매장에서 찾아가는 서비스의 이용 조건을 정합니다.</p>
        <h2>제2조 (주문과 결제)</h2>
        <p>주문은 회원가입 없이 이름과 휴대폰 번호로 할 수 있습니다. 결제 금액은 가게가 정한 판매 가격으로 계산합니다.</p>
        <h2>제3조 (픽업)</h2>
        <p>주문하신 상품은 고르신 날짜와 시간에 매장 픽업 냉장고에 준비합니다. 받는 분을 따로 적으면 그분이 찾아가실 수 있습니다.</p>
        <h2>제4조 (취소와 환불)</h2>
        <p>자세한 내용은 환불 정책을 따릅니다.</p>
      </article>
    </section>
  );
}
