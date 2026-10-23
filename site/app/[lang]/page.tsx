import Link from "next/link";
import { Promises, SectionHead, SilverBand, StagedNote, Steps, StoreBoard, StoreInfo } from "@/components/blocks";
import { Lines } from "@/components/lines";
import { PhotoSlot } from "@/components/photo-slot";
import { ProductGrid } from "@/components/product-card";
import { featured, findProduct, getLocalizedCatalog } from "@/lib/catalog";
import { localePath } from "@/lib/i18n";
import { getLang, getT } from "@/lib/i18n/server";
import { PHOTOS } from "@/lib/photos";

// 홈 = 시안 1안(두 손님 나란히) + 2안 매장 현황판
export default async function Home() {
  const lang = await getLang();
  const all = await getT();
  const t = all.home;
  const catalog = await getLocalizedCatalog(lang);
  const products = catalog.products;
  const me = findProduct(catalog, "dinner-set-1")!;
  const parent = findProduct(catalog, "silver-dinner-set")!;
  const guests = [
    { ...t.me, p: me, href: localePath(lang, `/menu/${me.slug}`), primary: true, drawing: "table" as const, src: PHOTOS.dinnerTable },
    { ...t.parent, p: parent, href: localePath(lang, "/silver"), primary: false, drawing: "tray" as const, src: PHOTOS.silverTray },
  ];

  return (
    <>
      <section className="gut">
        <div className="wrap grid gap-6 pb-10 pt-9">
          <div className="grid justify-items-center gap-2 text-center">
            <span className="hand">{t.hand}</span>
            <h1 className="title text-[clamp(1.9rem,6vw,2.8rem)]">{t.title}</h1>
            <p className="text-muted"><Lines text={t.lead} /></p>
          </div>
          <div className="grid gap-4 md:grid-cols-2">
            {guests.map((g) => (
              <article key={g.who} className="grid grid-rows-[auto_1fr] overflow-hidden rounded-3xl bg-white">
                <PhotoSlot drawing={g.drawing} caption={g.cap} src={g.src} rounded={false} />
                <div className="grid content-start gap-2.5 p-5">
                  <span className="text-[.78rem] font-extrabold tracking-wide text-accent-deep">{g.who}</span>
                  <h2 className="h2 text-[1.4rem]"><Lines text={g.title} /></h2>
                  <p className="text-[.92rem] text-muted">{g.body}</p>
                  <div className="flex items-baseline justify-between gap-3 border-t border-line pt-2.5">
                    <span>{g.p.name}</span><b className="num shrink-0 text-[1.15rem]">{all.money(g.p.price)}</b>
                  </div>
                  <Link href={g.href} className={`btn ${g.primary ? "btn-primary" : "btn-ghost"} w-full`}>{g.cta}</Link>
                </div>
              </article>
            ))}
          </div>
          <StoreBoard status={catalog.status} total={products.length} onSale={products.filter((p) => !p.soldOut).length} />
        </div>
      </section>

      <section className="gut sec sec-alt">
        <div className="wrap grid gap-2.5 text-center">
          <p className="font-serif text-[1.3rem] font-black">{t.q1}</p>
          <p className="font-serif text-[1.3rem] font-black text-brand">{t.q2}</p>
        </div>
      </section>

      <section className="gut sec">
        <div className="wrap">
          <div className="mb-6 flex flex-wrap items-end justify-between gap-2.5">
            <div className="grid gap-2"><span className="eyebrow">{t.todayEyebrow}</span><h2 className="h2">{t.todayTitle}</h2></div>
            <Link href={localePath(lang, "/menu")} className="text-[.85rem] font-bold text-brand underline underline-offset-4">{t.allMenu}</Link>
          </div>
          <ProductGrid products={featured(catalog)} />
          <StagedNote className="mt-3.5" />
        </div>
      </section>

      <section className="gut sec sec-alt">
        <div className="wrap"><SectionHead eyebrow={t.howEyebrow} title={t.howTitle} /><Steps items={all.howTo} /></div>
      </section>

      <section className="gut sec">
        <div className="wrap"><SectionHead eyebrow={t.promiseEyebrow} title={t.promiseTitle} /><Promises /></div>
      </section>

      <section className="gut sec sec-alt"><div className="wrap"><SilverBand /></div></section>
      <section className="gut sec"><div className="wrap"><StoreInfo /></div></section>
    </>
  );
}
