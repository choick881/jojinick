// 주문 저장·결제 승인의 실제 처리. Supabase Edge Function(supabase/functions/orders)이 비밀 키로 만든 DB 클라이언트를 넘겨 부른다.
// 비밀 키는 Supabase 안에서만 쓰이므로 Vercel에는 비밀 키가 필요 없다. 네트워크·시계는 인자로 받아 테스트할 수 있다.
import type { SupabaseClient } from "@supabase/supabase-js";
import { makeOrderName, makeOrderNumber, parseOrderRequest } from "./order";
import { priceCart } from "./price";
import { isSlotOpen } from "./slots";
import type { ConfirmInput, ConfirmResult } from "./toss";

export type ServiceResult = { status: number; body: Record<string, unknown> };

const PENDING_HOLD_MINUTES = 30; // 결제 대기 주문이 정원을 잡아 두는 시간

const fail = (error: string, status = 400, extra: Record<string, unknown> = {}): ServiceResult => ({ status, body: { error, ...extra } });

/** 금액은 DB 가격으로 다시 계산하고, 픽업 마감·정원을 검사한 뒤 '결제 대기' 주문을 저장한다 */
export async function createOrder(db: SupabaseClient, raw: unknown, now: Date, randomId: string): Promise<ServiceResult> {
  const parsed = parseOrderRequest(raw);
  if (!parsed.ok) return fail(parsed.error);
  const { items, customer, recipient, pickup } = parsed.value;

  const { data: products, error: productError } = await db
    .from("products")
    .select("id, slug, name, price, sold_out")
    .eq("is_active", true)
    .in("slug", items.map((i) => i.slug));
  if (productError) {
    console.error("[orders] 상품 조회 실패:", productError.code, productError.message);
    return fail("SERVER", 500);
  }

  const priced = priceCart(items, (products ?? []).map((p) => ({ slug: p.slug, name: p.name, price: p.price, soldOut: p.sold_out })));
  if (!priced.ok) return fail(priced.error);

  if (!isSlotOpen(pickup.date, pickup.time, now)) return fail("SLOT_CLOSED");

  const { data: slot } = await db.from("pickup_slots").select("capacity, is_active").eq("time", pickup.time).maybeSingle();
  if (!slot?.is_active) return fail("SLOT_CLOSED");
  const holdSince = new Date(now.getTime() - PENDING_HOLD_MINUTES * 60_000).toISOString();
  const { count } = await db
    .from("orders")
    .select("id", { count: "exact", head: true })
    .eq("pickup_date", pickup.date)
    .eq("pickup_time", pickup.time)
    .or(`status.in.(paid,picked_up),and(status.eq.pending,created_at.gte.${holdSince})`);
  if ((count ?? 0) >= slot.capacity) return fail("SLOT_FULL", 409);

  const orderNumber = makeOrderNumber(now, randomId);
  const orderName = makeOrderName(priced.lines.map((l) => l.name));
  const { data: order, error: orderError } = await db
    .from("orders")
    .insert({
      order_number: orderNumber,
      order_name: orderName,
      customer_name: customer.name,
      customer_phone: customer.phone,
      recipient_name: recipient?.name ?? null,
      recipient_phone: recipient?.phone ?? null,
      fulfillment_type: "pickup",
      pickup_date: pickup.date,
      pickup_time: pickup.time,
      total_amount: priced.total,
    })
    .select("id")
    .single();
  if (orderError || !order) {
    console.error("[orders] 주문 저장 실패:", orderError?.code, orderError?.message);
    return fail("SERVER", 500);
  }

  const idBySlug = new Map((products ?? []).map((p) => [p.slug, p.id]));
  const { error: itemsError } = await db.from("order_items").insert(
    priced.lines.map((l) => ({ order_id: order.id, product_id: idBySlug.get(l.slug)!, product_name: l.name, unit_price: l.unitPrice, quantity: l.qty })),
  );
  if (itemsError) {
    console.error("[orders] 주문 상품 저장 실패:", itemsError.code, itemsError.message);
    await db.from("orders").delete().eq("id", order.id);
    return fail("SERVER", 500);
  }

  return { status: 200, body: { orderId: orderNumber, orderName, amount: priced.total, customerName: customer.name, customerMobilePhone: customer.phone } };
}

