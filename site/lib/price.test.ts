import { describe, expect, it } from "vitest";
import { MAX_QTY, priceCart } from "./price";

const products = [
  { slug: "dinner-set-1", name: "1인 저녁세트", price: 13900 },
  { slug: "spinach-namul", name: "시금치나물", price: 3500 },
  { slug: "sold", name: "품절 반찬", price: 4000, soldOut: true },
];

describe("priceCart", () => {
  it("DB 가격으로 합계를 계산한다", () => {
    const r = priceCart([{ slug: "dinner-set-1", qty: 2 }, { slug: "spinach-namul", qty: 1 }], products);
    expect(r.ok).toBe(true);
    if (r.ok) {
      expect(r.total).toBe(13900 * 2 + 3500);
      expect(r.lines).toHaveLength(2);
    }
  });

  it("같은 상품이 두 번 오면 합친다", () => {
    const r = priceCart([{ slug: "spinach-namul", qty: 1 }, { slug: "spinach-namul", qty: 2 }], products);
    expect(r.ok && r.lines[0].qty).toBe(3);
  });

  it("빈 장바구니를 거절한다", () => {
    expect(priceCart([], products)).toEqual({ ok: false, error: "EMPTY" });
  });

  it("없는 상품을 거절한다", () => {
    expect(priceCart([{ slug: "nope", qty: 1 }], products)).toMatchObject({ ok: false, error: "UNKNOWN_PRODUCT" });
  });

  it("품절 상품을 거절한다", () => {
    expect(priceCart([{ slug: "sold", qty: 1 }], products)).toMatchObject({ ok: false, error: "SOLD_OUT" });
  });

  it("수량은 1 이상 정수, 상품당 최대치까지만", () => {
    expect(priceCart([{ slug: "spinach-namul", qty: 0 }], products)).toMatchObject({ ok: false, error: "BAD_QTY" });
    expect(priceCart([{ slug: "spinach-namul", qty: 1.5 }], products)).toMatchObject({ ok: false, error: "BAD_QTY" });
    expect(priceCart([{ slug: "spinach-namul", qty: MAX_QTY + 1 }], products)).toMatchObject({ ok: false, error: "BAD_QTY" });
  });

  it("클라이언트가 보낸 가격 필드는 무시한다", () => {
    const r = priceCart([{ slug: "dinner-set-1", qty: 1, price: 100 } as never], products);
    expect(r.ok && r.total).toBe(13900);
  });
});
