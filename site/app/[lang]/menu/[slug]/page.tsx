import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Faq, Promises, SectionHead, StagedNote, Steps } from "@/components/blocks";
import { BuyBox } from "@/components/buy-box";
import { Lines } from "@/components/lines";
import { PhotoSlot } from "@/components/photo-slot";
import { findProduct, getCatalog, localizeProduct, type Product } from "@/lib/catalog";
import { LOCALES, alternates, getDict, hasLocale, localePath, type Dict } from "@/lib/i18n";
import { getLang, getT } from "@/lib/i18n/server";
import { PHOTOS, productPhoto, setContentsPhoto } from "@/lib/photos";
import { absoluteUrl, jsonLd } from "@/lib/site";

export async function generateStaticParams() {
  const slugs = (await getCatalog()).products.map((p) => p.slug);
  return LOCALES.flatMap((lang) => slugs.map((slug) => ({ lang, slug })));
}

export async function generateMetadata({ params }: PageProps<"/[lang]/menu/[slug]">): Promise<Metadata> {
  const { lang, slug } = await params;
  const base = findProduct(await getCatalog(), slug);
  if (!base || !hasLocale(lang)) return {};
  const t = getDict(lang);
  const p = localizeProduct(base, lang);
  const description = t.product.metaDescription(p.name, t.money(p.price), p.size);
  return { title: p.name, description, alternates: alternates(lang, `/menu/${p.slug}`), openGraph: { title: `${p.name} · ${t.common.siteName}`, description } };
}

/** 데우는 법. 판단은 한국어 원본(구성 역할 "국"·"메인찬")으로 하고 문구만 화면 언어로 */
function heatingSteps(base: Product, shown: Product, t: Dict["product"]) {
  if (base.components?.length) {
    const roles = new Set(base.components.map((c) => c.role));
    const steps = [];
    if (roles.has("국")) steps.push({ title: t.heatSoup, body: t.heating.soup });
    if (roles.has("메인찬")) steps.push({ title: t.heatMain, body: t.heating.main });
    steps.push({ title: t.heatSides, body: t.heatSidesBody });
    return steps;
  }
  return [{ title: shown.categoryName, body: t.heating[base.category] ?? t.heating.basic }];
}

