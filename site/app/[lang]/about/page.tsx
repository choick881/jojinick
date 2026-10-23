import type { Metadata } from "next";
import { SectionHead, StagedNote } from "@/components/blocks";
import { PhotoSlot } from "@/components/photo-slot";
import { alternates, getDict, hasLocale } from "@/lib/i18n";
import { getT } from "@/lib/i18n/server";
import { PHOTOS } from "@/lib/photos";

export async function generateMetadata({ params }: PageProps<"/[lang]/about">): Promise<Metadata> {
  const { lang } = await params;
  if (!hasLocale(lang)) return {};
  const t = getDict(lang).about;
  return { title: t.title, description: t.description, alternates: alternates(lang, "/about") };
}

const List = ({ items }: { items: { t: string; b: string }[] }) => (
  <ul className="grid gap-3 md:grid-cols-2">
    {items.map((x) => <li key={x.t} className="card grid gap-1 px-5 py-4.5"><b className="text-brand">{x.t}</b><span className="text-[.9rem] text-muted">{x.b}</span></li>)}
  </ul>
);

export default async function AboutPage() {
  const t = (await getT()).about;
  return (
    <>
      <section className="gut pt-9">
        <div className="wrap grid gap-2"><span className="eyebrow">{t.eyebrow}</span><h1 className="title text-[clamp(1.7rem,5vw,2.3rem)]">{t.h1}</h1><p className="lead">{t.lead}</p></div>
      </section>
      <section className="gut sec pt-7">
        <div className="wrap">
          <PhotoSlot drawing="shop" caption={t.shopPhoto} src={PHOTOS.shop} ratio="16 / 9" className="mb-1.5" />
          <StagedNote className="mb-7" />
          <SectionHead eyebrow={t.principlesEyebrow} title={t.principlesTitle} />
          <List items={t.principles} />
        </div>
      </section>
      <section className="gut sec sec-alt"><div className="wrap"><SectionHead eyebrow={t.hygieneEyebrow} title={t.hygieneTitle} /><List items={t.hygiene} /></div></section>
      <section className="gut sec">
        <div className="wrap">
          <SectionHead eyebrow={t.makerEyebrow} title={t.makerTitle} />
          <div className="grid gap-4 rounded-3xl bg-white p-6 md:grid-cols-[200px_1fr] md:items-center">
            <PhotoSlot drawing="person" caption={t.makerPhoto} ratio="1 / 1" className="!rounded-full" />
            <div className="grid gap-1.5"><b className="text-[1.1rem]">{t.makerName}</b><p className="lead">{t.makerBody}</p></div>
          </div>
        </div>
      </section>
    </>
  );
}
