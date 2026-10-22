// 주문 만들기: 실제 처리(DB 가격 재계산·픽업 마감·정원 검사·저장)는 Supabase 함수 "orders"(lib/order-service.ts)가 한다.
import { NextResponse } from "next/server";
import { ORDERING_OPEN } from "@/lib/site";
import { callOrders } from "@/lib/supabase/functions";

export async function POST(request: Request) {
  if (!ORDERING_OPEN) return NextResponse.json({ error: "NOT_OPEN" }, { status: 503 }); // 오픈 준비 중(운영 배포)
  return callOrders("create", await request.json().catch(() => null));
}
