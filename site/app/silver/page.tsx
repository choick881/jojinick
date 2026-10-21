import type { Metadata } from "next";
import { SectionHead, Steps } from "@/components/blocks";
import { ProductGrid } from "@/components/product-card";
import { getProducts } from "@/lib/catalog";

export const metadata: Metadata = { title: "어르신 밥상", description: "잘게 썰고 푹 익힌 부드러운 반찬. 자녀가 결제하고 부모님이 성함으로 찾아가세요." };

const LEVELS = [
  { name: "씹기 쉬움", body: "잘게 썰어 이가 약해도 편하게." },
  { name: "잇몸으로", body: "잇몸으로 눌러 으깨질 만큼 푹 익혀요." },
  { name: "혀로", body: "혀로 눌러도 풀어질 만큼 부드럽게." },
];

// 이 화면은 처음부터 큰 글씨(1.15배)로 보여 준다
export default function SilverPage() {
  const items = getProducts().filter((p) => p.category === "silver");
  return (
    <div className="text-[1.15rem]">
      <section className="gut pt-9">
        <div className="wrap grid gap-2"><span className="eyebrow">어르신 밥상</span><h1 className="title text-[clamp(1.7rem,5vw,2.3rem)]">부모님께 전하는 한 끼</h1><p className="lead">잘게 썰고 푹 익혀 부드럽게 만들었어요. 이 화면은 처음부터 큰 글씨로 보여 드려요.</p></div>
      </section>
      <section className="gut sec pt-7">
        <div className="wrap">
          <SectionHead eyebrow="부드러움 3단계" title="드시기 편한 정도를 고르세요" lead="가게에서 정한 기준이에요. 공인 인증 등급이 아닙니다." />
          <ul className="grid gap-3 md:grid-cols-3">
            {LEVELS.map((l) => <li key={l.name} className="card grid gap-1 p-5"><b className="text-[1.2rem] text-brand">{l.name}</b><span className="text-muted">{l.body}</span></li>)}
          </ul>
        </div>
      </section>
      <section className="gut sec sec-alt">
        <div className="wrap"><SectionHead eyebrow="상품" title={`어르신 밥상 ${items.length}가지`} /><ProductGrid products={items} big /></div>
      </section>
      <section className="gut sec">
        <div className="wrap">
          <SectionHead eyebrow="자녀가 대신 주문하기" title="멀리 계셔도 챙겨 드릴 수 있어요" />
          <Steps items={[
            { title: "자녀가 결제해요", body: "주문할 때 '받는 분'에 부모님 성함과 연락처를 적어요." },
            { title: "부모님께 문자가 가요", body: "픽업 시간과 주문번호를 부모님 휴대폰으로 보내 드려요." },
            { title: "부모님이 찾아가세요", body: "매장 픽업 냉장고에서 성함이 적힌 봉투를 꺼내요." },
          ]} />
          <div className="mt-5 grid gap-1 rounded-[var(--r)] border-2 border-brand bg-white p-5 text-center">
            <span>인터넷이 어려우시면 전화로 주문하세요</span>
            <b className="num select-all text-[1.6rem] text-brand">전화번호 준비 중</b>
            <span className="staged">번호가 정해지면 이 자리에 크게 넣습니다</span>
          </div>
        </div>
      </section>
    </div>
  );
}
