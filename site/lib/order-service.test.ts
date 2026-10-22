import type { SupabaseClient } from "@supabase/supabase-js";
import { describe, expect, it, vi } from "vitest";
import { checkHealth, confirmOrder, createOrder, registerAdmin } from "./order-service";

// 가짜 DB: 어떤 표에 어떤 호출을 했는지 기록하고, handler가 돌려준 값을 결과로 준다
type Query = { table: string; ops: [string, unknown[]][] };
function fakeDb(handler: (q: Query) => unknown) {
  const queries: Query[] = [];
  const from = (table: string) => {
    const q: Query = { table, ops: [] };
    queries.push(q);
    const chain: unknown = new Proxy(
      {},
      {
        get(_, prop: string) {
          if (prop === "then") return (ok: (v: unknown) => void, bad: (e: unknown) => void) => Promise.resolve(handler(q)).then(ok, bad);
          return (...args: unknown[]) => {
            q.ops.push([prop, args]);
            return chain;
          };
        },
      },
    );
    return chain;
  };
  return { db: { from } as unknown as SupabaseClient, queries };
}
const has = (q: Query, op: string) => q.ops.some(([o]) => o === op);
const arg = (q: Query, op: string) => q.ops.find(([o]) => o === op)?.[1][0];

describe("confirmOrder", () => {
  const order = { id: "o1", order_name: "두부조림", total_amount: 7900, status: "pending", pickup_date: "2026-10-22", pickup_time: "18:00", recipient_name: null };
  const setup = (status = "pending") => fakeDb((q) => (has(q, "update") ? {} : { data: { ...order, status } }));

  it("금액을 바꾼 요청은 토스를 부르지 않고 400으로 거절한다", async () => {
    const { db, queries } = setup();
    const confirm = vi.fn();
    const r = await confirmOrder(db, { paymentKey: "pk", orderId: "OD-1", amount: 100 }, confirm);
    expect(r).toEqual({ status: 400, body: { error: "AMOUNT_MISMATCH" } });
    expect(confirm).not.toHaveBeenCalled();
    expect(queries.some((q) => has(q, "update"))).toBe(false);
  });

  it("금액이 맞으면 승인 후 결제 완료로 바꾼다", async () => {
    const { db, queries } = setup();
    const r = await confirmOrder(db, { paymentKey: "pk", orderId: "OD-1", amount: 7900 }, async () => ({ ok: true, approvedAt: "2026-10-21T10:00:00+09:00", method: "카드" }));
    expect(r.status).toBe(200);
    expect(r.body).toMatchObject({ ok: true, orderId: "OD-1", amount: 7900 });
    expect(arg(queries.find((q) => has(q, "update"))!, "update")).toEqual({ status: "paid", toss_payment_key: "pk", paid_at: "2026-10-21T10:00:00+09:00" });
  });

  it("토스 승인이 실패하면 실패로 기록하고 400", async () => {
    const { db, queries } = setup();
    const r = await confirmOrder(db, { paymentKey: "pk", orderId: "OD-1", amount: 7900 }, async () => ({ ok: false, code: "REJECT_CARD_COMPANY", message: "카드사 거절" }));
    expect(r.status).toBe(400);
    expect(arg(queries.find((q) => has(q, "update"))!, "update")).toEqual({ status: "failed", memo: "REJECT_CARD_COMPANY: 카드사 거절" });
  });

  it("이미 결제된 주문은 다시 승인하지 않고 같은 결과", async () => {
    const { db } = setup("paid");
    const confirm = vi.fn();
    const r = await confirmOrder(db, { paymentKey: "pk", orderId: "OD-1", amount: 7900 }, confirm);
    expect(r.status).toBe(200);
    expect(confirm).not.toHaveBeenCalled();
  });

  it("필수 값이 빠지면 400", async () => {
    const { db } = setup();
    expect((await confirmOrder(db, { orderId: "OD-1", amount: 7900 }, vi.fn())).status).toBe(400);
  });
});

