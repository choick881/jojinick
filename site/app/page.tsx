import Link from "next/link";
import { HOW_TO, Promises, SectionHead, SilverBand, Steps, StoreBoard, StoreInfo } from "@/components/blocks";
import { PhotoSlot } from "@/components/photo-slot";
import { ProductGrid } from "@/components/product-card";
import { featured, findProduct, getCatalog } from "@/lib/catalog";
import { won } from "@/lib/price";

// 홈 = 시안 1안(두 손님 나란히) + 2안 매장 현황판
export default async function Home() {
  const catalog = await getCatalog();
  const all = catalog.products;
  const me = findProduct(catalog, "dinner-set-1")!;
  const parent = findProduct(catalog, "silver-dinner-set")!;
  const guests = [
    { who: "나를 위한 한 끼", title: <>퇴근길, 저녁이<br />준비되어 있어요</>, body: "아침에 만든 국과 반찬을 1인분씩. 미리 결제하고 찾아가 데우기만 하세요.", p: me, href: `/menu/${me.slug}`, cta: "미리 결제하기", primary: true, drawing: "table" as const, cap: "퇴근 후 혼자 먹는 따뜻한 저녁상" },
    { who: "부모님께 전하는 한 끼", title: <>부모님 저녁,<br />대신 챙겨 드려요</>, body: "부드럽게 만든 어르신 밥상. 자녀가 결제하면 부모님이 성함으로 찾아가세요.", p: parent, href: "/silver", cta: "부모님 반찬 보내기", primary: false, drawing: "tray" as const, cap: "부드러운 반찬을 담은 어르신 밥상" },
  ];

  return (
    <>
      <section className="gut">
        <div className="wrap grid gap-6 pb-10 pt-9">
          <div className="grid justify-items-center gap-2 text-center">
            <span className="hand">따뜻한 한 끼를 생각합니다</span>
            <h1 className="title text-[clamp(1.9rem,6vw,2.8rem)]">매일의 식사에 온기를 담다</h1>
            <p className="text-muted">나를 위한 한 끼도, 부모님께 전하는 한 끼도.<br />익숙한 집밥으로 마음을 전합니다.</p>
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            {guests.map((g) => (
              <article key={g.who} className="grid grid-rows-[auto_1fr] overflow-hidden rounded-3xl bg-white">
                <PhotoSlot drawing={g.drawing} caption={g.cap} rounded={false} />
                <div className="grid content-start gap-2.5 p-5">
                  <span className="text-[.78rem] font-extrabold tracking-wide text-accent-deep">{g.who}</span>
                  <h2 className="h2 text-[1.4rem]">{g.title}</h2>
                  <p className="text-[.92rem] text-muted">{g.body}</p>
                  <div className="flex items-baseline justify-between border-t border-line pt-2.5">
                    <span>{g.p.name}</span><b className="num text-[1.15rem]">{won(g.p.price)}</b>
                  </div>
                  <Link href={g.href} className={`btn ${g.primary ? "btn-primary" : "btn-ghost"} w-full`}>{g.cta}</Link>
                </div>
              </article>
            ))}
          </div>
          <StoreBoard status={catalog.status} total={all.length} onSale={all.filter((p) => !p.soldOut).length} />
        </div>
      </section>

      <section className="gut sec sec-alt">
        <div className="wrap grid gap-2.5 text-center">
          <p className="font-serif text-[1.3rem] font-black">퇴근하고 요리할 힘, 남아 있나요?</p>
          <p className="font-serif text-[1.3rem] font-black text-brand">부모님 식사, 매일 챙기기 어렵죠?</p>
        </div>
      </section>

      <section className="gut sec">
        <div className="wrap">
          <div className="mb-6 flex flex-wrap items-end justify-between gap-2.5">
            <div className="grid gap-2"><span className="eyebrow">오늘의 반찬</span><h2 className="h2">오늘 아침에 만들었어요</h2></div>
            <Link href="/menu" className="text-[.85rem] font-bold text-brand underline underline-offset-4">전체 메뉴 보기</Link>
          </div>
          <ProductGrid products={featured(catalog)} />
        </div>
      </section>

      <section className="gut sec sec-alt">
        <div className="wrap"><SectionHead eyebrow="이용 방법" title="세 단계면 저녁 준비 끝" /><Steps items={HOW_TO} /></div>
      </section>

      <section className="gut sec">
        <div className="wrap"><SectionHead eyebrow="온담찬의 약속" title="숫자로 말씀드릴게요" /><Promises /></div>
      </section>

      <section className="gut sec sec-alt"><div className="wrap"><SilverBand /></div></section>
      <section className="gut sec"><div className="wrap"><StoreInfo /></div></section>
    </>
  );
}
