// 메뉴 데이터의 단일 진입점. Supabase에서 읽고, 실패하면 저장소의 메뉴 파일(brand/menu.json 복사본)로 대신한다.
import { cacheLife, cacheTag } from "next/cache";
import menu from "@/data/menu.json";
import { fromDb, fromMenuJson, type Catalog, type Product } from "./catalog-map";
import { SUPABASE_PUBLISHABLE_KEY, SUPABASE_URL } from "./supabase-config";

export type { Catalog, Category, Component, Product, Softness, StoreStatus } from "./catalog-map";

/** 관리자 화면에서 품절·제조 시각을 바꾸면 revalidateTag(CATALOG_TAG)로 새로 읽는다 */
export const CATALOG_TAG = "catalog";

async function rest<T>(path: string): Promise<T> {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/${path}`, {
    headers: { apikey: SUPABASE_PUBLISHABLE_KEY, Authorization: `Bearer ${SUPABASE_PUBLISHABLE_KEY}` },
    signal: AbortSignal.timeout(5000),
  });
  if (!res.ok) throw new Error(`Supabase ${path}: ${res.status}`);
  return res.json() as Promise<T>;
}

export async function getCatalog(): Promise<Catalog> {
  "use cache";
  cacheLife("minutes");
  cacheTag(CATALOG_TAG);
  try {
    const [products, categories, status] = await Promise.all([
      rest<Parameters<typeof fromDb>[0]["products"]>("products?select=slug,category,name,price,size,featured,softness,ingredients,origin,allergens,components,sort,sold_out&is_active=eq.true"),
      rest<Parameters<typeof fromDb>[0]["categories"]>("categories?select=slug,name,sort"),
      rest<{ made_at: string }[]>("store_status?select=made_at&id=eq.1"),
    ]);
    if (!products.length) throw new Error("상품이 비어 있음");
    return fromDb({ products, categories, status });
  } catch (e) {
    console.warn("[catalog] Supabase를 읽지 못해 메뉴 파일을 씁니다:", (e as Error).message);
    return fromMenuJson(menu);
  }
}

export const findProduct = (c: Catalog, slug: string): Product | undefined => c.products.find((p) => p.slug === slug);

/** 홈 '오늘의 반찬'에 올릴 순서 */
export const FEATURED_ORDER = ["dinner-set-1", "banchan-3-set", "beef-jangjorim", "doenjang-jjigae", "spicy-pork", "silver-soft-3-set", "spinach-namul", "japchae"];

export function featured(c: Catalog): Product[] {
  return FEATURED_ORDER.map((s) => findProduct(c, s)).filter((p): p is Product => Boolean(p));
}

/** 분류별 데우는 법 (상세페이지) */
export const HEATING: Record<string, string> = {
  soup: "냄비에 붓고 중불에서 3~4분, 보글보글 끓으면 불을 꺼요.",
  main: "뚜껑을 살짝 열고 전자레인지 700W 기준 1분 30초 데워요.",
  basic: "데우지 않고 그대로 드세요.",
};
