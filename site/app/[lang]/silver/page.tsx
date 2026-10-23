import type { Metadata } from "next";
import { SectionHead, StagedNote, Steps } from "@/components/blocks";
import { ProductGrid } from "@/components/product-card";
import { getLocalizedCatalog } from "@/lib/catalog";
import { alternates, getDict, hasLocale } from "@/lib/i18n";
import { getLang, getT } from "@/lib/i18n/server";

export async function generateMetadata({ params }: PageProps<"/[lang]/silver">): Promise<Metadata> {
  const { lang } = await params;
  if (!hasLocale(lang)) return {};
  const t = getDict(lang).silver;
  return { title: t.title, description: t.description, alternates: alternates(lang, "/silver") };
}

// 이 화면은 처음부터 큰 글씨(1.15배)로 보여 준다
export default async function SilverPage() {
  const lang = await getLang();
  const t = (await getT()).silver;
  const items = (await getLocalizedCatalog(lang)).products.filter((p) => p.category === "silver");
  return (
    <div className="text-[1.15rem]">
      <section className="gut pt-9">
        <div className="wrap grid gap-2"><span className="eyebrow">{t.eyebrow}</span><h1 className="title text-[clamp(1.7rem,5vw,2.3rem)]">{t.h1}</h1><p className="lead">{t.lead}</p></div>
      </section>
      <section className="gut sec pt-7">
        <div className="wrap">
          <SectionHead eyebrow={t.levelsEyebrow} title={t.levelsTitle} lead={t.levelsLead} />
          <ul className="grid gap-3 md:grid-cols-3">
            {t.levels.map((l) => <li key={l.name} className="card grid gap-1 p-5"><b className="text-[1.2rem] text-brand">{l.name}</b><span className="text-muted">{l.body}</span></li>)}
          </ul>
        </div>
      </section>
      <section className="gut sec sec-alt">
        <div className="wrap"><SectionHead eyebrow={t.itemsEyebrow} title={t.itemsTitle(items.length)} /><ProductGrid products={items} big /><StagedNote className="mt-3.5" /></div>
      </section>
      <section className="gut sec">
        <div className="wrap">
          <SectionHead eyebrow={t.proxyEyebrow} title={t.proxyTitle} />
          <Steps items={t.proxySteps} />
          <div className="mt-5 grid gap-1 rounded-[var(--r)] border-2 border-brand bg-white p-5 text-center">
            <span>{t.phoneLead}</span>
            <b className="num select-all text-[1.6rem] text-brand">{t.phoneValue}</b>
            <span className="staged">{t.phoneNote}</span>
          </div>
        </div>
      </section>
    </div>
  );
}
