import type { Metadata } from "next";
import { StagedNote } from "@/components/blocks";
import { MenuBrowser } from "@/components/menu-browser";
import { ProductGrid } from "@/components/product-card";
import { getLocalizedCatalog } from "@/lib/catalog";
import { alternates, getDict, hasLocale } from "@/lib/i18n";
import { getLang, getT } from "@/lib/i18n/server";

export async function generateMetadata({ params }: PageProps<"/[lang]/menu">): Promise<Metadata> {
  const { lang } = await params;
  if (!hasLocale(lang)) return {};
  const t = getDict(lang).menuPage;
  return { title: t.title, description: t.description, alternates: alternates(lang, "/menu") };
}

export default async function MenuPage() {
  const lang = await getLang();
  const all = await getT();
  const t = all.menuPage;
  const { products, categories, status } = await getLocalizedCatalog(lang);
  const panels: Record<string, React.ReactNode> = { all: <ProductGrid products={products} /> };
  for (const c of categories) panels[c.slug] = <ProductGrid products={products.filter((p) => p.category === c.slug)} />;
  return (
    <section className="gut pb-18 pt-9">
      <div className="wrap">
        <div className="mb-6 grid gap-2"><span className="eyebrow">{t.eyebrow}</span><h1 className="title text-[clamp(1.7rem,5vw,2.3rem)]">{t.h1}</h1><p className="lead">{t.lead}</p></div>
        <div className="summary mb-4.5">
          <div><small>{all.common.madeToday}{status.isExample && all.common.example}</small><b className="num">{status.madeAt}</b></div>
          <div><small>{all.common.pickup}</small><b className="num">17:30~20:30</b></div>
          <div><small>{all.common.storage}</small><b>{all.common.chilled}</b></div>
        </div>
        <MenuBrowser categories={categories} panels={panels} />
        <StagedNote className="mt-3.5" />
      </div>
    </section>
  );
}
