// 주문 요청 검사와 주문번호·주문명 만들기. 서버(/api/orders)가 쓰며, 네트워크와 무관한 순수 함수다.
import type { CartItem } from "./price";

export type Person = { name: string; phone: string };
export type OrderRequest = {
  items: CartItem[];
  customer: Person;
  recipient: Person | null;
  pickup: { date: string; time: string };
};
export type ParseError = "BAD_ITEMS" | "BAD_CUSTOMER" | "BAD_RECIPIENT" | "BAD_PICKUP" | "NOT_AGREED";

const MAX_NAME = 30;

/** 휴대폰 번호를 숫자만 남겨 돌려준다. 010·011·016~019로 시작하는 10~11자리만 받는다. */
export function normalizePhone(input: unknown): string | null {
  const digits = String(input ?? "").replace(/\D/g, "");
  return /^01[016789]\d{7,8}$/.test(digits) ? digits : null;
}

function person(v: unknown): Person | null {
  const o = (v ?? {}) as Record<string, unknown>;
  const name = String(o.name ?? "").trim();
  const phone = normalizePhone(o.phone);
  if (!name || name.length > MAX_NAME || !phone) return null;
  return { name, phone };
}

export function parseOrderRequest(body: unknown): { ok: true; value: OrderRequest } | { ok: false; error: ParseError } {
  const b = (body ?? {}) as Record<string, unknown>;
  if (!Array.isArray(b.items) || b.items.length === 0 || b.items.length > 30) return { ok: false, error: "BAD_ITEMS" };
  const items = b.items.map((i) => ({ slug: String((i as CartItem)?.slug ?? ""), qty: Number((i as CartItem)?.qty) }));

  const customer = person(b.customer);
  if (!customer) return { ok: false, error: "BAD_CUSTOMER" };

  let recipient: Person | null = null;
  if (b.recipient) {
    recipient = person(b.recipient);
    if (!recipient) return { ok: false, error: "BAD_RECIPIENT" };
  }

  const p = (b.pickup ?? {}) as Record<string, unknown>;
  const date = String(p.date ?? "");
  const time = String(p.time ?? "");
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !/^\d{2}:\d{2}$/.test(time)) return { ok: false, error: "BAD_PICKUP" };

  if (b.agree !== true) return { ok: false, error: "NOT_AGREED" };
  return { ok: true, value: { items, customer, recipient, pickup: { date, time } } };
}

/** 토스 orderId 규칙: 영문·숫자·-·_ 6~64자 */
export function makeOrderNumber(now: Date, random: string): string {
  const kst = new Date(now.getTime() + 9 * 3600_000);
  const ymd = kst.toISOString().slice(0, 10).replace(/-/g, "");
  return `OD-${ymd}-${random.replace(/[^A-Za-z0-9]/g, "").slice(0, 12)}`;
}

export function makeOrderName(names: string[]): string {
  return names.length > 1 ? `${names[0]} 외 ${names.length - 1}건` : names[0] ?? "";
}

/** 화면에 보일 오류 문구 */
export const ORDER_ERROR_MESSAGE: Record<string, string> = {
  BAD_ITEMS: "담은 상품을 확인해 주세요.",
  BAD_CUSTOMER: "주문하시는 분의 이름과 휴대폰 번호를 확인해 주세요.",
  BAD_RECIPIENT: "받는 분의 성함과 휴대폰 번호를 확인해 주세요.",
  BAD_PICKUP: "픽업 날짜와 시간을 다시 골라 주세요.",
  NOT_AGREED: "환불 정책 확인에 체크해 주세요.",
  EMPTY: "담은 상품이 없어요.",
  UNKNOWN_PRODUCT: "판매하지 않는 상품이 들어 있어요. 장바구니를 확인해 주세요.",
  SOLD_OUT: "품절된 상품이 있어요. 장바구니에서 빼 주세요.",
  BAD_QTY: "상품은 한 번에 5개까지 주문할 수 있어요.",
  SLOT_CLOSED: "고르신 픽업 시간은 주문이 마감되었어요. 다른 시간을 골라 주세요.",
  SLOT_FULL: "고르신 픽업 시간은 주문이 꽉 찼어요. 다른 시간을 골라 주세요.",
  SERVER: "주문을 저장하지 못했어요. 잠시 뒤 다시 시도해 주세요.",
  NOT_CONFIGURED: "결제 준비가 아직 끝나지 않았어요. 가게에 문의해 주세요.",
};
