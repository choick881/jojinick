import type { Metadata } from "next";
import { SectionHead } from "@/components/blocks";
import { PhotoSlot } from "@/components/photo-slot";

export const metadata: Metadata = { title: "가게 이야기", description: "양주에서 매일 아침 반찬을 만드는 작은 무인 가게. 판매만 무인이고, 음식은 사람이 직접 만듭니다." };

const PRINCIPLES = [
  { t: "판매 시간만 무인", b: "만들고 진열하고 정리하는 일은 사람이 합니다." },
  { t: "당일 제조", b: "그날 팔 반찬은 그날 아침에 만듭니다." },
  { t: "1~2인분 소포장", b: "남기지 않을 만큼만 담습니다." },
  { t: "버리는 음식 줄이기", b: "미리 주문을 받아 만드는 양을 맞춥니다." },
];
const HYGIENE = [
  { t: "쇼케이스 온도 기록", b: "냉장 0~10℃를 유지하고 매일 기록합니다." },
  { t: "제조시간 라벨", b: "모든 용기에 만든 시각을 분 단위로 적습니다." },
];

const List = ({ items }: { items: { t: string; b: string }[] }) => (
  <ul className="grid gap-3 md:grid-cols-2">
    {items.map((x) => <li key={x.t} className="card grid gap-1 px-5 py-4.5"><b className="text-brand">{x.t}</b><span className="text-[.9rem] text-muted">{x.b}</span></li>)}
  </ul>
);

export default function AboutPage() {
  return (
    <>
      <section className="gut pt-9">
        <div className="wrap grid gap-2"><span className="eyebrow">가게 이야기</span><h1 className="title text-[clamp(1.7rem,5vw,2.3rem)]">동네 부엌처럼 운영합니다</h1><p className="lead">양주에서 매일 아침 반찬을 만드는 작은 무인 가게입니다. 판매만 무인이고, 음식은 사람이 직접 만듭니다.</p></div>
      </section>
      <section className="gut sec pt-7">
        <div className="wrap">
          <PhotoSlot drawing="shop" caption="따뜻한 가게 내부 (나무 선반, 쇼케이스)" ratio="16 / 9" className="mb-7" />
          <SectionHead eyebrow="운영 원칙" title="네 가지를 지킵니다" />
          <List items={PRINCIPLES} />
        </div>
      </section>
      <section className="gut sec sec-alt"><div className="wrap"><SectionHead eyebrow="위생과 신선도" title="보이는 곳에서 관리합니다" /><List items={HYGIENE} /></div></section>
      <section className="gut sec">
        <div className="wrap">
          <SectionHead eyebrow="만드는 사람" title="곧 소개해 드릴게요" />
          <div className="grid gap-4 rounded-3xl bg-white p-6 md:grid-cols-[200px_1fr] md:items-center">
            <PhotoSlot drawing="person" caption="프로필 사진" ratio="1 / 1" className="!rounded-full" />
            <div className="grid gap-1.5"><b className="text-[1.1rem]">만드는 사람</b><p className="lead">요리사 프로필과 이야기가 이 자리에 들어갑니다. 사진, 경력, 좋아하는 반찬 한 가지를 받아 채울게요.</p></div>
          </div>
        </div>
      </section>
    </>
  );
}
