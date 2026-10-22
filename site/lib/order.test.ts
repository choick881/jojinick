import { describe, expect, it } from "vitest";
import { makeOrderName, makeOrderNumber, normalizePhone, parseOrderRequest } from "./order";

const ok = {
  items: [{ slug: "dinner-set-1", qty: 2 }],
  customer: { name: " 홍길동 ", phone: "010-1234-5678" },
  pickup: { date: "2026-10-22", time: "18:30" },
  agree: true,
};

describe("parseOrderRequest", () => {
  it("정상 요청을 다듬어 돌려준다", () => {
    const r = parseOrderRequest(ok);
    expect(r.ok).toBe(true);
    if (r.ok) {
      expect(r.value.customer).toEqual({ name: "홍길동", phone: "01012345678" });
      expect(r.value.recipient).toBeNull();
    }
  });

  it("받는 분을 따로 받는다", () => {
    const r = parseOrderRequest({ ...ok, recipient: { name: "김순자", phone: "010 9876 5432" } });
    expect(r.ok && r.value.recipient).toEqual({ name: "김순자", phone: "01098765432" });
  });

  it("빈 이름·잘못된 휴대폰·약관 미동의를 거절한다", () => {
    expect(parseOrderRequest({ ...ok, customer: { name: " ", phone: "010-1234-5678" } })).toMatchObject({ ok: false, error: "BAD_CUSTOMER" });
    expect(parseOrderRequest({ ...ok, customer: { name: "홍", phone: "02-123-4567" } })).toMatchObject({ ok: false, error: "BAD_CUSTOMER" });
    expect(parseOrderRequest({ ...ok, agree: false })).toMatchObject({ ok: false, error: "NOT_AGREED" });
  });

  it("받는 분 정보가 반쪽이면 거절한다", () => {
    expect(parseOrderRequest({ ...ok, recipient: { name: "김순자", phone: "" } })).toMatchObject({ ok: false, error: "BAD_RECIPIENT" });
  });

  it("픽업 날짜·시간 형식이 틀리면 거절한다", () => {
    expect(parseOrderRequest({ ...ok, pickup: { date: "10/22", time: "18:30" } })).toMatchObject({ ok: false, error: "BAD_PICKUP" });
    expect(parseOrderRequest({ ...ok, pickup: { date: "2026-10-22", time: "6pm" } })).toMatchObject({ ok: false, error: "BAD_PICKUP" });
  });

  it("상품 목록이 배열이 아니거나 비어 있으면 거절한다", () => {
    expect(parseOrderRequest({ ...ok, items: "x" })).toMatchObject({ ok: false, error: "BAD_ITEMS" });
    expect(parseOrderRequest({ ...ok, items: [] })).toMatchObject({ ok: false, error: "BAD_ITEMS" });
    expect(parseOrderRequest(null)).toMatchObject({ ok: false });
  });

  it("너무 긴 이름은 거절한다", () => {
    expect(parseOrderRequest({ ...ok, customer: { name: "가".repeat(31), phone: "01012345678" } })).toMatchObject({ ok: false, error: "BAD_CUSTOMER" });
  });
});

describe("normalizePhone", () => {
  it("숫자만 남기고 010 형식만 받는다", () => {
    expect(normalizePhone("010-1234-5678")).toBe("01012345678");
    expect(normalizePhone("011 123 4567")).toBe("0111234567");
    expect(normalizePhone("02-123-4567")).toBeNull();
  });
});

describe("주문번호·주문명", () => {
  it("토스 orderId 규칙(영문·숫자·-·_ 6~64자)을 지킨다", () => {
    const n = makeOrderNumber(new Date(Date.UTC(2026, 9, 21, 10, 0)), "a1b2c3d4");
    expect(n).toBe("OD-20261021-a1b2c3d4");
    expect(n).toMatch(/^[A-Za-z0-9_-]{6,64}$/);
  });
  it("여러 상품이면 '첫 상품 외 N건'", () => {
    expect(makeOrderName(["1인 저녁세트"])).toBe("1인 저녁세트");
    expect(makeOrderName(["1인 저녁세트", "잡채", "된장찌개"])).toBe("1인 저녁세트 외 2건");
  });
});