/** DB의 주문 금액과 토스가 돌려준 금액을 대조한 뒤 승인하고, 성공하면 '결제 완료'로 바꾼다 */
export async function confirmOrder(db: SupabaseClient, raw: unknown, confirm: (input: ConfirmInput) => Promise<ConfirmResult>): Promise<ServiceResult> {
  const b = (raw ?? {}) as { paymentKey?: unknown; orderId?: unknown; amount?: unknown };
  const paymentKey = typeof b.paymentKey === "string" ? b.paymentKey : "";
  const orderId = typeof b.orderId === "string" ? b.orderId : "";
  const amount = Number(b.amount);
  if (!paymentKey || !orderId || !Number.isInteger(amount)) return fail("BAD_REQUEST");

  const { data: order } = await db
    .from("orders")
    .select("id, order_name, total_amount, status, pickup_date, pickup_time, recipient_name")
    .eq("order_number", orderId)
    .maybeSingle();
  if (!order) return fail("ORDER_NOT_FOUND", 404);

  const summary = { orderId, orderName: order.order_name, amount: order.total_amount, pickupDate: order.pickup_date, pickupTime: order.pickup_time, recipientName: order.recipient_name };
  if (order.status === "paid") return { status: 200, body: { ok: true, ...summary } }; // 새로고침 등으로 다시 불려도 같은 결과
  if (order.status !== "pending") return fail("ORDER_NOT_PENDING", 409);
  if (order.total_amount !== amount) return fail("AMOUNT_MISMATCH");

  const result = await confirm({ paymentKey, orderId, amount });
  if (!result.ok) {
    await db.from("orders").update({ status: "failed", memo: `${result.code}: ${result.message}` }).eq("id", order.id).eq("status", "pending");
    return fail(result.code, 400, { message: result.message });
  }

  await db
    .from("orders")
    .update({ status: "paid", toss_payment_key: paymentKey, paid_at: result.approvedAt ?? new Date().toISOString() })
    .eq("id", order.id)
    .eq("status", "pending");
  return { status: 200, body: { ok: true, ...summary } };
}

/** 관리자 처음 등록: 허용 목록에 있고 등록 기한(invite_expires_at)이 남은 이메일만 계정을 만든다. 한 번 쓰면 기한을 지운다 */
export async function registerAdmin(db: SupabaseClient, raw: unknown, now: Date): Promise<ServiceResult> {
  const b = (raw ?? {}) as { email?: unknown; password?: unknown };
  const email = String(b.email ?? "").trim().toLowerCase();
  const password = String(b.password ?? "");
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return fail("BAD_EMAIL");
  if (password.length < 8) return fail("WEAK_PASSWORD");

  const { data: invite } = await db.from("admin_users").select("email, invite_expires_at").eq("email", email).maybeSingle();
  const expires = invite?.invite_expires_at ? new Date(invite.invite_expires_at) : null;
  if (!expires || expires <= now) return fail("NOT_INVITED", 403);

  const { error } = await db.auth.admin.createUser({ email, password, email_confirm: true });
  if (error) {
    console.error("[orders] 관리자 등록 실패:", error.status, error.message);
    return fail(error.status === 422 ? "ALREADY_REGISTERED" : "SERVER", error.status === 422 ? 409 : 500);
  }
  await db.from("admin_users").update({ invite_expires_at: null }).eq("email", email);
  return { status: 200, body: { ok: true } };
}

/** 점검: 주문 DB에 접속되는지만 알려 준다 */
export async function checkHealth(db: SupabaseClient): Promise<ServiceResult> {
  const { error } = await db.from("orders").select("id", { head: true, count: "exact" }).limit(1);
  if (error) return { status: 500, body: { db: "접속 실패", code: error.code ?? null } };
  return { status: 200, body: { db: "ok" } };
}
