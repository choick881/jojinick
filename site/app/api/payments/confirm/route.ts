// 결제 승인: 금액 대조·토스 승인·결제 완료 기록은 Supabase 함수 "orders"(lib/order-service.ts)가 한다.
import { callOrders } from "@/lib/supabase/functions";

export async function POST(request: Request) {
  return callOrders("confirm", await request.json().catch(() => null));
}
