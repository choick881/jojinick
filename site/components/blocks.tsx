// 여러 페이지에서 함께 쓰는 섹션 조각
import Link from "next/link";
import type { StoreStatus } from "@/lib/catalog";
import { PhotoSlot } from "./photo-slot";

export function SectionHead({ eyebrow, title, lead }: { eyebrow: string; title: React.ReactNode; lead?: React.ReactNode }) {
  return (
    <div className="mb-6 grid gap-2">
      <span className="eyebrow">{eyebrow}</span>
      <h2 className="h2">{title}</h2>
      {lead && <p className="lead">{lead}</p>}
    </div>
  );
}

/** 홈 2안에서 가져온 매장 현황판 */
export function StoreBoard({ status, total, onSale }: { status: StoreStatus; total: number; onSale: number }) {
  const pct = total ? Math.round((onSale / total) * 100) : 0;
  return (
    <div className="grid gap-2.5 rounded-[var(--r)] bg-ink px-5 py-4 text-paper" aria-label="오늘 매장 현황">
      <div className="flex flex-wrap items-baseline justify-between gap-2 text-[.76rem] text-[#CDBEAB]">
        <span>오늘 아침 제조 완료</span>
        {status.isExample && <span>예시 · 관리자 화면 연결 후 실시간</span>}
      </div>
      <div className="num text-[1.15rem] font-extrabold leading-tight sm:text-[1.35rem] md:text-[1.5rem]">
        {status.madeAt} · <em className="not-italic text-[#F2A58A]">{total}종 중 {onSale}종</em> 판매 중
      </div>
      <div className="h-2 overflow-hidden rounded-full bg-[#4A3C31]" aria-hidden="true"><i className="block h-full bg-[#F2A58A]" style={{ width: `${pct}%` }} /></div>
      <small className="text-[.76rem] text-[#CDBEAB]">픽업 17:30~20:30 · 30분 단위로 미리 골라 주세요</small>
    </div>
  );
}

export function Steps({ items }: { items: { title: string; body: string }[] }) {
  return (
    <ol className="grid gap-3 md:grid-cols-3">
      {items.map((s, i) => (
        <li key={s.title} className="card grid content-start gap-1.5 p-5">
          <span className="grid size-[34px] place-items-center rounded-full bg-brand text-[.85rem] font-extrabold text-white">{i + 1}</span>
          <b>{s.title}</b>
          <span className="text-[.88rem] text-muted">{s.body}</span>
        </li>
      ))}
    </ol>
  );
}

export function Promises() {
  const items = [
    { big: "07:00", title: "매일 아침 만듭니다", body: "그날 판매할 반찬은 그날 아침에." },
    { big: "1~2인분", title: "딱 한 끼 양으로", body: "남기거나 버리지 않게 나눠 담아요." },
    { big: "모든 용기", title: "제조 시각 라벨", body: "언제 만들었는지 바로 확인하세요." },
  ];
  return (
    <ul className="grid gap-3 md:grid-cols-3">
      {items.map((p) => (
        <li key={p.title} className="card grid gap-1 px-5 py-6 text-center">
          <span className="num font-serif text-[1.9rem] font-black leading-tight text-brand">{p.big}</span>
          <b>{p.title}</b>
          <span className="text-[.88rem] text-muted">{p.body}</span>
        </li>
      ))}
    </ul>
  );
}

export const HOW_TO = [
  { title: "미리 결제하고 시간 고르기", body: "메뉴를 담고 픽업 시간을 30분 단위로 골라요." },
  { title: "매장 픽업 냉장고에서 꺼내기", body: "문자로 온 주문번호가 붙은 봉투를 꺼내 가세요." },
  { title: "집에서 데우기만", body: "국은 냄비에 3~4분, 반찬은 그대로 드세요." },
];

export function StoreInfo() {
  return (
    <>
      <SectionHead eyebrow="매장 안내" title="양주 ○○동, 퇴근길에 들르세요" />
      <div className="grid gap-5 md:grid-cols-[1.2fr_1fr] md:items-center">
        <div className="grid aspect-[16/10] place-items-center rounded-[var(--r)] p-3 text-center text-[.85rem] text-muted"
          style={{ background: "repeating-linear-gradient(45deg,#EDE2CE 0 12px,#E8DBC4 12px 24px)" }}>
          <span><b className="block text-base text-brand">카카오맵 자리</b>주소가 정해지면 지도와 길찾기 버튼이 들어갑니다</span>
        </div>
        <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-2">
          <dt className="text-[.88rem] text-muted">주소</dt><dd className="font-bold">경기도 양주시 <span className="todo">준비 중</span></dd>
          <dt className="text-[.88rem] text-muted">매장</dt><dd className="num font-bold">매일 06:00~23:00 (무인 판매)</dd>
          <dt className="text-[.88rem] text-muted">픽업</dt><dd className="num font-bold">17:30~20:30 (30분 단위)</dd>
          <dt className="text-[.88rem] text-muted">문의</dt><dd className="font-bold">전화번호 준비 중</dd>
        </dl>
      </div>
    </>
  );
}

export function SilverBand() {
  return (
    <div className="card grid gap-4 p-6 md:grid-cols-2 md:items-center md:p-8">
      <div className="grid gap-2.5">
        <span className="eyebrow">어르신 밥상</span>
        <h2 className="h2">부드럽게, 큰 글씨로,<br />대신 주문까지</h2>
        <p className="lead">잘게 썰고 푹 익힌 반찬을 작은 양으로 담았어요. 자녀가 결제하면 부모님이 성함으로 찾아가세요.</p>
        <div className="flex flex-wrap gap-2">
          {["씹기 쉬움", "잇몸으로", "혀로"].map((l) => <span key={l} className="rounded-full border-[1.5px] border-brand px-3.5 py-1 text-[.9rem] font-bold text-brand">{l}</span>)}
        </div>
        <div><Link href="/silver" className="btn btn-ghost">어르신 밥상 보기</Link></div>
      </div>
      <PhotoSlot drawing="tray" caption="어르신 1인 저녁세트" />
    </div>
  );
}

export function Faq({ items }: { items: { q: string; a: string }[] }) {
  return (
    <div className="grid gap-2.5">
      {items.map((f, i) => (
        <details key={f.q} open={i === 0} className="group card border border-line">
          <summary className="relative cursor-pointer list-none py-4 pl-[18px] pr-12 font-bold [&::-webkit-details-marker]:hidden">
            {f.q}
            <span aria-hidden="true" className="absolute right-[18px] top-1/2 -translate-y-1/2 text-[1.3rem] text-brand group-open:hidden">+</span>
            <span aria-hidden="true" className="absolute right-[18px] top-1/2 hidden -translate-y-1/2 text-[1.3rem] text-brand group-open:inline">−</span>
          </summary>
          <p className="px-[18px] pb-4 text-[.92rem] text-muted">{f.a}</p>
        </details>
      ))}
    </div>
  );
}

export const STAGED_NOTE = "상품 이미지는 연출된 예시로, 실제 상품과 구성·담음새가 다를 수 있습니다.";
