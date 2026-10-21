import Link from "next/link";

export default function NotFound() {
  return (
    <section className="gut sec">
      <div className="narrow grid justify-items-center gap-4 text-center">
        <span className="hand">앗, 길을 잃었어요</span>
        <h1 className="title text-[1.8rem]">찾으시는 페이지가 없어요</h1>
        <p className="lead">메뉴가 바뀌었거나 주소가 잘못되었을 수 있어요.</p>
        <Link href="/menu" className="btn btn-primary">오늘의 메뉴 보기</Link>
      </div>
    </section>
  );
}
