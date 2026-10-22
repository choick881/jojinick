import "server-only";
// 사이트 서버(Vercel) → Supabase 함수 "orders" 호출. 공개(publishable) 키만 쓰므로 Vercel에 비밀 키가 필요 없다.
import { NextResponse } from "next/server";
import { SUPABASE_PUBLISHABLE_KEY, SUPABASE_URL } from "../supabase-config";

export type OrdersAction = "create" | "confirm" | "health" | "register-admin";

export async function invokeOrders(action: OrdersAction, payload?: unknown): Promise<{ status: number; body: Record<string, unknown> }> {
  try {
    const res = await fetch(`${SUPABASE_URL}/functions/v1/orders`, {
      method: "POST",
      headers: { apikey: SUPABASE_PUBLISHABLE_KEY, "Content-Type": "application/json" },
      body: JSON.stringify({ action, payload }),
      signal: AbortSignal.timeout(20_000),
    });
    return { status: res.status, body: await res.json().catch(() => ({ error: "SERVER" })) };
  } catch (e) {
    console.error(`[orders:${action}] Supabase 함수 호출 실패:`, (e as Error).message);
    return { status: 502, body: { error: "SERVER" } };
  }
}

/** API 라우트용: 함수의 응답을 그대로 돌려준다 */
export async function callOrders(action: OrdersAction, payload?: unknown): Promise<NextResponse> {
  const { status, body } = await invokeOrders(action, payload);
  return NextResponse.json(body, { status });
}
