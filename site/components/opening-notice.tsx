import Link from "next/link";

/** 오픈 준비 중 띠(모든 화면 맨 위). 운영 배포에서 주문을 열기 전까지만 보인다 */
export function OpeningBanner() {
  return (
    <p className="bg-brand px-4 py-2 text-center text-[.88rem] font-bold text-white" role="status">
      온담찬은 지금 <span className="text-[#FFD9A8]">오픈 준비 중</span>이에요 · 메뉴를 먼저 둘러보세요
    </p>
  );
}

/** 주문 화면 대신 보여 줄 안내 */
export function OpeningNotice() {
  return (
    <div className="card mx-auto grid max-w-md justify-items-center gap-4 p-7 text-center">
      <span className="hand text-[1.4rem]">곧 문을 열어요</span>
      <h1 className="title text-[1.7rem]">지금은 주문을 받지 않아요</h1>
      <p className="lead">양주 무인 반찬가게 온담찬이 오픈 준비 중입니다. 문을 열면 이 화면에서 미리 결제하고 픽업 시간을 고를 수 있어요.</p>
      <Link href="/menu" className="btn btn-primary">메뉴 둘러보기</Link>
    </div>
  );
}