export default async function ProductPage({ params }: PageProps<"/[lang]/menu/[slug]">) {
  const lang = await getLang();
  const all = await getT();
  const t = all.product;
  const catalog = await getCatalog();
  const base = findProduct(catalog, (await params).slug);
  if (!base) notFound();
  const p = localizeProduct(base, lang);
  const status = catalog.status;
  const isSet = Boolean(p.components?.length);
  const firstItem = p.components?.[0];
  const heat = heatingSteps(base, p, t);
  const softness = p.softness ? (all.softness[p.softness] ?? p.softness) : null;

  const productLd = {
    "@context": "https://schema.org",
    "@type": "Product",
    name: p.name,
    description: p.size,
    category: p.categoryName,
    brand: { "@type": "Brand", name: all.common.siteName },
    offers: {
      "@type": "Offer",
      price: p.price,
      priceCurrency: "KRW",
      availability: p.soldOut ? "https://schema.org/OutOfStock" : "https://schema.org/InStock",
      url: absoluteUrl(localePath(lang, `/menu/${p.slug}`)),
    },
  };

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: jsonLd(productLd) }} />
      {/* 1. 구매 영역 */}
      <section className="gut pb-12 pt-6">
        <div className="wrap grid gap-6 md:grid-cols-[1.1fr_1fr] md:items-start md:gap-10">
          <div className="min-w-0">
            <PhotoSlot drawing={isSet ? "table" : "bowl"} caption={t.photoCaption(p.name)} src={productPhoto(p.slug)} ratio="4 / 5" sizes="(min-width: 860px) 55vw, 100vw" />
            <StagedNote className="mt-1.5" />
          </div>
          <div className="grid min-w-0 gap-4.5">
            <span className="hand">{t.hand}</span>
            <div className="flex flex-wrap gap-1.5">
              {p.featured && <span className="rounded-full bg-accent px-2.5 py-0.5 text-[.72rem] font-bold text-white">{t.featured}</span>}
              <span className="rounded-full bg-sand px-2.5 py-0.5 text-[.72rem] font-bold text-brand">{p.categoryName}</span>
              <span className="rounded-full bg-sand px-2.5 py-0.5 text-[.72rem] font-bold text-brand">{t.storePickup}</span>
              {softness && <span className="rounded-full bg-sand px-2.5 py-0.5 text-[.72rem] font-bold text-brand">{t.softness(softness)}</span>}
            </div>
            <div className="grid gap-1.5">
              <h1 className="title text-[1.8rem]">{p.name}</h1>
              <p className="text-muted">{p.size}</p>
            </div>
            <div className="flex items-baseline gap-2"><b className="num text-[1.75rem] font-extrabold">{all.money(p.price)}</b></div>
            {/* B안 요약표 */}
            <div className="summary" aria-label={t.summary}>
              <div><small>{t.madeAt}{status.isExample && all.common.example}</small><b className="num">{t.madeAtValue(status.madeAt)}</b></div>
              <div><small>{all.common.pickup}</small><b className="num">17:30~20:30</b></div>
              <div><small>{all.common.storage}</small><b>{all.common.chilled}</b></div>
            </div>
            <BuyBox slug={p.slug} name={p.name} price={p.price} soldOut={p.soldOut} />
            <p className="rounded-[10px] border border-dashed border-line bg-white px-3 py-2.5 text-[.85rem] text-muted">
              <b className="text-ink">{t.forParentsStrong}</b>{t.forParents}
            </p>
          </div>
        </div>
      </section>

      {/* 2. 후킹 */}
      <section className="gut sec sec-alt text-center">
        <div className="narrow grid justify-items-center gap-2.5">
          <span className="eyebrow">{t.hookEyebrow}</span>
          <h2 className="h2"><Lines text={t.hookTitle} /></h2>
          <p className="lead">{t.hookLead}</p>
        </div>
      </section>

      {/* 3. 구성 */}
      {isSet && (
        <section className="gut sec">
          <div className="narrow">
            <SectionHead eyebrow={t.setEyebrow} title={<Lines text={t.setTitle(p.components!.length)} />} />
            <PhotoSlot drawing="boxes" caption={t.setPhoto} src={setContentsPhoto(p.slug)} ratio="3 / 2" />
            <ul className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-4">
              {p.components!.map((c, i) => (
                <li key={i} className="card grid gap-1 p-3.5">
                  <small className="text-[.72rem] font-bold text-brand">{c.role}</small>
                  <b className="text-[.95rem]">{c.name}</b>
                  <span className="num text-[.82rem] text-muted">{c.amount}</span>
                </li>
              ))}
            </ul>
            <p className="mt-2.5 text-[.82rem] text-muted">{t.setNote}</p>
          </div>
        </section>
      )}

      {/* 4. 약속 */}
      <section className={`gut sec ${isSet ? "sec-alt" : ""}`}>
        <div className="narrow"><SectionHead eyebrow={all.home.promiseEyebrow} title={all.home.promiseTitle} /><Promises /></div>
      </section>

      {/* 5. 제조시간 라벨 */}
      <section className="gut sec">
        <div className="narrow grid items-center gap-6 md:grid-cols-2">
          <div className="grid gap-2.5">
            <span className="eyebrow">{t.labelEyebrow}</span>
            <h2 className="h2"><Lines text={t.labelTitle} /></h2>
            <ul className="grid gap-2.5">
              {t.labelPoints.map((x) => (
                <li key={x} className="grid grid-cols-[18px_1fr] items-start gap-2"><span className="mt-[.6em] size-2.5 rounded-full bg-accent" aria-hidden="true" />{x}</li>
              ))}
            </ul>
          </div>
          <div role="img" aria-label={t.labelAria(firstItem?.name ?? p.name, status.madeAt)}
            className="grid w-full max-w-[360px] -rotate-[1.5deg] gap-3 justify-self-center rounded-2xl bg-white px-5.5 pb-4.5 pt-5.5 shadow-[0_1px_0_var(--line),0_10px_30px_rgba(43,33,26,.1)]">
            <div className="flex items-center justify-between gap-2.5 border-b-2 border-ink pb-2.5">
              <Image src="/brand/symbol.svg" alt="" width={26} height={26} />
              <span className="text-[13px] font-bold text-brand">{t.labelShop}</span>
            </div>
            <h3 className="text-[24px] font-extrabold">{firstItem?.name ?? p.name}</h3>
            <div className="flex items-baseline justify-between rounded-[10px] border-2 border-accent bg-[#FFF4EC] px-3 py-2.5">
              <span className="text-[14px] font-bold text-accent-deep">{t.labelMade}</span><b className="num text-[26px] font-extrabold">10.21 {status.madeAt}</b>
            </div>
            <dl className="grid grid-cols-[auto_1fr] gap-x-3.5 gap-y-1.5 text-[15px]">
              <dt className="text-muted">{t.labelAmount}</dt><dd className="num font-bold">{firstItem?.amount ?? p.size}</dd>
              <dt className="text-muted">{t.labelExpiry}</dt><dd className="num font-bold">{t.labelExpiryValue}</dd>
              <dt className="text-muted">{t.labelStorage}</dt><dd className="font-bold">{t.labelStorageValue}</dd>
            </dl>
            <p className="text-[11.5px] leading-normal text-muted">{t.labelNote}</p>
          </div>
        </div>
      </section>

      {/* 6. 데우는 법 */}
      <section className="gut sec sec-alt">
        <div className="narrow">
          <SectionHead eyebrow={t.heatEyebrow} title={<Lines text={t.heatTitle} />} />
          <Steps items={heat} />
        </div>
      </section>

      {/* 7. 정보 고시 */}
      <section className="gut sec">
        <div className="narrow">
          <SectionHead eyebrow={t.infoEyebrow} title={t.infoTitle} />
          <div className="overflow-x-auto rounded-xl border border-line">
            <table className="w-full border-collapse bg-white text-[.85rem]">
              <tbody className="[&_td]:border-b [&_td]:border-line [&_td]:px-3.5 [&_td]:py-2.5 [&_th]:w-[34%] [&_th]:border-b [&_th]:border-line [&_th]:bg-[#FAF5EB] [&_th]:px-3.5 [&_th]:py-2.5 [&_th]:text-left [&_th]:align-top [&_th]:font-medium [&_th]:text-muted [&_tr:last-child>*]:border-0">
                <tr><th>{t.infoName}</th><td>{p.name}</td></tr>
                <tr><th>{t.infoType}</th><td>{t.infoTypeValue}<span className="todo">{t.todoOwner}</span></td></tr>
                <tr><th>{t.infoAmount}</th><td className="num">{p.size}</td></tr>
                <tr><th>{t.infoIngredients}</th><td>{p.ingredients || p.origin ? `${p.ingredients} ${p.origin}` : <>{t.infoPerItem}<span className="todo">{t.todoOwner}</span></>}</td></tr>
                <tr><th>{t.infoAllergens}</th><td>{p.allergens || <>{t.infoPerItem}<span className="todo">{t.todoOwner}</span></>}</td></tr>
                <tr><th>{t.infoMadeExpiry}</th><td>{t.infoOnLabel}</td></tr>
                <tr><th>{t.infoStorage}</th><td>{t.infoStorageValue}</td></tr>
                <tr><th>{t.infoMaker}</th><td>{t.infoMakerValue}<span className="todo">{t.todoAddress}</span></td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* 8. 픽업 안내 */}
      <section className="gut sec sec-alt">
        <div className="narrow">
          <SectionHead eyebrow={t.pickupEyebrow} title={<Lines text={t.pickupTitle} />} />
          <PhotoSlot drawing="locker" caption={t.pickupPhoto} src={PHOTOS.pickup} alt={t.pickupPhotoAlt} ratio="3 / 2" className="mb-1.5" />
          <StagedNote className="mb-5" />
          <Steps items={all.howTo} />
          <p className="mt-3 text-[.85rem] text-muted">{t.cancelNote}<Link href={localePath(lang, "/policy/refund")} className="underline underline-offset-4">{t.refundLink}</Link></p>
        </div>
      </section>

      {/* 9. FAQ */}
      <section className="gut sec">
        <div className="narrow"><SectionHead eyebrow={t.faqEyebrow} title={t.faqTitle} /><Faq items={t.faq} /></div>
      </section>

      {/* 10. 마무리 */}
      <section className="gut sec sec-alt pb-28 md:pb-16">
        <div className="narrow grid justify-items-center gap-4 text-center">
          <span className="hand">{t.endHand}</span>
          <h2 className="h2"><Lines text={t.endTitle} /></h2>
          <p className="lead">{p.name} <b className="num">{all.money(p.price)}</b>{t.endPickup}</p>
          <Link href={localePath(lang, "/menu")} className="btn btn-ghost">{t.otherMenu}</Link>
        </div>
      </section>
    </>
  );
}
