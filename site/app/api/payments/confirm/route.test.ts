import { beforeEach, describe, expect, it, vi } from "vitest";

// DB와 토스 호출을 가짜로 바꿔, 승인 라우트의 금액 대조·상태 처리만 검사한다
const order = { id: "o1", order_name: "두부조림", total_amount: 7900, status: "pending", pickup_date: "2026-10-22", pickup_time: "18:00:00", recipient_name: null };
const updates: unknown[] = [];
const confirmPayment = vi.fn();

vi.mock("@/lib/toss", () => ({ confirmPayment: (...a: unknown[]) => confirmPayment(...a) }));
vi.mock("@/lib/supabase/admin", () => ({
  createAdminClient: () => ({
    from: () => ({
      select: () => ({ eq: () => ({ maybeSingle: async () => ({ data: { ...order } }) }) }),
      update: (v: unknown) => {
        updates.push(v);
        return { eq: () => ({ eq: async () => ({}) }) };
      },
    }),
  }),
}));

const { POST } = await import("./route");
const call = (body: unknown) => POST(new Request("http://x/api/payments/confirm", { method: "POST", body: JSON.stringify(body) }));

describe("POST /api/payments/confirm", () => {
  beforeEach(() => {
    updates.length = 0;
    confirmPayment.mockReset();
  });

  it("금액을 바꾼 요청은 토스를 부르지 않고 400으로 거절한다", async () => {
    const res = await call({ paymentKey: "pk", orderId: "OD-1", amount: 100 });
    expect(res.status).toBe(400);
    expect((await res.json()).error).toBe("AMOUNT_MISMATCH");
    expect(confirmPayment).not.toHaveBeenCalled();
    expect(updates).toEqual([]);
  });

  it("금액이 맞으면 승인 후 결제 완료로 바꾼다", async () => {
    confirmPayment.mockResolvedValue({ ok: true, approvedAt: "2026-10-21T10:00:00+09:00", method: "카드" });
    const res = await call({ paymentKey: "pk", orderId: "OD-1", amount: 7900 });
    expect(res.status).toBe(200);
    expect(await res.json()).toMatchObject({ ok: true, orderId: "OD-1", amount: 7900 });
    expect(updates).toEqual([{ status: "paid", toss_payment_key: "pk", paid_at: "2026-10-21T10:00:00+09:00" }]);
  });

  it("토스 승인이 실패하면 실패로 기록하고 400", async () => {
    confirmPayment.mockResolvedValue({ ok: false, code: "REJECT_CARD_COMPANY", message: "카드사 거절" });
    const res = await call({ paymentKey: "pk", orderId: "OD-1", amount: 7900 });
    expect(res.status).toBe(400);
    expect(updates).toEqual([{ status: "failed", memo: "REJECT_CARD_COMPANY: 카드사 거절" }]);
  });

  it("필수 값이 빠지면 400", async () => {
    expect((await call({ orderId: "OD-1", amount: 7900 })).status).toBe(400);
  });
});
