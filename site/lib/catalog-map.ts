// DB 행·메뉴 파일을 사이트가 쓰는 하나의 모양(Catalog)으로 바꾼다. 네트워크와 무관한 순수 함수라 테스트한다.

export type Softness = "씹기 쉬움" | "잇몸으로" | "혀로";
export type Component = { role: string; name: string; amount: string };
export type Category = { slug: string; name: string; nameEn?: string };
/** 영어 화면(/en)용 값. 빈 칸은 한국어 값으로 대신한다(localizeProduct) */
export type ProductEn = { name: string; size: string; ingredients: string; origin: string; allergens: string; components?: Component[]; categoryName: string };
export type Product = {
  slug: string;
  category: string;
  categoryName: string;
  name: string;
  price: number;
  size: string;
  featured: boolean;
  softness: Softness | null;
  ingredients: string;
  origin: string;
  allergens: string;
  components?: Component[];
  soldOut: boolean;
  en?: ProductEn;
};
/** 매장 현황판 값. isExample이면 화면에 '예시'로 표시한다. */
export type StoreStatus = { madeAt: string; isExample: boolean };
export type Catalog = { products: Product[]; categories: Category[]; status: StoreStatus; source: "db" | "file" };

const EXAMPLE_STATUS: StoreStatus = { madeAt: "07:10", isExample: true };

type DbCategory = { slug: string; name: string; sort: number; name_en?: string | null };
type DbProduct = {
  slug: string; category: string; name: string; price: number; size: string; featured: boolean;
  softness: string | null; ingredients: string; origin: string; allergens: string;
  components: Component[] | null; sort: number; sold_out: boolean;
  name_en?: string | null; size_en?: string | null; ingredients_en?: string | null; origin_en?: string | null; allergens_en?: string | null;
  components_en?: Component[] | null;
};

type EnFields = { name_en?: string | null; size_en?: string | null; ingredients_en?: string | null; origin_en?: string | null; allergens_en?: string | null; components_en?: Component[] | null };
const toEn = (p: EnFields, categoryName: string): ProductEn => ({
  name: p.name_en ?? "", size: p.size_en ?? "", ingredients: p.ingredients_en ?? "", origin: p.origin_en ?? "", allergens: p.allergens_en ?? "",
  components: p.components_en ?? undefined, categoryName,
});

export function fromDb(rows: { products: DbProduct[]; categories: DbCategory[]; status: { made_at: string }[] }): Catalog {
  const categories = [...rows.categories].sort((a, b) => a.sort - b.sort).map(({ slug, name, name_en }) => ({ slug, name, nameEn: name_en ?? "" }));
  const nameOf = new Map(categories.map((c) => [c.slug, c.name]));
  const nameEnOf = new Map(categories.map((c) => [c.slug, c.nameEn]));
  const products = [...rows.products].sort((a, b) => a.sort - b.sort).map((p) => ({
    slug: p.slug,
    category: p.category,
    categoryName: nameOf.get(p.category) ?? "",
    name: p.name,
    price: p.price,
    size: p.size,
    featured: p.featured,
    softness: (p.softness as Softness | null) ?? null,
    ingredients: p.ingredients,
    origin: p.origin,
    allergens: p.allergens,
    components: p.components ?? undefined,
    soldOut: p.sold_out,
    en: toEn(p, nameEnOf.get(p.category) ?? ""),
  }));
  const madeAt = rows.status[0]?.made_at?.slice(0, 5);
  return { products, categories, status: madeAt ? { madeAt, isExample: false } : EXAMPLE_STATUS, source: "db" };
}

type MenuJson = {
  categories: Array<{ slug: string; name: string; name_en?: string }>;
  products: Array<Omit<Product, "categoryName" | "soldOut" | "featured" | "softness" | "en"> & { featured?: boolean; softness: string | null } & EnFields>;
};

export function fromMenuJson(menu: MenuJson): Catalog {
  const nameOf = new Map(menu.categories.map((c) => [c.slug, c.name]));
  const nameEnOf = new Map(menu.categories.map((c) => [c.slug, c.name_en ?? ""]));
  return {
    categories: menu.categories.map(({ slug, name, name_en }) => ({ slug, name, nameEn: name_en ?? "" })),
    products: menu.products.map(({ name_en, size_en, ingredients_en, origin_en, allergens_en, components_en, ...p }) => ({
      ...p,
      featured: Boolean(p.featured),
      softness: (p.softness as Softness | null) ?? null,
      categoryName: nameOf.get(p.category) ?? "",
      soldOut: false,
      en: toEn({ name_en, size_en, ingredients_en, origin_en, allergens_en, components_en }, nameEnOf.get(p.category) ?? ""),
    })),
    status: EXAMPLE_STATUS,
    source: "file",
  };
}

/** 화면 언어에 맞춘 상품. 영어 값이 비어 있으면 한국어 값을 그대로 쓴다 */
export function localizeProduct(p: Product, lang: "ko" | "en"): Product {
  if (lang === "ko" || !p.en) return p;
  const e = p.en;
  return {
    ...p,
    name: e.name || p.name,
    size: e.size || p.size,
    ingredients: e.ingredients || p.ingredients,
    origin: e.origin || p.origin,
    allergens: e.allergens || p.allergens,
    components: e.components?.length ? e.components : p.components,
    categoryName: e.categoryName || p.categoryName,
  };
}

export function localizeCatalog(c: Catalog, lang: "ko" | "en"): Catalog {
  if (lang === "ko") return c;
  return { ...c, products: c.products.map((p) => localizeProduct(p, lang)), categories: c.categories.map((x) => ({ ...x, name: x.nameEn || x.name })) };
}
