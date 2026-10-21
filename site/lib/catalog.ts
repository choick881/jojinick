// 메뉴 데이터의 단일 진입점. 지금은 brand/menu.json 복사본(data/menu.json)을 읽고,
// Supabase가 연결되면(Phase 3) 이 파일만 바꿔 DB에서 읽는다.
import menu from "@/data/menu.json";

export type Softness = "씹기 쉬움" | "잇몸으로" | "혀로";
export type Component = { role: string; name: string; amount: string };
export type Product = {
  slug: string;
  category: string;
  name: string;
  price: number;
  size: string;
  featured?: boolean;
  softness: Softness | null;
  ingredients: string;
  origin: string;
  allergens: string;
  components?: Component[];
  soldOut?: boolean;
};
export type Category = { slug: string; name: string };

/** 매장 현황판 값. DB 연결 전에는 예시 값이며 isExample로 화면에 표시한다. */
export type StoreStatus = { madeAt: string; isExample: boolean };

const products = menu.products as Product[];
export const categories: Category[] = menu.categories;
export const softnessLevels = menu.softness_scale.levels as Softness[];

export function getProducts(): Product[] {
  return products;
}

export function getProduct(slug: string): Product | undefined {
  return products.find((p) => p.slug === slug);
}

export function categoryName(slug: string): string {
  return categories.find((c) => c.slug === slug)?.name ?? "";
}

export function getStoreStatus(): StoreStatus {
  return { madeAt: "07:10", isExample: true };
}

/** 홈 '오늘의 반찬'에 올릴 순서 */
export const FEATURED_ORDER = ["dinner-set-1", "banchan-3-set", "beef-jangjorim", "doenjang-jjigae", "spicy-pork", "silver-soft-3-set", "spinach-namul", "japchae"];

export function getFeatured(): Product[] {
  return FEATURED_ORDER.map((s) => getProduct(s)).filter((p): p is Product => Boolean(p));
}

/** 분류별 데우는 법 (상세페이지) */
export const HEATING: Record<string, string> = {
  soup: "냄비에 붓고 중불에서 3~4분, 보글보글 끓으면 불을 꺼요.",
  main: "뚜껑을 살짝 열고 전자레인지 700W 기준 1분 30초 데워요.",
  basic: "데우지 않고 그대로 드세요.",
};
