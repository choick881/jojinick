// 점검용: 주문 DB에 접속되는지만 알려 준다(키 값·데이터는 돌려주지 않음).
import { connection } from "next/server";
import { callOrders } from "@/lib/supabase/functions";

export async function GET() {
  await connection();
  return callOrders("health");
}
