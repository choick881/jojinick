import Link from "next/link";
import { categoryName, type Product } from "@/lib/catalog";
import { won } from "@/lib/price";
import { AddToCart } from "./add-to-cart";
import { PhotoSlot } from "./photo-slot";

export function ProductCard({ p, big = false }: { p: Product; big?: boolean }) {
  const tag = p.soldOut ? { t: "품절", c: "bg-ink text-white" } : p.featured ? { t: "추천", c: "bg-white text-brand" } : null;
  return (
    <article className={`card grid min-w-0 grid-rows-[auto_1fr] overflow-hidden ${p.soldOut ? "[&_figure]:opacity-60 [&_figure]:grayscale" : ""}`}>
      <Link href={`/menu/${p.slug}`} aria-label={`${p.name} 자세히 보기`}>
        <PhotoSlot drawing="bowl" caption={p.name} ratio="1 / 1" rounded={false} sizes="(min-width: 1020px) 25vw, 50vw">
          {tag && <span className={`absolute left-2.5 top-2.5 rounded-full px-2.5 py-0.5 text-[.66rem] font-extrabold ${tag.c}`}>{tag.t}</span>}
        </PhotoSlot>
      </Link>
      <div className="grid content-start gap-1 px-3.5 pb-3.5 pt-3">
        <Link href={`/menu/${p.slug}`} className={`font-bold leading-snug hover:underline ${big ? "text-[1.1rem]" : "text-[.95rem]"}`}>{p.name}</Link>
        <span className={`leading-snug text-muted ${big ? "text-[.95rem]" : "text-[.76rem]"}`}>{categoryName(p.category)} · {p.size}</span>
        {p.softness && <span className="w-fit rounded bg-[var(--soft)] px-1.5 text-[.68rem] font-bold text-brand">{p.softness}</span>}
        <div className="mt-1.5 flex items-center justify-between gap-2">
          <span className={`num font-extrabold ${big ? "text-[1.1rem]" : ""}`}>{won(p.price)}</span>
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
