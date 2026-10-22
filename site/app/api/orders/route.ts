// 주문 만들기: 실제 처리(DB 가격 재계산·픽업 마감·정원 검사·저장)는 Supabase 함수 "orders"(lib/order-service.ts)가 한다.
import { callOrders } from "@/lib/supabase/functions";

export async function POST(request: Request) {
  return callOrders("create", await request.json().catch(() => null));
}
