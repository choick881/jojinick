// 장바구니 금액 계산. 결제 금액은 반드시 서버가 이 함수로 다시 계산한다(클라이언트 가격은 믿지 않음).

export const MAX_QTY = 5;

export type PricedProduct = { slug: string; name: string; price: number; soldOut?: boolean };
export type CartItem = { slug: string; qty: number };
export type PricedLine = { slug: string; name: string; unitPrice: number; qty: number; amount: number };
export type PriceResult =
  | { ok: true; lines: PricedLine[]; total: number }
  | { ok: false; error: "EMPTY" | "UNKNOWN_PRODUCT" | "SOLD_OUT" | "BAD_QTY"; slug?: string };

export function priceCart(items: CartItem[], products: PricedProduct[]): PriceResult {
  if (!Array.isArray(items) || items.length === 0) return { ok: false, error: "EMPTY" };

  const merged = new Map<string, number>();
  for (const { slug, qty } of items) {
    if (!Number.isInteger(qty) || qty < 1) return { ok: false, error: "BAD_QTY", slug };
    merged.set(slug, (merged.get(slug) ?? 0) + qty);
  }

  const bySlug = new Map(products.map((p) => [p.slug, p]));
  const lines: PricedLine[] = [];
  for (const [slug, qty] of merged) {
    const p = bySlug.get(slug);
    if (!p) return { ok: false, error: "UNKNOWN_PRODUCT", slug };
    if (p.soldOut) return { ok: false, error: "SOLD_OUT", slug };
    if (qty > MAX_QTY) return { ok: false, error: "BAD_QTY", slug };
    lines.push({ slug, name: p.name, unitPrice: p.price, qty, amount: p.price * qty });
  }
  return { ok: true, lines, total: lines.reduce((sum, l) => sum + l.amount, 0) };
}

export const won = (n: number) => `${n.toLocaleString("ko-KR")}원`;
