// DB 행·메뉴 파일을 사이트가 쓰는 하나의 모양(Catalog)으로 바꾼다. 네트워크와 무관한 순수 함수라 테스트한다.

export type Softness = "씹기 쉬움" | "잇몸으로" | "혀로";
export type Component = { role: string; name: string; amount: string };
export type Category = { slug: string; name: string };
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
};
/** 매장 현황판 값. isExample이면 화면에 '예시'로 표시한다. */
export type StoreStatus = { madeAt: string; isExample: boolean };
export type Catalog = { products: Product[]; categories: Category[]; status: StoreStatus; source: "db" | "file" };

const EXAMPLE_STATUS: StoreStatus = { madeAt: "07:10", isExample: true };

type DbCategory = { slug: string; name: string; sort: number };
type DbProduct = {
  slug: string; category: string; name: string; price: number; size: string; featured: boolean;
  softness: string | null; ingredients: string; origin: string; allergens: string;
  components: Component[] | null; sort: number; sold_out: boolean;
};

export function fromDb(rows: { products: DbProduct[]; categories: DbCategory[]; status: { made_at: string }[] }): Catalog {
  const categories = [...rows.categories].sort((a, b) => a.sort - b.sort).map(({ slug, name }) => ({ slug, name }));
  const nameOf = new Map(categories.map((c) => [c.slug, c.name]));
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
  }));
  const madeAt = rows.status[0]?.made_at?.slice(0, 5);
  return { products, categories, status: madeAt ? { madeAt, isExample: false } : EXAMPLE_STATUS, source: "db" };
}

type MenuJson = {
  categories: Category[];
  products: Array<Omit<Product, "categoryName" | "soldOut" | "featured" | "softness"> & { featured?: boolean; softness: string | null }>;
};

export function fromMenuJson(menu: MenuJson): Catalog {
  const nameOf = new Map(menu.categories.map((c) => [c.slug, c.name]));
  return {
    categories: menu.categories,
    products: menu.products.map((p) => ({
      ...p,
      featured: Boolean(p.featured),
      softness: (p.softness as Softness | null) ?? null,
      categoryName: nameOf.get(p.category) ?? "",
      soldOut: false,
    })),
    status: EXAMPLE_STATUS,
    source: "file",
  };
}
