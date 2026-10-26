import Link from "next/link";
import type { Product } from "@/lib/catalog";
import { localePath } from "@/lib/i18n";
import { getLang, getT } from "@/lib/i18n/server";
import { productPhoto } from "@/lib/photos";
import { AddToCart } from "./add-to-cart";
import { PhotoSlot } from "./photo-slot";

/** 상품 카드. p는 화면 언어로 바꾼 상품(localizeProduct)이다 */
export async function ProductCard({ p, big = false }: { p: Product; big?: boolean }) {
  const lang = await getLang();
  const t = await getT();
  const tag = p.soldOut ? { t: t.card.soldOut, c: "bg-ink text-white" } : p.featured ? { t: t.card.featured, c: "bg-white text-brand" } : null;
  const href = localePath(lang, `/menu/${p.slug}`);
  return (
    <article className={`card grid min-w-0 grid-rows-[auto_1fr] overflow-hidden ${p.soldOut ? "[&_figure]:opacity-60 [&_figure]:grayscale" : ""}`}>
      <Link href={href} tabIndex={-1} aria-hidden="true">
        <PhotoSlot drawing="bowl" caption={p.name} src={productPhoto(p.slug)} ratio="1 / 1" rounded={false} sizes="(min-width: 1020px) 25vw, 50vw">
          {tag && <span className={`absolute left-2.5 top-2.5 rounded-full px-2.5 py-0.5 text-[.66rem] font-extrabold ${tag.c}`}>{tag.t}</span>}
        </PhotoSlot>
      </Link>
      <div className="grid content-start gap-1 px-3.5 pb-3.5 pt-3">
        <Link href={href} className={`font-bold leading-snug hover:underline ${big ? "text-[1.1rem]" : "text-[.95rem]"}`}>{p.name}</Link>
        <span className={`leading-snug text-muted ${big ? "text-[.95rem]" : "text-[.76rem]"}`}>{p.categoryName} · {p.size}</span>
        {p.softness && <span className="w-fit rounded bg-[var(--soft)] px-1.5 text-[.68rem] font-bold text-brand">{t.softness[p.softness] ?? p.softness}</span>}
        <div className="mt-1.5 flex items-center justify-between gap-2">
          <span className={`num font-extrabold ${big ? "text-[1.1rem]" : ""}`}>{t.money(p.price)}</span>
          <AddToCart slug={p.slug} name={p.name} soldOut={p.soldOut} />
        </div>
      </div>
    </article>
  );
}

export function ProductGrid({ products, big }: { products: Product[]; big?: boolean }) {
  return (
    <div className="grid grid-cols-2 gap-3.5 md:grid-cols-3 lg:grid-cols-4">
      {products.map((p) => <ProductCard key={p.slug} p={p} big={big} />)}
    </div>
  );
}
