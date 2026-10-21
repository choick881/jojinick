// 주문 만들기: 금액은 서버가 DB 가격으로 다시 계산하고, 픽업 시간 마감·정원을 검사한 뒤 '결제 대기' 주문을 저장한다.
import { NextResponse } from "next/server";
import { makeOrderName, makeOrderNumber, parseOrderRequest } from "@/lib/order";
import { priceCart } from "@/lib/price";
import { isSlotOpen } from "@/lib/slots";
import { createAdminClient } from "@/lib/supabase/admin";

const PENDING_HOLD_MINUTES = 30; // 결제 대기 주문이 정원을 잡아 두는 시간

const fail = (error: string, status = 400) => NextResponse.json({ error }, { status });

export async function POST(request: Request) {
  const parsed = parseOrderRequest(await request.json().catch(() => null));
  if (!parsed.ok) return fail(parsed.error);
  const { items, customer, recipient, pickup } = parsed.value;

  const db = createAdminClient();
  if (!db) return fail("NOT_CONFIGURED", 503);

  const { data: products, error: productError } = await db
    .from("products")
    .select("id, slug, name, price, sold_out")
    .eq("is_active", true)
    .in("slug", items.map((i) => i.slug));
  if (productError) return fail("SERVER", 500);

  const priced = priceCart(items, (products ?? []).map((p) => ({ slug: p.slug, name: p.name, price: p.price, soldOut: p.sold_out })));
  if (!priced.ok) return fail(priced.error);

  const now = new Date();
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

  const orderNumber = makeOrderNumber(now, crypto.randomUUID());
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
  if (orderError || !order) return fail("SERVER", 500);

  const idBySlug = new Map((products ?? []).map((p) => [p.slug, p.id]));
  const { error: itemsError } = await db.from("order_items").insert(
    priced.lines.map((l) => ({ order_id: order.id, product_id: idBySlug.get(l.slug)!, product_name: l.name, unit_price: l.unitPrice, quantity: l.qty })),
  );
  if (itemsError) {
    await db.from("orders").delete().eq("id", order.id);
    return fail("SERVER", 500);
  }

  return NextResponse.json({ orderId: orderNumber, orderName, amount: priced.total, customerName: customer.name, customerMobilePhone: customer.phone });
}
