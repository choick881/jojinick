import type { Metadata } from "next";
import { STAGED_NOTE } from "@/components/blocks";
import { MenuBrowser } from "@/components/menu-browser";
import { ProductGrid } from "@/components/product-card";
import { getCatalog } from "@/lib/catalog";

export const metadata: Metadata = { title: "메뉴", description: "오늘 아침 만든 저녁세트, 기본찬, 메인찬, 국·찌개, 어르신 밥상." };

export default async function MenuPage() {
  const { products: all, categories, status } = await getCatalog();
  const panels: Record<string, React.ReactNode> = { all: <ProductGrid products={all} /> };
  for (const c of categories) panels[c.slug] = <ProductGrid products={all.filter((p) => p.category === c.slug)} />;
  return (
    <section className="gut pb-18 pt-9">
      <div className="wrap">
        <div className="mb-6 grid gap-2"><span className="eyebrow">메뉴</span><h1 className="title text-[clamp(1.7rem,5vw,2.3rem)]">오늘의 메뉴</h1><p className="lead">매일 아침 만들어 그날 판매합니다. 품절된 메뉴는 내일 다시 만나요.</p></div>
        <div className="summary mb-4.5">
          <div><small>오늘 만든 시각{status.isExample && " (예시)"}</small><b className="num">{status.madeAt}</b></div>
          <div><small>픽업</small><b className="num">17:30~20:30</b></div>
          <div><small>보관</small><b>냉장</b></div>
        </div>
        <MenuBrowser categories={categories} panels={panels} />
        <p className="staged mt-3.5">{STAGED_NOTE}</p>
      </div>
    </section>
  );
}