describe("createOrder", () => {
  const now = new Date("2026-10-22T03:00:00Z"); // 한국 12:00 → 오늘 18:00 주문 가능
  const body = { items: [{ slug: "tofu", qty: 2 }], customer: { name: "홍길동", phone: "010-1234-5678" }, pickup: { date: "2026-10-22", time: "18:00" }, agree: true };
  const handler = (opts: { soldOut?: boolean; taken?: number } = {}) => (q: Query) => {
    if (q.table === "products") return { data: [{ id: "p1", slug: "tofu", name: "두부조림", price: 7900, sold_out: Boolean(opts.soldOut) }] };
    if (q.table === "pickup_slots") return { data: { capacity: 3, is_active: true } };
    if (q.table === "orders" && has(q, "insert")) return { data: { id: "o1" } };
    if (q.table === "orders") return { count: opts.taken ?? 0 };
    return {};
  };

  it("DB 가격으로 합계를 계산해 결제 대기 주문을 저장한다", async () => {
    const { db, queries } = fakeDb(handler());
    const r = await createOrder(db, body, now, "abc123");
    expect(r.status).toBe(200);
    expect(r.body).toMatchObject({ orderId: "OD-20261022-abc123", orderName: "두부조림", amount: 15800, customerMobilePhone: "01012345678" });
    const saved = arg(queries.find((q) => q.table === "orders" && has(q, "insert"))!, "insert") as Record<string, unknown>;
    expect(saved).toMatchObject({ total_amount: 15800, pickup_time: "18:00", customer_phone: "01012345678" });
  });

  it("품절 상품이 있으면 저장하지 않는다", async () => {
    const { db, queries } = fakeDb(handler({ soldOut: true }));
    expect((await createOrder(db, body, now, "x")).body).toEqual({ error: "SOLD_OUT" });
    expect(queries.some((q) => has(q, "insert"))).toBe(false);
  });

  it("픽업 시간 정원이 차면 409", async () => {
    const { db } = fakeDb(handler({ taken: 3 }));
    expect(await createOrder(db, body, now, "x")).toEqual({ status: 409, body: { error: "SLOT_FULL" } });
  });

  it("마감된 픽업 시간은 거절", async () => {
    const { db } = fakeDb(handler());
    const late = new Date("2026-10-22T08:30:00Z"); // 한국 17:30 → 18:00 슬롯은 마감
    expect((await createOrder(db, body, late, "x")).body).toEqual({ error: "SLOT_CLOSED" });
  });

  it("잘못된 요청은 DB를 건드리지 않고 400", async () => {
    const { db, queries } = fakeDb(handler());
    expect((await createOrder(db, { items: [] }, now, "x")).status).toBe(400);
    expect(queries).toHaveLength(0);
  });
});

describe("checkHealth", () => {
  it("접속되면 ok, 안 되면 오류 코드만", async () => {
    expect((await checkHealth(fakeDb(() => ({ error: null })).db)).body).toEqual({ db: "ok" });
    expect(await checkHealth(fakeDb(() => ({ error: { code: "PGRST301", message: "비밀" } })).db)).toEqual({ status: 500, body: { db: "접속 실패", code: "PGRST301" } });
  });
});

describe("registerAdmin", () => {
  const now = new Date("2026-10-22T07:00:00Z");
  const setup = (invite: string | null, createError: { status: number; message: string } | null = null) => {
    const createUser = vi.fn(async () => ({ error: createError }));
    const { db, queries } = fakeDb((q) => (has(q, "update") ? {} : { data: invite === undefined ? null : { email: "boss@example.com", invite_expires_at: invite } }));
    (db as unknown as { auth: unknown }).auth = { admin: { createUser } };
    return { db, queries, createUser };
  };

  it("허용 목록·기한 안이면 확인된 계정을 만들고 기한을 지운다", async () => {
    const { db, queries, createUser } = setup("2026-10-23T00:00:00Z");
    expect(await registerAdmin(db, { email: " Boss@Example.com ", password: "12345678" }, now)).toEqual({ status: 200, body: { ok: true } });
    expect(createUser).toHaveBeenCalledWith({ email: "boss@example.com", password: "12345678", email_confirm: true });
    expect(arg(queries.find((q) => has(q, "update"))!, "update")).toEqual({ invite_expires_at: null });
  });

  it("기한이 지났거나 없으면 403, 계정을 만들지 않는다", async () => {
    for (const invite of ["2026-10-22T06:00:00Z", null]) {
      const { db, createUser } = setup(invite);
      expect((await registerAdmin(db, { email: "boss@example.com", password: "12345678" }, now)).status).toBe(403);
      expect(createUser).not.toHaveBeenCalled();
    }
  });

  it("짧은 비밀번호·이미 있는 계정", async () => {
    expect((await registerAdmin(setup("2026-10-23T00:00:00Z").db, { email: "boss@example.com", password: "123" }, now)).body).toEqual({ error: "WEAK_PASSWORD" });
    const taken = setup("2026-10-23T00:00:00Z", { status: 422, message: "already registered" });
    expect(await registerAdmin(taken.db, { email: "boss@example.com", password: "12345678" }, now)).toEqual({ status: 409, body: { error: "ALREADY_REGISTERED" } });
  });
});
