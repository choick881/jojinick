import { describe, expect, it } from "vitest";
import menu from "@/data/menu.json";
import { fromDb, fromMenuJson } from "./catalog-map";

const categories = [{ slug: "soup", name: "국·찌개", sort: 3 }, { slug: "main", name: "메인찬", sort: 2 }];
const products = [
  { slug: "doenjang-jjigae", category: "soup", name: "된장찌개", price: 6000, size: "450g", featured: false, softness: null, ingredients: "", origin: "", allergens: "", components: null, sort: 12, sold_out: true },
  { slug: "spicy-pork", category: "main", name: "제육볶음", price: 5000, size: "200g", featured: true, softness: null, ingredients: "돼지고기", origin: "국내산", allergens: "대두", components: null, sort: 9, sold_out: false },
];

describe("fromDb", () => {
  const c = fromDb({ products, categories, status: [{ made_at: "07:10:00" }] });

  it("분류를 sort 순서로 정렬한다", () => {
    expect(c.categories.map((x) => x.slug)).toEqual(["main", "soup"]);
  });
  it("상품에 분류 이름과 품절 여부를 붙인다", () => {
    const p = c.products.find((x) => x.slug === "doenjang-jjigae")!;
    expect(p.categoryName).toBe("국·찌개");
    expect(p.soldOut).toBe(true);
  });
  it("제조 시각을 HH:MM으로 줄이고 DB 값임을 표시한다", () => {
    expect(c.status).toEqual({ madeAt: "07:10", isExample: false });
    expect(c.source).toBe("db");
  });
  it("현황판 행이 없으면 예시 값을 쓴다", () => {
    expect(fromDb({ products, categories, status: [] }).status.isExample).toBe(true);
  });
});

describe("fromMenuJson", () => {
  const c = fromMenuJson(menu);
  it("메뉴 파일의 상품 17개를 그대로 쓰고 예시로 표시한다", () => {
    expect(c.products).toHaveLength(17);
    expect(c.source).toBe("file");
    expect(c.status.isExample).toBe(true);
    expect(c.products[0].categoryName).toBe("저녁세트");
  });
});
