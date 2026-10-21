// 결제 승인: DB의 주문 금액과 토스가 돌려준 금액을 대조한 뒤 토스 승인 API를 부르고, 성공하면 '결제 완료'로 바꾼다.
import { NextResponse } from "next/server";
import { createAdminClient } from "@/lib/supabase/admin";
import { confirmPayment } from "@/lib/toss";

export async function POST(request: Request) {
  const body = (await request.json().catch(() => ({}))) as { paymentKey?: unknown; orderId?: unknown; amount?: unknown };
  const paymentKey = typeof body.paymentKey === "string" ? body.paymentKey : "";
  const orderId = typeof body.orderId === "string" ? body.orderId : "";
  const amount = Number(body.amount);
  if (!paymentKey || !orderId || !Number.isInteger(amount)) return NextResponse.json({ error: "BAD_REQUEST" }, { status: 400 });

  const db = createAdminClient();
  if (!db) return NextResponse.json({ error: "NOT_CONFIGURED" }, { status: 503 });

  const { data: order } = await db
    .from("orders")
    .select("id, order_name, total_amount, status, pickup_date, pickup_time, recipient_name")
    .eq("order_number", orderId)
    .maybeSingle();
  if (!order) return NextResponse.json({ error: "ORDER_NOT_FOUND" }, { status: 404 });

  const summary = { orderId, orderName: order.order_name, amount: order.total_amount, pickupDate: order.pickup_date, pickupTime: order.pickup_time, recipientName: order.recipient_name };
  if (order.status === "paid") return NextResponse.json({ ok: true, ...summary }); // 새로고침 등으로 다시 불려도 같은 결과
  if (order.status !== "pending") return NextResponse.json({ error: "ORDER_NOT_PENDING" }, { status: 409 });
  if (order.total_amount !== amount) return NextResponse.json({ error: "AMOUNT_MISMATCH" }, { status: 400 });

  const result = await confirmPayment({ paymentKey, orderId, amount });
  if (!result.ok) {
    await db.from("orders").update({ status: "failed", memo: `${result.code}: ${result.message}` }).eq("id", order.id).eq("status", "pending");
    return NextResponse.json({ error: result.code, message: result.message }, { status: 400 });
  }

  await db
    .from("orders")
    .update({ status: "paid", toss_payment_key: paymentKey, paid_at: result.approvedAt ?? new Date().toISOString() })
    .eq("id", order.id)
    .eq("status", "pending");
  return NextResponse.json({ ok: true, ...summary });
}
